# 安装说明

本工具的主格式是开放的 Agent Skills 格式（一个包含 `SKILL.md` 的文件夹），Claude、Codex、Cursor、Grok 都能直接识别。不支持 Skill 的聊天工具使用 `dist/` 下的单文件提示词。

技能文件夹位于仓库的 `skills/caffrey-prd-plus/`，下文简称“技能文件夹”。

## 先下载仓库

```bash
git clone https://github.com/<你的用户名>/caffrey-prd-plus.git
cd caffrey-prd-plus
```

## Claude

**Claude Code**

```bash
# 所有项目可用
mkdir -p ~/.claude/skills && cp -r skills/caffrey-prd-plus ~/.claude/skills/
# 或只在当前项目可用
mkdir -p .claude/skills && cp -r skills/caffrey-prd-plus .claude/skills/
```

**Claude 网页版 / 桌面版**：把技能文件夹压缩成 zip，在设置的 Skills 管理处上传。

## Codex

Codex 读取 `.agents/skills` 目录。

```bash
# 所有项目可用
mkdir -p ~/.agents/skills && cp -r skills/caffrey-prd-plus ~/.agents/skills/
# 或只在当前仓库可用
mkdir -p .agents/skills && cp -r skills/caffrey-prd-plus .agents/skills/
```

## Cursor

Cursor 读取 `~/.cursor/skills`、`~/.agents/skills`，并兼容 `~/.claude/skills` 和 `~/.codex/skills`。已按上文给 Claude 或 Codex 安装过的，不需要重复安装。

```bash
mkdir -p ~/.cursor/skills && cp -r skills/caffrey-prd-plus ~/.cursor/skills/
```

## Grok

**Grok Build（命令行）**

```bash
mkdir -p ~/.grok/skills && cp -r skills/caffrey-prd-plus ~/.grok/skills/
```

**Grok Bot**（待实测）

Grok Bot 支持在对话中让 Bot 把一套流程保存为私有技能。建议做法：

1. 把 `dist/caffrey-prd-plus-prompt.md` 发给 Bot。
2. 说：“请把这份文件完整保存为一个名为 caffrey-prd-plus 的私有技能，以后我说写 PRD、整理需求时使用它。”
3. 在 Bot 的 Connect apps → Private skills 中确认该技能已对当前 Bot 启用。

如果 Grok Bot 后续开放了技能包安装入口，直接安装技能文件夹即可。

## 其他工具（ChatGPT、Gemini、Kimi、豆包等）

使用单文件版 `dist/caffrey-prd-plus-prompt.md`（约 3 万字）：

- 支持“知识库 / 文件”的自定义助手（如 GPTs、Gems）：上传该文件，在指令中写“按照知识库中的 caffrey-prd-plus 文件工作”。
- 普通对话：开始时上传该文件，说“请按这个文件的规则帮我写 PRD”。

## 通用安装工具（可选）

也可以使用社区的 skills 命令行工具，一次安装到多个 agent：

```bash
npx skills add <你的用户名>/caffrey-prd-plus
```

## 更新单文件版

修改了技能文件夹的内容后，重新生成单文件版：

```bash
python3 scripts/build_single.py
```
