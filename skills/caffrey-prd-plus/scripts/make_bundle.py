#!/usr/bin/env python3
"""把 PRD 全包目录检查、补全并打成压缩包。只依赖 Python 标准库；SVG 转 PNG 时按顺序尝试 cairosvg、rsvg-convert、Playwright。

用法：python3 make_bundle.py <全包目录> [--no-zip]

全包目录结构：
  <全包目录>/
    pages/01-xxx.md          Wiki 页面，按文件名顺序排列；pages/01-xxx/ 子目录中的 md 是 01-xxx 的子页面
    images/xxx.svg|png       线框图；正文用 ![说明](../images/xxx.png) 引用
脚本会：
  1. 检查正文引用的图片：缺 PNG 但有同名 SVG 时转成 PNG；仍缺失的列出来。
  2. 生成 manifest.yaml（Wiki 层级、页面标题、图片清单）。
  3. 复制导入说明 IMPORT.md（已存在则保留）。
  4. 打成 <全包目录>.zip。
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)')
HERE = Path(__file__).resolve().parent


def svg_to_png(svg: Path, png: Path) -> str:
    """返回使用的转换方式；都失败时返回空字符串。"""
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=None, scale=2)
        return 'cairosvg'
    except Exception:
        pass
    if shutil.which('rsvg-convert'):
        r = subprocess.run(['rsvg-convert', '-z', '2', '-o', str(png), str(svg)], capture_output=True)
        if r.returncode == 0:
            return 'rsvg-convert'
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        text = svg.read_text(encoding='utf-8')
        m = re.search(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', text)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (375, 812)
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
            page.goto(svg.resolve().as_uri())
            page.screenshot(path=str(png), omit_background=False)
            b.close()
        return 'playwright'
    except Exception:
        pass
    return ''


def title_of(md: Path) -> str:
    for line in md.read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return re.sub(r'^\d+-', '', md.stem)


def q(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def collect_pages(root: Path, folder: Path, depth: int, out: list):
    for md in sorted(folder.glob('*.md')):
        out.append((depth, md))
        sub = folder / md.stem
        if sub.is_dir():
            collect_pages(root, sub, depth + 1, out)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).resolve()
    make_zip = '--no-zip' not in sys.argv
    pages_dir = root / 'pages'
    if not pages_dir.is_dir():
        sys.exit(f'找不到 {pages_dir}，请把 PRD 放在 pages/ 下')

    pages: list = []
    collect_pages(root, pages_dir, 0, pages)
    if not pages:
        sys.exit('pages/ 下没有 md 文件')

    images, missing, converted, failed = [], [], [], []
    for _, md in pages:
        for alt, ref in IMG_RE.findall(md.read_text(encoding='utf-8')):
            if re.match(r'^[a-z]+://', ref):
                continue
            target = (md.parent / ref).resolve()
            if not target.exists() and target.suffix.lower() == '.png':
                svg = target.with_suffix('.svg')
                if svg.exists():
                    how = svg_to_png(svg, target)
                    (converted if how else failed).append((svg.relative_to(root).as_posix(), how))
            if target.exists():
                images.append((target.relative_to(root).as_posix(), alt, md.relative_to(root).as_posix()))
            else:
                missing.append((md.relative_to(root).as_posix(), ref))

    referenced = {i[0] for i in images}
    unused = [p.relative_to(root).as_posix() for p in sorted((root / 'images').glob('*.png'))
              if p.relative_to(root).as_posix() not in referenced] if (root / 'images').is_dir() else []

    lines = ['# 由 make_bundle.py 生成。导入飞书 Wiki 时按 wiki 的层级和顺序创建节点，说明见 IMPORT.md',
             f'bundle: {q(root.name)}', 'wiki:']
    for depth, md in pages:
        ind = '  ' * (depth + 1)
        lines += [f'{ind}- title: {q(title_of(md))}', f'{ind}  file: {q(md.relative_to(root).as_posix())}',
                  f'{ind}  level: {depth + 1}']
    lines.append('images:' if images else 'images: []')
    for f, alt, used in images:
        lines += [f'  - file: {q(f)}', f'    alt: {q(alt)}', f'    used_in: {q(used)}']
    (root / 'manifest.yaml').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    imp = root / 'IMPORT.md'
    tpl = HERE.parent / 'assets' / 'IMPORT.md'
    if not imp.exists() and tpl.exists():
        shutil.copy(tpl, imp)

    print(f'页面 {len(pages)} 个，图片 {len(images)} 张')
    for svg, how in converted:
        print(f'  已转换 {svg} → PNG（{how}）')
    for svg, _ in failed:
        print(f'  ✗ 无法转换 {svg}：请安装 cairosvg（pip install cairosvg）或 Playwright 后重试，或手动导出 PNG')
    for md, ref in missing:
        print(f'  ✗ {md} 引用的图片不存在：{ref}')
    for f in unused:
        print(f'  提示：{f} 没有被任何页面引用')

    if missing or failed:
        sys.exit('有缺失的图片，未打包。')
    if make_zip:
        z = root.with_suffix('.zip')
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(root.rglob('*')):
                if p.is_file() and p.name != '.DS_Store':
                    zf.write(p, Path(root.name) / p.relative_to(root))
        print(f'已打包：{z}')


if __name__ == '__main__':
    main()
