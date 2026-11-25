---
name: stochastic-inventory-models
description: When the user wants to model inventory systems with uncertain demand, optimize safety stock levels, implement (s,S) or (Q,r) policies, or analyze service levels under uncertainty. Also use when the user mentions "stochastic inventory," "probabilistic inventory," "(Q,r) policy," "(s,S) policy," "base stock policy," "safety stock optimization," "service level constraints," "lead time demand distribution," "fill rate calculation," or "inventory with demand uncertainty." For deterministic models, see economic-order-quantity or lot-sizing-problems. For single-period uncertainty, see newsvendor-problem.
---

# Stochastic Inventory Models

You are an expert in stochastic inventory theory and probabilistic inventory optimization. Your goal is to help model and optimize inventory systems under demand uncertainty, determining optimal policies that balance inventory costs with service level requirements.

## Initial Assessment

Before modeling stochastic inventory, understand:

1. **Demand Uncertainty**
   - Demand distribution? (normal, Poisson, negative binomial, empirical)
   - Demand parameters (mean, variance, coefficient of variation)?
   - Time period for demand (daily, weekly)?
   - Intermittent or smooth demand pattern?
   - Historical data available?

2. **Lead Time**
   - Lead time from order to receipt?
   - Lead time variability?
   - Lead time distribution?
   - Correlation between demand and lead time?

3. **Inventory Policy Type**
   - Continuous vs. periodic review?
   - (Q,r) continuous review policy?
   - (R,S) periodic review policy?
   - (s,S) policy with bandwidth?
   - Base stock policy?

4. **Service Level Requirements**
   - Target service level? (Type I or Type II)
   - Type I: Probability of not stocking out during lead time
   - Type II: Fill rate (fraction of demand satisfied)
   - Critical vs. non-critical items?

5. **Cost Structure**
   - Fixed ordering cost?
   - Holding cost per unit per period?
   - Backorder cost vs. lost sales?
   - Emergency replenishment options?

---

## Stochastic Inventory Fundamentals

### Key Concepts

**Demand During Lead Time (DDLT):**
- Random variable representing total demand during replenishment lead time
- Critical for determining reorder point and safety stock

**Safety Stock (SS):**
- Buffer inventory to protect against demand uncertainty
- SS = k × σ_DDLT, where k is safety factor

**Service Levels:**
- **Type I (Cycle Service Level, CSL):** P(no stockout during lead time)
- **Type II (Fill Rate, FR):** Fraction of demand met from stock

**Inventory Position:**
- On-hand + on-order - backorders
- Decision based on position, not just on-hand

---

## Python Implementation: Stochastic Models

### (Q,r) Continuous Review Policy

