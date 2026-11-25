---
name: supplier-risk-management
description: When the user wants to assess supplier risks, monitor supplier health, or develop risk mitigation strategies. Also use when the user mentions "supplier risk assessment," "supply chain risk," "business continuity," "supplier monitoring," "supply disruption," "risk scoring," "supplier financial health," or "contingency planning." For initial supplier selection, see supplier-selection. For overall supply chain risk, see risk-mitigation.
---

# Supplier Risk Management

You are an expert in supplier risk management and business continuity planning. Your goal is to help organizations identify, assess, monitor, and mitigate supplier-related risks to ensure supply chain resilience and continuity.

## Initial Assessment

Before implementing supplier risk management, understand:

1. **Risk Management Context**
   - What's driving risk management focus? (disruption, compliance, audit)
   - Current risk management maturity?
   - Recent supply disruptions or issues?
   - Industry-specific risks?

2. **Supplier Portfolio**
   - How many active suppliers?
   - Critical vs. non-critical suppliers?
   - Single-source dependencies?
   - Geographic concentration?

3. **Risk Appetite**
   - Risk tolerance levels?
   - Business impact thresholds?
   - Insurance coverage?
   - Contingency budget?

4. **Monitoring Capabilities**
   - Current monitoring processes?
   - Available risk data sources?
   - Systems and tools in place?
   - Resources for risk management?

---

## Supplier Risk Framework

### Risk Categories

**1. Financial Risk**
- Bankruptcy or insolvency
- Credit rating downgrades
- Cash flow problems
- Acquisition or ownership changes
- Loan defaults

**2. Operational Risk**
- Capacity constraints
- Quality failures
- Technology obsolescence
- Process breakdowns
- Labor strikes or shortages
- Natural disasters at facilities

**3. Geopolitical Risk**
- Political instability
- Trade restrictions and tariffs
- Sanctions
- Border closures
- Currency volatility
- Regulatory changes

**4. Cybersecurity Risk**
- Data breaches
- Ransomware attacks
- System outages
- IP theft
- Supply chain attacks

**5. Compliance Risk**
- Regulatory violations
- Safety incidents
- Environmental non-compliance
- Ethics violations
- Corruption or fraud
- Forced labor concerns

**6. Reputational Risk**
- Negative publicity
- Social media crises
- Product recalls
- ESG controversies
- Association with bad actors

**7. Concentration Risk**
- Single-source dependencies
- Geographic concentration
- Over-reliance on one supplier
- Supplier of supplier risks (N-tier)

---

## Risk Assessment Methodology

### Comprehensive Risk Scoring Model

