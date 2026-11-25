---
name: midscenejs-docs
description: 关于自动规划（Auto Planning）和即时操作（Instant Action）的区别，请参考 [API](/api.md) 文档。
metadata:
  source: llms.txt
  source_url: https://midscenejs.com/zh/llms-full.txt
  generated: 2026-05-11T07:20:10.605Z
---

# YAML 脚本运行器

> 关于自动规划（Auto Planning）和即时操作（Instant Action）的区别，请参考 [API](/api.md) 文档。

关于自动规划（Auto Planning）和即时操作（Instant Action）的区别，请参考 [API](/api.md) 文档。

## Available Resources

### url: /zh/android-api-reference.md

### Action Space（动作空间）

### AndroidDevice {#androiddevice}

- **yadb**
  - URL: https://github.com/ysbing/YADB

- **Scrcpy 截图模式**
  - URL: #scrcpy

### AndroidAgent {#androidagent}

- **API constructors**
  - URL: ./api#common-parameters

- **Android 平台特定动作**
  - URL: ./automate-with-scripts-in-yaml#the-android-part

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **`AndroidDevice`**
  - URL: #androiddevice

- **Android 快速开始**
  - URL: ./android-getting-started

### url: /zh/android-getting-started.md

### 配置 AI 模型服务

### 准备工作

- **Android Studio**
  - URL: https://developer.android.com/studio

- **Android environment variables**
  - URL: https://developer.android.com/tools/variables

### 试用 Playground（零代码）

- **模型配置**
  - URL: /zh/model-config.md

### 开始体验

### 集成 Midscene Agent

### 进阶

### 常见问题

- **ADBKeyBoard**
  - URL: https://github.com/senzhk/ADBKeyBoard

### 更多

- **API 参考（通用）**
  - URL: /zh/api.md#interaction-methods

- **Android Agent API**
  - URL: /zh/android-api-reference.md

- **https://github.com/web-infra-dev/midscene-example/blob/main/android/javascript-sdk-demo**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/android/javascript-sdk-demo

### url: /zh/android-introduction.md

### 案例展示

### 在 Android 上试用 Midscene Playground

### 下一步

- **快速开始**
  - URL: /zh/android-getting-started.md

- **使用 JavaScript SDK**
  - URL: /zh/android-getting-started.md

- **使用 YAML 格式的自动化脚本**
  - URL: /zh/automate-with-scripts-in-yaml.md

### url: /zh/api.md

### 构造器

- **PuppeteerAgent**
  - URL: /zh/web-api-reference.md#puppeteer-agent

- **PlaywrightAgent**
  - URL: /zh/web-api-reference.md#playwright-agent

- **AgentOverChromeBridge**
  - URL: /zh/web-api-reference.md#chrome-bridge-agent

- **Android API 参考**
  - URL: /zh/android-api-reference.md

- **iOS API 参考**
  - URL: /zh/ios-api-reference.md

- **自定义界面 Agent**
  - URL: /zh/integrate-with-any-interface.md

- **Link**: `outputFormat: 'single-html' | 'html-and-external-assets'`: 控制报告的生成格式。`'single-html'`（默认）将所有截图作为 base64 内嵌到单个 HTML 文件中，并把 `reportFileName` 作为 HTML 文件名。`'html-and-external-assets'` 将截图保存为独立的 PNG 文件到子目录，并把 `reportFileName` 作为该目录名，适用于报告文件过大的场景。**注意**：使用 `'html-and-external-assets'` 时，报告必须通过 HTTP 服务器或 CDN 地址访问，无法直接使用 `file://` 协议打开。这是因为浏览器的 CORS（跨源资源共享）限制会阻止从 file 协议加载相对路径的本地图片。如需在本地测试，可在报告目录下启动简易的 HTTP 服务器。进入报告目录后运行以下命令之一：
* 使用 Node.js：`npx serve`
* 使用 Python：`python -m http.server` 或 `python3 -m http.server`
  然后通过 `
  - URL: http://localhost:3000`（或终端显示的端口）访问报告。

### 交互方法

- **缓存功能**
  - URL: /zh/caching.md

