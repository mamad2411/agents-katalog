---
name: pureadmin-utils
description: "@pureadmin/utils 完整工具函数 API 手册。需要查阅具体函数签名和用法时加载。"
---

# @pureadmin/utils 完整 API 手册

> **共 140+ 工具函数**，项目已安装。**导入方式**：`import { 函数名 } from "@pureadmin/utils"`。开发时优先使用这些工具函数，不要重新造轮子。
> **签名来源**：从 `node_modules/@pureadmin/utils/dist/index.d.mts` 源码验证。
> **在线文档**：[pure-admin-utils 文档](https://pure-admin-utils.netlify.app/)

---

## Vue Hooks

### useECharts

ECharts 初始化与自适应。

```typescript
const { setOptions, echarts, resize } = useECharts(chartRef, options?);
setOptions({ series: [...] });
```

**签名**：`(elRef: ElementRef<HTMLDivElement>, options?: EchartOptions) => { echarts, setOptions, getInstance, showLoading, hideLoading, clear, resize, getGlobalProperties, getDom, getWidth, getHeight, getOption, appendData, getDataURL, getConnectedDataURL, addTooltip }`

**EchartOptions**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `theme` | `'default' \| 'light' \| 'dark' \| string` | 主题色 |
| `renderer` | `'canvas' \| 'svg'` | 渲染模式，默认 `canvas` |
| `devicePixelRatio` | `number` | 设备像素比 |
| `ssr` | `boolean` | 服务端渲染 |
| `useDirtyRect` | `boolean` | 脏矩形渲染 |
| `width` | `number \| string` | 显式指定宽度 |
| `height` | `number \| string` | 显式指定高度 |

**UtilsEChartsOption**（setOptions 参数）扩展 EChartsOption：
| 参数 | 类型 | 说明 |
|------|------|------|
| `clear` | `boolean` | 是否清空当前实例，默认 `true` |
| `addTooltip` | `'x' \| 'y' \| true` | 给轴添加 Tooltip |
| `delay` | `number` | resize 防抖延时 |
| `resize` | `boolean` | 是否监听页面 resize，默认 `true` |
| `container` | `string \| ElementRef \| (string \| ElementRef)[]` | 监听指定容器尺寸变化 |

---

### useDark

暗黑模式切换。

```typescript
const { isDark, toggleDark } = useDark();
```

**签名**：`(options?: { selector?: 'html' \| 'body', className?: string }) => { isDark: ShallowRef<boolean>, toggleDark: () => void }`

---

### useDraggable

元素拖拽（弹窗类）。

```typescript
const { init, draggable, transform, reset } = useDraggable(dialogRef, headerRef);
```

**签名**：`(targetRef: ElementRef | string, dragRef: ElementRef | string, args?: ArgsDraggable) => { draggable, dragging, transform: { offsetX, offsetY }, init, open, close, reset }`

**ArgsDraggable**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `dragRefStyle` | `CSSProperties` | 拖拽区域样式，默认 `{ cursor: "move", userSelect: "none" }` |
| `resize` | `boolean \| number` | 页面 resize 时是否恢复初始位置，默认 `true` |

---

### useWatermark

水印生成。

```typescript
const { setWatermark, clear } = useWatermark();
setWatermark("ZgAdmin");
```

**签名**：`(appendEl?: ElementRef, resizeReDraw?: boolean) => { setWatermark, clear }`

**setWatermark 参数**：`(str: string, attr?: attr)`

**attr 配置**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `font` | `string` | `'normal 16px Arial, ...'` | 字体 |
| `color` | `string` | `'rgba(128,128,128,0.3)'` | 字体颜色 |
| `width` | `number` | `250` | 宽度 |
| `height` | `number` | `100` | 高度 |
| `rotate` | `number` | `-10` | 旋转角度 |
| `zIndex` | `string` | `'100000'` | z-index |
| `gradient` | `Array<{value, color}>` | — | 字体渐变色 |
| `shadowConfig` | `Array<any>` | — | 阴影 [shadowBlur, shadowColor?, shadowOffsetX?, shadowOffsetY?] |
| `globalAlpha` | `number` | — | 透明度 0.0-1.0 |
| `lineHeight` | `number` | `20` | 多行行高 |
| `wrap` | `string` | `'、'` | 换行标识符 |
| `textAlign` | `CanvasTextAlign` | — | 文本对齐 |
| `image` | `string` | — | 图片路径 |
| `forever` | `boolean` | `false` | 不可删除 |
| `verticalOffset` | `number` | `0` | 偶数列垂直偏移 |

---

### useLoader

动态加载 CSS/JS。

```typescript
const { loadCss, loadScript } = useLoader();
loadScript({ src: "https://cdn..." });
```

**签名**：`(destroy?: boolean) => { loadCss, loadScript }`

**OptionsScript**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `src` | `string \| string[]` | 资源链接地址 |
| `element` | `'head' \| 'body' \| HTMLElement` | 标签插入位置 |

---

### useResizeObserver

监听元素尺寸。

```typescript
const { stop, restart } = useResizeObserver(elRef, (entries) => {...});
```

**签名**：`(target: ElementRef | string | (ElementRef | string)[], callback: ResizeObserverCallback, options?: UseResizeObserverOptions) => { stop, restart }`

**UseResizeObserverOptions**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `time` | `number` | `40` | 防抖延迟(ms) |
| `immediate` | `boolean` | `true` | 初始化时立刻触发 |
| `box` | `'content-box' \| 'border-box' \| 'device-pixel-content-box'` | `'content-box'` | 观察模式 |

---

### useScrollTo

缓动滚动。

```typescript
const { start, stop } = useScrollTo({
  el: elRef,
  to: 0,
  directions: "scrollTop",
  duration: 500,
  callback: (msg) => {}
});
```

**签名**：`(options: ScrollOptions) => { start, stop }`

**ScrollOptions**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `el` | `HTMLElement` | 滚动对象实例（必填） |
| `to` | `number` | 滚动到某个位置（必填） |
| `directions` | `'scrollTop' \| 'scrollLeft'` | 滚动方向（必填） |
| `duration` | `number` | 滚动时长(ms)，默认 `0` |
| `callback` | `(msg?) => void` | 完成回调 |

---

### useCopyToClipboard

复制到剪贴板。

```typescript
const { copied, update } = useCopyToClipboard();
update("复制的文本");
```

**签名**：`(defaultValue?: string) => { clipboardValue: ShallowRef<string>, copied: ShallowRef<boolean>, update: (value: string | RefValue<string>) => void }`

---

### useAttrs

增强的 attrs 过滤。

```typescript
const attrs = useAttrs({ excludeListeners: true, excludeKeys: ["class"] });
```

**签名**：`(params?: { excludeListeners?: boolean, excludeKeys?: string[] }) => RefValue<Recordable> | {}`

---

### useGlobal

获取 Vue 全局属性。

```typescript
const global = useGlobal();
```

**签名**：`<T>() => T`

---

### useDynamicComponent

TSX 中加载动态组件。

```typescript
const component = useDynamicComponent("MyComponent");
```

**签名**：`(component: string) => Component`

---

## 金额（Amount）

| 函数 | 签名 | 说明 |
|------|------|------|
| `addZero` | `(val: any) => string \| boolean` | 在数值后加 `.00` |
| `centsToDollars` | `(val: any, format?: boolean) => any` | 分转元，format 控制整金额是否加 `.00` |
| `dollarsToCents` | `(val: number, digit?: number) => number` | 元转分，digit 转换倍数默认 100 |
| `getDecimalPlaces` | `(val: string \| number) => number` | 获取数值的小数位数 |
| `priceUppercase` | `(val: any, format?: string) => string` | 金额转大写汉字，format 为"整"后缀 |
| `priceToThousands` | `(amount: number, options?: AmountOpt) => string` | 金额千分位格式化，AmountOpt: `{ digit?, round? }` |

---

## 数组（Array）

| 函数 | 签名 | 说明 |
|------|------|------|
| `isIncludeAllChildren` | `(c: Array, m: Array) => boolean` | 母体数组是否包含子体全部元素 |
| `intersection` | `(...rest: any[]) => any[]` | 数组交集 |
| `swapOrder` | `(arr: any[], fIndex: number, sIndex: number) => any[]` | 数组两元素互换（改变原数组） |
| `getKeyList` | `(arr: any, key: string, duplicates?: boolean) => any[]` | 从对象数组提取指定 key 列表，默认去重 |
| `randomDivide` | `(total: number, parts: number, options?: DivideOptions) => number[]` | 总数随机分配到指定份数 |
| `arrayAllExist` | `(array: any[], checkArray: any[]) => boolean` | 数组是否包含另一数组所有值（基本类型） |
| `arrayAllExistDeep` | `(array: any[], checkArray: any[]) => boolean` | 数组是否包含另一数组所有值（深度对比） |
| `arrayAnyExist` | `(array: any[], checkArray: any[]) => boolean` | 数组是否包含另一数组任意值（基本类型） |
| `arrayAnyExistDeep` | `(array: any[], checkArray: any[]) => boolean` | 数组是否包含另一数组任意值（深度对比） |
| `extractFields` | `<T, K extends keyof T>(array: T[], ...keys: K[]) => Pick<T, K>[]` | 提取对象数组中的指定字段 |

**DivideOptions**：`{ minPerPart?, maxPerPart?, order?: 'asc' | 'desc' | 'random' }`

---

## 树形（Tree）

| 函数 | 签名 | 说明 |
|------|------|------|
| `buildHierarchyTree` | `(tree: any[], pathList?) => any` | 扁平数组转树（基于 id/parentId） |
| `handleTree` | `(data: any[], id?, parentId?, children?) => any` | 扁平数组转树（自定义键名） |
| `deleteChildren` | `(tree: any[], pathList?) => any` | 删除空 children 并组建 uniqueId |
| `getNodeByUniqueId` | `(tree: any[], uniqueId: number \| string) => any` | 按 uniqueId 查找节点 |
| `appendFieldByUniqueId` | `(tree: any[], uniqueId, fields: object) => any` | 向指定节点追加字段 |
| `extractPathList` | `(tree: any[]) => any` | 提取所有 uniqueId 路径 |

---

## 克隆与比较

| 函数 | 签名 | 说明 |
|------|------|------|
| `clone` | `(val: any, deep?: boolean) => any` | 浅拷/深拷贝，默认浅拷 |
| `cloneDeep` | `(val: any) => any` | 深拷贝 |
| `deepEqual` | `(a: any, b: any, seen?: WeakMap) => boolean` | 深度比较（支持循环引用） |
| `isEqualObject` | `(obj: Record, other: Record) => boolean` | 两对象深度相等 |
| `isEqualArray` | `(arr: any[], other: any[]) => boolean` | 两数组深度相等 |
| `isEqual` | `(a: unknown, b: unknown) => boolean` | 两值深度相等 |
| `mapsEqual` | `(a: Map, b: Map, equalFn) => boolean` | 两 Map 相等 |
| `setsEqual` | `(a: Set, b: Set) => boolean` | 两 Set 相等 |
| `hasOwnProp` | `(obj: object, key: string \| number) => boolean` | 对象是否有指定自身属性 |

---

## 对象（Object）

| 函数 | 签名 | 说明 |
|------|------|------|
| `cleanObject` | `<T>(obj: T, options?: CleanOptions) => DeepClean<T> \| undefined` | 移除无效值（null/undefined/空字符串/空数组/空对象） |
| `delObjectProperty` | `<T, K>(obj: T, props: K \| K[]) => Omit<T, K>` | 删除对象指定属性，返回新对象 |
| `toSet` | `(value: any) => Set<any> \| undefined` | 参数转 Set |
| `shouldCleanKey` | `(key, value, options: CleanOptions) => boolean` | 判断是否要清理某字段 |
| `isInvalidValue` | `(value: any, options: CleanOptions) => boolean` | 检查值是否无效 |
| `entries` | `<T>(obj: Recordable<T>) => [string, T][]` | 对象 entries |

**CleanOptions**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `includeKeys` | `Set \| array \| Record \| Function` | 白名单字段 |
| `excludeKeys` | `Set \| array \| Record \| Function` | 黑名单字段 |
| `stripKeysInObjects` | `{ [objectKey]: (string \| Function)[] \| Function }` | 移除对象字段的子字段 |
| `excludeEmptyObjects` | `boolean` | 清理空对象 `{}` |
| `excludeEmptyArrays` | `boolean` | 清理空数组 `[]` |
| `excludeWhitespaceStrings` | `boolean` | 清理空白字符串 |
| `customFilter` | `(value, key?, parent?) => boolean` | 自定义过滤函数 |
| `maxDepth` | `number` | 最大递归深度 |
| `allowRootIfEmpty` | `boolean` | 允许顶层返回 undefined |

---

## 类型判断（is）

### 通用类型守卫

| 函数 | 签名 | 说明 |
|------|------|------|
| `is` | `(val: unknown, type: string) => boolean` | 判断某值是否为某种类型 |
| `isObject` | `(val: any) => val is Record<any, any>` | 是否是对象 |
| `isPlainObject` | `(val: any) => val is Record<any, any>` | 是否是普通对象（Object 构造或 null prototype） |
| `isDef` | `<T>(val?) => val is T` | 是否非 undefined |
| `isUnDef` | `<T>(val?) => val is T` | 是否是 undefined |
| `isNull` | `(val: unknown) => val is null` | 是否是 null |
| `isNullAndUnDef` | `(val: unknown) => val is null \| undefined` | 是否是 null 且 undefined |
| `isNullOrUnDef` | `(val: unknown) => val is null \| undefined` | 是否是 null 或 undefined |
| `isEmpty` | `<T>(val: T) => val is T` | 是否为空（数组/对象/字符串/Map/Set） |
| `isAllEmpty` | `<T>(val: T) => val is T` | 是否为空（含 null/undefined） |
| `isDate` | `(val: unknown) => val is Date` | 是否是 Date |
| `isLeapYear` | `(val: number) => boolean` | 是否是闰年 |
| `isNumber` | `(val: unknown) => val is number` | 是否是 number |
| `isPromise` | `<T>(val: unknown) => val is Promise<T>` | 是否是 Promise |
| `isString` | `(val: unknown) => val is string` | 是否是 string |
| `isFunction` | `(val: unknown) => val is Function` | 是否是 Function |
| `isBoolean` | `(val: unknown) => val is boolean` | 是否是 Boolean |
| `isRegExp` | `(val: unknown) => val is RegExp` | 是否是 RegExp |
| `isArray` | `(val: any) => val is Array<any>` | 是否是 Array |
| `isJSON` | `(val: any) => boolean` | 是否是标准 JSON |
| `isWindow` | `(val: any) => val is Window` | 是否是 Window |
| `isElement` | `(val: unknown) => val is Element` | 是否是 Element |

### 格式校验

| 函数 | 签名 | 说明 |
|------|------|------|
| `isUrl` | `(value: string) => boolean` | 是否是 URL |
| `isPhone` | `(value: any) => boolean` | 是否是手机号 |
| `isEmail` | `(value: string) => boolean` | 是否是邮箱 |
| `isQQ` | `(value: number) => boolean` | 是否是 QQ 号 |
| `isPostCode` | `(value: number) => boolean` | 是否是中国大陆邮编（6位非0开头） |
| `hasCNChars` | `(value: any, options?: isParams) => boolean` | 是否包含中文，options: `{ unicode?, replaceUnicode?, all?, pure? }` |
| `isLowerCase` | `(value: string) => boolean` | 是否是小写字母 |
| `isUpperCase` | `(value: string) => boolean` | 是否是大写字母 |
| `isAlphabets` | `(value: string) => boolean` | 是否是大小写字母 |
| `isExistSpace` | `(value: string) => boolean` | 是否有空格 |
| `isHtml` | `(value: string) => boolean` | 是否是 HTML |
| `isBase64` | `(val: string) => boolean` | 是否是 Base64 |
| `isHex` | `(color: string) => boolean` | 是否是 hex 颜色 |
| `isRgb` | `(color: string) => boolean` | 是否是 rgb 颜色 |
| `isRgba` | `(color: string) => boolean` | 是否是 rgba 颜色 |

### 环境判断

| 常量/函数 | 类型 | 说明 |
|-----------|------|------|
| `isServer` | `boolean` | 是否处于服务端（根据 window 判断） |
| `isClient` | `boolean` | 是否处于浏览器环境（根据 window 判断） |
| `isBrowser` | `boolean` | 是否处于浏览器环境（根据 document 判断） |

---

## 字符串（Substring / Space / NameTransform）

### 截取

| 函数 | 签名 | 说明 |
|------|------|------|
| `subBefore` | `(val: string, character: string) => string` | 截取指定字符前面的值 |
| `subAfter` | `(val: string, character: string) => string` | 截取指定字符后面的值 |
| `subBothSides` | `(val: string, character: string) => string[]` | 截取指定字符两边的值 |
| `subBetween` | `(val: string, before: string, after: string) => string` | 截取两个字符之间的值 |
| `subTextAddEllipsis` | `(str: string \| number, len?: number) => string` | 截取并追加省略号，默认保留 3 位 |
| `splitNum` | `(number: number) => number[] \| string` | 数字拆分为单个数字数组 |
| `hideTextAtIndex` | `(text: string \| number, index, symbol?: string) => string` | 敏感信息隐藏，index 支持 `number \| number[] \| {start,end} \| {start,end}[]` |

### 空格

| 函数 | 签名 | 说明 |
|------|------|------|
| `removeLeftSpace` | `(str: string) => string` | 去掉左边空格 |
| `removeRightSpace` | `(str: string) => string` | 去掉右边空格 |
| `removeBothSidesSpace` | `(str: string) => string` | 去掉左右两边空格 |
| `removeAllSpace` | `(str: string) => string` | 去掉全部空格 |

### 命名转换

| 函数 | 签名 | 说明 |
|------|------|------|
| `nameCamelize` | `(str: string) => string` | 横线转驼峰 |
| `nameHyphenate` | `(str: string) => string` | 驼峰转横线 |

---

## 日期（Date）

| 函数 | 签名 | 说明 |
|------|------|------|
| `dateFormat` | `(format: string) => string` | 日期格式化，如 `"YYYY-MM-DD HH:mm:ss"` |
| `getCurrentWeek` | `(prefix?: string) => string` | 当前星期几，prefix 默认 `星期` |
| `monthDays` | `(time: Date \| string) => number` | 指定日期月份的总天数 |
| `createYear` | `(start: number) => number[]` | 从当前年份到 start 年份的数组 |
| `getCurrentDate` | `(options?: currentDateOpt) => currentDateType` | 当前日期，返回 `{ ymd, hms, week }`，options: `{ type?: 1\|2\|3, prefix? }` |
| `getTime` | `(seconds: number, bool?: boolean) => hmsType` | 秒转为时分秒，bool 是否补 0 默认 true |

---

## 颜色（Color）

| 函数 | 签名 | 说明 |
|------|------|------|
| `randomColor` | `(options?: ColorOptions) => string \| string[]` | 随机颜色，options: `{ type?: 'rgb'\|'hex'\|'hsl', num? }` |
| `randomGradient` | `(options?: GradientOptions) => string` | 随机渐变色 |
| `hexToRgb` | `(str: string) => number[]` | hex 转 rgb |
| `rgbToHex` | `(r: number, g: number, b: number) => string` | rgb 转 hex |
| `darken` | `(color: string, level: number) => string` | 颜色加深（hex 格式） |
| `lighten` | `(color: string, level: number) => string` | 颜色变浅（hex 格式） |

**GradientOptions**：`{ baseHue?, hueOffset?, saturation?, lightness?, angle?, randomizeHue?, randomizeSaturation?, randomizeLightness?, randomizeAngle? }`

---

## 数学（Math）

| 函数 | 签名 | 说明 |
|------|------|------|
| `max` | `(list: number[]) => number` | 数组最大值 |
| `min` | `(list: number[]) => number` | 数组最小值 |
| `sum` | `(list: number[]) => number` | 数组求和 |
| `average` | `(list: number[]) => number` | 数组平均值 |
| `numberToChinese` | `(num: number \| string) => string` | 阿拉伯数字转中文数字 |
| `exceedMathMax` | `(num: number) => boolean` | 数值是否超过 JS 最大值 |
| `addition` | `(num1: number, num2: number, decimal?: number) => number` | 加法（避免浮点精度问题） |
| `subtraction` | `(num1: number, num2: number, decimal?: number) => number` | 减法 |
| `multiplication` | `(num1: number, num2: number, decimal?: number) => number` | 乘法 |
| `divisionOperation` | `(num1: number, num2: number, decimal?: number) => number` | 除法 |
| `formatBytes` | `(byte: number, digits?: number) => string` | 字节智能转化（B/KB/MB/GB...） |

---

## DOM / 下载

| 函数 | 签名 | 说明 |
|------|------|------|
| `downloadByData` | `(data: BlobPart, filename: string, mime?: string, bom?: BlobPart) => void` | 文件流下载 |
| `downloadByOnlineUrl` | `(url: string, filename: string, mime?: string, bom?: BlobPart) => void` | 在线 URL 下载 |
| `downloadByBase64` | `(buf: string, filename: string, mime?: string, bom?: BlobPart) => void` | Base64 下载 |
| `downloadByUrl` | `(url: string, fileName: string, target?: string) => boolean \| undefined` | 文件地址下载 |
| `openLink` | `(href: string, target?: Target) => void` | 新窗口打开链接 |

---

## CSS 类操作（Class）

| 函数 | 签名 | 说明 |
|------|------|------|
| `hasClass` | `(element: HTMLElement \| Element, name: string) => boolean` | 元素是否存在指定类名 |
| `addClass` | `(element: HTMLElement \| Element, name: string, extraName?: string) => void` | 添加类名 |
| `removeClass` | `(element: HTMLElement \| Element, name: string, extraName?: string) => void` | 删除类名 |
| `toggleClass` | `(bool: boolean, name: string, element?: HTMLElement \| Element) => void` | 条件添加/删除类名 |
| `getClass` | `(element: HTMLElement \| Element) => string \| string[]` | 获取元素所有类名 |

---

## Base64 转换

| 函数 | 签名 | 说明 |
|------|------|------|
| `dataURLtoBlob` | `(base64Buf: string) => Blob` | Base64 转 Blob |
| `urlToBase64` | `(url: string, mineType?: string, encoderOptions?: number) => Promise<string>` | 图片 URL 转 Base64 |
| `convertImageToGray` | `(url: string, options?: grayOpt) => Promise<string>` | 彩色图片转灰色，grayOpt: `{ red?, green?, blue?, scale? }` |

---

## 鼠标事件

| 函数 | 签名 | 说明 |
|------|------|------|
| `banMouseEvent` | `(eventList: Array<MouseEvent>) => void` | 禁止鼠标事件（`contextmenu`/`selectstart`/`copy`） |
| `allowMouseEvent` | `(eventList: Array<MouseEvent>) => void` | 允许鼠标事件 |

---

## FormData

| 函数 | 签名 | 说明 |
|------|------|------|
| `formDataHander` | `(obj: any) => FormData` | 对象转 FormData |
| `createFormData` | `(obj: Record<string, any>, options?: FormDataOptions) => FormData` | 对象转 FormData（更灵活），options: `{ fileKey?, handleFile?, filter? }` |

---

## 坐标转换（Coordtransform）

| 函数 | 签名 | 说明 |
|------|------|------|
| `bd09togcj02` | `(lng: number, lat: number) => number[]` | 百度坐标(BD-09) → 火星坐标(GCJ-02) |
| `gcj02tobd09` | `(lng: number, lat: number) => number[]` | 火星坐标(GCJ-02) → 百度坐标(BD-09) |
| `wgs84togcj02` | `(lng: number, lat: number) => number[]` | WGS-84 → GCJ-02 |
| `gcj02towgs84` | `(lng: number, lat: number) => number[]` | GCJ-02 → WGS-84 |
| `out_of_china` | `(lng: number, lat: number) => boolean` | 是否是中国以外坐标 |

---

## UUID

| 函数 | 签名 | 说明 |
|------|------|------|
| `buildUUID` | `() => string` | 32 位 UUID（无横杠） |
| `buildGUID` | `() => string` | 36 位 GUID（带横杠） |
| `buildPrefixUUID` | `(prefix?: string) => string` | 自定义前缀 UUID |
| `uuid` | `(len?: number, radix?: number, prefix?: string) => string` | 指定长度和基数的 UUID |

---

## URL

| 函数 | 签名 | 说明 |
|------|------|------|
| `getLocation` | `() => Location` | 获取浏览器当前 location 信息 |
| `getQueryMap` | `(url: string) => object` | 提取 URL 中所有参数 |

---

## 路径转换

| 函数 | 签名 | 说明 |
|------|------|------|
| `convertPath` | `(path: string) => string` | Windows 反斜杠路径转斜杠路径 |

---

## SVG

| 函数 | 签名 | 说明 |
|------|------|------|
| `getSvgInfo` | `(svgStr: string) => SvgInfo` | 解析 SVG 字符串，返回 `{ width, height, body }` |

---

## 性能

| 函数 | 签名 | 说明 |
|------|------|------|
| `getPerformance` | `() => Promise<Performance>` | 页面加载性能计时，返回 `{ dns, tcp, request, dom, whiteScreen }`（秒） |
| `getPackageSize` | `(options: packageOpt) => void` | 获取指定文件夹文件总大小 |
| `getBrowserInfo` | `() => BrowserType` | 获取浏览器型号和版本 |
| `deviceDetection` | `() => boolean` | 设备检测，true=移动端 |
| `getPackageSize` | `(options: { folder?, format?, callback }) => void` | 获取包大小 |

---

## 防抖节流

| 函数 | 签名 | 说明 |
|------|------|------|
| `debounce` | `<T>(fn: T, timeout?: number, immediate?: boolean) => () => void` | 防抖，默认 200ms |
| `throttle` | `<T>(fn: T, timeout?: number) => () => void` | 节流，默认 1000ms |
| `delay` | `(timeout?: number) => Promise` | 延时等待，默认 20ms |

---

## 存储（Storage）

| 函数 | 签名 | 说明 |
|------|------|------|
| `storageLocal` | `() => localStorageProxy` | localStorage 封装，`setItem<T>/getItem<T>/removeItem/clear` |
| `storageSession` | `() => sessionStorageProxy` | sessionStorage 封装，接口同上 |

---

## 组件安装（Install）

| 函数 | 签名 | 说明 |
|------|------|------|
| `withInstall` | `<T, E>(main: T, extra?: E) => SFCWithInstall<T> & E` | 添加 install 方法，支持 app.use |
| `withNoopInstall` | `<T>(component: T) => SFCWithInstall<T>` | 添加空 install 方法 |
| `withInstallFunction` | `<T>(fn: T, name: string) => SFCInstallWithContext<T>` | 向 Vue3 全局属性添加函数 |

---

## 其他

| 函数 | 签名 | 说明 |
|------|------|------|
| `copyTextToClipboard` | `(input: string, { target }?) => boolean` | 文本复制到剪贴板 |
| `shuffleArray` | `(array: number[]) => number[]` | Fisher-Yates 洗牌算法 |
| `easeInOutQuad` | `({ timeElapsed, startValue, byValue, duration }) => number` | 二次方缓动函数 |