```python
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize_scalar, fsolve
from typing import Dict, Tuple
import matplotlib.pyplot as plt

class ContinuousReviewQrPolicy:
    """
    (Q,r) Continuous Review Inventory Policy

    - Monitor inventory continuously
    - When inventory position ≤ r, order Q units
    - Optimize Q and r to minimize costs while meeting service level
    """

    def __init__(self, demand_mean: float, demand_std: float,
                 lead_time: float, holding_cost: float,
                 ordering_cost: float, backorder_cost: float = None,
                 service_level: float = 0.95):
        """
        Parameters:
        -----------
        demand_mean : float
            Mean demand per period
        demand_std : float
            Standard deviation of demand per period
        lead_time : float
            Lead time in periods
        holding_cost : float
            Holding cost per unit per period
        ordering_cost : float
            Fixed ordering cost
        backorder_cost : float, optional
            Backorder cost per unit per period (if None, uses lost sales)
        service_level : float
            Target Type I service level (cycle service level)
        """
        self.mu = demand_mean
        self.sigma = demand_std
        self.L = lead_time
        self.h = holding_cost
        self.K = ordering_cost
        self.b = backorder_cost
        self.alpha = service_level

        # Lead time demand distribution
        self.mu_L = demand_mean * lead_time
        self.sigma_L = demand_std * np.sqrt(lead_time)

    def calculate_eoq(self) -> float:
        """Calculate basic EOQ (ignoring uncertainty)"""
        return np.sqrt(2 * self.mu * self.K / self.h)

    def calculate_reorder_point(self, Q: float, service_level: float = None) -> Dict:
        """
        Calculate reorder point for given order quantity

        Parameters:
        -----------
        Q : float
            Order quantity
        service_level : float, optional
            Target service level (uses self.alpha if None)

        Returns:
        --------
        Dictionary with reorder point, safety stock, and metrics
        """

        if service_level is None:
            service_level = self.alpha

        # Safety factor for target service level
        z = stats.norm.ppf(service_level)

        # Safety stock
        safety_stock = z * self.sigma_L

        # Reorder point
        r = self.mu_L + safety_stock

        # Expected shortage per cycle (for Type II service level)
        def G(k):
            """Unit normal loss function"""
            return stats.norm.pdf(k) - k * (1 - stats.norm.cdf(k))

        k = (r - self.mu_L) / self.sigma_L
        expected_shortage = self.sigma_L * G(k)

        # Fill rate (Type II service level)
        fill_rate = 1 - expected_shortage / Q

        return {
            'reorder_point': r,
            'safety_stock': safety_stock,
            'safety_factor': z,
            'expected_shortage_per_cycle': expected_shortage,
            'fill_rate': fill_rate,
            'cycle_service_level': service_level
        }

    def optimize_Qr_cost(self) -> Dict:
        """
        Optimize Q and r jointly to minimize expected total cost

        Uses iterative approach:
        1. Start with EOQ
        2. Calculate optimal r given Q
        3. Calculate optimal Q given r
        4. Iterate until convergence
        """

        # Initialize with EOQ and basic r
        Q = self.calculate_eoq()

        # Iterate
        for _ in range(10):
            # Calculate r given Q
            r_result = self.calculate_reorder_point(Q, self.alpha)
            r = r_result['reorder_point']

            # Calculate Q given r (considering safety stock)
            # Modified EOQ accounting for safety stock
            Q_new = np.sqrt(2 * self.mu * self.K / self.h)

            if abs(Q_new - Q) < 0.01:
                break

            Q = Q_new

        # Final calculations
        r_result = self.calculate_reorder_point(Q, self.alpha)
        r = r_result['reorder_point']
        ss = r_result['safety_stock']

        # Cost calculations
        ordering_cost_annual = (self.mu / Q) * self.K
        holding_cost_annual = (Q / 2 + ss) * self.h

        # Backorder cost (if specified)
        if self.b is not None:
            expected_shortage = r_result['expected_shortage_per_cycle']
            backorder_cost_annual = (self.mu / Q) * expected_shortage * self.b
            total_cost = ordering_cost_annual + holding_cost_annual + backorder_cost_annual
        else:
            backorder_cost_annual = 0
            total_cost = ordering_cost_annual + holding_cost_annual

        return {
            'policy': '(Q,r)',
            'order_quantity': Q,
            'reorder_point': r,
            'safety_stock': ss,
            'safety_factor': r_result['safety_factor'],
            'avg_inventory': Q / 2 + ss,
            'ordering_cost': ordering_cost_annual,
            'holding_cost': holding_cost_annual,
            'backorder_cost': backorder_cost_annual,
            'total_cost': total_cost,
            'cycle_service_level': r_result['cycle_service_level'],
            'fill_rate': r_result['fill_rate']
        }

    def simulate(self, num_periods: int, Q: float, r: float,
                seed: int = None) -> pd.DataFrame:
        """
        Simulate (Q,r) policy over time

        Parameters:
        -----------
        num_periods : int
            Number of periods to simulate
        Q : float
            Order quantity
        r : float
            Reorder point
        seed : int, optional
            Random seed for reproducibility
        """

        if seed is not None:
            np.random.seed(seed)

        # Initialize
        inventory_position = Q  # Start with one order
        inventory_on_hand = Q
        orders_outstanding = []  # List of (arrival_period, quantity)

        results = []

        for t in range(num_periods):
            # Receive orders arriving this period
            arrivals = [order for order in orders_outstanding
                       if order['arrival'] == t]
            for arrival in arrivals:
                inventory_on_hand += arrival['quantity']
                orders_outstanding.remove(arrival)

            # Generate demand
            demand = max(0, np.random.normal(self.mu, self.sigma))

            # Satisfy demand
            sales = min(demand, inventory_on_hand)
            stockout = demand - sales
            inventory_on_hand -= sales

            # Update inventory position
            inventory_position = inventory_on_hand + sum(
                o['quantity'] for o in orders_outstanding)

            # Check if order needed
            order_placed = 0
            if inventory_position <= r:
                order_placed = Q
                orders_outstanding.append({
                    'order_period': t,
                    'arrival': t + int(self.L),
                    'quantity': Q
                })
                inventory_position += Q

            results.append({
                'period': t,
                'demand': demand,
                'sales': sales,
                'stockout': stockout,
                'inventory_on_hand': inventory_on_hand,
                'inventory_position': inventory_position,
                'order_placed': order_placed,
                'orders_outstanding': len(orders_outstanding)
            })

        df = pd.DataFrame(results)

        # Calculate performance metrics
        fill_rate = df['sales'].sum() / df['demand'].sum()
        avg_inventory = df['inventory_on_hand'].mean()
        stockout_periods = (df['stockout'] > 0).sum()
        cycle_service_level = 1 - stockout_periods / num_periods

        summary = {
            'fill_rate': fill_rate,
            'cycle_service_level': cycle_service_level,
            'avg_inventory': avg_inventory,
            'total_stockouts': df['stockout'].sum(),
            'num_orders': (df['order_placed'] > 0).sum()
        }

        return df, summary

    def plot_simulation(self, simulation_df: pd.DataFrame, Q: float, r: float):
        """Visualize simulation results"""

        fig, axes = plt.subplots(3, 1, figsize=(14, 10))

        periods = simulation_df['period']

        # Plot 1: Inventory levels and reorder point
        axes[0].plot(periods, simulation_df['inventory_position'],
                    label='Inventory Position', linewidth=2, color='blue')
        axes[0].plot(periods, simulation_df['inventory_on_hand'],
                    label='On-Hand Inventory', linewidth=2, color='green', alpha=0.7)
        axes[0].axhline(y=r, color='red', linestyle='--', linewidth=2,
                       label=f'Reorder Point (r={r:.0f})')
        axes[0].fill_between(periods, 0, simulation_df['inventory_on_hand'],
                            alpha=0.2, color='green')

        # Mark order placements
        order_periods = periods[simulation_df['order_placed'] > 0]
        axes[0].scatter(order_periods,
                       simulation_df.loc[simulation_df['order_placed'] > 0,
                                        'inventory_position'],
                       color='red', s=100, marker='^', zorder=5,
                       label='Order Placed')

        axes[0].set_ylabel('Inventory Level')
        axes[0].set_title('(Q,r) Policy: Inventory Levels Over Time', fontweight='bold')
        axes[0].legend(loc='upper right')
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Demand and sales
        axes[1].plot(periods, simulation_df['demand'], label='Demand',
                    linewidth=2, color='blue', alpha=0.6)
        axes[1].plot(periods, simulation_df['sales'], label='Sales',
                    linewidth=2, color='green')
        axes[1].fill_between(periods, simulation_df['sales'],
                            simulation_df['demand'],
                            where=(simulation_df['stockout'] > 0),
                            alpha=0.3, color='red', label='Stockouts')

        axes[1].set_ylabel('Units')
        axes[1].set_title('Demand vs. Sales', fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Plot 3: Cumulative stockouts
        axes[2].plot(periods, simulation_df['stockout'].cumsum(),
                    linewidth=2, color='red')
        axes[2].set_xlabel('Period')
        axes[2].set_ylabel('Cumulative Stockout Units')
        axes[2].set_title('Cumulative Stockouts Over Time', fontweight='bold')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        return plt


# Example Usage
def example_continuous_review():
    """Example: (Q,r) continuous review policy"""

    print("\n" + "=" * 70)
    print("(Q,r) CONTINUOUS REVIEW STOCHASTIC INVENTORY MODEL")
    print("=" * 70)

    # Create model
    model = ContinuousReviewQrPolicy(
        demand_mean=100,        # Average demand: 100 units/day
        demand_std=20,          # Std dev: 20 units/day
        lead_time=7,            # Lead time: 7 days
        holding_cost=2.0,       # $2/unit/day
        ordering_cost=200,      # $200 per order
        backorder_cost=10,      # $10/unit backordered
        service_level=0.95      # 95% cycle service level
    )

    print("\nInput Parameters:")
    print(f"  Demand: Normal(μ={model.mu}, σ={model.sigma}) per day")
    print(f"  Lead Time: {model.L} days")
    print(f"  Lead Time Demand: Normal(μ={model.mu_L:.0f}, σ={model.sigma_L:.1f})")
    print(f"  Holding Cost: ${model.h}/unit/day")
    print(f"  Ordering Cost: ${model.K}")
    print(f"  Backorder Cost: ${model.b}/unit/day")
    print(f"  Target Service Level: {model.alpha:.1%}")

    # Optimize policy
    optimal = model.optimize_Qr_cost()

    print(f"\n{'=' * 70}")
    print("OPTIMAL (Q,r) POLICY")
    print("=" * 70)

    print(f"\n{'Order Quantity (Q):':<35} {optimal['order_quantity']:.0f} units")
    print(f"{'Reorder Point (r):':<35} {optimal['reorder_point']:.0f} units")
    print(f"{'Safety Stock:':<35} {optimal['safety_stock']:.0f} units")
    print(f"{'Safety Factor (z):':<35} {optimal['safety_factor']:.2f}")
    print(f"{'Average Inventory:':<35} {optimal['avg_inventory']:.0f} units")

    print(f"\n{'Performance Metrics:':<35}")
    print(f"  {'Cycle Service Level:':<33} {optimal['cycle_service_level']:.1%}")
    print(f"  {'Fill Rate:':<33} {optimal['fill_rate']:.2%}")

    print(f"\n{'Annual Costs:':<35}")
    print(f"  {'Ordering Cost:':<33} ${optimal['ordering_cost']:,.2f}")
    print(f"  {'Holding Cost:':<33} ${optimal['holding_cost']:,.2f}")
    print(f"  {'Backorder Cost:':<33} ${optimal['backorder_cost']:,.2f}")
    print(f"  {'-'*50}")
    print(f"  {'Total Annual Cost:':<33} ${optimal['total_cost']:,.2f}")

    # Simulate
    print("\n\nSimulating policy for 365 days...")
    simulation, summary = model.simulate(
        num_periods=365,
        Q=optimal['order_quantity'],
        r=optimal['reorder_point'],
        seed=42
    )

    print(f"\n{'Simulation Results (365 days):':<35}")
    print(f"  {'Fill Rate (actual):':<33} {summary['fill_rate']:.2%}")
    print(f"  {'Cycle Service Level (actual):':<33} {summary['cycle_service_level']:.1%}")
    print(f"  {'Average Inventory:':<33} {summary['avg_inventory']:.0f} units")
    print(f"  {'Total Stockout Units:':<33} {summary['total_stockouts']:.0f}")
    print(f"  {'Number of Orders:':<33} {summary['num_orders']}")

    # Plot
    model.plot_simulation(simulation, optimal['order_quantity'],
                         optimal['reorder_point'])
    plt.savefig('/tmp/qr_policy_simulation.png', dpi=300, bbox_inches='tight')
    print(f"\nSimulation plot saved to /tmp/qr_policy_simulation.png")

    return model, optimal, simulation


if __name__ == "__main__":
    example_continuous_review()
```