- **模型策略**
  - URL: /zh/model-strategy.md

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **通过图像提示**
  - URL: #通过图像提示

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **YADB**
  - URL: https://github.com/ysbing/YADB

- **通过图像提示**
  - URL: #通过图像提示

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

### 数据提取

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

### 更多方法

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

- **使用图片作为提示词**
  - URL: #使用图片作为提示词

### 属性

### 深度定位（deepLocate）

### 使用图片作为提示词

### 报告合并工具

### url: /zh/automate-with-scripts-in-yaml.md

- **Web**
  - URL: https://github.com/web-infra-dev/midscene-example/tree/main/yaml-scripts-demo

- **Android**
  - URL: https://github.com/web-infra-dev/midscene-example/tree/main/android/yaml-scripts-demo

- **Computer（Mac/Windows/Linux）**
  - URL: https://github.com/web-infra-dev/midscene-example/tree/main/computer/yaml-scripts-demo

### 配置 AI 模型服务

### 脚本文件结构

- **缓存功能文档**
  - URL: /zh/caching.md

### 注意事项

### url: /zh/awesome-midscene.md

### 社区项目

- **midscene-ios**
  - URL: https://github.com/lhuanyu/midscene-ios

- **midscene-pc**
  - URL: https://github.com/Mofangbao/midscene-pc

- **midscene-pc-docker**
  - URL: https://github.com/Mofangbao/midscene-pc-docker

- **Midscene-Python**
  - URL: https://github.com/Python51888/Midscene-Python

- **midscene-java**
  - URL: https://github.com/Master-Frank/midscene-java

- **midscene-java**
  - URL: https://github.com/alstafeev/midscene-java

### 如何贡献

### 收录标准

### url: /zh/blog-introducing-instant-actions-and-deep-think.md

### 即时操作（Instant Actions）- 让交互表现更稳定

### 深度思考（Deep Think）- 让元素定位更准确

### url: /zh/bridge-mode.md

### 配置 AI 模型服务

### 快速开始

### 在 YAML 自动化脚本中使用桥接模式

### 远程访问配置

### FAQ

- **模型策略**
  - URL: /zh/model-strategy.md

### 更多

- **API 参考**
  - URL: /zh/api.md#interaction-methods

- **API 参考（Web）**
  - URL: /zh/web-api-reference.md#chrome-bridge-agent

- **https://github.com/web-infra-dev/midscene-example/blob/main/bridge-mode-demo**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/bridge-mode-demo

### url: /zh/caching.md

### 缓存文件和存储

### 缓存策略

### 使用 Midscene 的 Playwright AI Fixture

### 缓存清理

### FAQ

### url: /zh/changelog.md

### v1.7 - 灵活处理报告文件、支持 Qwen 3.6 模型

### 示例

- **Android API**
  - URL: /zh/android-api-reference.md

### v1.6 - CDP 连接、双指缩放与多模型增强

- **Skills 文档**
  - URL: /zh/skills.md

- **MCP 服务**
  - URL: /zh/mcp.md

- **iOS API**
  - URL: /zh/ios-api-reference.md

### v1.5 - HarmonyOS（鸿蒙）自动化支持

### v1.4 - Skills：让 AI 助手直接操控你的设备

### v1.3 - PC 桌面自动化支持

### v1.2 - 智谱 AI 开源模型支持与文件上传支持

- **GLM-V 模型配置**
  - URL: /zh/model-common-config.md#glm-v

- **AutoGLM 模型配置**
  - URL: /zh/model-common-config.md#auto-glm

### v1.1 - `aiAct`深度思考与可扩展的 MCP SDK

### v1.0 - Midscene v1.0 正式发布！

- **iOS 自动化 - 美团下单咖啡**
  - URL: /zh/showcases.md#ios

- **iOS 自动化 - Twitter 自动点赞 @midscene\_ai 首条推文**
  - URL: /zh/showcases.md#ios

- **Android 自动化 - 懂车帝查看小米 SU7 参数**
  - URL: /zh/showcases.md#android

