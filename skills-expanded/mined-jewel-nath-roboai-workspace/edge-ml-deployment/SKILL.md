---
name: edge-ml-deployment
description: Edge ML inference deployment with TensorRT, ONNX, quantization, Jetson optimization, RLDS, LeRobot, and data pipelines.
category: ai
tags: [edge-ml, tensorrt, onnx, quantization, jetson, deployment, inference, lerobot]
version: "1.0.0"
---

# Edge ML Deployment

Deploying ML models on edge devices for real-time robot control. This skill covers optimization, quantization, and deployment pipelines.

## When to Use

- Deploying perception models on embedded GPUs (Jetson, etc.)
- Optimizing models for real-time inference (< 10ms latency)
- Quantizing models to reduce memory and compute
- Converting PyTorch/TensorFlow to deployment formats (ONNX, TensorRT)
- Setting up data pipelines for robot learning
- Deploying VLA policies on edge devices

## Quick Start

```bash
# Install TensorRT
sudo apt install tensorrt

# Install ONNX
pip install onnx onnxruntime onnxruntime-gpu

# For Jetson
sudo apt install nvidia-jetpack

# For LeRobot
pip install lerobot
```

## Core Concepts

### 1. Model Optimization Pipeline

Convert and optimize models for edge deployment.

```python
import torch
import onnx
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

class ModelOptimizer:
    def __init__(self, model, input_shape):
        self.model = model
        self.input_shape = input_shape
    
    def export_onnx(self, output_path="model.onnx"):
        """Export PyTorch model to ONNX."""
        dummy_input = torch.randn(*self.input_shape)
        
        torch.onnx.export(
            self.model,
            dummy_input,
            output_path,
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={"input": {0: "batch_size"}},
            opset_version=13
        )
        
        # Verify
        onnx_model = onnx.load(output_path)
        onnx.checker.check_model(onnx_model)
        return output_path
    
    def build_tensorrt_engine(self, onnx_path, engine_path="model.trt", fp16=True):
        """Build TensorRT engine from ONNX."""
        logger = trt.Logger(trt.Logger.INFO)
        builder = trt.Builder(logger)
        network = builder.create_network(
            1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        )
        parser = trt.OnnxParser(network, logger)
        
        # Parse ONNX
        with open(onnx_path, "rb") as f:
            parser.parse(f.read())
        
        # Build config
        config = builder.create_builder_config()
        config.max_workspace_size = 1 << 30  # 1GB
        
        if fp16:
            config.set_flag(trt.BuilderFlag.FP16)
        
        # Build engine
        engine = builder.build_engine(network, config)
        
        # Save
        with open(engine_path, "wb") as f:
            f.write(engine.serialize())
        
        return engine
    
    def quantize_static(self, onnx_path, output_path="model_quant.onnx"):
        """Apply static quantization."""
        from onnxruntime.quantization import quantize_static, CalibrationDataReader
        
        class DataReader(CalibrationDataReader):
            def __init__(self):
                self.enum_data = []
                for _ in range(100):
                    self.enum_data.append(
                        np.random.randn(*self.input_shape).astype(np.float32)
                    )
                self.enum_data = iter(self.enum_data)
            
            def get_next(self):
                return next(self.enum_data, None)
        
        quantize_static(onnx_path, output_path, DataReader())
        return output_path
```

### 2. TensorRT Inference

High-performance inference on NVIDIA GPUs.

```python
import tensorrt as trt
import pycuda.driver as cuda
import numpy as np

class TensorRTInference:
    def __init__(self, engine_path):
        self.logger = trt.Logger(trt.Logger.WARNING)
        
        # Load engine
        with open(engine_path, "rb") as f:
            runtime = trt.Runtime(self.logger)
            self.engine = runtime.deserialize_cuda_engine(f.read())
        
        self.context = self.engine.create_execution_context()
        
        # Allocate buffers
        self.allocate_buffers()
    
    def allocate_buffers(self):
        self.inputs = []
        self.outputs = []
        self.bindings = []
        
        for i in range(self.engine.num_bindings):
            shape = self.engine.get_binding_shape(i)
            size = trt.volume(shape)
            dtype = trt.nptype(self.engine.get_binding_dtype(i))
            
            # Allocate host and device memory
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            
            self.bindings.append(int(device_mem))
            
            if self.engine.binding_is_input(i):
                self.inputs.append({"host": host_mem, "device": device_mem})
            else:
                self.outputs.append({"host": host_mem, "device": device_mem})
    
    def infer(self, input_data):
        # Copy input to device
        np.copyto(self.inputs[0]["host"], input_data.ravel())
        cuda.memcpy_htod(self.inputs[0]["device"], self.inputs[0]["host"])
        
        # Execute
        self.context.execute_v2(bindings=self.bindings)
        
        # Copy output to host
        cuda.memcpy_dtoh(self.outputs[0]["host"], self.outputs[0]["device"])
        
        return self.outputs[0]["host"].copy()

# Usage
trt_infer = TensorRTInference("model.trt")
output = trt_infer.infer(input_batch)
```

