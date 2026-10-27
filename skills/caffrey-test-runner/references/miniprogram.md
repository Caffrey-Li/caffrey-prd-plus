# 小程序执行指南

浏览器工具操作不了小程序，需要借助微信开发者工具的自动化能力。以下以微信小程序为例；其他平台的小程序按各自开发者工具的自动化文档处理。

## 一、准备开发者工具

1. 打开微信开发者工具：设置 → 安全设置 → 打开「服务端口」（较新版本中还需打开 HTTP 调试和自动化测试相关开关）。
2. 用命令行以自动化模式打开项目（端口默认 9420）：
   - Mac：`/Applications/wechatwebdevtools.app/Contents/MacOS/cli auto --project /项目路径 --auto-port 9420`
   - Windows：`"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" auto --project C:\项目路径 --auto-port 9420`
3. env 中需要：`ENTRY`（项目路径）、测试账号；登录、支付使用测试号和支付沙箱。

具体开关名称和命令以微信官方文档「小程序自动化」为准：https://developers.weixin.qq.com/miniprogram/dev/devtools/auto/quick-start.html

## 二、可用方式

| 方式 | 适合 | 说明 |
| --- | --- | --- |
| miniprogram-automator 脚本 | 批量执行、回归测试 | 官方 Node.js 自动化库（`npm i miniprogram-automator`），可连接上面打开的开发者工具，按页面路径跳转、按选择器或文字找元素、截图 |
| 小程序 MCP | agent 直接执行 | 社区有基于 miniprogram-automator 的 MCP 服务，如 weapp-dev-mcp；属于第三方工具，使用前自行评估 |
| computer use | 没法开启自动化时的兜底 | 操作开发者工具中的模拟器，按可见文字点击；速度较慢 |
| Minium | 团队已有 Python 测试体系 | 腾讯提供的小程序测试框架 |

## 三、转成 miniprogram-automator 脚本

```js
const automator = require('miniprogram-automator');

(async () => {
  const mp = await automator.connect({ wsEndpoint: 'ws://localhost:9420' });
  const page = await mp.reLaunch('/pages/counselor/list');  // 页面路径问研发，或放进 env.PAGES
  // 按用例逐步操作，如：const el = await page.$('.switch'); await el.tap();
  await mp.screenshot({ path: 'test-results/TC-001.png' });
  await mp.disconnect();
})();
```

- 小程序里按文字找元素不如网页方便，转脚本时需要研发提供页面路径和关键元素的选择器（或为元素加上固定的 class、id）。缺少时列出来问。
- 微信登录授权、手机号授权、支付等弹窗由微信控制，脚本通常无法点击，用测试号免授权或记为“需人工”。
- API 写法以官方文档为准。
