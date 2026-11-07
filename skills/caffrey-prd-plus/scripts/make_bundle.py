#!/usr/bin/env python3
"""检查并打包 PRD 全包。只依赖 Python 标准库；画图时调用本机已有的工具。

用法：python3 make_bundle.py <全包目录> [--no-zip]

全包目录：
  pages/01-xxx.md     Wiki 页面，按文件名排序；pages/01-xxx/ 下的 md 是子页面
  images/xxx.svg      线框图，正文用 ![说明](../images/xxx.png) 引用

脚本会：
  1. 线框图 SVG 转 PNG。
  2. 把正文中的 mermaid 代码块渲染成 images/diagram-页面序号-图序号.png。
  3. 检查图片引用和编号链接 [R-01](#R-01) 是否都能找到。
  4. 生成 preview.html：自包含，链接可跳转，悬停显示目标内容，跳转后可返回。
  5. 生成 manifest.yaml，复制 IMPORT.md，打成同名 zip。

转图工具按顺序尝试：SVG 用 cairosvg、rsvg-convert、Playwright；Mermaid 用 mmdc、npx @mermaid-js/mermaid-cli、Playwright 加 Mermaid CDN。
"""
import base64
import html
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)')
LINK_RE = re.compile(r'(?<!!)\[([^\]]+)\]\(#([^)\s]+)\)')
MERMAID_RE = re.compile(r'```mermaid\n(.*?)```', re.S)
ID_RE = re.compile(r'^([A-Z]{1,2}-\d{2,3}|\d+\.\d+|[A-Z])(?=[\s.、]|$)')


# ---------- 转图 ----------

def svg_to_png(svg: Path, png: Path) -> str:
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(url=str(svg), write_to=str(png), scale=2)
        return 'cairosvg'
    except Exception:
        pass
    if shutil.which('rsvg-convert'):
        if subprocess.run(['rsvg-convert', '-z', '2', '-o', str(png), str(svg)], capture_output=True).returncode == 0:
            return 'rsvg-convert'
    m = re.search(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', svg.read_text(encoding='utf-8'))
    w, h = (int(m.group(1)), int(m.group(2))) if m else (375, 812)
    return 'playwright' if _pw_shot(svg.resolve().as_uri(), png, w, h) else ''


def _pw_shot(url: str, png: Path, w: int, h: int, selector: str = '') -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
            page.goto(url)
            if selector:
                page.wait_for_selector(selector, timeout=20000)
                page.locator(selector).screenshot(path=str(png))
            else:
                page.screenshot(path=str(png))
            b.close()
        return True
    except Exception:
        return False


def mermaid_to_png(src: str, png: Path) -> str:
    with tempfile.TemporaryDirectory() as td:
        mmd = Path(td) / 'd.mmd'
        mmd.write_text(src, encoding='utf-8')
        cmds = []
        if shutil.which('mmdc'):
            cmds.append(('mmdc', ['mmdc', '-q', '-i', str(mmd), '-o', str(png), '-s', '2', '-b', 'white']))
        if shutil.which('npx'):
            cmds.append(('npx mermaid-cli', ['npx', '-y', '@mermaid-js/mermaid-cli', '-q', '-i', str(mmd), '-o', str(png), '-s', '2', '-b', 'white']))
        for name, cmd in cmds:
            try:
                if subprocess.run(cmd, capture_output=True, timeout=180).returncode == 0 and png.exists():
                    return name
            except Exception:
                pass
        page = Path(td) / 'm.html'
        page.write_text('<html><body style="margin:0;background:#fff"><pre class="mermaid">' + html.escape(src) +
                        '</pre><script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'
                        '<script>mermaid.initialize({startOnLoad:true});</script></body></html>', encoding='utf-8')
        if _pw_shot(page.as_uri(), png, 1400, 1000, 'pre.mermaid svg'):
            return 'playwright + Mermaid CDN'
    return ''


# ---------- Markdown 转 HTML（只覆盖 PRD 用到的写法） ----------

def inline(text: str, imgs: dict) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r'`([^`]+)`', r'<code>\1</code>', out)
    out = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)

    def img(m):
        data = imgs.get(m.group(2))
        src = data or m.group(2)
        return f'<img alt="{m.group(1)}" src="{src}">'
    out = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', img, out)
    out = re.sub(r'\[([^\]]+)\]\(#([^)\s]+)\)', r'<a class="ref" href="#\2">\1</a>', out)
    out = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2" target="_blank">\1</a>', out)
    return out


