---
name: voyager-bench
description: Benchmark model performance on Axelera AI Metis hardware with the Voyager SDK. Use when the user wants to measure FPS, throughput, latency, or compare model variants. Use to quantify a working pipeline. Prefer voyager-debug when performance is a suspected fault or regression.
argument-hint: "<model> [options]"
allowed-tools: Read, Bash, Glob, Grep, Task, mcp__voyager__*
---

# Benchmark Model Performance

Measure and analyze model performance on Axelera AI hardware

## Use This Skill When / Not When

- Use when: the user wants to quantify a working pipeline (FPS, latency,
  throughput, model-variant comparisons).
- Not when: performance is a suspected fault or regression -- route to
  voyager-debug.
- Not when: the pipeline still needs to be built -- route to voyager-launch.

## Instructions

Benchmark the specified model/pipeline: **$ARGUMENTS**

{{INCLUDE common/voyager-sdk-setup.md}}

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Environment Setup

```bash
# Environment activation is handled by Step 0/Step 3 of the setup
# include (venv/ or axelera-env/); verify it is active
python -c "import axelera" 2>/dev/null || echo "SDK env not active"

# Verify hardware only when .voyager-runtime.json reports execute_on_device
axdevice
```

### Step 2: Basic Benchmarking

Run benchmark on deployed model using inference with performance flags:

```bash
# Benchmark with video file (run N frames, no display, show stats)
./inference.py <model> media/traffic1_1080p.mp4 --no-display --frames 500 --show-stats

# Benchmark with SDK fake video source (synthetic frames, low I/O overhead)
./inference.py <model> fakevideo:640x480@30 --no-display --frames 1000 --show-stats

# Benchmark and save tracer data to CSV
./inference.py <model> <source> --no-display --frames 1000 --show-stats --save-tracers perf.csv
```

### Step 3: Performance Metrics

Key metrics to measure:

- **System Throughput (FPS)**: End-to-end pipeline performance
- **Device Throughput (FPS)**: AIPU-only performance
- **Latency (ms)**: Time per frame
- **CPU Utilization (%)**: Host CPU usage

### Step 4: Detailed Performance Tracing

```bash
# Enable statistics display
./inference.py <model> <source> --show-stats

# Save tracer data to CSV
./inference.py <model> <source> --save-tracers performance.csv

# Append to existing file (for comparison)
./inference.py <model> <source> --save-tracers +performance.csv
```

### Step 5: Multi-Stream Benchmarking

```bash
# Benchmark multiple streams
./inference.py <model> video1.mp4 video2.mp4 --no-display --frames 500 --show-stats --save-tracers multi.csv

# Maximum stream capacity test
./inference.py <model> usb:0 usb:1 video.mp4 video2.mp4 --no-display --show-stats --save-tracers capacity.csv
```

### Step 6: Component-Level Profiling

```bash
# GStreamer latency tracing
GST_TRACERS="latency" ./inference.py <model> <source>

# GStreamer statistics
GST_TRACERS="stats" ./inference.py <model> <source>

# Detailed debug output
GST_DEBUG=3 ./inference.py <model> <source>
```

### Step 7: Accuracy vs Performance Analysis

```bash
# Measure accuracy
./inference.py <model> dataset --no-display

# Record both accuracy and performance
./inference.py <model> dataset --no-display --show-stats --save-tracers acc_perf.csv
```

### Step 8: Compare Model Variants

Benchmark different model sizes:

```bash
# Small model
./inference.py yolov8n-coco video.mp4 --no-display --frames 500 --show-stats --save-tracers yolov8n_bench.csv

# Medium model
./inference.py yolov8s-coco video.mp4 --no-display --frames 500 --show-stats --save-tracers yolov8s_bench.csv

# Large model
./inference.py yolov8m-coco video.mp4 --no-display --frames 500 --show-stats --save-tracers yolov8m_bench.csv
```

### Step 9: Resolution Impact

Test different input resolutions only with model names verified by
`./deploy.py --help-network`, local `ax_models/**/*.yaml`, or Voyager SDK RAG. Do not
invent `-320` or `-1280` suffixes.

```bash
# Verified model variant from the SDK model catalog
./inference.py yolov8n-coco video.mp4 --no-display --frames 500 --show-stats --save-tracers res_640.csv
```

### Step 10: Core Configuration Testing