### 3. Jetson Deployment

Optimize for NVIDIA Jetson edge devices.

```bash
# On Jetson, use JetPack
sudo apt update
sudo apt install nvidia-jetpack

# MAXN mode for maximum performance
sudo nvpmodel -m 0
sudo jetson_clocks

# Monitor
jtop  # Install with: sudo pip3 install jetson-stats
```

```python
# Jetson-specific optimizations
class JetsonOptimizer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def optimize_for_jetson(self, model):
        """Apply Jetson-specific optimizations."""
        # Convert to TorchScript
        model.eval()
        example_input = torch.randn(1, 3, 224, 224).to(self.device)
        
        # Trace
        traced_model = torch.jit.trace(model, example_input)
        
        # Optimize for inference
        optimized = torch.jit.optimize_for_inference(traced_model)
        
        return optimized
    
    def benchmark(self, model, input_shape, num_runs=100):
        """Benchmark inference latency."""
        import time
        
        dummy_input = torch.randn(*input_shape).to(self.device)
        
        # Warmup
        for _ in range(10):
            _ = model(dummy_input)
        
        # Benchmark
        torch.cuda.synchronize()
        start = time.time()
        
        for _ in range(num_runs):
            _ = model(dummy_input)
        
        torch.cuda.synchronize()
        elapsed = time.time() - start
        
        latency_ms = (elapsed / num_runs) * 1000
        fps = num_runs / elapsed
        
        print(f"Latency: {latency_ms:.2f} ms")
        print(f"FPS: {fps:.1f}")
        
        return latency_ms, fps
```

### 4. Robot Learning Data Pipeline

RLDS and LeRobot for robot learning datasets.

```python
# LeRobot dataset format
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset

dataset = LeRobotDataset.create(
    repo_id="username/robot_task",
    robot_type="panda",
    fps=30,
    features={
        "observation.image": {"dtype": "image", "shape": (224, 224, 3), "names": ["height", "width", "channels"]},
        "observation.state": {"dtype": "float32", "shape": (7,), "names": ["joint_pos"]},
        "action": {"dtype": "float32", "shape": (7,), "names": ["joint_target"]},
    }
)

# Add episode
dataset.add_frame({"observation.image": image, "observation.state": state, "action": action})
dataset.save_episode()

# Load and train
from lerobot.common.policies.act.configuration_act import ACTConfig
from lerobot.common.policies.act.modeling_act import ACTPolicy

cfg = ACTConfig()
policy = ACTPolicy(cfg, dataset_stats=dataset.stats)

# Training loop
for batch in dataloader:
    loss, _ = policy.forward(batch)
    loss.backward()
    optimizer.step()
```

## Configuration Reference

| Platform | Format | Latency | Memory |
|----------|--------|---------|--------|
| Jetson Nano | TensorRT FP16 | 10-30ms | 4GB |
| Jetson Orin | TensorRT FP16 | 2-5ms | 16GB |
| x86 + GPU | TensorRT FP32 | 1-3ms | 24GB+ |
| ARM CPU | ONNX Quantized | 50-100ms | 2GB |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| High latency | Batch size too small | Increase batch, use TensorRT |
| Out of memory | Model too large | Quantize to INT8, prune |
| Accuracy drop | Quantization | Use calibration, partial quantization |

## Common Patterns

### Pattern 1: Full TensorRT Engine Build Pipeline (Jetson)

Complete, copy-paste-ready pipeline for converting a PyTorch model to a TensorRT engine and serialising it to disk.