- **Android 自动化 - Booking 预订圣诞酒店**
  - URL: /zh/showcases.md#android

- **MCP 集成 - Midscene MCP 操作界面发布 prepatch 版本**
  - URL: /zh/showcases.md#mcp

### V0.30 - 缓存管理升级与移动端体验优化

- **midscene-java**
  - URL: /zh/awesome-midscene.md

### v0.29 - 新增 iOS 平台支持

### v0.28 - 扩展界面操作能力，构建你自己的 GUI 自动化 Agent（预览特性）

- **Awesome Midscene**
  - URL: /zh/awesome-midscene.md

### v0.27 - 核心模块重构，断言与报告功能全面升级

### v0.26 - 工具链全面接入 [Rslib](https://github.com/web-infra-dev/rslib)，大幅提高开发体验、降低贡献门槛

- **freezePageContext**
  - URL: /zh/api.md#agentfreezepagecontext

- **keyboardDismissStrategy**
  - URL: /zh/integrate-with-android.md#androiddevice-的构造函数

- **Rslib**
  - URL: https://github.com/web-infra-dev/rslib

### v0.25 - 支持使用图像作为 AI prompt 输入

- **使用图片作为提示词**
  - URL: /zh/api.md#%E4%BD%BF%E7%94%A8%E5%9B%BE%E7%89%87%E4%BD%9C%E4%B8%BA%E6%8F%90%E7%A4%BA%E8%AF%8D

- **reportFileName**
  - URL: /zh/api.md

- **LLMs.txt**
  - URL: /zh/llm-txt.md

### v0.24 - Android 自动化支持 MCP 调用

- **MCP 服务**
  - URL: /zh/mcp.md

### v0.23 - 全新报告样式与 YAML 脚本能力增强

### v0.22 - Chrome 扩展录制功能上线

### v0.21 - Chrome 扩展界面升级

### v0.20 - 支持传入 XPath 定位元素

### v0.19 - 支持获取完整的执行过程数据

### v0.18 - 回放报告功能增强

- **自定义报告节点 API 文档**
  - URL: /zh/api.md#agentlogscreenshot

- **Android 更多配置项 API 文档**
  - URL: /zh/integrate-with-android.md#androiddevice-%E7%9A%84%E6%9E%84%E9%80%A0%E5%87%BD%E6%95%B0

### v0.17 - 让 AI 看见页面 DOM

### v0.16 - 支持 MCP

### v0.15 - Android 自动化上线！

### v0.14 - 即时操作 API

### v0.13 - 深度思考模式

### v0.12 - 集成 Qwen 2.5 VL

### v0.11.0 - UI-TARS 模型缓存

- **开启缓存**
  - URL: /zh/caching.md

### v0.10.0 - UI-TARS 模型上线

### v0.9.0 - 桥接模式上线！

### v0.8.0 - Chrome 插件

### v0.7.0 - Playground 能力

### v0.6.0 - 支持字节豆包模型

### v0.5.0 - 支持 GPT-4o 结构化输出

### v0.4.0 - 支持使用 Cli

### v0.3.0 - 支持 AI HTML 报告

### v0.2.0 - 通过自然语言控制 puppeteer

### v0.1.0 - 通过自然语言控制 playwright

### url: /zh/common/get-cdp-url.md

- **Link**: **BrowserBase**：在  注册并获取你的 CDP URL
  - URL: https://browserbase.com

- **Link**: **Browserless**：使用  或运行你自己的实例
  - URL: https://browserless.io

### url: /zh/common/prepare-ios.md

### 准备工作

- **Run Prebuilt WDA**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/run-prebuilt-wda/

- **Real Device Configuration**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/real-device-config/

### url: /zh/common/setup-env.md

### 配置 AI 模型服务

### url: /zh/common/start-experience.md

### url: /zh/common/troubleshooting-llm-connectivity.md

### 模型服务连接问题排查

### url: /zh/computer-api-reference.md

### Agent 创建

- **Xvfb**
  - URL: https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml

### 设备管理

### ComputerAgent

### 可用操作

### 示例

### TypeScript 类型

### 另请参阅

