---
name: sales-operations-planning
description: When the user wants to implement S&OP process, integrate demand and supply planning, balance business objectives, or facilitate executive planning meetings. Also use when the user mentions "S&OP," "IBP" (Integrated Business Planning), "demand-supply balancing," "executive S&OP," "monthly planning cycle," "consensus demand," "supply review," or "financial reconciliation." For detailed demand forecasts, see demand-forecasting. For capacity analysis, see capacity-planning.
---

# Sales & Operations Planning (S&OP)

You are an expert in Sales & Operations Planning (S&OP) and Integrated Business Planning (IBP). Your goal is to help organizations implement effective S&OP processes that align demand, supply, finance, and strategy to drive better business decisions.

## Initial Assessment

Before implementing or improving S&OP, understand:

1. **Current State**
   - Existing planning process? (informal, Excel-based, system-driven)
   - Planning cycle and frequency? (monthly, weekly)
   - Who participates? (Sales, Ops, Finance, Exec team)
   - Current pain points and issues?

2. **Organization Context**
   - Company size and complexity?
   - Number of product families/SKUs?
   - Geographic scope? (single site, regional, global)
   - Industry characteristics? (seasonal, promotional, project-based)

3. **Planning Maturity**
   - Forecast accuracy levels?
   - Cross-functional collaboration quality?
   - Data systems and integration?
   - Performance measurement?

4. **Business Objectives**
   - Strategic goals? (growth, margin, service, inventory)
   - Key metrics and targets?
   - Decision-making authority and governance?
   - Stakeholder expectations?

---

## S&OP Framework

### S&OP Definition

**Sales & Operations Planning (S&OP)** is a monthly integrated business management process that brings together all plans for the business (customers, sales, marketing, operations, engineering, finance, product management) into one integrated set of plans.

**Key Principles:**
1. **Cross-Functional Integration**: Break down silos
2. **Forward-Looking**: 18-24 month rolling horizon
3. **Executive-Owned**: Leadership accountability
4. **Single Version of Truth**: One consensus plan
5. **Decision-Focused**: Drive actions, not just reports

### S&OP vs. IBP (Integrated Business Planning)

| Aspect | S&OP | IBP |
|--------|------|-----|
| **Scope** | Demand-Supply balance | Strategic + Financial integration |
| **Horizon** | 12-18 months | 24-36+ months |
| **Frequency** | Monthly | Monthly + quarterly reviews |
| **Focus** | Operational alignment | Strategic + operational |
| **Participants** | Cross-functional | Includes Finance, Strategy |
| **Outputs** | Volume plans | Volume + Financial plans |

---

## S&OP Process Steps

### Monthly S&OP Cycle

**Five-Step Process:**

```
Week 1: Data Gathering & Demand Review
Week 2: Supply/Capacity Review
Week 3: Pre-S&OP Meeting
Week 4: Executive S&OP Meeting
Week 5: Implementation & Monitoring
```

### Step 1: Data Gathering & Forecasting

**Objectives:**
- Collect actual performance data
- Generate statistical baseline forecasts
- Identify exceptions and anomalies

**Activities:**
- Update actual sales, production, inventory
- Run forecasting models
- Calculate forecast accuracy
- Flag exceptions (large changes, new products)

**Outputs:**
- Statistical forecast by product family
- Forecast accuracy metrics (MAPE, bias)
- Exception reports
- Data quality issues log

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SopDataGathering:
    """Data gathering and baseline forecasting for S&OP"""

    def __init__(self, historical_data):
        """
        Parameters:
        - historical_data: DataFrame with 'date', 'product_family', 'actual_sales'
        """
        self.data = historical_data

    def calculate_forecast_accuracy(self, forecast_col='forecast',
                                    actual_col='actual_sales'):
        """Calculate forecast accuracy metrics"""

        df = self.data.copy()

        # MAPE (Mean Absolute Percentage Error)
        df['ape'] = np.abs((df[actual_col] - df[forecast_col]) / df[actual_col]) * 100
        mape = df['ape'].mean()

        # Bias (average error)
        df['error'] = df[forecast_col] - df[actual_col]
        bias = df['error'].mean()
        bias_pct = (bias / df[actual_col].mean()) * 100

        # MAD (Mean Absolute Deviation)
        mad = np.abs(df['error']).mean()

        # Tracking signal
        cumulative_error = df['error'].sum()
        tracking_signal = cumulative_error / mad if mad > 0 else 0

        return {
            'mape': mape,
            'bias': bias,
            'bias_pct': bias_pct,
            'mad': mad,
            'tracking_signal': tracking_signal
        }

    def identify_exceptions(self, threshold_pct=20):
        """
        Identify forecast exceptions requiring attention

        Parameters:
        - threshold_pct: % change threshold for flagging
        """

        df = self.data.copy()

        # Calculate month-over-month change
        df = df.sort_values(['product_family', 'date'])
        df['prev_forecast'] = df.groupby('product_family')['forecast'].shift(1)
        df['forecast_change_pct'] = (
            (df['forecast'] - df['prev_forecast']) / df['prev_forecast'] * 100
        )

        # Flag large changes
        exceptions = df[
            np.abs(df['forecast_change_pct']) > threshold_pct
        ].copy()

        return exceptions[['product_family', 'date', 'forecast',
                          'prev_forecast', 'forecast_change_pct']]

    def generate_baseline_forecast(self, periods_ahead=18):
        """
        Generate statistical baseline forecast

        Simple approach using moving average with trend
        """

        forecasts = []

        for product in self.data['product_family'].unique():
            product_data = self.data[
                self.data['product_family'] == product
            ].sort_values('date')

            # Calculate moving average and trend
            recent_avg = product_data['actual_sales'].tail(3).mean()
            older_avg = product_data['actual_sales'].tail(6).head(3).mean()
            trend = (recent_avg - older_avg) / 3  # Per period trend

            # Generate forecast
            last_date = product_data['date'].max()

            for i in range(1, periods_ahead + 1):
                forecast_date = last_date + pd.DateOffset(months=i)
                forecast_value = recent_avg + (trend * i)
                forecast_value = max(0, forecast_value)  # No negative forecasts

                forecasts.append({
                    'product_family': product,
                    'date': forecast_date,
                    'baseline_forecast': forecast_value,
                    'method': 'MA_with_trend'
                })

        return pd.DataFrame(forecasts)