```python
import torch
import onnx
import onnxruntime as ort
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
from pathlib import Path

# ─── Step 1: train / load your PyTorch model ───────────────────────────────
# Assumes model outputs a single tensor (e.g. action prediction)
model = torch.load("policy.pt", map_location="cuda")
model.eval()

obs_dim = 24       # Example: 24-dim robot state vector
batch_size = 1     # Edge devices almost always run batch=1

# ─── Step 2: export to ONNX ────────────────────────────────────────────────
onnx_path = Path("policy.onnx")
dummy = torch.randn(batch_size, obs_dim, device="cuda")

torch.onnx.export(
    model,
    dummy,
    str(onnx_path),
    input_names=["observation"],
    output_names=["action"],
    opset_version=13,
    dynamic_axes={"observation": {0: "batch"}, "action": {0: "batch"}},
    do_constant_folding=True,
)

# Verify the exported graph is valid
onnx_model = onnx.load(str(onnx_path))
onnx.checker.check_model(onnx_model)
print(f"ONNX export OK — {onnx_path.stat().st_size // 1024} KB")

# ─── Step 3: quick ONNX Runtime sanity-check ───────────────────────────────
sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
ort_out = sess.run(None, {"observation": np.random.randn(1, obs_dim).astype(np.float32)})
print(f"ORT output shape: {ort_out[0].shape}")

# ─── Step 4: build TensorRT FP16 engine ────────────────────────────────────
TRT_LOGGER = trt.Logger(trt.Logger.INFO)

def build_engine(onnx_path: Path, engine_path: Path, fp16: bool = True) -> None:
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    )
    parser = trt.OnnxParser(network, TRT_LOGGER)

    with open(str(onnx_path), "rb") as f:
        if not parser.parse(f.read()):
            for i in range(parser.num_errors):
                print(parser.get_error(i))
            raise RuntimeError("ONNX parse failed")

    config = builder.create_builder_config()
    config.max_workspace_size = 512 * (1 << 20)   # 512 MB

    if fp16 and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
        print("FP16 mode enabled")

    # Dynamic shape profile for batch=1
    profile = builder.create_optimization_profile()
    profile.set_shape("observation",
                      min=(1, obs_dim), opt=(1, obs_dim), max=(4, obs_dim))
    config.add_optimization_profile(profile)

    engine = builder.build_engine(network, config)
    if engine is None:
        raise RuntimeError("Engine build failed")

    with open(str(engine_path), "wb") as f:
        f.write(engine.serialize())
    print(f"TensorRT engine saved → {engine_path}")

build_engine(onnx_path, Path("policy.trt"), fp16=True)
```

### Pattern 2: ONNX Export from PyTorch for ARM64 (Raspberry Pi 5)

OrbiBot runs on a Raspberry Pi 5 (ARM64, no dedicated GPU). Use ONNX Runtime CPU with INT8 quantization instead of TensorRT.

```python
import torch
import onnx
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType
from pathlib import Path
import numpy as np
import time

obs_dim = 24
action_dim = 4

class PolicyNet(torch.nn.Module):
    """Example lightweight policy for mecanum robot."""
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(obs_dim, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, action_dim),
            torch.nn.Tanh(),
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        return self.net(obs)

# ─── Export ────────────────────────────────────────────────────────────────
model = PolicyNet()
model.eval()
dummy = torch.zeros(1, obs_dim)

fp32_path = Path("policy_fp32.onnx")
torch.onnx.export(
    model, dummy, str(fp32_path),
    input_names=["obs"], output_names=["action"],
    opset_version=13,
)
onnx.checker.check_model(onnx.load(str(fp32_path)))

# ─── Dynamic INT8 quantization (no calibration data required) ──────────────
int8_path = Path("policy_int8.onnx")
quantize_dynamic(
    str(fp32_path),
    str(int8_path),
    weight_type=QuantType.QInt8,
)
print(f"FP32: {fp32_path.stat().st_size // 1024} KB")
print(f"INT8: {int8_path.stat().st_size // 1024} KB")

# ─── Benchmark on host CPU ─────────────────────────────────────────────────
def benchmark_ort(model_path: Path, n: int = 200) -> float:
    sess_opts = ort.SessionOptions()
    sess_opts.intra_op_num_threads = 4    # RPi 5 has 4 cores
    sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    sess = ort.InferenceSession(str(model_path),
                                sess_opts,
                                providers=["CPUExecutionProvider"])
    data = {"obs": np.random.randn(1, obs_dim).astype(np.float32)}

    # Warm up
    for _ in range(10):
        sess.run(None, data)

    start = time.perf_counter()
    for _ in range(n):
        sess.run(None, data)
    elapsed_ms = (time.perf_counter() - start) / n * 1000

    print(f"{model_path.name}: {elapsed_ms:.2f} ms/inference")
    return elapsed_ms

benchmark_ort(fp32_path)
benchmark_ort(int8_path)
```

