---

## name: federated-learning
description: >
  Federated learning expert for privacy-preserving machine learning and distributed training.
  Use this skill whenever the user needs: building federated learning systems, training models
  across distributed data, implementing privacy techniques, handling non-IID data challenges,
  designing communication-efficient protocols, or any task involving training machine learning
  models without centralizing raw data. This skill covers federated averaging, differential
  privacy, secure aggregation, and real-world FL system design.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: machine-learning

# Federated Learning — Privacy-Preserving Distributed Machine Learning

Covers: **Federated Averaging · Differential Privacy · Secure Aggregation · Non-IID Data · Communication Efficiency · Cross-Device FL · Horizontal/Vertical FL · System Design**

-----

## Federated Learning Fundamentals

### What is Federated Learning?

Federated learning enables distributed data model training across sources without sharing raw data. Instead of moving data to the model, we move the model to the data.

```python
# Basic federated learning architecture
class FederatedLearningSystem:
    def __init__(self, server, clients, model, aggregator):
        self.server = server
        self.clients = clients  # Each client has local data
        self.model = model
        self.aggregator = aggregator
        self.rounds = 0
    
    def train_round(self):
        """
        Execute one round of federated learning.
        """
        # 1. Server sends global model to clients
        global_model = self.server.get_model()
        for client in self.clients:
            client.receive_model(global_model)
        
        # 2. Clients train locally
        client_updates = []
        for client in self.clients:
            local_update = client.train()
            client_updates.append(local_update)
        
        # 3. Server aggregates updates
        global_model = self.aggregator.aggregate(client_updates)
        self.server.update_model(global_model)
        
        self.rounds += 1
        return self.server.evaluate()
    
    def train(self, num_rounds, convergence_threshold=0.01):
        """Run federated training until convergence."""
        history = []
        prev_accuracy = 0
        
        for round_num in range(num_rounds):
            metrics = self.train_round()
            history.append(metrics)
            
            # Check convergence
            if abs(metrics['accuracy'] - prev_accuracy) < convergence_threshold:
                print(f"Converged at round {round_num}")
                break
            
            prev_accuracy = metrics['accuracy']
        
        return history
```

### Types of Federated Learning

| Type | Description | Use Case |
|------|-------------|----------|
| **Horizontal FL** | Same features, different samples | Cross-device (phones, IoT) |
| **Vertical FL** | Different features, same samples | Cross-silo (banks, hospitals) |
| **Transfer FL** | Pre-trained + local adaptation | Knowledge transfer |
| **Split FL** | Model split between server/edge | Edge computing |

```python
# Horizontal Federated Learning
class HorizontalFLClient:
    """
    Horizontal FL: All clients have same feature space,
    different samples.
    """
    def __init__(self, client_id, data, model):
        self.client_id = client_id
        self.data = data  # Local dataset
        self.model = model
    
    def train_local(self, epochs=5):
        """Train on local data."""
        self.model.fit(self.data['X'], self.data['y'], epochs=epochs)
        return self.model.get_weights()

# Vertical Federated Learning
class VerticalFLClient:
    """
    Vertical FL: Different clients have different features
    for the same samples.
    """
    def __init__(self, client_id, features, sample_ids):
        self.client_id = client_id
        self.features = features  # Local feature columns
        self.sample_ids = sample_ids  # Aligned sample IDs
    
    def compute_hidden_representation(self, model):
        """Compute local embeddings for aligned samples."""
        return model.forward(self.features)
```

-----

## Federated Averaging (FedAvg)

### The FedAvg Algorithm