# Example usage
historical = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=12, freq='MS'),
    'product_family': ['Electronics'] * 12,
    'actual_sales': [1000, 1100, 1050, 1200, 1250, 1300, 1280, 1350, 1400, 1450, 1500, 1550],
    'forecast': [980, 1120, 1000, 1180, 1300, 1250, 1300, 1320, 1380, 1480, 1520, 1500]
})

sop_data = SopDataGathering(historical)

# Calculate accuracy
accuracy = sop_data.calculate_forecast_accuracy()
print("Forecast Accuracy:")
print(f"  MAPE: {accuracy['mape']:.1f}%")
print(f"  Bias: {accuracy['bias_pct']:.1f}%")

# Identify exceptions
exceptions = sop_data.identify_exceptions(threshold_pct=15)
print(f"\nExceptions (>{15}% change): {len(exceptions)}")

# Generate baseline
baseline = sop_data.generate_baseline_forecast(periods_ahead=6)
print("\nBaseline Forecast (next 6 months):")
print(baseline.head())
```

### Step 2: Demand Review

**Objectives:**
- Review and adjust statistical forecast
- Incorporate market intelligence
- Build consensus demand plan

**Participants:**
- Sales leadership
- Marketing
- Product management
- Demand planning
- Finance (observer)

**Activities:**
- Review statistical forecast
- Discuss upcoming promotions, launches
- Consider market trends, competitive actions
- Adjust forecasts based on business intelligence
- Document assumptions and risks

**Key Questions:**
- What's changed since last month?
- Any new customer wins/losses?
- Promotional plans finalized?
- Pricing changes impact?
- Competitive landscape shifts?

**Outputs:**
- Consensus demand forecast by product family
- Demand assumptions documented
- Upside/downside scenarios
- Risks and opportunities identified

```python
class DemandReview:
    """Demand review and consensus building"""

    def __init__(self, statistical_forecast):
        self.statistical_fcst = statistical_forecast
        self.adjustments = []
        self.assumptions = []

    def add_adjustment(self, product_family, period, adjustment_type,
                      adjustment_value, reason, owner):
        """
        Record demand adjustment

        Parameters:
        - adjustment_type: 'absolute', 'percentage', 'additive'
        - adjustment_value: amount of adjustment
        - reason: business rationale
        - owner: who made the adjustment (Sales, Marketing, etc.)
        """

        self.adjustments.append({
            'product_family': product_family,
            'period': period,
            'adjustment_type': adjustment_type,
            'adjustment_value': adjustment_value,
            'reason': reason,
            'owner': owner,
            'timestamp': datetime.now()
        })

    def add_assumption(self, assumption_text, category, impact_level):
        """
        Document planning assumption

        Parameters:
        - category: 'promotion', 'market', 'competitive', 'economic'
        - impact_level: 'low', 'medium', 'high'
        """

        self.assumptions.append({
            'assumption': assumption_text,
            'category': category,
            'impact_level': impact_level,
            'date_added': datetime.now()
        })

    def calculate_consensus_forecast(self):
        """Apply adjustments to create consensus forecast"""

        consensus = self.statistical_fcst.copy()

        for adj in self.adjustments:
            mask = (
                (consensus['product_family'] == adj['product_family']) &
                (consensus['period'] == adj['period'])
            )

            if adj['adjustment_type'] == 'percentage':
                consensus.loc[mask, 'consensus_forecast'] = (
                    consensus.loc[mask, 'statistical_forecast'] *
                    (1 + adj['adjustment_value'] / 100)
                )
            elif adj['adjustment_type'] == 'additive':
                consensus.loc[mask, 'consensus_forecast'] = (
                    consensus.loc[mask, 'statistical_forecast'] +
                    adj['adjustment_value']
                )
            elif adj['adjustment_type'] == 'absolute':
                consensus.loc[mask, 'consensus_forecast'] = adj['adjustment_value']

        # Calculate forecast value added (FVA)
        consensus['adjustment'] = (
            consensus['consensus_forecast'] - consensus['statistical_forecast']
        )

        return consensus

    def create_demand_scenarios(self, consensus_forecast):
        """
        Create upside/downside scenarios

        Typically: Base, Optimistic (+15%), Pessimistic (-15%)
        """

        scenarios = consensus_forecast.copy()

        scenarios['base_case'] = scenarios['consensus_forecast']
        scenarios['optimistic'] = scenarios['consensus_forecast'] * 1.15
        scenarios['pessimistic'] = scenarios['consensus_forecast'] * 0.85

        return scenarios

    def get_adjustment_summary(self):
        """Summarize adjustments by owner and type"""

        if not self.adjustments:
            return pd.DataFrame()

        df = pd.DataFrame(self.adjustments)

        summary = df.groupby(['owner', 'adjustment_type']).agg({
            'adjustment_value': ['count', 'sum', 'mean']
        }).reset_index()

        return summary