### Pattern 3: Quantization-Aware Training Setup

For accuracy-sensitive tasks, QAT produces better INT8 models than post-training quantization.

```python
import torch
import torch.nn as nn
from torch.quantization import (
    get_default_qat_qconfig,
    prepare_qat,
    convert,
)

class QATPolicy(nn.Module):
    """Policy wrapped for quantization-aware training."""

    def __init__(self, obs_dim: int, action_dim: int):
        super().__init__()
        # QuantStub/DeQuantStub bracket the quantizable region
        self.quant = torch.quantization.QuantStub()
        self.dequant = torch.quantization.DeQuantStub()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, 64),     nn.ReLU(),
            nn.Linear(64, action_dim), nn.Tanh(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.quant(x)
        x = self.net(x)
        return self.dequant(x)

def prepare_qat_model(model: QATPolicy) -> QATPolicy:
    model.train()
    model.qconfig = get_default_qat_qconfig("fbgemm")   # x86; use "qnnpack" on ARM
    prepare_qat(model, inplace=True)
    return model

def finalize_qat_model(model: QATPolicy) -> nn.Module:
    """Call after training is complete to fold BN and convert to INT8."""
    model.eval()
    return convert(model, inplace=True)

# Usage
obs_dim, action_dim = 24, 4
policy = QATPolicy(obs_dim, action_dim)
policy = prepare_qat_model(policy)

optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)
dummy_obs = torch.randn(32, obs_dim)
dummy_act = torch.randn(32, action_dim)

for epoch in range(50):
    pred = policy(dummy_obs)
    loss = nn.MSELoss()(pred, dummy_act)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

int8_policy = finalize_qat_model(policy)
torch.save(int8_policy.state_dict(), "policy_qat_int8.pt")
print("QAT INT8 model saved")
```

### Pattern 4: ROS 2 Inference Node with Latency Monitoring (RPi 5 / ARM64)

Complete ROS 2 Jazzy node that loads an ONNX model at startup, subscribes to robot state, and publishes velocity commands — with built-in per-cycle latency tracking.

