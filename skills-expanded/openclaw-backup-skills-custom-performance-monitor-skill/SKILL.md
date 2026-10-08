---
name: performance-monitor
description: Real-time monitoring and optimization of system performance. Use when you need to track response times, resource usage, skill efficiency, and overall system health. This skill enables continuous performance optimization, bottleneck detection, and proactive improvements to keep OpenClaw running at peak performance.
---

# Performance Monitor

**System yang tetap KILAT** meski loaded! ⚡

## 🎯 Core Function

Monitor dan optimize **semua aspek performance**:

1. **Response Time Tracking** - Measure how fast I respond
2. **Resource Usage** - Monitor CPU, memory, disk, network
3. **Skill Efficiency** - Track which skills are fast/slow
4. **Bottleneck Detection** - Find what's slowing things down
5. **Auto Optimization** - Improve performance automatically

## 📊 Metrics Tracked

### Response Metrics:
```
✅ Average response time: [X ms]
✅ Fastest response: [Y ms]
✅ Slowest response: [Z ms]
✅ P95 response time: [XX ms]
✅ P99 response time: [XXX ms]
✅ Requests per minute: [X]
```

### Resource Metrics:
```
✅ CPU usage: [XX%]
✅ Memory usage: [XX MB]
✅ Disk I/O: [X MB/s]
✅ Network: [X KB/s]
✅ Active connections: [X]
✅ Concurrent tasks: [X]
```

### Skill Metrics:
```
✅ Most used skills: [list]
✅ Slowest skills: [list]
✅ Fastest skills: [list]
✅ Error rates: [skill, %]
✅ Efficiency scores: [skill, %]
```

## 🔧 Monitoring Modes

### Mode 1: Real-Time
```
Live monitoring with immediate alerts
- Response time spikes
- Resource usage thresholds
- Error rate increases
- System health changes
```

### Mode 2: Periodic Reports
```
Regular performance reports:
- Every hour: Quick snapshot
- Daily: Detailed analysis
- Weekly: Trends & improvements
- Monthly: Comprehensive review
```

### Mode 3: On-Demand
```
Manual performance check:
- `/performance` - Quick status
- `/performance-detailed` - Full report
- `/performance-benchmark` - Stress test
```

## 📈 Performance Dashboard

### Quick Status (`/performance`):
```
PERFORMANCE STATUS: ✅ OPTIMAL

Response Time:
✓ Avg: 850ms
✓ Fast: 120ms
✓ Slow: 2.5s

Resources:
✓ CPU: 45%
✓ Memory: 1.2GB
✓ Disk: 60%

Health: 98%
Status: All systems normal
```

### Detailed Report (`/performance-detailed`):
```
DETAILED PERFORMANCE REPORT
============================

## Response Times (Last 24h)
- Average: 850ms
- P50: 650ms
- P95: 1.8s
- P99: 3.2s

Top 5 Fastest Tasks:
1. Simple greeting: 120ms
2. Yes/No answers: 180ms
3. Status checks: 220ms
4. Short queries: 350ms
5. Quick facts: 420ms

Top 5 Slowest Tasks:
1. Complex code generation: 8.5s
2. Full research reports: 12s
3. Multi-step workflows: 15s
4. Video generation: 45s
5. Large file processing: 60s

## Resource Usage
- CPU: 45% (avg 52%)
- Memory: 1.2GB / 4GB (30%)
- Disk I/O: Read 15MB/s, Write 5MB/s
- Network: Stable

## Skill Performance
- Fastest: context-mastery (50ms)
- Slowest: ai-video-generator (45s)
- Most used: autonomous-coding (120/day)

## Optimization Suggestions
1. Clear cache (saves 200MB)
2. Optimize database query (saves 1.2s)
3. Enable compression (saves 30% bandwidth)
```

## 🔍 Bottleneck Detection

### Common Bottlenecks:

**Slow Response:**
```
DIAGNOSIS:
- Network latency: High
- Processing time: Normal
- Query speed: Slow

ACTION: Optimize database queries
```