- **通用 API 参考**
  - URL: /zh/api.md

- **模型配置**
  - URL: /zh/model-config.md

- **缓存**
  - URL: /zh/caching.md

### url: /zh/computer-getting-started.md

### 配置 AI 模型服务

### 系统要求

### 试用 Playground（零代码）

- **模型配置**
  - URL: /zh/model-config.md

### 开始体验

### 与 Midscene Agent 集成

### 通过 RDP 连接远程 Windows 桌面

- **FreeRDP**
  - URL: https://www.freerdp.com/

### 多显示器支持

### 使用示例

### 环境检查

### 常见问题

### 下一步

- **API 参考**
  - URL: /zh/computer-api-reference.md

- **使用 YAML 格式自动化脚本**
  - URL: /zh/automate-with-scripts-in-yaml.md

- **YAML 脚本运行器**
  - URL: /zh/yaml-script-runner.md

- **缓存提高效率**
  - URL: /zh/caching.md

### url: /zh/computer-introduction.md

### 案例展示

### 在 Playground 中试用

### 核心功能

### 使用场景

### 下一步

- **开始使用**
  - URL: /zh/computer-getting-started.md

- **API 参考**
  - URL: /zh/computer-api-reference.md

- **使用 YAML 格式自动化脚本**
  - URL: /zh/automate-with-scripts-in-yaml.md

### url: /zh/consume-report-file.md

### 示例

### 使用命令行工具解析

### 使用 JavaScript SDK 解析

### 关于 JSON 和 Markdown 的内容字段

### url: /zh/data-privacy.md

### url: /zh/faq.md

### 各平台常见问题

- **Web 浏览器 - Playwright**
  - URL: /zh/integrate-with-playwright.md#faq

- **Web 浏览器 - Puppeteer**
  - URL: /zh/integrate-with-puppeteer.md#faq

- **Web 浏览器 - Chrome 插件**
  - URL: /zh/quick-experience.md#faq

- **Web 浏览器 - 桥接模式**
  - URL: /zh/bridge-mode.md#faq

- **Android**
  - URL: /zh/android-getting-started.md#常见问题

- **iOS**
  - URL: /zh/ios-getting-started.md#常见问题

- **HarmonyOS**
  - URL: /zh/harmony-getting-started.md#常见问题

- **PC 桌面**
  - URL: /zh/computer-getting-started.md#常见问题

### 会有哪些信息发送到 AI 模型？

### 我的模型服务商需要在请求中添加指定的 header

### 如何配置 midscene\_run 目录？

- **缓存**
  - URL: /zh/caching.md

### 如何提升运行效率？

- **缓存**
  - URL: /zh/caching.md

### 如何通过链接控制报告中播放器的默认回放样式？

### 元素定位出现偏移

### 豆包手机是否使用了 Midscene 作为底层方案？

### url: /zh/harmony-api-reference.md

### Action Space（动作空间）

### HarmonyDevice {#harmonydevice}

### HarmonyAgent {#harmonyagent}

- **API constructors**
  - URL: ./api#common-parameters

- **HarmonyOS 平台特定动作**
  - URL: ./automate-with-scripts-in-yaml#harmony-部分

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **Link**: `uri: string` —— 可以是应用 bundle name（如 `com.huawei.hmos.settings`），也可以是在 `appNameMapping` 中注册的应用名称。如果传入 ` 或 `https://` 开头的 URL，将通过浏览器打开。
  - URL: http://`

- **`HarmonyDevice`**
  - URL: #harmonydevice

- **HarmonyOS 快速开始**
  - URL: ./harmony-getting-started

### url: /zh/harmony-getting-started.md

### 配置 AI 模型服务

### 准备工作

- **DevEco Studio**
  - URL: https://developer.huawei.com/consumer/cn/deveco-studio/

- **HarmonyOS 命令行工具**
  - URL: https://developer.huawei.com/consumer/cn/download/

### 试用 Playground（零代码）

- **模型配置**
  - URL: /zh/model-config.md

### 开始体验

### 集成 Midscene Agent

### 进阶

### 更多

- **API 参考（通用）**
  - URL: /zh/api.md#interaction-methods

