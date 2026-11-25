---
name: voyager-debug
description: Systematically debug and fix issues with Axelera AI Voyager SDK pipelines, models, inference, installation, or hardware. Use when the user brings an existing error, log, crash, accuracy issue, or regression, or when the Voyager SDK install is missing, broken, or outdated, the driver or firmware mismatch, or the Metis board is not detected or not working. Prefer voyager-launch when debugging is part of building a new end-to-end pipeline, and voyager-bench for pure performance measurement.
argument-hint: "<issue description>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, Task, mcp__voyager__*
---

# Debug Pipeline or Model

Systematically debug and fix issues with Axelera AI pipelines, models, or inference

## Use This Skill When / Not When

- Use when: the user brings an existing error, crash, log, regression, or
  wrong output.
- Use when: the SDK install is missing, broken, or old, the driver/firmware
  mismatch, or the Metis board is not detected -- follow
  `references/install-and-board-health.md`.
- Not when: debugging is part of building a brand-new pipeline -- route to
  voyager-launch.
- Not when: they want pure performance measurement of a working pipeline --
  route to voyager-bench.
- Process precedence: when a failure is on the table, this skill runs before
  any domain skill changes code or config.

## Instructions

Debug the specified issue: **$ARGUMENTS**

{{INCLUDE common/voyager-sdk-setup.md}}

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Issue Classification

Identify the type of issue:

- **Deployment Error**: Model fails to compile/deploy
- **Runtime Error**: Inference fails or crashes
- **Accuracy Issue**: Model produces incorrect results
- **Performance Issue**: Low throughput or high latency
- **Display Issue**: Visualization problems

### Step 2: Environment Diagnostics

Run initial diagnostics. Only probe hardware directly when
`.voyager-runtime.json` says `execution.mode` is `execute_on_device`.

```bash
# Check environment
echo "AXELERA_FRAMEWORK: $AXELERA_FRAMEWORK"
echo "AXELERA_RUNTIME_DIR: $AXELERA_RUNTIME_DIR"
echo "PYTHONPATH: $PYTHONPATH"

# Check hardware on a Voyager SDK host
axdevice

# Check Python environment
python --version
pip list | grep axelera

# Version evidence for install/driver/firmware problems
axversion            # SDK version
axversion --driver   # driver version
axdevice -v          # firmware + board controller
```

If the problem is the environment itself (SDK missing or old, driver or
firmware mismatch, board not detected, ENOTTY/AXL_IOCTL errors), follow
`references/install-and-board-health.md`: it carries the fresh-install
commands, the v1.7.0 compatibility matrix, the upgrade path including the
post-upgrade driver/model-recompile trap, and the board-not-detected
ladder. Firmware flashing, device reboots, and system package installs
always need explicit user confirmation first.

### Step 3: Deployment Debugging

**Quantization Issues:**

```bash
# Run quantize-only to isolate issues
./deploy.py <model> --mode QUANTIZE

# Enable debug quantization
./deploy.py <model> --mode QUANTIZE_DEBUG

# Check calibration data
ls -la <calibration-data-path>
```

**Compilation Issues:**

```bash
# Verbose compilation logging
./deploy.py <model> --loglevel DEBUG

# Check ONNX model validity
python -c "import onnx; onnx.checker.check_model('<model>.onnx')"

# Verify model inputs/outputs
python -c "import onnx; m = onnx.load('<model>.onnx'); print(m.graph.input, m.graph.output)"
```

**Common deployment errors:**

- "Unsupported operator": Check ONNX opset version, may need model modification
- "Out of memory": Reduce model size or batch size
- "Calibration failed": Check calibration data format and quantity

### Step 4: Runtime Debugging

**Inference Crashes:**

```bash
# Run with verbose logging
./inference.py <model> <source> --loglevel DEBUG

# Check GStreamer pipeline
GST_DEBUG=3 ./inference.py <model> <source>

# Check for segfaults
gdb --args python inference.py <model> <source>
```

**Stream Issues:**

```bash
# Test input source independently
gst-launch-1.0 uridecodebin uri=file:///path/to/video.mp4 ! fakesink

# Check USB camera
v4l2-ctl --list-devices
gst-launch-1.0 v4l2src device=/dev/video0 ! fakesink
```

### Step 5: Accuracy Debugging

**Evaluate Model Accuracy:**

