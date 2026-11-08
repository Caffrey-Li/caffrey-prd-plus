# 本地 MCP 服务

此版本从本地仓库读取两个技能的规范，通过标准输入输出提供 MCP 服务。仅供本机使用：没有远程服务、身份认证或在线部署能力，不要将其直接暴露到公网。

需要 Python 3.11 或更新版本，以及本仓库。安装 `requirements.txt` 中的依赖后，用安装了依赖的 Python 运行本目录的 `server.py`。例如在支持本地 MCP 的客户端中配置：

```bash
python3 -m pip install -r mcp/requirements.txt
```

建议先启用自己的 Python 虚拟环境，然后使用该环境中的 Python 路径配置客户端。

```json
{
  "mcpServers": {
    "caffrey-prd-plus": {
      "command": "/你的环境/bin/python",
      "args": ["/你的仓库/caffrey-prd-plus/mcp/server.py"]
    }
  }
}
```

将路径换成实际位置；各客户端配置入口和格式可能不同，需参考各客户端文档。本服务使用仓库内的 `skills/`，移动或删除仓库会导致服务不可用。

提供 `start_prd`、`get_questions`、`get_reference`、`check_prd`、`build_bundle` 五个工具，以及新建 PRD、修改 PRD、检查 PRD、生成测试用例、执行测试五个提示词。问题库由 Agent 按材料筛选并拟建议答案；检查工具只检查部分待定词、编号链接、括号和字段表，结果可能误报，不能代表 PRD 完整合格。`build_bundle` 会在指定的本地目录写入文件并生成 ZIP，需要图表渲染工具；交付前仍要按技能规范验证预览。

使用 Python SDK 的客户端完成了本地协议测试。Claude、Codex、Cursor、Muse、WorkBuddy、Trae、Grok Bot、Coze 和飞书智能伙伴尚未逐一实测；网页平台需要另行实现并验证远程接入。本地服务不直接操作被测网站或替代有浏览器操作能力的测试 Agent。

## HTTP 开发预览

`python mcp/http_server.py --port 8765` 启动仅监听本机的 HTTP 测试服务，地址为 `http://127.0.0.1:8765/mcp`。这是开发预览：只提供规范、问题和检查工具，不提供访问服务端文件的打包工具。该地址只能供同一台电脑测试，网页平台无法连接。

预览没有公网所需的身份验证、加密和用户隔离，不可通过端口映射、反向代理或隧道公开。实现并验证这些能力，以及安全的文件交付和目标平台兼容性后，才能考虑部署。
