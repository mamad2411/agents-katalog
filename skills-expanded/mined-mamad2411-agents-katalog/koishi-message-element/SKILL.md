---
name: koishi-message-element
description: 编写和排查 Koishi 消息元素、JSX 消息、插值转义、嵌套结构、图片/at/链接等标准元素、消息组件边界与平台兼容性。
---

# Koishi 消息元素

这个 skill 用于生成、解释和审查 Koishi 的跨平台消息结构。Koishi 使用“消息元素”描述消息，而不是把平台消息格式直接写进插件。目标是让插件输出尽量保持跨平台，并在需要适配平台差异时能明确边界。

## 输出优先级

1. **纯文本能表达且不会有转义风险时，直接返回字符串。**
2. **只要包含 at、图片、链接、引用、文件、换行分段、嵌套等结构，一律优先使用 JSX。**
3. **只有在用户明确要求或需要嵌入 Buffer 时才使用 `h()` API 或元素字符串。**
4. **不要把非纯文本消息拼成元素字符串。** 元素字符串主要用于本地化条目、配置模板或必须解析外部消息片段的场景。

写插件时优先使用 Koishi 标准元素，不要直接拼某个平台的私有格式。只有在明确要做平台特化时，才使用平台专属字段或适配器能力。

## 为什么优先使用 JSX 而不是 `h()`

`h()` 和 JSX 最终都能表达同一棵元素树，但在插件代码中默认推荐 JSX：

- **形态更接近 Satori 消息元素。** Satori 元素本身采用类 XML 语法，JSX 与这种表示方式在形态上高度一致。
- **更安全地处理插值。** 用户输入、URL、用户 ID 等值可以作为 JSX 文本节点或属性值传入，这比手写元素字符串更少转义负担。

## 基础写法

### 纯文本

```ts
session.send('你好，世界！')
```

### 使用 JSX（默认推荐）

```tsx
session.send(<>
  <at id={session.userId}/>
  你好！
</>)
```

多个结构混排时也使用 JSX：

```tsx
const url = 'https://koishi.chat'

session.send(<>
  文档：<a href={url}>Koishi</a> ({url})
</>)
```

### 使用 `h()` API（用户要求时）

`h()` 的基本签名是 `h(type, attrs?, ...children?)`：

```ts
import { h } from 'koishi'

// 第一个参数是元素名称
h('br')

// 第二个参数可以是属性对象
h('quote', { id: messageId })

// 后续参数是 children，可以是字符串或其他元素
h('p', {}, 'hello')
```

常见标准元素的 `h()` 写法：

```ts
import { h } from 'koishi'

// at 用户
h('at', { id: userId })
h.at(userId)

// 引用消息
h('quote', { id: messageId })
h.quote(messageId)

// 图片、音频、视频、文件
h('img', { src: imageUrl })
h.image(imageUrl)
h.audio(audioUrl)
h.video(videoUrl)
h.file(fileUrl)

// 二进制资源
h.image(buffer, 'image/png')
h.audio(buffer, 'audio/mpeg')
h.video(buffer, 'video/mp4')
h.file(buffer, 'application/octet-stream')
```

## 插值、赋值、转义与解析

### JSX 插值与属性赋值

JSX 中用单花括号 `{}` 插入 JavaScript 表达式。用户输入作为文本节点或属性值传入时，会作为数据参与渲染，不要先拼成元素字符串再解析。

```tsx
ctx.command('say <text:text>').action(({ session }, text) => {
  return <>你说的是：{text}</>
})
```

属性也用 JSX 表达式赋值：

```tsx
ctx.command('avatar <url:string>').action(({ session }, url) => {
  return <img src={url}/>
})
```

混排元素与文本时，继续使用 JSX，而不是字符串拼接：

```tsx
ctx.command('hello').action(({ session }) => {
  return <>
    <at id={session.userId}/>
    {' '}你好！
    <img src="https://example.com/hello.png"/>
  </>
})
```

### 本地化条目的插值

本地化条目无法使用 JSX，可以使用消息元素字符串里的插值语法。这里的 `{}` 不是任意 JavaScript 表达式，而是传入对象的属性路径。

```yaml
commands:
  welcome:
    messages:
      output: 你好呀，<at id={userId}/>！今天是 {date}。
```

