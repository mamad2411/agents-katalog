---
description: 部署应用到指定环境（dev/test/pre/pro）
parameters:
  - name: environment
    type: string
    enum: [dev, test, pre, pro]
    required: true
---

# 部署流程

## 1. 运行测试
```powershell
gradlew test
```

## 2. 打包
```powershell
gradlew :taotao-cloud-member-assembly:bootJar
```

## 3. 启动（指定环境）
```powershell
java --enable-preview `
  -jar taotao-cloud-member-assembly/build/libs/taotao-cloud-member-assembly-*.jar `
  --spring.profiles.active={environment}
```

## 4. 健康检查
```powershell
curl -f http://localhost:{port}/actuator/health
```

## 输出
- 环境
- JAR 大小
- 健康检查状态
