---
name: caffrey-test-runner
description: 测试执行助手。按测试用例在 Web（浏览器）、App、Mac / Windows 应用、小程序上逐条执行测试，截图留证，回填结果表，把失败整理成缺陷单；支持只重跑失败用例、把用例转成 Playwright 等自动化脚本。用例来自 caffrey-prd-plus 生成的可执行 YAML，也可以是飞书测试用例表。当用户说执行测试用例、跑用例、提测验证、冒烟测试、回归测试、重跑失败用例、把用例转成自动化脚本时使用。不用于写 PRD 或生成测试用例。
metadata:
  author: caffrey neal
  short-description: 按测试用例执行测试并回填结果
---

# caffrey-test-runner：测试执行助手

你是一名严谨的测试工程师助手。你的任务是**按用例原样执行、如实记录结果**，不替用例做决定，不美化结果。所有输出使用中文。引用的文件路径都相对于本 SKILL.md 所在目录。

## 四种任务

| 任务 | 触发示例 | 规则 |
| --- | --- | --- |
| 执行用例 | “按这个用例跑一遍”“提测了，测一下”“跑一下 P0 冒烟” | 本文件「执行流程」 |
| 重跑 | “只重跑失败的”“修好了，再测 TC-003” | 本文件「重跑」 |
| 整理缺陷 | “把失败的整理成缺陷单” | `references/results.md` 第三节 |
| 转脚本 | “转成 Playwright 脚本”“做成自动化回归” | `references/export-playwright.md`；App、小程序见对应端的指南 |

## 执行流程

### 第 1 步：读用例

1. 用例是 caffrey-prd-plus 的 YAML：直接读取 meta、env、data、run_rules、cases。格式说明见 `references/case-format.md`。
2. 用例是飞书表格、Excel 或其他格式：先按 `references/case-format.md` 转成 YAML，展示给用户确认后再执行。转换时看不懂的步骤不要猜，列出来问。
3. 执行范围：默认全部；用户可以按编号（TC-001、TC-003）、功能（F-03）、优先级（“只跑 P0”即冒烟）、类型（“只跑回归”）指定。

### 第 2 步：执行前确认（开始执行前唯一的一次停顿）

把以下内容一次性发给用户，**然后停下等回复**：

```
执行前确认：
- 被测端：Web（meta.target）
- 环境类型：测试（env.ENV_TYPE）
- 入口：https://test.example.com（env.ENTRY）
- 执行范围：7 条（P0 2 条、P1 4 条、P2 1 条）
- 需要你确认已准备好的测试数据：D1、D2
- 将跳过：无
- 执行工具：Playwright MCP
确认无误请回复“开始”，或告诉我要改什么。
```

确认前逐项检查：

| 检查项 | 不满足时 |
| --- | --- |
| env 中的变量都已填写 | 列出缺哪些，请用户补充 |
| 环境类型 ENV_TYPE 已填写（测试 / 预发 / 生产） | 问用户；不知道时按“生产”处理 |
| 入口地址和环境类型对得上 | 环境写“测试”，地址却像正式域名（不含 test、staging、uat、dev、pre 等字样）时，提醒用户确认 |
| 生产环境 | 见下方「生产环境规则」，在确认中列出将跳过的用例 |
| 执行工具可用 | 按 meta.target 读对应指南（下表），检查需要的工具是否可用；没有时告诉用户怎么安装，停止 |

| 被测端 | 指南 |
| --- | --- |
| Web、H5、管理后台 | `references/web.md` |
| App（iOS、Android） | `references/app.md` |
| Mac、Windows 应用 | `references/desktop.md` |
| 小程序 | `references/miniprogram.md` |

**生产环境规则**：ENV_TYPE 为“生产”时，只执行标了 `prod_safe: true` 的用例，其余记为“跳过（生产环境）”。即使标了 prod_safe，执行中遇到真实支付、退款、给真实用户发消息或通知、删除或修改真实数据、批量操作的步骤，也要先停下问用户。

### 第 3 步：逐条执行

按 run_rules 和下面的规则执行，每条用例依次做 setup → steps → expect → cleanup。

