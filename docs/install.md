# 安装与更新

本工具的主格式是开放的 Agent Skills 格式（一个包含 `SKILL.md` 的文件夹），Claude、Codex、Cursor、DeepSeek Harness、Grok、WorkBuddy 都能直接识别。不支持 Skill 的聊天工具使用 `dist/` 下的单文件版。

仓库包含两个技能：`caffrey-prd-plus`（写 PRD）和 `caffrey-test-runner`（执行测试）。一键脚本和插件会同时安装两个；单文件版只包含 `caffrey-prd-plus`。

**每个工具只选一种安装方式**，否则同一个工具里可能出现两个同名技能。

| 安装方式 | 适用工具 | 怎么更新 |
| --- | --- | --- |
| 一键脚本（推荐） | Claude Code、Codex、Cursor、DeepSeek Harness、Grok Build、WorkBuddy | 使用时有新版会提示，回复“更新 PRD 技能”即可 |
| WorkBuddy 技能管理导入 | WorkBuddy | 在技能管理中重新导入 |
| Claude Code 插件 | Claude Code | `/plugin marketplace update caffrey-prd-plus`，或开启自动更新 |
| Cursor 插件 | Cursor | 在 Customize 中更新插件 |
| 手动复制 | 所有支持 Skill 的工具 | 重新复制 |
| 单文件版 | Grok Bot、ChatGPT、Gemini 等 | 使用时有新版会提示，重新下载上传 |

## 一键脚本（推荐）

需要电脑上装有 git。在终端运行：

```bash
curl -fsSL https://raw.githubusercontent.com/Caffrey-Li/caffrey-prd-plus/main/scripts/install.sh | bash
```

脚本会把仓库下载到 `~/.caffrey-prd-plus`，再把技能复制到：

- `~/.agents/skills/`：Codex、Cursor、DeepSeek Harness 共用
- `~/.claude/skills/`：电脑上装了 Claude Code 时
- `~/.grok/skills/`：电脑上装了 Grok Build 时
- `~/.workbuddy/skills/`：电脑上装了 WorkBuddy 时

**更新**：再运行一次同样的命令，或者在使用技能时看到新版本提示后回复“更新 PRD 技能”，agent 会征得你同意后执行 `bash ~/.caffrey-prd-plus/scripts/install.sh`。更新后新开一个对话生效。

Windows 用户请在 Git Bash 中运行。

## Claude Code 插件

在 Claude Code 对话中依次运行：

```
/plugin marketplace add Caffrey-Li/caffrey-prd-plus
/plugin install caffrey-prd-plus@caffrey-prd-plus
```

**自动更新**：运行 `/plugin`，进入 **Marketplaces**，选中 caffrey-prd-plus，选择 **Enable auto-update**。不开自动更新时，用 `/plugin marketplace update caffrey-prd-plus` 手动更新。

插件方式安装后，技能名为 `caffrey-prd-plus:caffrey-prd-plus`，直接说“帮我写个 PRD”即可触发。

**Claude 网页版 / 桌面版**：把 `skills/` 下的每个技能文件夹分别压缩成 zip，在设置的 Skills 管理处逐个上传。更新时重新上传。

## Cursor 插件

1. 打开 Cursor 的 **Customize**（自定义）页面，选择导入插件 **From GitHub Repository**。
2. 填入 `https://github.com/Caffrey-Li/caffrey-prd-plus`。
3. 在插件列表中安装 **caffrey-prd-plus**，技能会出现在 Customize 的技能列表中。

安装后在 Agent 对话中说“帮我写个 PRD：……”即可触发，也可以输入 `/caffrey-prd-plus` 手动调用。

## 手动复制

先下载仓库：

```bash
git clone https://github.com/Caffrey-Li/caffrey-prd-plus.git
cd caffrey-prd-plus
```

再按工具复制 `skills/` 下的技能文件夹（下面的命令会同时复制写 PRD 和执行测试两个技能）：

| 工具 | 命令 |
| --- | --- |
| Claude Code | `mkdir -p ~/.claude/skills && cp -r skills/* ~/.claude/skills/` |
| Codex | `mkdir -p ~/.agents/skills && cp -r skills/* ~/.agents/skills/` |
| Cursor | `mkdir -p ~/.cursor/skills && cp -r skills/* ~/.cursor/skills/` |
| DeepSeek Harness | `mkdir -p ~/.dsh/skills && cp -r skills/* ~/.dsh/skills/` |
| Grok Build | `mkdir -p ~/.grok/skills && cp -r skills/* ~/.grok/skills/` |
| WorkBuddy | `mkdir -p ~/.workbuddy/skills && cp -r skills/* ~/.workbuddy/skills/` |

