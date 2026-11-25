---
name: burn-app-dev
description: This skill should be used when the user asks about "Burn tensors", "tensor operations", "Module derive", "burn config", "autodiff", "backward pass", "gradient", "record serialization", "model weights", or core Burn application development patterns.
version: 0.1.0
---

# Burn Application Development

Core knowledge for building applications with the Burn deep learning framework.

## Tensors

Burn tensors are the fundamental data structure. Three element types:

- `Tensor<B, D, Float>` — Floating point operations
- `Tensor<B, D, Int>` — Integer operations
- `Tensor<B, D, Bool>` — Boolean masks

Key patterns:

```rust
// Creation
let tensor = Tensor::<B, 2>::zeros([batch, features], &device);
let tensor = Tensor::from_data([[1.0, 2.0], [3.0, 4.0]], &device);

// Operations (return new tensors, original unchanged)
let result = tensor.matmul(other);
let result = tensor.relu();

// Clone for multiple uses (cheap, reference counted)
let a = tensor.clone();
let b = tensor.clone();
```

## Modules

Neural network layers use the `Module` derive macro:

```rust
#[derive(Module, Debug)]
pub struct Model<B: Backend> {
    conv: Conv2d<B>,
    pool: AdaptiveAvgPool2d,
    linear: Linear<B>,
    activation: Relu,
}

impl<B: Backend> Model<B> {
    pub fn forward(&self, x: Tensor<B, 4>) -> Tensor<B, 2> {
        let x = self.conv.forward(x);
        let x = self.activation.forward(x);
        let x = self.pool.forward(x);
        let x = x.flatten(1, 3);
        self.linear.forward(x)
    }
}
```

## Config

Type-safe configuration with the `Config` derive:

```rust
#[derive(Config)]
pub struct ModelConfig {
    #[config(default = 64)]
    hidden_size: usize,
    #[config(default = 0.1)]
    dropout: f64,
}

// Usage
let config = ModelConfig::new();
let model = config.init::<B>(&device);
```

## Autodiff

Automatic differentiation for training:

```rust
// AutodiffBackend wraps any backend
type MyBackend = Autodiff<Wgpu>;

// Forward pass tracks gradients
let output = model.forward(input);
let loss = output.cross_entropy(targets);

// Backward pass
let grads = loss.backward();
let grad_tensor = tensor.grad(&grads).unwrap();
```

Key difference from PyTorch: gradients are returned as a separate `Gradients` struct, not stored on tensors.

## Records

Serialization for model weights:

```rust
// Save
let recorder = CompactRecorder::new();
model.save_file("model.bin", &recorder)?;

// Load
let model = config.init::<B>(&device);
let model = model.load_file("model.bin", &recorder, &device)?;
```

## Additional Resources

Consult `references/topic-map-app.md` for:
- Detailed tensor operation reference
- Built-in module catalog (Conv, Pool, RNN, Transformer, Loss)
- Advanced autodiff patterns
- Record format options
