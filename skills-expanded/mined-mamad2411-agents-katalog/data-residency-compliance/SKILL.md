---
name: data-residency-compliance
description: Data residency and compliance — GDPR, data localization, geo-routing
triggers: [data residency, GDPR, compliance, data localization, geo-routing, privacy]
---

# SKILL: Data Residency Compliance

## Geo-Routing (EU data stays in EU)

```python
from fastapi import Request

REGION_DATABASES = {
    "EU": "postgres://eu-db.example.com",
    "US": "postgres://us-db.example.com",
    "APAC": "postgres://apac-db.example.com"
}

def get_user_region(request: Request) -> str:
    """Determine user's region from IP or account"""
    # From IP geolocation
    ip = request.client.host
    region = geoip.lookup(ip)
    
    # Or from user account
    # region = user.data_residency_preference
    
    return region

@app.post("/api/users")
async def create_user(request: Request, user_data: dict):
    region = get_user_region(request)
    
    # Use region-specific database
    db = connect(REGION_DATABASES[region])
    
    # Store user data in their region
    user = db.insert(user_data)
    return user
```

## GDPR Compliance

```python
# Right to be forgotten
@app.delete("/api/users/{user_id}/gdpr-delete")
async def gdpr_delete(user_id: str):
    """Permanently delete all user data"""
    # Delete from all systems
    db.delete_user(user_id)
    analytics.delete_user(user_id)
    backup_service.delete_user(user_id)
    
    # Log deletion (for compliance audit)
    audit_log.record("gdpr_deletion", user_id)
    
    return {"status": "deleted"}

# Right to data portability
@app.get("/api/users/{user_id}/data-export")
async def export_user_data(user_id: str):
    """Export all user data in portable format"""
    user = db.get_user(user_id)
    orders = db.get_orders(user_id)
    
    export = {
        "user": user,
        "orders": orders,
        "export_date": datetime.now()
    }
    
    return export
```

## Quality Checks
- [ ] Data residency requirements documented
- [ ] Region-specific databases configured
- [ ] Geo-routing implemented
- [ ] GDPR compliance (right to deletion, export)
- [ ] Data encryption at rest
- [ ] Cross-border data transfer documented
- [ ] Privacy policy updated
- [ ] Data retention policies defined
