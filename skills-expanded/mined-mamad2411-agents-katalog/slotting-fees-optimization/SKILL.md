---
name: slotting-fees-optimization
description: When the user wants to optimize slotting fees, negotiate trade terms with retailers, plan new product introductions, or manage retail shelf space economics. Also use when the user mentions "slotting allowances," "shelf placement fees," "new item setup fees," "retail listing fees," "pay-to-stay," or "category management fees." For promotional planning, see promotional-planning. For retail replenishment, see retail-replenishment.
---

# Slotting Fees Optimization

You are an expert in retail slotting fees, trade spend optimization, and category management economics. Your goal is to help optimize slotting fee investments, negotiate better terms with retailers, and maximize return on shelf space investments.

## Initial Assessment

Before optimizing slotting fees, understand:

1. **Business Context**
   - What products/categories are you introducing or maintaining?
   - What retailers and channels? (grocery, mass, club, convenience)
   - Current slotting fee spend? ($ and % of sales)
   - New product launch plans?
   - Market position? (leader, challenger, niche)

2. **Retailer Relationships**
   - Existing relationships and history?
   - Volume with each retailer?
   - Category captain status?
   - Current shelf space and facings?
   - Performance metrics (velocity, profit per linear foot)?

3. **Product Performance**
   - Expected sales velocity?
   - Margin structure?
   - Promotional plans?
   - Cannibalization of existing products?
   - Competitive set and differentiation?

4. **Financial Constraints**
   - New product launch budget?
   - Slotting fee budget limits?
   - ROI requirements?
   - Payback period expectations?

---

## Slotting Fee Framework

### Understanding Slotting Fees

**What Are Slotting Fees?**
- One-time payment to retailer for shelf space
- Compensates retailer for:
  - Opportunity cost (displacing existing product)
  - Risk of failure (most new products fail)
  - Administrative costs (setup, systems, labor)
  - Warehouse space allocation

**Typical Slotting Fee Ranges (per SKU per store):**

| Channel | Low | Average | High |
|---------|-----|---------|------|
| Grocery | $500 | $1,500 | $5,000 |
| Mass Merchant | $1,000 | $3,000 | $10,000 |
| Club | $5,000 | $15,000 | $50,000 |
| Convenience | $100 | $500 | $2,000 |
| Drug | $1,000 | $2,500 | $7,500 |
| Natural/Organic | $500 | $2,000 | $5,000 |

**Factors Influencing Slotting Fees:**
- Retailer size and power
- Product category (shelf-stable vs. refrigerated vs. frozen)
- Brand strength (established vs. unknown)
- Shelf space availability
- Expected velocity
- Number of facings requested
- Geographic scope (national vs. regional)

---

## Slotting Fee Economics

### ROI Calculation Model

