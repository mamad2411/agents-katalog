---
description: CodeSpirit 枚举开发规范 - 枚举定义、Display特性和多语言支持
globs: 
  - "*Enum.cs"
  - "**/Enums/**/*.cs"
alwaysApply: false
---

# 枚举（Enum）规则

## 基本要求

1. 枚举需添加 Display 特性（支持多语言）
2. 每个枚举值必须添加 XML 文档注释
3. 枚举值使用 PascalCase 命名
4. 明确指定枚举值（避免依赖默认值）

## 枚举示例（多语言）

```csharp
using CodeSpirit.Localization.Resources;
using System.ComponentModel.DataAnnotations;

/// <summary>
/// 题目类型枚举
/// </summary>
public enum QuestionType
{
    /// <summary>
    /// 单选题
    /// </summary>
    [Display(Name = "SingleChoice", ResourceType = typeof(DisplayResources))]
    SingleChoice = 1,
    
    /// <summary>
    /// 多选题
    /// </summary>
    [Display(Name = "MultipleChoice", ResourceType = typeof(DisplayResources))]
    MultipleChoice = 2,
    
    /// <summary>
    /// 判断题
    /// </summary>
    [Display(Name = "TrueFalse", ResourceType = typeof(DisplayResources))]
    TrueFalse = 3
}
```

## 资源文件配置

对应的资源文件（Display.resx）：
```xml
<data name="SingleChoice" xml:space="preserve">
  <value>单选题</value>
</data>
<data name="MultipleChoice" xml:space="preserve">
  <value>多选题</value>
</data>
<data name="TrueFalse" xml:space="preserve">
  <value>判断题</value>
</data>
```

英文资源文件（Display.en.resx）：
```xml
<data name="SingleChoice" xml:space="preserve">
  <value>Single Choice</value>
</data>
<data name="MultipleChoice" xml:space="preserve">
  <value>Multiple Choice</value>
</data>
<data name="TrueFalse" xml:space="preserve">
  <value>True/False</value>
</data>
```

## 在 QueryDto 中的使用

枚举用于查询 DTO 筛选条件时，**仅使用 `[DisplayName]`**，不要添加 `[AmisSelectField]`。框架会根据枚举的 Display 特性自动生成下拉选项。详见 [dto.mdc - 查询 DTO 中枚举字段](mdc:.cursor/rules/dto.mdc)。

## 参考文档

- 多语言规范: [i18n.mdc](mdc:.cursor/rules/i18n.mdc)
- 查询 DTO 枚举配置: [dto.mdc](mdc:.cursor/rules/dto.mdc)