---

## Periodic Review (R,S) Policy

```python
class PeriodicReviewRSPolicy:
    """
    (R,S) Periodic Review Policy

    - Review inventory every R periods
    - Order up to level S (order-up-to level)
    - Must cover demand during R + L periods
    """

    def __init__(self, demand_mean: float, demand_std: float,
                 lead_time: float, review_period: float,
                 holding_cost: float, ordering_cost: float,
                 service_level: float = 0.95):
        """
        Parameters:
        -----------
        demand_mean : float
            Mean demand per period
        demand_std : float
            Std dev of demand per period
        lead_time : float
            Lead time in periods
        review_period : float
            Time between reviews (R)
        holding_cost : float
            Holding cost per unit per period
        ordering_cost : float
            Fixed ordering cost per order
        service_level : float
            Target Type I service level
        """
        self.mu = demand_mean
        self.sigma = demand_std
        self.L = lead_time
        self.R = review_period
        self.h = holding_cost
        self.K = ordering_cost
        self.alpha = service_level

        # Protection period = R + L
        self.T = review_period + lead_time

        # Demand distribution during protection period
        self.mu_T = demand_mean * self.T
        self.sigma_T = demand_std * np.sqrt(self.T)

    def calculate_order_up_to_level(self) -> Dict:
        """
        Calculate order-up-to level S

        S = E[Demand during R+L] + Safety Stock
        """

        # Safety factor
        z = stats.norm.ppf(self.alpha)

        # Safety stock
        safety_stock = z * self.sigma_T

        # Order-up-to level
        S = self.mu_T + safety_stock

        # Average inventory (approximation)
        # On average, order R*mu units every R periods
        avg_order = self.R * self.mu
        avg_inventory = avg_order / 2 + safety_stock

        # Costs
        orders_per_year = 1 / self.R  # If period = year/365
        ordering_cost_annual = orders_per_year * self.K
        holding_cost_annual = avg_inventory * self.h * self.R
        total_cost = ordering_cost_annual + holding_cost_annual

        return {
            'policy': '(R,S)',
            'review_period': self.R,
            'order_up_to_level': S,
            'safety_stock': safety_stock,
            'safety_factor': z,
            'avg_inventory': avg_inventory,
            'ordering_cost': ordering_cost_annual,
            'holding_cost': holding_cost_annual,
            'total_cost': total_cost,
            'service_level': self.alpha
        }


# Example: Periodic Review
def example_periodic_review():
    """Example: (R,S) periodic review policy"""

    print("\n" + "=" * 70)
    print("(R,S) PERIODIC REVIEW STOCHASTIC INVENTORY MODEL")
    print("=" * 70)

    model = PeriodicReviewRSPolicy(
        demand_mean=50,         # 50 units/day
        demand_std=10,          # Std dev 10
        lead_time=5,            # 5 days lead time
        review_period=7,        # Review weekly
        holding_cost=1.5,       # $1.50/unit/day
        ordering_cost=150,      # $150 per order
        service_level=0.98      # 98% service level
    )

    print("\nInput Parameters:")
    print(f"  Review Period (R): {model.R} days")
    print(f"  Lead Time (L): {model.L} days")
    print(f"  Protection Period (R+L): {model.T} days")
    print(f"  Demand per Day: Normal(μ={model.mu}, σ={model.sigma})")
    print(f"  Demand during Protection: Normal(μ={model.mu_T:.0f}, σ={model.sigma_T:.1f})")

    result = model.calculate_order_up_to_level()

    print(f"\n{'=' * 70}")
    print("OPTIMAL (R,S) POLICY")
    print("=" * 70)

    print(f"\n{'Review Period (R):':<35} {result['review_period']:.0f} days")
    print(f"{'Order-Up-To Level (S):':<35} {result['order_up_to_level']:.0f} units")
    print(f"{'Safety Stock:':<35} {result['safety_stock']:.0f} units")
    print(f"{'Safety Factor:':<35} {result['safety_factor']:.2f}")
    print(f"{'Target Service Level:':<35} {result['service_level']:.1%}")

    print(f"\n{'Policy:':<35} Review inventory every {result['review_period']:.0f} days")
    print(f"{'      ':<35} Order up to {result['order_up_to_level']:.0f} units")

    return model, result


if __name__ == "__main__":
    example_periodic_review()
```

