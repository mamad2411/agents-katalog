---
name: threats-modules
description: "Skill for the Threats_modules area of Securacy. 26 symbols across 5 files."
---

# Threats_modules

26 symbols | 5 files | Cohesion: 98%

## When to Use

- Working with code in `backend/`
- Understanding how load_and_process_data, create_embeddings, retrieve_relevant_threats work
- Modifying threats_modules-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | stream_csv_from_s3, get_csv_dataframe, iterate_csv_files, list_threatdb_files, download_threatdb_files (+5) |
| `backend/buddlyai/Services/threats_modules/threat_rag.py` | __init__, load_and_process_data, create_embeddings, retrieve_relevant_threats, analyze_threat_scenario (+2) |
| `backend/buddlyai/Services/threats_modules/threat_db.py` | get_db_path, get_embeddings_path, __init__, get_all_threats, export_to_dataframe |
| `backend/buddlyai/privacy/privacy_threat_analysis_prompt.py` | create_privacythreat_analysis_prompt, generate_privacythreat_json_with_rag |
| `backend/buddlyai/appsec/threat_analysis_prompt.py` | create_threat_analysis_prompt, generate_threat_json_with_rag |

## Entry Points

Start here when exploring this area:

- **`load_and_process_data`** (Function) — `backend/buddlyai/Services/threats_modules/threat_rag.py:39`
- **`create_embeddings`** (Function) — `backend/buddlyai/Services/threats_modules/threat_rag.py:84`
- **`retrieve_relevant_threats`** (Function) — `backend/buddlyai/Services/threats_modules/threat_rag.py:117`
- **`get_db_path`** (Function) — `backend/buddlyai/Services/threats_modules/threat_db.py:29`
- **`get_embeddings_path`** (Function) — `backend/buddlyai/Services/threats_modules/threat_db.py:40`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `load_and_process_data` | Function | `backend/buddlyai/Services/threats_modules/threat_rag.py` | 39 |
| `create_embeddings` | Function | `backend/buddlyai/Services/threats_modules/threat_rag.py` | 84 |
| `retrieve_relevant_threats` | Function | `backend/buddlyai/Services/threats_modules/threat_rag.py` | 117 |
| `get_db_path` | Function | `backend/buddlyai/Services/threats_modules/threat_db.py` | 29 |
| `get_embeddings_path` | Function | `backend/buddlyai/Services/threats_modules/threat_db.py` | 40 |
| `get_all_threats` | Function | `backend/buddlyai/Services/threats_modules/threat_db.py` | 297 |
| `export_to_dataframe` | Function | `backend/buddlyai/Services/threats_modules/threat_db.py` | 415 |
| `create_privacythreat_analysis_prompt` | Function | `backend/buddlyai/privacy/privacy_threat_analysis_prompt.py` | 13 |
| `generate_privacythreat_json_with_rag` | Function | `backend/buddlyai/privacy/privacy_threat_analysis_prompt.py` | 27 |
| `create_threat_analysis_prompt` | Function | `backend/buddlyai/appsec/threat_analysis_prompt.py` | 13 |
| `generate_threat_json_with_rag` | Function | `backend/buddlyai/appsec/threat_analysis_prompt.py` | 28 |
| `analyze_threat_scenario` | Function | `backend/buddlyai/Services/threats_modules/threat_rag.py` | 147 |
| `stream_csv_from_s3` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 72 |
| `get_csv_dataframe` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 98 |
| `iterate_csv_files` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 111 |
| `list_threatdb_files` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 129 |
| `download_threatdb_files` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 153 |
| `upload_local_threatdb` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 246 |
| `get_s3_threatdb_manager` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 307 |
| `upload_threatdb_to_s3` | Function | `backend/buddlyai/Services/threats_modules/s3_threatdb.py` | 318 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Securacymcp | 1 calls |

## How to Explore

1. `gitnexus_context({name: "load_and_process_data"})` — see callers and callees
2. `gitnexus_query({query: "threats_modules"})` — find related execution flows
3. Read key files listed above for implementation details
