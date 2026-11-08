# AGENTS.md

本仓库是 caffrey-prd-plus：给产品经理用的中文 PRD 技能包，含 `caffrey-prd-plus`（写 PRD）和 `caffrey-test-runner`（执行测试）两个技能。

适用于 Claude、Codex、Cursor、Grok 等任何在本仓库工作的 Agent。用户电脑上唯一的工作目录是 `~/Projects/Caffrey-PRD/caffrey-prd-plus`，不要另建克隆。

## 开始前

1. 先读 `docs/HANDOFF.md`，它记录了当前版本、核心设计、发版流程和正在进行的任务。
2. `docs/HANDOFF.md` 第三节“核心设计”中的决定，改动前先问用户。
3. 临时文件放在仓库外的系统临时目录，或仓库内的 `.tmp/`（已被 `.gitignore` 忽略）。

## 规则

- 规范只维护一份，在 `skills/` 下；`dist/caffrey-prd-plus-prompt.md` 由脚本生成，不要手改。
- 改了技能内容，同步改受影响的 `examples/`。
- 与用户沟通用中文，简洁。

## 每次执行完（必做，按顺序）

1. **发版**：改了技能或 MCP 服务时，按交接文档第五节发版：写 `CHANGELOG.md`，运行 `python3 scripts/release.py X.Y.Z`，检查；只改文档或规则文件时不升版本号。
2. **清理**：删除本次执行中产生、项目不需要的文件。
   - 要删：临时脚本、测试截图、中间产物、打包出的 zip、`.tmp/`、`__pycache__/`、`.pytest_cache/`、`.DS_Store`、`node_modules/`、`test-results/`、`playwright-report/`。
   - 不能删：`skills/`、`examples/`、`dist/`、`docs/`、`scripts/`、`mcp/`、`tests/`、`.claude-plugin/`、`.cursor-plugin/`、`.cursor/`、`AGENTS.md`、`CLAUDE.md`、`README.md`、`CHANGELOG.md`、`LICENSE`、`.gitignore`。
   - 交给用户的安装包放在仓库外，告诉用户位置；拿不准的先问用户。没有删除权限时，移到 `~/Projects/Caffrey-PRD/_to_delete/` 并告诉用户。
3. **更新 `docs/HANDOFF.md`**：顶部日期、接手方和当前版本；第二节“当前状态”；第七节进度；第八节待办勾选完成项、补充新待办；结构变了改第四节；新约定写进第六节。只写结论，不写过程。
4. **提交推送**：`git status` 确认没有多余文件，再提交并推送 main。
5. **回复用户**：做了什么、当前版本、删除了哪些文件、需要用户做的事。

## 检查命令

```bash
# 渲染 Mermaid、检查链接、生成 preview.html；示例 PRD 正文放在 <目录>/pages/ 下
python3 skills/caffrey-prd-plus/scripts/make_bundle.py <目录> --no-zip

# 单元测试
python3 -m pytest -q tests
```

渲染 Mermaid 需要 `mmdc`（`npm i -g @mermaid-js/mermaid-cli`）或 Playwright，脚本会自动选择。
