# App 端执行指南（iOS、Android）

## 一、可用方式

| 方式 | 适合 | 怎么准备 |
| --- | --- | --- |
| 模拟器 + computer use | 第一轮提测、探索性验证；不需要写脚本 | iOS 用 Xcode 自带的模拟器（只能在 Mac 上），Android 用 Android Studio 的模拟器；在模拟器中装好测试包；在 Claude 桌面版中开启 computer use，按提示授予屏幕和操作权限 |
| Maestro | 批量执行、回归测试；用例转成 Maestro 流程后可反复运行 | 按 https://docs.maestro.dev 安装 Maestro CLI；连接模拟器或真机；运行 `maestro test 流程文件.yaml` |
| Appium | 团队已有 Appium 体系时沿用 | 按团队现有配置 |

env 中需要：`ENTRY`（包名，如 com.example.app，或安装包路径）、测试账号。

## 二、用 computer use 执行

- 每步先截图确认当前画面，再操作；按可见文字定位元素。
- 系统权限弹窗（定位、通知、相机）：按用例处理；用例没写时选“允许”，并在备注里说明。
- 推送、短信等需要真机的步骤：记为“需人工”。
- 只操作模拟器窗口，不碰电脑上的其他应用。

## 三、转成 Maestro 流程

每条用例转成一个流程文件 `flows/TC-001.yaml`：

```yaml
appId: ${ENTRY}
---
- launchApp
- tapOn: "咨询"
- tapOn: "只看今天可约"
- assertVisible: "林静"
- assertNotVisible: "周远"
- takeScreenshot: TC-001
```

| 用例动作 / 断言 | Maestro 写法 |
| --- | --- |
| open | `launchApp`，再用 `tapOn` 导航到页面 |
| click | `tapOn: "文案"` |
| input | `tapOn: "输入框文案"` 后 `inputText: "值"` |
| back | `back`（Android） |
| scroll | `scroll`，或 `scrollUntilVisible` |
| wait until | `extendedWaitUntil` |
| visible / hidden | `assertVisible` / `assertNotVisible` |

Maestro 没有直接对应的断言（如 count、each、disabled），在流程文件里写注释，并在转换说明中列出，由人工补充或改用 computer use 验证。具体命令以 Maestro 官方文档为准。