```bash
# Run accuracy evaluation
./inference.py <model> dataset --no-display

# Compare with reference implementation
# Check preprocessing matches training
# Verify postprocessing/decoder settings
```

**Common accuracy issues:**

- Wrong normalization (mean/std values)
- Incorrect input resolution
- Wrong color space (RGB vs BGR)
- Decoder threshold settings

**Debug preprocessing:**

First search the local SDK tree or Voyager RAG for an existing debug operator
or trace hook. Do not add ad-hoc YAML operators such as `AxDebugSave` unless
the checked SDK version contains that exact operator.

### Step 6: Performance Debugging

**Measure Throughput:**

```bash
# Benchmark mode (see voyager-bench for full benchmarking)
./inference.py <model> <source> --no-display --frames 500 --show-stats

# Save performance tracers
./inference.py <model> <source> --save-tracers perf.csv --show-stats
```

**Performance Metrics:**

- System throughput: End-to-end FPS
- Device throughput: device-only FPS
- CPU utilization: Host CPU usage
- Latency: Frame processing time

**Common performance issues:**

- CPU bottleneck: Check preprocessing complexity
- Memory bandwidth: Check tensor sizes
- Pipeline stalls: Check synchronization

### Step 7: Display Debugging

**No Display:**

```bash
# Check display availability
echo $DISPLAY

# Try different renderers
./inference.py <model> <source> --display opencv
./inference.py <model> <source> --display console
./inference.py <model> <source> --no-display
```

**OpenGL Issues:**

```bash
# Check OpenGL support
glxinfo | head -20

# Fallback to OpenCV
./inference.py <model> <source> --display opencv
```

### Step 8: YAML Pipeline Debugging

**Validate YAML:**

```python
import yaml
with open('ax_models/path/to/model.yaml') as f:
    config = yaml.safe_load(f)
    print(yaml.dump(config, default_flow_style=False))
```

**Check operator configuration:**

- Verify operator types are valid
- Check parameter types and ranges
- Ensure input/output connections are correct

### Step 9: GStreamer Pipeline Debugging

```bash
# List available elements
gst-inspect-1.0 | grep ax

# Check specific element
gst-inspect-1.0 axinference

# Debug pipeline construction
GST_DEBUG=4 ./inference.py <model> <source>

# Generate pipeline graphs: the GST pipe writes *.dot/*.svg itself when
# TRACE logging is enabled; collect them from the run's logging directory.
./inference.py <model> <source> --loglevel TRACE
```

### Step 10: Model-Specific Debugging

**YOLO Models:**

- Check anchor configuration
- Verify class count matches dataset
- Check stride configuration

**Classification Models:**

- Verify input normalization
- Check class label mapping
- Verify top-k settings

**Segmentation Models:**

- Check output resolution
- Verify class IDs
- Check threshold settings

### Step 11: Logging and Tracing

```bash
# Enable all logging
./inference.py <model> <source> --loglevel TRACE

# Save logs to file
./inference.py <model> <source> --loglevel DEBUG 2>&1 | tee debug.log

# Enable GStreamer tracing
GST_TRACERS="latency;stats" ./inference.py <model> <source>
```

### Step 12: Collecting Debug Information

For reporting issues, collect:

```bash
# System info
uname -a
cat /etc/os-release
python --version

# SDK version
cat $AXELERA_FRAMEWORK/RELEASE_NOTES.md | head -5

# Hardware info
axdevice
lspci | grep -i axelera

# Error logs
./deploy.py <model> --loglevel DEBUG 2>&1 | tee deploy_debug.log
```

### Step 13: Resolution Steps

After identifying the issue:

1. Document the root cause
2. Implement fix (code, configuration, or environment)
3. Test the fix thoroughly
4. Verify no regression in other functionality
5. Update documentation if needed

### Step 14: Summary Report

Provide a summary including:

- Issue description
- Root cause identified
- Solution implemented
- Files modified
- Axelera Voyager task ID for reference

## Parallel Orchestration

See `common/agent-orchestration.md` for the full lane rules. For this skill:

- Fan out read-only investigation lanes in parallel: driver/runtime state,
  model and YAML configuration, source/media integrity, and environment/venv
  checks.
- Serialize any on-device reproduction run; exactly one process may use the
  Metis device at a time.
- Reconcile the lanes' hypotheses into one root-cause picture before changing
  anything.
