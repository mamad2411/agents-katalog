---
name: pricing-strategy-advanced
description: SaaS pricing strategies — packaging, metering, experimentation, value-based pricing
triggers: [pricing, SaaS pricing, monetization, pricing strategy, subscription, billing]
---

# SKILL: Pricing Strategy Advanced

## Pricing Models

### Value-Based Pricing
```python
# Price based on customer value, not cost
tiers = {
    "starter": {
        "price": 29,
        "limits": {"users": 5, "projects": 10}
    },
    "professional": {
        "price": 99,
        "limits": {"users": 25, "projects": 100}
    },
    "enterprise": {
        "price": 499,
        "limits": {"users": "unlimited", "projects": "unlimited"}
    }
}
```

### Usage-Based Pricing
```python
# Charge based on consumption
def calculate_bill(usage):
    rates = {
        "api_calls": 0.001,  # $0.001 per API call
        "storage_gb": 0.10,  # $0.10 per GB
        "users": 5.00        # $5 per user
    }
    
    total = (
        usage["api_calls"] * rates["api_calls"] +
        usage["storage_gb"] * rates["storage_gb"] +
        usage["users"] * rates["users"]
    )
    
    return total
```

### Tiered Pricing with Overage
```python
def calculate_with_overage(usage, plan):
    base_price = plan["price"]
    included = plan["included_usage"]
    overage_rate = plan["overage_rate"]
    
    if usage <= included:
        return base_price
    else:
        overage = usage - included
        return base_price + (overage * overage_rate)

# Example
plan = {
    "price": 99,
    "included_usage": 10000,  # 10k API calls
    "overage_rate": 0.01      # $0.01 per extra call
}

# Usage: 15,000 calls
bill = calculate_with_overage(15000, plan)  # $99 + (5000 * 0.01) = $149
```

## Packaging Strategy

```python
# Good/Better/Best packaging
packages = {
    "basic": {
        "features": ["core_features"],
        "support": "email",
        "sla": "best_effort"
    },
    "professional": {
        "features": ["core_features", "advanced_analytics"],
        "support": "chat + email",
        "sla": "99.5%"
    },
    "enterprise": {
        "features": ["all_features"],
        "support": "dedicated_success_manager",
        "sla": "99.99%",
        "custom": True
    }
}
```

## Quality Checks
- [ ] Value metric identified (what drives value)
- [ ] Packaging strategy (good/better/best)
- [ ] Experimentation framework (A/B test pricing)
- [ ] Grandfather pricing for existing customers
- [ ] Transparent pricing (no hidden fees)
- [ ] Annual discount (vs monthly)
- [ ] Free trial strategy
- [ ] Expansion revenue tracked
