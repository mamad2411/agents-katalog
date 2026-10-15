---
name: neural-networks-forecasting
description: When the user wants to forecast using deep learning, LSTMs, transformers, or neural networks. Also use when the user mentions "neural network forecasting," "LSTM," "GRU," "transformer forecasting," "attention mechanisms," "seq2seq," "temporal convolution," "deep learning time series," or complex non-linear patterns. For traditional forecasting, see demand-forecasting. For general ML, see ml-supply-chain.
---

# Neural Networks for Forecasting

You are an expert in applying neural networks and deep learning to supply chain forecasting. Your goal is to build sophisticated deep learning models (LSTM, GRU, Transformers) that capture complex temporal patterns, seasonality, and non-linear relationships in demand data.

## Initial Assessment

1. **Data Volume**: Sufficient data? (NNs need 1000+ samples)
2. **Patterns**: Complex non-linear or long-term dependencies?
3. **Features**: Multi-variate or univariate?
4. **Horizon**: Short-term or long-term forecasting?
5. **Resources**: GPU available for training?

---

## LSTM for Demand Forecasting

```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

class LSTMForecaster:
    """
    LSTM-based demand forecasting
    """
    
    def __init__(self, sequence_length=30, forecast_horizon=7):
        self.seq_len = sequence_length
        self.horizon = forecast_horizon
        self.model = None
    
    def build_model(self, n_features):
        """Build LSTM architecture"""
        
        model = keras.Sequential([
            # First LSTM layer
            layers.LSTM(128, return_sequences=True,
                       input_shape=(self.seq_len, n_features)),
            layers.Dropout(0.2),
            
            # Second LSTM layer  
            layers.LSTM(64, return_sequences=True),
            layers.Dropout(0.2),
            
            # Third LSTM layer
            layers.LSTM(32, return_sequences=False),
            layers.Dropout(0.2),
            
            # Output layer
            layers.Dense(32, activation='relu'),
            layers.Dense(self.horizon)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
```

---

## Transformer for Multi-Horizon Forecasting

```python
class TransformerForecaster:
    """
    Transformer with self-attention for forecasting
    """
    
    def build_model(self, seq_len, n_features, horizon):
        inputs = layers.Input(shape=(seq_len, n_features))
        
        # Positional encoding
        x = self.positional_encoding(inputs)
        
        # Multi-head attention
        attention_output = layers.MultiHeadAttention(
            num_heads=8,
            key_dim=64
        )(x, x)
        
        x = layers.Add()([x, attention_output])
        x = layers.LayerNormalization()(x)
        
        # Feed-forward
        ff = layers.Dense(256, activation='relu')(x)
        ff = layers.Dense(n_features)(ff)
        
        x = layers.Add()([x, ff])
        x = layers.LayerNormalization()(x)
        
        # Output
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(128, activation='relu')(x)
        outputs = layers.Dense(horizon)(x)
        
        model = keras.Model(inputs, outputs)
        model.compile(optimizer='adam', loss='mse')
        
        return model
```

---

## Temporal Convolutional Network (TCN)

```python
class TCNForecaster:
    """
    TCN with dilated convolutions
    """
    
    def build_tcn_block(self, x, filters, kernel_size, dilation_rate):
        # Dilated causal convolution
        conv = layers.Conv1D(
            filters=filters,
            kernel_size=kernel_size,
            padding='causal',
            dilation_rate=dilation_rate,
            activation='relu'
        )(x)
        
        conv = layers.Dropout(0.2)(conv)
        
        # Residual connection
        if x.shape[-1] != filters:
            x = layers.Conv1D(filters, 1)(x)
        
        return layers.Add()([x, conv])
```

---

## Ensemble Neural Networks

```python
def ensemble_forecast(models, X_test):
    """
    Combine predictions from multiple NN models
    """
    
    predictions = []
    for model in models:
        pred = model.predict(X_test)
        predictions.append(pred)
    
    # Average ensemble
    ensemble_pred = np.mean(predictions, axis=0)
    
    return ensemble_pred
```

---

## Tools & Libraries

- `TensorFlow/Keras`: deep learning
- `PyTorch`: flexible NNs
- `N-BEATS`: specialized forecasting NN
- `DeepAR`: probabilistic forecasting

---

## Related Skills

- **demand-forecasting**: traditional methods
- **ml-supply-chain**: general ML
- **optimization-ml-hybrid**: combine with optimization
