---
name: ddt
description: 检查并纠正代码里的过度封装、过度抽象、薄 helper、薄类型拆分、实例属性绕传参数和编码规范问题；当用户要求内联小函数、合并薄类型、提升代码可读性或检查代码是否符合项目规范时使用。
---

# ddt

DDT 表示 dont-do-that packaging。

这个 skill 用来约束一种常见坏味道，就是明明代码很短、语义很直接、调用关系也很单一，却还要硬拆一层函数、硬拆一层类型，或者把 class 已经持有的实例状态沿着私有方法一层层传下去，最后让人类阅读路径变长，理解成本变高。

## 规范读取要求

如果这个 skill 要审查或修改项目代码，必须先让 agent 读取仓库内的 `CLAUDE.md` 和存在的 `AGENTS.md` 文件，再判断代码是否符合编码规范。检查时要同时看项目规范、用户长期约束和当前代码，不允许只按这个 skill 的过度封装规则下结论。

重点检查这些规范是否被破坏：service 查询和变更职责拆分、复杂业务是否进入 `logic/`、类型是否放在 `src/types/**`、业务数字是否使用 `enum/**`、数据库读写是否优先使用 Kysely、SQL 别名是否具备可读性、static 方法内是否显式用类名调用同类 static 方法、导入是否合并、导出函数和 class static 方法是否有简短 JSDoc。

## 什么时候触发

当用户表达下面这类意思时，优先使用这个 skill。

| 用户表达                                         | 重点检查                                |
| ------------------------------------------------ | --------------------------------------- |
| 代码过度封装、过度抽象、拆得太碎                 | 小函数、小类型和中间层是否只有形式价值  |
| 某个函数只有 2 到 5 行，且只被一个地方调用       | 是否应该内联回调用处                    |
| 某个类型本来一份就够，却被拆成多个薄类型来回跳转 | 是否应该合并成直接类型                  |
| 要求把 helper 内联回主流程                       | helper 是否只有一次调用、没有新业务语义 |
| 要求把薄类型合并，减少阅读跳转                   | 子类型是否没有稳定复用边界              |
| 要求代码更贴近人类阅读                           | 是否为了形式分层牺牲主流程可读性        |
| class 内部把实例属性当参数层层传递               | 是否应该让私有方法直接读取 `this.xxx`   |

## 总决策图

遇到封装、类型拆分或参数传递时，先走这个判断图。目标不是“越少越好”，而是收掉没有真实收益的层。

```text
看到一层函数 / 类型 / 参数传递
        │
        ▼
它是否被多个地方稳定复用？
        ├─ 是 ──► 保留，并确认命名和注释能表达业务语义
        │
        └─ 否
             │
             ▼
它是否明显降低主流程认知负担？
        ├─ 是 ──► 保留，但避免继续拆更薄的层
        │
        └─ 否
             │
             ▼
它是否表达独立业务边界、外部协议或测试边界？
        ├─ 是 ──► 保留，并让边界更清楚
        │
        └─ 否 ──► 收回：内联函数、合并类型、删除透传参数或中间层
```

## 核心原则

先判断拆分有没有真实收益，再决定保留还是收回。

如果一个函数只有很少几行，只有一个调用方，而且函数名也没有提供新的业务语义，默认这是过度封装，应该直接内联回调用处。不要为了看起来更模块化就保留这种薄函数。

如果一个类型只是从另一个类型里薄薄切出一层，没有形成稳定复用，也没有显著降低理解成本，默认这是过度拆分，应该合并回更直接的类型定义。只有在某个子类型真的被多个地方独立使用，或者拆出来以后能明显降低主类型复杂度时，才保留拆分。

代码优先服务人类阅读，不优先服务形式上的解耦。局部轻微耦合通常比多跳一层更好读。

class 内部已经稳定存在的实例状态，不要再为了“显式传参”沿着私有方法链路传递。私有方法本来就是实例行为，直接读 `this.xxx` 往往比 `const xxx = this.xxx; this.a(xxx); this.b(xxx);` 更短，也更能表达这个值属于对象状态。只有参数来自当前调用现场、会随每次调用变化、方法需要脱离实例复用，或者显式传入能明显降低耦合时，才保留参数。

兜底逻辑也要看真实收益。只有输入来自不稳定外部边界，或者缺少兜底会造成明确错误时，才保留防御分支。不要为了“更稳”给已经有确定生命周期、确定状态机、确定类型约束的流程再加一层兜底。

## 函数判断表

遇到小函数时，按这张表判断。只要命中“倾向内联”的多项，就收回到调用处。

