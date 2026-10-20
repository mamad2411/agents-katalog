---
description: 生成 OpenAPI / Swagger 文档
---

# Swagger 文档生成

## 确认 Knife4j 配置

项目使用 Knife4j 4.5.0，自动集成在 `taotao-cloud-boot-starter-openapi` 中。

## 查看文档

1. **启动应用**
```powershell
gradlew :taotao-cloud-member-assembly:bootRun --args='--spring.profiles.active=dev'
```

2. **访问文档**
- Knife4j UI：`http://localhost:{port}/doc.html`
- OpenAPI JSON：`http://localhost:{port}/v3/api-docs`

## 检查 API 完整性
- [ ] 所有 Controller 有 `@Tag` 注解
- [ ] 所有接口方法有 `@Operation` 注解
- [ ] DTO 字段有 `@Schema` 注解
