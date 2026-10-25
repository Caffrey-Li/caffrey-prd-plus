# 原型图

PRD 正文里只放文本线框图（`wireframe.md`）。用户说“出原型图”“画个原型”“做个能点的原型”时，才按本文件出原型图。原型图是 PRD 的附件，**以 PRD 第八章为准**：页面、元素、跳转都来自 8.3 用户路径和 8.4 页面说明，不新增功能。

## 一、出之前

| 情况 | 怎么做 |
| --- | --- |
| 已有 PRD，8.4 有线框图 | 直接出 |
| 还没有 PRD | 告诉用户原型图要基于 PRD 的页面说明，建议先走新建流程出 PRD；用户坚持直接出时，按用户描述出，并在原型顶部注明“未经 PRD 梳理” |
| 范围 | 默认出 8.4 中所有页面和弹窗；用户可指定，例如“只出 F-01、F-03” |
| 配色 | 用户团队有设计规范（7.2 I-07）或指定了主色时照用；用户要求灰度时，主色改为 `#333333` |

## 二、出什么

一个**自包含的 HTML 文件**，用浏览器直接打开：

- 文件名：`【需求名称】-原型图-v0.x.html`，版本号与 PRD 一致。
- 所有页面并排放在一张画布上，按 8.3 用户路径的顺序排列；每个页面上方写“页面名（功能编号）”。
- 手机页面 390 × 844；电脑页面 1440 × 900，画布上按 50% 缩放显示。
- 可以点击：按钮和链接按 8.2、8.3 的跳转关系链接到目标页面（`href="#F-03"`），被跳到的页面加主色描边。
- 弹窗单独画一页：背景是触发它的页面（可简化为色块），上面盖 50% 黑色遮罩。
- 顶部固定一条说明栏：需求名称和版本、“示例数据，仅供示意”、页面目录、“显示规则编号”开关（默认打开）。
- 元素旁边的小圆点编号与线框图的 ①②③ 一致，方便对照规则；关掉开关后隐藏。
- 不引用任何外部资源（字体、图标库、图片、脚本），离线也能打开。

## 三、按平台交付

| 平台 | 交付方式 |
| --- | --- |
| 能写文件的工具（Claude Code、Codex、Cursor、WorkBuddy、DeepSeek Harness、Grok Build 等） | 写成 `.html` 文件，告诉用户文件位置，用浏览器打开 |
| 能预览 HTML 的平台（如 Artifact、Canvas） | 直接生成可预览的页面 |
| 只能聊天的工具（Grok Bot 等） | 在一个 `html` 代码块里输出完整文件，告诉用户“复制全部内容，保存为 .html 文件，用浏览器打开”。超过 4 个页面时分成多个文件，每个文件都是完整可打开的 HTML，并在说明栏写“第 1/2 部分” |

## 四、设计规范（用户没有自己的规范时）

| 项目 | 默认值 |
| --- | --- |
| 主色 | 只用 1 个，默认 `#2E7D6B`；用于主按钮、选中态、价格等强调信息。在说明栏写“主色为示意” |
| 中性色 | 文字 `#1F2329`；次要文字 `#646A73`；辅助文字 `#86909C`；禁用文字 `#A9AEB8`；分隔线 `#EEEFF1`；边框 `#C9CDD4`；页面背景 `#F5F6F7`；卡片 `#FFFFFF`；浅色填充 `#F2F3F5` |
| 字体 | `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` |
| 字号 | 11 / 12 / 13 / 14 / 15 / 16 / 17 / 22，导航标题 17，正文 14 |
| 圆角 | 卡片 12；主按钮全圆角；输入框、时段按钮 8；标签 4 |
| 间距 | 4 的倍数；页面左右边距 16；卡片内边距 16 |
| 点击区域 | 按钮、可点击项高度不小于 44 |
| 图标 | 内联 SVG 线性图标，线宽 1.8-2；不用表情符号 |
| 头像、图片 | 浅灰底（`#E8EAED`）加文字（姓氏或“图片”），不用真实图片 |
| 平台惯例 | 小程序右上角画胶囊按钮；App、小程序不画手机状态栏；后台用顶栏 + 左侧导航 |
| 禁止 | 渐变、大面积阴影、动画、装饰插画 |

