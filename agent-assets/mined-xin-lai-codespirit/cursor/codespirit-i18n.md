---
description: CodeSpirit 多语言国际化规范 - 资源文件、本地化、前后端多语言支持
globs: 
  - "*Dto.cs"
  - "**/Dtos/**/*.cs"
  - "*Enum.cs"
  - "**/Enums/**/*.cs"
  - "*Controller.cs"
  - "**/Controllers/**/*.cs"
  - "**/Resources/**/*.cs"
alwaysApply: false
---

# 多语言国际化规范

## 支持语言
- **简体中文** (zh-CN) - 默认语言
- **英文** (en)

## 资源文件命名规范

### 共享资源
```
CodeSpirit.Localization/Resources/
  ├── SharedResources.cs              # 资源类
  ├── Shared.resx                     # 中文（默认）
  ├── Shared.en.resx                  # 英文
  ├── Display.resx / Display.en.resx  # 显示文本资源
  ├── Validation.resx / Validation.en.resx  # 验证消息资源
```

### 服务特定资源
```
CodeSpirit.ExamApi/Resources/
  ├── ExamDisplayResources.cs         # 资源类
  ├── ExamDisplay.resx                # 中文（默认）
  └── ExamDisplay.en.resx             # 英文
```

## 资源键命名规范
- **通用**: `Common.{Key}` (如 `Common.Save`, `Common.Delete`)
- **错误**: `Errors.{Key}` (如 `Errors.NotFound`, `Errors.InvalidInput`)
- **验证**: `Validation.{Rule}` (如 `Validation.Required`, `Validation.StringLengthMax`)
- **DTO描述**: `{EntityName}.{PropertyName}.Description` (如 `Question.Content.Description`)

示例资源文件（Display.resx）：
```xml
<data name="Common.Save" xml:space="preserve">
  <value>保存</value>
</data>
<data name="Common.Delete" xml:space="preserve">
  <value>删除</value>
</data>
<data name="Question.Content.Description" xml:space="preserve">
  <value>请输入题目的具体内容</value>
</data>
```

## Controller 中使用本地化

```csharp
using CodeSpirit.Localization.Resources;
using Microsoft.Extensions.Localization;

public class QuestionsController : ApiControllerBase
{
    private readonly IStringLocalizer<SharedResources> _localizer;
    
    public QuestionsController(IStringLocalizer<SharedResources> localizer)
    {
        _localizer = localizer;
    }
    
    [HttpPost]
    public async Task<ActionResult<ApiResponse>> Create(CreateQuestionDto dto)
    {
        await _service.CreateAsync(dto);
        return SuccessResponse(message: _localizer["Common.Save"].Value);
    }
}
```

## DTO 验证特性多语言

### Display 特性
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

### 描述信息多语言
```csharp
using CodeSpirit.Localization.Attributes;

public class CreateQuestionDto
{
    [Display(Name = "Content", ResourceType = typeof(DisplayResources))]
    [LocalizedDescription("Question.Content.Description", typeof(ExamDisplayResources))]
    public string Content { get; set; } = string.Empty;
}
```

## 本地化异常

```csharp
// 使用资源键
throw new BusinessException("Errors.InvalidStartTime");

// 带参数（使用占位符 {0}, {1}）
throw new ValidationException("Errors.NotFound", resourceId);
```

资源文件定义：
```xml
<data name="Errors.NotFound" xml:space="preserve">
  <value>资源 {0} 未找到</value>
</data>
```

## 枚举多语言
```csharp
public enum QuestionType
{
    [Display(Name = "SingleChoice", ResourceType = typeof(DisplayResources))]
    SingleChoice = 1,
    
    [Display(Name = "MultipleChoice", ResourceType = typeof(DisplayResources))]
    MultipleChoice = 2,
    
    [Display(Name = "TrueFalse", ResourceType = typeof(DisplayResources))]
    TrueFalse = 3
}
```

资源文件：
```xml
<data name="SingleChoice" xml:space="preserve">
  <value>单选题</value>
</data>
<data name="MultipleChoice" xml:space="preserve">
  <value>多选题</value>
</data>
```

## 注意事项

### 强制要求（必须遵守）
- ✅ 所有面向用户的文本必须支持多语言
- ✅ 资源文件必须同时提供中文和英文版本
- ✅ 验证消息、异常消息全部使用本地化

### 最佳实践（推荐遵守）
- 💡 新开发的 DTO、枚举、控制器应使用多语言写法
- 💡 逐步迁移现有硬编码文本到资源文件
- 💡 定期检查资源文件是否有缺失的翻译

### 迁移指南
对于现有代码，建议采用渐进式迁移：
1. 新功能必须使用多语言写法
2. 修改现有功能时，同步迁移为多语言写法
3. 定期批量迁移高频使用的文本

