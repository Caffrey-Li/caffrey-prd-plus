#!/usr/bin/env python3
"""把技能包合并成单个提示词文件，供不支持 Skill 的聊天工具使用。

用法：python3 scripts/build_single.py
输出：dist/caffrey-prd-plus-prompt.md
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "caffrey-prd-plus"
OUT = ROOT / "dist" / "caffrey-prd-plus-prompt.md"

ORDER = [
    "references/prd-template.md",
    "references/section-matrix.md",
    "references/wireframe.md",
    "references/prototype.md",
    "references/field-spec.md",
    "references/new-product-mode.md",
    "references/product-overview-template.md",
    "references/types/_index.md",
    "references/types/*.md",
    "references/industries/_index.md",
    "references/industries/*.md",
    "references/question-bank.md",
    "references/quality-checklist.md",
    "references/change-management.md",
    "references/user-stories.md",
    "references/test-cases.md",
]

HEADER = """<!-- 本文件由 scripts/build_single.py 自动生成，请勿直接修改 -->
# caffrey-prd-plus 单文件版 v{version}

使用说明（写给 AI）：这是 caffrey-prd-plus 技能的单文件版本。下文中提到的
`references/xxx.md` 文件，都已按「=== 文件：references/xxx.md ===」的分隔标题
收录在本文件中，直接查阅对应部分即可，不需要再读取外部文件。

版本检查时，本地版本以本文件标题中的版本号为准。单文件版需要用户手动更新：
提示用户从 https://raw.githubusercontent.com/Caffrey-Li/caffrey-prd-plus/main/dist/caffrey-prd-plus-prompt.md
下载最新文件并重新上传。

"""


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip()
    return text


def collect() -> list[Path]:
    seen, files = set(), []
    for pattern in ORDER:
        for p in sorted(SKILL.glob(pattern)):
            if p not in seen:
                seen.add(p)
                files.append(p)
    return files


def main() -> None:
    version = (SKILL / "VERSION").read_text(encoding="utf-8").strip()
    parts = [HEADER.format(version=version), strip_frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))]
    for p in collect():
        rel = p.relative_to(SKILL).as_posix()
        parts.append(f"\n\n=== 文件：{rel} ===\n\n{p.read_text(encoding='utf-8')}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(parts)
    OUT.write_text(text, encoding="utf-8")
    print(f"已生成 {OUT.relative_to(ROOT)}：{len(text)} 字符")


if __name__ == "__main__":
    main()