```python
import pandas as pd
import numpy as np

class SlottingFeeAnalyzer:
    """
    Analyze slotting fee economics and ROI
    """

    def __init__(self, product_data, retailer_data):
        """
        Initialize analyzer

        Parameters:
        - product_data: dict with product financials
        - retailer_data: dict with retailer scope and fees
        """
        self.product = product_data
        self.retailer = retailer_data

    def calculate_roi(self, time_horizon_months=12):
        """
        Calculate ROI on slotting fee investment

        Returns:
        - comprehensive financial analysis
        """

        # Slotting fee investment
        slotting_fee_per_store = self.retailer['slotting_fee_per_store']
        num_stores = self.retailer['num_stores']
        total_slotting = slotting_fee_per_store * num_stores

        # Sales forecast
        weekly_sales_per_store = self.product['expected_weekly_units_per_store']
        weeks_in_period = (time_horizon_months / 12) * 52
        total_units = weekly_sales_per_store * num_stores * weeks_in_period

        # Revenue
        retail_price = self.product['retail_price']
        wholesale_price = retail_price * (1 - self.retailer['retail_margin'])
        total_revenue = total_units * wholesale_price

        # Costs
        cogs_per_unit = self.product['cogs']
        total_cogs = total_units * cogs_per_unit

        # Gross profit
        gross_profit = total_revenue - total_cogs

        # Other trade spend
        promotional_rate = self.product.get('promotional_rate_pct', 0.20)
        promotional_spend = total_revenue * promotional_rate

        # Marketing support
        marketing_spend = self.product.get('marketing_spend', 0)

        # Net profit
        total_trade_investment = total_slotting + promotional_spend + marketing_spend
        net_profit = gross_profit - total_trade_investment

        # ROI metrics
        roi = net_profit / total_trade_investment if total_trade_investment > 0 else 0
        payback_months = (total_slotting / (net_profit / time_horizon_months)
                         if net_profit > 0 else float('inf'))

        # Profit per store
        profit_per_store = net_profit / num_stores

        # Sales per linear foot (assuming 1 facing = 4 inches)
        facings = self.product.get('facings', 1)
        linear_feet = (facings * 4) / 12
        annual_sales_per_lf = (total_revenue / time_horizon_months * 12) / (num_stores * linear_feet)

        return {
            'investment': {
                'slotting_fee': total_slotting,
                'slotting_per_store': slotting_fee_per_store,
                'promotional_spend': promotional_spend,
                'marketing_spend': marketing_spend,
                'total_investment': total_trade_investment
            },
            'sales': {
                'total_units': total_units,
                'total_revenue': total_revenue,
                'units_per_store_per_week': weekly_sales_per_store
            },
            'profitability': {
                'gross_profit': gross_profit,
                'net_profit': net_profit,
                'profit_per_store': profit_per_store,
                'gross_margin_pct': (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
            },
            'roi_metrics': {
                'roi': roi,
                'roi_pct': roi * 100,
                'payback_months': payback_months,
                'sales_per_linear_foot': annual_sales_per_lf
            },
            'recommendation': self._generate_recommendation(roi, payback_months)
        }

    def _generate_recommendation(self, roi, payback_months):
        """Generate go/no-go recommendation"""

        if roi > 0.50 and payback_months < 12:
            return {
                'decision': 'STRONG GO',
                'rationale': 'High ROI and fast payback'
            }
        elif roi > 0.25 and payback_months < 18:
            return {
                'decision': 'GO',
                'rationale': 'Positive ROI with acceptable payback'
            }
        elif roi > 0:
            return {
                'decision': 'MARGINAL',
                'rationale': 'Positive but weak ROI - negotiate better terms'
            }
        else:
            return {
                'decision': 'NO GO',
                'rationale': 'Negative ROI - do not proceed'
            }

    def sensitivity_analysis(self, variable, values):
        """
        Run sensitivity analysis on key variables

        Parameters:
        - variable: which variable to vary ('sales', 'slotting_fee', etc.)
        - values: range of values to test

        Returns:
        - sensitivity results
        """

        base_case = self.calculate_roi()
        results = []

        for value in values:
            # Modify parameter
            if variable == 'weekly_sales_per_store':
                self.product['expected_weekly_units_per_store'] = value
            elif variable == 'slotting_fee_per_store':
                self.retailer['slotting_fee_per_store'] = value
            elif variable == 'retail_price':
                self.product['retail_price'] = value

            # Recalculate
            scenario = self.calculate_roi()

            results.append({
                variable: value,
                'roi_pct': scenario['roi_metrics']['roi_pct'],
                'payback_months': scenario['roi_metrics']['payback_months'],
                'net_profit': scenario['profitability']['net_profit']
            })

        return pd.DataFrame(results)


# Example usage
product = {
    'sku': 'NEW_PRODUCT_A',
    'retail_price': 4.99,
    'cogs': 2.00,
    'expected_weekly_units_per_store': 5,
    'facings': 2,
    'promotional_rate_pct': 0.20,
    'marketing_spend': 50000
}

retailer = {
    'name': 'Major Grocery Chain',
    'num_stores': 500,
    'slotting_fee_per_store': 1500,
    'retail_margin': 0.25
}

analyzer = SlottingFeeAnalyzer(product, retailer)
analysis = analyzer.calculate_roi(time_horizon_months=12)

print(f"Total Investment: ${analysis['investment']['total_investment']:,.0f}")
print(f"Net Profit (Year 1): ${analysis['profitability']['net_profit']:,.0f}")
print(f"ROI: {analysis['roi_metrics']['roi_pct']:.0f}%")
print(f"Payback: {analysis['roi_metrics']['payback_months']:.1f} months")
print(f"Recommendation: {analysis['recommendation']['decision']}")
```

