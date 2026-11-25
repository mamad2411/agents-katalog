---
name: stochastic-processes
description: >
  Expert guidance on random processes, Markov chains, Brownian motion, and stochastic calculus. 
  Use for: modeling random systems, Markov chain analysis, Poisson processes, Brownian motion, 
  Ito calculus, stochastic differential equations, martingale theory, and financial mathematics.
license: MIT
compatibility: opencode
metadata:
  audience: mathematicians, data-scientists, financial-analysts
  category: mathematics
  tags: [stochastic-processes, markov-chains, brownian-motion, probability]
---

# Stochastic Processes — Theory and Applications

Covers: **Probability Foundations · Markov Chains · Poisson Processes · Brownian Motion · Stochastic Calculus · Applications**

-----

## Probability Foundations

### Probability Spaces and Random Variables

A probability space consists of three components: the sample space Omega representing all possible outcomes, a sigma-algebra F containing all measurable events, and a probability measure P assigning probabilities to events. Understanding this foundation is essential for rigorously defining stochastic processes.

A random variable is a measurable function X: Omega -> R that assigns a real number to each outcome. The distribution of X is characterized by its cumulative distribution function F(x) = P(X <= x), or by its probability density function f(x) for continuous variables.

**Key Distributions:**

| Distribution | Parameters | Mean | Variance |
|--------------|-----------|------|----------|
| Normal | mu, sigma^2 | mu | sigma^2 |
| Exponential | lambda | 1/lambda | 1/lambda^2 |
| Poisson | lambda | lambda | lambda |
| Uniform | a, b | (a+b)/2 | (b-a)^2/12 |
| Bernoulli | p | p | p(1-p) |

### Expectations and Moments

```python
import numpy as np
from scipy import stats

# Calculate expectations
def expectation(distribution, func=lambda x: x):
    """Calculate E[g(X)] for distribution"""
    if hasattr(distribution, 'expect'):
        return distribution.expect(func)
    # Monte Carlo approximation
    samples = distribution.rvs(100000)
    return np.mean(func(samples))

# Normal distribution example
normal = stats.norm(loc=5, scale=2)
E_x = normal.mean()  # 5
Var_x = normal.var()  # 4
E_x2 = normal.moment(2)  # E[X^2] = Var + E[X]^2 = 4 + 25 = 29

# Conditional expectation
# E[X|Y=y] - expectation of X given Y=y
def conditional_expectation(joint_samples, x_idx, y_idx, y_value):
    """Calculate E[X|Y=y] from samples"""
    mask = joint_samples[:, y_idx] == y_value
    return np.mean(joint_samples[mask, x_idx])

# Moment generating function
def mgf_normal(t, mu, sigma):
    """MGF of normal distribution"""
    return np.exp(mu * t + 0.5 * sigma**2 * t**2)

# Characteristic function
def cf_normal(t, mu, sigma):
    """Characteristic function of normal"""
    return np.exp(1j * mu * t - 0.5 * sigma**2 * t**2)
```

-----

## Markov Chains

### Definition and Properties

A stochastic process {X_n} is a Markov chain if it satisfies the Markov property: given the present, the future is independent of the past. Formally, P(X_{n+1} = j | X_n = i, X_{n-1} = i_{n-1}, ..., X_0 = i_0) = P(X_{n+1} = j | X_n = i).

The transition matrix P with entries P_{ij} = P(X_{n+1} = j | X_n = i) characterizes the chain. A Markov chain is homogeneous if these transition probabilities are independent of n.

**Key Properties:**

- **Irreducible** — Every state can be reached from every other state
- **Recurrent** — Expected return time to any state is finite
- **Transient** — Some states may never be revisited
- **Periodic** — Returns to states occur at regular intervals
- **Aperiodic** — No regular return pattern

### Markov Chain Implementation