```python
import pandas as pd
import numpy as np

class SupplierRiskAssessment:
    """Comprehensive supplier risk assessment framework"""

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name
        self.risk_scores = {}
        self.weights = {
            'financial': 0.25,
            'operational': 0.25,
            'geopolitical': 0.15,
            'compliance': 0.15,
            'quality': 0.10,
            'cybersecurity': 0.10
        }

    def assess_financial_risk(self, financial_data):
        """
        Assess financial risk (0-100, higher = riskier)

        financial_data: dict with financial metrics
        """
        score = 0
        factors = []

        # Credit rating
        credit_rating = financial_data.get('credit_rating', 'BB')
        rating_scores = {
            'AAA': 0, 'AA': 5, 'A': 10, 'BBB': 20,
            'BB': 40, 'B': 60, 'CCC': 80, 'CC': 90, 'D': 100
        }
        rating_score = rating_scores.get(credit_rating, 50)
        score += rating_score * 0.3

        if rating_score >= 40:
            factors.append(f"Poor credit rating ({credit_rating})")

        # Years in business
        years = financial_data.get('years_in_business', 10)
        if years < 3:
            score += 20
            factors.append("Limited operating history")
        elif years < 5:
            score += 10

        # Revenue trend
        revenue_growth = financial_data.get('revenue_growth_3yr', 0)
        if revenue_growth < -0.15:
            score += 15
            factors.append("Significant revenue decline")
        elif revenue_growth < 0:
            score += 8

        # Profitability
        ebitda_margin = financial_data.get('ebitda_margin', 0.1)
        if ebitda_margin < 0:
            score += 15
            factors.append("Unprofitable operations")
        elif ebitda_margin < 0.05:
            score += 8

        # Liquidity
        current_ratio = financial_data.get('current_ratio', 1.5)
        if current_ratio < 1.0:
            score += 15
            factors.append("Liquidity crisis")
        elif current_ratio < 1.2:
            score += 8

        # Leverage
        debt_to_equity = financial_data.get('debt_to_equity', 1.0)
        if debt_to_equity > 3.0:
            score += 15
            factors.append("Excessive leverage")
        elif debt_to_equity > 2.0:
            score += 8

        self.risk_scores['financial'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['financial']

    def assess_operational_risk(self, operational_data):
        """Assess operational risk"""
        score = 0
        factors = []

        # Capacity utilization
        capacity_util = operational_data.get('capacity_utilization', 0.75)
        if capacity_util > 0.95:
            score += 20
            factors.append("Critical capacity constraints")
        elif capacity_util > 0.85:
            score += 10

        # Single facility risk
        num_facilities = operational_data.get('num_facilities', 2)
        if num_facilities == 1:
            score += 15
            factors.append("Single facility risk")

        # Technology age
        tech_age_years = operational_data.get('technology_age_years', 5)
        if tech_age_years > 15:
            score += 10
            factors.append("Outdated technology")

        # Workforce stability
        employee_turnover = operational_data.get('employee_turnover', 0.15)
        if employee_turnover > 0.30:
            score += 15
            factors.append("High workforce turnover")
        elif employee_turnover > 0.20:
            score += 8

        # Recent disruptions
        disruptions_12mo = operational_data.get('disruptions_last_12mo', 0)
        if disruptions_12mo > 2:
            score += 20
            factors.append("Frequent operational disruptions")
        elif disruptions_12mo > 0:
            score += 10

        # Quality performance
        defect_ppm = operational_data.get('defect_rate_ppm', 500)
        if defect_ppm > 2000:
            score += 15
            factors.append("Quality issues")
        elif defect_ppm > 1000:
            score += 8

        self.risk_scores['operational'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['operational']

    def assess_geopolitical_risk(self, geo_data):
        """Assess geopolitical risk"""
        score = 0
        factors = []

        # Country risk
        country_risk_index = geo_data.get('country_risk_index', 50)  # 0-100
        score += country_risk_index * 0.4

        if country_risk_index > 70:
            factors.append("High-risk country location")

        # Trade restrictions
        if geo_data.get('trade_restrictions', False):
            score += 20
            factors.append("Active trade restrictions")

        # Currency volatility
        currency_volatility = geo_data.get('currency_volatility_12mo', 0.05)
        if currency_volatility > 0.20:
            score += 15
            factors.append("High currency volatility")
        elif currency_volatility > 0.10:
            score += 8

        # Political stability
        political_stability = geo_data.get('political_stability', 7)  # 0-10
        if political_stability < 4:
            score += 15
            factors.append("Political instability")

        # Border distance/complexity
        if geo_data.get('cross_border', False):
            score += 5
            if geo_data.get('multiple_borders', False):
                score += 5
                factors.append("Complex cross-border logistics")

        self.risk_scores['geopolitical'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['geopolitical']

    def assess_compliance_risk(self, compliance_data):
        """Assess compliance and regulatory risk"""
        score = 0
        factors = []

        # Certifications
        required_certs = compliance_data.get('required_certifications', [])
        actual_certs = compliance_data.get('actual_certifications', [])
        missing_certs = set(required_certs) - set(actual_certs)

        if missing_certs:
            score += 20
            factors.append(f"Missing certifications: {', '.join(missing_certs)}")

        # Recent violations
        violations_3yr = compliance_data.get('violations_last_3yr', 0)
        if violations_3yr > 2:
            score += 25
            factors.append("Multiple compliance violations")
        elif violations_3yr > 0:
            score += 12

        # Audit results
        last_audit_score = compliance_data.get('last_audit_score', 85)  # 0-100
        if last_audit_score < 70:
            score += 20
            factors.append("Failed recent audit")
        elif last_audit_score < 80:
            score += 10

        # Environmental incidents
        if compliance_data.get('environmental_incidents', 0) > 0:
            score += 15
            factors.append("Environmental incidents")

        # Labor concerns
        if compliance_data.get('labor_concerns', False):
            score += 20
            factors.append("Labor or human rights concerns")

        self.risk_scores['compliance'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['compliance']

    def assess_quality_risk(self, quality_data):
        """Assess quality risk"""
        score = 0
        factors = []

        # Defect rate
        defect_ppm = quality_data.get('defect_rate_ppm', 500)
        if defect_ppm > 2000:
            score += 30
            factors.append("High defect rate")
        elif defect_ppm > 1000:
            score += 15

        # Quality certifications
        if not quality_data.get('iso_9001', False):
            score += 10
            factors.append("No ISO 9001 certification")

        # Recent recalls
        recalls_3yr = quality_data.get('recalls_last_3yr', 0)
        if recalls_3yr > 0:
            score += 25 * recalls_3yr
            factors.append(f"{recalls_3yr} product recalls")

        # Customer complaints
        complaints = quality_data.get('customer_complaints_per_1000', 5)
        if complaints > 20:
            score += 20
            factors.append("High customer complaint rate")
        elif complaints > 10:
            score += 10

        # Corrective actions
        open_corrective_actions = quality_data.get('open_corrective_actions', 0)
        if open_corrective_actions > 5:
            score += 15
            factors.append("Multiple open corrective actions")

        self.risk_scores['quality'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['quality']

    def assess_cybersecurity_risk(self, cyber_data):
        """Assess cybersecurity risk"""
        score = 0
        factors = []

        # Security certifications
        if not cyber_data.get('iso_27001', False):
            score += 15
            factors.append("No ISO 27001 certification")

        # Recent breaches
        breaches_3yr = cyber_data.get('breaches_last_3yr', 0)
        if breaches_3yr > 0:
            score += 30 * breaches_3yr
            factors.append(f"{breaches_3yr} security breaches")

        # Security maturity
        security_maturity = cyber_data.get('security_maturity', 3)  # 1-5
        if security_maturity < 2:
            score += 25
            factors.append("Immature cybersecurity practices")
        elif security_maturity < 3:
            score += 12

        # Third-party access
        if cyber_data.get('network_integration', False):
            score += 10
            if not cyber_data.get('secure_access_controls', False):
                score += 10
                factors.append("Inadequate access controls")

        # Incident response
        if not cyber_data.get('incident_response_plan', False):
            score += 10
            factors.append("No incident response plan")

        self.risk_scores['cybersecurity'] = {
            'score': min(100, score),
            'factors': factors
        }
        return self.risk_scores['cybersecurity']

    def calculate_overall_risk(self):
        """Calculate weighted overall risk score"""

        if not self.risk_scores:
            return None

        overall_score = sum(
            self.risk_scores[category]['score'] * weight
            for category, weight in self.weights.items()
            if category in self.risk_scores
        )

        # Classify risk level
        if overall_score < 25:
            risk_level = 'Low'
            action = 'Monitor periodically'
        elif overall_score < 50:
            risk_level = 'Medium'
            action = 'Monitor regularly, develop contingency'
        elif overall_score < 75:
            risk_level = 'High'
            action = 'Active mitigation required'
        else:
            risk_level = 'Critical'
            action = 'Immediate action, consider alternate supplier'

        # Collect all factors
        all_factors = []
        for category, data in self.risk_scores.items():
            for factor in data['factors']:
                all_factors.append(f"{category.capitalize()}: {factor}")

        return {
            'supplier': self.supplier_name,
            'overall_score': round(overall_score, 1),
            'risk_level': risk_level,
            'recommended_action': action,
            'category_scores': {
                cat: data['score']
                for cat, data in self.risk_scores.items()
            },
            'risk_factors': all_factors
        }


# Example usage
supplier = SupplierRiskAssessment('Acme Manufacturing Inc.')

# Assess each risk category
supplier.assess_financial_risk({
    'credit_rating': 'BB',
    'years_in_business': 8,
    'revenue_growth_3yr': -0.05,
    'ebitda_margin': 0.08,
    'current_ratio': 1.3,
    'debt_to_equity': 2.2
})

supplier.assess_operational_risk({
    'capacity_utilization': 0.88,
    'num_facilities': 2,
    'technology_age_years': 8,
    'employee_turnover': 0.18,
    'disruptions_last_12mo': 1,
    'defect_rate_ppm': 800
})

supplier.assess_geopolitical_risk({
    'country_risk_index': 35,
    'trade_restrictions': False,
    'currency_volatility_12mo': 0.08,
    'political_stability': 7,
    'cross_border': True,
    'multiple_borders': False
})

supplier.assess_compliance_risk({
    'required_certifications': ['ISO9001', 'ISO14001'],
    'actual_certifications': ['ISO9001'],
    'violations_last_3yr': 0,
    'last_audit_score': 85,
    'environmental_incidents': 0,
    'labor_concerns': False
})

supplier.assess_quality_risk({
    'defect_rate_ppm': 800,
    'iso_9001': True,
    'recalls_last_3yr': 0,
    'customer_complaints_per_1000': 8,
    'open_corrective_actions': 2
})

supplier.assess_cybersecurity_risk({
    'iso_27001': False,
    'breaches_last_3yr': 0,
    'security_maturity': 3,
    'network_integration': True,
    'secure_access_controls': True,
    'incident_response_plan': True
})

result = supplier.calculate_overall_risk()

print(f"Supplier: {result['supplier']}")
print(f"Overall Risk Score: {result['overall_score']}/100")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommended Action: {result['recommended_action']}")
print("\nCategory Scores:")
for cat, score in result['category_scores'].items():
    print(f"  {cat.capitalize()}: {score}/100")
```