- **HarmonyOS Agent API**
  - URL: /zh/harmony-api-reference.md

- **https://github.com/web-infra-dev/midscene-example/blob/main/harmony/javascript-sdk-demo**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/harmony/javascript-sdk-demo

### 常见问题

### url: /zh/harmony-introduction.md

### 案例展示

### 在 HarmonyOS 上试用 Midscene Playground

### 下一步

- **快速开始**
  - URL: /zh/harmony-getting-started.md

- **使用 JavaScript SDK**
  - URL: /zh/harmony-getting-started.md

- **使用 YAML 格式的自动化脚本**
  - URL: /zh/automate-with-scripts-in-yaml.md

### url: /zh/index.md

### url: /zh/integrate-with-android.md

### Preparation

- **Android Studio**
  - URL: https://developer.android.com/studio

- **Android command-line tools**
  - URL: https://developer.android.com/studio#command-line-tools-only

### 配置 AI 模型服务

### 集成 Midscene

### 构造函数与接口

- **yadb**
  - URL: https://github.com/ysbing/YADB

- **构造器**
  - URL: /zh/api.md

### 扩展自定义交互动作

### 更多

- **API 参考**
  - URL: /zh/api.md

### FAQ

- **ADBKeyBoard**
  - URL: https://github.com/senzhk/ADBKeyBoard

### url: /zh/integrate-with-any-interface.md

### 演示和社区项目

- **演示项目**
  - URL: https://github.com/web-infra-dev/midscene-example/tree/main/custom-interface

- **Android (adb) Agent**
  - URL: https://github.com/web-infra-dev/midscene/blob/main/packages/android/src/device.ts

- **iOS (WebDriverAgent) Agent**
  - URL: https://github.com/web-infra-dev/midscene/blob/main/packages/ios/src/device.ts

- **midscene-ios**
  - URL: https://github.com/lhuanyu/midscene-ios

### 配置 AI 模型服务

### 实现你自己的界面类

### API 参考

- **Zod**
  - URL: https://www.npmjs.com/package/zod

### 常见问题（FAQ）

### url: /zh/integrate-with-harmony.md

### Preparation

- **DevEco Studio**
  - URL: https://developer.huawei.com/consumer/cn/deveco-studio/

- **HarmonyOS 命令行工具**
  - URL: https://developer.huawei.com/consumer/cn/download/

### 配置 AI 模型服务

### 集成 Midscene

### 构造函数与接口

- **构造器**
  - URL: /zh/api.md

### 扩展自定义交互动作

### 更多

- **API 参考**
  - URL: /zh/api.md

### FAQ

### url: /zh/integrate-with-ios.md

### 关于 WebDriver 和 Midscene 的关系

### 准备 WebDriver 服务

- **Run Prebuilt WDA**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/run-prebuilt-wda/

- **Real Device Configuration**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/real-device-config/

### 配置 AI 模型服务

### 集成 Midscene

### 构造函数与接口

- **构造器**
  - URL: /zh/api.md

### 扩展自定义交互动作

### 更多

- **API 参考**
  - URL: /zh/api.md

### FAQ

### 更多

- **API 参考**
  - URL: /zh/api.md

### url: /zh/integrate-with-playwright.md

### 配置 AI 模型服务

### 直接集成 Midscene Agent

### 在 Playwright 的测试用例中集成 Midscene

- **Link**: `outputFormat`: 控制报告的生成格式。`'single-html'`（默认）将所有截图作为 base64 内嵌到单个 HTML 文件中。`'html-and-external-assets'` 将截图保存为独立的 PNG 文件到子目录，适用于报告文件过大的场景。**注意**：使用 `'html-and-external-assets'` 时，报告必须通过 HTTP 服务器访问，无法直接使用 `file://` 协议打开（因为浏览器的 CORS 限制会阻止从 file 协议加载相对路径的本地图片）。进入报告目录后运行以下命令之一：

* 使用 Node.js：`npx serve`
* 使用 Python：`python -m http.server` 或 `python3 -m http.server`

