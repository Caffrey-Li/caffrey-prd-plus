# Web 端执行指南

适用于网站、H5、管理后台、SaaS 页面。

## 一、可用工具

| 工具 | 适合 | 怎么准备 |
| --- | --- | --- |
| Playwright MCP | 在 Claude Code、Cursor、Codex 中批量执行；能保存截图文件；也是转脚本前的首选 | Claude Code：`claude mcp add playwright npx @playwright/mcp@latest`<br>Codex：`codex mcp add playwright npx "@playwright/mcp@latest"`<br>Cursor：Cursor Settings → MCP → Add new MCP Server，类型选 command，命令填 `npx @playwright/mcp@latest`<br>需要电脑上装有 Node.js |
| Claude in Chrome（浏览器扩展） | 用你自己的 Chrome 和登录状态，适合需要单点登录、内网的系统 | 安装扩展并在 Claude 中启用，给被测网站授予访问权限 |
| Claude 桌面版内置浏览器 | 独立的浏览器窗格，不影响你自己的 Chrome | 打开 Claude 桌面版即可 |

当前 agent 中三者都没有时，告诉用户：“当前环境没有可以操作浏览器的工具。推荐在 Claude Code 中运行 `claude mcp add playwright npx @playwright/mcp@latest` 后重新开始。”然后停止。

## 二、元素定位

优先用可访问性信息（角色 + 名称），其次用可见文字。

| 元素 | 定位方法 |
| --- | --- |
| 页面「X」 | open 时：env.PAGES 中有 X 就直接打开对应网址；否则从 ENTRY 进入后，通过导航菜单、标签栏找到 X。判断当前页面：页面标题、导航标题或主标题（h1）为 X |
| 按钮「X」 | 角色为 button、名称为 X；找不到时找文字为 X 的可点击元素 |
| 链接「X」 | 角色为 link、名称为 X |
| 输入框「X」 | 标签（label）为 X，或占位文字（placeholder）为 X 的输入框 |
| 下拉「X」 | 标签或当前显示文字为 X 的下拉；原生 select 直接选值，自定义下拉先点开，再点选项文字 |
| 单选、多选「X」 | 标签为 X 的单选框、复选框 |
| 开关「X」 | 角色为 switch 或 checkbox、名称为 X；找不到时找文字 X 旁边的开关 |
| 日期、时段「X」 | 文字为 X 的日期或时段按钮；日期选择器先点开，再按 X 选择 |
| 文本「X」 | 包含 X 的可见文字 |
| 卡片「X」 | 列表中包含文字 X 的卡片或列表项；X 是一类卡片的统称时，指列表中所有卡片 |
| 弹窗「X」 | 角色为 dialog、标题包含 X 的弹层 |
| 区域、列表「X」 | 标题或 aria-label 为 X 的区域 |
| 提示 / toast | 页面上短暂出现的提示文字 |

找到多个匹配时：有 `@` 范围就在范围内找；没有时取可见的第一个，并在备注里写“匹配到多个元素”。

## 三、断言判断

| 断言 | 判断方法 |
| --- | --- |
| visible / hidden | 元素在页面上可见（非隐藏、尺寸不为 0）/ 不存在或不可见 |
| text / contains / matches | 取元素的可见文字，去掉首尾空白后比较 |
| enabled / disabled | 看 disabled 属性、aria-disabled；没有这些属性时，点击无反应且呈置灰样式也记为 disabled，备注写判断依据 |
| checked / unchecked | 看选中状态（checked、aria-checked） |
| count | 只数可见的元素 |
| each | 每个可见项都满足；没有任何项时记为失败 |
| page | 当前页面标题、导航标题或主标题为期望值 |
| toast | 5 秒内出现期望文字 |

## 四、登录与验证码

- 只用 env 中的账号登录；密码不出现在结果里。
- 遇到短信验证码、图形验证码、人机验证：停止，记为阻塞，建议让研发在测试环境为测试账号配置固定验证码或白名单。不尝试绕过。
- 已用 Claude in Chrome 并处于登录状态时，login 步骤先检查是否已经是目标账号，是就跳过登录。

## 五、截图与证据

- Playwright MCP：截图保存到 `test-results/<运行编号>/`，文件名见 `results.md`。
- 浏览器扩展、内置浏览器：不能保存文件时，在对话中附上截图，结果表“证据”列写“见对话截图 TC-001”。

## 六、常见情况

| 情况 | 处理 |
| --- | --- |
| 操作后打开了新标签页 | 切换到新标签页继续；用例结束后关闭 |
| 页面内嵌 iframe | 进入 iframe 再定位 |
| 浏览器原生弹窗（alert、confirm） | 使用浏览器扩展时，原生弹窗会卡住扩展，执行前提醒用户；Playwright 中按用例点确定或取消 |
| 上传文件 | 文件路径放在 env（如 `UPLOAD_IMAGE`），没有时记为阻塞 |
| 页面加载慢 | 最多等 10 秒；超时记为失败，备注写“加载超时” |
| 弹出 Cookie 提示、新手引导 | 先关闭，不计入步骤，备注说明 |
