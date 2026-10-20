---
name: marches-publics
description: "Search public procurement contracts (BOAMP) for IT, cybersecurity, and consulting opportunities. Use when the user asks about public tenders, government contracts, or wants to find procurement opportunities in a specific sector or territory."
metadata: { "openclaw": { "emoji": "\uD83C\uDFDB\uFE0F", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# marches-publics

Search French public procurement contracts via the BOAMP (Bulletin Officiel des Annonces de Marches Publics).

## Triggers

- `/marches cybersecurite 31`
- `/marches audit informatique Toulouse`
- "marches publics IT Toulouse"
- "appels d'offres cybersecurite"
- "qui achete du conseil IT dans le 31?"

## How it works

Queries the BOAMP OpenDataSoft API (DILA) which publishes all public procurement announcements. No authentication required.

API endpoint: `https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records`

## CPV code filtering

The skill can filter by CPV (Common Procurement Vocabulary) codes relevant to IT and consulting:

| CPV Code   | Description                          |
|------------|--------------------------------------|
| 72000000   | IT services (parent)                 |
| 72200000   | Software and consulting              |
| 72300000   | Data services                        |
| 72400000   | Internet services                    |
| 72500000   | IT support services                  |
| 72600000   | IT support and consulting            |
| 79417000   | Security consulting                  |
| 79000000   | Business services (parent)           |
| 79400000   | Consulting and management            |

## Usage

```bash
python3 {baseDir}/scripts/boamp.py --query "cybersecurite" --department 31 --format json
python3 {baseDir}/scripts/boamp.py --query "audit informatique" --cpv 72000000 --format text
python3 {baseDir}/scripts/boamp.py --query "RGPD" --days 30 --format json
```

## Arguments

| Argument       | Required | Default | Description                                  |
|----------------|----------|---------|----------------------------------------------|
| `--query`      | yes      |         | Keywords to search in contract titles/descriptions |
| `--department`  | no       |         | Department code (e.g. 31, 75)                 |
| `--cpv`        | no       |         | CPV code to filter by (e.g. 72000000)          |
| `--days`       | no       | 30      | Look back N days from today                    |
| `--per-page`   | no       | 20      | Number of results (1-100)                      |
| `--format`     | no       | json    | Output format: `json` or `text`                |

## Output fields

- `title` — contract title
- `buyer` — purchasing organization
- `amount` — estimated value if available
- `deadline` — submission deadline
- `cpv_code` — CPV classification code
- `department` — department code
- `description` — contract summary
- `url` — link to the full notice
- `publication_date` — date of publication