然后通过 `
  - URL: http://localhost:3000`（或终端显示的端口）访问报告。

### Advanced

- **Link**: **BrowserBase**：在  注册并获取你的 CDP URL
  - URL: https://browserbase.com

- **Link**: **Browserless**：使用  或运行你自己的实例
  - URL: https://browserless.io

### FAQ

- **Agent**
  - URL: /zh/api.md#%E6%9E%84%E9%80%A0%E5%99%A8

- **Yaml**
  - URL: /zh/automate-with-scripts-in-yaml.md#web-%E9%83%A8%E5%88%86

### 更多

- **API 参考**
  - URL: /zh/api.md#interaction-methods

- **Playwright Agent API**
  - URL: /zh/web-api-reference.md#playwright-agent

- **直接集成 Playwright**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/playwright-demo

### url: /zh/integrate-with-puppeteer.md

### 配置 AI 模型服务

### 集成 Midscene Agent

### Advanced

- **Link**: **BrowserBase**：在  注册并获取你的 CDP URL
  - URL: https://browserbase.com

- **Link**: **Browserless**：使用  或运行你自己的实例
  - URL: https://browserless.io

### FAQ

### 更多

- **API 参考**
  - URL: /zh/api.md#interaction-methods

- **Puppeteer Agent API**
  - URL: /zh/web-api-reference.md#puppeteer-agent

- **https://github.com/web-infra-dev/midscene-example/blob/main/puppeteer-demo**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/puppeteer-demo

### url: /zh/introduction.md

### 功能特性

- **与 Puppeteer 集成**
  - URL: /zh/integrate-with-puppeteer.md

- **JavaScript SDK**
  - URL: /zh/android-getting-started.md

- **JavaScript SDK**
  - URL: /zh/ios-getting-started.md

- **JavaScript SDK**
  - URL: /zh/integrate-with-any-interface.md

- ****交互 API****: 与用户界面交互。
  - URL: /zh/api.md#interaction-methods

- **文档**
  - URL: /zh/mcp.md

- ****使用缓存，提高执行效率****: 使用缓存能力重放脚本，提高执行效率。
  - URL: /zh/caching.md

### 演示案例

- **iOS 自动化 - 美团下单咖啡**
  - URL: /zh/showcases.md#ios

- **iOS 自动化 - Twitter 自动点赞 @midscene\_ai 首条推文**
  - URL: /zh/showcases.md#ios

- **Android 自动化 - 懂车帝查看小米 SU7 参数**
  - URL: /zh/showcases.md#android

- **Android 自动化 - Booking 预订东京圣诞酒店**
  - URL: /zh/showcases.md#android

- **MCP 集成 - Midscene MCP 操作界面发布 prepatch 版本**
  - URL: /zh/showcases.md#mcp

### 零代码快速体验

- **Chrome 插件**
  - URL: /zh/quick-experience.md

- **Android Playground**
  - URL: /zh/android-getting-started.md#试用-playground-零代码

- **iOS Playground**
  - URL: /zh/ios-getting-started.md#试用-playground

### 视觉语言模型驱动

### 两种自动化风格

### 资源

- **https://midscenejs.com**
  - URL: https://midscenejs.com/

- **https://github.com/web-infra-dev/midscene-example**
  - URL: https://github.com/web-infra-dev/midscene-example

- **https://midscenejs.com/api.html**
  - URL: /zh/api.md

- **https://github.com/web-infra-dev/midscene**
  - URL: https://github.com/web-infra-dev/midscene

### 社区

- **Web Infra 团队微信公众号**
  - URL: https://lf3-static.bytednsdoc.com/obj/eden-cn/vhaeh7vhabf/web-infra-wechat.jpg

- **Discord**
  - URL: https://discord.gg/2JyBHxszE4

- **在 X 上关注我们**
  - URL: https://x.com/midscene_ai

- **飞书交流群**
  - URL: https://applink.larkoffice.com/client/chat/chatter/add_by_link?link_token=693v0991-a6bb-4b44-b2e1-365ca0d199ba

### 致谢

- **Rsbuild**
  - URL: https://github.com/web-infra-dev/rsbuild