```python
# Federated Averaging (FedAvg)
class FederatedAveraging:
    """
    FedAvg: Weighted averaging of client model updates.
    """
    def __init__(self, client_weights=None):
        self.client_weights = client_weights  # Optional weights
    
    def aggregate(self, client_models):
        """
        Aggregate client models using weighted average.
        
        client_models: List of (num_samples, model_weights) tuples
        """
        if not client_models:
            return None
        
        total_samples = sum(n for n, _ in client_models)
        
        # Initialize aggregated weights
        aggregated = {}
        
        # Get all parameter names
        param_names = client_models[0][1].keys()
        
        for param in param_names:
            weighted_sum = None
            
            for num_samples, model in client_models:
                weight = num_samples / total_samples
                if self.client_weights:
                    weight *= self.client_weights.get(model.get('id', 0), 1.0)
                
                if weighted_sum is None:
                    weighted_sum = weight * model[param]
                else:
                    weighted_sum += weight * model[param]
            
            aggregated[param] = weighted_sum
        
        return aggregated

# FedAvg implementation
def fedavg_round(server_model, clients, local_epochs, batch_size):
    """
    Execute one FedAvg round.
    """
    # Get global model
    global_weights = server_model.get_weights()
    
    client_updates = []
    
    for client in clients:
        # Send global model
        client.set_weights(global_weights)
        
        # Local training
        num_samples = client.local_train(epochs=local_epochs, batch_size=batch_size)
        
        # Get update (model delta)
        delta = server_model.compute_delta(global_weights, client.get_weights())
        
        client_updates.append((num_samples, delta))
    
    # Aggregate
    aggregator = FederatedAveraging()
    new_global_weights = aggregator.aggregate(client_updates)
    
    return server_model.set_weights(new_global_weights)
```

### FedAvg Variants

```python
# FedProx: Handling heterogeneity
class FedProx:
    """
    FedProx: Adds proximal term to handle non-IID data.
    """
    def __init__(self, mu=0.01):
        self.mu = mu  # Proximal parameter
    
    def local_loss(self, model, global_weights, X, y):
        """Local loss with proximal term."""
        # Standard loss
        ce_loss = model.compute_loss(X, y)
        
        # Proximal term: ||θ - θ_global||²
        proximal = 0
        for local_w, global_w in zip(model.weights.values(), global_weights.values()):
            proximal += torch.sum((local_w - global_w) ** 2)
        
        return ce_loss + (self.mu / 2) * proximal

# FedMomentum: Adding momentum
class FedMomentum:
    """
    FedMomentum: Client momentum for faster convergence.
    """
    def __init__(self, momentum=0.9):
        self.momentum = momentum
        self.velocity = {}
    
    def aggregate(self, client_updates):
        """Aggregate with momentum."""
        if not self.velocity:
            # Initialize velocity
            for param in client_updates[0][1].keys():
                self.velocity[param] = torch.zeros_like(client_updates[0][1][param])
        
        # Accumulate momentum
        for _, update in client_updates:
            for param in update.keys():
                self.velocity[param] = self.momentum * self.velocity[param] + update[param]
        
        return self.velocity
```

-----

## Privacy in Federated Learning

### Differential Privacy

```python
import numpy as np

class DifferentialPrivacy:
    """
    Add noise to ensure differential privacy.
    """
    def __init__(self, epsilon=1.0, delta=1e-5, sensitivity=1.0):
        self.epsilon = epsilon  # Privacy budget
        self.delta = delta      # Failure probability
        self.sensitivity = sensitivity  # Maximum change from one sample
    
    def add_noise(self, gradient):
        """
        Add Gaussian noise for (ε, δ)-differential privacy.
        """
        # Compute noise scale
        sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * self.sensitivity / self.epsilon
        
        # Add Gaussian noise
        noise = np.random.normal(0, sigma, gradient.shape)
        
        return gradient + noise
    
    def add_laplace_noise(self, gradient):
        """Add Laplace noise (simpler DP)."""
        b = self.sensitivity / self.epsilon
        noise = np.random.laplace(0, b, gradient.shape)
        
        return gradient + noise

# Rényi Differential Privacy for composition
def rdp_compose(orders, alphas, sigma):
    """
    Compute Rényi DP composition.
    """
    total = 0
    for alpha, order in zip(alphas, orders):
        # Gaussian mechanism Rényi divergence
        rho = order / (2 * sigma**2)
        total += rho
    return total
```

### Secure Aggregation

