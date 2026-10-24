# caffrey-prd-plus

给产品经理用的 PRD 助手。把零散的需求整理成结构完整、可协作落地的中文 PRD，可在 Claude、Codex、Cursor、Grok 等 AI 工具中使用。

## 能做什么

- **新建 PRD**：输入一句话、会议纪要、截图或旧文档，先确认需求类型、行业和规模，再直接出一版草稿，并附上待你确认的问题。
- **迭代 PRD**：按版本号规则修改已有 PRD，自动记录变更、在正文标记改动、提醒需要重新确认的人。
- **拆用户故事**：按功能编号拆成“作为……我想要……以便……”的用户故事和验收条件。
- **生成测试用例**：PRD 定稿后，按验收标准生成可粘贴到飞书表格的测试用例。

## 特点

- **一套固定骨架**：16 章加附录，按“为什么做 → 做什么 → 影响谁 → 怎么做 → 怎么验收 → 怎么上线”排列。
- **20 类需求类型**：App、Web 应用、官网、小程序、H5、硬件/IoT、开放平台、Web 游戏、小游戏、AI 功能、数据类、策略类、运营活动、B 端项目、SaaS、内部工具、商业化/支付、技术改造、合规整改、内容配置。一个需求可以组合多个类型。
- **行业包**：游戏娱乐、风电能源、心理咨询、服务行业、AI 服务，自动补充行业特有的检查项。欢迎贡献更多行业。
- **线下协作**：干系人分工、系统影响、数据影响、接口与架构、外部依赖、待确认事项六张表。
- **全局与交互规范**：通用规则写一次，页面说明只写例外。
- **不完整也清晰**：每章只有“已填写 / 待补充 / 不适用（原因）”三种状态，不编造数字和人名。
- **飞书友好**：不使用需要渲染的流程图，流程和状态都用表格表达，直接粘贴即可。

## 安装

见 [docs/install.md](docs/install.md)。

## 使用示例

```
帮我写个 PRD：心理咨询小程序要加一个在线预约咨询师的功能，用户能看咨询师资料、选时间、付款，咨询前一天提醒。
```

示例输出见 [examples/](examples/)。

## 目录结构

```
skills/caffrey-prd-plus/      技能文件夹（安装这个）
  SKILL.md                    主流程与写作规则
  references/
    prd-template.md           PRD 核心骨架
    section-matrix.md         规模分级与章节取舍
    types/                    20 类需求类型模块
    industries/               行业包
    question-bank.md          追问题库
    quality-checklist.md      自检清单
    change-management.md      版本迭代与变更记录
    user-stories.md           用户故事格式
    test-cases.md             测试用例格式
dist/caffrey-prd-plus-prompt.md   单文件版（给不支持 Skill 的工具）
scripts/build_single.py           生成单文件版的脚本
```

## 贡献

- 新增需求类型：在 `references/types/` 新建文件，并登记到 `types/_index.md`。
- 新增行业包：在 `references/industries/` 新建文件，并登记到 `industries/_index.md`。
- 修改后运行 `python3 scripts/build_single.py` 更新单文件版。

## 许可证

MIT