```python
#!/usr/bin/env python3
"""
orbibot_agent/policy_inference_node.py

ROS 2 inference node for a sim-trained locomotion policy.
Uses ONNX Runtime on ARM64 (Raspberry Pi 5, no GPU).
"""

import time
import numpy as np
import onnxruntime as ort

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

# Module-level constant
INFERENCE_RATE_HZ = 20.0


class PolicyInferenceNode(Node):
    """
    Loads an ONNX policy at startup and runs inference at a fixed rate.

    Topics
    ------
    Subscribes:
      /odometry/filtered  (nav_msgs/Odometry)
      /imu/data_filtered  (sensor_msgs/Imu)
    Publishes:
      /cmd_vel            (geometry_msgs/Twist)
    """

    def __init__(self) -> None:
        super().__init__("policy_inference_node")

        # ── Parameters ────────────────────────────────────────────────────
        self.declare_parameter("model_path", "/opt/orbibot/policies/policy_int8.onnx")
        self.declare_parameter("obs_dim", 24)
        self.declare_parameter("max_linear_vel", 0.5)
        self.declare_parameter("max_angular_vel", 1.9)
        self.declare_parameter("latency_warn_ms", 15.0)

        model_path = self.get_parameter("model_path").value
        self._obs_dim = self.get_parameter("obs_dim").value
        self._max_lin = self.get_parameter("max_linear_vel").value
        self._max_ang = self.get_parameter("max_angular_vel").value
        self._latency_warn_ms = self.get_parameter("latency_warn_ms").value

        # ── Load model once at startup (NOT inside the callback) ───────────
        self._session = self._load_model(model_path)

        # ── State buffers ──────────────────────────────────────────────────
        self._latest_obs: np.ndarray = np.zeros(self._obs_dim, dtype=np.float32)
        self._latency_history: list[float] = []

        # ── Publishers / Subscribers ───────────────────────────────────────
        self._cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        self.create_subscription(
            Odometry, "/odometry/filtered",
            self._odom_callback, qos_profile_sensor_data
        )
        self.create_subscription(
            Imu, "/imu/data_filtered",
            self._imu_callback, qos_profile_sensor_data
        )

        # ── Inference timer ────────────────────────────────────────────────
        self._timer = self.create_timer(1.0 / INFERENCE_RATE_HZ, self._inference_step)

        self.get_logger().info(
            f"PolicyInferenceNode ready — model: {model_path}, "
            f"obs_dim: {self._obs_dim}, rate: {INFERENCE_RATE_HZ} Hz"
        )

    # ── Model loading ──────────────────────────────────────────────────────

    def _load_model(self, model_path: str) -> ort.InferenceSession:
        """Load ONNX model with ARM64-optimised session options."""
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4          # RPi 5 has 4 performance cores
        opts.inter_op_num_threads = 1
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        opts.enable_mem_pattern = True

        sess = ort.InferenceSession(
            model_path,
            sess_options=opts,
            providers=["CPUExecutionProvider"],
        )

        # Warm up: run 20 dummy inferences so the first real call isn't slow
        dummy = {"obs": np.zeros((1, self._obs_dim), dtype=np.float32)}
        for _ in range(20):
            sess.run(None, dummy)

        self.get_logger().info("ONNX model loaded and warmed up")
        return sess

    # ── Sensor callbacks ───────────────────────────────────────────────────

    def _odom_callback(self, msg: Odometry) -> None:
        """Store velocity components from filtered odometry."""
        self._latest_obs[0] = msg.twist.twist.linear.x
        self._latest_obs[1] = msg.twist.twist.linear.y
        self._latest_obs[2] = msg.twist.twist.angular.z

    def _imu_callback(self, msg: Imu) -> None:
        """Store orientation quaternion from filtered IMU."""
        self._latest_obs[3] = msg.orientation.x
        self._latest_obs[4] = msg.orientation.y
        self._latest_obs[5] = msg.orientation.z
        self._latest_obs[6] = msg.orientation.w
        self._latest_obs[7] = msg.angular_velocity.z
        # Remaining obs slots are task-specific (e.g. goal direction, distances)

    # ── Inference step ─────────────────────────────────────────────────────

    def _inference_step(self) -> None:
        """Run one policy inference and publish the resulting command."""
        t_start = time.perf_counter()

        feed = {"obs": self._latest_obs.reshape(1, -1)}
        result = self._session.run(None, feed)
        action = result[0].squeeze()           # Shape: (action_dim,)

        elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        self._latency_history.append(elapsed_ms)

        if elapsed_ms > self._latency_warn_ms:
            self.get_logger().warning(
                f"Inference latency {elapsed_ms:.1f} ms exceeds "
                f"threshold {self._latency_warn_ms} ms",
                throttle_duration_sec=5.0,
            )

        # Log rolling mean every 100 cycles
        if len(self._latency_history) % 100 == 0:
            mean_ms = np.mean(self._latency_history[-100:])
            self.get_logger().info(
                f"Inference latency (last 100): mean={mean_ms:.2f} ms",
                throttle_duration_sec=10.0,
            )

        # Publish cmd_vel (clip to safety limits)
        cmd = Twist()
        cmd.linear.x  = float(np.clip(action[0], -self._max_lin, self._max_lin))
        cmd.linear.y  = float(np.clip(action[1], -self._max_lin, self._max_lin))
        cmd.angular.z = float(np.clip(action[2], -self._max_ang, self._max_ang))
        self._cmd_pub.publish(cmd)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = PolicyInferenceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

### Pattern 5: Model Warm-Up Utility

Always warm up the model before entering the real-time loop. Cold inference is 3–10× slower on ARM due to cache misses and runtime JIT compilation.

```python
import numpy as np
import onnxruntime as ort
import time
from typing import Optional