| 判断点     | 倾向内联                                                 | 倾向保留                                   |
| ---------- | -------------------------------------------------------- | ------------------------------------------ |
| 行数       | 2 到 5 行简单逻辑                                        | 逻辑已经长到会压坏主流程                   |
| 调用方     | 只有一个调用方，且离定义点很近                           | 多处复用，且复用不是偶然                   |
| 函数名     | 只是复述实现，比如 parse、build、normalize、remember、to | 名字表达稳定业务动作或领域概念             |
| 主流程阅读 | 调用者仍然必须点进去看细节                               | 抽出后主流程明显更清楚                     |
| 测试价值   | 没有独立测试价值                                         | 需要独立测试或独立注释                     |
| 边界意义   | 只是赋值、一次分支、一次 map、一次字符串判断             | 表达外部协议、复杂算法或不可忽略的业务边界 |

只有下面这些情况才建议保留独立函数：函数被多个地方复用；函数承载了清晰、稳定、不可忽略的业务语义；函数内部逻辑已经长到会压坏主流程阅读；函数需要独立测试、独立注释或独立复用。

## 类型判断表

遇到类型拆分时，先看一份类型能不能直接把当前问题表达清楚。如果能，就不要为了层次感继续拆。

| 判断点   | 倾向合并                                     | 倾向拆分                                         |
| -------- | -------------------------------------------- | ------------------------------------------------ |
| 消费范围 | 子类型只服务一个父类型，且只在一个地方被消费 | 子类型被多个模块共享                             |
| 语义边界 | 只是改名、摘字段或一层别名                   | 子类型本身有稳定业务语义                         |
| 阅读路径 | 拆完以后名字变多、跳转变多                   | 主类型已经长到影响阅读，拆分后更清楚             |
| 外部契约 | 只是内部中间形态                             | API 返回体、数据库行、消息体、事件载荷等独立边界 |
| 复用价值 | 没有独立复用                                 | 多处独立使用，且未来语义稳定                     |

只有下面这些情况才建议拆出子类型：子类型会被多个模块共享；某个嵌套结构本身就有稳定语义；主类型已经长到影响阅读，拆出来能明显提升可读性；这个子类型本身就是一个独立边界，比如 API 返回体、数据库行结构、消息体结构。

## 实例属性和参数传递判断表

class 内部私有方法之间传参时，先判断这个参数是不是已经来自当前实例属性。

| 判断点   | 倾向直接读实例属性                             | 倾向保留参数                             |
| -------- | ---------------------------------------------- | ---------------------------------------- |
| 参数来源 | 调用方只是 `const value = this.value` 后继续传 | 参数来自当前调用现场                     |
| 传递路径 | 多个私有方法只接收再转交                       | 每层都会形成新的局部含义                 |
| 方法边界 | 方法只服务当前 class                           | 方法需要脱离实例复用                     |
| 调用变化 | 值是对象固定状态                               | 值每次调用会按分支变化                   |
| 测试收益 | 传参只让阅读路径更长                           | 显式传参能让测试明显更简单，且不制造绕行 |

如果调用方只是从 `this` 读出值再传给同类私有方法，默认这是不必要的参数绕行。目标方法直接读取实例属性，通常更能表达这个值属于对象状态。

## 兜底逻辑判断表

| 情况                                              | 动作             | 理由                             |
| ------------------------------------------------- | ---------------- | -------------------------------- |
| 输入来自用户、网络、数据库、外部 SDK 或历史脏数据 | 保留必要兜底     | 外部边界不稳定                   |
| 状态已经由生命周期、事件顺序或类型定义保证        | 删除重复兜底     | 防御分支只会制造误导             |
| 缺少兜底会造成明确错误或数据损坏                  | 保留，并注释原因 | 这是业务保护，不是噪音           |
| 兜底只是为了“更稳”，没有可触发路径                | 删除             | 读者会误以为存在未说明的异常状态 |

## 执行动作

当确认存在过度封装时，直接做这些事。

| 问题                             | 动作                              |
| -------------------------------- | --------------------------------- |
| 单一调用方的小函数               | 内联回调用处，删掉 helper         |
| 无收益的中间层                   | 删除透传层，让调用关系更短        |
| 过薄的类型                       | 合并回主类型或更直接的边界类型    |
| 只是转手传递的实例属性参数       | 让目标私有方法直接读取 `this.xxx` |
| 主流程已经保证不会触发的兜底分支 | 删除重复防御                      |
| 必要注释被薄封装掩盖             | 保留注释，但只解释关键意图        |

如果用户是在 review 代码而不是要求直接修改，就明确指出哪些函数或类型属于过度封装，并给出一句话理由，重点讲清楚为什么这层拆分让阅读变差。

## 输出要求