---

## Negotiation Strategies

### Slotting Fee Negotiation Framework

```python
class SlottingNegotiator:
    """
    Framework for negotiating slotting fees
    """

    def __init__(self, manufacturer_profile, product_profile):
        self.manufacturer = manufacturer_profile
        self.product = product_profile

    def assess_negotiating_power(self):
        """
        Assess negotiating power with retailer

        Factors that strengthen position:
        - Established brand with consumer pull
        - Category leadership
        - High expected velocity
        - Innovation/differentiation
        - Strong marketing support
        - Category captain status
        """

        power_score = 0

        # Brand strength (0-25 points)
        brand_strength = self.manufacturer.get('brand_awareness_pct', 0)
        power_score += (brand_strength / 4)

        # Market share in category (0-25 points)
        market_share = self.manufacturer.get('category_market_share_pct', 0)
        power_score += (market_share * 2.5)

        # Innovation (0-20 points)
        if self.product.get('first_to_market', False):
            power_score += 20
        elif self.product.get('highly_differentiated', False):
            power_score += 15
        elif self.product.get('line_extension', False):
            power_score += 5

        # Expected velocity (0-15 points)
        expected_velocity = self.product.get('expected_velocity_rank', 'medium')
        velocity_points = {'high': 15, 'medium': 10, 'low': 5}
        power_score += velocity_points.get(expected_velocity, 5)

        # Marketing support (0-15 points)
        marketing_budget = self.product.get('marketing_budget', 0)
        if marketing_budget > 500000:
            power_score += 15
        elif marketing_budget > 100000:
            power_score += 10
        else:
            power_score += 5

        # Classify negotiating position
        if power_score >= 75:
            position = 'STRONG'
        elif power_score >= 50:
            position = 'MODERATE'
        else:
            position = 'WEAK'

        return {
            'power_score': power_score,
            'position': position,
            'factors': self._identify_strengths_weaknesses(power_score)
        }

    def _identify_strengths_weaknesses(self, score):
        """Identify negotiating strengths and weaknesses"""

        strengths = []
        weaknesses = []

        if self.manufacturer.get('brand_awareness_pct', 0) > 60:
            strengths.append('Strong brand awareness')
        else:
            weaknesses.append('Low brand awareness')

        if self.manufacturer.get('category_market_share_pct', 0) > 15:
            strengths.append('Category leader')
        else:
            weaknesses.append('Small market share')

        if self.product.get('first_to_market', False):
            strengths.append('First-to-market innovation')

        return {'strengths': strengths, 'weaknesses': weaknesses}

    def generate_negotiation_tactics(self):
        """Generate negotiation tactics based on position"""

        power = self.assess_negotiating_power()
        position = power['position']

        tactics = []

        if position == 'STRONG':
            tactics = [
                'Refuse slotting fees entirely (consumer pull)',
                'Offer performance-based fees (pay only if targets met)',
                'Demand prime shelf location',
                'Request multi-year shelf space guarantee',
                'Negotiate category captain role',
                'Offer exclusive innovation window'
            ]

        elif position == 'MODERATE':
            tactics = [
                'Negotiate reduced slotting fee',
                'Offer performance guarantees (sales velocity)',
                'Bundle multiple SKUs for lower per-SKU fee',
                'Propose trial period with reduced fee',
                'Offer incremental promotional support',
                'Share consumer research data'
            ]

        else:  # WEAK
            tactics = [
                'Pay standard slotting fee',
                'Offer higher promotional support',
                'Accept secondary shelf location',
                'Start with limited distribution (test stores)',
                'Propose consignment terms',
                'Offer free fills or extended payment terms'
            ]

        return {
            'position': position,
            'tactics': tactics,
            'priority': self._prioritize_tactics(tactics)
        }

    def _prioritize_tactics(self, tactics):
        """Prioritize tactics to focus negotiation"""
        return tactics[:3]  # Top 3 tactics


# Example
manufacturer = {
    'brand_awareness_pct': 75,
    'category_market_share_pct': 22,
    'category_captain': True
}

product = {
    'first_to_market': True,
    'highly_differentiated': True,
    'expected_velocity_rank': 'high',
    'marketing_budget': 1000000
}

negotiator = SlottingNegotiator(manufacturer, product)
power = negotiator.assess_negotiating_power()
tactics = negotiator.generate_negotiation_tactics()

print(f"Negotiating Position: {power['position']} (Score: {power['power_score']:.0f})")
print("\nStrengths:")
for s in power['factors']['strengths']:
    print(f"  - {s}")

print("\nRecommended Tactics:")
for t in tactics['priority']:
    print(f"  - {t}")
```