def warm_up_session(
    session: ort.InferenceSession,
    input_name: str,
    input_shape: tuple,
    n_warmup: int = 30,
    verbose: bool = True,
) -> Optional[float]:
    """
    Run n_warmup dummy inferences to prime CPU caches and ORT kernels.

    Args:
        session: Active ORT InferenceSession.
        input_name: Name of the input tensor (from session.get_inputs()[0].name).
        input_shape: Shape including batch dimension, e.g. (1, 24).
        n_warmup: Number of warm-up iterations (30 is usually enough on RPi 5).
        verbose: Print timing summary if True.

    Returns:
        Mean latency in ms after warm-up, or None if verbose=False.
    """
    dummy = {input_name: np.zeros(input_shape, dtype=np.float32)}

    # Discard first n_warmup runs
    for _ in range(n_warmup):
        session.run(None, dummy)

    if not verbose:
        return None

    # Measure post-warm-up latency
    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        session.run(None, dummy)
        times.append((time.perf_counter() - t0) * 1000.0)

    mean_ms = float(np.mean(times))
    p95_ms  = float(np.percentile(times, 95))
    print(f"Warm-up complete — mean: {mean_ms:.2f} ms, p95: {p95_ms:.2f} ms")
    return mean_ms


# Usage in any node or script
sess = ort.InferenceSession("policy_int8.onnx",
                            providers=["CPUExecutionProvider"])
input_name = sess.get_inputs()[0].name
warm_up_session(sess, input_name, input_shape=(1, 24), n_warmup=30)
```

---

## Anti-Patterns

### ❌ Loading the model inside the subscriber or timer callback

```python
# WRONG — loads from disk on every inference call, adds 200–800 ms of I/O
def _inference_callback(self, msg):
    sess = ort.InferenceSession("policy.onnx")   # ← do NOT do this
    result = sess.run(None, {"obs": obs})
```

**What happens:** The real-time loop stalls for hundreds of milliseconds while the file is read and the graph is compiled. The robot receives stale or no commands and may stop or oscillate.

### ✅ Load once at node construction, reuse the session

```python
class PolicyInferenceNode(Node):
    def __init__(self):
        super().__init__("policy_inference_node")
        # Load ONCE — inside __init__, not in any callback
        self._session = ort.InferenceSession("policy.onnx",
                                             providers=["CPUExecutionProvider"])
        self._warm_up()

    def _warm_up(self):
        dummy = {"obs": np.zeros((1, 24), dtype=np.float32)}
        for _ in range(30):
            self._session.run(None, dummy)

    def _inference_step(self):
        # Fast reuse — already loaded and warmed
        result = self._session.run(None, {"obs": self._obs})
```

---

### ❌ Deploying without benchmarking on the target hardware

```python
# WRONG — benchmark on a laptop with an RTX GPU, then paste to RPi 5
# "It ran at 2 ms on my machine, should be fine"
```

**What happens:** A 2 ms model on a desktop GPU can easily take 80–150 ms on a Raspberry Pi 5 ARM CPU. At 20 Hz control, 80 ms latency means the robot is always acting on 1.6-cycle-old observations, causing oscillation or crashes.

### ✅ Benchmark directly on the deployment device before committing

```python
# Run benchmark_ort() from Pattern 2 on the actual RPi 5
# Require latency_ms < (1000 / control_rate_hz) * 0.5
# For 20 Hz: latency must be < 25 ms to leave 50 % headroom

CONTROL_HZ = 20.0
latency_ms = benchmark_ort(Path("policy_int8.onnx"), n=200)

headroom_ms = (1000.0 / CONTROL_HZ) * 0.5
assert latency_ms < headroom_ms, (
    f"Model too slow for {CONTROL_HZ} Hz: {latency_ms:.1f} ms > {headroom_ms:.1f} ms. "
    "Apply INT8 quantization or prune the model."
)
```

---

### ❌ Ignoring memory limits on embedded hardware

```python
# WRONG — loading a 400 MB FP32 ResNet-50 on a 4 GB RPi 5
# alongside SLAM, EKF, and camera nodes
model = torch.load("resnet50_fp32.pt")   # 400 MB just for the model weights
```

**What happens:** The operating system OOM-kills ROS 2 nodes when physical RAM is exhausted. SLAM or the hardware driver may be killed mid-run, causing the robot to continue driving with no localization.

### ✅ Profile total system memory before deployment

```bash
# On the RPi 5, check total RSS of all ROS 2 nodes at steady state
ros2 topic pub /trigger std_msgs/Bool "{data: true}" &
sleep 5
for pid in $(pgrep -f ros2); do
    ps -p $pid -o pid,rss,comm --no-headers
