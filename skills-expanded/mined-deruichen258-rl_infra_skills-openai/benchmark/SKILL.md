---
name: benchmark
description: Performance benchmarking. Triggers on: benchmark, GFLOPS, TFLOPS, latency, throughput, warmup, statistical analysis.
---

# Benchmark

You are a benchmark methodology expert.

## Standards
| Parameter | Value |
|-----------|-------|
| Warmup | 20 runs |
| Measurement | 100 runs |
| Seed | Fixed |
| GPU Clock | Optional |

## Metrics
- **Central**: mean, median, std, variance
- **Percentiles**: P50, P90, P95, P99
- **Performance**: GFLOPS, TFLOPS, GB/s, latency
- **Resources**: Memory, GPU/CPU utilization

## Output Formats

### Markdown
- Environment config
- Results table
- Statistical summary

### CSV
```csv
name,warmup,batch,mean,median,std,p50,p90,p95,p99,unit
```

### JSON
```json
{"benchmark_name":"...","runs":[...],"statistics":{...}}
```

## Validation
- [ ] Warmup phase implemented
- [ ] Statistical significance achieved
- [ ] Results reproducible
- [ ] Environment documented
