#!/usr/bin/env python3
"""发布新版本：同步所有版本号并重新生成单文件版。

用法：python3 scripts/release.py 0.3.0
发布前先在 CHANGELOG.md 顶部写好该版本的更新内容。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "skills" / "caffrey-prd-plus" / "VERSION"
MANIFESTS = [
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".cursor-plugin" / "plugin.json",
]
CURSOR_MARKETPLACE = ROOT / ".cursor-plugin" / "marketplace.json"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("用法：python3 scripts/release.py 0.3.0")
    version = sys.argv[1]

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## v{version}" not in changelog:
        sys.exit(f"CHANGELOG.md 中没有 “## v{version}” 的更新内容，请先补上。")

    VERSION_FILE.write_text(version + "\n", encoding="utf-8")
    for path in MANIFESTS:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = version
        write_json(path, data)
    data = json.loads(CURSOR_MARKETPLACE.read_text(encoding="utf-8"))
    data.setdefault("metadata", {})["version"] = version
    write_json(CURSOR_MARKETPLACE, data)

    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_single.py")], check=True)
    print(f"已同步版本号为 v{version}。提交并推送到 GitHub 后，用户即可收到更新提示。")


if __name__ == "__main__":
    main()
