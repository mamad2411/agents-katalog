---
description: 运行测试并生成 JaCoCo 覆盖率报告
parameters:
  - name: module
    type: string
    description: 测试模块名（domain/application/infrastructure/interfaces）
    required: false
  - name: coverage
    type: boolean
    default: true
---

# 测试执行

## 执行步骤

### 1. 清理并编译
```powershell
gradlew clean compileJava
```

### 2. 运行测试
```powershell
# 运行指定模块测试
gradlew :taotao-cloud-member-{module}:test

# 运行所有测试
gradlew test
```

### 3. 生成覆盖率报告
```powershell
gradlew jacocoTestReport
# 报告位置: build/reports/jacoco/test/html/index.html
```

### 4. 输出测试结果
- 测试总数
- 通过数
- 失败数（列出每个失败用例的类名 + 方法名 + 错误信息）
- 覆盖率