# Example
statistical_fcst = pd.DataFrame({
    'product_family': ['Electronics', 'Electronics', 'Appliances', 'Appliances'],
    'period': ['2025-01', '2025-02', '2025-01', '2025-02'],
    'statistical_forecast': [10000, 10200, 5000, 5100]
})

demand_review = DemandReview(statistical_fcst)

# Add adjustments
demand_review.add_adjustment(
    product_family='Electronics',
    period='2025-01',
    adjustment_type='percentage',
    adjustment_value=10,  # +10%
    reason='New product launch expected to drive 10% uplift',
    owner='Product Management'
)

demand_review.add_adjustment(
    product_family='Appliances',
    period='2025-02',
    adjustment_type='additive',
    adjustment_value=-500,
    reason='Competitor pricing pressure',
    owner='Sales'
)

# Add assumptions
demand_review.add_assumption(
    'Q1 promotional campaign will increase demand 10-15%',
    category='promotion',
    impact_level='high'
)

# Calculate consensus
consensus = demand_review.calculate_consensus_forecast()
print("Consensus Demand Forecast:")
print(consensus)

# Scenarios
scenarios = demand_review.create_demand_scenarios(consensus)
print("\nDemand Scenarios:")
print(scenarios[['product_family', 'period', 'pessimistic', 'base_case', 'optimistic']])
```

### Step 3: Supply Review

**Objectives:**
- Assess supply capacity to meet demand
- Identify constraints and gaps
- Develop supply alternatives

**Participants:**
- Operations leadership
- Manufacturing
- Procurement
- Supply planning
- Engineering

**Activities:**
- Review production capacity vs. demand
- Identify bottlenecks and constraints
- Assess supplier capability
- Evaluate inventory positions
- Propose supply solutions

**Key Questions:**
- Can we meet the demand plan?
- What are the constraints?
- Lead time for capacity additions?
- Supply chain risks?
- Cost implications?

**Outputs:**
- Supply plan by product family
- Capacity gaps identified
- Alternative supply scenarios
- Inventory strategy
- Investment requirements

```python
class SupplyReview:
    """Supply review and capacity analysis"""

    def __init__(self, consensus_demand, capacity_data):
        """
        Parameters:
        - consensus_demand: demand forecast
        - capacity_data: available capacity by period
        """
        self.demand = consensus_demand
        self.capacity = capacity_data

    def analyze_capacity_gaps(self):
        """Identify where demand exceeds capacity"""

        # Merge demand and capacity
        analysis = self.demand.merge(
            self.capacity,
            on=['product_family', 'period'],
            how='left'
        )

        # Calculate gap
        analysis['gap'] = analysis['available_capacity'] - analysis['consensus_forecast']
        analysis['gap_pct'] = (analysis['gap'] / analysis['available_capacity']) * 100
        analysis['status'] = analysis['gap'].apply(
            lambda x: 'OK' if x >= 0 else 'CONSTRAINED'
        )

        # Utilization
        analysis['utilization'] = (
            analysis['consensus_forecast'] / analysis['available_capacity'] * 100
        )

        return analysis

    def propose_supply_scenarios(self, gap_analysis):
        """
        Develop supply alternatives for constrained periods

        Scenarios:
        1. Do Nothing (accept stockouts)
        2. Add Overtime
        3. Outsource
        4. Build Ahead
        """

        constrained = gap_analysis[gap_analysis['status'] == 'CONSTRAINED'].copy()

        if constrained.empty:
            return pd.DataFrame()

        scenarios = []

        for idx, row in constrained.iterrows():
            product = row['product_family']
            period = row['period']
            shortage = abs(row['gap'])

            # Scenario 1: Do Nothing
            scenarios.append({
                'product_family': product,
                'period': period,
                'scenario': 'Do Nothing',
                'additional_supply': 0,
                'cost': shortage * 100,  # Lost sales cost
                'risk': 'High',
                'feasibility': 'Certain'
            })

            # Scenario 2: Overtime
            overtime_capacity = row['available_capacity'] * 0.15  # 15% OT
            overtime_supply = min(shortage, overtime_capacity)
            scenarios.append({
                'product_family': product,
                'period': period,
                'scenario': 'Overtime',
                'additional_supply': overtime_supply,
                'cost': overtime_supply * 15,  # Premium cost
                'risk': 'Medium',
                'feasibility': 'High'
            })

            # Scenario 3: Outsource
            scenarios.append({
                'product_family': product,
                'period': period,
                'scenario': 'Outsource',
                'additional_supply': shortage,
                'cost': shortage * 20,  # Outsource premium
                'risk': 'Medium',
                'feasibility': 'Medium'
            })

            # Scenario 4: Build Ahead
            # Produce in prior period
            scenarios.append({
                'product_family': product,
                'period': period,
                'scenario': 'Build Ahead',
                'additional_supply': shortage,
                'cost': shortage * 5,  # Inventory holding cost
                'risk': 'Low',
                'feasibility': 'High'
            })

        return pd.DataFrame(scenarios)

    def calculate_inventory_plan(self, gap_analysis, safety_stock_days=30):
        """
        Develop inventory strategy

        Target: Safety stock + cycle stock
        """

        inventory_plan = gap_analysis.copy()

        # Daily demand rate
        inventory_plan['daily_demand'] = inventory_plan['consensus_forecast'] / 30

        # Safety stock
        inventory_plan['safety_stock'] = inventory_plan['daily_demand'] * safety_stock_days

        # Cycle stock (assume monthly production)
        inventory_plan['cycle_stock'] = inventory_plan['consensus_forecast'] / 2

        # Target inventory
        inventory_plan['target_inventory'] = (
            inventory_plan['safety_stock'] + inventory_plan['cycle_stock']
        )

        return inventory_plan[['product_family', 'period', 'consensus_forecast',
                              'safety_stock', 'cycle_stock', 'target_inventory']]

