---
name: "tensorflow-patterns"
description: "TensorFlow patterns with code: the Keras functional API, an optimized tf.data pipeline, custom layers and losses, SavedModel export with a serving signature, and TFLite post-training quantization. Use when building or exporting TensorFlow models."
---

# TensorFlow Patterns

Expert patterns for Keras functional API, tf.data pipeline ordering, custom layers, SavedModel export, and TFLite quantization.

## Pattern 1: Keras Functional API Model

Multi-input model with proper BatchNorm and Dropout usage.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_classifier(
    numeric_dim: int,
    cat_vocab_sizes: dict,   # {"country": 50, "device": 10}
    embedding_dim: int = 16,
    hidden_units: list = [256, 128],
    dropout_rate: float = 0.3,
    num_classes: int = 2,
) -> keras.Model:
    """Functional API model with numeric + categorical inputs."""

    # Numeric input
    numeric_input = keras.Input(shape=(numeric_dim,), name="numeric")
    x_num = layers.BatchNormalization()(numeric_input)
    x_num = layers.Dense(64, activation="relu")(x_num)

    # Categorical inputs with embeddings
    cat_inputs = []
    cat_embeddings = []
    for col, vocab_size in cat_vocab_sizes.items():
        inp = keras.Input(shape=(1,), dtype=tf.int32, name=col)
        emb = layers.Embedding(vocab_size + 1, embedding_dim, name=f"emb_{col}")(inp)
        emb = layers.Flatten()(emb)
        cat_inputs.append(inp)
        cat_embeddings.append(emb)

    # Concatenate all features
    all_inputs = cat_inputs + [numeric_input]
    x = layers.Concatenate()([x_num] + cat_embeddings)

    # Hidden layers
    for units in hidden_units:
        x = layers.Dense(units)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.Dropout(dropout_rate)(x)

    output = layers.Dense(num_classes, activation="softmax", name="output")(x)

    model = keras.Model(inputs=all_inputs, outputs=output, name="classifier")
    return model

model = build_classifier(numeric_dim=20, cat_vocab_sizes={"country": 50, "device": 10})
model.compile(
    optimizer=keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=1e-4),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy", keras.metrics.AUC(name="auc")],
)
model.summary()
```

## Pattern 2: Optimized tf.data Pipeline

Correct order: map → cache → shuffle → batch → prefetch.

```python
import tensorflow as tf

AUTO = tf.data.AUTOTUNE

def parse_tfrecord(serialized: tf.Tensor) -> tuple:
    """Parse a TFRecord example."""
    feature_desc = {
        "image": tf.io.FixedLenFeature([], tf.string),
        "label": tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(serialized, feature_desc)
    image = tf.image.decode_jpeg(example["image"], channels=3)
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.image.resize(image, [224, 224])
    return image, example["label"]

@tf.function
def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, max_delta=0.1)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    return image, label

def build_dataset(tfrecord_pattern: str, batch_size: int,
                  training: bool = True) -> tf.data.Dataset:
    files = tf.data.Dataset.list_files(tfrecord_pattern, shuffle=training)
    dataset = files.interleave(
        tf.data.TFRecordDataset,
        cycle_length=8,                   # read 8 files in parallel
        num_parallel_calls=AUTO,
    )

    dataset = dataset.map(parse_tfrecord, num_parallel_calls=AUTO)

    if training:
        dataset = dataset.map(augment, num_parallel_calls=AUTO)

    # CORRECT ORDER: cache after augmentation (if RAM permits), before shuffle
    # Omit cache() if dataset > available RAM
    # dataset = dataset.cache()

    if training:
        dataset = dataset.shuffle(buffer_size=10_000, reshuffle_each_iteration=True)

    dataset = dataset.batch(batch_size, drop_remainder=training)
    dataset = dataset.prefetch(AUTO)       # always last

    return dataset

train_ds = build_dataset("data/train-*.tfrecord", batch_size=64, training=True)
val_ds = build_dataset("data/val-*.tfrecord", batch_size=128, training=False)
```

## Pattern 3: Custom Keras Layer and Loss

Custom attention layer and focal loss for imbalanced classification.

```python
import tensorflow as tf
from tensorflow import keras

class SelfAttentionPooling(keras.layers.Layer):
    """Attention-weighted pooling over sequence dimension."""

    def __init__(self, units: int = 64, **kwargs):
        super().__init__(**kwargs)
        self.units = units

    def build(self, input_shape):
        self.W = self.add_weight(
            name="attention_W",
            shape=(input_shape[-1], self.units),
            initializer="glorot_uniform",
            trainable=True,
        )
        self.V = self.add_weight(
            name="attention_V",
            shape=(self.units, 1),
            initializer="glorot_uniform",
            trainable=True,
        )
        super().build(input_shape)

    def call(self, inputs, mask=None):
        # inputs: (batch, seq_len, features)
        score = tf.nn.tanh(tf.matmul(inputs, self.W))   # (batch, seq, units)
        score = tf.matmul(score, self.V)                  # (batch, seq, 1)
        if mask is not None:
            score += (1.0 - tf.cast(mask[:, :, tf.newaxis], tf.float32)) * -1e9
        weights = tf.nn.softmax(score, axis=1)            # (batch, seq, 1)
        return tf.reduce_sum(inputs * weights, axis=1)    # (batch, features)

    def get_config(self):
        return {**super().get_config(), "units": self.units}


