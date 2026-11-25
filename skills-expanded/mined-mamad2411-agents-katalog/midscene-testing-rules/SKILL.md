---
name: midscene-testing-rules
description: |
  约束基于 Midscene.js 的自动化测试用例写法规范，特别是 Android 微信小程序环境的兼容处理。
  当用户需要编写、修改或审查 Midscene.js 测试脚本、测试用例时，务必使用此 skill。
  适用于 PC（桌面 Web）、Web（Puppeteer）、Android（App/小程序）三种平台的测试代码生成与审查。
  如果用户提到"写个测试"、"自动化测试"、"midscene"、"用例"、"aiTap"、"aiAssert"等，立即触发此 skill。
---

# Midscene.js 测试用例写法规范

项目在原版 Midscene.js 基础上进行了平台兼容封装（特别是 Android 微信小程序），编写用例时必须遵循以下规范。

## 单条用例格式

```ts
import { AndroidAgent } from "@midscene/android";

export default {
  description: "用例描述，简短清晰",
  run: async (agent: AndroidAgent) => {
    try {
      await agent.aiTap('点击"登录"按钮', { deepThink: false });
    } catch (error) {
      throw new Error("操作失败的描述", { cause: error });
    }
  },
};
```

### 约束

1. **必须 `export default`**，包含 `description` 和 `run`
2. `description` 用中文简短描述
3. `run` 是 `async` 函数，参数根据平台选对应 Agent（Android 用 `AndroidAgent`，PC 用 `ComputerAgent`，Web 用 `PuppeteerAgent`）
4. **每个操作步骤独立 `try-catch`**，不要把多个操作放在一个 try 里。如果多个步骤之间逻辑不相关，必须拆分为独立的 try-catch，这样报错时能精确定位到具体步骤：

   ```ts
   // ✅ 正确：逻辑无关的步骤各自独立 try-catch
   try {
     await agent.aiTap('点击底部菜单"我的"', { deepThink: false });
   } catch (error) {
     console.error('❌ 点击底部菜单失败:', error);
     throw new Error('点击底部菜单失败', { cause: error });
   }

   try {
     await agent.aiTap('点击"优惠券"', { deepThink: false });
   } catch (error) {
     console.error('❌ 点击优惠券失败:', error);
     throw new Error('点击优惠券失败', { cause: error });
   }

   // ❌ 错误：多个无关步骤混在一起，报错时无法区分是哪一步
   try {
     await agent.aiTap('点击底部菜单"我的"', { deepThink: false });
     await agent.aiTap('点击"优惠券"', { deepThink: false });
   } catch (error) {
     throw new Error('操作失败', { cause: error });
   }
   ```

5. 错误处理：`throw new Error('描述', { cause: error })`，cause 必须保留。catch 中建议先用 `console.error('❌ ...', error)` 输出，方便调试时查看完整错误堆栈
6. 所有 AI 操作传 `{ deepThink: false }` 提升速度

## Android 平台特殊规范（重点）

### 输入：禁止 `agent.aiInput`，必须用 `adbInput`

微信小程序沙箱环境导致 `agent.aiInput` 异常，必须使用团队封装的 `adbInput`：

```ts
// ❌ 错误
await agent.aiInput("用户名输入框", "admin");

// ✅ 正确
import { adbInput } from "@/tests/utils/android";
await adbInput("用户名输入框", "admin");
```

### 常用封装

```ts
import {
  openApp, // 打开 config.ts 配置的 App
  openWxMiniprogram, // 打开 config.ts 配置的微信小程序
  adbTap, // UI 坐标系点击
  adbInput, // 绕过小程序限制的输入
  testSignIn, // 检查并自动登录
} from "@/tests/utils/android";
import { sleep } from "@/tests/utils";
```

### 断言

```ts
try {
  await agent.aiAssert("已登录，右上角显示用户名");
  console.info("✅ 断言成功");
} catch (error) {
  console.info("❌ 断言失败");
  throw new Error("断言失败原因", { cause: error });
}
```

断言描述要**具体**，避免"页面显示正常"这类模糊描述。

## 任务编排（入口文件 test.ts）

```ts
import {
  createAgent,
  defaultOptions,
  onTesting,
  runTasks,
  Tasks,
} from "@/tests/utils";

const tasks: Tasks = [
  () => import("@/tests/project-c/tasks/通用/打开app/index"),
  () => import("@/tests/project-c/tasks/登录/index"),
];

const options = { ...defaultOptions, platform: "Android" };

onTesting(async () => {
  const agent = await createAgent(options.platform);
  await runTasks(agent, tasks);
}, options);

export default {
  description: "C端自动化测试",
  tasks,
  options,
};
```

约束：

- `tasks` 用动态导入 `() => import('...')`
- `options` 必须含 `platform` 字段
- 使用 `onTesting` 包装入口

## 命名规范

- 入口文件：`test.ts`
- 单条用例：`tasks/分类/用例名/index.ts`
- 分类和用例目录用中文描述

## 完整示例：Android 小程序登录检查

```ts
import { AndroidAgent } from "@midscene/android";
import { testSignIn } from "@/tests/utils/android";
import { sleep } from "@/tests/utils";

export default {
  description: "检查登录状态",
  run: async (agent: AndroidAgent) => {
    try {
      await agent.aiAct('点击底部菜单"我的"', { deepThink: false });
      await testSignIn(agent);
      await sleep(1000);
      await agent.aiTap('点击"首页"', { deepThink: false });
    } catch (error) {
      throw new Error("检查登录失败", { cause: error });
    }
  },
};
```

## 参考

- [Midscene.js Android API](https://midscenejs.com/zh/android-api-reference.html)
- [Midscene.js PC API](https://midscenejs.com/zh/computer-api-reference.html)