- **UI-TARS**
  - URL: https://github.com/bytedance/ui-tars

- **Qwen2.5-VL**
  - URL: https://github.com/QwenLM/Qwen2.5-VL

- **scrcpy**
  - URL: https://github.com/Genymobile/scrcpy

- **appium-adb**
  - URL: https://github.com/appium/appium-adb

- **appium-webdriveragent**
  - URL: https://github.com/appium/WebDriverAgent

- **YADB**
  - URL: https://github.com/ysbing/YADB

- **libnut-core**
  - URL: https://github.com/nut-tree/libnut-core

- **Puppeteer**
  - URL: https://github.com/puppeteer/puppeteer

- **Playwright**
  - URL: https://github.com/microsoft/playwright

### License

### url: /zh/ios-api-reference.md

### Action Space（动作空间）

### IOSDevice {#iosdevice}

- **API 参考（通用）**
  - URL: ./api#interaction-methods

### IOSAgent {#iosagent}

- **API constructors**
  - URL: ./api#common-parameters

- **iOS 平台特定动作**
  - URL: ./automate-with-scripts-in-yaml#the-ios-part

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **`IOSDevice`**
  - URL: #iosdevice

- **iOS 快速开始**
  - URL: ./ios-getting-started

- **与任意界面集成**
  - URL: ./integrate-with-any-interface

### url: /zh/ios-getting-started.md

### 配置 AI 模型服务

### 准备工作

### 准备工作

- **Run Prebuilt WDA**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/run-prebuilt-wda/

- **Real Device Configuration**
  - URL: https://appium.github.io/appium-xcuitest-driver/5.12/real-device-config/

### 试用 Playground（零代码）

- **模型配置**
  - URL: /zh/model-config.md

### 开始体验

### 集成 Midscene Agent

### API 参考与更多资源

### 常见问题

### 更多

- **API 参考（通用）**
  - URL: /zh/api.md#interaction-methods

- **iOS Agent API**
  - URL: /zh/ios-api-reference.md

- **https://github.com/web-infra-dev/midscene-example/blob/main/ios/javascript-sdk-demo**
  - URL: https://github.com/web-infra-dev/midscene-example/blob/main/ios/javascript-sdk-demo

### url: /zh/ios-introduction.md

### 案例展示

### 在 Playground 中试用

### 关于 WebDriverAgent

### 下一步

- **使用 JavaScript SDK**
  - URL: /zh/ios-getting-started.md

- **使用 YAML 格式的自动化脚本**
  - URL: /zh/automate-with-scripts-in-yaml.md

### url: /zh/llm-txt.md

### 目录概览

- **llms.txt**
  - URL: https://midscenejs.com/zh/llms.txt

- **llms-full.txt**
  - URL: https://midscenejs.com/zh/llms-full.txt

### 使用方法

### url: /zh/mcp-android.md

### 使用场景

### 设置 Midscene MCP

- **选择 AI 模型**
  - URL: /zh/model-config.md

- **Android adb**
  - URL: https://developer.android.com/tools/adb?hl=zh-cn

### 可用工具

### 常见问题

- **Link**: 网页 URL：如 `
  - URL: https://www.example.com`

### url: /zh/mcp.md

### MCP 工具列表

### 查看执行报告

### 配置 MCP

- **模型策略**
  - URL: /zh/model-strategy.md

- **iOS 快速开始**
  - URL: /zh/ios-getting-started.md

- **模型策略**
  - URL: /zh/model-strategy.md

- **Android 快速开始**
  - URL: /zh/android-getting-started.md

- **模型策略**
  - URL: /zh/model-strategy.md

### 实现自己的 MCP

### url: /zh/model-common-config.md

### 配置环境变量的方式

### 常用模型配置

- **https://github.com/zai-org/GLM-V**
  - URL: https://github.com/zai-org/GLM-V

- **https://huggingface.co/zai-org/GLM-4.6V**
  - URL: https://huggingface.co/zai-org/GLM-4.6V

- **https://github.com/zai-org/Open-AutoGLM**
  - URL: https://github.com/zai-org/Open-AutoGLM

