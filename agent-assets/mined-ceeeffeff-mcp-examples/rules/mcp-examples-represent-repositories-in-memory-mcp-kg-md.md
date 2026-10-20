---
# alwaysApply: true
---

## 🛠️ Enhanced Recommendations for Knowledge Graph Generation

### 1. Enforce Explicit Relations
Use `memory_create_relations` for all dependencies, security, and infrastructure integrations:
```json
{
"relations": [
{
"from": "src/scraper_service/main.py",
"relationType": "dependsOn",
"to": "config/db.yml"
},
{
"from": "vault/secrets/db-credentials.json",
"relationType": "securedBy",
"to": "vault/secrets/rotation-policy.json"
},
{
"from": "terraform/resources--services/api.tf",
"relationType": "triggers",
"to": "scripts/deploy-api.sh"
}
]
}
```

### 2. Ensure Complete Entity Coverage
Add missing files using `memory_create_entities`:
```json
{
"entities": [
{
"entityType": "Source Code",
"name": "src/seomax/models/database.py",
"observations": [
"Tech Stack: Python 3.9",
"Imports module from src/seomax/implementations/firestore_database.py"
]
},
{
"entityType": "Infrastructure",
"name": "scripts/deploy-api.sh",
"observations": [
"Triggers: terraform/resources--services/api.tf",
"Uses: AWS CLI"
]
}
]
}
```

### 3. Refine Observations
Replace vague terms with precise relational metadata:
- "Depends On: config/db.yml" → "Loads configuration from config/db.yml"
- "Linked To: src/seomax/models/database.py" → "Imports module from src/seomax/models/database.py"

### 4. Tool Usage Guide
- Use `file_glob_search` with patterns like `**/*.py`, `**/*.yml`, `**/*.sh` to ensure completeness
- Always model relations before adding entities
- Use `memory_create_relations` for security, dependencies, and infrastructure integrations

## ✅ Best Practices
1. **Always Model Relations**: Use `memory_create_relations` for all dependencies and integrations
2. **Ensure Completeness**: Scan repositories with `file_glob_search` to include all files
3. **Use Precise Observations**: Describe relationships explicitly (e.g., "Loads configuration from...")
4. **Avoid Isolated Entities**: Relate entities to dependencies, security measures, and infrastructure components

## 🧠 Lessons Learned
- A KG without relations is a partial snapshot, not a comprehensive model
- Missing entities create blind spots in the graph
- Ambiguous observations lack context and utility
- Use `memory_create_relations` and `memory_create_entities` to build a relational, complete KG