class FocalLoss(keras.losses.Loss):
    """Focal loss for class imbalance (Lin et al. 2017)."""

    def __init__(self, gamma: float = 2.0, alpha: float = 0.25, **kwargs):
        super().__init__(**kwargs)
        self.gamma = gamma
        self.alpha = alpha

    def call(self, y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
        cross_entropy = -y_true * tf.math.log(y_pred)
        p_t = tf.where(tf.equal(y_true, 1), y_pred, 1 - y_pred)
        focal_factor = (1 - p_t) ** self.gamma
        alpha_t = tf.where(tf.equal(y_true, 1), self.alpha, 1 - self.alpha)
        return tf.reduce_mean(alpha_t * focal_factor * cross_entropy)
```

## Pattern 4: SavedModel Export with Serving Signature

Export model with explicit input/output signatures for TF Serving.

```python
import tensorflow as tf

def export_saved_model(model: tf.keras.Model, export_path: str,
                        input_spec: dict):
    """Export with serving_default signature for TF Serving."""

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, input_spec["numeric_dim"]],
                      dtype=tf.float32, name="numeric"),
    ])
    def serving_fn(numeric):
        outputs = model({"numeric": numeric}, training=False)
        probabilities = tf.nn.softmax(outputs, axis=-1)
        return {
            "probabilities": probabilities,
            "predicted_class": tf.argmax(probabilities, axis=-1),
        }

    tf.saved_model.save(
        model,
        export_path,
        signatures={"serving_default": serving_fn}
    )
    print(f"SavedModel exported to {export_path}")

    # Verify signature
    loaded = tf.saved_model.load(export_path)
    infer = loaded.signatures["serving_default"]
    print("Input keys:", list(infer.structured_input_signature[1].keys()))
    print("Output keys:", list(infer.structured_outputs.keys()))

export_saved_model(model, "models/classifier/1", {"numeric_dim": 20})
```

## Pattern 5: TFLite Post-Training Quantization

Convert SavedModel to int8 TFLite with calibration.

```python
import tensorflow as tf
import numpy as np

def quantize_to_tflite(saved_model_path: str, output_path: str,
                        calibration_data: np.ndarray) -> dict:
    """Full integer PTQ quantization with calibration dataset."""
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)

    # Enable optimizations (weights in int8)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    # Full integer quantization: needs representative data for activation calibration
    def representative_dataset():
        for i in range(0, len(calibration_data), 32):
            batch = calibration_data[i:i+32].astype(np.float32)
            yield [batch]

    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_model = converter.convert()

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    original_mb = sum(
        p.numpy().nbytes for p in tf.keras.models.load_model(saved_model_path).weights
    ) / 1e6
    quantized_mb = len(tflite_model) / 1e6

    return {
        "original_size_mb": round(original_mb, 2),
        "quantized_size_mb": round(quantized_mb, 2),
        "compression_ratio": round(original_mb / quantized_mb, 2),
    }

stats = quantize_to_tflite("models/classifier/1", "model_int8.tflite",
                             calibration_data=X_val[:500])
print(f"Compression: {stats['compression_ratio']}x ({stats['original_size_mb']}MB → {stats['quantized_size_mb']}MB)")
```

## Anti-Patterns

### Anti-Pattern 1: Wrong tf.data Order (cache After shuffle or batch)
`.cache()` after `.shuffle()` serves the same shuffled order every epoch. `.cache()` after `.batch()` caches batches, preventing re-batching with different sizes. Always: `map → cache → shuffle → batch → prefetch`.

### Anti-Pattern 2: Using HDF5 (.h5) for Production Serving
HDF5 saves architecture + weights but not the computation graph. TF Serving cannot load H5 files. SavedModel format includes the computation graph, serving signatures, and custom layer code. Always export in SavedModel format for any serving use case.

### Anti-Pattern 3: PTQ When Accuracy Loss is Unacceptable
Post-training quantization can cause 2-5% accuracy drop on sensitive tasks (medical imaging, NLP classification). If the task requires < 1% accuracy degradation, use quantization-aware training — it simulates quantization during training and learns weights that are robust to quantization noise.

### Anti-Pattern 4: Setting num_parallel_calls to a Fixed Integer
`num_parallel_calls=4` may over-subscribe on a 2-core machine or under-subscribe on a 32-core machine. Use `tf.data.AUTOTUNE` for all map and interleave calls — it adapts to available hardware at runtime.
