---
name: python-tips
description: Python 编程常用技巧与陷阱。涉及 Python 写法、坑、性能优化时使用。
---

# Python 技巧

## 常用陷阱
- 默认参数不要用可变对象:`def f(x=[])` 是坑,用 `None` + 判断
- `is` vs `==`:`is` 比身份(None/单例),`==` 比值
- 不要用 `except Exception: pass` 吞错

## 性能
- 列表推导比 for+append 快
- 字符串拼接用 `join`,别用 `+`
- 大数据集用 `array`/`numpy`,别用 list 存数值

## 代码风格
- 类型注解优先:`def add(a: int, b: int) -> int`