```bash
# Single core
./deploy.py <model> --aipu-cores 1
./inference.py <model> video.mp4 --aipu-cores 1 --no-display --frames 500 --show-stats --save-tracers cores_1.csv

# Dual core
./deploy.py <model> --aipu-cores 2
./inference.py <model> video.mp4 --aipu-cores 2 --no-display --frames 500 --show-stats --save-tracers cores_2.csv

# Quad core
./deploy.py <model> --aipu-cores 4
./inference.py <model> video.mp4 --aipu-cores 4 --no-display --frames 500 --show-stats --save-tracers cores_4.csv
```

Multi-core comparisons apply to the GST/AIPU path. The `torch-aipu` pipe
supports one AIPU core only in current Voyager SDK builds, so do not present
`torch-aipu --aipu-cores 4` as a valid benchmark.

### Step 11: Benchmark Report Generation

The `--save-tracers` CSV header is `timestamp,` followed by the raw metric
keys from `stream.get_all_metrics()`, such as `__end_to_end_fps__`,
`__cpu_usage__`, `__latency__`, and `__core_temp__`. The exact key set varies
by pipeline and tracers, so discover the columns before summarizing:

```python
import pandas as pd

# Load tracer data and discover the real column names
df = pd.read_csv('performance.csv')
print(df.columns.tolist())

print("Performance Summary")
print("=" * 40)
if '__end_to_end_fps__' in df.columns:
    fps = df['__end_to_end_fps__']
    print(f"Average FPS: {fps.mean():.1f}")
    print(f"Min FPS: {fps.min():.1f}")
    print(f"Max FPS: {fps.max():.1f}")
if '__latency__' in df.columns:
    print(f"P95 Latency: {df['__latency__'].quantile(0.95):.1f} ms")
if '__cpu_usage__' in df.columns:
    print(f"CPU Usage: {df['__cpu_usage__'].mean():.1f}%")
```

### Step 12: Performance Bottleneck Analysis

Identify bottlenecks:

**CPU Bottleneck:**

- High CPU utilization (>80%)
- System FPS << Device FPS
- Solution: Optimize preprocessing/postprocessing

**Memory Bottleneck:**

- High memory usage
- Frame drops
- Solution: Reduce batch size, optimize buffers

**I/O Bottleneck:**

- Low device utilization
- Stream stalls
- Solution: Use faster input source, enable buffering

**Device Bottleneck:**

- Device FPS is limiting factor
- CPU utilization low
- Solution: Use smaller model or more cores

### Step 13: Optimization Recommendations

Based on benchmark results:

- If CPU bound: Use OpenCL preprocessing
- If memory bound: Reduce resolution or batch
- If I/O bound: Use hardware decoder
- If device bound: Try model pruning/quantization

### Step 14: Benchmark Comparison Table

Create comparison table:

```
| Model      | Resolution | FPS   | Latency | CPU % | mAP   |
|------------|------------|-------|---------|-------|-------|
| yolov8n    | 640x640    | 120   | 8.3ms   | 45%   | 37.3  |
| yolov8s    | 640x640    | 85    | 11.8ms  | 52%   | 44.9  |
| yolov8m    | 640x640    | 55    | 18.2ms  | 58%   | 50.2  |
```

### Step 15: Continuous Benchmarking

Set up automated benchmarks:

```bash
#!/bin/bash
# benchmark_suite.sh

MODELS="yolov8n-coco yolov8s-coco yolov5s-v7-coco"
SOURCE="media/traffic1_1080p.mp4"
OUTPUT_DIR="benchmark_results/$(date +%Y%m%d)"

mkdir -p $OUTPUT_DIR

for model in $MODELS; do
    echo "Benchmarking $model..."
    ./inference.py $model $SOURCE --no-display \
        --frames 1000 --show-stats \
        --save-tracers "$OUTPUT_DIR/${model}.csv"
done

echo "Results saved to $OUTPUT_DIR"
```

## Parallel Orchestration

See `common/agent-orchestration.md` for the full lane rules. For this skill:

- Serialize every benchmark run. The Metis device is exclusive, and anything
  running in parallel with a measurement invalidates the numbers.
- Run long sweeps as background runners with logs under `results/`; poll the
  log instead of busy-waiting.
- Parallelize post-run work freely: CSV parsing, plots, comparison tables,
  and report writing on already-finished runs.
