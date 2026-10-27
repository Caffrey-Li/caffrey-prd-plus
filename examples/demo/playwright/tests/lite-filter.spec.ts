// 由 caffrey-test-runner 根据 demo-test-cases.yaml 转换生成。
// 一条用例对应一个 test；标题中的 @P0 等标签可用于筛选，如 npx playwright test --grep @P0
import { test, expect } from '@playwright/test';
import { el, open, fill, guardProd, textOf, expectEachContains } from './helpers';

test.describe('咨询师列表增加“只看今天可约” PRD v1.0', () => {

  test('TC-001 打开开关后只显示今天可约的咨询师 @P0 @F-01 @正常', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
    });
    await test.step('steps', async () => {
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('expect', async () => {
      await expect(el(page, '卡片「${COUNSELOR_TODAY}」')).toBeVisible();
      await expect(el(page, '卡片「${COUNSELOR_NOT_TODAY}」').filter({ visible: true })).toHaveCount(0);
    });
  });

  test('TC-002 关闭开关后恢复原筛选结果 @P0 @F-01 @正常', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('steps', async () => {
      await el(page, '开关「只看今天可约」').setChecked(false);
    });
    await test.step('expect', async () => {
      await expect(el(page, '卡片「${COUNSELOR_TODAY}」')).toBeVisible();
      await expect(el(page, '卡片「${COUNSELOR_NOT_TODAY}」')).toBeVisible();
      await expect(el(page, '下拉「可约日期」')).toBeEnabled();
    });
  });

  test('TC-003 与擅长方向筛选组合时同时满足两个条件 @P1 @F-01 @正常', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
    });
    await test.step('steps', async () => {
      await el(page, '下拉「擅长方向」').selectOption({ label: fill('${TAG_OF_TODAY}') });
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('expect', async () => {
      await expect(el(page, '卡片「${COUNSELOR_TODAY}」')).toBeVisible();
      await expectEachContains(el(page, '卡片「咨询师」'), fill('${TAG_OF_TODAY}'));
    });
  });

  test('TC-004 打开开关时清空并置灰“可约日期” @P1 @F-01 @边界', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
    });
    await test.step('steps', async () => {
      await el(page, '下拉「可约日期」').selectOption({ label: '明天' });
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('expect', async () => {
      await expect(el(page, '下拉「可约日期」')).toBeDisabled();
      await expect.poll(() => textOf(el(page, '下拉「可约日期」'))).toBe('可约日期');
    });
  });

  test('TC-005 今天没有可约咨询师时显示空状态 @P1 @F-01 @边界', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await el(page, '单选「今天无可约」@区域「演示数据」').click();
      await open(page, '页面「咨询师列表」');
    });
    await test.step('steps', async () => {
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('expect', async () => {
      await expect(el(page, '文本「今天暂无可约的咨询师」')).toBeVisible();
      await expect(el(page, '按钮「查看全部」')).toBeVisible();
      await expect(el(page, '卡片「咨询师」').filter({ visible: true })).toHaveCount(0);
    });
  });

  test('TC-006 离开列表再回来，开关恢复为关闭 @P2 @F-01 @正常', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
      await el(page, '开关「只看今天可约」').setChecked(true);
    });
    await test.step('steps', async () => {
      await el(page, '链接「首页」@区域「底部标签栏」').click();
      await el(page, '链接「咨询」@区域「底部标签栏」').click();
    });
    await test.step('expect', async () => {
      await expect(el(page, '页面「咨询师列表」')).toBeVisible();
      await expect(el(page, '开关「只看今天可约」')).not.toBeChecked();
    });
  });

  test('TC-007 回归：开关关闭时，原有筛选不受影响 @P1 @F-01 @回归', async ({ page }) => {
    guardProd(true);
    await test.step('setup', async () => {
      await open(page, '${ENTRY}');
      await open(page, '页面「咨询师列表」');
    });
    await test.step('steps', async () => {
      await el(page, '下拉「擅长方向」').selectOption({ label: fill('${TAG_OF_TODAY}') });
      await el(page, '列表「咨询师」').evaluate((e) => e.scrollIntoView({ block: 'end' }));
    });
    await test.step('expect', async () => {
      await expect(el(page, '开关「只看今天可约」')).not.toBeChecked();
      await expectEachContains(el(page, '卡片「咨询师」'), fill('${TAG_OF_TODAY}'));
      expect(await el(page, '卡片「咨询师」').filter({ visible: true }).count()).toBeGreaterThanOrEqual(1);
    });
  });
});