---

## Alternative Approaches to Slotting Fees

### Performance-Based Agreements

```python
def design_performance_based_agreement(product, retailer, targets):
    """
    Design performance-based slotting agreement

    Instead of upfront slotting fee, tie payments to performance

    Parameters:
    - product: product information
    - retailer: retailer information
    - targets: performance targets

    Returns:
    - performance-based terms
    """

    # Traditional slotting fee
    traditional_fee = retailer['traditional_slotting_fee']

    # Performance tiers
    agreement = {
        'structure': 'performance_based',
        'upfront_fee': traditional_fee * 0.25,  # 25% upfront
        'performance_tiers': []
    }

    # Tier 1: Meet baseline target
    baseline_sales = targets['baseline_units_year1']
    tier1_payment = traditional_fee * 0.25

    agreement['performance_tiers'].append({
        'tier': 1,
        'target': f"{baseline_sales:,} units in Year 1",
        'payment': tier1_payment,
        'trigger': 'Meet baseline sales'
    })

    # Tier 2: Exceed baseline by 25%
    tier2_target = baseline_sales * 1.25
    tier2_payment = traditional_fee * 0.25

    agreement['performance_tiers'].append({
        'tier': 2,
        'target': f"{tier2_target:,} units in Year 1",
        'payment': tier2_payment,
        'trigger': 'Exceed baseline by 25%'
    })

    # Tier 3: Exceed baseline by 50%
    tier3_target = baseline_sales * 1.50
    tier3_payment = traditional_fee * 0.25

    agreement['performance_tiers'].append({
        'tier': 3,
        'target': f"{tier3_target:,} units in Year 1",
        'payment': tier3_payment,
        'trigger': 'Exceed baseline by 50%'
    })

    # Total potential payment
    agreement['max_total_payment'] = (
        agreement['upfront_fee'] +
        sum(tier['payment'] for tier in agreement['performance_tiers'])
    )

    # Benefits
    agreement['benefits'] = {
        'manufacturer': 'Reduced upfront risk, pay only for performance',
        'retailer': 'Potential for higher total fees, shared success'
    }

    return agreement


# Example
performance_agreement = design_performance_based_agreement(
    product={'sku': 'NEW_PRODUCT'},
    retailer={'traditional_slotting_fee': 750000},
    targets={'baseline_units_year1': 100000}
)

print("Performance-Based Agreement:")
print(f"Upfront: ${performance_agreement['upfront_fee']:,.0f}")
for tier in performance_agreement['performance_tiers']:
    print(f"Tier {tier['tier']}: {tier['target']} → ${tier['payment']:,.0f}")
print(f"Max Total: ${performance_agreement['max_total_payment']:,.0f}")
```

---

## Portfolio Optimization

