# Memory Optimization Skill

**版本**: v1.0
**创建日期**: 2026-03-26
**作?*: 象腿 (main agent)
**用?*: 优化memory管理，自动修剪低价值记忆，提升检索效?
---

## 🎯 核心功能

Memory Optimization skill负责?1. **记忆评分**: 为每条记忆计算相关度分数
2. **自动修剪**: 删除/归档低价值记忆（相关?0.6?3. **智能检?*: 基于相关度排序的memory检?4. **容量控制**: 控制memory总大小（window: 200?5. **定期维护**: 定期清理和优化memory

---

## 📋 Memory架构回顾

### L0? 完整原始记录

**位置**: `memory/YYYY-MM-DD.md`

**内容**: 完整的对话记录、操作日志、事件详?
**特点**:
- 100%保留原始数据
- 用于深度检索和审计
- 文件大小: 10-50KB/?
---

### L1? 关键点提?
**位置**: `memory/summaries/YYYY-MM-DD-summary.md`

**内容**: 当日关键点、重要决策、错误记?
**特点**:
- 保留70% token（相比L0?- 提取关键信息，丢弃冗?- 文件大小: 3-15KB/?
---

### L2? 结构化知?
**位置**: `MEMORY.md`

**内容**: 长期有价值的知识、经验、洞?
**特点**:
- 保留90% token（相比L0?- 结构化存储，易于检?- 文件大小: 20-30KB

---

### L3? 核心洞察

**位置**: `library/insights/`, `library/sops/`, `library/references/`

**内容**: 最核心的洞察、SOP、参考资?
**特点**:
- 保留95% token（相比L0?- 精华中的精华
- 文件大小: 5-10KB/文档

---

## 🔄 Memory优化策略

### 策略1: 相关度评?
```python
def calculate_relevance_score(memory, query):
    """
    计算记忆与查询的相关度分?
    Args:
        memory: 记忆对象
        query: 查询字符?
    Returns:
        float: 相关度分?(0.0-1.0)
    """
    # 1. 关键词匹?(40%)
    keyword_score = calculate_keyword_match(memory, query)

    # 2. 时间衰减 (20%)
    time_score = calculate_time_decay(memory)

    # 3. 访问频率 (20%)
    access_score = calculate_access_frequency(memory)

    # 4. 标签匹配 (20%)
    tag_score = calculate_tag_match(memory, query)

    # 综合评分
    total_score = (
        keyword_score * 0.4 +
        time_score * 0.2 +
        access_score * 0.2 +
        tag_score * 0.2
    )

    return total_score
```

---

### 策略2: 自动修剪

```python
def prune_low_value_memories(memories, threshold=0.6):
    """
    修剪低价值记?
    Args:
        memories: 记忆列表
        threshold: 修剪阈值（默认0.6?
    Returns:
        tuple: (保留的记? 删除的记?
    """
    kept = []
    pruned = []

    for memory in memories:
        score = memory.get('relevance_score', 0.5)

        if score >= threshold:
            kept.append(memory)
        else:
            # 归档到archive
            archive_memory(memory)
            pruned.append(memory)

    log(f"Pruned {len(pruned)} low-value memories (threshold: {threshold})")
    log(f"Kept {len(kept)} high-value memories")

    return kept, pruned
```

---

### 策略3: 容量控制

```python
def control_memory_size(memories, window=200):
    """
    控制memory总大?
    Args:
        memories: 记忆列表
        window: 最大记忆数量（默认200?
    Returns:
        list: 修剪后的记忆列表
    """
    if len(memories) <= window:
        return memories

    # 按相关度排序
    sorted_memories = sorted(
        memories,
        key=lambda m: m.get('relevance_score', 0.5),
        reverse=True
    )

    # 保留前N?    kept = sorted_memories[:window]
    pruned = sorted_memories[window:]

    # 归档删除的记?    for memory in pruned:
        archive_memory(memory)

    log(f"Memory size controlled: {len(memories)} -> {len(kept)} (window: {window})")

    return kept
```

---

### 策略4: 智能检?
```python
def smart_retrieve_memories(query, memories, top_k=10):
    """
    基于相关度的智能检?
    Args:
        query: 查询字符?        memories: 记忆列表
        top_k: 返回前K条结果（默认10?
    Returns:
        list: 相关度最高的前K条记?    """
    # 计算所有记忆的相关?    scored_memories = []
    for memory in memories:
        score = calculate_relevance_score(memory, query)
        memory['relevance_score'] = score
        scored_memories.append(memory)

    # 按相关度排序
    sorted_memories = sorted(
        scored_memories,
        key=lambda m: m['relevance_score'],
        reverse=True
    )

    # 返回前K?    return sorted_memories[:top_k]
```

---

## 🛠?PowerShell实现

