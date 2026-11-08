import asyncio
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

try:
    from mcp import Client, StdioServerParameters
except ImportError:
    Client = None

SERVER = Path(__file__).resolve().parents[1] / 'mcp' / 'server.py'


@unittest.skipUnless(Client is not None, '需安装 mcp/requirements.txt')
class MCPServerTest(unittest.TestCase):
    def test_stdio_tools_and_reference_boundary(self):
        async def run():
            params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], env={'PYTHONDONTWRITEBYTECODE': '1'})
            async with Client(params) as client:
                tools = {tool.name for tool in (await client.list_tools()).tools}
                self.assertEqual(tools, {'start_prd', 'get_questions', 'get_reference', 'check_prd', 'build_bundle'})
                self.assertEqual({p.name for p in (await client.list_prompts()).prompts}, {'write_prd', 'update_prd', 'review_prd', 'create_test_cases', 'execute_tests'})
                review = await client.call_tool('get_reference', {'path': 'prd/references/prd-review.md'})
                self.assertIn('检查核对已有 PRD', review.content[0].text)
                ref = await client.call_tool('get_reference', {'path': 'prd/references/prd-template.md'})
                self.assertFalse(ref.is_error)
                self.assertIn('PRD 核心模版', ref.content[0].text)
                invalid = await client.call_tool('get_reference', {'path': 'prd/../../CHANGELOG.md'})
                self.assertTrue(invalid.is_error)
                result = await client.call_tool('check_prd', {'markdown': '# 示例\n待确认\n[规则](#R-99)'})
                self.assertFalse(result.is_error)
                self.assertIn('待确认', result.content[0].text)
                self.assertIn('#R-99', result.content[0].text)
                result = await client.call_tool('check_prd', {'markdown': '| 字段 | 类型 | 必填 | 长度 / 格式 |\n| --- | --- | --- | --- |\n| 姓名 | 文本 | 必填 | |\n补充（内容）'})
                self.assertIn('必填列', result.content[0].text)
                self.assertIn('长度或格式', result.content[0].text)
                self.assertIn('括号', result.content[0].text)
                questions = await client.call_tool('get_questions', {'sections': ['目标']})
                self.assertIn('目标与成功标准', questions.content[0].text)
                self.assertNotIn('## 六、协作与影响范围', questions.content[0].text)
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / 'bundle'
                    (root / 'pages').mkdir(parents=True)
                    (root / 'pages/01.md').write_text('# 示例\n', encoding='utf-8')
                    packed = await client.call_tool('build_bundle', {'directory': str(root)})
                    self.assertFalse(packed.is_error)
                    self.assertTrue(root.with_suffix('.zip').is_file())

        asyncio.run(run())

    def test_http_preview_has_no_filesystem_bundle_tool(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        http_script = SERVER.with_name('http_server.py')
        process = subprocess.Popen([sys.executable, '-B', str(http_script), '--port', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                if process.poll() is not None:
                    self.fail('HTTP 预览启动失败')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.1):
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                self.fail('HTTP 预览启动超时')

            async def run():
                async with Client(f'http://127.0.0.1:{port}/mcp') as client:
                    names = {tool.name for tool in (await client.list_tools()).tools}
                    self.assertEqual(names, {'start_prd', 'get_questions', 'get_reference', 'check_prd'})
                    result = await client.call_tool('get_reference', {'path': 'prd/references/prd-template.md'})
                    self.assertFalse(result.is_error)
                    self.assertIn('PRD 核心模版', result.content[0].text)

            asyncio.run(run())
        finally:
            process.terminate()
            process.wait(timeout=10)