# Example
consensus_demand = pd.DataFrame({
    'product_family': ['Electronics', 'Electronics', 'Appliances'],
    'period': ['2025-01', '2025-02', '2025-01'],
    'consensus_forecast': [11000, 10200, 4500]
})

capacity_data = pd.DataFrame({
    'product_family': ['Electronics', 'Electronics', 'Appliances'],
    'period': ['2025-01', '2025-02', '2025-01'],
    'available_capacity': [10000, 12000, 5000]
})

supply_review = SupplyReview(consensus_demand, capacity_data)

# Analyze gaps
gaps = supply_review.analyze_capacity_gaps()
print("Capacity Gap Analysis:")
print(gaps[['product_family', 'period', 'consensus_forecast',
            'available_capacity', 'gap', 'status', 'utilization']])

# Propose scenarios
scenarios = supply_review.propose_supply_scenarios(gaps)
if not scenarios.empty:
    print("\nSupply Scenarios for Constrained Periods:")
    print(scenarios)

# Inventory plan
inventory = supply_review.calculate_inventory_plan(gaps)
print("\nInventory Plan:")
print(inventory)
```

### Step 4: Pre-S&OP Meeting

**Objectives:**
- Reconcile demand and supply
- Develop recommendations for executive team
- Prepare scenarios and trade-offs

**Participants:**
- S&OP process owner/facilitator
- Demand planning leader
- Supply planning leader
- Finance
- Selected business unit leaders

**Activities:**
- Review demand-supply balance
- Identify gaps and conflicts
- Develop scenarios with pros/cons/costs
- Align financial impact
- Prepare executive presentation

**Key Outputs:**
- Balanced demand-supply plan (base case)
- Alternative scenarios with trade-offs
- Financial reconciliation
- Recommendation with rationale
- Open issues requiring executive decision

```python
class PreSopMeeting:
    """Pre-S&OP meeting preparation and analysis"""

    def __init__(self, demand_plan, supply_plan, financial_data):
        self.demand = demand_plan
        self.supply = supply_plan
        self.financial = financial_data

    def create_demand_supply_balance(self):
        """Create integrated view of demand and supply"""

        balance = self.demand.merge(
            self.supply,
            on=['product_family', 'period'],
            how='outer'
        )

        balance['supply_demand_gap'] = (
            balance['supply_plan'] - balance['consensus_forecast']
        )

        balance['inventory_impact'] = balance['supply_demand_gap'].cumsum()

        return balance

    def financial_reconciliation(self, balance_plan):
        """Calculate financial impact of plan"""

        financial = balance_plan.merge(
            self.financial,
            on='product_family',
            how='left'
        )

        # Revenue
        financial['revenue'] = (
            financial['consensus_forecast'] * financial['price_per_unit']
        )

        # COGS
        financial['cogs'] = (
            financial['supply_plan'] * financial['cost_per_unit']
        )

        # Inventory value
        financial['inventory_value'] = (
            financial['inventory_impact'] * financial['cost_per_unit']
        )

        # Gross margin
        financial['gross_margin'] = financial['revenue'] - financial['cogs']

        # Aggregate by period
        summary = financial.groupby('period').agg({
            'revenue': 'sum',
            'cogs': 'sum',
            'gross_margin': 'sum',
            'inventory_value': 'sum'
        }).reset_index()

        summary['gross_margin_pct'] = (
            summary['gross_margin'] / summary['revenue'] * 100
        )

        return summary

    def create_scenario_comparison(self, scenarios_list):
        """
        Compare multiple scenarios

        Parameters:
        - scenarios_list: list of dicts with scenario details
        """

        comparison = pd.DataFrame(scenarios_list)

        # Rank scenarios
        comparison['total_score'] = (
            comparison['service_level'] * 0.4 +
            (100 - comparison['cost_impact_pct']) * 0.3 +
            comparison['feasibility'] * 0.3
        )

        comparison = comparison.sort_values('total_score', ascending=False)

        return comparison

    def generate_executive_summary(self, balance, financials):
        """Create executive summary for S&OP meeting"""

        summary = {
            'planning_period': balance['period'].min(),
            'total_demand': balance['consensus_forecast'].sum(),
            'total_supply': balance['supply_plan'].sum(),
            'net_inventory_change': balance['supply_demand_gap'].sum(),
            'revenue_plan': financials['revenue'].sum(),
            'gross_margin_pct': (
                financials['gross_margin'].sum() /
                financials['revenue'].sum() * 100
            ),
            'constraints': balance[balance['supply_demand_gap'] < 0].shape[0],
            'excess_capacity': balance[balance['supply_demand_gap'] > balance['consensus_forecast'] * 0.2].shape[0]
        }

        return summary

