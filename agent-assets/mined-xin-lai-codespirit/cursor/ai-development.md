---
description: CodeSpirit AI功能开发规范 - AI表单填充、长任务处理、LLM集成
globs: *.cs
alwaysApply: false
---

# AI 功能开发规范

## 📋 目录

1. [架构概览](#架构概览)
2. [AI 表单填充](#ai-表单填充)
3. [AI 长任务处理](#ai-长任务处理)
4. [LLM 集成](#llm-集成)
5. [提示词管理](#提示词管理)
6. [错误处理](#错误处理)
7. [性能优化](#性能优化)
8. [安全最佳实践](#安全最佳实践)

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              前端                                        │
│  ┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐   │
│  │   表单组件       │───▶│   AI填充按钮     │───▶│  自动生成UI      │   │
│  └─────────────────┘    └──────────────────┘    └──────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ POST /api/{controller}/ai-fill
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              后端                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AiFormFill中间件（自动拦截 ai-fill 请求）                        │   │
│  └────────────────────────────────┬────────────────────────────────┘   │
│                                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AiFormFillService → AiFormPromptBuilder → LLM客户端            │   │
│  └────────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────┼─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              LLM服务（OpenAI / 通义千问 / DeepSeek）                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 模式选择决策树

```
使用哪种AI填充模式？
├── 需要基于单个字段触发填充？
│   └── 是 → 字段触发模式 (TriggerField = "FieldName")
│
├── 需要用户输入自定义需求一次性填充整个表单？
│   └── 是 → 全局填充模式 (GlobalFillPrompt = "提示词")
│
└── 需要复杂的AI长任务处理（批量生成、进度跟踪）？
    └── 是 → AI长任务模式 (HeaderOperation + aiForm)
```

---

## AI 表单填充

### 快速开始（零代码方案）

#### 1. 服务注册
```csharp
// Program.cs 或 ApiConfiguration

// 注册 LLM 服务（必需）
builder.Services.AddLLMServices();

// 注册 AI 表单填充自动端点（推荐）
builder.Services.AddAiFormFillEndpoints();

var app = builder.Build();

// 启用 AI 填充中间件
app.UseAiFormFillEndpoints();
```

#### 2. DTO 配置
```csharp
[AiFormFill(TriggerField = nameof(Topic))]
public class CreateQuestionDto
{
    [Required]
    [DisplayName("主题")]
    public string Topic { get; set; } = string.Empty;
    
    [DisplayName("题目内容")]
    [AiFieldFill(Priority = 1, CustomDescription = "根据主题生成的题目内容")]
    public string? Content { get; set; }
    
    [DisplayName("选项A")]
    [AiFieldFill(Priority = 2)]
    public string? OptionA { get; set; }
}
```

**完成！** 系统自动生成 `POST /api/questions/ai-fill` 端点，无需编写任何控制器代码。

### AiFormFillAttribute 完整参数

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `TriggerField` | string | "" | 触发字段名称，为空时启用全局模式 |
| `IgnoreFields` | string[] | [] | 需要忽略的字段列表 |
| `CustomPromptTemplate` | string | "" | 自定义提示词模板 |
| `ApiEndpoint` | string | "ai-fill" | API端点路径 |
| `MaxTokens` | int | 1000 | 最大Token数量 |
| `EnableCache` | bool | true | 是否启用缓存 |
| `CacheExpirationMinutes` | int | 30 | 缓存过期时间（分钟） |
| `GlobalFillPrompt` | string | "使用AI智能优化表单" | 全局模式提示文本 |
| `UseIndependentLLM` | bool | false | 是否使用独立的LLM配置 |
| `LLMSettingsKey` | string | "AiFormFillLLM" | 独立LLM配置的设置键名 |
| `DisableThinking` | bool | true | 是否禁用思考模式 |
| `ResponseFormatType` | string | "json_object" | 响应格式类型 |
| `Temperature` | double | 0.1 | 温度参数，控制随机性 |
| `TopP` | double | 0.9 | Top-p参数，控制多样性 |

### AiFieldFillAttribute 参数

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `Enabled` | bool | true | 是否参与AI填充 |
| `Weight` | int | 1 | 字段权重（影响提示词中的重要性） |
| `Priority` | int | 0 | 字段填充优先级 |
| `CustomDescription` | string | "" | 自定义字段描述（自动添加到JSON注释） |

### 使用模式

#### 字段触发模式
用户输入触发字段后，AI 智能填充其他相关字段：

```csharp
[AiFormFill(TriggerField = nameof(Topic))]
public class CreateSurveyDto
{
    [Required]
    [DisplayName("问卷主题")]
    public string Topic { get; set; } = string.Empty;
    
    [DisplayName("问卷描述")]
    [AiFieldFill(Priority = 1, CustomDescription = "基于主题生成的详细描述")]
    public string? Description { get; set; }
    
    [DisplayName("目标受众")]
    [AiFieldFill(Priority = 2)]
    public string? TargetAudience { get; set; }
}
```

#### 全局填充模式
用户在表单顶部输入自定义需求，AI 一次性填充整个表单：

```csharp
[AiFormFill(GlobalFillPrompt = "描述您想创建的内容")]
public class CreateContentDto
{
    [DisplayName("标题")]
    public string? Title { get; set; }
    
    [DisplayName("内容")]
    public string? Content { get; set; }
    
    [DisplayName("标签")]
    public List<string>? Tags { get; set; }
}
```

### 自定义提示词模板

#### 基础模板（自动追加JSON结构）
```csharp
[AiFormFill(
    TriggerField = nameof(Topic),
    CustomPromptTemplate = "基于主题 '{Topic}' 生成相关内容，要求专业准确")]
public class CustomPromptDto { }
```

#### 完整模板（包含JSON结构，不会重复追加）
```csharp
[AiFormFill(
    TriggerField = nameof(Description),
    CustomPromptTemplate = @"你是一个目标管理专家。

用户输入：{Description}
请优化目标描述，并提取关键信息。

**返回JSON结构说明：**
```json
{
  ""description"": ""string, 必填。优化后的目标描述"",
  ""title"": ""string, 必填。提取的简短标题""
}
```

请严格按照上述JSON结构返回。")]
public class GoalDto { }
```

> 💡 系统会智能检测模板中是否已包含 JSON 结构说明（关键词：` ```json `），不会重复追加。

### 独立 LLM 配置

为 AI 表单填充配置专用的 LLM 设置：

```csharp
[AiFormFill(
    TriggerField = nameof(Topic),
    UseIndependentLLM = true,
    LLMSettingsKey = "AiFormFillLLM",
    DisableThinking = true,
    Temperature = 0.1)]
public class SmartSurveyDto { }
```

配置文件：
```json
{
  "AiFormFillLLM": {
    "ApiBaseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "ApiKey": "your-api-key",
    "ModelName": "qwq-plus",
    "TimeoutSeconds": 120,
    "DisableThinking": true,
    "ResponseFormatType": "json_object"
  }
}
```

### 自动化特性
系统自动完成：
- ✅ 生成 AI 填充 API 端点（如 `POST /exam/api/Questions/ai-fill`）
- ✅ 路由自动推断（根据 DTO 命名空间和类名）
- ✅ 中间件拦截处理
- ✅ 前端 UI 自动增强（触发字段显示 AI 填充按钮）
- ✅ 提示词自动构建（分析 DTO 结构、验证规则、CustomDescription）
- ✅ 响应自动解析（JSON 转 DTO）
- ✅ 智能 JSON 结构检测（避免重复追加）
- ✅ 流式模式自动检测和重试

---

## AI 长任务处理

用于耗时较长的 AI 任务（如批量生成、复杂分析等），支持异步处理和进度跟踪：

### 定义任务 API
```csharp
[HttpPost("ai/generate-async")]
[HeaderOperation("AI智能生成", "aiForm", 
    Icon = "fa-solid fa-magic",
    StatusApi = "/exam/api/Questions/ai/task-status",  // 状态查询 API（必需）
    PollingInterval = 2000,                             // 轮询间隔（毫秒）
    MaxPollingTime = 300000,                            // 最大轮询时间（5分钟）
    FormTitle = "生成配置",
    StepsTitle = "AI生成进度",
    LogTitle = "生成日志",
    ResultTitle = "生成结果")]
[DisplayName("AI智能生成题目")]
public async Task<ActionResult<ApiResponse<string>>> GenerateQuestionsAsync(
    [FromBody] GenerateQuestionsRequest request)
{
    var taskId = await _aiGeneratorService.GenerateAsync(request);
    return SuccessResponse(taskId);
}

[HttpGet("ai/task-status")]
[DisplayName("查询任务状态")]
public async Task<ActionResult<ApiResponse<AiTaskStatus>>> GetTaskStatus(
    [FromQuery] string taskId)
{
    var status = await _aiGeneratorService.GetTaskStatusAsync(taskId);
    return SuccessResponse(status);
}
```

### 任务状态响应
```csharp
public class AiTaskStatus
{
    public string Status { get; set; }       // "pending", "processing", "completed", "failed"
    public int Progress { get; set; }        // 0-100
    public List<string> Logs { get; set; }   // 日志列表
    public object? Result { get; set; }      // 任务结果
    public string? ErrorMessage { get; set; } // 错误消息
}
```

---

## LLM 集成

### 方式一：LLMAssistant（推荐）

```csharp
using CodeSpirit.LLM;

public class QuestionGeneratorService : IScopedDependency
{
    private readonly LLMAssistant _llmAssistant;
    
    public QuestionGeneratorService(LLMAssistant llmAssistant)
    {
        _llmAssistant = llmAssistant;
    }
    
    // 基础内容生成
    public async Task<string> GenerateContentAsync(string prompt)
    {
        return await _llmAssistant.GenerateContentAsync(prompt);
    }
    
    // 带系统提示词
    public async Task<string> GenerateWithSystemPromptAsync(
        string systemPrompt, string userPrompt)
    {
        return await _llmAssistant.GenerateContentAsync(systemPrompt, userPrompt);
    }
}
```

### 方式二：结构化任务处理（推荐复杂场景）

```csharp
public class AuditService : IScopedDependency
{
    private readonly LLMAssistant _llmAssistant;
    
    public async Task<AuditResult> AuditQuestionAsync(QuestionDto question)
    {
        var result = await _llmAssistant.ProcessStructuredTaskWithTemplateAsync<AuditResult>(
            "question_audit",  // 模板名称
            new { question },  // 模板数据
            new StructuredTaskOptions 
            { 
                EnableRetry = true, 
                MaxRetries = 2 
            });
        
        if (result.IsSuccess)
        {
            return result.Result!;
        }
        
        throw new BusinessException($"审核失败: {string.Join("; ", result.Errors)}");
    }
}
```

### 方式三：批量处理

```csharp
public async Task<List<AuditResult>> BatchAuditAsync(List<QuestionDto> questions)
{
    var batchResult = await _llmAssistant.ProcessBatchStructuredTaskAsync<QuestionDto, AuditResult>(
        questions,
        batch => BuildBatchPrompt(batch),
        new BatchProcessingOptions 
        { 
            BatchSize = 10,
            MaxRetries = 2,
            DelayBetweenBatches = TimeSpan.FromSeconds(1),
            ContinueOnFailure = true
        });
    
    return batchResult.SuccessResults
        .Where(r => r.IsSuccess)
        .Select(r => r.Result!)
        .ToList();
}
```

### 增强功能组件

#### ILLMJsonProcessor - JSON 处理
```csharp
private readonly ILLMJsonProcessor _jsonProcessor;

public async Task<T> ParseAiResponse<T>(string aiResponse) where T : class
{
    var result = await _jsonProcessor.ParseStructuredResponseAsync<T>(aiResponse);
    
    if (result.IsSuccess)
    {
        if (result.WasRepaired)
        {
            _logger.LogWarning("JSON已自动修复");
        }
        return result.Result!;
    }
    
    throw new InvalidOperationException($"解析失败: {string.Join("; ", result.Errors)}");
}
```

#### ILLMPromptBuilder - 提示词构建
```csharp
private readonly ILLMPromptBuilder _promptBuilder;

public string BuildComplexPrompt(object data)
{
    return _promptBuilder
        .Reset()
        .WithSystemPrompt("你是一个专业的助手")
        .WithTemplate("my_template", data)
        .WithValidationRules("规则1", "规则2")
        .WithOutputFormat<MyResult>()
        .Build();
}
```

### 流式响应
```csharp
public async Task GenerateStreamAsync(string prompt, Func<string, Task> onChunk)
{
    var client = await _llmClientFactory.CreateClientAsync();
    
    await client.GenerateContentStreamAsync(prompt, async chunk =>
    {
        await onChunk(chunk);
    });
}
```

---

## 提示词管理

### 最佳实践
- **角色设定清晰**：明确 AI 扮演的角色
- **任务描述具体**：明确要完成的任务和要求
- **输出格式明确**：指定 JSON 格式和字段名称
- **约束条件清晰**：长度限制、验证规则等
- **提供示例**：复杂场景提供输出示例

### 提示词模板示例
```csharp
public static class PromptTemplates
{
    public const string QuestionGenerator = @"你是一个专业的出题专家。

任务：根据以下信息生成一道高质量的题目。

主题：{Topic}
题型：{QuestionType}
难度：{Difficulty}

要求：
1. 题目内容清晰准确，符合{Difficulty}难度
2. 选项设计合理，避免明显错误
3. 只有一个正确答案
4. 题目内容不超过 2000 字符

输出格式（JSON）：
{{
  ""Content"": ""题目内容"",
  ""OptionA"": ""选项A内容"",
  ""OptionB"": ""选项B内容"",
  ""OptionC"": ""选项C内容"",
  ""OptionD"": ""选项D内容"",
  ""CorrectAnswer"": ""A""
}}";
}
```

---

## 错误处理

### 常见错误类型

| 错误类型 | 原因 | 处理方式 |
|---------|------|---------|
| 401 Unauthorized | API 密钥无效 | 检查配置，更新密钥 |
| 400 Bad Request | 模型名称错误 | 验证模型名称是否正确 |
| 429 Too Many Requests | 请求限流 | 添加重试和延迟 |
| Timeout | 请求超时 | 增加超时时间，拆分请求 |
| JSON解析失败 | 响应格式不正确 | 使用 ILLMJsonProcessor 自动修复 |

### 自动错误处理
系统自动处理：
- ✅ **流式模式检测**：自动检测"只支持流式模式"的模型并重试
- ✅ **JSON 自动修复**：截断、括号不匹配、引号错误等
- ✅ **重试机制**：支持配置重试次数和延迟

### 错误处理示例
```csharp
public async Task<T> SafeGenerateAsync<T>(string prompt) where T : class
{
    try
    {
        var result = await _llmAssistant.ProcessStructuredTaskWithTemplateAsync<T>(
            "template", 
            new { prompt },
            new StructuredTaskOptions { EnableRetry = true, MaxRetries = 3 });
        
        if (result.IsSuccess)
        {
            return result.Result!;
        }
        
        _logger.LogError("AI生成失败: {Errors}", string.Join("; ", result.Errors));
        throw new BusinessException("AI生成失败，请稍后重试");
    }
    catch (HttpRequestException ex)
    {
        _logger.LogError(ex, "LLM API请求失败");
        throw new BusinessException("AI服务暂时不可用");
    }
    catch (TaskCanceledException ex)
    {
        _logger.LogError(ex, "LLM请求超时");
        throw new BusinessException("AI响应超时，请缩短输入或稍后重试");
    }
}
```

### 日志配置
```json
{
  "Logging": {
    "LogLevel": {
      "CodeSpirit.AiFormFill": "Information",
      "CodeSpirit.LLM": "Information"
    }
  }
}
```

---

## 性能优化

### 缓存策略
```csharp
[AiFormFill(
    TriggerField = nameof(Topic),
    EnableCache = true,               // 启用缓存
    CacheExpirationMinutes = 30       // 30分钟过期
)]
```

**缓存键规则**：包含输入内容的哈希值，相同输入直接返回缓存结果。

### 批量处理优化
```csharp
var options = new BatchProcessingOptions
{
    BatchSize = 10,                              // 每批10条
    DelayBetweenBatches = TimeSpan.FromSeconds(1), // 批次间延迟
    MaxRetries = 2,                              // 最大重试次数
    ContinueOnFailure = true                     // 失败时继续处理
};
```

### Token 控制
- 合理设置 `MaxTokens`，避免过度消耗
- 使用缓存减少重复请求
- 长文本分段处理
- 定期监控 Token 使用量

### 并发控制
```csharp
// ❌ 避免：直接并发大量请求
var tasks = topics.Select(t => GenerateAsync(t));
await Task.WhenAll(tasks);  // 可能触发限流

// ✅ 推荐：使用批量处理器
await _batchProcessor.ProcessBatchWithRetryAsync(topics, ProcessBatch, options);
```

---

## 安全最佳实践

### API 密钥管理
```csharp
// ✅ 使用 Aspire 统一配置（推荐）
var llmApiKey = builder.AddParameter("llm-ApiKey", secret: true);

// ✅ 使用环境变量
.WithEnvironment("LLM__ApiKey", llmApiKey)

// ❌ 禁止：硬编码密钥
var apiKey = "sk-xxxxxxxx";  // 绝对禁止！
```

### 敏感数据保护
```csharp
// 排除敏感字段
[AiFieldFill(Enabled = false)]
public string Password { get; set; }

[AiFieldFill(Enabled = false)]
public string IdCard { get; set; }

// 使用 IgnoreFields
[AiFormFill(
    TriggerField = nameof(Name),
    IgnoreFields = new[] { "Password", "IdCard", "BankAccount" }
)]
```

### 输出审核
- 对 AI 生成内容进行后处理验证
- 设置合理的内容长度限制
- 记录审计日志
- 敏感词过滤

### 权限控制
```csharp
[HttpPost("ai-fill")]
[Authorize]
[RequirePermission("Question.AiFill")]
public async Task<ActionResult> AiFill([FromBody] CreateQuestionDto dto)
{
    // AI 填充需要特定权限
}
```

---

## 注意事项

- ✅ AI 填充特性仅用于表单填充场景
- ✅ 长任务处理必须提供状态查询 API
- ✅ 提示词应明确输出格式为 JSON
- ✅ 处理 LLM 响应异常（格式错误、超时等）
- ✅ 敏感数据不要发送给 LLM
- ✅ 定期审查 AI 生成的内容质量
- ✅ 使用 `LLMAssistant` 而非直接使用 `ILLMClient`
- ✅ 复杂场景使用 `ProcessStructuredTaskWithTemplateAsync`
