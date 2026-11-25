-----
name: modeling-science
description: >
  Expert in scientific modeling, simulation, and computational methods. Use this 
  skill for building mathematical models, running simulations, validating results, 
  creating visualizations, and applying numerical methods. Covers physics simulations, 
  mathematical modeling, computational biology, climate models, and Monte Carlo methods.
license: MIT
compatibility: opencode
metadata:
  audience: data-science
  category: data-science
  tags: [modeling, simulation, scientific-computing, numerical-methods]

# Scientific Modeling and Simulation

Covers: **Mathematical Models · Simulation Techniques · Validation · Visualization · Numerical Methods · Monte Carlo · Agent-Based Models**

-----

## Modeling Fundamentals

### What is a Scientific Model

A scientific model is a simplified representation of a system that captures essential features while ignoring irrelevant details. Models allow prediction, explanation, and understanding of complex phenomena.

### Model Classification

| Type | Description | Examples |
|------|-------------|----------|
| **Physical** | Physical replicas | Wind tunnels, prototypes |
| **Mathematical** | Equations describing behavior | Differential equations |
| **Computational** | Numerical simulations | Climate models, molecular dynamics |
| **Conceptual** | Abstract representations | Flowcharts, diagrams |
| **Empirical** | Data-driven, no theory | Regression models |

### The Modeling Process

```
┌─────────────────────────────────────────────────────────────┐
│  1. Define Problem    → What question to answer?           │
│  2. Make Assumptions → What factors matter?               │
│  3. Develop Model    → Mathematical/ computational form    │
│  4. Analyze          → Solve equations, run simulations    │
│  5. Validate         → Compare to real data               │
│  6. Use Model        → Make predictions, gain insights     │
│  7. Refine           → Iterate based on validation         │
└─────────────────────────────────────────────────────────────┘
```

-----

## Mathematical Modeling

### Deterministic Models

```python
import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import minimize, curve_fit

class ExponentialDecayModel:
    """Model: N(t) = N0 * e^(-λt)"""
    
    def __init__(self, N0: float = None, lambda_decay: float = None):
        self.N0 = N0
        self.lambda_decay = lambda_decay
    
    def fit(self, t_data: np.ndarray, y_data: np.ndarray):
        """Fit model to observed data"""
        def residuals(params):
            N0, lam = params
            y_pred = N0 * np.exp(-lam * t_data)
            return np.sum((y_data - y_pred) ** 2)
        
        # Initial guess
        x0 = [y_data[0], 0.1]
        result = minimize(residuals, x0, method='Nelder-Mead')
        self.N0, self.lambda_decay = result.x
        return self
    
    def predict(self, t: np.ndarray) -> np.ndarray:
        return self.N0 * np.exp(-self.lambda_decay * t)
    
    def half_life(self) -> float:
        return np.log(2) / self.lambda_decay


class LogisticGrowthModel:
    """Model: dN/dt = rN(1 - N/K)"""
    
    def __init__(self, r: float = None, K: float = None, N0: float = None):
        self.r = r  # Growth rate
        self.K = K  # Carrying capacity
        self.N0 = N0  # Initial population
    
    def derivative(self, t, N):
        return self.r * N * (1 - N / self.K)
    
    def solve(self, t_span: tuple, steps: int = 100):
        t = np.linspace(t_span[0], t_span[1], steps)
        solution = odeint(self.derivative, self.N0, t)
        return t, solution.flatten()
    
    def fit(self, t_data: np.ndarray, y_data: np.ndarray):
        def residuals(params):
            r, K, N0 = params
            try:
                t, y_pred = self._solve_internal(t_data, r, K, N0)
                return np.sum((y_data - y_pred) ** 2)
            except:
                return 1e10
        
        x0 = [0.1, max(y_data) * 1.5, y_data[0]]
        result = minimize(residuals, x0, method='Nelder-Mead')
        self.r, self.K, self.N0 = result.x
        return self
    
    def _solve_internal(self, t, r, K, N0):
        self.r, self.K, self.N0 = r, K, N0
        return self.solve((t[0], t[-1]), len(t))
```

