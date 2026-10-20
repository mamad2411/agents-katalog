---
name: securacymcp
description: "Skill for the Securacymcp area of Securacy. 101 symbols across 20 files."
---

# Securacymcp

101 symbols | 20 files | Cohesion: 79%

## When to Use

- Working with code in `securacymcp/`
- Understanding how record_usage, get_tenant_request_count, get_db_conn work
- Modifying securacymcp-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacymcp/backend_client.py` | get_structured_input_from_tf, get_cyber_controls, get_token, invalidate, _refresh (+10) |
| `securacymcp/tools.py` | _fresh_acc, get_cyber_controls_logic, _prune_diagram_cache, get_structured_input_from_diagram_bytes, get_structured_input_from_tf_logic (+9) |
| `securacymcp/http_server.py` | _check_metering_db, lifespan, _signal_shutdown, main, _handle_sse (+8) |
| `backend/buddlyai/Services/threats_modules/threat_db.py` | initialize_database, load_csv_files_from_s3, load_csv_files, _load_single_csv, _create_combined_text (+4) |
| `securacymcp/api_keys.py` | _ensure_ddl, _hash_key, generate_key, create_api_key, revoke_api_key (+2) |
| `securacymcp/tests/test_tools.py` | test_returns_zero_dict, test_returns_controls, test_returns_structured_input_from_tf, test_returns_dfd, test_returns_structured_input (+2) |
| `securacymcp/tests/test_metering.py` | test_count_within_window, test_count_excludes_old, test_init_pool_raises_without_database_url, test_get_db_conn_triggers_lazy_init, _real_get (+1) |
| `securacymcp/metering.py` | _ensure_ddl, record_usage, get_tenant_request_count, close |
| `securacymcp/db.py` | _init_pool, get_db_conn, release_db_conn, close_db_conn |
| `securacymcp/logger.py` | configure_structured_logging, __init__, _get_log_directory, _setup_root_logger |

## Entry Points

Start here when exploring this area:

- **`record_usage`** (Function) — `securacymcp/metering.py:62`
- **`get_tenant_request_count`** (Function) — `securacymcp/metering.py:176`
- **`get_db_conn`** (Function) — `securacymcp/db.py:42`
- **`release_db_conn`** (Function) — `securacymcp/db.py:49`
- **`generate_key`** (Function) — `securacymcp/api_keys.py:60`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `record_usage` | Function | `securacymcp/metering.py` | 62 |
| `get_tenant_request_count` | Function | `securacymcp/metering.py` | 176 |
| `get_db_conn` | Function | `securacymcp/db.py` | 42 |
| `release_db_conn` | Function | `securacymcp/db.py` | 49 |
| `generate_key` | Function | `securacymcp/api_keys.py` | 60 |
| `create_api_key` | Function | `securacymcp/api_keys.py` | 64 |
| `revoke_api_key` | Function | `securacymcp/api_keys.py` | 139 |
| `test_count_within_window` | Function | `securacymcp/tests/test_metering.py` | 67 |
| `test_count_excludes_old` | Function | `securacymcp/tests/test_metering.py` | 73 |
| `test_init_pool_raises_without_database_url` | Function | `securacymcp/tests/test_metering.py` | 169 |
| `test_get_db_conn_triggers_lazy_init` | Function | `securacymcp/tests/test_metering.py` | 176 |
| `test_prefix` | Function | `securacymcp/tests/test_api_keys.py` | 11 |
| `test_uniqueness` | Function | `securacymcp/tests/test_api_keys.py` | 16 |
| `test_revoke_already_revoked` | Function | `securacymcp/tests/test_api_keys.py` | 87 |
| `commit` | Function | `securacymcp/tests/conftest.py` | 51 |
| `rollback` | Function | `securacymcp/tests/conftest.py` | 54 |
| `copy_threat` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 199 |
| `update_threat_json` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 255 |
| `copy_threat_run` | Function | `backend/buddlyai/DB/DBservice.py` | 164 |
| `updateThreatJson` | Function | `backend/buddlyai/DB/DBservice.py` | 268 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Require_jwt → _init_pool` | cross_community | 5 |
| `Get_structured_input_from_diagram_bytes → _refresh` | cross_community | 5 |
| `Get_structured_input_from_tf_logic → _refresh` | cross_community | 5 |
| `Get_security_threats_logic → _refresh` | cross_community | 5 |
| `Get_usage → _init_pool` | cross_community | 5 |
| `Create_api_key_endpoint → _init_pool` | cross_community | 5 |
| `Export_report_logic → _refresh` | intra_community | 5 |
| `List_api_keys_endpoint → _init_pool` | cross_community | 5 |
| `Revoke_api_key_endpoint → _init_pool` | cross_community | 5 |
| `Get_structured_input_logic → _refresh` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 8 calls |
| DB | 1 calls |
| Services | 1 calls |

## How to Explore

1. `gitnexus_context({name: "record_usage"})` — see callers and callees
2. `gitnexus_query({query: "securacymcp"})` — find related execution flows
3. Read key files listed above for implementation details