# Example
demand_plan = pd.DataFrame({
    'product_family': ['Electronics'] * 3,
    'period': ['2025-01', '2025-02', '2025-03'],
    'consensus_forecast': [11000, 10200, 10500]
})

supply_plan = pd.DataFrame({
    'product_family': ['Electronics'] * 3,
    'period': ['2025-01', '2025-02', '2025-03'],
    'supply_plan': [10000, 11000, 10500]
})

financial_data = pd.DataFrame({
    'product_family': ['Electronics'],
    'price_per_unit': [100],
    'cost_per_unit': [60]
})

pre_sop = PreSopMeeting(demand_plan, supply_plan, financial_data)

# Create balance
balance = pre_sop.create_demand_supply_balance()
print("Demand-Supply Balance:")
print(balance)

# Financial reconciliation
financials = pre_sop.financial_reconciliation(balance)
print("\nFinancial Summary:")
print(financials)

# Executive summary
exec_summary = pre_sop.generate_executive_summary(balance, financials)
print("\nExecutive Summary:")
for key, value in exec_summary.items():
    print(f"  {key}: {value}")

# Scenario comparison
scenarios = [
    {
        'scenario': 'Base Plan',
        'service_level': 95,
        'cost_impact_pct': 0,
        'feasibility': 90,
        'description': 'Meet demand with overtime'
    },
    {
        'scenario': 'Constrain Demand',
        'service_level': 85,
        'cost_impact_pct': -5,
        'feasibility': 100,
        'description': 'Limit sales to capacity'
    },
    {
        'scenario': 'Outsource',
        'service_level': 98,
        'cost_impact_pct': 15,
        'feasibility': 70,
        'description': 'Use contract manufacturer'
    }
]

scenario_comparison = pre_sop.create_scenario_comparison(scenarios)
print("\nScenario Comparison:")
print(scenario_comparison)
```

### Step 5: Executive S&OP Meeting

**Objectives:**
- Make final decisions on plans
- Resolve gaps and trade-offs
- Approve resource commitments
- Align on strategic priorities

**Participants:**
- CEO or COO (chair)
- VP Sales
- VP Operations
- CFO
- VP Supply Chain
- VP Product/Marketing
- Business unit heads

**Duration:** 2-4 hours

**Agenda:**
1. **Review Performance** (15 min)
   - Last month actual vs. plan
   - Key metrics and KPIs
   - Forecast accuracy

2. **Demand Review** (30 min)
   - Consensus demand by product family
   - Key changes and assumptions
   - Risks and opportunities

3. **Supply Review** (30 min)
   - Capacity and constraints
   - Supply alternatives
   - Inventory strategy

4. **Financial Review** (20 min)
   - Revenue and margin impact
   - Working capital
   - Budget alignment

5. **Scenarios and Trade-Offs** (45 min)
   - Present alternatives
   - Discuss implications
   - Make decisions

6. **Strategic Issues** (30 min)
   - New product launches
   - Capacity investments
   - Market opportunities
   - Risk mitigation

7. **Decisions and Actions** (20 min)
   - Document decisions
   - Assign action items
   - Set follow-ups

**Key Decisions:**
- Approve demand plan
- Approve supply and inventory plan
- Resource allocation decisions
- Investment approvals
- Policy changes

**Outputs:**
- Approved S&OP plan
- Decision log
- Action items with owners
- Risks and contingencies

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class SopDecision:
    """Record of S&OP decision"""
    decision_id: str
    decision_text: str
    category: str  # 'demand', 'supply', 'financial', 'strategic'
    owner: str
    due_date: datetime
    status: str  # 'approved', 'pending', 'rejected'
    rationale: str
    financial_impact: float

@dataclass
class SopActionItem:
    """Action item from S&OP meeting"""
    action_id: str
    description: str
    owner: str
    due_date: datetime
    status: str  # 'open', 'in_progress', 'completed'
    priority: str  # 'high', 'medium', 'low'

class ExecutiveSopMeeting:
    """Executive S&OP meeting management"""

    def __init__(self, meeting_date):
        self.meeting_date = meeting_date
        self.decisions = []
        self.action_items = []
        self.approved_plan = None

    def add_decision(self, decision: SopDecision):
        """Record a decision from the meeting"""
        self.decisions.append(decision)

    def add_action_item(self, action: SopActionItem):
        """Record an action item"""
        self.action_items.append(action)

    def approve_plan(self, plan_data):
        """Approve the S&OP plan"""
        self.approved_plan = {
            'approval_date': self.meeting_date,
            'plan': plan_data,
            'status': 'approved'
        }

    def generate_meeting_minutes(self):
        """Create meeting minutes document"""

        minutes = {
            'meeting_date': self.meeting_date,
            'decisions_count': len(self.decisions),
            'action_items_count': len(self.action_items),
            'decisions': [
                {
                    'id': d.decision_id,
                    'decision': d.decision_text,
                    'owner': d.owner,
                    'impact': d.financial_impact
                }
                for d in self.decisions
            ],
            'action_items': [
                {
                    'id': a.action_id,
                    'action': a.description,
                    'owner': a.owner,
                    'due': a.due_date,
                    'priority': a.priority
                }
                for a in self.action_items
            ]
        }

        return minutes

    def get_decision_summary(self):
        """Summarize decisions by category"""

        if not self.decisions:
            return pd.DataFrame()

        decisions_df = pd.DataFrame([
            {
                'category': d.category,
                'status': d.status,
                'financial_impact': d.financial_impact
            }
            for d in self.decisions
        ])

        summary = decisions_df.groupby(['category', 'status']).agg({
            'financial_impact': 'sum'
        }).reset_index()

        return summary

# Example
exec_sop = ExecutiveSopMeeting(meeting_date=datetime(2025, 1, 15))

# Record decisions
exec_sop.add_decision(SopDecision(
    decision_id='DEC-001',
    decision_text='Approve demand plan for Q1 with 11K units for Electronics',
    category='demand',
    owner='VP Sales',
    due_date=datetime(2025, 1, 31),
    status='approved',
    rationale='Aligned with new product launch plan',
    financial_impact=0
))

exec_sop.add_decision(SopDecision(
    decision_id='DEC-002',
    decision_text='Authorize overtime to cover Jan capacity gap',
    category='supply',
    owner='VP Operations',
    due_date=datetime(2025, 1, 20),
    status='approved',
    rationale='Most cost-effective option, $150K vs $220K outsourcing',
    financial_impact=-150000
))

exec_sop.add_decision(SopDecision(
    decision_id='DEC-003',
    decision_text='Approve $3.5M investment for new production line',
    category='strategic',
    owner='CFO',
    due_date=datetime(2025, 6, 30),
    status='approved',
    rationale='Required to support Q3 demand growth',
    financial_impact=-3500000
))

# Add action items
exec_sop.add_action_item(SopActionItem(
    action_id='ACT-001',
    description='Finalize contract with overtime labor agency',
    owner='HR Director',
    due_date=datetime(2025, 1, 20),
    status='open',
    priority='high'
))

exec_sop.add_action_item(SopActionItem(
    action_id='ACT-002',
    description='Complete business case for production line investment',
    owner='VP Operations',
    due_date=datetime(2025, 2, 15),
    status='in_progress',
    priority='high'
))

# Generate minutes
minutes = exec_sop.generate_meeting_minutes()
print("S&OP Meeting Minutes:")
print(f"Date: {minutes['meeting_date']}")
print(f"Decisions: {minutes['decisions_count']}")
print(f"Action Items: {minutes['action_items_count']}")

# Decision summary
decision_summary = exec_sop.get_decision_summary()
print("\nDecisions by Category:")
print(decision_summary)
```

