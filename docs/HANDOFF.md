# caffrey-prd-plus 交接文档

更新：2026-11-08，接手方为 Codex 和 Claude，当前版本 **v0.11.0**。新对话接手时先读根目录 `AGENTS.md`（所有 Agent 共用的项目规则）和本文件，再读 `CHANGELOG.md` 和两个技能的 `SKILL.md`。**正在进行的任务见第七节“插件化”。**

## 一、项目是什么

给产品经理用的开源技能包（MIT），作者 caffrey neal（GitHub：Caffrey-Li）。

- 仓库：https://github.com/Caffrey-Li/caffrey-prd-plus （公开，main 分支）
- 用户电脑上的工作目录：`~/Projects/Caffrey-PRD/caffrey-prd-plus/`（git 仓库，唯一的工作目录，不要另建克隆）
- 两个技能：

| 技能 | 作用 |
| --- | --- |
| `caffrey-prd-plus` | 把需求整理成中文 PRD；新产品先出总纲再分模块；迭代变更；拆用户故事；定稿后出测试用例；按需出原型图 |
| `caffrey-test-runner` | 按 YAML 测试用例在 Web / App / 桌面应用 / 小程序上执行测试，出结果表和缺陷单，可转 Playwright 脚本 |

## 二、当前状态

| 项目 | 状态 |
| --- | --- |
| GitHub | v0.11.0 |
| 用户电脑 | `caffrey-prd-plus` 已合并为 v0.11.0 的 git 仓库；`caffrey-prd-plus-git` 内容已删除，空文件夹由用户删除 |
| 上一个 Claude 账号 | 已装到 v0.8.1 前后的版本，额度用完，不再使用 |
| 接手方 | Codex（2026-11-07 起）和新 Claude 账号交替开发；入口为 `AGENTS.md`，Claude Code 读 `CLAUDE.md`，Cursor 读 `.cursor/rules/`，都指向它；Grok Bot 用 `docs/GROK-BOT-PROMPT.md` |
| 新 Claude 账号 | 已连接 GitHub，可推送；已拿到 v0.6.0 技能 zip，需换成 v0.11.0 |

## 三、核心设计（已和用户确认，改动前先问）

1. **输出**：中文；最终存放在飞书。流程、用户路径、状态、信息流转、交互时序用 Mermaid 黑白灰图，规则在 `references/diagrams.md`；全包时同时渲染 PNG，lark-cli 导入为飞书画板。
2. **第 1 步必须停下让用户选**：文档版本（精简 / 核心 / 完整，默认推荐精简）、19 个板块（可增减）、交付方式（全包 / 只要文本）。
   **第 2 步先确认再写**（v0.7.0）：列出所有不确定的信息，附建议答案，一轮最多 8 个，全部确认才写；确认不了的放进“本期不做”。文档直接是 v1.0。
3. **定稿后询问**：PRD 定稿后询问是否一起生成测试用例和 Agent 测试方案，用户确认后生成；原型图只在用户要求时出。
4. **写作要求**（v0.7.0）：正文不出现 TBD、待确认、待补充、不适用、暂无；不用括号补充，不写再次说明；每类内容只写在一处，其他地方用编号链接 `[R-01](#R-01)`（F- 功能、R- 规则、G- / I- 规范、D- / E- 字段与枚举、S- 场景）；没有内容就删除；PRD 后不附自检和问题清单。
5. **PRD 结构**：标题、一句话、需求变更记录，然后一至十五章 + 附录，没有“零”；编号固定。第一章先写定位；目标必须达成，写达成时间。字段表必填列只写是 / 否，文本等类型必须写长度 / 格式，预览带斑马纹（v0.8.0）。上线计划、里程碑只写用户提供的，没有就不写（v0.8.1）。8.4 每个页面固定为：线框图 → 入口 → 操作与规则 → 字段与组件。
6. **线框图**：只用黑白灰、以骨架为主。只要文本时用文本线框图（`text` 代码块、只画左边框、横线手机 32 / 电脑 60）；全包时用灰度 SVG 转 PNG。编号 ①②③ 对应「操作与规则」。
7. **全包交付**：`pages/*.md` + `images/`（线框图 PNG、diagram-XX-YY.png）+ `preview.html`（链接跳转、悬停显示内容、返回按钮）+ `manifest.yaml`（Wiki 层级、图、编号）+ `IMPORT.md`，脚本检查链接并在图渲染失败时报错；交付前检查预览交互。不能完成时说明缺口，输出完整可复制内容并转交能打包的 Agent。
8. **测试用例**：飞书表格 + agent 可执行 YAML（meta / env / data / run_rules / cases；元素写成“类型「文案」”；环境值用 `${变量}`；`ENV_TYPE` 为生产时只跑 `prod_safe` 用例）+ Agent 测试方案；方案先覆盖网页，从 PRD 预期出发操作实际页面并输出测试报告。
9. **行业包**：游戏娱乐、风电能源、心理咨询、服务行业、AI 服务；法规类检查项在第 2 步请用户和法务确认，任何版本都不能省。
10. **平台**：Grok Bot 用单文件版（`dist/`）；Claude Code、Codex、Cursor、DeepSeek Harness、Grok Build、WorkBuddy 用一键脚本或插件；Claude 网页 / 桌面版上传技能 zip。