### Differential Equation Models

```python
class PredatorPreyModel:
    """Lotka-Volterra predator-prey model"""
    
    def __init__(self, alpha: float = 1.1, beta: float = 0.4, 
                 delta: float = 0.1, gamma: float = 0.4):
        self.alpha = alpha  # Prey birth rate
        self.beta = beta   # Predation rate
        self.delta = delta  # Predator reproduction
        self.gamma = gamma  # Predator death rate
    
    def equations(self, t, y):
        """dy/dt = f(t, y)"""
        prey, predator = y
        dprey_dt = self.alpha * prey - self.beta * prey * predator
        dpredator_dt = self.delta * prey * predator - self.gamma * predator
        return [dprey_dt, dpredator_dt]
    
    def simulate(self, y0: list, t_span: tuple, steps: int = 1000):
        t = np.linspace(t_span[0], t_span[1], steps)
        solution = odeint(self.equations, y0, t)
        return t, solution[:, 0], solution[:, 1]


class SIRModel:
    """Epidemiological SIR model"""
    
    def __init__(self, beta: float, gamma: float):
        self.beta = beta  # Infection rate
        self.gamma = gamma  # Recovery rate
    
    def equations(self, t, y, N):
        S, I, R = y
        dSdt = -self.beta * S * I / N
        dIdt = self.beta * S * I / N - self.gamma * I
        dRdt = self.gamma * I
        return [dSdt, dIdt, dRdt]
    
    def simulate(self, N: int, I0: int, t_span: tuple, steps: int = 100):
        S0 = N - I0
        R0 = 0
        y0 = [S0, I0, R0]
        
        t = np.linspace(t_span[0], t_span[1], steps)
        solution = odeint(self.equations, y0, t, args=(N,))
        
        return {
            't': t,
            'S': solution[:, 0],
            'I': solution[:, 1],
            'R': solution[:, 2]
        }
    
    def R0_effective(self) -> float:
        """Basic reproduction number"""
        return self.beta / self.gamma
```

### Statistical Models

```python
from scipy import stats
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures

class LinearRegressionModel:
    """Multiple linear regression: y = Xβ + ε"""
    
    def __init__(self, regularization: str = None, alpha: float = 1.0):
        self.regularization = regularization
        self.alpha = alpha
        self.model = None
        self.coefficients = None
        self.intercept = None
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        X = np.array(X)
        y = np.array(y)
        
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        
        if self.regularization == 'ridge':
            self.model = Ridge(alpha=self.alpha)
        elif self.regularization == 'lasso':
            self.model = Lasso(alpha=self.alpha)
        else:
            self.model = LinearRegression()
        
        self.model.fit(X, y)
        self.coefficients = self.model.coef_
        self.intercept = self.model.intercept_
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        X = np.array(X)
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        return self.model.predict(X)
    
    def r_squared(self, X: np.ndarray, y: np.ndarray) -> float:
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)


class PolynomialRegression:
    """Polynomial regression for non-linear relationships"""
    
    def __init__(self, degree: int = 2):
        self.degree = degree
        self.poly = PolynomialFeatures(degree=degree)
        self.model = LinearRegression()
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        X_poly = self.poly.fit_transform(X.reshape(-1, 1))
        self.model.fit(X_poly, y)
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        X_poly = self.poly.transform(X.reshape(-1, 1))
        return self.model.predict(X_poly)
    
    def coefficients(self) -> dict:
        return {
            'intercept': self.model.intercept_,
            'coefficients': self.model.coef_
        }
```

-----

## Simulation Methods

### Monte Carlo Simulation

