---
description: 异常处理(Exception)
globs: 
---
# 异常处理

框架自带有： `CoolCommException`

## 通用异常

CoolCommException

返回码： 1001

返回消息：comm fail

用法：

```ts
// 可以自定义返回消息
throw new CoolCommException('用户不存在~');
```