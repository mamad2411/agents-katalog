---
name: json-database
description: "Manage the comprehensive resume database stored as JSON files. Use when you need to: (1) Load resume data (experiences, skills, projects, education), (2) Save or update resume information, (3) Query specific data from the database, (4) Initialize a new database, (5) Validate database structure. This is the central data store for the rescume system that persists user's resume information across sessions."
---

# JSON Resume Database Manager

A tool skill for managing the comprehensive resume database that stores all user resume information in structured JSON format.

## Database Structure

The database consists of five JSON files in `data/comprehensive_db/`:

```
data/comprehensive_db/
├── experiences.json    # Work experiences with bullets
├── skills.json         # All skills with proficiency
├── projects.json       # Projects and achievements
├── education.json      # Education background
└── metadata.json       # Personal info (name, contact, etc.)
```

## Quick Reference

| Task | Function |
|------|----------|
| Load all data | `db_load()` |
| Save data | `db_save(data)` |
| Get experiences | `db_get('experiences')` |
| Add experience | `db_add('experiences', experience_data)` |
| Update skill | `db_update('skills', skill_id, new_data)` |
| Initialize new DB | `db_init()` |
| Validate structure | `db_validate()` |

## Data Schemas

### experiences.json

```json
{
  "experiences": [
    {
      "id": "exp_001",
      "company": "Company Name",
      "role": "Job Title",
      "duration": "2023-2024",
      "location": "City, State",
      "bullets": [
        {
          "id": "bullet_001",
          "text": "Built recommendation system improving engagement by 25%",
          "skills_demonstrated": ["Python", "ML", "A/B Testing"],
          "metrics": ["25% improvement"],
          "priority_base": 8.5,
          "category": "technical"
        }
      ]
    }
  ]
}
```

### skills.json

```json
{
  "skills": [
    {
      "id": "skill_001",
      "name": "Python",
      "category": "programming_language",
      "proficiency": "expert",
      "years_experience": 5,
      "last_used": "2024",
      "evidence_bullets": ["bullet_001", "bullet_005"]
    }
  ]
}
```

### projects.json

```json
{
  "projects": [
    {
      "id": "project_001",
      "name": "Project Name",
      "description": "Brief description",
      "role": "Your role",
      "technologies": ["Python", "SQL"],
      "outcomes": ["Reduced latency by 40%"],
      "duration": "3 months",
      "link": "https://github.com/..."
    }
  ]
}
```

### education.json

```json
{
  "education": [
    {
      "id": "edu_001",
      "institution": "University of Pennsylvania",
      "degree": "M.S.E. in Data Science",
      "field": "Data Science",
      "graduation_date": "2025",
      "gpa": "3.8",
      "relevant_coursework": ["Machine Learning", "Statistics"],
      "honors": ["Dean's List"]
    }
  ]
}
```

### metadata.json

```json
{
  "name": "Your Name",
  "email": "email@example.com",
  "phone": "+1-555-0123",
  "location": "City, State",
  "linkedin": "linkedin.com/in/yourprofile",
  "github": "github.com/yourusername",
  "portfolio": "yourwebsite.com",
  "last_updated": "2024-02-05"
}
```

## Core Operations

### Initialize Database

Creates a new database with empty structure:

```bash
python scripts/db_init.py --output data/comprehensive_db/
```

This creates all five JSON files with proper empty structure.

### Load Data

Load entire database:

```bash
python scripts/db_load.py --db-path data/comprehensive_db/
```

Returns JSON object with all five data files combined.

Load specific file:

```bash
python scripts/db_load.py --db-path data/comprehensive_db/ --file experiences
```

### Save Data

Save entire database:

```bash
python scripts/db_save.py --db-path data/comprehensive_db/ --data '{"experiences": [...], "skills": [...]}'
```

Save specific file:

```bash
python scripts/db_save.py --db-path data/comprehensive_db/ --file experiences --data '[...]'
```

### Add Entry

Add new experience:

```bash
python scripts/db_add.py --db-path data/comprehensive_db/ --type experience --data '{
  "company": "New Company",
  "role": "Data Scientist",
  ...
}'
```

Auto-generates unique ID (e.g., `exp_005`).

### Update Entry

Update existing entry by ID:

```bash
python scripts/db_update.py --db-path data/comprehensive_db/ --type experience --id exp_001 --data '{
  "role": "Senior Data Scientist"
}'
```

Merges new data with existing entry.

### Query Data

Find experiences that demonstrate a specific skill:

```bash
python scripts/db_query.py --db-path data/comprehensive_db/ --query '{
  "type": "experiences",
  "filter": {"skills_demonstrated": {"contains": "Python"}}
}'
```

Returns matching experiences.

### Validate Database

Check database structure and integrity:

```bash
python scripts/db_validate.py --db-path data/comprehensive_db/
```