给出的建议或修改，默认遵守这些表达习惯。

直接指出该内联的点和该合并的点。不要泛泛而谈抽象层次。不要为了凑整再引入新的 helper。不要把刚收回去的逻辑换个名字再包一层。

如果要解释原因，用一句短话说清楚就够了，比如只有一个调用方且逻辑过薄，内联后更好读。或者这个子类型没有独立复用价值，合并后阅读路径更短。

## 反模式清单

下面这些默认都属于 dont-do-that packaging。

| 反模式                                                                 | 为什么不好                             |
| ---------------------------------------------------------------------- | -------------------------------------- |
| 只有一个调用方的 2 到 5 行薄函数                                       | 多一次跳转，却没有补充业务语义         |
| 只做一次字段拷贝、一次简单判断、一次字符串匹配、一次 map 包装的 helper | 代码本身已经足够直观                   |
| 为了拆而拆的 parseX、buildX、normalizeX、rememberX、toX                | 名字看起来工整，但仍要点进去看实现     |
| 只包一层取值、改名、透传的 getter、selector、mapper、convert 函数      | 把简单数据流藏到了另一个位置           |
| 本来一个类型能表达清楚，却拆成主类型加子类型再加别名类型               | 类型跳转变多，边界反而变模糊           |
| 没有复用价值，却只为了工整把嵌套对象强行拆出去                         | 形式分层压过了阅读路径                 |
| 单点简单查询或判断的业务数字机械新增枚举                               | 读者还要跳到 enum 文件才能知道简单含义 |
| class 已经持有的实例属性先读出来再传给同类私有方法                     | 误导读者以为这是调用现场的可变输入     |
| 主流程已经保证不会触发的防御分支                                       | 让人误以为存在未说明的异常路径         |

单点简单查询或判断的业务数字，不要为了避开“魔法数字”机械新增枚举。比如逻辑删除字段 `doDelete = 0` 只在一个很短的查询里使用时，直接写在查询条件里更清楚；只有状态值会跨多个文件、多个分支、多个业务动作复用，或者数字本身难以从上下文理解时，才抽到 `enum/**`。

主流程已经通过事件顺序、状态变量或类型定义保证不会触发的防御分支，不要再作为“兜底”保留。比如 `textEnd` 已经负责关闭正文消息时，工具调用开始分支里就不应该再补一次正文关闭。

## 例子

例子一。

下面这种写法就是典型的薄函数过度封装。`handleMessageEvent()` 只有两行真正逻辑，而且只在一个 `case` 里被调用。

```ts
case AgentFlowEnum.MESSAGE: {
  this.handleMessageEvent(chunk, messageData);
  break;
}

private handleMessageEvent(chunk: DifyMsgSSERes, messageData: MessagePayload) {
  messageData.data.answer = chunk.answer ?? "";
  this.writeMessagePayload(messageData);
}
```

更合适的写法是直接内联回 `switch` 分支，阅读路径更短。

```ts
case AgentFlowEnum.MESSAGE: {
  messageData.data.answer = chunk.answer ?? "";
  this.writeMessagePayload(messageData);
  break;
}
```

例子二。

下面这种写法也是典型的为了拆而拆。`parseRound()` 只有正则匹配和 `parseInt()`，而且只被 `resolveRound()` 用一次。

```ts
private resolveRound(logData: AgentMessageData): number {
  const round = this.parseRound(logData.label);
  if (round !== null) {
    return round;
  }

  if (logData.parent_id !== null) {
    const parentRound = this.roundMap.get(logData.parent_id);
    if (parentRound !== undefined) {
      return parentRound;
    }
  }

  throw new Error(`agent_log round not found: ${logData.label}`);
}

private parseRound(label: string | undefined): number | null {
  if (!label) return null;
  const matched = label.trim().match(/^ROUND (\d+)$/u);
  if (!matched) {
    return null;
  }
  return Number.parseInt(matched[1], 10);
}
```

更合适的写法是把这几行逻辑直接收回 `resolveRound()`。

```ts
private resolveRound(logData: AgentMessageData): number {
  const matched = logData.label.trim().match(/^ROUND (\d+)$/u);
  if (matched) {
    return Number.parseInt(matched[1], 10);
  }

  if (logData.parent_id !== null) {
    const parentRound = this.roundMap.get(logData.parent_id);
    if (parentRound !== undefined) {
      return parentRound;
    }
  }

  throw new Error(`agent_log round not found: ${logData.label}`);
}
```

例子三。

下面这种类型拆分也属于过度。读代码的人需要先看 `DifyMsgSSERes`，再跳到 `DifyWorkflowEventData`，再跳到 `AgentMessageData`，但实际这里并没有形成稳定复用边界。

