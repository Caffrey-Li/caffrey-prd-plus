# 把用例转成 Playwright 脚本（Web）

agent 直接执行适合第一轮提测；用例稳定后，转成 Playwright 脚本，每次发版自动跑回归，更快、更稳定、成本更低。

## 一、生成的文件

```
e2e/
  package.json              依赖 @playwright/test，脚本：test、test:smoke（只跑 @P0）、report
  playwright.config.ts      从 assets/playwright/ 复制：读取 .env、每条截图、失败保留 trace、输出 JSON 报告
  .env.example              与用例 YAML 的 env 一一对应
  tests/helpers.ts          从 assets/playwright/ 复制：把“类型「文案」”翻译成定位器
  tests/<需求名>.spec.ts    一条用例一个 test
```

模板在本技能的 `assets/playwright/`，完整可运行的样例在仓库 `examples/demo/playwright/`。

## 二、转换步骤

1. **先看页面**：用浏览器工具打开被测页面，确认每个“类型「文案」”都能定位到。定位不到的（如“卡片「咨询师」”这类统称），在 `helpers.ts` 的 `SELECTORS` 中填选择器。
2. **填页面导航**：用例中每个 `open: 页面「X」`，在 `PAGES` 中写清楚怎么进入：点哪个菜单，或直接打开哪个网址。
3. **逐条转换**：按第三节的对照表，一条用例一个 test，标题写成 `用例编号 标题 @优先级 @功能编号 @类型`；setup、steps、expect 各包在一个 `test.step` 里（结果转换时据此区分“阻塞”和“失败”）。
4. **生产环境保护**：每个 test 第一行写 `guardProd(用例的 prod_safe)`。
5. **试跑**：`npm install`、`npx playwright install chromium`、复制 `.env.example` 为 `.env` 并填写，运行 `npx playwright test`。先在测试环境跑通再交付。
6. **转成结果表**：运行 `node <本技能目录>/scripts/pw_results.js test-results/results.json`，生成 `results.md` 和 `results.yaml`；再按 `results.md` 第三节为失败用例写缺陷单（把报错翻译成人能看懂的“实际结果”）。

## 三、对照表

| 用例 | Playwright |
| --- | --- |
| `open: ${ENTRY}` | `await open(page, '${ENTRY}')` |
| `open: 页面「X」` | `await open(page, '页面「X」')`（按 PAGES 导航，并确认页面标题可见） |
| `login: ${USER_A}` | 按登录页写成 fill + click；账号密码用 `env('USER_A_ACCOUNT')` 这类拆开的变量 |
| `click: T` | `await el(page, 'T').click()` |
| `input: {target: T, value: V}` | `await el(page, 'T').fill(fill('V'))` |
| `clear: T` | `await el(page, 'T').clear()` |
| `select: {target: 下拉「X」, value: V}` | 原生下拉：`selectOption({ label: V })`；自定义下拉：先 click 下拉，再 click 选项文字 |
| `check` / `uncheck` | `setChecked(true / false)` |
| `toggle: {target: T, value: 开 / 关}` | `await el(page, 'T').setChecked(true / false)` |
| `scroll: {target: T, to: 底部}` | `await el(page, 'T').evaluate(e => e.scrollIntoView({ block: 'end' }))` |
| `back: N` | 循环 N 次 `await page.goBack()` |
| `wait: 2s` | `await page.waitForTimeout(2000)` |
| `wait: {until: T, timeout: 10s}` | `await expect(el(page, 'T')).toBeVisible({ timeout: 10_000 })` |
| `api` | 使用 `request` fixture |
| `note` | `test.fixme(true, '需人工：……')`，并在结果中记为“需人工” |
| `visible: T` | `await expect(el(page, 'T')).toBeVisible()` |
| `hidden: T` | `await expect(el(page, 'T').filter({ visible: true })).toHaveCount(0)` |
| `text` | `await expect.poll(() => textOf(el(page, 'T'))).toBe(V)`（下拉框取选中项文字） |
| `contains` / `matches` | `toContainText(V)` / `toHaveText(new RegExp(V))` |
| `enabled` / `disabled` | `toBeEnabled()` / `toBeDisabled()` |
| `checked` / `unchecked` | `toBeChecked()` / `not.toBeChecked()` |
| `count: {value: N}` | `await expect(el(page, 'T').filter({ visible: true })).toHaveCount(N)` |
| `count: {min: N}` | `expect(await el(page, 'T').filter({ visible: true }).count()).toBeGreaterThanOrEqual(N)` |
| `each: {contains: V}` | `await expectEachContains(el(page, 'T'), V)` |
| `page: X` | `await expect(el(page, '页面「X」')).toBeVisible()` |
| `toast: V` | `await expect(page.getByText(V)).toBeVisible({ timeout: 5_000 })` |

字符串中的 `${变量}` 交给 `el()`、`open()` 自动替换；直接用作值时包一层 `fill()`。

## 四、交付说明

转换完成后告诉用户：

- 生成了哪些文件，在哪里。
- 哪些用例因为 note、缺少选择器等原因没有完全自动化。
- 怎么运行：首次 `npm install && npx playwright install chromium`，之后 `npx playwright test`；只跑冒烟 `npm run test:smoke`；看报告 `npm run report`。
- 接入持续集成（CI）时，把 `.env` 中的值配置成 CI 的环境变量，不要把账号密码提交到仓库。
