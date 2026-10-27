# 可执行用例格式（YAML）

与 caffrey-prd-plus 生成的可执行用例一致。一个文件包含 meta、env、data、run_rules、cases 五部分。

```yaml
meta:
  prd: 在线预约咨询师 PRD
  prd_version: v1.0
  generator: caffrey-prd-plus v0.4.0
  target: Web                     # 被测端：Web / H5 / 小程序 / App / Mac / Windows / API

env:                              # 执行前由用户填写，用例中用 ${名称} 引用
  ENV_TYPE: 测试                  # 测试 / 预发 / 生产
  ENTRY: ""                       # Web 填网址；App 填包名或安装包路径；小程序填项目路径；桌面应用填应用名称
  PAGES: {}                       # 可选：页面名 → 网址，如 { 咨询师列表: /counselors }，open 页面时直接打开
  USER_A: { account: "", password: "" }

data:                             # 执行前需要准备的测试数据
  - id: D1
    desc: ……
    how: ……

run_rules: |
  ……（执行规则，见 SKILL.md）

cases:
  - id: TC-001
    feature: F-03
    title: 选中时段后锁定并显示倒计时
    type: 正常                    # 正常 / 异常 / 边界 / 权限 / 回归 / 非功能
    priority: P0
    prod_safe: false              # 可选：true 表示可在生产环境执行（只读、不产生交易和通知）
    pre: [D1]
    setup:
      - login: ${USER_A}
    steps:
      - open: 页面「咨询师列表」
      - click: 时段「14:00-14:50」
    expect:
      - visible: 文本「锁定剩余」
    cleanup:
      - back: 2
```

## 动作

| 动作 | 写法 |
| --- | --- |
| open | `open: 页面「咨询师列表」`，或 `open: ${ENTRY}` |
| login | `login: ${USER_A}` |
| click | `click: 按钮「同意并继续」` |
| input | `input: { target: 输入框「称呼」, value: "测试来访者01" }` |
| clear | `clear: 输入框「称呼」` |
| select | `select: { target: 下拉「擅长方向」, value: "焦虑" }` |
| check / uncheck | `check: 多选「我已阅读并同意」` |
| toggle | `toggle: { target: 开关「只看今天可约」, value: 开 }` |
| scroll | `scroll: { target: 区域「同意书正文」, to: 底部 }` |
| back | `back: 1`（返回几级） |
| wait | `wait: 2s`，或 `wait: { until: 文本「支付成功」, timeout: 10s }` |
| api | `api: { method: POST, path: /xxx, body: {...} }` |
| note | `note: 在真机上确认收到服务通知`（人工步骤） |

## 断言

| 断言 | 写法 |
| --- | --- |
| visible / hidden | `visible: 弹窗「确认取消预约」` |
| text | `text: { target: 文本「预约单状态」, value: "已预约" }`（去掉首尾空白后完全一致） |
| contains | `contains: { target: …, value: "已" }` |
| matches | `matches: { target: …, value: '正则' }` |
| enabled / disabled | `disabled: 按钮「同意并继续」` |
| checked / unchecked | `unchecked: 开关「只看今天可约」` |
| count | `count: { target: 卡片「咨询师」, value: 3 }`，或 `{ target: …, min: 1 }` |
| each | `each: { target: 卡片「咨询师」, contains: "今天" }`（每一项都满足；列表为空时记为失败） |
| page | `page: 预约详情` |
| toast | `toast: "请输入称呼"`（5 秒内出现） |

## 元素写法

- `类型「文案」`。类型：页面、按钮、输入框、下拉、单选、多选、开关、日期、时段、卡片、文本、链接、标签页、弹窗、区域、列表、提示。
- 文案与界面上的可见文字一致。
- `卡片「咨询师」` 这类写法中，文案是一类卡片的统称时，表示列表中所有这类卡片；是具体内容（如姓名）时，表示包含这段文字的那张卡片。
- 同名元素有多个时用 `@` 限定范围：`按钮「确认取消」@弹窗「确认取消预约」`。

## 把其他格式转成 YAML

用户给的是飞书表格、Excel 或文字描述时：

1. 每行用例转成一个 case；“操作步骤”拆成一步一个动作，“预期结果”拆成可判断的断言。
2. 表格里的具体账号、网址提到 env，用变量引用；测试数据提到 data。
3. 无法转成断言的预期（如“体验流畅”），转成 note 并在转换说明里列出。
4. 被测端、环境类型不明确时问用户。
5. 转换完成后展示 YAML 和“转换说明”（哪些地方做了解释、哪些转成了 note），用户确认后再执行。
