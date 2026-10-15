---
name: gomtm-golang-spec
description: use when 针对 gomtm 的 Go 源码规范, 确保代码风格和结构符合社区最佳实践
---

通常已经有其他通用的针对 golang 语言相关的技能文件,这里针对gomtm对应的实际技术栈进行深度指引.


## 坏味道- 繁琐的 logger nil 预防

- ❌错误: logger实例如果进行`!=nil`判断,会大量增加代码行数. logger作为核心对象,应当假定始终存在. 就算程序因此崩溃也不能因此增加`!=nil`的判断.

```go
	if a.Logger != nil {
		a.Logger.Info().Msg("some msg")
	}
```
✅正确: 不进行`!=nil`判断; 或者在包或者实例级别进行单次预防性判断;

## 坏味道- 碎片化函数 (Fragmented / Micro Functions)

### 识别

使用 GitNexus Cypher 查询找出 `.go` 文件中仅有**一个调用方**的函数：

```cypher
MATCH (caller:Function)-[r:CodeRelation {type: 'CALLS'}]->(callee:Function)
WHERE callee.filePath =~ '.*\.go$'
WITH callee, count(r) as callerCount
WHERE callerCount = 1
RETURN callee.name as functionName, callee.filePath as filePath, callerCount
LIMIT 50
```

### 决策标准

| 条件 | 动作 |
|------|------|
| 函数体 **≤ 30 行**（不含空行和注释） | **直接内联合并**到唯一调用方 |
| 函数体 **> 30 行** 或含复杂逻辑分支 | 保留，但标记 `//go:inline` 注释说明 |
| 函数被 **测试文件** 引用 | 保留，不可内联 |

### 合并示例

**Before** — `diagnosticEntriesFromDirectoryUsage` 仅被 `loadLargeDirDiagnostics` 调用，函数体4行，应内联：

```go
func loadLargeDirDiagnostics(ctx context.Context, root string, depth int) []diagnosticEntry {
    cmd := mtutils.SudoCommandContext(ctx, "du", "-k", fmt.Sprintf("--max-depth=%d", depth), root)
    cmd.Stderr = io.Discard
    output, err := cmd.Output()
    if err != nil && len(output) == 0 {
        return nil
    }
    return diagnosticEntriesFromDirectoryUsage(parseTopDirectoryUsage(string(output), diagnosticMinLargeDirBytes, diagnosticMaxLargeDirs))
}

func parseTopDirectoryUsage(output string, minBytes int64, limit int) []topDirectoryUsage {
    entries := sortAndLimitDiagnosticEntries(parseDuEntries(output), minBytes, limit)
    results := make([]topDirectoryUsage, 0, len(entries))
    for _, entry := range entries {
        results = append(results, topDirectoryUsage{Path: entry.label, SizeBytes: entry.sizeBytes})
    }
    return results
}
```

**After** — 消除 `diagnosticEntriesFromDirectoryUsage`，`parseTopDirectoryUsage` 因 > 30 行保留：

```go
func loadLargeDirDiagnostics(ctx context.Context, root string, depth int) []diagnosticEntry {
    cmd := mtutils.SudoCommandContext(ctx, "du", "-k", fmt.Sprintf("--max-depth=%d", depth), root)
    cmd.Stderr = io.Discard
    output, err := cmd.Output()
    if err != nil && len(output) == 0 {
        return nil
    }
    entries := sortAndLimitDiagnosticEntries(parseDuEntries(string(output)), diagnosticMinLargeDirBytes, diagnosticMaxLargeDirs)
    results := make([]diagnosticEntry, 0, len(entries))
    for _, entry := range entries {
        results = append(results, diagnosticEntry{label: entry.label, sizeBytes: entry.sizeBytes})
    }
    return results
}
```

### 工作流

1. **查询**: 运行上述 Cypher 获取单调用方函数列表
2. **逐个确认**: 用 `gitnexus_context` 确认调用关系和函数行数
3. **评估**: ≤ 60 行 → 内联；> 60 行 → 跳过
4. **合并**: 将碎片函数体复制进调用方，删除原函数，更新调用点
5. **验证**: 运行 `gitnexus_detect_changes` 确认影响范围符合预期

### 关键工具

- `gitnexus_cypher` — 查询单调用方函数
- `gitnexus_context` — 确认函数内容、入边、出边调用
- `gitnexus_detect_changes` — 合并后验证影响范围