done | sort -k2 -rn | head -20

# Target: model RSS < 150 MB, total system < 3.2 GB (leave 800 MB headroom)
```

For models larger than 100 MB FP32, always apply at minimum `quantize_dynamic` (Pattern 2) to reduce to INT8 before deploying on the RPi 5.

---

### ❌ Blocking inference in the real-time control loop

```python
# WRONG — inference runs on the main thread, blocking all other callbacks
class BadControlNode(Node):
    def __init__(self):
        super().__init__("bad_node")
        self.create_timer(0.05, self._control_loop)   # 20 Hz

    def _control_loop(self):
        result = self._heavy_model.infer(self._obs)   # May take 40 ms
        self._publish_cmd(result)
        # If infer() takes 40 ms, this callback runs at ~12 Hz, not 20 Hz
        # Worse: all other callbacks are starved during the 40 ms block
```

**What happens:** Under load (e.g. when SLAM is also running), inference spikes above the timer period. ROS 2 callback queues back up, producing timestamp discontinuities in `/odom` and `/scan` that cause SLAM divergence.

### ✅ Use a dedicated callback group and multi-threaded executor

```python
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class CorrectControlNode(Node):
    def __init__(self):
        super().__init__("correct_node")
        # Inference gets its own callback group so it does not block sensors
        self._inference_cg = MutuallyExclusiveCallbackGroup()
        self._sensor_cg    = MutuallyExclusiveCallbackGroup()

        self.create_timer(0.05, self._inference_step,
                          callback_group=self._inference_cg)
        self.create_subscription(Imu, "/imu/data_filtered",
                                 self._imu_cb, qos_profile_sensor_data,
                                 callback_group=self._sensor_cg)

def main(args=None):
    rclpy.init(args=args)
    node = CorrectControlNode()
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)
    executor.spin()
```

---

## Workflow Integration

Edge ML deployment sits at the end of the robot learning pipeline. It receives a trained policy and makes it production-ready for on-board inference.

### Full Pipeline

```
[learning-robotics]   Train policy (BC / DAgger / RL)
        │
        ▼
[sim-to-real]         Validate transfer gap, domain randomize
        │
        ▼
[camera-vision]       Preprocess visual observations (resize, normalise, undistort)
        │
        ▼
[edge-ml-deployment]  Export → quantize → benchmark → ROS 2 node ← YOU ARE HERE
        │
        ▼
[ros2_node_creation]  Wire the inference node into the ROS 2 graph
        │
        ▼
[robot-bringup]       systemd service, watchdog, ordered startup
```

### Step 1 — Receive Checkpoint from `learning-robotics`

The `learning-robotics` skill produces a checkpoint (Stable-Baselines3 `.zip`, PyTorch `.pt`, or LeRobot `.safetensors`). This skill takes over from there.

```python
# learning-robotics hands off a trained SB3 checkpoint
from stable_baselines3 import PPO

policy = PPO.load("checkpoints/indoor_nav_v3.zip")

# Extract the underlying MLP actor for ONNX export
# (SB3 wraps the network; we need the raw nn.Module)
actor = policy.policy.mlp_extractor.policy_net
```

If the policy architecture is too large for the RPi 5 (>100 MB FP32), feed that constraint back to `learning-robotics` and request a smaller network (fewer layers, lower hidden dimension) or knowledge distillation before attempting quantization here.

### Step 2 — Preprocess Visual Inputs with `camera-vision`

If the policy takes RGB images as input (e.g. a VLA or ACT policy), the `camera-vision` skill defines the preprocessing pipeline: undistortion, resizing, and normalisation. Those transforms must match exactly what was used during training.

```python
# camera-vision skill pattern — run BEFORE feeding to the policy
import cv2
import numpy as np

# Load calibration from camera-vision calibration workflow
K = np.load("camera_matrix.npy")
D = np.load("dist_coeffs.npy")