## 五、内容规则

1. **与线框图一致**：区域顺序、元素、文案、编号都和 8.4 线框图对应。线框图里没有的功能、按钮、字段，原型图里也不加。
2. **示例数据可以写，但要声明**：为了看起来像真实页面，可以填示例姓名、价格、时间，说明栏必须写“示例数据，仅供示意”。示例数据不能写回 PRD。
3. **待确认的规则不拍板**：PRD 里标了【TBD】或【待确认】的规则，原型中显示“待确认”，例如“预计退款 ¥ 待确认”。
4. **只画默认状态**：加载、空状态、异常状态遵循 I-02，不单独画；某个状态对理解很关键时，加一页并在标题注明状态。
5. **缺页面说明不硬画**：8.1 中有界面、但 8.4 没有页面说明的功能，不出原型；在交付时列出来，例如“F-02 咨询师详情在 8.4 没有页面说明，未出原型，需要的话先补 PRD”。

## 六、HTML 骨架

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>【需求名称】- 原型图 v0.1</title>
<style>
:root{--primary:#2E7D6B;--text:#1F2329;--text-2:#646A73;--text-3:#86909C;--line:#EEEFF1;--bg:#F5F6F7;--card:#FFFFFF;--fill:#F2F3F5}
*{box-sizing:border-box} body{margin:0;background:#E9EBEE;color:var(--text);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
a{color:inherit;text-decoration:none}
.topbar{position:sticky;top:0;z-index:9;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:12px 24px;background:#fff;border-bottom:1px solid var(--line);font-size:13px}
.canvas{display:flex;flex-wrap:wrap;gap:48px;padding:32px 24px}
.board{display:flex;flex-direction:column;gap:8px} .board-title{font-size:13px;color:var(--text-2)}
.screen{width:390px;height:844px;display:flex;flex-direction:column;overflow:hidden;position:relative;background:var(--bg);border-radius:20px;box-shadow:0 0 0 1px #D9DCE1}
.board:target .screen{box-shadow:0 0 0 3px var(--primary)}
.num{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:8px;background:#646A73;color:#fff;font-size:10px;font-weight:600;vertical-align:middle}
body.hide-num .num{display:none}
</style>
</head>
<body>
<header class="topbar">
  <strong>【需求名称】原型图 v0.1</strong>
  <span>示例数据，仅供示意 · 主色为示意</span>
  <nav><a href="#F-01">咨询师列表</a> · <a href="#F-03">选择时段</a></nav>
  <label><input type="checkbox" id="toggle-num" checked> 显示规则编号</label>
</header>
<main class="canvas">
  <section class="board" id="F-01">
    <div class="board-title">咨询师列表（F-01）</div>
    <div class="screen">
      <!-- 页面内容：按 8.4 线框图从上到下实现，编号写成 <span class="num">1</span> -->
    </div>
  </section>
</main>
<script>
document.getElementById('toggle-num').addEventListener('change', function (e) {
  document.body.classList.toggle('hide-num', !e.target.checked);
});
</script>
</body>
</html>
```

完整样例见仓库 `examples/prototype-psych-booking.html`。

## 七、交付说明

原型图之后输出三到五行：

- 文件位置，或保存方式（聊天工具）。
- 出了哪些页面；没出的功能及原因（见第五节第 5 条）。
- 放进飞书：用浏览器打开后截图，插入 PRD 附录 B，或放在对应页面线框图下方；原型图不替代线框图。
- PRD 修改后原型图不会自动更新，需要时再说“重新出原型图”。
