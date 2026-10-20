---
name: omop-ohdsi
description: "OHDSI (Observational Health Data Sciences and Informatics) OMOP Common Data Model. Tools for converting EHR data to OMOP CDM, running cohort analyses, and population-level estimation. Standard for observational research."
tags: [omop, ohdsi, ehr, observational-research, real-world-evidence, healthcare, zorai]
---
## Overview

OHDSI (Observational Health Data Sciences and Informatics) provides tools for converting EHR data to the OMOP Common Data Model, running cohort analyses, and population-level estimation. Standard for real-world evidence research.

## Installation

```bash
uv pip install ohdsi-feature-extraction
```

## Key Tools in the Ecosystem

- **ACHILLES** — data quality and characterization dashboards for OMOP CDM
- **ATLAS** — web-based cohort definition and analysis
- **CohortMethod** — comparative cohort studies between treatments
- **PatientLevelPrediction** — ML models for patient outcomes
- **FeatureExtraction** — automated covariate building from OMOP data

## Python Example

```python
# Using the OHDSI Python API
from ohdsi_database_connector import DatabaseConnector

connection_details = {
    "dbms": "postgresql",
    "server": "localhost/omop_cdm",
    "user": "ohdsi",
    "password": "your_password",
}
conn = DatabaseConnector(connectionDetails=connection_details)

# Run a cohort SQL query
sql = "SELECT person_id, condition_concept_id, condition_start_date FROM condition_occurrence"
results = conn.querySql(sql)
```

## Workflow

1. Map source EHR data to OMOP CDM v5.x
2. Run ACHILLES for data quality characterization
3. Define cohorts in ATLAS or via SQL
4. Extract features with FeatureExtraction
5. Run analyses: CohortMethod, SelfControlledCaseSeries
6. Build predictive models with PatientLevelPrediction