## 四、仓库结构

```
skills/caffrey-prd-plus/       SKILL.md、VERSION、references/（模版、版本取舍、线框图、字段、全包、原型图、20 类需求类型、5 个行业包等）、scripts/make_bundle.py、assets/IMPORT.md
skills/caffrey-test-runner/    SKILL.md、VERSION、references/（用例格式、各端执行指南、结果格式、转 Playwright）、assets/playwright/、scripts/pw_results.js
dist/caffrey-prd-plus-prompt.md  单文件版（只含 PRD 技能），由脚本生成，不要手改
scripts/                       install.sh（一键安装）、release.py（发版）、build_single.py（生成单文件版）
mcp/                           本地 MCP 服务（server.py）、本机 HTTP 预览（http_server.py）与使用说明
tests/                         单元测试：python3 -m pytest -q tests
.claude-plugin/、.cursor-plugin/ 插件清单（隐藏文件夹）
examples/                      同一需求的完整版 / 核心版 / 精简版示例（example-psych-booking*.md）、精简版小需求示例、新产品总纲示例、全包样例 bundle-lite-filter/、测试用例样例、原型图样例、demo/
docs/                          install.md（安装说明）、HANDOFF.md（本文件）、START-PROMPT.md（Claude 开场提示词）、CODEX-START-PROMPT.md、GROK-BOT-PROMPT.md
AGENTS.md                      所有 Agent 共用的项目规则；CLAUDE.md、.cursor/rules/ 指向它
.gitignore                     忽略临时文件（.tmp/、zip、缓存等）
```

## 五、发版流程

1. 修改技能内容；同步修改受影响的示例。
2. `CHANGELOG.md` 顶部写 `## vX.Y.Z（日期）`：新功能或结构调整升次版本号，措辞修正升修订号。
3. 运行 `python3 scripts/release.py X.Y.Z`：同步两个技能的 VERSION、插件清单版本号，重新生成单文件版。
4. 检查：线框图格式（行首只能是 ┌│├└，横线 32 / 60）、表格列数一致、文件引用都存在。
5. 提交并推送 main。Claude 会话的提交作者用 `Claude <noreply@anthropic.com>`；Codex 等其他工具用用户本机的 git 身份。
6. 给 Claude 网页 / 桌面版用户打技能 zip：在 `skills/` 下分别把 `caffrey-prd-plus`、`caffrey-test-runner` 文件夹各压成一个 zip，放在仓库外。
7. 推送不是在用户电脑上做的（如 Claude 云端会话），在用户电脑的项目文件夹中 `git pull`。
8. 按 `AGENTS.md` 清理本次产生的临时文件，更新本文件。

## 六、注意事项

