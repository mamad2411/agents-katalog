---
name: arkui-codegen
autoTrigger: true
description: |
  ArkUI/ArkTS 代码生成与修改约束。以下场景自动触发：
  1. 直接涉及 UI 代码：生成组件、写页面、实现功能、ArkUI、build、@Component、@Entry、
     @Builder、@Styles、@Extend、@State、@Link、@Prop、鸿蒙、HarmonyOS、ets 文件
  2. 修改/编辑 .ets 文件中的任何代码（改逻辑、改条件、改样式、加功能、删功能、重构）
  3. 用户提供的文件路径以 .ets 结尾，或代码片段包含 build()、@Component 等 ArkUI 特征
  4. 修改红点、角标、Tab、导航、列表项等 UI 相关业务逻辑
---

# ArkUI 代码生成约束

生成或修改 ArkTS UI 代码时，**必须**遵守以下 UI DSL 编译器约束。这些规则由 ArkTS 编译器强制检查（`<ArkTSCheck>`），LSP/codelinter 不一定能提前发现。

---

## Part A: build() 方法体限制（最高频）

build() 内只允许 **UI 描述语句**（组件声明 + 链式属性/事件 + 条件/循环渲染）。以下均**禁止**：

### A1. 禁止声明局部变量

```ts
// ❌ build() 内声明变量
build() {
  const isVip = this.user.isVip
  Column() {
    Text(isVip ? 'VIP' : 'Normal')
  }
}

// ✅ 提升到类属性或 aboutToAppear 预计算
@State isVip: boolean = false

aboutToAppear() {
  this.isVip = this.user.isVip
}

build() {
  Column() {
    Text(this.isVip ? 'VIP' : 'Normal')
  }
}

// ✅ 简单表达式可直接内联
build() {
  Column() {
    Text(this.user.isVip ? 'VIP' : 'Normal')
  }
}
```

### A2. 禁止 console.log / console 调用

```ts
// ❌
build() {
  console.log('rendering')
  Column() { ... }
}

// ✅ 移到生命周期或事件回调
aboutToAppear() {
  console.log('rendering')
}
```

### A3. 禁止 switch 语句

```ts
// ❌
build() {
  Column() {
    switch (this.type) {
      case 'A': Text('A'); break
      case 'B': Text('B'); break
    }
  }
}

// ✅ 用 if/else
build() {
  Column() {
    if (this.type === 'A') {
      Text('A')
    } else if (this.type === 'B') {
      Text('B')
    }
  }
}
```

### A4. 禁止 for/while 循环

```ts
// ❌
build() {
  Column() {
    for (let i = 0; i < this.list.length; i++) {
      Text(this.list[i])
    }
  }
}

// ✅ 用 ForEach
build() {
  Column() {
    ForEach(this.list, (item: string) => {
      Text(item)
    }, (item: string) => item)
  }
}
```

### A5. 禁止调用普通函数（非 @Builder）

```ts
// ❌
build() {
  Column() {
    this.renderHeader() // 普通方法
  }
}

// ✅ 用 @Builder
@Builder
renderHeader() {
  Text('Header')
}

build() {
  Column() {
    this.renderHeader()
  }
}
```

### A6. 禁止在 UI 描述中赋值状态变量

```ts
// ❌
build() {
  this.count = 0
  Column() { ... }
}

// ✅ 放到事件回调
build() {
  Column() {
    Button('Reset')
      .onClick(() => {
        this.count = 0
      })
  }
}
```

### A7. 禁止 return / async / await

```ts
// ❌
build() {
  if (!this.visible) return  // 禁止 return
  const data = await fetchData()  // 禁止 async/await
  Column() { ... }
}

// ✅
build() {
  Column() {
    if (this.visible) {
      // UI 内容
    }
  }
}
```

### A8. 禁止本地作用域块 `{}`

```ts
// ❌
build() {
  Column() {
    {
      Text('hello')
    }
  }
}

// ✅ 直接写组件
build() {
  Column() {
    Text('hello')
  }
}
```

---

## Part B: build() 结构要求

### B1. 只能有一个根组件

```ts
// ❌ 多个根
build() {
  Column() { ... }
  Row() { ... }
}

// ✅ 一个根
build() {
  Column() {
    Row() { ... }
  }
}
```

### B2. @Entry 组件的根必须是容器组件

