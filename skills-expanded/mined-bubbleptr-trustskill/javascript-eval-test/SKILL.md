---
name: javascript-eval-test
description: 测试 JavaScript AST 分析能力
---

# JavaScript Eval 测试

这个 skill 包含各种 JavaScript 危险模式，用于测试 AST 分析能力。

```javascript
// 危险：eval() 调用
const userInput = "console.log('hello')";
eval(userInput);

// 危险：Function 构造器
const fn = Function("return 1 + 2");

// 危险：new Function()
const add = new Function("a", "b", "return a + b");

// 危险：setTimeout 字符串参数
setTimeout("alert('hello')", 1000);

// 危险：child_process.exec
const { exec } = require('child_process');
exec('ls -la');

// 危险：vm 模块
const vm = require('vm');
vm.runInNewContext('console.log("hello")');
```

预期：AST 分析应该检测到以上所有危险模式。
