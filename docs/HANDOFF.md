# caffrey-prd-plus 交接文档

更新：2026-11-05，当前版本 **v0.8.0**。新对话接手时先读本文件，再读仓库中的 `CHANGELOG.md` 和两个技能的 `SKILL.md`。

## 一、项目是什么

给产品经理用的开源技能包（MIT），作者 caffrey neal（GitHub：Caffrey-Li）。

- 仓库：https://github.com/Caffrey-Li/caffrey-prd-plus （公开，main 分支）
- 用户电脑上的工作目录：`~/Projects/Caffrey-PRD/caffrey-prd-plus/`（与仓库一致）
- 两个技能：

| 技能 | 作用 |
| --- | --- |
| `caffrey-prd-plus` | 把需求整理成中文 PRD；新产品先出总纲再分模块；迭代变更；拆用户故事；定稿后出测试用例；按需出原型图 |
| `caffrey-test-runner` | 按 YAML 测试用例在 Web / App / 桌面应用 / 小程序上执行测试，出结果表和缺陷单，可转 Playwright 脚本 |

## 二、当前状态

| 项目 | 状态 |
| --- | --- |
| GitHub | v0.8.0 |
| 用户电脑 | v0.8.0 |
| 旧 Claude 账号里装的技能 | v0.4.0（旧，不再维护） |
| 新 Claude 账号 | 还没装技能、还没授权 GitHub |

## 三、核心设计（已和用户确认，改动前先问）

1. **输出**：中文；最终存放在飞书。流程、用户路径、状态、信息流转、交互时序用 Mermaid 黑白灰图，规则在 `references/diagrams.md`；全包时同时渲染 PNG，lark-cli 导入为飞书画板。
2. **第 1 步必须停下让用户选**：文档版本（精简 / 核心 / 完整，默认推荐精简）、19 个板块（可增减）、交付方式（全包 / 只要文本）。
   **第 2 步先确认再写**（v0.7.0）：列出所有不确定的信息，附建议答案，一轮最多 8 个，全部确认才写；确认不了的放进“本期不做”。文档直接是 v1.0。
3. **只出需求文档**：原型图、测试用例只在用户要求时出。
4. **写作要求**（v0.7.0）：正文不出现 TBD、待确认、待补充、不适用、暂无；不用括号补充，不写再次说明；每类内容只写在一处，其他地方用编号链接 `[R-01](#R-01)`（F- 功能、R- 规则、G- / I- 规范、D- / E- 字段与枚举、S- 场景）；没有内容就删除；PRD 后不附自检和问题清单。
5. **PRD 结构**：标题、一句话、需求变更记录，然后一至十五章 + 附录，没有“零”；编号固定。第一章先写定位；目标必须达成，写达成时间。字段表必填列只写是 / 否，文本等类型必须写长度 / 格式，预览带斑马纹（v0.8.0）。8.4 每个页面固定为：线框图 → 入口 → 操作与规则 → 字段与组件。
6. **线框图**：只用黑白灰、以骨架为主。只要文本时用文本线框图（`text` 代码块、只画左边框、横线手机 32 / 电脑 60）；全包时用灰度 SVG 转 PNG。编号 ①②③ 对应「操作与规则」。
7. **全包交付**：`pages/*.md` + `images/`（线框图 PNG、diagram-XX-YY.png）+ `preview.html`（链接跳转、悬停显示内容、返回按钮）+ `manifest.yaml`（Wiki 层级、图、编号）+ `IMPORT.md`，用 `scripts/make_bundle.py` 打包，脚本会检查每个链接。
8. **测试用例**：飞书表格 + agent 可执行 YAML（meta / env / data / run_rules / cases；元素写成“类型「文案」”；环境值用 `${变量}`；`ENV_TYPE` 为生产时只跑 `prod_safe` 用例）。
9. **行业包**：游戏娱乐、风电能源、心理咨询、服务行业、AI 服务；法规类检查项在第 2 步请用户和法务确认，任何版本都不能省。
10. **平台**：Grok Bot 用单文件版（`dist/`）；Claude Code、Codex、Cursor、DeepSeek Harness、Grok Build、WorkBuddy 用一键脚本或插件；Claude 网页 / 桌面版上传技能 zip。

