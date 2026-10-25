#!/usr/bin/env bash
# 安装或更新 caffrey-prd-plus。重复运行即为更新。
# 用法：bash install.sh
# Windows 请在 Git Bash 中运行。
set -euo pipefail

REPO_URL="${CAFFREY_PRD_REPO:-https://github.com/Caffrey-Li/caffrey-prd-plus.git}"
HOME_DIR="${CAFFREY_PRD_HOME:-$HOME/.caffrey-prd-plus}"
NAME="caffrey-prd-plus"

if ! command -v git >/dev/null 2>&1; then
  echo "需要先安装 git：https://git-scm.com/downloads" >&2
  exit 1
fi

if [ -d "$HOME_DIR/.git" ]; then
  echo "更新仓库：$HOME_DIR"
  git -C "$HOME_DIR" pull --ff-only --quiet
else
  echo "下载仓库到：$HOME_DIR"
  git clone --quiet --depth 1 "$REPO_URL" "$HOME_DIR"
fi

SRC="$HOME_DIR/skills/$NAME"
VERSION="$(cat "$SRC/VERSION")"

# ~/.agents/skills 同时被 Codex、Cursor、DeepSeek Harness 读取
targets=("$HOME/.agents/skills")
[ -d "$HOME/.claude" ] && targets+=("$HOME/.claude/skills")
[ -d "$HOME/.grok" ] && targets+=("$HOME/.grok/skills")
[ -d "$HOME/.workbuddy" ] && targets+=("$HOME/.workbuddy/skills")

for dir in "${targets[@]}"; do
  dest="$dir/$NAME"
  mkdir -p "$dir"
  rm -rf "$dest"
  cp -R "$SRC" "$dest"
  echo "script" > "$dest/.install-method"
  echo "已安装到：$dest"
done

echo "caffrey-prd-plus v$VERSION 安装完成。请新开一个对话让新版本生效。"