```python
# Secure Aggregation Protocol
class SecureAggregation:
    """
    Secure aggregation: Clients encrypt updates before sending.
    Server only sees aggregate, not individual updates.
    """
    def __init__(self, num_clients):
        self.num_clients = num_clients
        self.public_keys = {}
        self.secret_keys = {}
    
    def setup_keys(self):
        """Generate key pairs for all clients."""
        import phe
        
        for i in range(self.num_clients):
            pk, sk = phe.generate_paillier_keypair()
            self.public_keys[i] = pk
            self.secret_keys[i] = sk
    
    def encrypt_update(self, client_id, update):
        """Client encrypts their update."""
        return self.public_keys[client_id].encrypt(update)
    
    def aggregate_encrypted(self, encrypted_updates):
        """Server aggregates encrypted updates."""
        # Homomorphic addition of encrypted values
        aggregate = None
        
        for enc_update in encrypted_updates:
            if aggregate is None:
                aggregate = enc_update
            else:
                aggregate = aggregate + enc_update
        
        return aggregate
    
    def decrypt_aggregate(self, aggregate):
        """Server decrypts final aggregate (no individual data)."""
        # Average (divide by number of clients)
        return aggregate / self.num_clients

# Secret Sharing for Secure Aggregation
class SecretSharing:
    """
    Shamir's Secret Sharing for secure aggregation.
    """
    def __init__(self, threshold, num_shares):
        self.threshold = threshold
        self.num_shares = num_shares
    
    def share(self, secret):
        """Split secret into shares."""
        # Generate random polynomial
        coeffs = [secret] + [np.random.random() for _ in range(self.threshold - 1)]
        
        # Evaluate at different points
        shares = []
        for x in range(1, self.num_shares + 1):
            y = sum(c * (x ** i) for i, c in enumerate(coeffs))
            shares.append((x, y))
        
        return shares
    
    def reconstruct(self, shares):
        """Reconstruct secret from threshold shares."""
        secret = 0
        for i, (xi, yi) in enumerate(shares[:self.threshold]):
            # Lagrange interpolation at x=0
            numerator = 1
            denominator = 1
            for j, (xj, _) in enumerate(shares[:self.threshold]):
                if i != j:
                    numerator *= -xj
                    denominator *= (xi - xj)
            secret += yi * numerator / denominator
        
        return secret
```

-----

## Non-IID Data Challenges

### Handling Data Heterogeneity

```python
# Non-IID data handling strategies
class NonIIDStrategies:
    
    @staticmethod
    def fedavg_client_selection(clients, rounds):
        """
        Active client selection to improve convergence.
        """
        # Select clients with diverse data
        client_diversity = []
        for client in clients:
            diversity = compute_label_distribution(client.data)
            client_diversity.append((client, diversity))
        
        # Sort by diversity and select diverse subset
        sorted_clients = sorted(client_diversity, key=lambda x: x[1])
        
        # Select top-k diverse clients
        return [c[0] for c in sorted_clients[:k]]
    
    @staticmethod
    def knowledge_distillation(global_model, client_data_summary, server_data):
        """
        Knowledge distillation from server data.
        """
        # Server generates synthetic data
        synthetic_data = generate_synthetic_data(global_model, client_data_summary)
        
        # Client trains on both local and synthetic data
        for client in clients:
            combined_data = combine(client.local_data, synthetic_data)
            client.train(combined_data)
    
    @staticmethod
    def mixture_of_distributions(client_updates):
        """
        Model mixture of client distributions.
        """
        # Each client has different distribution
        mixture_weights = {}
        
        for client in clients:
            distribution = estimate_distribution(client.data)
            mixture_weights[client.id] = distribution
        
        return mixture_weights
```

### Data Partitioning Strategies

```python
# Simulating Non-IID data
def create_noniid_partitions(dataset, num_clients, alpha=0.5):
    """
    Create Non-IID partitions using Dirichlet distribution.
    
    alpha: Concentration parameter (lower = more non-IID)
    """
    from sklearn.model_selection import train_test_split
    
    partitions = []
    
    for _ in range(num_clients):
        # Sample from Dirichlet distribution
        proportions = np.random.dirichlet([alpha] * 10)  # 10 classes
        
        # Allocate data according to proportions
        client_indices = []
        for class_idx, prop in enumerate(proportions):
            class_indices = np.where(dataset.labels == class_idx)[0]
            n_samples = int(prop * len(class_indices))
            sampled = np.random.choice(class_indices, n_samples, replace=False)
            client_indices.extend(sampled)
        
        partitions.append(client_indices)
    
    return partitions
```

-----

## Communication Efficiency

### Compression Techniques