---

## S&OP Maturity Model

### Level 1: Reactive (Ad Hoc)

**Characteristics:**
- No formal S&OP process
- Excel-based, manual
- Sales and Ops don't communicate
- Fire-fighting mode

**Symptoms:**
- Frequent expediting
- Poor forecast accuracy (<60%)
- Excess inventory or stockouts
- Missed commitments

### Level 2: Rudimentary

**Characteristics:**
- Monthly S&OP meetings started
- Some cross-functional participation
- Focus on short-term (1-3 months)
- Limited data integration

**Capabilities:**
- Basic demand review
- Capacity check
- Executive awareness

### Level 3: Standard

**Characteristics:**
- Structured 5-step process
- 12-18 month horizon
- Good data integration
- Regular cadence

**Capabilities:**
- Consensus forecasting
- Capacity planning
- Financial reconciliation
- Scenario analysis

### Level 4: Advanced

**Characteristics:**
- Integrated Business Planning (IBP)
- 24+ month horizon
- Strategic alignment
- Real-time updates

**Capabilities:**
- Portfolio management
- Profitability optimization
- What-if simulation
- Automated analytics

### Level 5: Proactive/Best-in-Class

**Characteristics:**
- Predictive and prescriptive
- AI/ML-driven insights
- Dynamic planning
- Value chain collaboration

**Capabilities:**
- Predictive analytics
- Optimization algorithms
- Digital twin modeling
- External collaboration (suppliers, customers)

---

## S&OP Metrics & KPIs

### Forecast Accuracy

**MAPE (Mean Absolute Percentage Error)**
- Target: <20% for aggregate, <30% for detailed
- Measured monthly by product family
- Track trend over time

**Bias**
- Target: ±5%
- Positive bias = over-forecasting
- Negative bias = under-forecasting

**Forecast Value Added (FVA)**
- Does manual override improve accuracy?
- Measure statistical vs. consensus performance

### Supply Performance

**Plan Attainment**
- % of production plan achieved
- Target: >95%

**Capacity Utilization**
- % of capacity used
- Target: 80-90% (allows flexibility)

**Supply Flexibility**
- Lead time to adjust capacity
- % changeover time

### Inventory Metrics

**Inventory Turns**
- COGS / Average Inventory
- Target: Industry-dependent (6-12 turns typical)

**Days of Supply**
- Inventory / Daily Sales
- Target: 30-60 days

**Inventory Accuracy**
- % of SKUs within tolerance
- Target: >95%

### Financial Metrics

**Revenue Plan Attainment**
- Actual revenue / plan
- Target: 95-105%

**Gross Margin**
- % margin vs. plan
- Track variance drivers

**Working Capital**
- Cash tied up in inventory
- Optimize cash-to-cash cycle

### Process Metrics

