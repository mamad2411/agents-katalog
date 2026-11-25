---
name: tensorflow-patterns
description: "When to activate: TensorFlow, Keras, tf.keras, TFX, TF Serving, SavedModel, quantization, TFLite, ONNX, custom layer"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# TensorFlow / Keras Patterns

## Functional API

```python
import tensorflow as tf
from tensorflow import keras

inputs = keras.Input(shape=(128,), name="features")
x = keras.layers.Dense(256, activation="relu")(inputs)
x = keras.layers.Dropout(0.3)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(64, activation="relu")(x)
outputs = keras.layers.Dense(1, activation="sigmoid", name="output")(x)

model = keras.Model(inputs=inputs, outputs=outputs, name="classifier")
model.compile(
    optimizer=keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy", keras.metrics.AUC(name="auc")],
)
```

## Custom Layer

```python
class MultiHeadAttentionPooling(keras.layers.Layer):
    def __init__(self, num_heads: int, key_dim: int, **kwargs):
        super().__init__(**kwargs)
        self.attn = keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=key_dim)
        self.norm = keras.layers.LayerNormalization()

    def call(self, x, training=False):
        # x: (batch, seq_len, dim)
        attended = self.attn(x, x, training=training)
        normed = self.norm(x + attended)
        return tf.reduce_mean(normed, axis=1)  # (batch, dim)
```

## Custom Training Loop

```python
optimizer = keras.optimizers.Adam(1e-3)
loss_fn = keras.losses.BinaryCrossentropy()

@tf.function
def train_step(x_batch, y_batch):
    with tf.GradientTape() as tape:
        logits = model(x_batch, training=True)
        loss = loss_fn(y_batch, logits)
        loss += sum(model.losses)  # regularization
    grads = tape.gradient(loss, model.trainable_weights)
    optimizer.apply_gradients(zip(grads, model.trainable_weights))
    return loss

for epoch in range(20):
    for x_batch, y_batch in train_dataset:
        loss = train_step(x_batch, y_batch)
    print(f"Epoch {epoch+1}, loss={loss:.4f}")
```

## Callbacks

```python
callbacks = [
    keras.callbacks.ModelCheckpoint(
        "best_model.keras", monitor="val_auc", save_best_only=True, mode="max"
    ),
    keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-6),
    keras.callbacks.TensorBoard(log_dir="logs/", histogram_freq=1),
]

model.fit(train_ds, validation_data=val_ds, epochs=50, callbacks=callbacks)
```

## SavedModel & TF Serving

```python
# Save
model.export("serving/classifier/1")

# TF Serving docker:
# docker run -p 8501:8501 \
#   -v $(pwd)/serving:/models \
#   -e MODEL_NAME=classifier \
#   tensorflow/serving

# Inference via REST
import requests
payload = {"instances": X_test[:5].tolist()}
resp = requests.post("http://localhost:8501/v1/models/classifier:predict", json=payload)
predictions = resp.json()["predictions"]
```

## TFLite Quantization

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Post-training dynamic quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Full integer quantization (requires representative dataset)
def representative_data_gen():
    for batch in train_dataset.take(100):
        yield [batch[0]]

converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()
with open("model_quant.tflite", "wb") as f:
    f.write(tflite_model)
```

## Export to ONNX

```python
import tf2onnx
import onnx

model_proto, _ = tf2onnx.convert.from_keras(
    model,
    input_signature=[tf.TensorSpec((None, 128), tf.float32, name="features")],
    opset=17,
    output_path="model.onnx",
)
```

## Key Patterns

- Use `tf.data` pipelines with `prefetch(tf.data.AUTOTUNE)` and `cache()` for GPU utilization
- Enable mixed precision: `keras.mixed_precision.set_global_policy("mixed_float16")`
- Use `@tf.function` on the hot path — avoid Python loops inside traced functions
- `model.export()` produces a TF2 SavedModel; `model.save()` produces legacy HDF5
