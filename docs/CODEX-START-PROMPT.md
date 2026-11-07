你好，我要你接手维护开源项目 caffrey-prd-plus（给产品经理用的中文 PRD 技能包，含写 PRD 和执行测试两个技能）。之前由 Claude 开发，现在交给你继续。

先做这几件事，做完告诉我结果，不要改任何内容：

1. 准备仓库：如果当前目录不是 https://github.com/Caffrey-Li/caffrey-prd-plus 的 git 仓库，就把它 clone 到 `~/Projects/Caffrey-PRD/caffrey-prd-plus-git`。不要覆盖或删除 `~/Projects/Caffrey-PRD/` 里已有的文件。
2. 读 `AGENTS.md`、`docs/HANDOFF.md`、`CHANGELOG.md`、`skills/caffrey-prd-plus/SKILL.md`、`skills/caffrey-prd-plus/references/prd-template.md`。
3. 用三五句话告诉我：当前版本、核心设计、正在进行的任务做到哪一步。
4. 检查能否 `git push` 到 main；不能的话告诉我怎么配置。
5. 跑一次检查：把 `examples/example-psych-booking.md` 中 `# 在线预约咨询师 PRD` 之后的正文放进临时目录的 `pages/01.md`，运行 `python3 skills/caffrey-prd-plus/scripts/make_bundle.py <临时目录> --no-zip`，告诉我是否通过；缺 `mmdc` 或 Playwright 时告诉我需要装什么。
6. 交接文档第七节是正在进行的“插件化”任务：保留现有技能，新增 MCP 服务，让各个 Agent 接入。用几句话复述方案，然后问我第七节末尾“待用户回答”的问题，等我回答后再开始做。

之后的工作规则：
- 交接文档“核心设计”里的决定，改动前先问我。
- 每次改完按交接文档的“发版流程”发版、推送，并更新 `docs/HANDOFF.md`。
- 回复用中文，简洁。
