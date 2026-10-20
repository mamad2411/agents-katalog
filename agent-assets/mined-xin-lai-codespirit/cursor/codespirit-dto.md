---
description: CodeSpirit DTO 开发规范 - 数据传输对象的特性、验证、映射和多语言支持
globs: 
  - "*Dto.cs"
  - "**/Dtos/**/*.cs"
alwaysApply: false
---

# DTO 类规则

## 属性特性要求

1. **所有属性必须添加 Display 特性（支持多语言）**
2. **Create/Update DTO 必须添加验证特性**
3. 列表 DTO 应参考 [UserDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserDto.cs) 添加必要的列特性
4. 查询 DTO 必须继承自 [QueryDtoBase.cs](mdc:Src/CodeSpirit.Core/Dtos/QueryDtoBase.cs)，并添加常见的查询逻辑，可以参考 [UserQueryDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserQueryDto.cs)
5. DTO 添加完成后，应添加或完善 DTO 映射文件，处理好映射关系，参考 [UserProfile.cs](mdc:Src/CodeSpirit.IdentityApi/MappingProfiles/UserProfile.cs)
6. BatchImportItemDto 需要添加 JsonProperty 特性，propertyName 与 DisplayName 一致，参考 [UserBatchImportItemDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserBatchImportItemDto.cs)
7. 如果需要显示用户信息，请使用聚合器字段特性 [AggregateFieldAttribute.cs](mdc:Src/CodeSpirit.Core/Attributes/AggregateFieldAttribute.cs)，参考 [CodeSpirit.Aggregator聚合器使用指南.md](mdc:Docs/CodeSpirit.Aggregator聚合器使用指南.md)

## 查询 DTO 中枚举字段

**枚举筛选字段仅需 `[DisplayName]`，不要使用 `[AmisSelectField]`。**

SearchFieldHelper 会自动为枚举类型生成 Select 下拉选项，选项文案来自枚举值的 `[Display(Name = "...")]` 特性。若添加 `AmisSelectField`（无论 Source 或 Options），会覆盖该自动行为，导致重复配置或硬编码。

```csharp
// ✅ 正确：仅 DisplayName，框架自动生成选项
[DisplayName("状态")]
public QuestionStatus? Status { get; set; }

// ❌ 错误：不要为枚举添加 AmisSelectField
[AmisSelectField(Options = "1:草稿,2:已发布,3:已归档")]  // 硬编码，无法多语言
[AmisSelectField(Source = "${ROOT_API}/api/.../status-options")]  // 过度设计，枚举无需 API
```

参考：[QuestionQueryDto.cs](mdc:Src/ApiServices/CodeSpirit.ExamApi/Dtos/Question/QuestionQueryDto.cs) 中的 Type、Difficulty、Status 字段。

## 多语言写法示例

```csharp
using CodeSpirit.Localization.Resources;

public class CreateQuestionDto
{
    [Display(Name = "Content", ResourceType = typeof(DisplayResources))]
    [Required(ErrorMessageResourceType = typeof(ValidationResources), 
             ErrorMessageResourceName = "Required")]
    [StringLength(2000, 
        ErrorMessageResourceType = typeof(ValidationResources),
        ErrorMessageResourceName = "StringLengthMax")]
    public string Content { get; set; } = string.Empty;
    
    [Display(Name = "Score", ResourceType = typeof(DisplayResources))]
    [Range(0, 100, 
        ErrorMessageResourceType = typeof(ValidationResources),
        ErrorMessageResourceName = "Range")]
    public decimal Score { get; set; }
}
```

## 参考文件

- 列表 DTO: [UserDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserDto.cs)
- 查询 DTO: [UserQueryDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserQueryDto.cs)
- 查询 DTO 枚举字段: [QuestionQueryDto.cs](mdc:Src/ApiServices/CodeSpirit.ExamApi/Dtos/Question/QuestionQueryDto.cs)
- 映射配置: [UserProfile.cs](mdc:Src/CodeSpirit.IdentityApi/MappingProfiles/UserProfile.cs)
- 批量导入: [UserBatchImportItemDto.cs](mdc:Src/CodeSpirit.IdentityApi/Dtos/User/UserBatchImportItemDto.cs)