## 四、仓库结构

```
skills/caffrey-prd-plus/       SKILL.md、VERSION、references/（模版、版本取舍、线框图、字段、全包、原型图、20 类需求类型、5 个行业包等）、scripts/make_bundle.py、assets/IMPORT.md
skills/caffrey-test-runner/    SKILL.md、VERSION、references/（用例格式、各端执行指南、结果格式、转 Playwright）、assets/playwright/、scripts/pw_results.js
dist/caffrey-prd-plus-prompt.md  单文件版（只含 PRD 技能），由脚本生成，不要手改
scripts/                       install.sh（一键安装）、release.py（发版）、build_single.py（生成单文件版）
.claude-plugin/、.cursor-plugin/ 插件清单（隐藏文件夹）
examples/                      完整版示例、精简版示例、全包样例、测试用例样例、原型图样例、demo/（演示页面 + 可运行的 Playwright 脚本）
docs/                          install.md（安装说明）、HANDOFF.md（本文件）
```

## 五、发版流程

1. 修改技能内容；同步修改受影响的示例。
2. `CHANGELOG.md` 顶部写 `## vX.Y.Z（日期）`：新功能或结构调整升次版本号，措辞修正升修订号。
3. 运行 `python3 scripts/release.py X.Y.Z`：同步两个技能的 VERSION、插件清单版本号，重新生成单文件版。
4. 检查：线框图格式（行首只能是 ┌│├└，横线 32 / 60）、表格列数一致、文件引用都存在。
5. 提交并推送 main。提交作者用 `Claude <noreply@anthropic.com>`（否则 GitHub 显示未验证）。
6. 给 Claude 网页 / 桌面版用户打技能 zip：在 `skills/` 下分别把 `caffrey-prd-plus`、`caffrey-test-runner` 文件夹各压成一个 zip。
7. 同步用户电脑上的项目文件夹（该文件夹不允许删除文件：先在 `$HOME` 生成 zip，再复制进去解压覆盖）。

## 六、注意事项

- **推送 GitHub**：需要新账号授权（Claude 的 GitHub 应用或 claude.ai 中连接 GitHub）。没有授权时只能让用户手动上传；网页拖拽上传会丢掉隐藏文件夹 `.claude-plugin`、`.cursor-plugin`，这两个文件夹里的文件要在 GitHub 网页上用“Create new file / 编辑”逐个改。
- **更新 Claude 里的技能**：只能上传 zip。替用户上传需要 Chrome 的 Claude 扩展在线；“生成技能确认卡片”只能替换 SKILL.md，不能更新参考文件，不要用。
- **云端环境**：npm 可能被网络策略拦截；预装了 Playwright 1.63，可用其自带的测试运行器。

## 七、待办

- [ ] 在 Claude 中上传 v0.8.0 的两个技能
- [ ] 用户用真实需求试用 v0.8.0，根据反馈继续精简
- [ ] Grok Bot：复测单文件版（约 6 万字，注意能否完整读取）、线框图、“出原型图”
- [ ] 在真实 Web 项目的测试环境试跑 caffrey-test-runner，调整定位规则
- [ ] 实测 WorkBuddy、Cursor 的安装方式，修正 docs/install.md
- [ ] 考虑建 GitHub Release，附两个技能 zip 和单文件版，方便别人下载更新

## 八、历史参考

- 模版分析与产品方案、PRD 结构建议、线框图与原型图对比画布，都在旧账号的 Claude Artifact 中，新账号无法访问；结论已写进本文件和 CHANGELOG。