### PowerShell相关度计?
```powershell
function Calculate-RelevanceScore {
    param(
        [hashtable]$Memory,
        [string]$Query
    )

    # 1. 关键词匹?(40%)
    $keywordScore = Calculate-KeywordMatch -Memory $Memory -Query $Query

    # 2. 时间衰减 (20%)
    $timeScore = Calculate-TimeDecay -Memory $Memory

    # 3. 访问频率 (20%)
    $accessScore = Calculate-AccessFrequency -Memory $Memory

    # 4. 标签匹配 (20%)
    $tagScore = Calculate-TagMatch -Memory $Memory -Query $Query

    # 综合评分
    $totalScore = ($keywordScore * 0.4) + ($timeScore * 0.2) + ($accessScore * 0.2) + ($tagScore * 0.2)

    return [math]::Round($totalScore, 2)
}

function Calculate-KeywordMatch {
    param(
        [hashtable]$Memory,
        [string]$Query
    )

    $memoryText = $Memory.content -join " "
    $queryWords = $Query -split "\s+"

    $matchCount = 0
    foreach ($word in $queryWords) {
        if ($memoryText -match [regex]::Escape($word)) {
            $matchCount++
        }
    }

    return $matchCount / $queryWords.Count
}

function Calculate-TimeDecay {
    param(
        [hashtable]$Memory
    )

    $memoryDate = [datetime]$Memory.created_at
    $daysSince = (Get-Date) - $memoryDate

    # 指数衰减?天内不衰减，之后每天衰减2%
    if ($daysSince.Days -le 7) {
        return 1.0
    } else {
        $decayRate = 1 - ($daysSince.Days * 0.02)
        return [math]::Max($decayRate, 0.1)  # 最?.1
    }
}

function Calculate-AccessFrequency {
    param(
        [hashtable]$Memory
    )

    $accessCount = $Memory.access_count
    $lastAccess = [datetime]$Memory.last_accessed

    # 访问次数越多，分数越高（但递减?    $score = [math]::Log($accessCount + 1) / 10

    # 最近访问过的有额外加分
    $daysSinceAccess = (Get-Date) - $lastAccess
    if ($daysSinceAccess.Days -le 7) {
        $score *= 1.5
    }

    return [math]::Min($score, 1.0)
}

function Calculate-TagMatch {
    param(
        [hashtable]$Memory,
        [string]$Query
    )

    $memoryTags = $Memory.tags -split ","
    $queryWords = $Query -split "\s+"

    $matchCount = 0
    foreach ($word in $queryWords) {
        foreach ($tag in $memoryTags) {
            if ($tag -match [regex]::Escape($word)) {
                $matchCount++
                break
            }
        }
    }

    if ($memoryTags.Count -eq 0) {
        return 0.5  # 无标签的记忆给中等分?    }

    return $matchCount / $memoryTags.Count
}
```

---

### PowerShell记忆修剪

```powershell
function Prune-LowValueMemories {
    param(
        [array]$Memories,
        [double]$Threshold = 0.6
    )

    $kept = @()
    $pruned = @()

    foreach ($memory in $Memories) {
        # 计算相关度分?        $score = $memory.relevance_score
        if (-not $score) {
            $score = Calculate-RelevanceScore -Memory $memory -Query ""
        }

        if ($score -ge $Threshold) {
            $kept += $memory
        } else {
            # 归档到archive
            Archive-Memory -Memory $memory
            $pruned += $memory
        }
    }

    Write-Host "Pruned $($pruned.Count) low-value memories (threshold: $Threshold)"
    Write-Host "Kept $($kept.Count) high-value memories"

    return $kept, $pruned
}

function Archive-Memory {
    param(
        [hashtable]$Memory
    )

    $archiveDir = "C:\Users\Administrator\.openclaw\workspace-main\memory\archive"
    if (-not (Test-Path $archiveDir)) {
        New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
    }

    $archiveFile = Join-Path $archiveDir "archive-$(Get-Date -Format 'yyyy-MM').json"

    # 追加到archive文件
    $archiveEntry = @{
        id = $Memory.id
        content = $Memory.content
        created_at = $Memory.created_at
        relevance_score = $Memory.relevance_score
        archived_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    }

    $json = $archiveEntry | ConvertTo-Json -Compress
    Add-Content -Path $archiveFile -Value $json -Encoding UTF8
}
```

---

### PowerShell智能检?
```powershell
function Smart-RetrieveMemories {
    param(
        [string]$Query,
        [array]$Memories,
        [int]$TopK = 10
    )

    # 计算所有记忆的相关?    $scoredMemories = @()
    foreach ($memory in $Memories) {
        $score = Calculate-RelevanceScore -Memory $memory -Query $Query
        $memory.relevance_score = $score
        $scoredMemories += $memory
    }

    # 按相关度排序
    $sortedMemories = $scoredMemories | Sort-Object -Property relevance_score -Descending

    # 返回前K?    return $sortedMemories | Select-Object -First $TopK
}
```

---

## 📊 性能优化

### 优化1: 增量评分