### Optimizing Slotting Investments Across Products

```python
from pulp import *

def optimize_slotting_portfolio(products, total_budget, constraints):
    """
    Optimize slotting fee allocation across product portfolio

    Parameters:
    - products: list of products with slotting costs and expected returns
    - total_budget: total slotting fee budget
    - constraints: business constraints

    Returns:
    - optimal allocation
    """

    # Create problem
    prob = LpProblem("Slotting_Portfolio", LpMaximize)

    # Decision variables: invest in product i or not
    invest = LpVariable.dicts("Invest",
                               [p['sku'] for p in products],
                               cat='Binary')

    # Objective: Maximize total NPV
    prob += lpSum([
        invest[p['sku']] * p['expected_npv']
        for p in products
    ])

    # Constraints

    # 1. Budget constraint
    prob += lpSum([
        invest[p['sku']] * p['total_slotting_cost']
        for p in products
    ]) <= total_budget

    # 2. Minimum new products per year
    min_new_products = constraints.get('min_new_products', 0)
    prob += lpSum([invest[p['sku']] for p in products]) >= min_new_products

    # 3. Category requirements (at least X products per category)
    categories = set(p['category'] for p in products)
    for category in categories:
        min_per_category = constraints.get(f'min_{category}', 0)
        prob += lpSum([
            invest[p['sku']]
            for p in products
            if p['category'] == category
        ]) >= min_per_category

    # 4. Strategic must-haves
    must_invest = constraints.get('must_invest', [])
    for sku in must_invest:
        if sku in [p['sku'] for p in products]:
            prob += invest[sku] == 1

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    selected_products = []
    total_cost = 0
    total_npv = 0

    for p in products:
        if invest[p['sku']].varValue > 0.5:
            selected_products.append({
                'sku': p['sku'],
                'category': p['category'],
                'slotting_cost': p['total_slotting_cost'],
                'expected_npv': p['expected_npv'],
                'roi': p['expected_npv'] / p['total_slotting_cost']
            })
            total_cost += p['total_slotting_cost']
            total_npv += p['expected_npv']

    results = {
        'status': LpStatus[prob.status],
        'selected_products': pd.DataFrame(selected_products),
        'num_products': len(selected_products),
        'total_slotting_cost': total_cost,
        'total_expected_npv': total_npv,
        'portfolio_roi': total_npv / total_cost if total_cost > 0 else 0
    }

    return results


# Example
products = [
    {'sku': 'Product_A', 'category': 'snacks', 'total_slotting_cost': 500000,
     'expected_npv': 750000},
    {'sku': 'Product_B', 'category': 'snacks', 'total_slotting_cost': 400000,
     'expected_npv': 300000},
    {'sku': 'Product_C', 'category': 'beverages', 'total_slotting_cost': 600000,
     'expected_npv': 900000},
    {'sku': 'Product_D', 'category': 'beverages', 'total_slotting_cost': 350000,
     'expected_npv': 200000},
    {'sku': 'Product_E', 'category': 'snacks', 'total_slotting_cost': 450000,
     'expected_npv': 600000}
]

result = optimize_slotting_portfolio(
    products=products,
    total_budget=1500000,
    constraints={
        'min_new_products': 3,
        'must_invest': ['Product_C']  # Strategic priority
    }
)

print(f"Selected {result['num_products']} products")
print(f"Total Investment: ${result['total_slotting_cost']:,.0f}")
print(f"Expected NPV: ${result['total_expected_npv']:,.0f}")
print(f"Portfolio ROI: {result['portfolio_roi']:.1%}")
print("\nSelected Products:")
print(result['selected_products'][['sku', 'slotting_cost', 'expected_npv', 'roi']])
```

---

## Monitoring and Performance Tracking

### Post-Launch Performance Tracking

