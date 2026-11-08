#!/usr/bin/env python3
"""本地 MCP 服务；规范以仓库中的 skills/ 为准。"""
import re
import subprocess
import sys
from pathlib import Path

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

ROOT = Path(__file__).resolve().parents[1]
PRD = ROOT / 'skills' / 'caffrey-prd-plus'
RUNNER = ROOT / 'skills' / 'caffrey-test-runner'
mcp = MCPServer('caffrey-prd-plus')


def read_reference(path: str) -> str:
    """只读取技能目录下的 Markdown 文件。"""
    roots = {'prd': PRD, 'runner': RUNNER}
    prefix, sep, name = path.partition('/')
    if not sep or prefix not in roots:
        raise ToolError('路径须以 prd/ 或 runner/ 开头')
    root = roots[prefix].resolve()
    target = (root / name).resolve()
    if not target.is_relative_to(root) or target.suffix != '.md' or not target.is_file():
        raise ToolError('只能读取技能目录中的 Markdown 文件')
    return target.read_text(encoding='utf-8')


@mcp.tool()
def start_prd() -> str:
    """获取 PRD 第一步的版本、板块和交付方式选择规则。"""
    text = (PRD / 'SKILL.md').read_text(encoding='utf-8')
    return text.split('### 第 1 步：', 1)[1].split('### 第 2 步：', 1)[0]


@mcp.tool()
def get_questions(sections: list[str] | None = None) -> str:
    """按题库标题关键词筛选问题；省略 sections 时返回完整题库。"""
    bank = read_reference('prd/references/question-bank.md')
    if not sections:
        return bank
    chunks = re.split(r'(?=^## )', bank, flags=re.M)
    selected = [chunk for chunk in chunks[1:] if any(s in chunk.split('\n', 1)[0] for s in sections if s)]
    if not selected:
        return '没有匹配的板块，请读取完整题库确认标题。'
    return chunks[0] + ''.join(selected)


@mcp.tool()
def get_reference(path: str) -> str:
    """读取规范，如 prd/references/prd-template.md 或 runner/SKILL.md。"""
    return read_reference(path)


@mcp.tool()
def check_prd(markdown: str) -> dict:
    """检查部分待定词、括号、字段表和编号链接；结果须结合上下文复核。"""
    body = re.sub(r'```[^\n]*\n.*?```', lambda m: '\n' * m.group().count('\n'), markdown, flags=re.S)
    issues = []
    for match in re.finditer(r'(?i)\bTBD\b|待确认|待补充|不适用|暂无', body):
        issues.append({'line': body.count('\n', 0, match.start()) + 1, 'message': f'发现待检查用语：{match.group()}'})
    definitions = set()
    for line in body.splitlines():
        match = re.match(r'^\s*(?:#{1,6}\s+|\|\s*)([A-Z]{1,2}-\d{2,3}|\d+\.\d+)(?=[\s.|、]|$)', line)
        if match:
            definitions.add(match.group(1))
    for match in re.finditer(r'(?<!!)\[[^\]]+\]\(#([^\s)]+)\)', body):
        if match.group(1) not in definitions:
            issues.append({'line': body.count('\n', 0, match.start()) + 1, 'message': f'未找到链接目标 #{match.group(1)}'})
    columns = None
    for number, line in enumerate(body.splitlines(), 1):
        prose = re.sub(r'!?\[[^\]]*\]\([^)]*\)|`[^`]*`', '', line)
        if re.search(r'[（）()]', prose):
            issues.append({'line': number, 'message': '发现括号，请检查是否为正文补充说明'})
        if not line.strip().startswith('|'):
            columns = None
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if '必填' in cells and '类型' in cells and '长度 / 格式' in cells:
            columns = {key: cells.index(key) for key in ('必填', '类型', '长度 / 格式')}
        elif columns and len(cells) > max(columns.values()) and not all(re.fullmatch(r':?-+:?', c) for c in cells):
            if cells[columns['必填']] not in ('是', '否'):
                issues.append({'line': number, 'message': '字段表必填列应为是或否'})
            field_type = cells[columns['类型']]
            if re.search(r'文本|数字|金额|日期|时间|上传', field_type) and not cells[columns['长度 / 格式']]:
                issues.append({'line': number, 'message': '字段表缺少长度或格式'})
    return {'issues': issues, 'limitations': '自动检查可能误报；图表完整性、字段语义、上线计划和里程碑是否有用户依据等仍须结合原始材料复核。'}


@mcp.tool()
def build_bundle(directory: str) -> str:
    """在本机指定的全包目录运行打包脚本；会写入文件。"""
    root = Path(directory).expanduser().resolve()
    if not root.is_dir() or not (root / 'pages').is_dir():
        raise ToolError('目录必须存在并包含 pages/ 子目录')
    result = subprocess.run([sys.executable, str(PRD / 'scripts' / 'make_bundle.py'), str(root)], capture_output=True, text=True, timeout=900)
    if result.returncode:
        raise ToolError((result.stdout + result.stderr).strip())
    return result.stdout


@mcp.prompt()
def write_prd() -> str:
    """按技能流程新建 PRD。"""
    return '请先调用 start_prd，按用户材料完成第一步选择并等待确认；再通过 get_questions 和 get_reference 获取需要的规范，逐步确认后撰写 PRD。'


@mcp.prompt()
def update_prd() -> str:
    """按变更管理规范更新 PRD。"""
    return '请调用 get_reference 读取 prd/references/change-management.md，按用户确认的变更更新 PRD。'


@mcp.prompt()
def review_prd() -> str:
    """检查核对已有 PRD。"""
    return '请调用 get_reference 读取 prd/references/prd-review.md，按四个维度检查用户提供的 PRD 并输出检查报告；本技能模版写的 PRD 可再调用 check_prd 辅助检查。用户确认后再出修订版。'


@mcp.prompt()
def create_test_cases() -> str:
    """根据定稿或已有 PRD 生成测试用例和方案。"""
    return '请调用 get_reference 读取 prd/references/test-cases.md、prd/references/test-plan.md 和 prd/references/prd-review.md，先列出影响测试的缺口请用户确认，再按 PRD 生成用例和网页 Agent 测试方案。'


@mcp.prompt()
def execute_tests() -> str:
    """按测试执行技能运行测试。"""
    return '请调用 get_reference 读取 runner/SKILL.md、runner/references/results.md 和目标端指南，确认被测地址、环境、数据、工具与执行范围并取得用户确认后逐条执行，先给出上线结论，再输出结果表和缺陷单。'


if __name__ == '__main__':
    mcp.run(transport='stdio')