```ts
// ❌
@Entry
@Component
struct MyPage {
  build() {
    Text('hello')  // Text 是原子组件，不能做 @Entry 的根
  }
}

// ✅
@Entry
@Component
struct MyPage {
  build() {
    Column() {
      Text('hello')
    }
  }
}
```

### B3. ForEach/LazyForEach 不能作为根组件

```ts
// ❌
build() {
  ForEach(this.list, (item: string) => {
    Text(item)
  })
}

// ✅
build() {
  List() {
    ForEach(this.list, (item: string) => {
      ListItem() {
        Text(item)
      }
    })
  }
}
```

---

## Part C: 组件子节点约束

### C1. 原子组件无子节点

`Text`、`Image`、`Blank`、`TextInput`、`TextArea`、`Divider`、`Progress`、`Toggle`、`Rating`、`Slider` 等原子组件不接受子组件。

```ts
// ❌
Text('hello') {
  Image($r('app.media.icon'))
}

// ✅
Column() {
  Text('hello')
  Image($r('app.media.icon'))
}
```

### C2. 单子组件限制

`Button`、`Badge`、`MenuItem` 等只允许一个子组件。

```ts
// ❌
Button() {
  Text('OK')
  Image($r('app.media.icon'))
}

// ✅
Button() {
  Row() {
    Image($r('app.media.icon'))
    Text('OK')
  }
}
```

### C3. 特定子组件类型

```ts
// Tabs 只接受 TabContent 子组件
Tabs() {
  TabContent() { ... }.tabBar('Tab1')
  TabContent() { ... }.tabBar('Tab2')
}

// List 只接受 ListItem / ListItemGroup
List() {
  ListItem() { ... }
  ListItemGroup() { ... }
}

// Grid 只接受 GridItem
Grid() {
  GridItem() { ... }
}

// Swiper 直接接受子组件
Swiper() {
  Text('Page1')
  Text('Page2')
}
```

---

## Part D: 装饰器规则

### D1. @Component 基本要求

- 必须修饰 `struct`（不能是 class）
- struct 必须包含 `build()` 方法
- 不能使用 `export default`，用 `export` 即可

```ts
// ❌
@Component
export default class MyView { ... }

// ✅
@Component
export struct MyView {
  build() { ... }
}
```

### D2. V1/V2 不可混用

- `@Component` (V1) 和 `@ComponentV2` 不能同时修饰一个 struct
- V1 装饰器（@State, @Prop, @Link, @Provide, @Consume, @ObjectLink）不能出现在 @ComponentV2 中
- V2 装饰器（@Local, @Param, @Event, @Monitor, @Computed）不能出现在 @Component 中

### D3. 状态装饰器互斥

一个属性只能有一个状态装饰器：

```ts
// ❌
@State @Prop count: number = 0

// ✅
@State count: number = 0
```

### D4. 初始化规则

```ts
// @State 必须本地初始化
@State count: number = 0  // ✅
@State count: number      // ❌

// @Link 不能本地初始化（由父组件传入）
@Link count: number       // ✅
@Link count: number = 0   // ❌

// @ObjectLink 不能本地初始化
@ObjectLink item: MyObservedClass  // ✅
```

### D5. @Watch 必须配合状态装饰器

```ts
// ❌
@Watch('onCountChange') count: number = 0

// ✅
@State @Watch('onCountChange') count: number = 0
```

### D6. @Builder 限制

```ts
// ❌ 不能用箭头函数
@Builder renderItem = () => { ... }

// ❌ 不能 async
@Builder async renderItem() { ... }

// ✅
@Builder
renderItem() {
  Text('item')
}
```

### D7. @Styles 限制

- 无参数
- 只能使用通用属性和事件

```ts
// ❌
@Styles
cardStyle(radius: number) {
  .width('100%')
  .borderRadius(radius)
}

// ✅
@Styles
cardStyle() {
  .width('100%')
  .borderRadius(8)
}
```

### D8. @Extend 限制

- 必须指定目标组件
- 全局作用域（不能在 struct 内）
- 仅支持内置组件

```ts
// ✅ 全局作用域
@Extend(Text)
function textStyle() {
  .fontSize(16)
  .fontColor('#333')
}
```

---

## Part E: 渲染控制语法

### E1. 条件渲染用 if/else

```ts
build() {
  Column() {
    if (this.isLoading) {
      LoadingProgress()
    } else if (this.hasError) {
      Text('Error')
    } else {
      this.contentBuilder()
    }
  }
}
```