```python
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
import matplotlib.pyplot as plt

@dataclass
class MarkovChain:
    """Homogeneous Markov chain"""
    states: List[str]
    transition_matrix: np.ndarray
    initial_distribution: Optional[np.ndarray] = None
    
    def __post_init__(self):
        n = len(self.states)
        if self.initial_distribution is None:
            self.initial_distribution = np.ones(n) / n
        
        # Validate
        assert np.allclose(self.transition_matrix.sum(axis=1), 1)
        assert len(self.states) == self.transition_matrix.shape[0]
    
    def simulate(self, n_steps: int, seed: int = None) -> List[str]:
        """Simulate chain for n_steps"""
        if seed is not None:
            np.random.seed(seed)
        
        path = []
        current = np.random.choice(len(self.states), p=self.initial_distribution)
        path.append(self.states[current])
        
        for _ in range(n_steps - 1):
            current = np.random.choice(
                len(self.states),
                p=self.transition_matrix[current]
            )
            path.append(self.states[current])
        
        return path
    
    def transition_prob(self, from_state: str, to_state: str, steps: int = 1) -> float:
        """Probability of transitioning from one state to another in n steps"""
        i = self.states.index(from_state)
        j = self.states.index(to_state)
        
        if steps == 1:
            return self.transition_matrix[i, j]
        
        return (self.transition_matrix ** steps)[i, j]
    
    def stationary_distribution(self) -> np.ndarray:
        """Find stationary distribution pi such that pi = pi * P"""
        eigenvalues, eigenvectors = np.linalg.eig(
            self.transition_matrix.T
        )
        
        # Find eigenvector with eigenvalue closest to 1
        idx = np.argmin(np.abs(eigenvalues - 1))
        stationary = np.real(eigenvectors[:, idx])
        return stationary / stationary.sum()
    
    def verify_ergodicity(self) -> Dict:
        """Check if chain is ergodic"""
        n = len(self.states)
        
        # Check irreducibility
        reachable = np.linalg.matrix_power(
            self.transition_matrix + np.eye(n), n - 1
        ) > 0
        irreducible = np.all(reachable)
        
        # Check aperiodicity
        eigenvalues = np.linalg.eigvals(self.transition_matrix)
        eigenvalues = np.round(eigenvalues, 10)
        eigenvalues = eigenvalues[np.abs(eigenvalues) > 0.01]
        is_aperiodic = not any(
            np.isclose(np.abs(e), 1) and 
            np.isclose(np.abs(e ** n - 1), 0)
            for n in range(2, n + 1)
            for e in eigenvalues
        )
        
        stationary = self.stationary_distribution()
        
        return {
            "irreducible": irreducible,
            "aperiodic": is_aperiodic,
            "has_stationary": True,
            "stationary_distribution": dict(zip(self.states, stationary))
        }

# Example: Weather model
weather_states = ["sunny", "cloudy", "rainy"]
weather_transitions = np.array([
    [0.7, 0.2, 0.1],  # Sunny -> sunny, cloudy, rainy
    [0.3, 0.4, 0.3],  # Cloudy -> sunny, cloudy, rainy
    [0.2, 0.3, 0.5]   # Rainy -> sunny, cloudy, rainy
])

weather_chain = MarkovChain(weather_states, weather_transitions)

# Simulate
path = weather_chain.simulate(30)
print("Weather sequence:", " -> ".join(path[:10]))

# Stationary distribution
stationary = weather_chain.stationary_distribution()
print("\nStationary distribution:")
for state, prob in zip(weather_states, stationary):
    print(f"  {state}: {prob:.3f}")

# Verify ergodicity
print("\nErgodicity:", weather_chain.verify_ergodicity())
```

### Continuous-Time Markov Chains

```python
class ContinuousTimeMarkovChain:
    """Continuous-time Markov chain with rate matrix Q"""
    
    def __init__(self, states: List[str], rate_matrix: np.ndarray):
        self.states = states
        self.rate_matrix = rate_matrix
        
        # Verify row sums to 0
        assert np.allclose(rate_matrix.sum(axis=1), 0)
        
        # Transition matrix for embedded chain
        n = len(states)
        self.embedded_matrix = np.zeros((n, n))
        for i in range(n):
            if rate_matrix[i].sum() > 0:
                self.embedded_matrix[i] = rate_matrix[i] / -rate_matrix[i, i]
    
    def simulate_jump_times(self, n_jumps: int, initial_state: int = 0, seed: int = None):
        """Simulate path with jump times"""
        if seed is not None:
            np.random.seed(seed)
        
        path = [initial_state]
        times = [0.0]
        current = initial_state
        
        for _ in range(n_jumps):
            # Time to next jump (exponential)
            rate = -self.rate_matrix[current, current]
            dt = np.random.exponential(1 / rate)
            times.append(times[-1] + dt)
            
            # Next state (embedded chain)
            current = np.random.choice(
                len(self.states),
                p=self.embedded_matrix[current]
            )
            path.append(current)
        
        return {
            "states": [self.states[s] for s in path],
            "times": times,
            "path": path
        }
```