---

## Business Impact Assessment

### Criticality Analysis

```python
def assess_supplier_criticality(supplier_data):
    """
    Determine supplier criticality to business

    Returns: criticality score (0-100) and tier classification
    """

    criticality_score = 0

    # Spend volume
    annual_spend = supplier_data.get('annual_spend', 0)
    if annual_spend > 10000000:  # >$10M
        criticality_score += 20
    elif annual_spend > 1000000:  # >$1M
        criticality_score += 15
    elif annual_spend > 100000:  # >$100K
        criticality_score += 10

    # Replaceability
    substitute_availability = supplier_data.get('substitute_availability', 'high')
    if substitute_availability == 'none':
        criticality_score += 30
    elif substitute_availability == 'low':
        criticality_score += 20
    elif substitute_availability == 'medium':
        criticality_score += 10

    # Lead time to replace
    replacement_time_weeks = supplier_data.get('replacement_time_weeks', 12)
    if replacement_time_weeks > 26:  # >6 months
        criticality_score += 20
    elif replacement_time_weeks > 12:  # >3 months
        criticality_score += 15
    elif replacement_time_weeks > 4:  # >1 month
        criticality_score += 10

    # Business impact
    revenue_at_risk = supplier_data.get('revenue_at_risk', 0)
    if revenue_at_risk > 50000000:  # >$50M
        criticality_score += 20
    elif revenue_at_risk > 10000000:  # >$10M
        criticality_score += 15
    elif revenue_at_risk > 1000000:  # >$1M
        criticality_score += 10

    # Customer impact
    customers_affected = supplier_data.get('customers_affected', 'none')
    if customers_affected == 'critical':
        criticality_score += 10
    elif customers_affected == 'major':
        criticality_score += 7

    # Classify tier
    if criticality_score >= 70:
        tier = 'Tier 1 - Critical'
        monitoring_frequency = 'Weekly'
    elif criticality_score >= 50:
        tier = 'Tier 2 - Important'
        monitoring_frequency = 'Monthly'
    elif criticality_score >= 30:
        tier = 'Tier 3 - Standard'
        monitoring_frequency = 'Quarterly'
    else:
        tier = 'Tier 4 - Low Impact'
        monitoring_frequency = 'Annual'

    return {
        'criticality_score': criticality_score,
        'tier': tier,
        'monitoring_frequency': monitoring_frequency
    }
```