def md_to_html(md: str, imgs: dict, diagrams: list) -> str:
    lines = md.split('\n')
    out, i, d = [], 0, 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            lang = ln[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            body = '\n'.join(lines[i + 1:j])
            if lang == 'mermaid' and d < len(diagrams) and diagrams[d]:
                out.append(f'<figure><img src="{diagrams[d]}" alt="图 {d + 1}"></figure>')
                d += 1
            else:
                if lang == 'mermaid':
                    d += 1
                out.append(f'<pre>{html.escape(body)}</pre>')
            i = j + 1
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            n = len(m.group(1))
            out.append(f'<h{n}>{inline(m.group(2), imgs)}</h{n}>')
            i += 1
            continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in re.split(r'(?<!\\)\|', lines[i].strip())[1:-1]])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            t = ['<table><thead><tr>' + ''.join(f'<th>{inline(c, imgs)}</th>' for c in head) + '</tr></thead><tbody>']
            for r in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c, imgs)}</td>' for c in r) + '</tr>')
            out.append(''.join(t) + '</tbody></table>')
            continue
        if re.match(r'^\s*([-*]|\d+\.)\s+', ln):
            ordered = bool(re.match(r'^\s*\d+\.', ln))
            items = []
            while i < len(lines) and re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]):
                items.append(re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i]))
                i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x, imgs)}</li>' for x in items) + f'</{tag}>')
            continue
        if ln.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i].lstrip('> '))
                i += 1
            out.append('<blockquote>' + inline(' '.join(q), imgs) + '</blockquote>')
            continue
        if ln.strip() == '---':
            out.append('<hr>')
        elif ln.strip():
            out.append(f'<p>{inline(ln, imgs)}</p>')
        i += 1
    return '\n'.join(out)


PREVIEW_JS = r'''
(function () {
  function plain(el) { return (el.innerText || '').replace(/\s+/g, ' ').trim(); }
  function idOf(text) { var m = text.match(/^([A-Z]{1,2}-\d{2,3}|\d+\.\d+|[A-Z])(?=[\s.、]|$)/); return m ? m[1] : null; }
  var defs = {};
  document.querySelectorAll('tbody tr').forEach(function (tr) {
    var c = tr.cells[0]; if (!c || c.querySelector('a')) return;
    var id = idOf(plain(c)); if (id && !defs[id]) defs[id] = tr;
  });
  document.querySelectorAll('h1,h2,h3,h4').forEach(function (h) {
    var id = idOf(plain(h)); if (id) defs[id] = h;
  });
  Object.keys(defs).forEach(function (id) { defs[id].id = id; });
  function summary(el) {
    if (el.tagName === 'TR') {
      var heads = el.closest('table').querySelectorAll('th');
      return Array.prototype.map.call(el.cells, function (c, i) {
        return (heads[i] ? plain(heads[i]) + '：' : '') + plain(c);
      }).filter(function (s) { return !/：(—)?$/.test(s); }).join('\n');
    }
    var parts = [plain(el)], n = el.nextElementSibling;
    while (n && !/^H[1-4]$/.test(n.tagName) && parts.join('').length < 240) {
      if (n.tagName !== 'FIGURE' && n.tagName !== 'PRE') parts.push(plain(n));
      n = n.nextElementSibling;
    }
    return parts.join('\n').slice(0, 260);
  }
  var tip = document.getElementById('tip'), back = document.getElementById('back'), stack = [];
  document.querySelectorAll('a.ref').forEach(function (a) {
    var id = decodeURIComponent(a.getAttribute('href').slice(1)), t = defs[id];
    if (!t) { a.classList.add('broken'); a.title = '找不到 ' + id; return; }
    a.addEventListener('mouseenter', function () {
      tip.textContent = summary(t); tip.style.display = 'block';
      var r = a.getBoundingClientRect();
      tip.style.left = Math.min(r.left, window.innerWidth - 380) + 'px';
      tip.style.top = (r.bottom + window.scrollY + 6) + 'px';
    });
    a.addEventListener('mouseleave', function () { tip.style.display = 'none'; });
    a.addEventListener('click', function (e) {
      e.preventDefault(); tip.style.display = 'none';
      stack.push(window.scrollY); back.style.display = 'block';
      t.scrollIntoView({ behavior: 'smooth', block: 'center' });
      t.classList.remove('hit'); void t.offsetWidth; t.classList.add('hit');
    });
  });
  back.addEventListener('click', function () {
    window.scrollTo({ top: stack.pop() || 0, behavior: 'smooth' });
    if (!stack.length) back.style.display = 'none';
  });
})();
'''