-----

## Poisson Processes

### Definition and Properties

A Poisson process with rate lambda counts events occurring randomly in time. It satisfies: the number of events in any interval follows a Poisson distribution, events occur independently of past events, and the process has stationary increments.

The interarrival times (times between consecutive events) are independently and exponentially distributed with mean 1/lambda. This property allows simple simulation of Poisson processes.

```python
class PoissonProcess:
    """Poisson process with rate lambda"""
    
    def __init__(self, lambda_rate: float):
        self.lambda_rate = lambda_rate
    
    def simulate(self, T: float, seed: int = None) -> Dict:
        """Simulate Poisson process up to time T"""
        if seed is not None:
            np.random.seed(seed)
        
        # Generate interarrival times
        interarrivals = []
        t = 0
        while True:
            dt = np.random.exponential(1 / self.lambda_rate)
            t += dt
            if t > T:
                break
            interarrivals.append(dt)
        
        # Arrival times
        arrival_times = np.cumsum(interarrivals)
        counts = np.arange(1, len(arrival_times) + 1)
        
        return {
            "arrival_times": arrival_times,
            "counts": counts,
            "n_events": len(arrival_times)
        }
    
    def probability_k_events(self, k: int, T: float) -> float:
        """P(N(T) = k)"""
        from scipy.special import gammainc
        mu = self.lambda_rate * T
        return np.exp(-mu) * (mu ** k) / np.math.factorial(k)
    
    def arrival_time_distribution(self, n: int) -> np.ndarray:
        """Distribution of arrival times given N(T) = n"""
        # Order statistics of uniform
        return np.sort(np.random.uniform(0, 1, n))

# Compound Poisson process
class CompoundPoissonProcess:
    """Compound Poisson process: N(t) with i.i.d. jump sizes"""
    
    def __init__(self, lambda_rate: float, jump_distribution):
        self.lambda_rate = lambda_rate
        self.jump_distribution = jump_distribution
    
    def simulate(self, T: float, seed: int = None) -> Dict:
        """Simulate compound Poisson process"""
        if seed is not None:
            np.random.seed(seed)
        
        # Generate Poisson arrivals
        poisson = PoissonProcess(self.lambda_rate)
        arrivals = poisson.simulate(T)
        
        # Generate jump sizes
        n = arrivals["n_events"]
        jump_sizes = self.jump_distribution.rvs(n)
        
        # Compound process values
        values = np.cumsum(jump_sizes)
        times = arrivals["arrival_times"]
        
        return {
            "times": times,
            "values": values,
            "jump_sizes": jump_sizes,
            "final_value": values[-1] if n > 0 else 0
        }
```

-----

## Brownian Motion

### Definition and Properties

Standard Brownian motion B(t) is a stochastic process with: B(0) = 0, stationary increments, independent increments, and continuous paths almost surely. The increments B(t) - B(s) ~ N(0, t-s).

Brownian motion is a martingale, has infinite variation, is nowhere differentiable, and exhibits fractal behavior. These properties make it both mathematically interesting and practically useful for modeling random fluctuations.

