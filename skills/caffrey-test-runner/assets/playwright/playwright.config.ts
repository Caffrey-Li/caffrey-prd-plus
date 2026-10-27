import { defineConfig } from '@playwright/test';
import * as fs from 'fs';

// 读取同目录下的 .env（不依赖第三方库）。也可以直接在命令行里设置环境变量。
if (fs.existsSync('.env')) {
  for (const line of fs.readFileSync('.env', 'utf-8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 10_000 },          // 找不到元素时最多等 10 秒，与 caffrey-test-runner 规则一致
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }], ['json', { outputFile: 'test-results/results.json' }]],
  use: {
    screenshot: 'on',                   // 每条用例都截图，失败时额外保留 trace
    trace: 'retain-on-failure',
    viewport: { width: 1280, height: 900 },
  },
});