```python
class SlottingPerformanceTracker:
    """
    Track actual performance vs. business case
    """

    def __init__(self, business_case):
        self.business_case = business_case
        self.actual_performance = []

    def record_performance(self, period_data):
        """Record actual sales performance for a period"""
        self.actual_performance.append(period_data)

    def compare_to_business_case(self):
        """Compare actual to business case projections"""

        if not self.actual_performance:
            return None

        df = pd.DataFrame(self.actual_performance)

        # Cumulative actuals
        cumulative_units = df['units_sold'].sum()
        cumulative_revenue = df['revenue'].sum()

        # Business case projections (annualized)
        bc_units = self.business_case['projected_annual_units']
        bc_revenue = self.business_case['projected_annual_revenue']

        # Months of data
        months_tracked = len(df)

        # Annualized actuals
        annualized_units = cumulative_units * (12 / months_tracked)
        annualized_revenue = cumulative_revenue * (12 / months_tracked)

        # Variance
        units_variance = annualized_units - bc_units
        revenue_variance = annualized_revenue - bc_revenue

        # ROI recalculation
        actual_gross_profit = cumulative_revenue * self.business_case['gross_margin']
        slotting_investment = self.business_case['slotting_fee']
        annualized_gross_profit = actual_gross_profit * (12 / months_tracked)

        actual_roi = (annualized_gross_profit - slotting_investment) / slotting_investment

        comparison = {
            'months_tracked': months_tracked,
            'business_case': {
                'projected_units': bc_units,
                'projected_revenue': bc_revenue,
                'projected_roi': self.business_case['projected_roi']
            },
            'actual_annualized': {
                'units': annualized_units,
                'revenue': annualized_revenue,
                'roi': actual_roi
            },
            'variance': {
                'units': units_variance,
                'units_pct': units_variance / bc_units * 100,
                'revenue': revenue_variance,
                'revenue_pct': revenue_variance / bc_revenue * 100
            },
            'performance_vs_plan': self._classify_performance(
                units_variance / bc_units * 100
            )
        }

        return comparison

    def _classify_performance(self, variance_pct):
        """Classify performance vs. plan"""

        if variance_pct > 10:
            return 'EXCEEDING'
        elif variance_pct > -10:
            return 'ON_TRACK'
        else:
            return 'UNDERPERFORMING'


# Example
business_case = {
    'projected_annual_units': 500000,
    'projected_annual_revenue': 2500000,
    'projected_roi': 0.45,
    'slotting_fee': 750000,
    'gross_margin': 0.35
}

tracker = SlottingPerformanceTracker(business_case)

# Record actual performance
tracker.record_performance({'month': 1, 'units_sold': 35000, 'revenue': 175000})
tracker.record_performance({'month': 2, 'units_sold': 40000, 'revenue': 200000})
tracker.record_performance({'month': 3, 'units_sold': 45000, 'revenue': 225000})

comparison = tracker.compare_to_business_case()

print(f"Performance: {comparison['performance_vs_plan']}")
print(f"Projected Annual Units: {comparison['business_case']['projected_units']:,}")
print(f"Actual Annualized Units: {comparison['actual_annualized']['units']:,.0f}")
print(f"Variance: {comparison['variance']['units_pct']:+.1f}%")
```

---

## Tools & Technologies

### Slotting and Trade Management Software

**Trade Promotion Management (TPM/TPO):**
- **SAP TPM**: Trade promotion and slotting management
- **Oracle TPM**: Deductions and trade spend management
- **Blacksmith Applications**: TPM/TPO for CPG
- **AFS Trade Promotion**: Analytics and optimization
- **Wipro Promax**: Cloud TPM platform

**Retail Analytics:**
- **Nielsen**: Retail measurement and shelf analytics
- **IRI**: Syndicated data and space planning
- **84.51° (Kroger)**: Retailer data and insights
- **Catalina**: Personalized retail media
- **dunnhumby**: Retail science and analytics

### Python Libraries

```python
# Financial modeling
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Optimization
from pulp import *

# Data analysis
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
```

---

## Common Challenges & Solutions

### Challenge: High Slotting Fees Prevent New Product Launch