```python
class BrownianMotion:
    """Standard Brownian motion"""
    
    def __init__(self, drift: float = 0, diffusion: float = 1):
        self.drift = drift
        self.diffusion = diffusion
    
    def simulate(self, T: float, n_steps: int, seed: int = None) -> Dict:
        """Simulate Brownian motion"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        t = np.linspace(0, T, n_steps + 1)
        
        # Increments
        dW = np.random.normal(0, np.sqrt(dt), n_steps)
        
        # Path
        W = np.zeros(n_steps + 1)
        W[1:] = np.cumsum(dW)
        
        # Add drift and diffusion
        if self.drift != 0 or self.diffusion != 1:
            W = self.drift * t + self.diffusion * W
        
        return {
            "time": t,
            "values": W,
            "final_value": W[-1]
        }
    
    def simulate_bridge(self, T: float, n_steps: int, start: float, end: float, seed: int = None):
        """Brownian bridge from start to end"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        t = np.linspace(0, T, n_steps + 1)
        
        # Standard Brownian bridge
        W = self.simulate(T, n_steps).values
        
        # Transform to bridge
        # B_bridge(t) = B(t) - t/T * B(T) + (t/T)*start + (1-t/T)*end
        bridge = W - t / T * W[-1]
        bridge = bridge + (t / T) * start + (1 - t / T) * end
        
        return {"time": t, "values": bridge}
    
    def hitting_time(self, a: float, max_T: float = 100) -> float:
        """First passage time to level a"""
        # For standard BM, hitting time has inverse Gaussian distribution
        if a <= 0:
            return np.inf
        
        # Monte Carlo simulation
        samples = []
        for _ in range(1000):
            path = self.simulate(max_T, 10000)
            hits = np.where(path["values"] >= a)[0]
            if len(hits) > 0:
                samples.append(path["time"][hits[0]])
        
        return np.mean(samples) if samples else np.inf

# Geometric Brownian motion
class GeometricBrownianMotion:
    """Geometric Brownian motion: S(t) = S(0) * exp((mu - sigma^2/2)t + sigma W(t))"""
    
    def __init__(self, mu: float, sigma: float):
        self.mu = mu  # drift
        self.sigma = sigma  # volatility
    
    def simulate(self, S0: float, T: float, n_steps: int, seed: int = None) -> Dict:
        """Simulate GBM path"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        t = np.linspace(0, T, n_steps + 1)
        
        # Increments
        dW = np.random.normal(0, np.sqrt(dt), n_steps)
        
        # GBM formula
        drift = (self.mu - 0.5 * self.sigma**2) * dt
        diffusion = self.sigma * dW
        
        log_returns = np.cumsum(drift + diffusion)
        prices = S0 * np.exp(log_returns)
        
        return {
            "time": t,
            "prices": prices,
            "log_returns": log_returns
        }
```

-----

## Stochastic Calculus

### Ito Integrals

The Ito integral extends the concept of integration to stochastic processes. For an Ito process dX = a(t)dt + b(t)dW, the Ito integral integral_0^t b(s)dW(s) captures the martingale part.

**Ito's Lemma:** If X is an Ito process and f is twice-differentiable, then f(X) is also an Ito process:

df(X) = f'(X)dX + (1/2)f''(X)(dX)^2

where (dt)^2 = 0, (dW)^2 = dt, and dW dt = 0.

```python
class ItoProcess:
    """Ito process dX = mu(t, X)dt + sigma(t, X)dW"""
    
    def __init__(self, mu_func, sigma_func):
        self.mu_func = mu_func  # drift function
        self.sigma_func = sigma_func  # diffusion function
    
    def simulate(self, x0: float, T: float, n_steps: int, seed: int = None) -> Dict:
        """Euler-Maruyama discretization"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        sqrt_dt = np.sqrt(dt)
        
        t = np.linspace(0, T, n_steps + 1)
        x = np.zeros(n_steps + 1)
        x[0] = x0
        
        for i in range(n_steps):
            mu = self.mu_func(t[i], x[i])
            sigma = self.sigma_func(t[i], x[i])
            
            dW = np.random.normal(0, sqrt_dt)
            x[i + 1] = x[i] + mu * dt + sigma * dW
        
        return {"time": t, "values": x}

# Example: Ornstein-Uhlenbeck process
def ou_drift(t, x):
    return -0.5 * x  # mean-reverting

def ou_diffusion(t, x):
    return 0.3  # constant volatility

ou_process = ItoProcess(ou_drift, ou_diffusion)
path = ou_process.simulate(x0=2.0, T=10, n_steps=1000)

# Verify mean reversion
print(f"Initial: {path['values'][0]:.3f}")
print(f"Final: {path['values'][-1]:.3f}")
print(f"Mean: {np.mean(path['values']):.3f}")  # Should be near 0
```

### Stochastic Differential Equations