```python
# Model compression for FL
class ModelCompression:
    
    @staticmethod
    def top_k_sparsification(gradient, k_ratio=0.01):
        """Keep only top-k% largest magnitude values."""
        flat_grad = gradient.flatten()
        k = int(len(flat_grad) * k_ratio)
        
        # Get indices of top-k values
        top_k_indices = np.argpartition(np.abs(flat_grad), -k)[-k:]
        
        # Create sparse update
        sparse_grad = np.zeros_like(flat_grad)
        sparse_grad[top_k_indices] = flat_grad[top_k_indices]
        
        return sparse_grad.reshape(gradient.shape)
    
    @staticmethod
    def quantization(gradient, bits=8):
        """Quantize gradient to fewer bits."""
        # Find min/max
        g_min = gradient.min()
        g_max = gradient.max()
        
        # Create quantization levels
        levels = 2 ** bits
        step = (g_max - g_min) / levels
        
        # Quantize
        quantized = np.round((gradient - g_min) / step) * step + g_min
        
        return quantized
    
    @staticmethod
    def random_sampling(gradient, sample_ratio=0.1):
        """Randomly sample gradient elements."""
        mask = np.random.binomial(1, sample_ratio, gradient.shape)
        
        # Scale to maintain expectation
        return (gradient * mask) / sample_ratio

# SignSGD for communication efficiency
class SignSGD:
    """
    SignSGD: Only send sign of gradient updates.
    """
    def __init__(self, num_bits=1):
        self.num_bits = num_bits
    
    def compress(self, gradient):
        """Compress to sign bits."""
        return np.sign(gradient)
    
    def decompress(self, compressed):
        """Decompress (sign to magnitude)."""
        # Majority vote at server
        return compressed
```

-----

## Federated Learning Frameworks

### Popular Frameworks

| Framework | Provider | Features |
|-----------|----------|----------|
| **PySyft** | OpenMined | Privacy, differential privacy |
| **TensorFlow Federated** | Google | Production-ready |
| **FATE** | Webank | Enterprise features |
| **Flower** | Adap | Cross-device, cross-silo |
| **NVIDIA FLARE** | NVIDIA | Healthcare, finance |
| **IBM FL** | IBM | Enterprise |

### Example: Flower Framework Usage

```python
# Flower (FL) basic example
fl.server.start_server(
    server_address="localhost:8080",
    strategy=strategy.FedAvg(
        fraction_fit=0.1,  # 10% clients per round
        min_fit_clients=10,
        min_available_clients=100
    ),
    client_manager=strategy.SimpleClientManager(),
    ray_init_args={"num_cpus": 4, "num_gpus": 1}
)

# Custom FL strategy
class CustomStrategy(fl.strategy.Strategy):
    def configure_fit(self, server_round, parameters, client_manager):
        # Select clients
        sample = client_manager.sample(10)
        
        # Return config for each client
        return [
            fl.server.client_config(cid, ...) for cid in sample
        ]
    
    def aggregate_fit(self, server_round, results, failures):
        # Aggregate results
        return aggregated_parameters, {}
```

-----

## Applications of Federated Learning

| Domain | Use Case | Example |
|--------|----------|---------|
| **Healthcare** | Medical imaging, EHR | Hospital network training |
| **Finance** | Fraud detection, credit scoring | Bank consortium |
| **Mobile** | Next-word prediction, recommendations | Keyboard apps |
| **IoT** | Anomaly detection, predictive maintenance | Smart devices |
| **Edge** | Autonomous vehicles, robotics | Edge computing |

```python
# Healthcare FL example
healthcare_fl = {
    'scenario': 'Multiple hospitals training on patient data',
    'challenge': 'HIPAA compliance, data sensitivity',
    'solution': 'FL with differential privacy',
    'model': 'Medical imaging classifier',
    'aggregation': 'Secure aggregation required'
}

# Mobile keyboard FL example
mobile_fl = {
    'scenario': 'Phone keyboards learning from typing patterns',
    'challenge': 'On-device computation, privacy',
    'solution': 'Cross-device FL with local training',
    'model': 'Language model for next-word prediction',
    'updates': 'FedAvg with compression'
}
```

-----

## Common Errors to Avoid

- **Ignoring data heterogeneity**: Non-IID data causes convergence issues
- **Not handling client dropouts**: Devices may go offline
- **Forgetting privacy attacks**: Model can leak information
- **Underestimating communication costs**: Network bandwidth is limited
- **Neglecting system heterogeneity**: Devices have different capabilities
- **Using naive aggregation**: Use weighted averaging by data size
- **Not verifying privacy guarantees**: Formal DP analysis needed
- **Ignoring adversarial clients**: Malicious updates possible
- **Overfitting to local data**: Local training too long causes drift
- **Not monitoring convergence**: FL convergence differs from centralized