```python
import random
from typing import Callable, List, Tuple

class MonteCarloSimulation:
    """Monte Carlo simulation framework"""
    
    def __init__(self, n_simulations: int = 10000):
        self.n_simulations = n_simulations
        self.results: List[float] = []
    
    def run(self, model_fn: Callable, *args, **kwargs) -> List[float]:
        """Run simulation multiple times"""
        self.results = [model_fn(*args, **kwargs) for _ in range(self.n_simulations)]
        return self.results
    
    def mean(self) -> float:
        return np.mean(self.results)
    
    def std(self) -> float:
        return np.std(self.results)
    
    def confidence_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval"""
        alpha = 1 - confidence
        lower = np.percentile(self.results, alpha/2 * 100)
        upper = np.percentile(self.results, (1 - alpha/2) * 100)
        return lower, upper
    
    def histogram(self, bins: int = 50):
        return np.histogram(self.results, bins=bins)


class PiEstimator:
    """Estimate π using Monte Carlo"""
    
    @staticmethod
    def estimate(n_points: int = 1000000) -> float:
        """Estimate π by throwing random points in unit square"""
        x = np.random.rand(n_points)
        y = np.random.rand(n_points)
        
        # Points inside unit circle
        inside = x**2 + y**2 <= 1
        pi_estimate = 4 * np.sum(inside) / n_points
        
        return pi_estimate
    
    @staticmethod
    def estimate_dart_throwing(n_darts: int = 10000) -> float:
        """Simulate throwing darts at a circular target"""
        hits = 0
        for _ in range(n_darts):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x**2 + y**2 <= 1:
                hits += 1
        return 4 * hits / n_darts


class OptionPricing:
    """Black-Scholes option pricing via Monte Carlo"""
    
    @staticmethod
    def simulate_price(S0: float, r: float, sigma: float, 
                      T: float, n_steps: int) -> float:
        """Geometric Brownian Motion price simulation"""
        dt = T / n_steps
        price = S0
        
        for _ in range(n_steps):
            z = np.random.standard_normal()
            price *= np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        
        return price
    
    @staticmethod
    def call_option_price(S0: float, K: float, r: float, 
                         sigma: float, T: float, n_sims: int = 10000) -> float:
        """Monte Carlo estimate of European call option"""
        payoffs = []
        
        for _ in range(n_sims):
            final_price = OptionPricing.simulate_price(S0, r, sigma, T, 100)
            payoff = max(0, final_price - K)
            payoffs.append(payoff)
        
        # Discounted expected payoff
        return np.exp(-r * T) * np.mean(payoffs)
```

### Agent-Based Modeling

```python
from typing import List, Tuple
from enum import Enum
import random

class Agent:
    """Base class for agents in simulation"""
    
    def __init__(self, agent_id: int, position: Tuple[float, float]):
        self.id = agent_id
        self.position = position
        self.state = "active"
    
    def move(self, new_position: Tuple[float, float]):
        self.position = new_position
    
    def step(self, environment: 'Environment'):
        """Override for agent-specific behavior"""
        pass


class InfectionState(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"


class DiseaseAgent(Agent):
    """Agent for epidemiological simulation"""
    
    def __init__(self, agent_id: int, position: Tuple[float, float]):
        super().__init__(agent_id, position)
        self.infection_state = InfectionState.SUSCEPTIBLE
        self.time_infected = 0
        self.infection_duration = 14  # days
        self.infection_radius = 1.0
        self.infection_probability = 0.3
    
    def infect(self):
        self.infection_state = InfectionState.INFECTED
        self.time_infected = 0
    
    def step(self, environment: 'Environment'):
        if self.infection_state == InfectionState.INFECTED:
            self.time_infected += 1
            
            if self.time_infected >= self.infection_duration:
                self.infection_state = InfectionState.RECOVERED
        
        # Random movement
        dx = random.uniform(-0.1, 0.1)
        dy = random.uniform(-0.1, 0.1)
        new_pos = (self.position[0] + dx, self.position[1] + dy)
        self.move(new_pos)
        
        # Check for infections
        if self.infection_state == InfectionState.INFECTED:
            self._try_infect_others(environment)
    
    def _try_infect_others(self, environment: 'Environment'):
        for other in environment.agents:
            if (other.id != self.id and 
                other.infection_state == InfectionState.SUSCEPTIBLE):
                dist = np.sqrt((self.position[0] - other.position[0])**2 + 
                              (self.position[1] - other.position[1])**2)
                if dist < self.infection_radius:
                    if random.random() < self.infection_probability:
                        other.infect()


class Environment:
    """Simulation environment for agents"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.agents: List[DiseaseAgent] = []
    
    def add_agent(self, agent: DiseaseAgent):
        self.agents.append(agent)
    
    def step(self):
        """Advance simulation by one time step"""
        for agent in self.agents:
            agent.step(self)
    
    def get_stats(self) -> dict:
        states = [a.infection_state for a in self.agents]
        return {
            'susceptible': states.count(InfectionState.SUSCEPTIBLE),
            'infected': states.count(InfectionState.INFECTED),
            'recovered': states.count(InfectionState.RECOVERED),
            'total': len(self.agents)
        }


class SimulationRunner:
    """Run agent-based simulations"""
    
    def __init__(self, environment: Environment):
        self.environment = environment
        self.history: List[dict] = []
    
    def run(self, n_steps: int, record_every: int = 1):
        for step in range(n_steps):
            self.environment.step()
            
            if step % record_every == 0:
                stats = self.environment.get_stats()
                stats['step'] = step
                self.history.append(stats)
        
        return self.history
```

