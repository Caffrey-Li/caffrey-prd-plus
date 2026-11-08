你好，我要你接手维护开源项目 caffrey-prd-plus（给产品经理用的中文 PRD 技能包，含写 PRD 和执行测试两个技能）。之前由其他 Agent 开发，现在交给你继续。

先做这几件事，做完告诉我结果，不要改任何内容：

1. 准备仓库：工作目录是 `~/Projects/Caffrey-PRD/caffrey-prd-plus`（https://github.com/Caffrey-Li/caffrey-prd-plus 的 git 仓库）。先 `git pull` 到最新；不要另建克隆。
2. 读 `AGENTS.md`、`docs/HANDOFF.md`、`CHANGELOG.md`、`skills/caffrey-prd-plus/SKILL.md`、`skills/caffrey-prd-plus/references/prd-template.md`。
3. 用三五句话告诉我：当前版本、核心设计、正在进行的任务做到哪一步。
4. 检查能否 `git push` 到 main；不能的话告诉我怎么配置。
5. 跑一次检查：`python3 -m pytest -q tests`；再把 `examples/example-psych-booking.md` 中 `# 在线预约咨询师 PRD` 之后的正文放进临时目录的 `pages/01.md`，运行 `python3 skills/caffrey-prd-plus/scripts/make_bundle.py <临时目录> --no-zip`，告诉我是否通过；缺 `mmdc` 或 Playwright 时告诉我需要装什么。检查完删除临时目录。
6. 根据交接文档第七节的进度，告诉我下一步建议做什么，等我确认后再开始。

之后按 `AGENTS.md` 的规则工作：
- 交接文档“核心设计”里的决定，改动前先问我。
- 每次执行完：按需发版、删除不需要的文件、更新 `docs/HANDOFF.md`、提交推送。
- 回复用中文，简洁。
