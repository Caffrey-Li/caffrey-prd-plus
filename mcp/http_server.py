#!/usr/bin/env python3
"""只监听本机的 HTTP 开发预览，不可直接用于公网。"""
import argparse

from mcp.server import MCPServer

import server

http = MCPServer('caffrey-prd-plus-http-preview')
for tool in (server.start_prd, server.get_questions, server.get_reference, server.check_prd):
    http.tool()(tool)
for prompt in (server.write_prd, server.update_prd, server.review_prd, server.create_test_cases, server.execute_tests):
    http.prompt()(prompt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='仅供本机测试的 HTTP MCP 预览')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    http.run(transport='streamable-http', host='127.0.0.1', port=args.port)