**Meeting Effectiveness**
- % decisions made on time
- Action item completion rate
- Participant engagement scores

**Cycle Time**
- Time from data gathering to decision
- Target: <4 weeks

**Plan Stability**
- How often plan changes
- Nervousness metric

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SopMetrics:
    """S&OP performance metrics tracking"""

    def __init__(self):
        self.metrics_history = []

    def calculate_monthly_metrics(self, actual_data, plan_data):
        """
        Calculate S&OP metrics for a month

        Parameters:
        - actual_data: actual performance
        - plan_data: planned performance
        """

        # Forecast accuracy (MAPE)
        mape = np.mean(
            np.abs((actual_data['demand'] - plan_data['forecast']) /
                   actual_data['demand'])
        ) * 100

        # Bias
        bias = np.mean(plan_data['forecast'] - actual_data['demand'])
        bias_pct = (bias / np.mean(actual_data['demand'])) * 100

        # Plan attainment
        plan_attainment = (
            actual_data['production'].sum() / plan_data['production_plan'].sum()
        ) * 100

        # Inventory metrics
        inventory_turns = (
            actual_data['cogs'].sum() /
            actual_data['avg_inventory'].mean()
        )

        days_of_supply = (
            actual_data['ending_inventory'].iloc[-1] /
            (actual_data['demand'].sum() / 30)
        )

        # Revenue attainment
        revenue_attainment = (
            actual_data['revenue'].sum() / plan_data['revenue_plan'].sum()
        ) * 100

        metrics = {
            'period': actual_data['period'].iloc[0],
            'mape': mape,
            'bias_pct': bias_pct,
            'plan_attainment': plan_attainment,
            'inventory_turns': inventory_turns,
            'days_of_supply': days_of_supply,
            'revenue_attainment': revenue_attainment
        }

        self.metrics_history.append(metrics)

        return metrics

    def plot_metrics_dashboard(self):
        """Create S&OP metrics dashboard"""

        if not self.metrics_history:
            return None

        df = pd.DataFrame(self.metrics_history)

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('S&OP Performance Dashboard', fontsize=16, fontweight='bold')

        # MAPE
        axes[0, 0].plot(df['period'], df['mape'], marker='o', linewidth=2)
        axes[0, 0].axhline(y=20, color='r', linestyle='--', label='Target')
        axes[0, 0].set_title('Forecast Accuracy (MAPE)')
        axes[0, 0].set_ylabel('MAPE (%)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Bias
        axes[0, 1].plot(df['period'], df['bias_pct'], marker='o', linewidth=2, color='orange')
        axes[0, 1].axhline(y=5, color='r', linestyle='--', alpha=0.5)
        axes[0, 1].axhline(y=-5, color='r', linestyle='--', alpha=0.5)
        axes[0, 1].set_title('Forecast Bias')
        axes[0, 1].set_ylabel('Bias (%)')
        axes[0, 1].grid(True, alpha=0.3)

        # Plan Attainment
        axes[0, 2].plot(df['period'], df['plan_attainment'], marker='o', linewidth=2, color='green')
        axes[0, 2].axhline(y=95, color='r', linestyle='--', label='Min Target')
        axes[0, 2].axhline(y=105, color='r', linestyle='--')
        axes[0, 2].set_title('Plan Attainment')
        axes[0, 2].set_ylabel('Attainment (%)')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)

        # Inventory Turns
        axes[1, 0].plot(df['period'], df['inventory_turns'], marker='o', linewidth=2, color='purple')
        axes[1, 0].axhline(y=8, color='g', linestyle='--', label='Target')
        axes[1, 0].set_title('Inventory Turns')
        axes[1, 0].set_ylabel('Turns')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        # Days of Supply
        axes[1, 1].plot(df['period'], df['days_of_supply'], marker='o', linewidth=2, color='brown')
        axes[1, 1].axhline(y=45, color='g', linestyle='--', label='Target')
        axes[1, 1].set_title('Days of Supply')
        axes[1, 1].set_ylabel('Days')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        # Revenue Attainment
        axes[1, 2].plot(df['period'], df['revenue_attainment'], marker='o', linewidth=2, color='red')
        axes[1, 2].axhline(y=95, color='r', linestyle='--', alpha=0.5)
        axes[1, 2].axhline(y=105, color='r', linestyle='--', alpha=0.5)
        axes[1, 2].axhspan(95, 105, alpha=0.2, color='green')
        axes[1, 2].set_title('Revenue Attainment')
        axes[1, 2].set_ylabel('Attainment (%)')
        axes[1, 2].grid(True, alpha=0.3)

        plt.tight_layout()

        return fig

# Example
metrics = SopMetrics()

# Simulate 6 months of data
for month in range(1, 7):
    actual = pd.DataFrame({
        'period': [f'2025-{month:02d}'],
        'demand': [10000 + np.random.randint(-500, 500)],
        'production': [10000 + np.random.randint(-300, 300)],
        'revenue': [1000000 + np.random.randint(-50000, 50000)],
        'cogs': [600000],
        'avg_inventory': [500000],
        'ending_inventory': [400000]
    })

    plan = pd.DataFrame({
        'forecast': [10000],
        'production_plan': [10000],
        'revenue_plan': [1000000]
    })

    monthly_metrics = metrics.calculate_monthly_metrics(actual, plan)
    print(f"Month {month} Metrics: MAPE={monthly_metrics['mape']:.1f}%")