```tsx
ctx.command('welcome').action(({ session }) => {
  return session.text('commands.welcome.messages.output', {
    userId: session.userId,
    date: new Date().toLocaleDateString(),
  })
})
```

### 何时使用 `h.escape()`

如果你**必须**生成元素字符串，并把普通文本插入到元素内容中，使用 `h.escape(source)` 转义文本内容中的特殊字符：

```ts
import { h } from 'koishi'

const safeText = h.escape(userInput)
const message = `<message>你说的是：${safeText}</message>`
```

如果文本要进入属性值，使用 `h.escape(source, true)`，第二个参数表示按属性上下文转义，会额外处理引号：

```ts
import { h } from 'koishi'

const safeUrl = h.escape(url, true)
const message = `<a href="${safeUrl}">查看链接</a>`
```

但在插件代码中，上面两种通常都不如 JSX 直接、安全：

```tsx
const message = <>你说的是：{userInput}</>
const link = <a href={url}>查看链接</a>
```

### 何时使用 `h.unescape()`

`h.unescape(source)` 会把消息元素转义还原成普通文本。它适合处理你已经确认来源可信、且需要展示或比对原始文本的场景。

```ts
import { h } from 'koishi'

const plainText = h.unescape('&lt;at id=&quot;123&quot;/&gt;')
// plainText === '<at id="123"/>'
```

不要对不可信输入调用 `h.unescape()`。

### 选择与转换元素

需要分析或改写已有消息元素时，使用消息 API，而不是硬改元素字符串：

- `h.select(source, query)`：按选择器查找元素，例如 `img`、`at`、`message > img`。
- `h.transform(source, rules, session?)`：同步替换或过滤元素。
- `h.transformAsync(source, rules, session?)`：异步替换或过滤元素。

```ts
import { h } from 'koishi'

const images = h.select(session.content, 'img')
```

把所有图片替换为文本占位：

```ts
import { h } from 'koishi'

const fallback = h.transform(session.content, {
  img: () => '[图片]',
})
```

## 嵌套结构

消息元素可以嵌套。嵌套时要分清：

- 属性用于描述元素元信息。
- children 用于描述元素内部内容。
- 文本节点和元素节点可以混排。

默认使用 JSX：

```tsx
return <>
  <at id={session.userId}/>
  {' '}请查看 <a href="https://koishi.chat">Koishi</a>
</>
```

用户明确要求 `h` 时，给出等价 API 写法：

```ts
import { h } from 'koishi'

return h('message', {},
  h('at', { id: session.userId }),
  ' 请查看 ',
  h('a', { href: 'https://koishi.chat' }, 'Koishi'),
)
```

## 常用标准元素

### at 用户

```tsx
return <at id={userId}/>
```

用于提及用户。不同平台对 at 的支持不完全一致；有些平台需要用户在当前频道可见。

### 引用回复

```tsx
return <>
  <quote id={messageId}/>
  你说得对
</>
```

引用、回复强依赖平台能力；不支持的平台可能降级、忽略或报错。

### 图片

```tsx
return <img src="https://example.com/image.png"/>
```

图片资源最好使用可被目标平台访问的 URL。若是本地文件，需要转换为 `file:` URL，并确认适配器或资源服务能正确处理。

```tsx
import { pathToFileURL } from 'url'
import { resolve } from 'path'

return <img src={pathToFileURL(resolve(__dirname, 'logo.png')).href}/>
```

### 链接

```tsx
const url = 'https://koishi.chat'
return <a href={url}>Koishi</a>
```

### 文件、音频、视频

```tsx
return <file src={fileUrl}/>
```

```tsx
return <audio src={audioUrl}/>
```

```tsx
return <video src={videoUrl}/>
```

文件、音频、视频受平台支持度、资源大小、格式和 URL 可访问性影响。需要给不支持的平台准备文本降级。

### 换行与多段消息

单条消息中的换行可以直接写文本换行或 `{'\n'}`。多段消息可以用 `message` 元素组织，但不要依赖某个平台的换行特殊规则。

```tsx
return <>
  第一行{`\n`}
  第二行
</>
```

```tsx
return <>
  <message>第一条</message>
  <message>第二条</message>
</>
```