### Risk Exposure Matrix

**Risk Score × Criticality Score = Exposure**

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_risk_exposure_matrix(suppliers_df):
    """
    Create risk exposure matrix (bubble chart)

    suppliers_df: DataFrame with risk_score, criticality_score, spend
    """

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter plot
    scatter = ax.scatter(
        suppliers_df['criticality_score'],
        suppliers_df['risk_score'],
        s=suppliers_df['spend'] / 10000,  # Bubble size by spend
        alpha=0.6,
        c=suppliers_df['risk_score'],
        cmap='RdYlGn_r'
    )

    # Add supplier labels
    for idx, row in suppliers_df.iterrows():
        ax.annotate(
            row['supplier_name'],
            (row['criticality_score'], row['risk_score']),
            fontsize=8
        )

    # Quadrant lines
    ax.axvline(50, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(50, color='gray', linestyle='--', alpha=0.5)

    # Quadrant labels
    ax.text(75, 75, 'High Risk\nHigh Criticality\nACT NOW', ha='center', fontsize=10, weight='bold', color='red')
    ax.text(25, 75, 'High Risk\nLow Criticality\nMONITOR', ha='center', fontsize=10)
    ax.text(75, 25, 'Low Risk\nHigh Criticality\nPROTECT', ha='center', fontsize=10)
    ax.text(25, 25, 'Low Risk\nLow Criticality\nROUTINE', ha='center', fontsize=10)

    ax.set_xlabel('Criticality Score', fontsize=12)
    ax.set_ylabel('Risk Score', fontsize=12)
    ax.set_title('Supplier Risk Exposure Matrix', fontsize=14, weight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    plt.colorbar(scatter, label='Risk Score')
    plt.tight_layout()

    return fig
```

---

## Risk Monitoring & Early Warning

### Key Risk Indicators (KRIs)

**Financial KRIs:**
- Credit rating changes
- Stock price volatility (public companies)
- Days payable outstanding (DPO) increases
- Debt covenant violations
- Bankruptcy filings in industry

**Operational KRIs:**
- On-time delivery decline
- Quality defect rate increases
- Lead time extensions
- Capacity utilization spikes
- Employee layoffs or strikes

**External KRIs:**
- Natural disasters in supplier regions
- Political events (elections, coups)
- Regulatory changes
- Cyber attacks in industry
- Pandemic or health alerts

```python
class RiskMonitoringSystem:
    """Automated risk monitoring and alerting"""

    def __init__(self):
        self.kris = {}
        self.thresholds = {}
        self.alerts = []

    def add_kri(self, kri_name, current_value, threshold, direction='above'):
        """
        Add Key Risk Indicator

        direction: 'above' (alert if above threshold) or 'below'
        """
        self.kris[kri_name] = current_value
        self.thresholds[kri_name] = {
            'value': threshold,
            'direction': direction
        }

    def check_alerts(self):
        """Check all KRIs against thresholds"""
        self.alerts = []

        for kri, value in self.kris.items():
            threshold = self.thresholds[kri]

            if threshold['direction'] == 'above':
                if value > threshold['value']:
                    severity = self._calculate_severity(value, threshold['value'], 'above')
                    self.alerts.append({
                        'kri': kri,
                        'current_value': value,
                        'threshold': threshold['value'],
                        'severity': severity,
                        'direction': 'exceeded'
                    })

            elif threshold['direction'] == 'below':
                if value < threshold['value']:
                    severity = self._calculate_severity(value, threshold['value'], 'below')
                    self.alerts.append({
                        'kri': kri,
                        'current_value': value,
                        'threshold': threshold['value'],
                        'severity': severity,
                        'direction': 'fell below'
                    })

        return self.alerts

    def _calculate_severity(self, current, threshold, direction):
        """Calculate alert severity"""
        if direction == 'above':
            pct_over = (current - threshold) / threshold
            if pct_over > 0.50:
                return 'Critical'
            elif pct_over > 0.25:
                return 'High'
            elif pct_over > 0.10:
                return 'Medium'
            else:
                return 'Low'
        else:  # below
            pct_under = (threshold - current) / threshold
            if pct_under > 0.50:
                return 'Critical'
            elif pct_under > 0.25:
                return 'High'
            elif pct_under > 0.10:
                return 'Medium'
            else:
                return 'Low'

    def generate_alert_report(self):
        """Generate formatted alert report"""
        if not self.alerts:
            return "No alerts triggered."

        report = ["=" * 60]
        report.append("SUPPLIER RISK ALERTS")
        report.append("=" * 60)
        report.append("")

        # Sort by severity
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        sorted_alerts = sorted(
            self.alerts,
            key=lambda x: severity_order[x['severity']]
        )

        for alert in sorted_alerts:
            report.append(f"[{alert['severity'].upper()}] {alert['kri']}")
            report.append(f"  Current: {alert['current_value']:.2f}")
            report.append(f"  Threshold: {alert['threshold']:.2f}")
            report.append(f"  Status: {alert['direction']}")
            report.append("")

        return "\n".join(report)


# Example
monitor = RiskMonitoringSystem()

# Add KRIs for a supplier
monitor.add_kri('defect_rate_ppm', 1500, 1000, direction='above')
monitor.add_kri('on_time_delivery_%', 88, 95, direction='below')
monitor.add_kri('lead_time_days', 28, 21, direction='above')
monitor.add_kri('capacity_utilization_%', 96, 90, direction='above')
monitor.add_kri('credit_score', 65, 70, direction='below')

# Check for alerts
alerts = monitor.check_alerts()

print(monitor.generate_alert_report())
```

---

## Risk Mitigation Strategies

### Mitigation Options by Risk Level

**For Critical Risk (Score >75):**
1. Dual sourcing immediately
2. Build safety stock (3-6 months)
3. Qualify backup supplier
4. Escalate to executive level
5. Consider insourcing or acquisition

**For High Risk (Score 50-75):**
1. Develop contingency plan
2. Increase monitoring frequency
3. Negotiate exit clauses
4. Identify alternate suppliers
5. Build buffer inventory (1-3 months)

**For Medium Risk (Score 25-50):**
1. Regular performance reviews
2. Request improvement plans
3. Diversify volume allocation
4. Monitor early warning signals
5. Annual risk reassessment

**For Low Risk (Score <25):**
1. Standard monitoring
2. Periodic audits
3. Maintain relationship
4. Focus on optimization

### Contingency Planning

```python
class ContingencyPlan:
    """Business continuity planning for supplier disruption"""

    def __init__(self, supplier_name, criticality_tier):
        self.supplier_name = supplier_name
        self.criticality_tier = criticality_tier
        self.mitigation_actions = []

    def add_mitigation(self, action, timeline_days, owner, status='Planned'):
        """Add mitigation action"""
        self.mitigation_actions.append({
            'action': action,
            'timeline_days': timeline_days,
            'owner': owner,
            'status': status
        })

    def calculate_recovery_time(self):
        """Estimate recovery time objective (RTO)"""
        if not self.mitigation_actions:
            return float('inf')

        # RTO is the longest timeline among active mitigations
        active_actions = [
            m for m in self.mitigation_actions
            if m['status'] in ['Planned', 'In Progress']
        ]

        if not active_actions:
            return 0

        return max(m['timeline_days'] for m in active_actions)

    def generate_plan_document(self):
        """Generate contingency plan document"""
        doc = []
        doc.append("=" * 70)
        doc.append(f"SUPPLIER CONTINGENCY PLAN: {self.supplier_name}")
        doc.append("=" * 70)
        doc.append(f"Criticality Tier: {self.criticality_tier}")
        doc.append(f"Recovery Time Objective (RTO): {self.calculate_recovery_time()} days")
        doc.append("")
        doc.append("MITIGATION ACTIONS:")
        doc.append("-" * 70)

        for i, action in enumerate(self.mitigation_actions, 1):
            doc.append(f"\n{i}. {action['action']}")
            doc.append(f"   Timeline: {action['timeline_days']} days")
            doc.append(f"   Owner: {action['owner']}")
            doc.append(f"   Status: {action['status']}")

        return "\n".join(doc)


# Example contingency plan
plan = ContingencyPlan('Acme Manufacturing', 'Tier 1 - Critical')

plan.add_mitigation(
    action='Activate backup supplier (XYZ Corp)',
    timeline_days=30,
    owner='Procurement Manager',
    status='Planned'
)

plan.add_mitigation(
    action='Build 60-day safety stock',
    timeline_days=45,
    owner='Supply Chain Manager',
    status='In Progress'
)

plan.add_mitigation(
    action='Expedite supplier qualification for Alternate Supplier',
    timeline_days=60,
    owner='Quality Manager',
    status='Planned'
)

plan.add_mitigation(
    action='Identify insourcing options',
    timeline_days=90,
    owner='Operations Manager',
    status='Planned'
)

print(plan.generate_plan_document())
```

### Dual Sourcing Strategy

```python
def design_dual_sourcing_strategy(primary_supplier, backup_supplier,
                                  annual_demand, disruption_scenarios):
    """
    Design optimal dual sourcing strategy

    disruption_scenarios: list of dicts with 'probability' and 'duration_days'
    """

    # Calculate expected disruption cost
    expected_disruption_days = sum(
        scenario['probability'] * scenario['duration_days']
        for scenario in disruption_scenarios
    )

    # Cost per day of disruption (lost revenue, expedite costs, etc.)
    disruption_cost_per_day = 50000  # Example: $50K/day

    expected_annual_disruption_cost = expected_disruption_days * disruption_cost_per_day

    # Evaluate sourcing strategies
    strategies = []

    # Strategy 1: 100% primary (single source)
    cost_100_0 = (
        annual_demand * primary_supplier['unit_cost'] +
        expected_annual_disruption_cost
    )
    strategies.append({
        'name': '100% Primary (Single Source)',
        'primary_%': 100,
        'backup_%': 0,
        'cost': cost_100_0,
        'risk': 'High'
    })

    # Strategy 2: 80/20 split
    primary_qty_80 = annual_demand * 0.8
    backup_qty_20 = annual_demand * 0.2
    cost_80_20 = (
        primary_qty_80 * primary_supplier['unit_cost'] +
        backup_qty_20 * backup_supplier['unit_cost'] +
        expected_annual_disruption_cost * 0.3  # 70% risk reduction
    )
    strategies.append({
        'name': '80/20 Split',
        'primary_%': 80,
        'backup_%': 20,
        'cost': cost_80_20,
        'risk': 'Medium'
    })

    # Strategy 3: 70/30 split
    primary_qty_70 = annual_demand * 0.7
    backup_qty_30 = annual_demand * 0.3
    cost_70_30 = (
        primary_qty_70 * primary_supplier['unit_cost'] +
        backup_qty_30 * backup_supplier['unit_cost'] +
        expected_annual_disruption_cost * 0.2  # 80% risk reduction
    )
    strategies.append({
        'name': '70/30 Split',
        'primary_%': 70,
        'backup_%': 30,
        'cost': cost_70_30,
        'risk': 'Low'
    })

    # Strategy 4: 50/50 split (full redundancy)
    primary_qty_50 = annual_demand * 0.5
    backup_qty_50 = annual_demand * 0.5
    cost_50_50 = (
        primary_qty_50 * primary_supplier['unit_cost'] +
        backup_qty_50 * backup_supplier['unit_cost'] +
        expected_annual_disruption_cost * 0.1  # 90% risk reduction
    )
    strategies.append({
        'name': '50/50 Split (Full Redundancy)',
        'primary_%': 50,
        'backup_%': 50,
        'cost': cost_50_50,
        'risk': 'Very Low'
    })

    # Find optimal strategy (lowest total cost)
    optimal = min(strategies, key=lambda x: x['cost'])

    return {
        'strategies': strategies,
        'optimal': optimal,
        'savings_vs_single_source': cost_100_0 - optimal['cost']
    }


# Example
primary = {'unit_cost': 10.00}
backup = {'unit_cost': 10.80}

disruption_scenarios = [
    {'probability': 0.10, 'duration_days': 30},   # 10% chance of 30-day disruption
    {'probability': 0.05, 'duration_days': 90},   # 5% chance of 90-day disruption
]

result = design_dual_sourcing_strategy(
    primary, backup, annual_demand=100000, disruption_scenarios=disruption_scenarios
)

print("Dual Sourcing Analysis:")
for strategy in result['strategies']:
    print(f"\n{strategy['name']}")
    print(f"  Split: {strategy['primary_%']}% / {strategy['backup_%']}%")
    print(f"  Total Cost: ${strategy['cost']:,.0f}")
    print(f"  Risk Level: {strategy['risk']}")

print(f"\n\nOptimal Strategy: {result['optimal']['name']}")
print(f"Savings vs Single Source: ${result['savings_vs_single_source']:,.0f}")
```

---

## Tools & Libraries

### Python Libraries

**Risk Analytics:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `scipy`: Statistical analysis
- `scikit-learn`: Predictive risk modeling

**Visualization:**
- `matplotlib`, `seaborn`: Risk charts and dashboards
- `plotly`: Interactive risk visualizations
- `networkx`: Supplier network mapping

**Monitoring:**
- `requests`: API integration for data feeds
- `beautifulsoup4`: Web scraping for news monitoring
- `schedule`: Automated monitoring tasks

### Commercial Software

**Risk Management Platforms:**
- **Resilinc**: Supply chain risk management and monitoring
- **RapidRatings**: Financial health ratings
- **Dun & Bradstreet**: Supplier risk intelligence
- **Everstream Analytics**: AI-powered risk prediction
- **Interos**: Supply chain resilience
- **Exiger**: Third-party risk management

**Supplier Performance:**
- **SAP Ariba**: Supplier management
- **Coupa**: Supplier risk and performance
- **Jaggaer**: Supplier lifecycle management
- **GEP**: Supplier risk assessment

**Business Continuity:**
- **LogicManager**: Integrated risk management
- **Resolver**: Incident and risk management
- **Fusion Framework**: Risk and resilience

---

## Common Challenges & Solutions

### Challenge: Limited Supplier Visibility

**Problem:**
- Lack of real-time data
- Suppliers reluctant to share information
- N-tier visibility (suppliers of suppliers)

**Solutions:**
- Contractual requirements for transparency
- Third-party risk monitoring services
- Supplier audits and site visits
- Industry benchmarking
- Collaborative risk sharing agreements
- Use of technology (IoT, blockchain)

### Challenge: Risk Assessment Subjectivity

**Problem:**
- Inconsistent risk scoring
- Personal biases
- Lack of standardized criteria

**Solutions:**
- Standardized risk assessment framework
- Quantitative metrics where possible
- Multiple evaluators (triangulation)
- Regular calibration sessions
- Automated scoring algorithms
- External validation (audits, ratings)

### Challenge: Alert Fatigue

**Problem:**
- Too many low-priority alerts
- Important signals missed
- Resources overwhelmed

**Solutions:**
- Risk-based prioritization (focus on critical suppliers)
- Threshold tuning (reduce false positives)
- Aggregated reporting (weekly digests)
- Escalation procedures (tiered response)
- Machine learning for anomaly detection

### Challenge: Mitigation Cost Justification

**Problem:**
- Hard to quantify risk savings
- Upfront costs vs. uncertain benefits
- Budget constraints

**Solutions:**
- Expected value analysis (probability × impact)
- Scenario planning (stress testing)
- Historical disruption cost data
- Insurance analogy (risk premium)
- Pilot programs (prove ROI)
- Executive risk workshops

### Challenge: Supplier Resistance

**Problem:**
- Suppliers push back on audits
- Don't want to share financial data
- Offended by risk questioning

**Solutions:**
- Frame as partnership (mutual benefit)
- Phased approach (build trust)
- Reciprocal transparency
- Industry standards compliance
- Contractual obligations
- Incentives for participation

---

## Output Format

### Supplier Risk Report

**Executive Summary:**
- Overall supplier risk portfolio status
- Critical alerts and actions required
- Trend analysis (improving/deteriorating)
- Key recommendations

**Individual Supplier Assessment:**

```
Supplier: Acme Manufacturing Inc.
Risk Tier: HIGH (Score: 62/100)
Criticality: Tier 1 - Critical Supplier

Risk Category Scores:
  Financial:       48/100 (Medium)
  Operational:     65/100 (High)
  Geopolitical:    35/100 (Low)
  Compliance:      25/100 (Low)
  Quality:         45/100 (Medium)
  Cybersecurity:   55/100 (Medium)

Top Risk Factors:
  1. High capacity utilization (>90%)
  2. Single facility operation
  3. Credit rating downgrade (BB)
  4. Missing ISO 27001 certification
  5. Elevated employee turnover

Business Impact:
  Annual Spend:           $5.2M
  Revenue at Risk:        $18M
  Customers Affected:     120 (15 critical accounts)
  Replacement Time:       16 weeks
  Criticality Score:      75/100

Mitigation Actions Required:
  1. [HIGH] Qualify backup supplier within 60 days
  2. [HIGH] Build 90-day safety stock
  3. [MEDIUM] Conduct site visit to assess capacity
  4. [MEDIUM] Request cybersecurity audit
  5. [LOW] Negotiate performance guarantees in contract renewal

Contingency Plan: ACTIVATED
  - Backup supplier identified: XYZ Corp
  - Safety stock build: In Progress (45 days complete)
  - Alternative sourcing: Under evaluation

Next Review: 30 days
```

**Portfolio Risk Dashboard:**

| Supplier | Risk Score | Criticality | Spend | Status | Trend | Action Required |
|----------|------------|-------------|-------|--------|-------|-----------------|
| Acme Mfg | 62 (High) | Tier 1 | $5.2M | ⚠ | ↗ | Dual source |
| Beta Corp | 35 (Medium) | Tier 1 | $3.8M | ✓ | → | Monitor |
| Gamma Inc | 78 (Critical) | Tier 2 | $1.5M | ⚠⚠ | ↗ | Replace |
| Delta Ltd | 22 (Low) | Tier 3 | $0.8M | ✓ | ↘ | None |

---

## Questions to Ask

If you need more context:
1. What suppliers or categories are of concern?
2. Have there been recent supply disruptions?
3. What risk data is currently available?
4. What's the supplier criticality (spend, replaceability, impact)?
5. Are there single-source dependencies?
6. What's the organization's risk tolerance?
7. What monitoring processes are in place?
8. Any industry-specific risks? (geopolitical, regulatory)
9. What's the budget for risk mitigation?
10. Who are the key stakeholders for risk management?

---

## Related Skills

- **supplier-selection**: For vetting suppliers during selection process
- **procurement-optimization**: For optimal sourcing strategies
- **strategic-sourcing**: For category risk management
- **spend-analysis**: For concentration risk analysis
- **contract-management**: For contractual risk protections
- **quality-management**: For supplier quality monitoring
- **risk-mitigation**: For overall supply chain risk strategies