Checks:
- All required files exist
- JSON is valid
- Schema matches expected structure
- IDs are unique
- Cross-references are valid (e.g., bullets reference valid skills)

## Python Script Reference

All scripts are in `scripts/` directory:

### db_init.py
Creates empty database structure.

**Usage:**
```bash
python scripts/db_init.py --output <path>
```

### db_load.py
Loads data from database.

**Usage:**
```bash
python scripts/db_load.py --db-path <path> [--file <filename>]
```

**Parameters:**
- `--db-path`: Path to comprehensive_db directory
- `--file`: Optional, specific file to load (experiences, skills, projects, education, metadata)

**Returns:** JSON string

### db_save.py
Saves data to database.

**Usage:**
```bash
python scripts/db_save.py --db-path <path> [--file <filename>] --data <json>
```

**Parameters:**
- `--db-path`: Path to comprehensive_db directory
- `--file`: Optional, specific file to save to
- `--data`: JSON string to save

### db_add.py
Adds new entry to database.

**Usage:**
```bash
python scripts/db_add.py --db-path <path> --type <type> --data <json>
```

**Parameters:**
- `--type`: Entry type (experience, skill, project, education)
- `--data`: JSON object for new entry (ID will be auto-generated)

**Returns:** ID of newly created entry

### db_update.py
Updates existing entry.

**Usage:**
```bash
python scripts/db_update.py --db-path <path> --type <type> --id <id> --data <json>
```

**Parameters:**
- `--type`: Entry type
- `--id`: Entry ID to update
- `--data`: JSON object with fields to update (partial update)

### db_query.py
Queries database.

**Usage:**
```bash
python scripts/db_query.py --db-path <path> --query <json>
```

**Query format:**
```json
{
  "type": "experiences",
  "filter": {
    "skills_demonstrated": {"contains": "Python"},
    "company": {"equals": "Google"}
  },
  "sort": {"field": "priority_base", "order": "desc"},
  "limit": 10
}
```

### db_validate.py
Validates database structure and integrity.

**Usage:**
```bash
python scripts/db_validate.py --db-path <path>
```

**Returns:** Validation report with any errors or warnings

## Integration with Subagents

### resume-parser subagent
**Uses:** `db_init`, `db_add`, `db_save`
**Flow:** Parse DOCX → Extract data → Add to database

### interview-conductor subagent
**Uses:** `db_load`, `db_update`
**Flow:** Load current data → Generate questions → Update with answers

### coverage-mapper subagent
**Uses:** `db_load`, `db_query`
**Flow:** Load all data → Query for skill matches → Build coverage matrix

### content-generator subagent
**Uses:** `db_load`, `db_query`
**Flow:** Query prioritized experiences → Generate resume content

## Best Practices

1. **Always validate** after manual edits: `db_validate.py`
2. **Use atomic operations**: Save entire database after updates to maintain consistency
3. **Generate unique IDs**: Let `db_add.py` auto-generate IDs (format: `type_NNN`)
4. **Backup before major changes**: Copy `comprehensive_db/` directory
5. **Keep cross-references valid**: When deleting entries, check for references

## Error Handling

All scripts return proper exit codes:
- `0`: Success
- `1`: Validation error (invalid JSON, missing required field)
- `2`: File not found
- `3`: ID conflict or not found

Check exit codes in bash:
```bash
python scripts/db_add.py ... && echo "Success" || echo "Failed"
```

## Database Growth

As database grows:
- **Performance**: JSON files are fast for databases <10MB
- **Backup**: Version control `comprehensive_db/` directory
- **Search**: `db_query.py` supports filtering and sorting
- **Cleanup**: Remove old/irrelevant experiences periodically

## Example Workflow

**Initial setup:**
```bash
# Initialize database
python scripts/db_init.py --output data/comprehensive_db/

# Add first experience
python scripts/db_add.py --db-path data/comprehensive_db/ --type experience --data '{
  "company": "Tech Corp",
  "role": "Data Scientist",
  "duration": "2023-2024",
  "bullets": [...]
}'

# Validate
python scripts/db_validate.py --db-path data/comprehensive_db/
```

**Querying:**
```bash
# Find all Python experiences
python scripts/db_query.py --db-path data/comprehensive_db/ --query '{
  "type": "experiences",
  "filter": {"skills_demonstrated": {"contains": "Python"}},
  "sort": {"field": "priority_base", "order": "desc"}
}'
```

**Updating:**
```bash
# Update a skill's proficiency
python scripts/db_update.py --db-path data/comprehensive_db/ --type skill --id skill_001 --data '{
  "proficiency": "expert",
  "years_experience": 6
}'
```

## Notes

- All dates use ISO format: `YYYY-MM-DD`
- IDs are immutable once created
- Database is portable (just copy `comprehensive_db/` folder)
- JSON files are human-readable and git-friendly
- No database server required (file-based)