- **推送 GitHub**：Codex 用用户本机的 git 身份推送。Claude 需要在 claude.ai「设置 → 连接器」连接 GitHub 并授权本仓库；Claude 会话中用户电脑的 shell 连不上 GitHub。没有授权时只能让用户手动上传；网页拖拽上传会丢掉隐藏文件夹 `.claude-plugin`、`.cursor-plugin`，这两个文件夹里的文件要在 GitHub 网页上用“Create new file / 编辑”逐个改。
- **更新 Claude 里的技能**：只能上传 zip。替用户上传需要 Chrome 的 Claude 扩展在线；“生成技能确认卡片”只能替换 SKILL.md，不能更新参考文件，不要用。
- **云端环境**：npm 可能被网络策略拦截；预装了 Playwright 1.63。`mmdc` 不要加 `-p` 参数，加了会找不到浏览器。
- **验证示例**：把示例 PRD 正文放进临时目录的 `pages/`，运行 `python3 skills/caffrey-prd-plus/scripts/make_bundle.py <目录> --no-zip`，脚本会渲染 Mermaid、检查所有链接；再用 Playwright 截图看 `preview.html`。
- **Mermaid 状态图**：一个对象一张图，嵌套画多个对象时同名状态会被合并。
- **用户电脑文件夹**：Claude 会话里默认不能删除文件，需要时先向用户申请删除权限；未获权限时多余文件移到 `~/Projects/Caffrey-PRD/_to_delete/`。

## 七、正在进行：插件化，让各个 Agent 接入

**用户需求**（2026-11-05）：“我想将这个做为一个插件，让各个 Agent 可以接入使用，需要如何改造。”

**已给出的方案**：

- 现状：已是开放技能格式，并带 Claude Code、Cursor 插件清单，能读技能的 Agent 已能用；缺口是 Coze、Dify、飞书智能伙伴、ChatGPT、自研 Agent。
- 方案：保留技能，新增一层 MCP 服务。
  - 提示词：写 PRD、改 PRD、出测试用例、执行测试。
  - 工具：`start_prd` 返回第 1 步选择题；`get_questions` 按板块返回第 2 步问题和建议答案；`get_reference` 按需返回模板、类型、行业检查项；`check_prd` 用代码检查 TBD、括号、链接、字段表必填和长度 / 格式、缺图、未提供的上线计划和里程碑；`build_bundle` 复用 make_bundle.py 生成全包。
  - 部署：本地版发 npm 或 pip 包，适合 Claude Code、Cursor、Codex、WorkBuddy；远程版部署成网址，适合网页类 Agent，需要服务器、域名和无头浏览器。
- 仓库改动：新建 `mcp/`，直接读 `skills/` 中的规范；自检清单中能用代码判断的项写成 `check_prd` 脚本，技能和 MCP 共用；`release.py` 同步 npm / pip 包版本，发布并登记 MCP 官方目录；`docs/install.md` 增加各 Agent 的接入配置。
- 限制：MCP 只提供规范、问题和检查，正文仍由接入的 Agent 写；远程版执行测试只能测网页。
- 建议顺序：先做本地版加 `check_prd`，再按需要做远程版。

**用户于 2026-11-07 确认的接入目标**：Claude、Codex、Cursor、Grok Bot、Meta Muse 个人助手、WorkBuddy、Trae、Coze、飞书智能伙伴。各平台的 MCP 能力和接入方式需逐一核实，不把 Muse Code 的能力等同于 Muse 助手。

**进度**：已实现本地 stdio MCP 服务，以及仅监听本机的 HTTP 开发预览，均用 MCP SDK 客户端验证。HTTP 预览不提供访问服务端文件的打包工具；它没有公网身份验证和用户隔离，不能公开。`check_prd` 当前只检查部分待定词、编号链接、括号和字段表，未覆盖原方案所有规则；尚未打包发布 pip / npm 包、登记 MCP 目录、实现带认证的远程服务或逐平台实测。用户目前没有确定部署平台；开发可继续，上线方案需之后确定。

## 八、其他待办

- [ ] 新 Claude 账号：上传 v0.11.0 的两个技能
- [ ] 用户用真实需求试用，根据反馈继续精简
- [ ] Grok Bot：复测单文件版（注意能否完整读取）、线框图、“出原型图”
- [ ] 在真实 Web 项目的测试环境试跑 caffrey-test-runner，调整定位规则
- [ ] 实测 WorkBuddy、Cursor 的安装方式，修正 docs/install.md
- [ ] 考虑建 GitHub Release，附两个技能 zip 和单文件版

## 九、历史参考

- 模版分析与产品方案、PRD 结构建议、线框图与原型图对比画布，都在旧账号的 Claude Artifact 中，新账号无法访问；结论已写进本文件和 CHANGELOG。
- 近期用户反馈的原话和改动：见 CHANGELOG v0.7.0 至 v0.8.1。
