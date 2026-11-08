#!/usr/bin/env node
// 把 Playwright 的 JSON 报告转成 caffrey-test-runner 的结果表（results.md）和结果文件（results.yaml）。
// 用法：node pw_results.js test-results/results.json [输出目录]
// 要求：test 标题以用例编号开头，并带 @优先级、@功能编号、@类型 标签，如 “TC-001 标题 @P0 @F-01 @正常”。
const fs = require('fs');
const path = require('path');

const input = process.argv[2] || 'test-results/results.json';
const outDir = process.argv[3] || path.dirname(input);
const report = JSON.parse(fs.readFileSync(input, 'utf-8'));

function envProblem(err) {
  if (/Executable doesn't exist|browserType\.launch|Failed to launch|Chromium distribution .* is not found/.test(err)) {
    return '环境问题：浏览器无法启动。运行 npx playwright install chromium，或设置 PW_CHANNEL=chrome 使用本机 Chrome';
  }
  const v = err.match(/缺少环境变量 (\w+)/);
  if (v) return `环境问题：缺少环境变量 ${v[1]}`;
  if (/net::ERR_|ECONNREFUSED|ENOTFOUND|ERR_NAME_NOT_RESOLVED/.test(err)) return '环境问题：被测地址无法访问';
  return '';
}

const rows = [];
(function walk(suite) {
  for (const spec of suite.specs || []) {
    for (const t of spec.tests || []) {
      const r = t.results[t.results.length - 1] || {};
      const tags = (spec.title.match(/@\S+/g) || []).map((s) => s.slice(1));
      const [id, ...rest] = spec.title.replace(/@\S+/g, '').trim().split(/\s+/);
      const skipNote = (t.annotations || []).find((a) => a.type === 'skip');
      let result = { passed: '通过', failed: '失败', timedOut: '失败', interrupted: '阻塞', skipped: '跳过' }[r.status] || '阻塞';
      if (result === '跳过' && skipNote && /生产/.test(skipNote.description || '')) result = '跳过（生产环境）';
      const err = (r.errors && r.errors[0] && r.errors[0].message) || '';
      const step = (r.steps || []).find((s) => s.error);
      const setupFailed = step && step.title === 'setup';
      if (setupFailed) result = '阻塞';
      // 环境问题（浏览器、环境变量、地址不可达）没有真正执行用例，记为阻塞，不算缺陷
      const envIssue = result !== '通过' && envProblem(err);
      if (envIssue) result = '阻塞';
      const shot = (r.attachments || []).find((a) => a.name === 'screenshot' && a.path);
      rows.push({
        id, title: rest.join(' '),
        feature: tags.find((x) => /^F-|^M\d+-F-/.test(x)) || '',
        priority: tags.find((x) => /^P\d$/.test(x)) || '',
        result,
        actual: result === '通过' ? '—' : envIssue || err.replace(/\u001b\[[0-9;]*m/g, '').split('\n').filter(Boolean).slice(0, 4).join('；'),
        failedAt: step ? step.title : '',
        evidence: shot ? path.relative(outDir, shot.path) : '',
      });
    }
  }
  for (const s of suite.suites || []) walk(s);
})({ suites: report.suites });

rows.sort((a, b) => a.id.localeCompare(b.id));
const count = (k) => rows.filter((r) => r.result.startsWith(k)).length;
const executed = rows.filter((r) => !r.result.startsWith('跳过')).length;
const passRate = executed ? Math.round((count('通过') / executed) * 100) : 0;
const failedFeatures = [...new Set(rows.filter((r) => r.result === '失败').map((r) => r.feature))].join('、') || '无';
const esc = (s) => String(s).replace(/\|/g, '\\|');

// 上线结论初判（规则见 references/results.md 第二节）。脚本不知道缺陷严重程度，
// 由执行 Agent 按缺陷单复核：有致命、严重缺陷时改为“不建议上线”。
const p0 = rows.filter((r) => r.priority === 'P0');
const p0Passed = p0.filter((r) => r.result === '通过').length;
const notRun = rows.filter((r) => r.result !== '通过' && r.result !== '失败');
const failed = rows.filter((r) => r.result === '失败');
let verdict;
if (p0.some((r) => r.result === '失败')) verdict = '不建议上线';
else if (p0.some((r) => r.result !== '通过')) verdict = '无法判定';
else if (failed.length || notRun.length) verdict = '有条件上线';
else verdict = '建议上线';
const verdictBasis = `P0 共 ${p0.length} 条，通过 ${p0Passed}；失败 ${failed.length} 条；未执行的用例 ${notRun.length} 条`;
const todo = [...failed.map((r) => `${r.id} 失败`), ...notRun.map((r) => `${r.id} ${r.result}`)].join('；');

const md = [
  '## 测试结果', '',
  `- 来源：Playwright 报告 ${path.basename(input)}`,
  `- 执行时间：${report.stats && report.stats.startTime ? report.stats.startTime : ''}`, '',
  `**上线结论（初判，待按缺陷严重程度复核）：${verdict}**`,
  `- 依据：${verdictBasis}`,
  ...(todo ? [`- 上线前要确认：${todo}`] : []), '',
  '| 用例编号 | 关联功能 | 优先级 | 结果 | 实际结果 | 证据 | 备注 |',
  '| --- | --- | --- | --- | --- | --- | --- |',
  ...rows.map((r) => `| ${r.id} | ${r.feature} | ${r.priority} | ${r.result} | ${esc(r.actual)} | ${r.evidence || '—'} | ${r.failedAt && r.result !== '通过' ? '失败于 ' + r.failedAt : ''} |`),
  '',
  `统计：共 ${rows.length} 条，通过 ${count('通过')} / 失败 ${count('失败')} / 阻塞 ${count('阻塞')} / 需人工 0 / 跳过 ${count('跳过')}，通过率 ${passRate}%（通过 ÷ 已执行）`,
  `失败涉及的功能：${failedFeatures}`, '',
].join('\n');

const yaml = [
  `source: ${path.basename(input)}`,
  `verdict: ${verdict}`,
  `verdict_basis: ${JSON.stringify(verdictBasis)}`,
  'results:',
  ...rows.flatMap((r) => [
    `  - id: ${r.id}`,
    `    result: ${r.result}`,
    ...(r.result === '通过' ? [] : [`    failed_at: ${r.failedAt || '—'}`, `    actual: ${JSON.stringify(r.actual)}`, `    evidence: ${JSON.stringify(r.evidence)}`]),
  ]),
  '',
].join('\n');

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'results.md'), md);
fs.writeFileSync(path.join(outDir, 'results.yaml'), yaml);
console.log(md);