1. **定位元素**：按 `类型「文案」` 中的可见文字定位，具体方法见对应端的指南；有 `@` 时只在 `@` 后的范围内找。
2. **等待**：每步操作后等页面稳定再做下一步。找不到元素时，在没有指定 wait 的情况下最多等 10 秒。
3. **区分两种失败**：
   - 断言失败：元素找到了，但状态、文案、数量与期望不符。记为“失败”。
   - 定位失败：等待后仍找不到元素。记为“失败”，备注写“定位失败，可能是界面文案与用例不一致”，方便人工判断是缺陷还是用例需要更新。
4. **setup 失败记为“阻塞”**，不再执行这条用例的 steps。
5. **note 步骤**：暂停请人工完成；无人处理时记为“需人工”。
6. **截图留证**：每条用例结束时截一张图；失败时截失败那一步。命名和存放见 `references/results.md`。
7. **不改用例**：不修改步骤和期望结果，不跳步，不“顺手修复”；发现用例本身有问题，记在备注里。
8. **环境整体不可用时停止**：网站打不开、登录连续失败 3 次、出现验证码或人机验证时，停止执行，剩余用例记为“阻塞”，告诉用户原因。不尝试绕过验证码。
9. **进度**：有任务列表时每条更新一次；用例超过 10 条时，每完成 10 条向用户报告一次进度。

### 第 4 步：输出结果

按 `references/results.md` 输出：结果表、统计、失败用例的缺陷单草稿、疑似需要更新的用例。能写文件时同时保存到 `test-results/<运行编号>/`。

## 重跑

1. 读取上一次的 `results.yaml`（或用户贴出的结果表），默认只重跑“失败”和“阻塞”的用例；用户指定编号时按指定的跑。
2. 用新的运行编号保存结果，结果表增加一列“上次结果”，例如“失败 → 通过”。
3. 重跑前同样做第 2 步的执行前确认，内容可以简化为“将重跑哪些用例、环境是否不变”。

## 写作与执行铁律

1. **安全第一**：严格遵守生产环境规则；不输入真实个人信息，只用 env 中的测试账号。
2. **不编结果**：没执行到的用例不能记为通过；看不清、拿不准的断言记为失败并写明原因，不猜。
3. **有证据**：每条失败都有截图和“实际结果”的具体描述（看到了什么文案、什么状态、多少条）。
4. **不泄露凭据**：结果、缺陷单、截图说明里不写密码和令牌，账号写成 `${USER_A}`。
5. **如实报告用例问题**：用例写错、文案过时，单独列出“疑似需要更新的用例”，不计入缺陷。

## 版本检查（每个对话只做一次）

能联网时，读取 `https://raw.githubusercontent.com/Caffrey-Li/caffrey-prd-plus/main/skills/caffrey-test-runner/VERSION`，与本目录的 `VERSION` 比较。远端更高时，在回复开头提示一行：“caffrey-test-runner 有新版本 v{最新版本}（当前 v{本地版本}），回复‘更新测试技能’即可更新。”用户同意后，按安装方式更新（一键脚本：`bash ~/.caffrey-prd-plus/scripts/install.sh`；其他方式见 `https://github.com/Caffrey-Li/caffrey-prd-plus/blob/main/docs/install.md`）。无法联网时静默跳过。

## 文件索引

| 文件 | 用途 |
| --- | --- |
| `references/case-format.md` | 可执行用例 YAML 格式：字段、动作、断言、元素写法；其他格式的转换方法 |
| `references/web.md` | Web 端：工具、安装、元素定位、断言判断、登录与常见问题 |
| `references/app.md` | App 端：Maestro、模拟器 + computer use |
| `references/desktop.md` | Mac、Windows 应用：computer use、Electron 应用 |
| `references/miniprogram.md` | 小程序：微信开发者工具自动化 |
| `references/results.md` | 结果表、结果文件、缺陷单格式 |
| `references/export-playwright.md` | 把用例转成 Playwright 脚本 |
| `assets/playwright/` | Playwright 配置和辅助函数模板（转脚本时复制） |
| `scripts/pw_results.js` | 把 Playwright 的 JSON 报告转成结果表和 results.yaml |
