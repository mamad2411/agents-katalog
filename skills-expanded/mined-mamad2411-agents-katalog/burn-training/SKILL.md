---
name: burn-training
description: This skill should be used when the user asks about "training loop", "Learner", "metrics", "dataset", "dataloader", "checkpointing", "optimizer", "learning rate scheduler", "custom training", or Burn training workflows.
version: 0.1.0
---

# Burn Training

Knowledge for training neural networks with Burn's Learner abstraction and custom loops.

## Learner Setup

The `Learner` orchestrates training with built-in features:

```rust
let learner = LearnerBuilder::new(artifact_dir)
    // Metrics
    .metric_train_numeric(AccuracyMetric::new())
    .metric_valid_numeric(AccuracyMetric::new())
    .metric_train_numeric(LossMetric::new())
    // Checkpointing
    .with_file_checkpointer(CompactRecorder::new())
    // Configuration
    .devices(vec![device.clone()])
    .num_epochs(config.num_epochs)
    .summary()
    .build(model, optim, lr_scheduler);

// Train
let trained_model = learner.fit(dataloader_train, dataloader_valid);
```

## Dataset Implementation

Implement the `Dataset` trait:

```rust
pub struct MyDataset {
    items: Vec<MyItem>,
}

impl Dataset<MyItem> for MyDataset {
    fn get(&self, index: usize) -> Option<MyItem> {
        self.items.get(index).cloned()
    }

    fn len(&self) -> usize {
        self.items.len()
    }
}
```

## Batcher

Convert dataset items to tensors:

```rust
#[derive(Clone)]
pub struct MyBatcher<B: Backend> {
    device: B::Device,
}

impl<B: Backend> Batcher<MyItem, MyBatch<B>> for MyBatcher<B> {
    fn batch(&self, items: Vec<MyItem>) -> MyBatch<B> {
        // Convert items to tensors
        let inputs = items.iter().map(|i| i.input.clone()).collect();
        let targets = items.iter().map(|i| i.target).collect();

        MyBatch {
            inputs: Tensor::stack(inputs, 0).to_device(&self.device),
            targets: Tensor::from_data(targets, &self.device),
        }
    }
}
```

## Metrics

Built-in metrics:
- `AccuracyMetric` — Classification accuracy
- `LossMetric` — Training/validation loss
- `LearningRateMetric` — Current LR

Custom metrics implement the `Metric` trait (not `MetricEntry`).

## Custom Training Loops

For advanced scenarios (multiple optimizers, GAN training):

```rust
for epoch in 0..num_epochs {
    for batch in dataloader.iter() {
        // Forward
        let output = model.forward(batch.inputs);
        let loss = output.cross_entropy(batch.targets);

        // Backward
        let grads = loss.backward();

        // Update
        model = optim.step(lr, model, grads);
    }
}
```

## Additional Resources

Consult `references/topic-map-training.md` for:
- Advanced Learner configuration
- Learning rate schedulers
- Multi-GPU training
- Checkpointing strategies
