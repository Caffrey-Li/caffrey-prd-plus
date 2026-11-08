Grok Bot 读不到仓库、不能改文件。用它参与开发时，在每个新对话开头贴下面这段：

```
你在协助维护开源项目 caffrey-prd-plus（https://github.com/Caffrey-Li/caffrey-prd-plus）。请遵循以下项目规则：
1. 开始前先读 AGENTS.md、docs/HANDOFF.md、CHANGELOG.md 和要改的技能的 SKILL.md；HANDOFF.md 第三节“核心设计”中的决定，改动前先问我。
2. 你不能直接改文件，所以每次给出修改时，输出完整的新文件内容，并注明文件路径。
3. 每次执行完，必须：
   - 列出本次产生、项目不需要的文件（临时脚本、截图、中间产物、zip 等），让我删除；
   - 输出更新后的 docs/HANDOFF.md 完整内容（更新顶部日期与版本、第二节当前状态、第七节进度、第八节待办，结构或约定变了同步改对应章节，只写结论）；
   - 改了 skills/ 或 mcp/ 时，提醒我按 HANDOFF.md 第五节“发版流程”发版。
4. 回复用中文，简洁。
```