PREVIEW_CSS = '''
body{margin:0;background:#f5f6f7;color:#1f2329;font:15px/1.7 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
main{max-width:980px;margin:24px auto;padding:32px 40px;background:#fff;border-radius:8px}
h1{font-size:26px}h2{font-size:21px;margin-top:36px;border-bottom:1px solid #eee;padding-bottom:6px}h3{font-size:17px;margin-top:28px}h4{font-size:15px;margin-top:22px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}th,td{border:1px solid #dee0e3;padding:6px 10px;text-align:left;vertical-align:top}th{background:#eef0f2}tbody tr:nth-child(even) td{background:#f2f3f5}
pre{background:#f5f6f7;padding:12px 16px;border-radius:6px;overflow:auto;font:13px/1.6 Menlo,Consolas,monospace}
code{background:#f2f3f5;padding:0 4px;border-radius:3px}figure{margin:12px 0}img{max-width:100%}
blockquote{margin:12px 0;padding:4px 14px;border-left:3px solid #ccc;color:#646a73}
a.ref{color:#1456f0;text-decoration:none;border-bottom:1px dashed #1456f0}a.ref.broken{color:#d83931;border-color:#d83931}
#tip{display:none;position:absolute;max-width:360px;white-space:pre-line;background:#1f2329;color:#fff;font-size:13px;line-height:1.6;padding:8px 12px;border-radius:6px;z-index:9;pointer-events:none}
#back{display:none;position:fixed;right:28px;bottom:28px;padding:10px 18px;border:0;border-radius:20px;background:#1f2329;color:#fff;font-size:14px;cursor:pointer}
.hit{animation:hit 1.6s}@keyframes hit{0%,60%{background:#fff3c4}100%{background:transparent}}
.page-sep{margin:48px 0;border:0;border-top:4px solid #f5f6f7}
'''


# ---------- 主流程 ----------

def title_of(md_text: str, stem: str) -> str:
    for line in md_text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return re.sub(r'^\d+-', '', stem)