-----

## Numerical Methods

### Numerical Integration

```python
class NumericalIntegration:
    """Numerical integration methods"""
    
    @staticmethod
    def trapezoidal(f: Callable, a: float, b: float, n: int = 1000) -> float:
        """Trapezoidal rule"""
        h = (b - a) / n
        result = 0.5 * (f(a) + f(b))
        
        for i in range(1, n):
            result += f(a + i * h)
        
        return result * h
    
    @staticmethod
    def simpson(f: Callable, a: float, b: float, n: int = 1000) -> float:
        """Simpson's 1/3 rule (n must be even)"""
        if n % 2 == 1:
            n += 1
        
        h = (b - a) / n
        result = f(a) + f(b)
        
        for i in range(1, n):
            x = a + i * h
            if i % 2 == 0:
                result += 2 * f(x)
            else:
                result += 4 * f(x)
        
        return result * h / 3
    
    @staticmethod
    def monte_carlo_integration(f: Callable, a: float, b: float, 
                                n_points: int = 10000) -> float:
        """Monte Carlo integration"""
        x = np.random.uniform(a, b, n_points)
        y = f(x)
        
        # Box method
        f_max = np.max(y)
        f_min = np.min(y)
        
        area = (b - a) * (f_max - f_min)
        under_curve = np.sum(y > 0) / n_points
        
        return area * under_curve


class RootFinding:
    """Root finding methods"""
    
    @staticmethod
    def bisection(f: Callable, a: float, b: float, tol: float = 1e-6) -> float:
        """Bisection method"""
        if f(a) * f(b) > 0:
            raise ValueError("Function must have opposite signs at endpoints")
        
        while (b - a) / 2 > tol:
            c = (a + b) / 2
            if f(c) == 0:
                return c
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
        
        return (a + b) / 2
    
    @staticmethod
    def newton(f: Callable, df: Callable, x0: float, 
               tol: float = 1e-6, max_iter: int = 100) -> float:
        """Newton-Raphson method"""
        x = x0
        
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x
            
            dfx = df(x)
            if abs(dfx) < 1e-10:
                raise ValueError("Derivative too small")
            
            x = x - fx / dfx
        
        return x
    
    @staticmethod
    def secant(f: Callable, x0: float, x1: float, 
               tol: float = 1e-6, max_iter: int = 100) -> float:
        """Secant method"""
        for _ in range(max_iter):
            fx0, fx1 = f(x0), f(x1)
            
            if abs(fx1) < tol:
                return x1
            
            if abs(fx1 - fx0) < 1e-10:
                raise ValueError("Division by zero")
            
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            x0, x1 = x1, x2
        
        return x1
```

-----

## Model Validation

### Cross-Validation