只想在某个项目里使用时，把 `~/` 换成项目根目录下的同名路径，例如 `.claude/skills/`、`.agents/skills/`。

**各工具读取的目录**

- Codex：`~/.agents/skills/`，以及仓库内的 `.agents/skills/`。
- Cursor：`~/.cursor/skills/`、`~/.agents/skills/`，并兼容 `~/.claude/skills/`、`~/.codex/skills/`。
- DeepSeek Harness：按优先级依次为 `<项目根>/.dsh/skills/`、`<项目根>/.agents/skills/`、`~/.dsh/skills/`、`~/.agents/skills/`。项目根是包含 `.git` 的最近一级目录；技能文件夹必须直接放在这些目录下，不能多套一层；修改后自动热加载。

## WorkBuddy（待实测）

WorkBuddy 使用同样的 `SKILL.md` 技能格式，任选一种方式：

1. **一键脚本**：电脑上装了 WorkBuddy（存在 `~/.workbuddy` 目录）时，一键脚本会自动复制到 `~/.workbuddy/skills/caffrey-prd-plus/`。
2. **技能管理导入**：在 WorkBuddy 的【技能管理】中选择“通过 URL 导入”，填入技能文件夹地址 `https://github.com/Caffrey-Li/caffrey-prd-plus/tree/main/skills/caffrey-prd-plus`；如果提示找不到技能，改填仓库地址 `https://github.com/Caffrey-Li/caffrey-prd-plus`。
3. **手动复制**：见上方「手动复制」表格中的 WorkBuddy 一行。只想在某个项目中使用时，复制到项目下的 `.workbuddy/skills/`。

装好后在【技能管理】中确认 caffrey-prd-plus 已启用，新开一个对话，说“帮我写个 PRD：……”即可触发。WorkBuddy 能写文件，说“出原型图”时会直接生成 HTML 文件。

## Grok Bot（待实测）

Grok Bot 支持在对话中让 Bot 把一套流程保存为私有技能：

1. 把 `dist/caffrey-prd-plus-prompt.md` 发给 Bot。
2. 说：“请把这份文件完整保存为一个名为 caffrey-prd-plus 的私有技能，以后我说写 PRD、整理需求时使用它。”
3. 在 Bot 的 Connect apps → Private skills 中确认该技能已对当前 Bot 启用。

## 其他聊天工具（ChatGPT、Gemini、Kimi、豆包等）

使用单文件版 [`dist/caffrey-prd-plus-prompt.md`](https://raw.githubusercontent.com/Caffrey-Li/caffrey-prd-plus/main/dist/caffrey-prd-plus-prompt.md)（约 3.7 万字）：

- 支持“知识库 / 文件”的自定义助手（如 GPTs、Gems）：上传该文件，在指令中写“按照知识库中的 caffrey-prd-plus 文件工作”。
- 普通对话：开始时上传该文件，说“请按这个文件的规则帮我写 PRD”。

**更新**：能联网的工具在使用时会提示新版本，按提示重新下载并上传即可。

## 执行测试需要的工具

`caffrey-test-runner` 需要能操作被测系统的工具，Web 端任选其一：

- **Playwright MCP**（推荐，可批量执行、保存截图）：Claude Code 运行 `claude mcp add playwright npx @playwright/mcp@latest`；Codex 运行 `codex mcp add playwright npx "@playwright/mcp@latest"`；Cursor 在 Settings → MCP 中添加命令 `npx @playwright/mcp@latest`。需要电脑上装有 Node.js。
- **Claude in Chrome**：用你自己的 Chrome 和登录状态。
- **Claude 桌面版内置浏览器**。

App、Mac / Windows 应用、小程序的准备方式见 `skills/caffrey-test-runner/references/` 下对应的指南。

**试跑**：打开 `examples/demo/demo-test-cases.yaml`，把 ENTRY 改成你电脑上 `examples/demo/lite-filter-demo.html` 的完整地址（如 `file:///Users/你的用户名/.../lite-filter-demo.html`），对 agent 说“用 caffrey-test-runner 执行这个文件”。

## 维护者：发布新版本

1. 修改技能内容。
2. 在 `CHANGELOG.md` 顶部写上新版本的更新内容，例如 `## v0.3.0（日期）`。
3. 运行 `python3 scripts/release.py 0.3.0`：同步所有版本号并重新生成单文件版。
4. 提交并推送到 GitHub。用户下次使用时就会看到更新提示。