def q(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def collect_pages(folder: Path, depth: int, out: list):
    for md in sorted(folder.glob('*.md')):
        out.append((depth, md))
        sub = folder / md.stem
        if sub.is_dir():
            collect_pages(sub, depth + 1, out)


def defined_ids(text: str) -> set:
    ids = set()
    for line in text.splitlines():
        h = re.match(r'^#{1,4}\s+(.*)$', line)
        if h:
            m = ID_RE.match(h.group(1).strip())
            if m:
                ids.add(m.group(1))
        elif line.startswith('|'):
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if cells and '](' not in cells[0]:
                m = ID_RE.match(cells[0])
                if m:
                    ids.add(m.group(1))
    return ids


def data_uri(path: Path) -> str:
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).resolve()
    make_zip = '--no-zip' not in sys.argv
    pages_dir, img_dir = root / 'pages', root / 'images'
    if not pages_dir.is_dir():
        sys.exit(f'找不到 {pages_dir}')
    img_dir.mkdir(exist_ok=True)
    pages: list = []
    collect_pages(pages_dir, 0, pages)
    if not pages:
        sys.exit('pages/ 下没有 md 文件')

    errors, notes, images, diagrams_all = [], [], [], []
    page_html = []
    all_ids, all_links = set(), []
    for pi, (_, md) in enumerate(pages, 1):
        text = md.read_text(encoding='utf-8')
        rel = md.relative_to(root).as_posix()
        all_ids |= defined_ids(text)
        all_links += [(rel, t) for _, t in LINK_RE.findall(text)]

        imgs = {}
        for alt, ref in IMG_RE.findall(text):
            if re.match(r'^[a-z]+://', ref):
                continue
            target = (md.parent / ref).resolve()
            if not target.exists() and target.suffix.lower() == '.png' and target.with_suffix('.svg').exists():
                how = svg_to_png(target.with_suffix('.svg'), target)
                notes.append(f'线框图 {target.name}：' + (f'已转 PNG（{how}）' if how else '无法转 PNG'))
            if target.exists():
                images.append((target.relative_to(root).as_posix(), alt, rel))
                imgs[ref] = data_uri(target)
            else:
                errors.append(f'{rel} 引用的图片不存在：{ref}')

        diag_uris = []
        for di, src in enumerate(MERMAID_RE.findall(text), 1):
            png = img_dir / f'diagram-{pi:02d}-{di:02d}.png'
            how = mermaid_to_png(src, png)
            if how:
                diagrams_all.append((png.relative_to(root).as_posix(), rel, di))
                diag_uris.append(data_uri(png))
                notes.append(f'{png.name}：已渲染（{how}）')
            else:
                diag_uris.append('')
                errors.append(f'{png.name}：无法渲染；安装 mermaid-cli 后重跑')
        page_html.append(md_to_html(text, imgs, diag_uris))

    for rel, target in all_links:
        if target not in all_ids:
            errors.append(f'{rel} 中的链接 #{target} 找不到定义：编号要写在表格第一列或标题开头')

    title = title_of(pages[0][1].read_text(encoding='utf-8'), pages[0][1].stem)
    (root / 'preview.html').write_text(
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(title)}</title><style>{PREVIEW_CSS}</style></head><body><main>'
        + '<hr class="page-sep">'.join(page_html) +
        f'</main><div id="tip"></div><button id="back">← 返回</button><script>{PREVIEW_JS}</script></body></html>',
        encoding='utf-8')

    lines = ['# 由 make_bundle.py 生成。导入飞书 Wiki 的方法见 IMPORT.md', f'bundle: {q(root.name)}', 'wiki:']
    for depth, md in pages:
        ind = '  ' * (depth + 1)
        lines += [f'{ind}- title: {q(title_of(md.read_text(encoding="utf-8"), md.stem))}',
                  f'{ind}  file: {q(md.relative_to(root).as_posix())}', f'{ind}  level: {depth + 1}']
    lines.append('images:' if images else 'images: []')
    for f, alt, used in images:
        lines += [f'  - file: {q(f)}', f'    alt: {q(alt)}', f'    used_in: {q(used)}']
    lines.append('diagrams:' if diagrams_all else 'diagrams: []')
    for f, used, n in diagrams_all:
        lines += [f'  - file: {q(f)}', f'    used_in: {q(used)}', f'    index: {n}']
    lines.append(f'anchors: [{", ".join(q(x) for x in sorted(all_ids))}]')
    (root / 'manifest.yaml').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    tpl = HERE.parent / 'assets' / 'IMPORT.md'
    if not tpl.exists():
        tpl = HERE / 'IMPORT.md'
    if tpl.exists():
        shutil.copy(tpl, root / 'IMPORT.md')

    print(f'页面 {len(pages)} 个，线框图 {len(images)} 张，Mermaid 图 {len(diagrams_all)} 张，编号 {len(all_ids)} 个，链接 {len(all_links)} 个')
    for n in notes:
        print('  ' + n)
    for e in errors:
        print('  ✗ ' + e)
    if errors:
        sys.exit('有问题未解决，未打包。')
    if make_zip:
        z = root.with_suffix('.zip')
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(root.rglob('*')):
                if p.is_file() and p.name != '.DS_Store':
                    zf.write(p, Path(root.name) / p.relative_to(root))
        print(f'已打包：{z}')


if __name__ == '__main__':
    main()