```ts
export type AgentMessageData = {
  id: string;
  parent_id: string | null;
  label: string;
  status: string;
};

export type DifyWorkflowEventData = AgentMessageData & {
  title?: string;
  outputs?: {
    structured_output?: Record<string, string>;
    answer_text?: string;
  };
};

export type DifyMsgSSERes = {
  event: string;
  data: DifyWorkflowEventData;
};

const logData = chunk.data;
```

更合适的写法是用一份类型直接把当前边界讲清楚，消费时也不需要再额外跳转。

```ts
export type AgentMessageData = {
  id: string;
  parent_id: string | null;
  label: string;
  status: string;
  title?: string;
  outputs?: {
    structured_output?: Record<string, string>;
    answer_text?: string;
  };
};

export type DifyMsgSSERes = {
  event: string;
  data: AgentMessageData;
};

const logData = chunk.data;
```

例子四。

下面这种 getter、selector、mapper、convert 风格的方法，如果本质上只是包一层取值改名透传，也属于过度封装。

```ts
const labels = toolList.map((tool) => this.mapToolLabel(tool));

private mapToolLabel(tool: AgentTool) {
  return tool.label;
}
```

更合适的写法是直接把这层薄包装收掉。

```ts
const labels = toolList.map((tool) => tool.label);
```

例子五。

下面这种枚举拆分看起来符合“不要魔法数字”，但实际只有一个查询使用，阅读者还得跳到 enum 文件才能知道 `NORMAL` 就是 `0`，属于为了形式牺牲可读性。

```ts
export const AgentAskTemplateDeleteStatus = {
  NORMAL: 0,
  DELETED: 1,
} as const;

export class AgentQuery {
  /**
   * 查询 Agent 问法模板列表
   */
  static async getAskTemplateList() {
    return await db
      .selectFrom("wzj_agent_ask_template")
      .select(["id", "ask", "description", "updateTime", "createTime"])
      .where("doDelete", "=", AgentAskTemplateDeleteStatus.NORMAL)
      .execute();
  }
}
```

更合适的写法是让这个单点条件直接留在查询里。`doDelete` 已经表达了逻辑删除语义，`0` 在这个上下文里没有必要再包一层枚举。

```ts
export class AgentQuery {
  /**
   * 查询 Agent 问法模板列表
   */
  static async getAskTemplateList() {
    return await db
      .selectFrom("wzj_agent_ask_template")
      .select(["id", "ask", "description", "updateTime", "createTime"])
      .where("doDelete", "=", 0)
      .execute();
  }
}
```

例子六。

下面这种嵌套 if 也属于不必要的阅读负担。外层只判断事件类型，内层只判断阶段，而且内层没有对应的 `else` 分支，读者需要多进一层才知道真正执行条件。

```ts
} else if (streamEvent.kind === "reasoningDelta") {
  if (this.phase !== "message" && this.phase !== "toolCall") {
    this.reasoningContent += streamEvent.delta;
    this.phase = "reasoning";
  }
}
```

更合适的写法是把同一动作的前置条件合并到一个 `else if` 里，让分支入口就表达完整执行条件。

```ts
} else if (
  streamEvent.kind === "reasoningDelta" &&
  this.phase !== "message" &&
  this.phase !== "toolCall"
) {
  this.reasoningContent += streamEvent.delta;
  this.phase = "reasoning";
}
```

例子七。

下面这种写法也是典型的参数绕行。`flashModel` 已经是当前实例的属性，调用方只是取出来再传给同类私有方法，中间没有形成新的输入语义。

```ts
async streamEvents() {
  const model = await this.flashModel;
  const workflow = this.createGraph(model);
  return await workflow.streamEvents();
}

private createGraph(model: ChatModel) {
  const defaultAgent = this.createDefaultAgent(model);
  return new StateGraph().addNode("default", defaultAgent.graph).compile();
}

private createDefaultAgent(model: ChatModel) {
  return createAgent({ model });
}
```

更合适的写法是让真正消费实例状态的方法直接读取 `this.flashModel`，调用链不再携带这个多余参数。

```ts
async streamEvents() {
  const workflow = await this.createGraph();
  return await workflow.streamEvents();
}

private async createGraph() {
  const defaultAgent = await this.createDefaultAgent();
  return new StateGraph().addNode("default", defaultAgent.graph).compile();
}

private async createDefaultAgent() {
  const model = await this.flashModel;
  return createAgent({ model });
}
```

## 决策偏好

拿不准时，优先少一层。

能直接放在当前上下文里读懂，就不要额外封装。

能用一个类型讲清楚，就不要先拆再绕回来。