### E2. ForEach 提供 key 生成器

```ts
// ❌ 缺少 keyGenerator，可能导致渲染异常
ForEach(this.list, (item: ItemType) => {
  Text(item.name)
})

// ✅ 提供唯一 key
ForEach(this.list, (item: ItemType) => {
  Text(item.name)
}, (item: ItemType) => item.id.toString())
```

### E3. LazyForEach 仅用于指定容器

LazyForEach 只能在 `List`、`Grid`、`Swiper`、`WaterFlow` 中使用，且需要实现 `IDataSource`。

```ts
// ✅
List() {
  LazyForEach(this.dataSource, (item: ItemType) => {
    ListItem() {
      Text(item.name)
    }
  }, (item: ItemType) => item.id.toString())
}
```

---

## Part F: 最佳实践

### F1. 复杂 UI 拆分子组件

超过 50 行的 build() 应拆分为子 @Component 或 @Builder。

### F2. @Builder 复用重复片段

```ts
@Builder
itemRow(icon: Resource, title: string) {
  Row() {
    Image(icon).width(24).height(24)
    Text(title).margin({ left: 8 })
  }
  .height(48)
  .padding({ left: 16, right: 16 })
}
```

### F3. 状态装饰器最小化

- 父→子单向：用 `@Prop`
- 父↔子双向：用 `@Link`
- 跨层级：用 `@Provide`/`@Consume`
- 不需要 UI 刷新的数据不加状态装饰器

### F4. 大列表性能

```ts
// 用 LazyForEach + cachedCount
List() {
  LazyForEach(this.dataSource, (item: ItemType) => {
    ListItem() { ... }
  }, (item: ItemType) => item.id.toString())
}
.cachedCount(5)
```

### F5. @Reusable 组件复用

频繁创建销毁的列表项组件标记 `@Reusable`：

```ts
@Reusable
@Component
struct ListItemView {
  @State item: ItemType = new ItemType()

  aboutToReuse(params: Record<string, Object>) {
    this.item = params['item'] as ItemType
  }

  build() { ... }
}
```

### F6. 避免在 build() 中计算

```ts
// ❌ build() 中做计算（且声明变量违规）
build() {
  const total = this.items.reduce((sum, item) => sum + item.price, 0)
  Text(`Total: ${total}`)
}

// ✅ V2 用 @Computed
@ComponentV2
struct MyView {
  @Local items: ItemType[] = []

  @Computed
  get total(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0)
  }

  build() {
    Text(`Total: ${this.total}`)
  }
}

// ✅ V1 在 aboutToAppear / 事件回调中预计算
@Component
struct MyView {
  @State items: ItemType[] = []
  @State total: number = 0

  aboutToAppear() {
    this.total = this.items.reduce((sum, item) => sum + item.price, 0)
  }

  build() {
    Text(`Total: ${this.total}`)
  }
}
```

---

## 生码模板

### 基础 @Component

```ts
@Component
export struct MyComponent {
  @Prop title: string = ''

  build() {
    Column() {
      Text(this.title)
        .fontSize(16)
    }
    .width('100%')
  }
}
```

### @Entry 页面

```ts
@Entry
@Component
struct MyPage {
  @State message: string = 'Hello'

  build() {
    Column() {
      Text(this.message)
        .fontSize(20)
    }
    .width('100%')
    .height('100%')
  }
}
```

### @CustomDialog

```ts
@CustomDialog
struct MyDialog {
  controller: CustomDialogController = new CustomDialogController({ builder: MyDialog() })
  onConfirm: () => void = () => {}

  build() {
    Column() {
      Text('Title').fontSize(18)
      Row() {
        Button('Cancel')
          .onClick(() => this.controller.close())
        Button('Confirm')
          .onClick(() => {
            this.onConfirm()
            this.controller.close()
          })
      }
      .justifyContent(FlexAlign.SpaceAround)
      .width('100%')
    }
    .padding(24)
  }
}
```

### @ComponentV2

```ts
@ComponentV2
export struct MyV2Component {
  @Param title: string = ''
  @Local count: number = 0
  @Event onCountChange: (count: number) => void = () => {}

  @Computed
  get displayText(): string {
    return `${this.title}: ${this.count}`
  }

  build() {
    Column() {
      Text(this.displayText)
      Button('+1')
        .onClick(() => {
          this.count++
          this.onCountChange(this.count)
        })
    }
  }
}
```
