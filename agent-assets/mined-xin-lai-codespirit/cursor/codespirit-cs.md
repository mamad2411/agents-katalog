---
description: CodeSpirit C# 通用开发规范 - XML注释、时间格式、序列化等通用要求
globs: *.cs
alwaysApply: true
---
# 通用要求

1. **所有公共成员必须添加 XML 文档注释**
   - 使用 `<summary>`、`<param>`、`<returns>`、`<exception>` 标签
   - 注释应清晰描述功能、参数和返回值

2. **复杂业务逻辑必须添加行内注释**
   - 解释关键算法和业务规则
   - 说明特殊处理的原因

3. **优先使用 UTC 时间**
   - 数据库存储使用 UTC 时间
   - 前端显示时转换为本地时间

4. **序列化和反序列化请使用 Newtonsoft.Json**
   - 统一使用 `Newtonsoft.Json` 而非 `System.Text.Json`
   - 配置使用 `JsonConvert.SerializeObject` 和 `JsonConvert.DeserializeObject`

## 专项规范

- **DTO 规范**: 参考 [dto.mdc](mdc:.cursor/rules/dto.mdc)
- **控制器规范**: 参考 [controller.mdc](mdc:.cursor/rules/controller.mdc)
- **服务类规范**: 参考 [service.mdc](mdc:.cursor/rules/service.mdc)
- **枚举规范**: 参考 [enum.mdc](mdc:.cursor/rules/enum.mdc)