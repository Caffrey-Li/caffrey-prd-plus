// caffrey-test-runner 转脚本时生成的通用辅助函数：把用例中的“类型「文案」”翻译成 Playwright 定位器。
import { Page, Locator, expect, test } from '@playwright/test';

/** 读取环境变量（对应用例 YAML 的 env） */
export function env(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`缺少环境变量 ${name}，请在 .env 中填写`);
  return v;
}

/** 把字符串中的 ${变量} 替换成环境变量的值 */
export function fill(s: string): string {
  return s.replace(/\$\{(\w+)\}/g, (_, k) => env(k));
}

/** 生产环境只执行 prod_safe 的用例 */
export function guardProd(prodSafe: boolean) {
  test.skip(process.env.ENV_TYPE === '生产' && !prodSafe, '跳过（生产环境）：该用例未标记 prod_safe');
}

/**
 * 无法只靠文字定位的元素，转脚本时打开被测页面检查后填写选择器。
 * 键是用例中的写法；“卡片”是所有卡片的默认选择器。
 */
export const SELECTORS: Record<string, string> = {
  '卡片': '.card',                    // 示例：所有卡片的默认选择器，按被测页面修改
  // '卡片「咨询师」': '.counselor-card',
};

/** 页面导航：页面名 → 如何从入口进入该页面（转脚本时按实际导航填写） */
export const PAGES: Record<string, (page: Page) => Promise<void>> = {
  // 示例：
  // '咨询师列表': async (page) => { await el(page, '链接「咨询」@区域「底部标签栏」').click(); },
  // '订单管理': async (page) => { await page.goto(new URL('/orders', env('ENTRY')).toString()); },
};

type Root = Page | Locator;

/** 把“类型「文案」[@范围]”转成定位器 */
export function el(page: Page, spec: string): Locator {
  const [main, scope] = fill(spec).split('@');
  const root: Root = scope ? el(page, scope) : page;
  if (SELECTORS[main]) return root.locator(SELECTORS[main]);
  const m = main.match(/^(.+?)「(.+)」$/);
  if (!m) throw new Error(`无法解析元素：${spec}`);
  const [, type, name] = m;
  switch (type) {
    case '按钮': return root.getByRole('button', { name, exact: true });
    case '链接': return root.getByRole('link', { name, exact: true });
    case '输入框': return root.getByLabel(name).or(root.getByPlaceholder(name));
    case '下拉': return root.getByRole('combobox', { name });
    case '单选': return root.getByRole('radio', { name });
    case '多选': return root.getByRole('checkbox', { name });
    case '开关': return root.getByRole('switch', { name }).or(root.getByRole('checkbox', { name }));
    case '文本': return root.getByText(name);
    case '卡片': return root.locator(SELECTORS['卡片']).filter({ hasText: name });
    case '弹窗': return root.getByRole('dialog', { name });
    case '区域':
    case '列表': return root.locator(`[aria-label="${name}"]`);
    case '页面': return page.getByRole('heading', { name, exact: true });
    default: return root.getByText(name, { exact: true });
  }
}

/** open 动作 */
export async function open(page: Page, target: string) {
  const m = target.match(/^页面「(.+)」$/);
  if (!m) { await page.goto(fill(target)); return; }
  const go = PAGES[m[1]];
  if (!go) throw new Error(`未定义如何进入页面「${m[1]}」，请在 PAGES 中补充`);
  await go(page);
  await expect(el(page, target)).toBeVisible();
}

/** 元素的可见文字；下拉框取当前选中项的文字 */
export async function textOf(loc: Locator): Promise<string> {
  return (await loc.first().evaluate((e: any) =>
    e.tagName === 'SELECT' ? e.options[e.selectedIndex]?.text ?? '' : e.innerText)).trim();
}

/** each 断言：每个可见项都包含 value；没有任何项时失败 */
export async function expectEachContains(loc: Locator, value: string) {
  const items = loc.filter({ visible: true });
  await expect(items.first()).toBeVisible();
  for (const item of await items.all()) await expect(item).toContainText(value);
}