```python
def incremental_scoring(memories, changed_memories):
    """
    只对变化的记忆重新评?
    Args:
        memories: 所有记?        changed_memories: 变化的记忆列?
    Returns:
        更新后的记忆列表
    """
    # 只对变化的记忆重新计算分?    for memory in changed_memories:
        memory['relevance_score'] = calculate_relevance_score(memory, "")

    return memories
```

---

### 优化2: 缓存评分结果

```python
class RelevanceCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 3600  # 缓存1小时

    def get_score(self, memory_id, query):
        cache_key = f"{memory_id}:{query}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['timestamp'] < self.ttl:
                return cached['score']

        return None

    def set_score(self, memory_id, query, score):
        cache_key = f"{memory_id}:{query}"
        self.cache[cache_key] = {
            'score': score,
            'timestamp': time.time()
        }

    def clear(self):
        self.cache.clear()
```

---

### 优化3: 批量操作

```python
def batch_prune_memories(memories, batch_size=50):
    """
    批量修剪记忆

    Args:
        memories: 记忆列表
        batch_size: 批次大小

    Returns:
        修剪后的记忆列表
    """
    pruned_count = 0

    for i in range(0, len(memories), batch_size):
        batch = memories[i:i + batch_size]

        # 批量计算相关?        for memory in batch:
            memory['relevance_score'] = calculate_relevance_score(memory, "")

        # 批量修剪
        kept, pruned = prune_low_value_memories(batch)
        pruned_count += len(pruned)

        log(f"Batch {i // batch_size + 1}: pruned {len(pruned)} memories")

    log(f"Total pruned: {pruned_count} memories")

    return kept
```

---

## 🎓 使用示例

### 示例1: 基础修剪

```python
# 加载所有记?memories = load_all_memories()

# 修剪低价值记?kept, pruned = prune_low_value_memories(memories, threshold=0.6)

# 保存结果
save_memories(kept)
```

### 示例2: 智能检?
```python
# 用户查询
query = "如何优化AI Agent的性能"

# 智能检?results = smart_retrieve_memories(query, memories, top_k=10)

# 输出结果
for i, memory in enumerate(results, 1):
    print(f"{i}. [Score: {memory['relevance_score']:.2f}] {memory['content'][:50]}...")
```

### 示例3: 定期维护

```python
# 每周执行一次memory维护
def weekly_maintenance():
    # 1. 加载所有记?    memories = load_all_memories()

    # 2. 容量控制（window: 200?    memories = control_memory_size(memories, window=200)

    # 3. 修剪低价值记忆（threshold: 0.6?    memories, _ = prune_low_value_memories(memories, threshold=0.6)

    # 4. 清理archive
    clean_old_archive()

    # 5. 保存结果
    save_memories(memories)

    log("Weekly memory maintenance completed")
```

---

## ⚙️ 配置文件

### memory-optimization-config.json

```json
{
  "version": "1.0",
  "config": {
    "window": 200,
    "prune_threshold": 0.6,
    "enable_auto_prune": true,
    "prune_interval": 604800,
    "enable_smart_retrieve": true,
    "top_k": 10
  },
  "scoring": {
    "keyword_weight": 0.4,
    "time_decay_weight": 0.2,
    "access_frequency_weight": 0.2,
    "tag_match_weight": 0.2
  },
  "time_decay": {
    "no_decay_days": 7,
    "decay_rate_per_day": 0.02,
    "min_score": 0.1
  },
  "archive": {
    "enabled": true,
    "archive_dir": "memory/archive",
    "retention_days": 90
  },
  "optimization": {
    "enable_incremental_scoring": true,
    "enable_score_cache": true,
    "cache_ttl": 3600,
    "batch_size": 50
  }
}
```

---

## 📈 性能指标

### 关键指标

```yaml
metrics:
  - name: "memory_size"
    description: "记忆总数?
    target: "<= 200"

  - name: "avg_relevance_score"
    description: "平均相关度分?
    target: "> 0.7"

  - name: "retrieval_accuracy"
    description: "检索准确率"
    formula: "相关结果?/ 总结果数"
    target: "> 0.8"

  - name: "prune_rate"
    description: "修剪?
    formula: "修剪记忆?/ 总记忆数"
    target: "< 0.2"

  - name: "token_efficiency"
    description: "Token效率"
    formula: "保留价?/ 总token?
    target: "> 0.95"
```

---

## 🚀 未来优化

### 短期 (1-2?
- [ ] 实现向量检索（embedding-based?- [ ] 添加记忆聚类分析
- [ ] 实现自动标签生成

### 中期 (1个月)
- [ ] 实现跨agent记忆共享
- [ ] 添加记忆图谱可视?- [ ] 实现记忆推荐系统

### 长期 (3个月)
- [ ] 引入强化学习优化修剪策略
- [ ] 实现自适应阈值调?- [ ] 构建记忆价值预测模?
---

*Skill版本: v1.0*
*最后更? 2026-03-26*
*维护? 象腿 (main agent)*