# Plot dashboard
metrics.plot_metrics_dashboard()
```

---

## Tools & Libraries

### Python Libraries

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scipy`: Statistical analysis

**Optimization:**
- `pulp`: Linear programming
- `pyomo`: Advanced optimization

**Visualization:**
- `matplotlib`, `seaborn`: Charts
- `plotly`: Interactive dashboards
- `dash`: Web applications

### Commercial S&OP Software

**Enterprise Platforms:**
- **Kinaxis RapidResponse**: Leading S&OP/IBP platform
- **o9 Solutions**: AI-powered digital platform
- **SAP IBP**: Integrated Business Planning
- **Oracle Cloud Supply Chain Planning**: S&OP modules
- **Blue Yonder**: S&OP and demand-supply matching
- **Anaplan**: Connected planning platform
- **Logility**: Supply chain planning suite

**Collaboration Tools:**
- **Microsoft Teams**: Meeting and collaboration
- **Slack**: Async communication
- **Miro / Mural**: Virtual whiteboarding
- **Power BI / Tableau**: Visualization

### Excel / Google Sheets

Still widely used for S&OP in mid-size companies:
- Planning templates
- Scenario modeling
- Financial reconciliation
- Executive dashboards

---

## Common Challenges & Solutions

### Challenge: Poor Cross-Functional Collaboration

**Problem:**
- Silos between Sales and Operations
- Finger-pointing and blame
- Low meeting engagement

**Solutions:**
- Executive sponsorship and accountability
- Clear roles and responsibilities (RACI)
- Shared metrics and incentives
- Trust-building activities
- Professional facilitation

### Challenge: Data Quality and Integration

**Problem:**
- Multiple sources of truth
- Manual data gathering
- Errors and inconsistencies
- Time-consuming preparation

**Solutions:**
- Single integrated system
- Automated data feeds
- Data governance process
- Master data management
- Exception-based review

### Challenge: Short-Term Focus

**Problem:**
- Only look 1-3 months ahead
- Reactive vs. proactive
- Miss strategic issues

**Solutions:**
- Extend horizon to 18-24 months
- Monthly rolling forecasts
- Quarterly strategic reviews
- Long-term capacity planning
- New product integration

### Challenge: Meeting Overload

**Problem:**
- Too many meetings
- Repetitive discussions
- Decision fatigue

**Solutions:**
- Streamline to 5-step process
- Pre-work and preparation
- Clear agendas and time limits
- Delegate tactical decisions
- Exception-based reviews

### Challenge: Lack of Executive Engagement

**Problem:**
- Executives skip meetings
- Rubber-stamp decisions
- Don't see value

**Solutions:**
- Right level of detail (strategic, not tactical)
- Clear decision needs
- Show business impact
- Tie to financial results
- Success stories and wins

---

## Output Format

### S&OP Report Structure

**Executive Dashboard (1 page):**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Forecast Accuracy (MAPE) | 18.5% | <20% | ✓ |
| Plan Attainment | 96% | >95% | ✓ |
| Inventory Turns | 7.2 | 8.0 | ⚠ |
| Revenue Attainment | 102% | 95-105% | ✓ |

**Demand Plan by Product Family:**

| Family | Jan | Feb | Mar | Q1 Total | vs. Last Month | vs. Last Year |
|--------|-----|-----|-----|----------|----------------|---------------|
| Electronics | 11,000 | 10,200 | 10,500 | 31,700 | +5% | +12% |
| Appliances | 4,500 | 4,800 | 5,000 | 14,300 | +2% | +8% |

**Supply Plan & Constraints:**

| Family | Demand | Capacity | Gap | Status | Solution |
|--------|--------|----------|-----|--------|----------|
| Electronics | 11,000 | 10,000 | (1,000) | Constrained | Overtime approved |
| Appliances | 4,500 | 5,000 | +500 | OK | Normal production |

**Financial Summary:**

| Metric | This Month | Next Month | Q1 Plan |
|--------|-----------|------------|---------|
| Revenue | $1.5M | $1.4M | $4.3M |
| COGS | $0.9M | $0.85M | $2.6M |
| Gross Margin % | 40% | 39% | 39.5% |
| Inventory Value | $5.2M | $5.0M | $5.0M |

**Decisions Made:**
1. Approve Q1 demand plan with noted assumptions
2. Authorize overtime for Electronics in January
3. Proceed with capacity expansion business case
4. Review appliance pricing strategy by March

**Action Items:**
- Finalize contract with overtime agency (HR, Jan 20)
- Complete expansion business case (Ops, Feb 15)
- Pricing analysis for appliances (Marketing, Mar 1)

---

## Questions to Ask

If you need more context:
1. What's the current S&OP process maturity level?
2. Who participates in S&OP currently?
3. What's the planning horizon? (months ahead)
4. What systems/tools are used?
5. What are the biggest challenges or pain points?
6. Who owns the S&OP process?
7. How are forecasts created today?
8. What decisions typically need to be made?

---

## Related Skills

- **demand-forecasting**: For demand planning input to S&OP
- **capacity-planning**: For supply capacity analysis
- **master-production-scheduling**: For detailed execution
- **scenario-planning**: For risk analysis and alternatives
- **inventory-optimization**: For inventory strategy
- **supply-chain-analytics**: For metrics and KPIs
- **network-design**: For strategic network decisions
- **financial-planning**: For financial reconciliation