**High Memory:**
```
DIAGNOSIS:
- Cache size: Growing
- Session data: Accumulating
- Memory leaks: Possible

ACTION:
1. Clear old caches
2. Compact sessions
3. Fix memory leak in [module]
```

**CPU Spikes:**
```
DIAGNOSIS:
- Processing: Heavy task
- Multiple tasks: Concurrent
- Inefficient: Algorithm issue

ACTION:
1. Queue heavy tasks
2. Optimize algorithms
3. Add caching
```

## ⚡ Auto-Optimization

### Automatic Actions:

**When Response Slow:**
```
1. Enable caching
2. Compress outputs
3. Reduce verbosity
4. Pre-fetch data
5. Optimize queries
```

**When Memory High:**
```
1. Clear stale caches
2. Compress session data
3. Remove unused imports
4. Optimize data structures
5. Run garbage collection
```

**When CPU High:**
```
1. Queue non-urgent tasks
2. Parallelize where possible
3. Use more efficient algorithms
4. Implement batching
5. Scale horizontally
```

## 🛠️ Commands

### `/performance`
Quick status check:
```
PERFORMANCE: ✅ OPTIMAL

Response: 850ms avg
Resources: Normal
Health: 98%
```

### `/performance-detailed`
Full performance report:
```
Detailed metrics for all areas...
```

### `/benchmark`
Run performance benchmark:
```
BENCHMARK STARTED

Testing...
✓ Simple queries: [X]
✓ Complex tasks: [Y]
✓ Skill efficiency: [Z]

Result: Performance Grade [A/B/C/D]
Recommendations: [optimization tips]
```

### `/optimize`
Run auto-optimization:
```
AUTO-OPTIMIZATION

Actions taken:
1. Cleared cache: +200MB
2. Compressed logs: -150MB
3. Optimized queries: +1.2s faster
4. Enabled compression: -30% bandwidth

Performance improved by: 25%
```

### `/monitor <metric>`
Monitor specific metric:
```
MONITORING: Response Time

Current: 850ms
Threshold: <1000ms ✅
Trend: Stable
Alerts: None
```

### `/alert`
Set performance alerts:
```
ALERTS CONFIGURED:

⚠️ Response time > 3s → Alert
⚠️ Memory > 3GB → Alert
⚠️ CPU > 80% → Alert
⚠️ Error rate > 5% → Alert
```

## 📊 Performance History

### Track Over Time:
```
PERFORMANCE TREND (Last 7 days):

Response Time:
Day 1: 920ms
Day 2: 880ms
Day 3: 850ms
Day 4: 830ms
Day 5: 810ms
Day 6: 790ms
Day 7: 770ms
Trend: ↘️ Improving

Resource Usage:
CPU: 52% → 45% (↓7%)
Memory: 1.5GB → 1.2GB (↓20%)
Disk: Stable
```

## 🚀 Optimization Tips

### For AI Response:
1. **Cache common responses**
2. **Pre-compute frequent queries**
3. **Use streaming for large outputs**
4. **Compress text responses**
5. **Lazy-load heavy features**

### For System:
1. **Clear caches regularly**
2. **Optimize database queries**
3. **Enable async processing**
4. **Use connection pooling**
5. **Monitor and alert proactively**

### For Skills:
1. **Profile skill execution**
2. **Optimize slow skills**
3. **Cache skill outputs**
4. **Batch similar requests**
5. **Parallelize independent tasks**

## 📈 Continuous Improvement

```
WEEKLY OPTIMIZATION:

This week:
- Reduced response time: 10%
- Saved memory: 500MB
- Fixed 3 performance bugs
- Optimized 5 slow skills
- Improved throughput: 25%

Next week focus:
- Optimize video generation
- Reduce database queries
- Improve caching strategy
```

---

**Goal:** Keep OpenClaw running KILAT! ⚡

**Status:** Performance Monitoring ACTIVE  
**Health:** 98%+  
**Optimization:** Continuous