```python
class SDESolver:
    """Solve stochastic differential equations"""
    
    @staticmethod
    def euler_maruyama(x0: float, T: float, n_steps: int, 
                      mu, sigma, seed: int = None):
        """Euler-Maruyama method"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        sqrt_dt = np.sqrt(dt)
        
        x = np.zeros(n_steps + 1)
        x[0] = x0
        
        for i in range(n_steps):
            dW = np.random.normal(0, sqrt_dt)
            x[i + 1] = x[i] + mu(x[i], i * dt) * dt + sigma(x[i], i * dt) * dW
        
        return x
    
    @staticmethod
    def milstein(x0: float, T: float, n_steps: int,
                mu, sigma, dsigma, seed: int = None):
        """Milstein method (includes second-order terms)"""
        if seed is not None:
            np.random.seed(seed)
        
        dt = T / n_steps
        sqrt_dt = np.sqrt(dt)
        
        x = np.zeros(n_steps + 1)
        x[0] = x0
        
        for i in range(n_steps):
            dW = np.random.normal(0, sqrt_dt)
            xi = x[i]
            t = i * dt
            
            # Milstein correction
            correction = 0.5 * sigma(xi, t) * dsigma(xi, t) * ((dW**2) - dt)
            
            x[i + 1] = xi + mu(xi, t) * dt + sigma(xi, t) * dW + correction
        
        return x

# Black-Scholes SDE: dS = mu*S dt + sigma*S dW
def bs_drift(S, t):
    return 0.05 * S  # mu = 5%

def bs_diffusion(S, t):
    return 0.2 * S  # sigma = 20%

def bs_dsigma(S):
    return 0.2  # derivative of sigma*S wrt S

# Simulate stock price
sde = SDESolver()
S0 = 100
prices = sde.euler_maruyama(S0, 1, 252, bs_drift, bs_diffusion)
print(f"Initial: ${S0:.2f}, Final: ${prices[-1]:.2f}")
```

-----

## Martingales

### Definition and Properties

A stochastic process M(t) is a martingale with respect to filtration F_t if: E|M(t)| < infinity for all t, M(t) is adapted to F_t, and E[M(t) | F_s] = M(s) for all s < t.

Martingales generalize the notion of fair games. They have many useful properties: they oscillate around their starting value, they have constant expectation, and various convergence theorems apply.

```python
class MartingaleTest:
    """Test if a process is a martingale"""
    
    @staticmethod
    def check_martingale(samples: np.ndarray, dt: float) -> Dict:
        """Check martingale properties empirically"""
        n_steps = samples.shape[1]
        
        # Check expectation is constant
        means = np.mean(samples, axis=0)
        mean_changes = np.diff(means)
        
        # Check increments are uncorrelated with past
        correlations = []
        for lag in range(1, 5):
            corr = np.corrcoef(
                samples[:, lag:],
                samples[:, :-lag]
            )[0, 1]
            correlations.append(corr)
        
        return {
            "means": means,
            "mean_drift": np.mean(mean_changes),
            "increments_correlations": correlations,
            "is_martingale": all(abs(c) < 0.1 for c in correlations)
        }

# Example: Brownian motion is a martingale
bm = BrownianMotion()
samples = np.array([bm.simulate(1, 1000).values for _ in range(100)])
result = MartingaleTest.check_martingale(samples, 0.001)
print(f"Brownian motion is martingale: {result['is_martingale']}")
```

-----

## Applications

### Financial Mathematics

```python
class BlackScholes:
    """Black-Scholes option pricing"""
    
    @staticmethod
    def call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Black-Scholes call price"""
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    @staticmethod
    def put_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Black-Scholes put price"""
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    @staticmethod
    def greeks(S: float, K: float, T: float, r: float, sigma: float) -> Dict:
        """Calculate Greeks"""
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        return {
            "delta": norm.cdf(d1),
            "gamma": norm.pdf(d1) / (S * sigma * np.sqrt(T)),
            "vega": S * norm.pdf(d1) * np.sqrt(T) / 100,
            "theta": (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                     - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365,
            "rho": K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        }

# Example
bs = BlackScholes()
call = bs.call_price(100, 100, 1, 0.05, 0.2)
greeks = bs.greeks(100, 100, 1, 0.05, 0.2)
print(f"Call price: ${call:.2f}")
print(f"Delta: {greeks['delta']:.3f}, Gamma: {greeks['gamma']:.4f}")
```

-----

## Best Practices

1. **Start with foundations** — Master probability theory before stochastic processes.

2. **Simulate extensively** — Use simulation to build intuition about process behavior.

3. **Verify assumptions** — Check Markov property, stationarity, and other assumptions.

4. **Use appropriate discretizations** — Choose step sizes carefully for numerical methods.

5. **Consider numerical stability** — Implement variance reduction when possible.

6. **Understand limitations** — Know when models break down and why.