```python
from sklearn.model_selection import KFold, LeaveOneOut, cross_val_score

class ModelValidator:
    """Model validation techniques"""
    
    @staticmethod
    def k_fold_cv(model, X: np.ndarray, y: np.ndarray, k: int = 5) -> dict:
        """K-fold cross-validation"""
        kf = KFold(n_splits=k, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
        
        return {
            'scores': scores,
            'mean': np.mean(scores),
            'std': np.std(scores),
            'k': k
        }
    
    @staticmethod
    def leave_one_out_cv(model, X: np.ndarray, y: np.ndarray) -> dict:
        """Leave-one-out cross-validation"""
        loo = LeaveOneOut()
        scores = cross_val_score(model, X, y, cv=loo, scoring='r2')
        
        return {
            'scores': scores,
            'mean': np.mean(scores),
            'n_samples': len(scores)
        }
    
    @staticmethod
    def train_test_split_data(X: np.ndarray, y: np.ndarray, 
                              test_size: float = 0.2) -> tuple:
        """Simple train-test split"""
        n = len(y)
        n_test = int(n * test_size)
        indices = np.random.permutation(n)
        
        test_indices = indices[:n_test]
        train_indices = indices[n_test:]
        
        return (X[train_indices], X[test_indices],
                y[train_indices], y[test_indices])
```

### Residual Analysis

```python
class ResidualAnalysis:
    """Analyze model residuals"""
    
    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray):
        self.residuals = y_true - y_pred
        self.y_true = y_true
        self.y_pred = y_pred
    
    def mean_residual(self) -> float:
        return np.mean(self.residuals)
    
    def rmse(self) -> float:
        return np.sqrt(np.mean(self.residuals ** 2))
    
    def mae(self) -> float:
        return np.mean(np.abs(self.residuals))
    
    def r_squared(self) -> float:
        ss_res = np.sum(self.residuals ** 2)
        ss_tot = np.sum((self.y_true - np.mean(self.y_true)) ** 2)
        return 1 - (ss_res / ss_tot)
    
    def normal_distribution_test(self) -> dict:
        """Shapiro-Wilk test for normality"""
        stat, p_value = stats.shapiro(self.residuals)
        return {'statistic': stat, 'p_value': p_value, 
                'normal': p_value > 0.05}
    
    def heteroscedasticity_test(self) -> dict:
        """Breusch-Pagan test"""
        # Simplified version
        squared_resid = self.residuals ** 2
        correlation = np.corrcoef(np.abs(self.y_pred), squared_resid)[0, 1]
        return {'correlation': correlation}
```

-----

## Visualization

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ModelVisualizer:
    """Visualization tools for models"""
    
    @staticmethod
    def plot_fit(X: np.ndarray, y_true: np.ndarray, 
                y_pred: np.ndarray, title: str = "Model Fit"):
        """Plot model predictions vs actual data"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scatter plot
        ax1.scatter(y_true, y_pred, alpha=0.5)
        ax1.plot([y_true.min(), y_true.max()], 
                [y_true.min(), y_true.max()], 'r--', lw=2)
        ax1.set_xlabel('Actual')
        ax1.set_ylabel('Predicted')
        ax1.set_title('Actual vs Predicted')
        
        # Residual plot
        residuals = y_true - y_pred
        ax2.scatter(y_pred, residuals, alpha=0.5)
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Residuals')
        ax2.set_title('Residual Plot')
        
        plt.suptitle(title)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_time_series(t: np.ndarray, y: np.ndarray, 
                        y_pred: np.ndarray = None, 
                        ci_lower: np.ndarray = None,
                        ci_upper: np.ndarray = None):
        """Plot time series with predictions and confidence intervals"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(t, y, 'b-', label='Observed', linewidth=1.5)
        
        if y_pred is not None:
            ax.plot(t, y_pred, 'r--', label='Model', linewidth=1.5)
        
        if ci_lower is not None and ci_upper is not None:
            ax.fill_between(t, ci_lower, ci_upper, 
                           color='red', alpha=0.2, label='95% CI')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_phase_space(x: np.ndarray, y: np.ndarray, 
                        color: np.ndarray = None):
        """Plot phase space diagram"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        sc = ax.scatter(x, y, c=color, cmap='viridis', s=1)
        
        if color is not None:
            plt.colorbar(sc, ax=ax, label='Time')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Phase Space')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
```
