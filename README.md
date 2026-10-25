# caffrey-prd-plus

给产品经理用的 PRD 助手。把零散的需求整理成结构完整、可协作落地的中文 PRD，可在 Claude、Codex、Cursor、Grok、DeepSeek Harness、WorkBuddy 等 AI 工具中使用。

## 能做什么

- **新建 PRD**：输入一句话、会议纪要、截图或旧文档，先确认需求类型、行业和文档版本，再直接出一版草稿，并附上待你确认的问题。
- **新产品模式**：碰到“做一个类似 XX 的产品”这类完整新产品，先出产品总纲（定位、竞品、模块地图、核心对象、MVP 与路线图），再按模块逐个出详细 PRD。
- **迭代 PRD**：按版本号规则修改已有 PRD，自动记录变更、在正文标记改动、提醒需要重新确认的人。
- **拆用户故事**：按功能编号拆成“作为……我想要……以便……”的用户故事和验收条件。
- **生成测试用例**：PRD 定稿后，按验收标准和字段表生成两份用例：可粘贴到飞书表格的版本，和测试 agent 能直接逐条执行、回填结果的 YAML 版本。

## 特点

- **一套固定骨架**：16 章加附录，按“为什么做 → 做什么 → 影响谁 → 怎么做 → 怎么验收 → 怎么上线”排列。
- **三种文档版本**：精简版（改动点、字段、验收、风险，适合小改动）、核心版（研发测试必需的内容）、完整版（全部 16 章）。按需求大小推荐，你也可以自己选或加减章节。
- **20 类需求类型**：App、Web 应用、官网、小程序、H5、硬件/IoT、开放平台、Web 游戏、小游戏、AI 功能、数据类、策略类、运营活动、B 端项目、SaaS、内部工具、商业化/支付、技术改造、合规整改、内容配置。一个需求可以组合多个类型。
- **行业包**：游戏娱乐、风电能源、心理咨询、服务行业、AI 服务，自动补充行业特有的检查项。欢迎贡献更多行业。
- **线下协作**：干系人分工、系统影响、数据影响、接口与架构、外部依赖、待确认事项六张表。
- **全局与交互规范**：通用规则写一次，页面说明只写例外。
- **字段与组件说明**：每个页面附字段表，写清类型、必填、长度格式、枚举、默认值、限制与校验、前置条件；共用的字段和枚举统一放在字段字典。
- **用户路径图**：完整版中每个模块附一张文本路径图，入口、主路径、分支一目了然。
- **页面线框图**：每个页面附一张黑白灰的文本线框图，以骨架为主，编号与规则逐条对应，直接粘贴进飞书即可。
- **原型图（按需）**：说“出原型图”，按 PRD 的页面说明生成一个可点击的 HTML 原型，浏览器直接打开；聊天工具里会输出完整代码，保存成 .html 即可。
- **不完整也清晰**：每章只有“已填写 / 待补充 / 不适用（原因）”三种状态，不编造数字和人名。
- **飞书友好**：不使用需要渲染的流程图，流程和状态都用表格表达，页面用文本线框图，直接粘贴即可。

## 安装

推荐一键安装（需要 git），会同时装到 Claude Code、Codex、Cursor、DeepSeek Harness、Grok Build、WorkBuddy：

```bash
curl -fsSL https://raw.githubusercontent.com/Caffrey-Li/caffrey-prd-plus/main/scripts/install.sh | bash
```

也可以用插件方式安装：

- **Claude Code**：`/plugin marketplace add Caffrey-Li/caffrey-prd-plus`，再 `/plugin install caffrey-prd-plus@caffrey-prd-plus`
- **Cursor**：在 Customize 中选择 From GitHub Repository，填入本仓库地址
- **WorkBuddy**：在【技能管理】中通过 URL 导入，或用一键脚本
- **Grok Bot、ChatGPT 等聊天工具**：上传 [单文件版](dist/caffrey-prd-plus-prompt.md)

详细步骤见 [docs/install.md](docs/install.md)。

## 更新

当前版本见 [CHANGELOG.md](CHANGELOG.md)。使用技能时，如果 agent 能联网，会检查 GitHub 上的最新版本；有新版会在回复开头提示，你回复“更新 PRD 技能”后才会更新，不会自动改动你的文件。插件方式安装的，由 Claude Code 或 Cursor 负责更新。

## 使用示例

```
帮我写个 PRD：心理咨询小程序要加一个在线预约咨询师的功能，用户能看咨询师资料、选时间、付款，咨询前一天提醒。
```

示例输出见 [examples/](examples/)：

- `example-psych-booking.md`：完整版（心理咨询小程序预约），含线框图、字段表和字段字典
- `example-lite-filter.md`：精简版（咨询师列表加一个筛选开关）
- `example-test-cases.md`、`example-test-cases.yaml`：上面精简版需求的测试用例（飞书表格 + 可执行 YAML）
- `prototype-psych-booking.html`：同一个需求的原型图样例（用浏览器打开）
- `example-plane-overview.md`：新产品模式的产品总纲（类似 Plane 的项目协同工具）

## 目录结构

```
skills/caffrey-prd-plus/      技能文件夹（安装这个）
  SKILL.md                    主流程与写作规则
  references/
    prd-template.md           PRD 核心骨架
    section-matrix.md         文档版本与章节取舍
    wireframe.md              页面线框图规范
    prototype.md              原型图规范（按需生成）
    field-spec.md             字段与组件说明规范
    new-product-mode.md       新产品模式流程
    product-overview-template.md  产品总纲模版
    types/                    20 类需求类型模块
    industries/               行业包
    question-bank.md          追问题库
    quality-checklist.md      自检清单
    change-management.md      版本迭代与变更记录
    user-stories.md           用户故事格式
    test-cases.md             测试用例（飞书表格 + 可执行 YAML）
  VERSION                     当前版本号
dist/caffrey-prd-plus-prompt.md   单文件版（给不支持 Skill 的工具）
scripts/install.sh                一键安装 / 更新脚本
scripts/release.py                发版脚本：同步版本号并生成单文件版
scripts/build_single.py           生成单文件版的脚本
.claude-plugin/                   Claude Code 插件清单
.cursor-plugin/                   Cursor 插件清单（支持从 GitHub 导入）
```

## 贡献

- 新增需求类型：在 `references/types/` 新建文件，并登记到 `types/_index.md`。
- 新增行业包：在 `references/industries/` 新建文件，并登记到 `industries/_index.md`。
- 修改后运行 `python3 scripts/build_single.py` 更新单文件版；发布新版本见 [docs/install.md](docs/install.md) 末尾。

## 许可证

MIT