def preprocess_frame(frame: np.ndarray, target_hw=(224, 224)) -> np.ndarray:
    """
    Undistort, resize, and normalise an RGB frame.
    Must match the preprocessing used during sim training (Gazebo camera plugin).
    """
    undistorted = cv2.undistort(frame, K, D)
    resized = cv2.resize(undistorted, (target_hw[1], target_hw[0]),
                         interpolation=cv2.INTER_LINEAR)
    normalised = resized.astype(np.float32) / 255.0
    # ImageNet-style normalisation (if policy was trained with torchvision transforms)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    normalised = (normalised - mean) / std
    return normalised.transpose(2, 0, 1)[np.newaxis]  # NCHW, batch=1
```

The output of `preprocess_frame` is the `"image"` input tensor fed to the ONNX session alongside the robot state vector.

### Step 3 — Export and Quantize (this skill)

Follow Patterns 1–3 above. For the RPi 5 specifically:

- Use ONNX Runtime, not TensorRT (no NVIDIA GPU)
- Use `quantize_dynamic` (Pattern 2) as the default — it requires no calibration data
- Use QAT (Pattern 3) only when dynamic quantization drops accuracy by more than 3 %
- Target: inference latency < 25 ms at 20 Hz for a state-only policy; < 40 ms for a lightweight image policy

```bash
# Validate quantized model size and latency on the target device
scp policy_int8.onnx orbibot@192.168.1.50:/opt/orbibot/policies/
ssh orbibot@192.168.1.50 "python3 /opt/orbibot/scripts/benchmark_policy.py"
```

### Step 4 — Wire into ROS 2 with `ros2_node_creation`

The `ros2_node_creation` skill provides node scaffolding, QoS profiles, and lifecycle node patterns. Use the `PolicyInferenceNode` from Pattern 4 as the base and apply the node creation conventions:

```python
# Follow ros2_node_creation: declare all parameters, use correct QoS
# Use MutuallyExclusiveCallbackGroup for inference (see Anti-Patterns)
# Use qos_profile_sensor_data for all sensor subscriptions
# Publish cmd_vel with depth=10 RELIABLE QoS

self._cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
```

Register the node as a ROS 2 entry point in `setup.py`:

```python
# In orbibot_agent/setup.py
entry_points={
    "console_scripts": [
        "policy_runner = orbibot_agent.policy_inference_node:main",
    ],
},
```

### Step 5 — Deploy with `robot-bringup`

The `robot-bringup` skill defines systemd unit file templates and ordered startup patterns. The policy runner must start after the hardware and localization nodes are ready.

```python
# In orbibot_bringup/launch/robot.launch.py
# Add policy runner as an optional component
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

run_policy = DeclareLaunchArgument("run_policy", default_value="false")

policy_node = Node(
    package="orbibot_agent",
    executable="policy_runner",
    name="policy_inference_node",
    parameters=[{
        "model_path": "/opt/orbibot/policies/policy_int8.onnx",
        "obs_dim": 24,
        "max_linear_vel": 0.5,
        "max_angular_vel": 1.9,
        "latency_warn_ms": 25.0,
    }],
    condition=IfCondition(LaunchConfiguration("run_policy")),
    output="screen",
)
```

### Configuration Reference — ARM64 (RPi 5) vs Jetson

| Parameter | RPi 5 (ARM64, no GPU) | Jetson Orin (GPU) |
|---|---|---|
| Runtime | ONNX Runtime CPU | TensorRT FP16 |
| Quantization | Dynamic INT8 | FP16 engine |
| `intra_op_num_threads` | 4 | 2–4 |
| Warm-up iterations | 30 | 20 |
| Target latency (state policy) | < 25 ms | < 5 ms |
| Target latency (image policy) | < 50 ms | < 15 ms |
| Max model size (FP32) | 100 MB | 500 MB |
| Memory headroom | 800 MB | 2 GB |

### Quick Cross-Skill Reference

| This skill depends on | For |
|---|---|
| `learning-robotics` | Trained checkpoint (input to export pipeline) |
| `sim-to-real` | Transfer-validated policy before deployment |
| `camera-vision` | Image preprocessing that must match training transforms |
| `ros2_node_creation` | Node scaffolding, QoS, callback group patterns |
| `robot-bringup` | systemd service, launch ordering, watchdog |

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering TensorRT, ONNX, quantization, Jetson, LeRobot