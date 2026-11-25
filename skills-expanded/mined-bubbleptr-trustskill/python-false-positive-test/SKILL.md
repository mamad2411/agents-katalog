---
name: python-false-positive-test
description: 测试 AST 能区分注释和代码中的危险模式
---

# Python False Positive 测试

这个 skill 包含注释和字符串中的危险模式，但实际代码是安全的。

```python
# 注意：不要使用 eval() 因为它很危险
# eval() is dangerous and should be avoided

def safe_function():
    """
    这个函数是安全的。
    警告：永远不要使用 exec() 或 eval()
    """
    message = "Don't use eval() in production code"
    print(message)

    # 安全的代码
    x = 1 + 2
    return x

# 调用安全函数
result = safe_function()
print(f"Result: {result}")
```

预期：AST 分析不应该报告问题（注释和字符串不是真实代码）。