- **https://huggingface.co/zai-org/AutoGLM-Phone-9B**
  - URL: https://huggingface.co/zai-org/AutoGLM-Phone-9B

- **Images and Vision guide**
  - URL: https://developers.openai.com/api/docs/guides/images-vision

- **Images and Vision guide**
  - URL: https://developers.openai.com/api/docs/guides/images-vision

- **Computer use guide**
  - URL: https://developers.openai.com/api/docs/guides/tools-computer-use

### 其他模型

- **阿里云**
  - URL: https://www.aliyun.com/

### 多模型示例：GPT-5.4 规划/理解 + Qwen 3.5 视觉定位 {#gpt54-planning-insight-qwen35}

### 更多

### url: /zh/model-config.md

### 必选配置

- **Images and Vision guide**
  - URL: https://developers.openai.com/api/docs/guides/images-vision

### 高阶配置（可选）

### 仍兼容的模型配置（不推荐）

### 使用 JavaScript 配置参数

### 常见问题

- **`createOpenAIClient`**
  - URL: /zh/api.md#自定义-openai-客户端

- **`createOpenAIClient`**
  - URL: /zh/api.md#自定义-openai-客户端

### url: /zh/model-strategy.md

- **豆包 Seed 模型**
  - URL: /zh/model-common-config.md#doubao-seed-model

- **Qwen3.X 系列**
  - URL: /zh/model-common-config.md#qwen3x

- **智谱 GLM-V**
  - URL: /zh/model-common-config.md#glm-v

- **智谱 AutoGLM**
  - URL: /zh/model-common-config.md#auto-glm

- **Gemini-3-Flash**
  - URL: /zh/model-common-config.md#gemini-3-pro

- **GPT-5.4**
  - URL: /zh/model-common-config.md#gpt-5-4

### 背景知识：UI 自动化的技术路线

### Midscene 采用纯视觉路线来完成元素定位

### 推荐使用的视觉模型

### 高阶特性：多模型配合

### 如何调优执行效果？

### 更多

### 模型服务连接问题排查

### url: /zh/quick-experience.md

### 安装 Chrome 扩展

### 配置 AI 模型服务

### 开始体验

### FAQ

### url: /zh/showcases-android.md

### url: /zh/showcases-computer.md

### url: /zh/showcases-harmony.md

### url: /zh/showcases-ios.md

### url: /zh/showcases-mcp.md

### url: /zh/showcases-web.md

### url: /zh/showcases.md

### Web

### iOS

### Android

### HarmonyOS

### Computer

### MCP

### 社区案例

### url: /zh/skills.md

### 支持的平台

### 安装

### 模型配置

### 使用 Skills

### 案例：编码 Agent 写完代码后自行验证功能

### 更多应用场景

### 更多

### url: /zh/use-javascript-to-optimize-ai-automation-code.md

### 使用 JavaScript 和结构化 API 编写自动化脚本

### 常用的结构化 API 方法

### 选用 `aiAct` 与结构化代码，哪个才是最优解？

### 想要轻松编写结构化代码？

- **Link**
  - URL: https://midscenejs.com/use-javascript-to-optimize-ai-automation-code.md

- **Link**
  - URL: https://midscenejs.com/api.md

### url: /zh/web-api-reference.md

### Action Space（动作空间）

### PuppeteerAgent {#puppeteer-agent}

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **集成到 Puppeteer**
  - URL: ./integrate-with-puppeteer

### PlaywrightAgent {#playwright-agent}

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **集成到 Playwright**
  - URL: ./integrate-with-playwright

### Chrome Bridge Agent {#chrome-bridge-agent}

- **API 参考（通用）**
  - URL: ./api#interaction-methods

- **桥接模式**
  - URL: ./bridge-mode

### url: /zh/yaml-script-runner.md

### 使用 `.env` 配置环境变量

### 开始使用

### 命令行工具的高级用法

### 命令行参数

- **glob**
  - URL: https://www.npmjs.com/package/glob

### 常见问题

## How to Use This Skill

Reference these resources when working with YAML 脚本运行器.