**Problem:**
- Retailer wants $2M in slotting fees
- Budget only $1M
- Can't launch without this retailer

**Solutions:**
- Negotiate performance-based terms (reduced upfront)
- Start with smaller store count (test stores)
- Bundle multiple SKUs for reduced per-SKU fee
- Offer higher promotional support instead of slotting
- Find alternative retailers with lower fees
- Delay launch until more capital available

### Challenge: Poor ROI on Previous Launches

**Problem:**
- Last 3 products underperformed projections
- Lost money on slotting investments
- Credibility damaged with management

**Solutions:**
- Post-mortem analysis (why did products fail?)
- Improve sales forecasting (conservative projections)
- Better product testing (more research, test markets)
- Tighter launch criteria (raise ROI bar)
- Negotiate performance guarantees with retailers
- Focus on fewer, better products

### Challenge: Retailer Demands Increasing Fees

**Problem:**
- Fees up 20% year-over-year
- Squeezing margins
- Threatening profitability

**Solutions:**
- Negotiate multi-year agreements (lock in rates)
- Demonstrate high velocity (data-driven negotiation)
- Pursue category captain status (eliminate some fees)
- Shift mix to online/direct (bypass retailers)
- Consolidate SKUs (reduce fee burden)
- Build consumer demand (pull vs. push)

---

## Output Format

### Slotting Fee Business Case Template

**Product Information:**
- Product: New Organic Granola Bar
- Category: Snacks - Bars
- SKUs: 3 flavors
- Retail Price: $4.99
- COGS: $2.10
- Gross Margin: 58%

**Retailer Information:**
- Retailer: National Grocery Chain
- Stores: 1,200
- Slotting Fee: $1,800 per SKU per store
- Total Slotting Investment: $6,480,000

**Sales Projections (Year 1):**

| Metric | Per Store Per Week | Total Annual |
|--------|--------------------|--------------|
| Units | 8 | 499,200 |
| Revenue (wholesale) | $30 | $18,637,000 |
| Gross Profit | $17.40 | $10,809,000 |

**Cost Structure:**

| Item | Amount | % of Sales |
|------|--------|------------|
| Slotting Fees | $6,480,000 | 34.8% |
| Promotional Support | $1,863,700 | 10.0% |
| Marketing | $500,000 | 2.7% |
| **Total Investment** | **$8,843,700** | **47.5%** |

**Financial Metrics:**

| Metric | Value |
|--------|-------|
| Year 1 Net Profit | $1,965,300 |
| ROI | 22.2% |
| Payback Period | 10.8 months |
| Sales per Linear Foot | $17,320 |

**Recommendation: GO**
- Positive ROI and sub-12 month payback
- High sales per linear foot justifies space
- Strong promotional plan to drive velocity
- Mitigate risk: Start with 600 stores (test phase)

**Risks & Mitigation:**
1. Risk: Lower than expected velocity
   - Mitigation: Performance-based agreement (25% upfront, balance at 6 months if targets met)

2. Risk: High cannibalization of existing products
   - Mitigation: Test market analysis shows <15% cannibalization

3. Risk: Retailer demands pay-to-stay fees Year 2
   - Mitigation: Negotiate 2-year agreement upfront

---

## Questions to Ask

If you need more context:
1. What products are you planning to introduce or maintain?
2. What retailers and how many stores?
3. What slotting fees are being quoted?
4. What are your sales projections (units per store per week)?
5. What's your product's margin structure?
6. Do you have existing relationships with these retailers?
7. Is this a new category entry or line extension?
8. What's your negotiating leverage (brand strength, innovation, etc.)?

---

## Related Skills

- **promotional-planning**: For trade promotion optimization
- **retail-replenishment**: For retailer inventory management
- **demand-forecasting**: For sales projections
- **markdown-optimization**: For pricing strategies
- **procurement-optimization**: For negotiation frameworks
- **supplier-selection**: For retailer selection criteria
- **strategic-sourcing**: For long-term retailer partnerships
- **spend-analysis**: For trade spend tracking and optimization