---

## Tools & Libraries

### Python Libraries
- `scipy.stats`: Probability distributions
- `numpy`, `pandas`: Numerical and data operations
- Custom implementations for policy optimization

### Commercial Software
- **Blue Yonder**: Advanced stochastic inventory optimization
- **ToolsGroup**: Probabilistic demand forecasting and inventory
- **Logility**: Inventory optimization with uncertainty
- **SAP IBP**: Stochastic planning capabilities
- **o9 Solutions**: Probabilistic inventory planning

---

## Common Challenges & Solutions

### Challenge: Intermittent Demand
**Problem:** Many zeros, high variability
**Solutions:**
- Use specialized distributions (Croston's method, Poisson, negative binomial)
- Higher safety stocks
- Consider make-to-order

### Challenge: Lead Time Variability
**Problem:** Supplier lead times uncertain
**Solutions:**
- Model lead time as random variable
- Combined uncertainty formula: σ²_DDLT = L·σ²_D + μ²_D·σ²_L
- Safety lead time approach

### Challenge: Service Level Selection
**Problem:** Difficult to specify target
**Solutions:**
- Use cost-based optimization (balance holding vs. stockout)
- ABC classification with differentiated service
- Empirically validate with business

### Challenge: Demand Distribution Selection
**Problem:** Don't know appropriate distribution
**Solutions:**
- Use empirical bootstrap methods
- Fit and test multiple distributions (normal, lognormal, gamma)
- Normal often works well for aggregate demand

---

## Related Skills

- **inventory-optimization**: General inventory management
- **economic-order-quantity**: Deterministic models
- **newsvendor-problem**: Single-period stochastic
- **multi-echelon-inventory**: Network-wide stochastic models
- **demand-forecasting**: Demand distribution estimation
- **safety-stock**: Safety stock calculation methods
