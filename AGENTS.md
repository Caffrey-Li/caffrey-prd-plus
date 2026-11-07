# AGENTS.md

本仓库是 caffrey-prd-plus：给产品经理用的中文 PRD 技能包，含 `caffrey-prd-plus`（写 PRD）和 `caffrey-test-runner`（执行测试）两个技能。

开始任何工作前先读 `docs/HANDOFF.md`，它记录了当前版本、核心设计、发版流程和正在进行的任务。

## 规则

- `docs/HANDOFF.md` 第三节“核心设计”中的决定，改动前先问用户。
- 规范只维护一份，在 `skills/` 下；`dist/caffrey-prd-plus-prompt.md` 由脚本生成，不要手改。
- 改了技能内容，同步改受影响的 `examples/`。
- 每次改完按交接文档第五节发版：写 `CHANGELOG.md`，运行 `python3 scripts/release.py X.Y.Z`，检查后提交推送，并更新 `docs/HANDOFF.md`。
- 与用户沟通用中文，简洁。

## 检查命令

```bash
# 渲染 Mermaid、检查链接、生成 preview.html；示例 PRD 正文放在 <目录>/pages/ 下
python3 skills/caffrey-prd-plus/scripts/make_bundle.py <目录> --no-zip
```

渲染 Mermaid 需要 `mmdc`（`npm i -g @mermaid-js/mermaid-cli`）或 Playwright，脚本会自动选择。
