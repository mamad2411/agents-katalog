---
name: elasticsearch-request-response-specification
description: "Elasticsearch Request & Response Specification API skill. Use when working with Elasticsearch Request & Response Specification for _async_search, {index}, _bulk. Covers 823 endpoints."
version: 1.0.0
generator: lapsh
---

# Elasticsearch Request & Response Specification

## Auth
ApiKey ids in path

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /_cat/aliases -- verify access
3. POST /_async_search -- create first _async_search

## Endpoints

823 endpoints across 79 groups. See references/api-spec.lap for full details.

### _async_search
| Method | Path | Description |
|--------|------|-------------|
| GET | /_async_search/{id} | Get async search results |
| DELETE | /_async_search/{id} | Delete an async search |
| GET | /_async_search/status/{id} | Get the async search status |
| POST | /_async_search | Run an async search |

### {index}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{index}/_async_search | Run an async search |
| PUT | /{index}/_bulk | Bulk index or delete documents |
| POST | /{index}/_bulk | Bulk index or delete documents |
| PUT | /{index}/_ccr/follow | Create a follower |
| GET | /{index}/_ccr/info | Get follower information |
| GET | /{index}/_ccr/stats | Get follower stats |
| POST | /{index}/_ccr/forget_follower | Forget a follower |
| POST | /{index}/_ccr/pause_follow | Pause a follower |
| POST | /{index}/_ccr/resume_follow | Resume a follower |
| POST | /{index}/_ccr/unfollow | Unfollow an index |
| GET | /{index}/_count | Count search results |
| POST | /{index}/_count | Count search results |
| PUT | /{index}/_create/{id} | Create a new document in the index |
| POST | /{index}/_create/{id} | Create a new document in the index |
| GET | /{index}/_doc/{id} | Get a document by its ID |
| PUT | /{index}/_doc/{id} | Create or update a document in an index |
| POST | /{index}/_doc/{id} | Create or update a document in an index |
| DELETE | /{index}/_doc/{id} | Delete a document |
| HEAD | /{index}/_doc/{id} | Check a document |
| POST | /{index}/_delete_by_query | Delete documents |
| GET | /{index}/_eql/search | Get EQL search results |
| POST | /{index}/_eql/search | Get EQL search results |
| GET | /{index}/_source/{id} | Get a document's source |
| HEAD | /{index}/_source/{id} | Check for a document source |
| GET | /{index}/_explain/{id} | Explain a document match result |
| POST | /{index}/_explain/{id} | Explain a document match result |
| GET | /{index}/_field_caps | Get the field capabilities |
| POST | /{index}/_field_caps | Get the field capabilities |
| GET | /{index}/_fleet/global_checkpoints | Get global checkpoints |
| GET | /{index}/_fleet/_fleet_msearch | Run multiple Fleet searches |
| POST | /{index}/_fleet/_fleet_msearch | Run multiple Fleet searches |
| GET | /{index}/_fleet/_fleet_search | Run a Fleet search |
| POST | /{index}/_fleet/_fleet_search | Run a Fleet search |
| GET | /{index}/_graph/explore | Explore graph analytics |
| POST | /{index}/_graph/explore | Explore graph analytics |
| GET | /{index}/_ilm/explain | Explain the lifecycle state |
| POST | /{index}/_ilm/remove | Remove policies from an index |
| POST | /{index}/_ilm/retry | Retry a policy |
| POST | /{index}/_doc | Create or update a document in an index |
| PUT | /{index}/_block/{block} | Add an index block |
| DELETE | /{index}/_block/{block} | Remove an index block |
| GET | /{index}/_analyze | Get tokens from text analysis |
| POST | /{index}/_analyze | Get tokens from text analysis |
| POST | /{index}/_cache/clear | Clear the cache |
| PUT | /{index}/_clone/{target} | Clone an index |
| POST | /{index}/_clone/{target} | Clone an index |
| POST | /{index}/_close | Close an index |
| GET | /{index} | Get index information |
| PUT | /{index} | Create an index |
| DELETE | /{index} | Delete indices |
| HEAD | /{index} | Check indices |
| GET | /{index}/_alias/{name} | Get aliases |
| PUT | /{index}/_alias/{name} | Create or update an alias |
| POST | /{index}/_alias/{name} | Create or update an alias |
| DELETE | /{index}/_alias/{name} | Delete an alias |
| HEAD | /{index}/_alias/{name} | Check aliases |
| PUT | /{index}/_aliases/{name} | Create or update an alias |
| POST | /{index}/_aliases/{name} | Create or update an alias |
| DELETE | /{index}/_aliases/{name} | Delete an alias |
| POST | /{index}/_disk_usage | Analyze the index disk usage |
| POST | /{index}/_downsample/{target_index} | Downsample an index |
| GET | /{index}/_lifecycle/explain | Get the status for a data stream lifecycle |
| GET | /{index}/_field_usage_stats | Get field usage stats |
| GET | /{index}/_flush | Flush data streams or indices |
| POST | /{index}/_flush | Flush data streams or indices |
| POST | /{index}/_forcemerge | Force a merge |
| GET | /{index}/_alias | Get aliases |
| GET | /{index}/_mapping/field/{fields} | Get mapping definitions |
| GET | /{index}/_mapping | Get mapping definitions |
| PUT | /{index}/_mapping | Update field mappings |
| POST | /{index}/_mapping | Update field mappings |
| GET | /{index}/_settings | Get index settings |
| PUT | /{index}/_settings | Update index settings |
| GET | /{index}/_settings/{name} | Get index settings |
| POST | /{index}/_open | Open a closed index |
| GET | /{index}/_recovery | Get index recovery information |
| GET | /{index}/_refresh | Refresh an index |
| POST | /{index}/_refresh | Refresh an index |
| GET | /{index}/_reload_search_analyzers | Reload search analyzers |
| POST | /{index}/_reload_search_analyzers | Reload search analyzers |
| GET | /{index}/_segments | Get index segments |
| GET | /{index}/_shard_stores | Get index shard stores |
| PUT | /{index}/_shrink/{target} | Shrink an index |
| POST | /{index}/_shrink/{target} | Shrink an index |
| PUT | /{index}/_split/{target} | Split an index |
| POST | /{index}/_split/{target} | Split an index |
| GET | /{index}/_stats | Get index statistics |
| GET | /{index}/_stats/{metric} | Get index statistics |
| GET | /{index}/_validate/query | Validate a query |
| POST | /{index}/_validate/query | Validate a query |
| GET | /{index}/_mget | Get multiple documents |
| POST | /{index}/_mget | Get multiple documents |
| GET | /{index}/_migration/deprecations | Get deprecation information |
| GET | /{index}/_msearch | Run multiple searches |
| POST | /{index}/_msearch | Run multiple searches |
| GET | /{index}/_msearch/template | Run multiple templated searches |
| POST | /{index}/_msearch/template | Run multiple templated searches |
| GET | /{index}/_mtermvectors | Get multiple term vectors |
| POST | /{index}/_mtermvectors | Get multiple term vectors |
| POST | /{index}/_pit | Open a point in time |
| GET | /{index}/_rank_eval | Evaluate ranked search results |
| POST | /{index}/_rank_eval | Evaluate ranked search results |
| GET | /{index}/_rollup/data | Get the rollup index capabilities |
| GET | /{index}/_rollup_search | Search rolled-up data |
| POST | /{index}/_rollup_search | Search rolled-up data |
| GET | /{index}/_search | Run a search |
| POST | /{index}/_search | Run a search |
| GET | /{index}/_mvt/{field}/{zoom}/{x}/{y} | Search a vector tile |
| POST | /{index}/_mvt/{field}/{zoom}/{x}/{y} | Search a vector tile |
| GET | /{index}/_search_shards | Get the search shards |
| POST | /{index}/_search_shards | Get the search shards |
| GET | /{index}/_search/template | Run a search with a search template |
| POST | /{index}/_search/template | Run a search with a search template |
| POST | /{index}/_searchable_snapshots/cache/clear | Clear the cache |
| GET | /{index}/_searchable_snapshots/stats | Get searchable snapshot statistics |
| GET | /{index}/_terms_enum | Get terms in an index |
| POST | /{index}/_terms_enum | Get terms in an index |
| GET | /{index}/_termvectors/{id} | Get term vector information |
| POST | /{index}/_termvectors/{id} | Get term vector information |
| GET | /{index}/_termvectors | Get term vector information |
| POST | /{index}/_termvectors | Get term vector information |
| POST | /{index}/_update/{id} | Update a document |
| POST | /{index}/_update_by_query | Update documents |

### _bulk
| Method | Path | Description |
|--------|------|-------------|
| PUT | /_bulk | Bulk index or delete documents |
| POST | /_bulk | Bulk index or delete documents |

### _cat
| Method | Path | Description |
|--------|------|-------------|
| GET | /_cat/aliases | Get aliases |
| GET | /_cat/aliases/{name} | Get aliases |
| GET | /_cat/allocation | Get shard allocation information |
| GET | /_cat/allocation/{node_id} | Get shard allocation information |
| GET | /_cat/circuit_breaker | Get circuit breakers statistics |
| GET | /_cat/circuit_breaker/{circuit_breaker_patterns} | Get circuit breakers statistics |
| GET | /_cat/component_templates | Get component templates |
| GET | /_cat/component_templates/{name} | Get component templates |
| GET | /_cat/count | Get a document count |
| POST | /_cat/count | Get a document count |
| GET | /_cat/count/{index} | Get a document count |
| POST | /_cat/count/{index} | Get a document count |
| GET | /_cat/fielddata | Get field data cache information |
| GET | /_cat/fielddata/{fields} | Get field data cache information |
| GET | /_cat/health | Get the cluster health status |
| GET | /_cat | Get CAT help |
| GET | /_cat/indices | Get index information |
| GET | /_cat/indices/{index} | Get index information |
| GET | /_cat/master | Get master node information |
| GET | /_cat/ml/data_frame/analytics | Get data frame analytics jobs |
| GET | /_cat/ml/data_frame/analytics/{id} | Get data frame analytics jobs |
| GET | /_cat/ml/datafeeds | Get datafeeds |
| GET | /_cat/ml/datafeeds/{datafeed_id} | Get datafeeds |
| GET | /_cat/ml/anomaly_detectors | Get anomaly detection jobs |
| GET | /_cat/ml/anomaly_detectors/{job_id} | Get anomaly detection jobs |
| GET | /_cat/ml/trained_models | Get trained models |
| GET | /_cat/ml/trained_models/{model_id} | Get trained models |
| GET | /_cat/nodeattrs | Get node attribute information |
| GET | /_cat/nodes | Get node information |
| GET | /_cat/pending_tasks | Get pending task information |
| GET | /_cat/plugins | Get plugin information |
| GET | /_cat/recovery | Get shard recovery information |
| GET | /_cat/recovery/{index} | Get shard recovery information |
| GET | /_cat/repositories | Get snapshot repository information |
| GET | /_cat/segments | Get segment information |
| GET | /_cat/segments/{index} | Get segment information |
| GET | /_cat/shards | Get shard information |
| GET | /_cat/shards/{index} | Get shard information |
| GET | /_cat/snapshots | Get snapshot information |
| GET | /_cat/snapshots/{repository} | Get snapshot information |
| GET | /_cat/tasks | Get task information |
| GET | /_cat/templates | Get index template information |
| GET | /_cat/templates/{name} | Get index template information |
| GET | /_cat/thread_pool | Get thread pool statistics |
| GET | /_cat/thread_pool/{thread_pool_patterns} | Get thread pool statistics |
| GET | /_cat/transforms | Get transform information |
| GET | /_cat/transforms/{transform_id} | Get transform information |

### _ccr
| Method | Path | Description |
|--------|------|-------------|
| GET | /_ccr/auto_follow/{name} | Get auto-follow patterns |
| PUT | /_ccr/auto_follow/{name} | Create or update auto-follow patterns |
| DELETE | /_ccr/auto_follow/{name} | Delete auto-follow patterns |
| GET | /_ccr/auto_follow | Get auto-follow patterns |
| POST | /_ccr/auto_follow/{name}/pause | Pause an auto-follow pattern |
| POST | /_ccr/auto_follow/{name}/resume | Resume an auto-follow pattern |
| GET | /_ccr/stats | Get cross-cluster replication stats |

### _search
| Method | Path | Description |
|--------|------|-------------|
| GET | /_search/scroll | Run a scrolling search |
| POST | /_search/scroll | Run a scrolling search |
| DELETE | /_search/scroll | Clear a scrolling search |
| GET | /_search/scroll/{scroll_id} | Run a scrolling search |
| POST | /_search/scroll/{scroll_id} | Run a scrolling search |
| DELETE | /_search/scroll/{scroll_id} | Clear a scrolling search |
| GET | /_search | Run a search |
| POST | /_search | Run a search |
| GET | /_search/template | Run a search with a search template |
| POST | /_search/template | Run a search with a search template |

### _pit
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /_pit | Close a point in time |

### _cluster
| Method | Path | Description |
|--------|------|-------------|
| GET | /_cluster/allocation/explain | Explain the shard allocations |
| POST | /_cluster/allocation/explain | Explain the shard allocations |
| POST | /_cluster/voting_config_exclusions | Update voting configuration exclusions |
| DELETE | /_cluster/voting_config_exclusions | Clear cluster voting config exclusions |
| GET | /_cluster/settings | Get cluster-wide settings |
| PUT | /_cluster/settings | Update the cluster settings |
| GET | /_cluster/health | Get the cluster health status |
| GET | /_cluster/health/{index} | Get the cluster health status |
| GET | /_cluster/pending_tasks | Get the pending cluster tasks |
| POST | /_cluster/reroute | Reroute the cluster |
| GET | /_cluster/state | Get the cluster state |
| GET | /_cluster/state/{metric} | Get the cluster state |
| GET | /_cluster/state/{metric}/{index} | Get the cluster state |
| GET | /_cluster/stats | Get cluster statistics |
| GET | /_cluster/stats/nodes/{node_id} | Get cluster statistics |

### _component_template
| Method | Path | Description |
|--------|------|-------------|
| GET | /_component_template/{name} | Get component templates |
| PUT | /_component_template/{name} | Create or update a component template |
| POST | /_component_template/{name} | Create or update a component template |
| DELETE | /_component_template/{name} | Delete component templates |
| HEAD | /_component_template/{name} | Check component templates |
| GET | /_component_template | Get component templates |

### _info
| Method | Path | Description |
|--------|------|-------------|
| GET | /_info/{target} | Get cluster info |

### _remote
| Method | Path | Description |
|--------|------|-------------|
| GET | /_remote/info | Get remote cluster information |

### _connector
| Method | Path | Description |
|--------|------|-------------|
| PUT | /_connector/{connector_id}/_check_in | Check in a connector |
| GET | /_connector/{connector_id} | Get a connector |
| PUT | /_connector/{connector_id} | Create or update a connector |
| DELETE | /_connector/{connector_id} | Delete a connector |
| GET | /_connector | Get all connectors |
| PUT | /_connector | Create or update a connector |
| POST | /_connector | Create a connector |
| PUT | /_connector/_sync_job/{connector_sync_job_id}/_cancel | Cancel a connector sync job |
| PUT | /_connector/_sync_job/{connector_sync_job_id}/_check_in | Check in a connector sync job |
| PUT | /_connector/_sync_job/{connector_sync_job_id}/_claim | Claim a connector sync job |
| GET | /_connector/_sync_job/{connector_sync_job_id} | Get a connector sync job |
| DELETE | /_connector/_sync_job/{connector_sync_job_id} | Delete a connector sync job |
| PUT | /_connector/_sync_job/{connector_sync_job_id}/_error | Set a connector sync job error |
| GET | /_connector/_sync_job | Get all connector sync jobs |
| POST | /_connector/_sync_job | Create a connector sync job |
| PUT | /_connector/_sync_job/{connector_sync_job_id}/_stats | Set the connector sync job stats |
| PUT | /_connector/{connector_id}/_filtering/_activate | Activate the connector draft filter |
| PUT | /_connector/{connector_id}/_api_key_id | Update the connector API key ID |
| PUT | /_connector/{connector_id}/_configuration | Update the connector configuration |
| PUT | /_connector/{connector_id}/_error | Update the connector error field |
| PUT | /_connector/{connector_id}/_features | Update the connector features |
| PUT | /_connector/{connector_id}/_filtering | Update the connector filtering |
| PUT | /_connector/{connector_id}/_filtering/_validation | Update the connector draft filtering validation |
| PUT | /_connector/{connector_id}/_index_name | Update the connector index name |
| PUT | /_connector/{connector_id}/_name | Update the connector name and description |
| PUT | /_connector/{connector_id}/_native | Update the connector is_native flag |
| PUT | /_connector/{connector_id}/_pipeline | Update the connector pipeline |
| PUT | /_connector/{connector_id}/_scheduling | Update the connector scheduling |
| PUT | /_connector/{connector_id}/_service_type | Update the connector service type |
| PUT | /_connector/{connector_id}/_status | Update the connector status |

### _count
| Method | Path | Description |
|--------|------|-------------|
| GET | /_count | Count search results |
| POST | /_count | Count search results |

### _dangling
| Method | Path | Description |
|--------|------|-------------|
| POST | /_dangling/{index_uuid} | Import a dangling index |
| DELETE | /_dangling/{index_uuid} | Delete a dangling index |
| GET | /_dangling | Get the dangling indices |

### _delete_by_query
| Method | Path | Description |
|--------|------|-------------|
| POST | /_delete_by_query/{task_id}/_rethrottle | Throttle a delete by query operation |

### _scripts
| Method | Path | Description |
|--------|------|-------------|
| GET | /_scripts/{id} | Get a script or search template |
| PUT | /_scripts/{id} | Create or update a script or search template |
| POST | /_scripts/{id} | Create or update a script or search template |
| DELETE | /_scripts/{id} | Delete a script or search template |
| PUT | /_scripts/{id}/{context} | Create or update a script or search template |
| POST | /_scripts/{id}/{context} | Create or update a script or search template |
| GET | /_scripts/painless/_execute | Run a script |
| POST | /_scripts/painless/_execute | Run a script |

### _enrich
| Method | Path | Description |
|--------|------|-------------|
| GET | /_enrich/policy/{name} | Get an enrich policy |
| PUT | /_enrich/policy/{name} | Create an enrich policy |
| DELETE | /_enrich/policy/{name} | Delete an enrich policy |
| PUT | /_enrich/policy/{name}/_execute | Run an enrich policy |
| GET | /_enrich/policy | Get an enrich policy |
| GET | /_enrich/_stats | Get enrich stats |

### _eql
| Method | Path | Description |
|--------|------|-------------|
| GET | /_eql/search/{id} | Get async EQL search results |
| DELETE | /_eql/search/{id} | Delete an async EQL search |
| GET | /_eql/search/status/{id} | Get the async EQL status |

### _query
| Method | Path | Description |
|--------|------|-------------|
| POST | /_query/async | Run an async ES|QL query |
| GET | /_query/async/{id} | Get async ES|QL query results |
| DELETE | /_query/async/{id} | Delete an async ES|QL query |
| POST | /_query/async/{id}/stop | Stop async ES|QL query |
| GET | /_query/queries/{id} | Get a specific running ES|QL query information |
| GET | /_query/queries | Get running ES|QL queries information |
| POST | /_query | Run an ES|QL query |

### _features
| Method | Path | Description |
|--------|------|-------------|
| GET | /_features | Get the features |
| POST | /_features/_reset | Reset the features |

### _field_caps
| Method | Path | Description |
|--------|------|-------------|
| GET | /_field_caps | Get the field capabilities |
| POST | /_field_caps | Get the field capabilities |

### _fleet
| Method | Path | Description |
|--------|------|-------------|
| GET | /_fleet/_fleet_msearch | Run multiple Fleet searches |
| POST | /_fleet/_fleet_msearch | Run multiple Fleet searches |

### _script_context
| Method | Path | Description |
|--------|------|-------------|
| GET | /_script_context | Get script contexts |

### _script_language
| Method | Path | Description |
|--------|------|-------------|
| GET | /_script_language | Get script languages |

### _health_report
| Method | Path | Description |
|--------|------|-------------|
| GET | /_health_report | Get the cluster health |
| GET | /_health_report/{feature} | Get the cluster health |

### _ilm
| Method | Path | Description |
|--------|------|-------------|
| GET | /_ilm/policy/{policy} | Get lifecycle policies |
| PUT | /_ilm/policy/{policy} | Create or update a lifecycle policy |
| DELETE | /_ilm/policy/{policy} | Delete a lifecycle policy |
| GET | /_ilm/policy | Get lifecycle policies |
| GET | /_ilm/status | Get the ILM status |
| POST | /_ilm/migrate_to_data_tiers | Migrate to data tiers routing |
| POST | /_ilm/move/{index} | Move to a lifecycle step |
| POST | /_ilm/start | Start the ILM plugin |
| POST | /_ilm/stop | Stop the ILM plugin |

### _analyze
| Method | Path | Description |
|--------|------|-------------|
| GET | /_analyze | Get tokens from text analysis |
| POST | /_analyze | Get tokens from text analysis |

### _migration
| Method | Path | Description |
|--------|------|-------------|
| POST | /_migration/reindex/{index}/_cancel | Cancel a migration reindex operation |
| GET | /_migration/reindex/{index}/_status | Get the migration reindexing status |
| POST | /_migration/reindex | Reindex legacy backing indices |
| GET | /_migration/deprecations | Get deprecation information |
| GET | /_migration/system_features | Get feature migration information |
| POST | /_migration/system_features | Start the feature migration |

### _cache
| Method | Path | Description |
|--------|------|-------------|
| POST | /_cache/clear | Clear the cache |

### _data_stream
| Method | Path | Description |
|--------|------|-------------|
| GET | /_data_stream/{name} | Get data streams |
| PUT | /_data_stream/{name} | Create a data stream |
| DELETE | /_data_stream/{name} | Delete data streams |
| GET | /_data_stream/_stats | Get data stream stats |
| GET | /_data_stream/{name}/_stats | Get data stream stats |
| GET | /_data_stream/{name}/_lifecycle | Get data stream lifecycles |
| PUT | /_data_stream/{name}/_lifecycle | Update data stream lifecycles |
| DELETE | /_data_stream/{name}/_lifecycle | Delete data stream lifecycles |
| GET | /_data_stream/{name}/_options | Get data stream options |
| PUT | /_data_stream/{name}/_options | Update data stream options |
| DELETE | /_data_stream/{name}/_options | Delete data stream options |
| GET | /_data_stream | Get data streams |
| GET | /_data_stream/{name}/_mappings | Get data stream mappings |
| PUT | /_data_stream/{name}/_mappings | Update data stream mappings |
| GET | /_data_stream/{name}/_settings | Get data stream settings |
| PUT | /_data_stream/{name}/_settings | Update data stream settings |
| POST | /_data_stream/_migrate/{name} | Convert an index alias to a data stream |
| POST | /_data_stream/_modify | Update data streams |
| POST | /_data_stream/_promote/{name} | Promote a data stream |

### _create_from
| Method | Path | Description |
|--------|------|-------------|
| PUT | /_create_from/{source}/{dest} | Create an index from a source index |
| POST | /_create_from/{source}/{dest} | Create an index from a source index |

### _index_template
| Method | Path | Description |
|--------|------|-------------|
| GET | /_index_template/{name} | Get index templates |
| PUT | /_index_template/{name} | Create or update an index template |
| POST | /_index_template/{name} | Create or update an index template |
| DELETE | /_index_template/{name} | Delete an index template |
| HEAD | /_index_template/{name} | Check index templates |
| GET | /_index_template | Get index templates |
| POST | /_index_template/_simulate_index/{name} | Simulate an index |
| POST | /_index_template/_simulate | Simulate an index template |
| POST | /_index_template/_simulate/{name} | Simulate an index template |

### _template
| Method | Path | Description |
|--------|------|-------------|
| GET | /_template/{name} | Get legacy index templates |
| PUT | /_template/{name} | Create or update a legacy index template |
| POST | /_template/{name} | Create or update a legacy index template |
| DELETE | /_template/{name} | Delete a legacy index template |
| HEAD | /_template/{name} | Check existence of index templates |
| GET | /_template | Get legacy index templates |

### _alias
| Method | Path | Description |
|--------|------|-------------|
| GET | /_alias/{name} | Get aliases |
| HEAD | /_alias/{name} | Check aliases |
| GET | /_alias | Get aliases |

### _flush
| Method | Path | Description |
|--------|------|-------------|
| GET | /_flush | Flush data streams or indices |
| POST | /_flush | Flush data streams or indices |

### _forcemerge
| Method | Path | Description |
|--------|------|-------------|
| POST | /_forcemerge | Force a merge |

### _lifecycle
| Method | Path | Description |
|--------|------|-------------|
| GET | /_lifecycle/stats | Get data stream lifecycle stats |

### _mapping
| Method | Path | Description |
|--------|------|-------------|
| GET | /_mapping/field/{fields} | Get mapping definitions |
| GET | /_mapping | Get mapping definitions |

### _settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /_settings | Get index settings |
| PUT | /_settings | Update index settings |
| GET | /_settings/{name} | Get index settings |

### _recovery
| Method | Path | Description |
|--------|------|-------------|
| GET | /_recovery | Get index recovery information |

### _refresh
| Method | Path | Description |
|--------|------|-------------|
| GET | /_refresh | Refresh an index |
| POST | /_refresh | Refresh an index |

### _resolve
| Method | Path | Description |
|--------|------|-------------|
| GET | /_resolve/cluster | Resolve the cluster |
| GET | /_resolve/cluster/{name} | Resolve the cluster |
| GET | /_resolve/index/{name} | Resolve indices |
| POST | /_resolve/index/{name} | Resolve indices |

### {alias}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{alias}/_rollover | Roll over to a new index |
| POST | /{alias}/_rollover/{new_index} | Roll over to a new index |

### _segments
| Method | Path | Description |
|--------|------|-------------|
| GET | /_segments | Get index segments |

### _shard_stores
| Method | Path | Description |
|--------|------|-------------|
| GET | /_shard_stores | Get index shard stores |

### _stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /_stats | Get index statistics |
| GET | /_stats/{metric} | Get index statistics |

### _aliases
| Method | Path | Description |
|--------|------|-------------|
| POST | /_aliases | Create or update an alias |

### _validate
| Method | Path | Description |
|--------|------|-------------|
| GET | /_validate/query | Validate a query |
| POST | /_validate/query | Validate a query |

### _inference
| Method | Path | Description |
|--------|------|-------------|
| POST | /_inference/chat_completion/{inference_id}/_stream | Perform chat completion inference on the service |
| POST | /_inference/completion/{inference_id} | Perform completion inference on the service |
| GET | /_inference/{inference_id} | Get an inference endpoint |
| PUT | /_inference/{inference_id} | Create an inference endpoint |
| POST | /_inference/{inference_id} | Perform inference on the service |
| DELETE | /_inference/{inference_id} | Delete an inference endpoint |
| GET | /_inference/{task_type}/{inference_id} | Get an inference endpoint |
| PUT | /_inference/{task_type}/{inference_id} | Create an inference endpoint |
| POST | /_inference/{task_type}/{inference_id} | Perform inference on the service |
| DELETE | /_inference/{task_type}/{inference_id} | Delete an inference endpoint |
| POST | /_inference/embedding/{inference_id} | Perform dense embedding inference on the service |
| GET | /_inference | Get an inference endpoint |
| GET | /_inference/{task_type}/_all | Get an inference endpoint |
| PUT | /_inference/{task_type}/{ai21_inference_id} | Create a AI21 inference endpoint |
| PUT | /_inference/{task_type}/{alibabacloud_inference_id} | Create an AlibabaCloud AI Search inference endpoint |
| PUT | /_inference/{task_type}/{amazonbedrock_inference_id} | Create an Amazon Bedrock inference endpoint |
| PUT | /_inference/{task_type}/{amazonsagemaker_inference_id} | Create an Amazon SageMaker inference endpoint |
| PUT | /_inference/{task_type}/{anthropic_inference_id} | Create an Anthropic inference endpoint |
| PUT | /_inference/{task_type}/{azureaistudio_inference_id} | Create an Azure AI studio inference endpoint |
| PUT | /_inference/{task_type}/{azureopenai_inference_id} | Create an Azure OpenAI inference endpoint |
| PUT | /_inference/{task_type}/{cohere_inference_id} | Create a Cohere inference endpoint |
| PUT | /_inference/{task_type}/{contextualai_inference_id} | Create an Contextual AI inference endpoint |
| PUT | /_inference/{task_type}/{custom_inference_id} | Create a custom inference endpoint |
| PUT | /_inference/{task_type}/{deepseek_inference_id} | Create a DeepSeek inference endpoint |
| PUT | /_inference/{task_type}/{elasticsearch_inference_id} | Create an Elasticsearch inference endpoint |
| PUT | /_inference/{task_type}/{elser_inference_id} | Create an ELSER inference endpoint |
| PUT | /_inference/{task_type}/{googleaistudio_inference_id} | Create an Google AI Studio inference endpoint |
| PUT | /_inference/{task_type}/{googlevertexai_inference_id} | Create a Google Vertex AI inference endpoint |
| PUT | /_inference/{task_type}/{groq_inference_id} | Create a Groq inference endpoint |
| PUT | /_inference/{task_type}/{huggingface_inference_id} | Create a Hugging Face inference endpoint |
| PUT | /_inference/{task_type}/{jinaai_inference_id} | Create an JinaAI inference endpoint |
| PUT | /_inference/{task_type}/{llama_inference_id} | Create a Llama inference endpoint |
| PUT | /_inference/{task_type}/{mistral_inference_id} | Create a Mistral inference endpoint |
| PUT | /_inference/{task_type}/{nvidia_inference_id} | Create an Nvidia inference endpoint |
| PUT | /_inference/{task_type}/{openai_inference_id} | Create an OpenAI inference endpoint |
| PUT | /_inference/{task_type}/{openshiftai_inference_id} | Create an OpenShift AI inference endpoint |
| PUT | /_inference/{task_type}/{voyageai_inference_id} | Create a VoyageAI inference endpoint |
| PUT | /_inference/{task_type}/{watsonx_inference_id} | Create a Watsonx inference endpoint |
| POST | /_inference/rerank/{inference_id} | Perform reranking inference on the service |
| POST | /_inference/sparse_embedding/{inference_id} | Perform sparse embedding inference on the service |
| POST | /_inference/completion/{inference_id}/_stream | Perform streaming completion inference on the service |
| POST | /_inference/text_embedding/{inference_id} | Perform text embedding inference on the service |
| PUT | /_inference/{inference_id}/_update | Update an inference endpoint |
| PUT | /_inference/{task_type}/{inference_id}/_update | Update an inference endpoint |

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Get cluster info |
| HEAD | / | Ping the cluster |

### _ingest
| Method | Path | Description |
|--------|------|-------------|
| GET | /_ingest/geoip/database/{id} | Get GeoIP database configurations |
| PUT | /_ingest/geoip/database/{id} | Create or update a GeoIP database configuration |
| DELETE | /_ingest/geoip/database/{id} | Delete GeoIP database configurations |
| GET | /_ingest/ip_location/database/{id} | Get IP geolocation database configurations |
| PUT | /_ingest/ip_location/database/{id} | Create or update an IP geolocation database configuration |
| DELETE | /_ingest/ip_location/database/{id} | Delete IP geolocation database configurations |
| GET | /_ingest/pipeline/{id} | Get pipelines |
| PUT | /_ingest/pipeline/{id} | Create or update a pipeline |
| DELETE | /_ingest/pipeline/{id} | Delete pipelines |
| GET | /_ingest/geoip/stats | Get GeoIP statistics |
| GET | /_ingest/geoip/database | Get GeoIP database configurations |
| GET | /_ingest/ip_location/database | Get IP geolocation database configurations |
| GET | /_ingest/pipeline | Get pipelines |
| GET | /_ingest/processor/grok | Run a grok processor |
| GET | /_ingest/pipeline/_simulate | Simulate a pipeline |
| POST | /_ingest/pipeline/_simulate | Simulate a pipeline |
| GET | /_ingest/pipeline/{id}/_simulate | Simulate a pipeline |
| POST | /_ingest/pipeline/{id}/_simulate | Simulate a pipeline |
| GET | /_ingest/_simulate | Simulate data ingestion |
| POST | /_ingest/_simulate | Simulate data ingestion |
| GET | /_ingest/{index}/_simulate | Simulate data ingestion |
| POST | /_ingest/{index}/_simulate | Simulate data ingestion |

### _license
| Method | Path | Description |
|--------|------|-------------|
| GET | /_license | Get license information |
| PUT | /_license | Update the license |
| POST | /_license | Update the license |
| DELETE | /_license | Delete the license |
| GET | /_license/basic_status | Get the basic license status |
| GET | /_license/trial_status | Get the trial status |
| POST | /_license/start_basic | Start a basic license |
| POST | /_license/start_trial | Start a trial |

### _logstash
| Method | Path | Description |
|--------|------|-------------|
| GET | /_logstash/pipeline/{id} | Get Logstash pipelines |
| PUT | /_logstash/pipeline/{id} | Create or update a Logstash pipeline |
| DELETE | /_logstash/pipeline/{id} | Delete a Logstash pipeline |
| GET | /_logstash/pipeline | Get Logstash pipelines |

### _mget
| Method | Path | Description |
|--------|------|-------------|
| GET | /_mget | Get multiple documents |
| POST | /_mget | Get multiple documents |

### _ml
| Method | Path | Description |
|--------|------|-------------|
| POST | /_ml/trained_models/{model_id}/deployment/cache/_clear | Clear trained model deployment cache |
| POST | /_ml/anomaly_detectors/{job_id}/_close | Close anomaly detection jobs |
| GET | /_ml/calendars/{calendar_id} | Get calendar configuration info |
| PUT | /_ml/calendars/{calendar_id} | Create a calendar |
| POST | /_ml/calendars/{calendar_id} | Get calendar configuration info |
| DELETE | /_ml/calendars/{calendar_id} | Delete a calendar |
| DELETE | /_ml/calendars/{calendar_id}/events/{event_id} | Delete events from a calendar |
| PUT | /_ml/calendars/{calendar_id}/jobs/{job_id} | Add anomaly detection job to calendar |
| DELETE | /_ml/calendars/{calendar_id}/jobs/{job_id} | Delete anomaly jobs from a calendar |
| GET | /_ml/data_frame/analytics/{id} | Get data frame analytics job configuration info |
| PUT | /_ml/data_frame/analytics/{id} | Create a data frame analytics job |
| DELETE | /_ml/data_frame/analytics/{id} | Delete a data frame analytics job |
| GET | /_ml/datafeeds/{datafeed_id} | Get datafeeds configuration info |
| PUT | /_ml/datafeeds/{datafeed_id} | Create a datafeed |
| DELETE | /_ml/datafeeds/{datafeed_id} | Delete a datafeed |
| DELETE | /_ml/_delete_expired_data/{job_id} | Delete expired ML data |
| DELETE | /_ml/_delete_expired_data | Delete expired ML data |
| GET | /_ml/filters/{filter_id} | Get filters |
| PUT | /_ml/filters/{filter_id} | Create a filter |
| DELETE | /_ml/filters/{filter_id} | Delete a filter |
| POST | /_ml/anomaly_detectors/{job_id}/_forecast | Predict future behavior of a time series |
| DELETE | /_ml/anomaly_detectors/{job_id}/_forecast | Delete forecasts from a job |
| DELETE | /_ml/anomaly_detectors/{job_id}/_forecast/{forecast_id} | Delete forecasts from a job |
| GET | /_ml/anomaly_detectors/{job_id} | Get anomaly detection jobs configuration info |
| PUT | /_ml/anomaly_detectors/{job_id} | Create an anomaly detection job |
| DELETE | /_ml/anomaly_detectors/{job_id} | Delete an anomaly detection job |
| GET | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id} | Get model snapshots info |
| POST | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id} | Get model snapshots info |
| DELETE | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id} | Delete a model snapshot |
| GET | /_ml/trained_models/{model_id} | Get trained model configuration info |
| PUT | /_ml/trained_models/{model_id} | Create a trained model |
| DELETE | /_ml/trained_models/{model_id} | Delete an unreferenced trained model |
| PUT | /_ml/trained_models/{model_id}/model_aliases/{model_alias} | Create or update a trained model alias |
| DELETE | /_ml/trained_models/{model_id}/model_aliases/{model_alias} | Delete a trained model alias |
| POST | /_ml/anomaly_detectors/_estimate_model_memory | Estimate job model memory usage |
| POST | /_ml/data_frame/_evaluate | Evaluate data frame analytics |
| GET | /_ml/data_frame/analytics/_explain | Explain data frame analytics config |
| POST | /_ml/data_frame/analytics/_explain | Explain data frame analytics config |
| GET | /_ml/data_frame/analytics/{id}/_explain | Explain data frame analytics config |
| POST | /_ml/data_frame/analytics/{id}/_explain | Explain data frame analytics config |
| POST | /_ml/anomaly_detectors/{job_id}/_flush | Force buffered data to be processed |
| GET | /_ml/anomaly_detectors/{job_id}/results/buckets/{timestamp} | Get anomaly detection job results for buckets |
| POST | /_ml/anomaly_detectors/{job_id}/results/buckets/{timestamp} | Get anomaly detection job results for buckets |
| GET | /_ml/anomaly_detectors/{job_id}/results/buckets | Get anomaly detection job results for buckets |
| POST | /_ml/anomaly_detectors/{job_id}/results/buckets | Get anomaly detection job results for buckets |
| GET | /_ml/calendars/{calendar_id}/events | Get info about events in calendars |
| POST | /_ml/calendars/{calendar_id}/events | Add scheduled events to the calendar |
| GET | /_ml/calendars | Get calendar configuration info |
| POST | /_ml/calendars | Get calendar configuration info |
| GET | /_ml/anomaly_detectors/{job_id}/results/categories/{category_id} | Get anomaly detection job results for categories |
| POST | /_ml/anomaly_detectors/{job_id}/results/categories/{category_id} | Get anomaly detection job results for categories |
| GET | /_ml/anomaly_detectors/{job_id}/results/categories | Get anomaly detection job results for categories |
| POST | /_ml/anomaly_detectors/{job_id}/results/categories | Get anomaly detection job results for categories |
| GET | /_ml/data_frame/analytics | Get data frame analytics job configuration info |
| GET | /_ml/data_frame/analytics/_stats | Get data frame analytics job stats |
| GET | /_ml/data_frame/analytics/{id}/_stats | Get data frame analytics job stats |
| GET | /_ml/datafeeds/{datafeed_id}/_stats | Get datafeed stats |
| GET | /_ml/datafeeds/_stats | Get datafeed stats |
| GET | /_ml/datafeeds | Get datafeeds configuration info |
| GET | /_ml/filters | Get filters |
| GET | /_ml/anomaly_detectors/{job_id}/results/influencers | Get anomaly detection job results for influencers |
| POST | /_ml/anomaly_detectors/{job_id}/results/influencers | Get anomaly detection job results for influencers |
| GET | /_ml/anomaly_detectors/_stats | Get anomaly detection job stats |
| GET | /_ml/anomaly_detectors/{job_id}/_stats | Get anomaly detection job stats |
| GET | /_ml/anomaly_detectors | Get anomaly detection jobs configuration info |
| GET | /_ml/memory/_stats | Get machine learning memory usage info |
| GET | /_ml/memory/{node_id}/_stats | Get machine learning memory usage info |
| GET | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_upgrade/_stats | Get anomaly detection job model snapshot upgrade usage info |
| GET | /_ml/anomaly_detectors/{job_id}/model_snapshots | Get model snapshots info |
| POST | /_ml/anomaly_detectors/{job_id}/model_snapshots | Get model snapshots info |
| GET | /_ml/anomaly_detectors/{job_id}/results/overall_buckets | Get overall bucket results |
| POST | /_ml/anomaly_detectors/{job_id}/results/overall_buckets | Get overall bucket results |
| GET | /_ml/anomaly_detectors/{job_id}/results/records | Get anomaly records for an anomaly detection job |
| POST | /_ml/anomaly_detectors/{job_id}/results/records | Get anomaly records for an anomaly detection job |
| GET | /_ml/trained_models | Get trained model configuration info |
| GET | /_ml/trained_models/{model_id}/_stats | Get trained models usage info |
| GET | /_ml/trained_models/_stats | Get trained models usage info |
| POST | /_ml/trained_models/{model_id}/_infer | Evaluate a trained model |
| GET | /_ml/info | Get machine learning information |
| POST | /_ml/anomaly_detectors/{job_id}/_open | Open anomaly detection jobs |
| POST | /_ml/anomaly_detectors/{job_id}/_data | Send data to an anomaly detection job for analysis |
| GET | /_ml/data_frame/analytics/_preview | Preview features used by data frame analytics |
| POST | /_ml/data_frame/analytics/_preview | Preview features used by data frame analytics |
| GET | /_ml/data_frame/analytics/{id}/_preview | Preview features used by data frame analytics |
| POST | /_ml/data_frame/analytics/{id}/_preview | Preview features used by data frame analytics |
| GET | /_ml/datafeeds/{datafeed_id}/_preview | Preview a datafeed |
| POST | /_ml/datafeeds/{datafeed_id}/_preview | Preview a datafeed |
| GET | /_ml/datafeeds/_preview | Preview a datafeed |
| POST | /_ml/datafeeds/_preview | Preview a datafeed |
| PUT | /_ml/trained_models/{model_id}/definition/{part} | Create part of a trained model definition |
| PUT | /_ml/trained_models/{model_id}/vocabulary | Create a trained model vocabulary |
| POST | /_ml/anomaly_detectors/{job_id}/_reset | Reset an anomaly detection job |
| POST | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_revert | Revert to a snapshot |
| POST | /_ml/set_upgrade_mode | Set upgrade_mode for ML indices |
| POST | /_ml/data_frame/analytics/{id}/_start | Start a data frame analytics job |
| POST | /_ml/datafeeds/{datafeed_id}/_start | Start datafeeds |
| POST | /_ml/trained_models/{model_id}/deployment/_start | Start a trained model deployment |
| POST | /_ml/data_frame/analytics/{id}/_stop | Stop data frame analytics jobs |
| POST | /_ml/datafeeds/{datafeed_id}/_stop | Stop datafeeds |
| POST | /_ml/trained_models/{model_id}/deployment/_stop | Stop a trained model deployment |
| POST | /_ml/data_frame/analytics/{id}/_update | Update a data frame analytics job |
| POST | /_ml/datafeeds/{datafeed_id}/_update | Update a datafeed |
| POST | /_ml/filters/{filter_id}/_update | Update a filter |
| POST | /_ml/anomaly_detectors/{job_id}/_update | Update an anomaly detection job |
| POST | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_update | Update a snapshot |
| POST | /_ml/trained_models/{model_id}/deployment/_update | Update a trained model deployment |
| POST | /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_upgrade | Upgrade a snapshot |

### _msearch
| Method | Path | Description |
|--------|------|-------------|
| GET | /_msearch | Run multiple searches |
| POST | /_msearch | Run multiple searches |
| GET | /_msearch/template | Run multiple templated searches |
| POST | /_msearch/template | Run multiple templated searches |

### _mtermvectors
| Method | Path | Description |
|--------|------|-------------|
| GET | /_mtermvectors | Get multiple term vectors |
| POST | /_mtermvectors | Get multiple term vectors |

### _nodes
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /_nodes/{node_id}/_repositories_metering/{max_archive_version} | Clear the archived repositories metering |
| GET | /_nodes/{node_id}/_repositories_metering | Get cluster repositories metering |
| GET | /_nodes/hot_threads | Get the hot threads for nodes |
| GET | /_nodes/{node_id}/hot_threads | Get the hot threads for nodes |
| GET | /_nodes | Get node information |
| GET | /_nodes/{node_id} | Get node information |
| GET | /_nodes/{metric} | Get node information |
| GET | /_nodes/{node_id}/{metric} | Get node information |
| POST | /_nodes/reload_secure_settings | Reload the keystore on nodes in the cluster |
| POST | /_nodes/{node_id}/reload_secure_settings | Reload the keystore on nodes in the cluster |
| GET | /_nodes/stats | Get node statistics |
| GET | /_nodes/{node_id}/stats | Get node statistics |
| GET | /_nodes/stats/{metric} | Get node statistics |
| GET | /_nodes/{node_id}/stats/{metric} | Get node statistics |
| GET | /_nodes/stats/{metric}/{index_metric} | Get node statistics |
| GET | /_nodes/{node_id}/stats/{metric}/{index_metric} | Get node statistics |
| GET | /_nodes/usage | Get feature usage information |
| GET | /_nodes/{node_id}/usage | Get feature usage information |
| GET | /_nodes/usage/{metric} | Get feature usage information |
| GET | /_nodes/{node_id}/usage/{metric} | Get feature usage information |

### _query_rules
| Method | Path | Description |
|--------|------|-------------|
| GET | /_query_rules/{ruleset_id}/_rule/{rule_id} | Get a query rule |
| PUT | /_query_rules/{ruleset_id}/_rule/{rule_id} | Create or update a query rule |
| DELETE | /_query_rules/{ruleset_id}/_rule/{rule_id} | Delete a query rule |
| GET | /_query_rules/{ruleset_id} | Get a query ruleset |
| PUT | /_query_rules/{ruleset_id} | Create or update a query ruleset |
| DELETE | /_query_rules/{ruleset_id} | Delete a query ruleset |
| GET | /_query_rules | Get all query rulesets |
| POST | /_query_rules/{ruleset_id}/_test | Test a query ruleset |

### _rank_eval
| Method | Path | Description |
|--------|------|-------------|
| GET | /_rank_eval | Evaluate ranked search results |
| POST | /_rank_eval | Evaluate ranked search results |

### _reindex
| Method | Path | Description |
|--------|------|-------------|
| POST | /_reindex | Reindex documents |
| POST | /_reindex/{task_id}/_rethrottle | Throttle a reindex operation |

### _render
| Method | Path | Description |
|--------|------|-------------|
| GET | /_render/template | Render a search template |
| POST | /_render/template | Render a search template |
| GET | /_render/template/{id} | Render a search template |
| POST | /_render/template/{id} | Render a search template |

### _rollup
| Method | Path | Description |
|--------|------|-------------|
| GET | /_rollup/job/{id} | Get rollup job information |
| PUT | /_rollup/job/{id} | Create a rollup job |
| DELETE | /_rollup/job/{id} | Delete a rollup job |
| GET | /_rollup/job | Get rollup job information |
| GET | /_rollup/data/{id} | Get the rollup job capabilities |
| GET | /_rollup/data | Get the rollup job capabilities |
| POST | /_rollup/job/{id}/_start | Start rollup jobs |
| POST | /_rollup/job/{id}/_stop | Stop rollup jobs |

### _application
| Method | Path | Description |
|--------|------|-------------|
| GET | /_application/search_application/{name} | Get search application details |
| PUT | /_application/search_application/{name} | Create or update a search application |
| DELETE | /_application/search_application/{name} | Delete a search application |
| GET | /_application/analytics/{name} | Get behavioral analytics collections |
| PUT | /_application/analytics/{name} | Create a behavioral analytics collection |
| DELETE | /_application/analytics/{name} | Delete a behavioral analytics collection |
| GET | /_application/analytics | Get behavioral analytics collections |
| GET | /_application/search_application | Get search applications |
| POST | /_application/analytics/{collection_name}/event/{event_type} | Create a behavioral analytics collection event |
| POST | /_application/search_application/{name}/_render_query | Render a search application query |
| GET | /_application/search_application/{name}/_search | Run a search application search |
| POST | /_application/search_application/{name}/_search | Run a search application search |

### _search_shards
| Method | Path | Description |
|--------|------|-------------|
| GET | /_search_shards | Get the search shards |
| POST | /_search_shards | Get the search shards |

### _searchable_snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /_searchable_snapshots/cache/stats | Get cache statistics |
| GET | /_searchable_snapshots/{node_id}/cache/stats | Get cache statistics |
| POST | /_searchable_snapshots/cache/clear | Clear the cache |
| GET | /_searchable_snapshots/stats | Get searchable snapshot statistics |

### _snapshot
| Method | Path | Description |
|--------|------|-------------|
| POST | /_snapshot/{repository}/{snapshot}/_mount | Mount a snapshot |
| POST | /_snapshot/{repository}/_cleanup | Clean up the snapshot repository |
| PUT | /_snapshot/{repository}/{snapshot}/_clone/{target_snapshot} | Clone a snapshot |
| GET | /_snapshot/{repository}/{snapshot} | Get snapshot information |
| PUT | /_snapshot/{repository}/{snapshot} | Create a snapshot |
| POST | /_snapshot/{repository}/{snapshot} | Create a snapshot |
| DELETE | /_snapshot/{repository}/{snapshot} | Delete snapshots |
| GET | /_snapshot/{repository} | Get snapshot repository information |
| PUT | /_snapshot/{repository} | Create or update a snapshot repository |
| POST | /_snapshot/{repository} | Create or update a snapshot repository |
| DELETE | /_snapshot/{repository} | Delete snapshot repositories |
| GET | /_snapshot | Get snapshot repository information |
| POST | /_snapshot/{repository}/_analyze | Analyze a snapshot repository |
| POST | /_snapshot/{repository}/_verify_integrity | Verify the repository integrity |
| POST | /_snapshot/{repository}/{snapshot}/_restore | Restore a snapshot |
| GET | /_snapshot/_status | Get the snapshot status |
| GET | /_snapshot/{repository}/_status | Get the snapshot status |
| GET | /_snapshot/{repository}/{snapshot}/_status | Get the snapshot status |
| POST | /_snapshot/{repository}/_verify | Verify a snapshot repository |

### _security
| Method | Path | Description |
|--------|------|-------------|
| POST | /_security/profile/_activate | Activate a user profile |
| GET | /_security/_authenticate | Authenticate a user |
| GET | /_security/role | Get roles |
| POST | /_security/role | Bulk create or update roles |
| DELETE | /_security/role | Bulk delete roles |
| POST | /_security/api_key/_bulk_update | Bulk update API keys |
| PUT | /_security/user/{username}/_password | Change passwords |
| POST | /_security/user/{username}/_password | Change passwords |
| PUT | /_security/user/_password | Change passwords |
| POST | /_security/user/_password | Change passwords |
| POST | /_security/api_key/{ids}/_clear_cache | Clear the API key cache |
| POST | /_security/privilege/{application}/_clear_cache | Clear the privileges cache |
| POST | /_security/realm/{realms}/_clear_cache | Clear the user cache |
| POST | /_security/role/{name}/_clear_cache | Clear the roles cache |
| POST | /_security/service/{namespace}/{service}/credential/token/{name}/_clear_cache | Clear service account token caches |
| GET | /_security/api_key | Get API key information |
| PUT | /_security/api_key | Create an API key |
| POST | /_security/api_key | Create an API key |
| DELETE | /_security/api_key | Invalidate API keys |
| POST | /_security/cross_cluster/api_key | Create a cross-cluster API key |
| PUT | /_security/service/{namespace}/{service}/credential/token/{name} | Create a service account token |
| POST | /_security/service/{namespace}/{service}/credential/token/{name} | Create a service account token |
| DELETE | /_security/service/{namespace}/{service}/credential/token/{name} | Delete service account tokens |
| POST | /_security/service/{namespace}/{service}/credential/token | Create a service account token |
| POST | /_security/delegate_pki | Delegate PKI authentication |
| GET | /_security/privilege/{application}/{name} | Get application privileges |
| DELETE | /_security/privilege/{application}/{name} | Delete application privileges |
| GET | /_security/role/{name} | Get roles |
| PUT | /_security/role/{name} | Create or update roles |
| POST | /_security/role/{name} | Create or update roles |
| DELETE | /_security/role/{name} | Delete roles |
| GET | /_security/role_mapping/{name} | Get role mappings |
| PUT | /_security/role_mapping/{name} | Create or update role mappings |
| POST | /_security/role_mapping/{name} | Create or update role mappings |
| DELETE | /_security/role_mapping/{name} | Delete role mappings |
| GET | /_security/user/{username} | Get users |
| PUT | /_security/user/{username} | Create or update users |
| POST | /_security/user/{username} | Create or update users |
| DELETE | /_security/user/{username} | Delete users |
| PUT | /_security/user/{username}/_disable | Disable users |
| POST | /_security/user/{username}/_disable | Disable users |
| PUT | /_security/profile/{uid}/_disable | Disable a user profile |
| POST | /_security/profile/{uid}/_disable | Disable a user profile |
| PUT | /_security/user/{username}/_enable | Enable users |
| POST | /_security/user/{username}/_enable | Enable users |
| PUT | /_security/profile/{uid}/_enable | Enable a user profile |
| POST | /_security/profile/{uid}/_enable | Enable a user profile |
| GET | /_security/enroll/kibana | Enroll Kibana |
| GET | /_security/enroll/node | Enroll a node |
| GET | /_security/privilege/_builtin | Get builtin privileges |
| GET | /_security/privilege | Get application privileges |
| PUT | /_security/privilege | Create or update application privileges |
| POST | /_security/privilege | Create or update application privileges |
| GET | /_security/privilege/{application} | Get application privileges |
| GET | /_security/role_mapping | Get role mappings |
| GET | /_security/service/{namespace}/{service} | Get service accounts |
| GET | /_security/service/{namespace} | Get service accounts |
| GET | /_security/service | Get service accounts |
| GET | /_security/service/{namespace}/{service}/credential | Get service account credentials |
| GET | /_security/settings | Get security index settings |
| PUT | /_security/settings | Update security index settings |
| GET | /_security/stats | Get security stats |
| POST | /_security/oauth2/token | Get a token |
| DELETE | /_security/oauth2/token | Invalidate a token |
| GET | /_security/user | Get users |
| GET | /_security/user/_privileges | Get user privileges |
| GET | /_security/profile/{uid} | Get a user profile |
| POST | /_security/api_key/grant | Grant an API key |
| GET | /_security/user/_has_privileges | Check user privileges |
| POST | /_security/user/_has_privileges | Check user privileges |
| GET | /_security/user/{user}/_has_privileges | Check user privileges |
| POST | /_security/user/{user}/_has_privileges | Check user privileges |
| GET | /_security/profile/_has_privileges | Check user profile privileges |
| POST | /_security/profile/_has_privileges | Check user profile privileges |
| POST | /_security/oidc/authenticate | Authenticate OpenID Connect |
| POST | /_security/oidc/logout | Logout of OpenID Connect |
| POST | /_security/oidc/prepare | Prepare OpenID connect authentication |
| GET | /_security/_query/api_key | Find API keys with a query |
| POST | /_security/_query/api_key | Find API keys with a query |
| GET | /_security/_query/role | Find roles with a query |
| POST | /_security/_query/role | Find roles with a query |
| GET | /_security/_query/user | Find users with a query |
| POST | /_security/_query/user | Find users with a query |
| POST | /_security/saml/authenticate | Authenticate SAML |
| POST | /_security/saml/complete_logout | Logout of SAML completely |
| POST | /_security/saml/invalidate | Invalidate SAML |
| POST | /_security/saml/logout | Logout of SAML |
| POST | /_security/saml/prepare | Prepare SAML authentication |
| GET | /_security/saml/metadata/{realm_name} | Create SAML service provider metadata |
| GET | /_security/profile/_suggest | Suggest a user profile |
| POST | /_security/profile/_suggest | Suggest a user profile |
| PUT | /_security/api_key/{id} | Update an API key |
| PUT | /_security/cross_cluster/api_key/{id} | Update a cross-cluster API key |
| PUT | /_security/profile/{uid}/_data | Update user profile data |
| POST | /_security/profile/{uid}/_data | Update user profile data |

### _slm
| Method | Path | Description |
|--------|------|-------------|
| GET | /_slm/policy/{policy_id} | Get policy information |
| PUT | /_slm/policy/{policy_id} | Create or update a policy |
| DELETE | /_slm/policy/{policy_id} | Delete a policy |
| PUT | /_slm/policy/{policy_id}/_execute | Run a policy |
| POST | /_slm/_execute_retention | Run a retention policy |
| GET | /_slm/policy | Get policy information |
| GET | /_slm/stats | Get snapshot lifecycle management statistics |
| GET | /_slm/status | Get the snapshot lifecycle management status |
| POST | /_slm/start | Start snapshot lifecycle management |
| POST | /_slm/stop | Stop snapshot lifecycle management |

### _sql
| Method | Path | Description |
|--------|------|-------------|
| POST | /_sql/close | Clear an SQL search cursor |
| DELETE | /_sql/async/delete/{id} | Delete an async SQL search |
| GET | /_sql/async/{id} | Get async SQL search results |
| GET | /_sql/async/status/{id} | Get the async SQL search status |
| GET | /_sql | Get SQL search results |
| POST | /_sql | Get SQL search results |
| GET | /_sql/translate | Translate SQL into Elasticsearch queries |
| POST | /_sql/translate | Translate SQL into Elasticsearch queries |

### _ssl
| Method | Path | Description |
|--------|------|-------------|
| GET | /_ssl/certificates | Get SSL certificates |

### _streams
| Method | Path | Description |
|--------|------|-------------|
| POST | /_streams/{name}/_disable | Disable a named stream |
| POST | /_streams/{name}/_enable | Enable a named stream |
| GET | /_streams/status | Get the status of streams |

### _synonyms
| Method | Path | Description |
|--------|------|-------------|
| GET | /_synonyms/{id} | Get a synonym set |
| PUT | /_synonyms/{id} | Create or update a synonym set |
| DELETE | /_synonyms/{id} | Delete a synonym set |
| GET | /_synonyms/{set_id}/{rule_id} | Get a synonym rule |
| PUT | /_synonyms/{set_id}/{rule_id} | Create or update a synonym rule |
| DELETE | /_synonyms/{set_id}/{rule_id} | Delete a synonym rule |
| GET | /_synonyms | Get all synonym sets |

### _tasks
| Method | Path | Description |
|--------|------|-------------|
| POST | /_tasks/_cancel | Cancel a task |
| POST | /_tasks/{task_id}/_cancel | Cancel a task |
| GET | /_tasks/{task_id} | Get task information |
| GET | /_tasks | Get all tasks |

### _text_structure
| Method | Path | Description |
|--------|------|-------------|
| GET | /_text_structure/find_field_structure | Find the structure of a text field |
| GET | /_text_structure/find_message_structure | Find the structure of text messages |
| POST | /_text_structure/find_message_structure | Find the structure of text messages |
| POST | /_text_structure/find_structure | Find the structure of a text file |
| GET | /_text_structure/test_grok_pattern | Test a Grok pattern |
| POST | /_text_structure/test_grok_pattern | Test a Grok pattern |

### _transform
| Method | Path | Description |
|--------|------|-------------|
| GET | /_transform/{transform_id} | Get transforms |
| PUT | /_transform/{transform_id} | Create a transform |
| DELETE | /_transform/{transform_id} | Delete a transform |
| GET | /_transform/_node_stats | Get node stats |
| GET | /_transform | Get transforms |
| GET | /_transform/{transform_id}/_stats | Get transform stats |
| GET | /_transform/{transform_id}/_preview | Preview a transform |
| POST | /_transform/{transform_id}/_preview | Preview a transform |
| GET | /_transform/_preview | Preview a transform |
| POST | /_transform/_preview | Preview a transform |
| POST | /_transform/{transform_id}/_reset | Reset a transform |
| POST | /_transform/{transform_id}/_schedule_now | Schedule a transform to start now |
| POST | /_transform/set_upgrade_mode | Set upgrade_mode for transform indices |
| POST | /_transform/{transform_id}/_start | Start a transform |
| POST | /_transform/{transform_id}/_stop | Stop transforms |
| POST | /_transform/{transform_id}/_update | Update a transform |
| POST | /_transform/_upgrade | Upgrade all transforms |

### _update_by_query
| Method | Path | Description |
|--------|------|-------------|
| POST | /_update_by_query/{task_id}/_rethrottle | Throttle an update by query operation |

### _watcher
| Method | Path | Description |
|--------|------|-------------|
| PUT | /_watcher/watch/{watch_id}/_ack | Acknowledge a watch |
| POST | /_watcher/watch/{watch_id}/_ack | Acknowledge a watch |
| PUT | /_watcher/watch/{watch_id}/_ack/{action_id} | Acknowledge a watch |
| POST | /_watcher/watch/{watch_id}/_ack/{action_id} | Acknowledge a watch |
| PUT | /_watcher/watch/{watch_id}/_activate | Activate a watch |
| POST | /_watcher/watch/{watch_id}/_activate | Activate a watch |
| PUT | /_watcher/watch/{watch_id}/_deactivate | Deactivate a watch |
| POST | /_watcher/watch/{watch_id}/_deactivate | Deactivate a watch |
| GET | /_watcher/watch/{id} | Get a watch |
| PUT | /_watcher/watch/{id} | Create or update a watch |
| POST | /_watcher/watch/{id} | Create or update a watch |
| DELETE | /_watcher/watch/{id} | Delete a watch |
| PUT | /_watcher/watch/{id}/_execute | Run a watch |
| POST | /_watcher/watch/{id}/_execute | Run a watch |
| PUT | /_watcher/watch/_execute | Run a watch |
| POST | /_watcher/watch/_execute | Run a watch |
| GET | /_watcher/settings | Get Watcher index settings |
| PUT | /_watcher/settings | Update Watcher index settings |
| GET | /_watcher/_query/watches | Query watches |
| POST | /_watcher/_query/watches | Query watches |
| POST | /_watcher/_start | Start the watch service |
| GET | /_watcher/stats | Get Watcher statistics |
| GET | /_watcher/stats/{metric} | Get Watcher statistics |
| POST | /_watcher/_stop | Stop the watch service |

### _xpack
| Method | Path | Description |
|--------|------|-------------|
| GET | /_xpack | Get information |
| GET | /_xpack/usage | Get usage information |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get _async_search details?" -> GET /_async_search/{id}
- "Delete a _async_search?" -> DELETE /_async_search/{id}
- "Get status details?" -> GET /_async_search/status/{id}
- "Create a _async_search?" -> POST /_async_search
- "Create a _async_search?" -> POST /{index}/_async_search
- "Create a _bulk?" -> POST /_bulk
- "Create a _bulk?" -> POST /{index}/_bulk
- "List all aliases?" -> GET /_cat/aliases
- "Get aliase details?" -> GET /_cat/aliases/{name}
- "List all allocation?" -> GET /_cat/allocation
- "Get allocation details?" -> GET /_cat/allocation/{node_id}
- "List all circuit_breaker?" -> GET /_cat/circuit_breaker
- "Get circuit_breaker details?" -> GET /_cat/circuit_breaker/{circuit_breaker_patterns}
- "List all component_templates?" -> GET /_cat/component_templates
- "Get component_template details?" -> GET /_cat/component_templates/{name}
- "List all count?" -> GET /_cat/count
- "Create a count?" -> POST /_cat/count
- "Get count details?" -> GET /_cat/count/{index}
- "List all fielddata?" -> GET /_cat/fielddata
- "Get fielddata details?" -> GET /_cat/fielddata/{fields}
- "List all health?" -> GET /_cat/health
- "List all _cat?" -> GET /_cat
- "List all indices?" -> GET /_cat/indices
- "Get indice details?" -> GET /_cat/indices/{index}
- "List all master?" -> GET /_cat/master
- "List all analytics?" -> GET /_cat/ml/data_frame/analytics
- "Get analytic details?" -> GET /_cat/ml/data_frame/analytics/{id}
- "List all datafeeds?" -> GET /_cat/ml/datafeeds
- "Get datafeed details?" -> GET /_cat/ml/datafeeds/{datafeed_id}
- "List all anomaly_detectors?" -> GET /_cat/ml/anomaly_detectors
- "Get anomaly_detector details?" -> GET /_cat/ml/anomaly_detectors/{job_id}
- "List all trained_models?" -> GET /_cat/ml/trained_models
- "Get trained_model details?" -> GET /_cat/ml/trained_models/{model_id}
- "List all nodeattrs?" -> GET /_cat/nodeattrs
- "List all nodes?" -> GET /_cat/nodes
- "List all pending_tasks?" -> GET /_cat/pending_tasks
- "List all plugins?" -> GET /_cat/plugins
- "List all recovery?" -> GET /_cat/recovery
- "Get recovery details?" -> GET /_cat/recovery/{index}
- "List all repositories?" -> GET /_cat/repositories
- "List all segments?" -> GET /_cat/segments
- "Get segment details?" -> GET /_cat/segments/{index}
- "List all shards?" -> GET /_cat/shards
- "Get shard details?" -> GET /_cat/shards/{index}
- "List all snapshots?" -> GET /_cat/snapshots
- "Get snapshot details?" -> GET /_cat/snapshots/{repository}
- "List all tasks?" -> GET /_cat/tasks
- "List all templates?" -> GET /_cat/templates
- "Get template details?" -> GET /_cat/templates/{name}
- "List all thread_pool?" -> GET /_cat/thread_pool
- "Get thread_pool details?" -> GET /_cat/thread_pool/{thread_pool_patterns}
- "List all transforms?" -> GET /_cat/transforms
- "Get transform details?" -> GET /_cat/transforms/{transform_id}
- "Get auto_follow details?" -> GET /_ccr/auto_follow/{name}
- "Update a auto_follow?" -> PUT /_ccr/auto_follow/{name}
- "Delete a auto_follow?" -> DELETE /_ccr/auto_follow/{name}
- "List all info?" -> GET /{index}/_ccr/info
- "List all stats?" -> GET /{index}/_ccr/stats
- "Create a forget_follower?" -> POST /{index}/_ccr/forget_follower
- "List all auto_follow?" -> GET /_ccr/auto_follow
- "Create a pause?" -> POST /_ccr/auto_follow/{name}/pause
- "Create a pause_follow?" -> POST /{index}/_ccr/pause_follow
- "Create a resume?" -> POST /_ccr/auto_follow/{name}/resume
- "Create a resume_follow?" -> POST /{index}/_ccr/resume_follow
- "List all stats?" -> GET /_ccr/stats
- "Create a unfollow?" -> POST /{index}/_ccr/unfollow
- "List all scroll?" -> GET /_search/scroll
- "Create a scroll?" -> POST /_search/scroll
- "Get scroll details?" -> GET /_search/scroll/{scroll_id}
- "Delete a scroll?" -> DELETE /_search/scroll/{scroll_id}
- "List all explain?" -> GET /_cluster/allocation/explain
- "Create a explain?" -> POST /_cluster/allocation/explain
- "Get _component_template details?" -> GET /_component_template/{name}
- "Update a _component_template?" -> PUT /_component_template/{name}
- "Delete a _component_template?" -> DELETE /_component_template/{name}
- "Create a voting_config_exclusion?" -> POST /_cluster/voting_config_exclusions
- "List all _component_template?" -> GET /_component_template
- "List all settings?" -> GET /_cluster/settings
- "List all health?" -> GET /_cluster/health
- "Get health details?" -> GET /_cluster/health/{index}
- "Get _info details?" -> GET /_info/{target}
- "List all pending_tasks?" -> GET /_cluster/pending_tasks
- "List all info?" -> GET /_remote/info
- "Create a reroute?" -> POST /_cluster/reroute
- "List all state?" -> GET /_cluster/state
- "Get state details?" -> GET /_cluster/state/{metric}
- "Get state details?" -> GET /_cluster/state/{metric}/{index}
- "List all stats?" -> GET /_cluster/stats
- "Get node details?" -> GET /_cluster/stats/nodes/{node_id}
- "Get _connector details?" -> GET /_connector/{connector_id}
- "Update a _connector?" -> PUT /_connector/{connector_id}
- "Delete a _connector?" -> DELETE /_connector/{connector_id}
- "Search _connector?" -> GET /_connector
- "Create a _connector?" -> POST /_connector
- "Get _sync_job details?" -> GET /_connector/_sync_job/{connector_sync_job_id}
- "Delete a _sync_job?" -> DELETE /_connector/_sync_job/{connector_sync_job_id}
- "List all _sync_job?" -> GET /_connector/_sync_job
- "Create a _sync_job?" -> POST /_connector/_sync_job
- "Search _count?" -> GET /_count
- "Create a _count?" -> POST /_count
- "Search _count?" -> GET /{index}/_count
- "Create a _count?" -> POST /{index}/_count
- "Update a _create?" -> PUT /{index}/_create/{id}
- "Delete a _dangling?" -> DELETE /_dangling/{index_uuid}
- "List all _dangling?" -> GET /_dangling
- "Get _doc details?" -> GET /{index}/_doc/{id}
- "Update a _doc?" -> PUT /{index}/_doc/{id}
- "Delete a _doc?" -> DELETE /{index}/_doc/{id}
- "Create a _delete_by_query?" -> POST /{index}/_delete_by_query
- "Create a _rethrottle?" -> POST /_delete_by_query/{task_id}/_rethrottle
- "Get _script details?" -> GET /_scripts/{id}
- "Update a _script?" -> PUT /_scripts/{id}
- "Delete a _script?" -> DELETE /_scripts/{id}
- "Get policy details?" -> GET /_enrich/policy/{name}
- "Update a policy?" -> PUT /_enrich/policy/{name}
- "Delete a policy?" -> DELETE /_enrich/policy/{name}
- "List all policy?" -> GET /_enrich/policy
- "List all _stats?" -> GET /_enrich/_stats
- "Get search details?" -> GET /_eql/search/{id}
- "Delete a search?" -> DELETE /_eql/search/{id}
- "Get status details?" -> GET /_eql/search/status/{id}
- "Search search?" -> GET /{index}/_eql/search
- "Create a search?" -> POST /{index}/_eql/search
- "Create a async?" -> POST /_query/async
- "Get async details?" -> GET /_query/async/{id}
- "Delete a async?" -> DELETE /_query/async/{id}
- "Create a stop?" -> POST /_query/async/{id}/stop
- "Get query details?" -> GET /_query/queries/{id}
- "List all queries?" -> GET /_query/queries
- "Create a _query?" -> POST /_query
- "Get _source details?" -> GET /{index}/_source/{id}
- "Search _explain?" -> GET /{index}/_explain/{id}
- "List all _features?" -> GET /_features
- "Create a _reset?" -> POST /_features/_reset
- "List all _field_caps?" -> GET /_field_caps
- "Create a _field_cap?" -> POST /_field_caps
- "List all _field_caps?" -> GET /{index}/_field_caps
- "Create a _field_cap?" -> POST /{index}/_field_caps
- "List all global_checkpoints?" -> GET /{index}/_fleet/global_checkpoints
- "List all _fleet_msearch?" -> GET /_fleet/_fleet_msearch
- "Create a _fleet_msearch?" -> POST /_fleet/_fleet_msearch
- "List all _fleet_msearch?" -> GET /{index}/_fleet/_fleet_msearch
- "Create a _fleet_msearch?" -> POST /{index}/_fleet/_fleet_msearch
- "Search _fleet_search?" -> GET /{index}/_fleet/_fleet_search
- "Create a _fleet_search?" -> POST /{index}/_fleet/_fleet_search
- "List all _script_context?" -> GET /_script_context
- "List all _script_language?" -> GET /_script_language
- "Search explore?" -> GET /{index}/_graph/explore
- "Create a explore?" -> POST /{index}/_graph/explore
- "List all _health_report?" -> GET /_health_report
- "Get _health_report details?" -> GET /_health_report/{feature}
- "Get policy details?" -> GET /_ilm/policy/{policy}
- "Update a policy?" -> PUT /_ilm/policy/{policy}
- "Delete a policy?" -> DELETE /_ilm/policy/{policy}
- "List all explain?" -> GET /{index}/_ilm/explain
- "List all policy?" -> GET /_ilm/policy
- "List all status?" -> GET /_ilm/status
- "Create a migrate_to_data_tier?" -> POST /_ilm/migrate_to_data_tiers
- "Create a remove?" -> POST /{index}/_ilm/remove
- "Create a retry?" -> POST /{index}/_ilm/retry
- "Create a start?" -> POST /_ilm/start
- "Create a stop?" -> POST /_ilm/stop
- "Create a _doc?" -> POST /{index}/_doc
- "Update a _block?" -> PUT /{index}/_block/{block}
- "Delete a _block?" -> DELETE /{index}/_block/{block}
- "List all _analyze?" -> GET /_analyze
- "Create a _analyze?" -> POST /_analyze
- "List all _analyze?" -> GET /{index}/_analyze
- "Create a _analyze?" -> POST /{index}/_analyze
- "Create a _cancel?" -> POST /_migration/reindex/{index}/_cancel
- "Create a clear?" -> POST /_cache/clear
- "Create a clear?" -> POST /{index}/_cache/clear
- "Update a _clone?" -> PUT /{index}/_clone/{target}
- "Create a _close?" -> POST /{index}/_close
- "Get _data_stream details?" -> GET /_data_stream/{name}
- "Update a _data_stream?" -> PUT /_data_stream/{name}
- "Delete a _data_stream?" -> DELETE /_data_stream/{name}
- "Update a _create_from?" -> PUT /_create_from/{source}/{dest}
- "List all _stats?" -> GET /_data_stream/_stats
- "List all _stats?" -> GET /_data_stream/{name}/_stats
- "Get _alia details?" -> GET /{index}/_alias/{name}
- "Update a _alia?" -> PUT /{index}/_alias/{name}
- "Delete a _alia?" -> DELETE /{index}/_alias/{name}
- "Update a _aliase?" -> PUT /{index}/_aliases/{name}
- "Delete a _aliase?" -> DELETE /{index}/_aliases/{name}
- "List all _lifecycle?" -> GET /_data_stream/{name}/_lifecycle
- "List all _options?" -> GET /_data_stream/{name}/_options
- "Get _index_template details?" -> GET /_index_template/{name}
- "Update a _index_template?" -> PUT /_index_template/{name}
- "Delete a _index_template?" -> DELETE /_index_template/{name}
- "Get _template details?" -> GET /_template/{name}
- "Update a _template?" -> PUT /_template/{name}
- "Delete a _template?" -> DELETE /_template/{name}
- "Create a _disk_usage?" -> POST /{index}/_disk_usage
- "Get _alia details?" -> GET /_alias/{name}
- "List all explain?" -> GET /{index}/_lifecycle/explain
- "List all _field_usage_stats?" -> GET /{index}/_field_usage_stats
- "List all _flush?" -> GET /_flush
- "Create a _flush?" -> POST /_flush
- "List all _flush?" -> GET /{index}/_flush
- "Create a _flush?" -> POST /{index}/_flush
- "Create a _forcemerge?" -> POST /_forcemerge
- "Create a _forcemerge?" -> POST /{index}/_forcemerge
- "List all _alias?" -> GET /_alias
- "List all _alias?" -> GET /{index}/_alias
- "List all stats?" -> GET /_lifecycle/stats
- "List all _data_stream?" -> GET /_data_stream
- "List all _mappings?" -> GET /_data_stream/{name}/_mappings
- "List all _settings?" -> GET /_data_stream/{name}/_settings
- "Get field details?" -> GET /_mapping/field/{fields}
- "Get field details?" -> GET /{index}/_mapping/field/{fields}
- "List all _index_template?" -> GET /_index_template
- "List all _mapping?" -> GET /_mapping
- "List all _mapping?" -> GET /{index}/_mapping
- "Create a _mapping?" -> POST /{index}/_mapping
- "List all _status?" -> GET /_migration/reindex/{index}/_status
- "List all _settings?" -> GET /_settings
- "List all _settings?" -> GET /{index}/_settings
- "Get _setting details?" -> GET /{index}/_settings/{name}
- "Get _setting details?" -> GET /_settings/{name}
- "List all _template?" -> GET /_template
- "Create a reindex?" -> POST /_migration/reindex
- "Create a _modify?" -> POST /_data_stream/_modify
- "Create a _open?" -> POST /{index}/_open
- "List all _recovery?" -> GET /_recovery
- "List all _recovery?" -> GET /{index}/_recovery
- "List all _refresh?" -> GET /_refresh
- "Create a _refresh?" -> POST /_refresh
- "List all _refresh?" -> GET /{index}/_refresh
- "Create a _refresh?" -> POST /{index}/_refresh
- "List all _reload_search_analyzers?" -> GET /{index}/_reload_search_analyzers
- "Create a _reload_search_analyzer?" -> POST /{index}/_reload_search_analyzers
- "List all cluster?" -> GET /_resolve/cluster
- "Get cluster details?" -> GET /_resolve/cluster/{name}
- "Get index details?" -> GET /_resolve/index/{name}
- "Create a _rollover?" -> POST /{alias}/_rollover
- "List all _segments?" -> GET /_segments
- "List all _segments?" -> GET /{index}/_segments
- "List all _shard_stores?" -> GET /_shard_stores
- "List all _shard_stores?" -> GET /{index}/_shard_stores
- "Update a _shrink?" -> PUT /{index}/_shrink/{target}
- "Create a _simulate?" -> POST /_index_template/_simulate
- "Update a _split?" -> PUT /{index}/_split/{target}
- "List all _stats?" -> GET /_stats
- "Get _stat details?" -> GET /_stats/{metric}
- "List all _stats?" -> GET /{index}/_stats
- "Get _stat details?" -> GET /{index}/_stats/{metric}
- "Create a _aliase?" -> POST /_aliases
- "Search query?" -> GET /_validate/query
- "Create a query?" -> POST /_validate/query
- "Search query?" -> GET /{index}/_validate/query
- "Create a query?" -> POST /{index}/_validate/query
- "Create a _stream?" -> POST /_inference/chat_completion/{inference_id}/_stream
- "Get _inference details?" -> GET /_inference/{inference_id}
- "Update a _inference?" -> PUT /_inference/{inference_id}
- "Delete a _inference?" -> DELETE /_inference/{inference_id}
- "Get _inference details?" -> GET /_inference/{task_type}/{inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{inference_id}
- "Delete a _inference?" -> DELETE /_inference/{task_type}/{inference_id}
- "List all _inference?" -> GET /_inference
- "List all _all?" -> GET /_inference/{task_type}/_all
- "Update a _inference?" -> PUT /_inference/{task_type}/{ai21_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{alibabacloud_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{amazonbedrock_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{amazonsagemaker_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{anthropic_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{azureaistudio_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{azureopenai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{cohere_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{contextualai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{custom_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{deepseek_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{elasticsearch_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{elser_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{googleaistudio_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{googlevertexai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{groq_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{huggingface_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{jinaai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{llama_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{mistral_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{nvidia_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{openai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{openshiftai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{voyageai_inference_id}
- "Update a _inference?" -> PUT /_inference/{task_type}/{watsonx_inference_id}
- "Create a _stream?" -> POST /_inference/completion/{inference_id}/_stream
- "Get database details?" -> GET /_ingest/geoip/database/{id}
- "Update a database?" -> PUT /_ingest/geoip/database/{id}
- "Delete a database?" -> DELETE /_ingest/geoip/database/{id}
- "Get database details?" -> GET /_ingest/ip_location/database/{id}
- "Update a database?" -> PUT /_ingest/ip_location/database/{id}
- "Delete a database?" -> DELETE /_ingest/ip_location/database/{id}
- "Get pipeline details?" -> GET /_ingest/pipeline/{id}
- "Update a pipeline?" -> PUT /_ingest/pipeline/{id}
- "Delete a pipeline?" -> DELETE /_ingest/pipeline/{id}
- "List all stats?" -> GET /_ingest/geoip/stats
- "List all database?" -> GET /_ingest/geoip/database
- "List all database?" -> GET /_ingest/ip_location/database
- "List all pipeline?" -> GET /_ingest/pipeline
- "List all grok?" -> GET /_ingest/processor/grok
- "List all _simulate?" -> GET /_ingest/pipeline/_simulate
- "Create a _simulate?" -> POST /_ingest/pipeline/_simulate
- "List all _simulate?" -> GET /_ingest/pipeline/{id}/_simulate
- "Create a _simulate?" -> POST /_ingest/pipeline/{id}/_simulate
- "List all _license?" -> GET /_license
- "Create a _license?" -> POST /_license
- "List all basic_status?" -> GET /_license/basic_status
- "List all trial_status?" -> GET /_license/trial_status
- "Create a start_basic?" -> POST /_license/start_basic
- "Create a start_trial?" -> POST /_license/start_trial
- "Get pipeline details?" -> GET /_logstash/pipeline/{id}
- "Update a pipeline?" -> PUT /_logstash/pipeline/{id}
- "Delete a pipeline?" -> DELETE /_logstash/pipeline/{id}
- "List all pipeline?" -> GET /_logstash/pipeline
- "List all _mget?" -> GET /_mget
- "Create a _mget?" -> POST /_mget
- "List all _mget?" -> GET /{index}/_mget
- "Create a _mget?" -> POST /{index}/_mget
- "List all deprecations?" -> GET /_migration/deprecations
- "List all deprecations?" -> GET /{index}/_migration/deprecations
- "List all system_features?" -> GET /_migration/system_features
- "Create a system_feature?" -> POST /_migration/system_features
- "Create a _clear?" -> POST /_ml/trained_models/{model_id}/deployment/cache/_clear
- "Create a _close?" -> POST /_ml/anomaly_detectors/{job_id}/_close
- "Get calendar details?" -> GET /_ml/calendars/{calendar_id}
- "Update a calendar?" -> PUT /_ml/calendars/{calendar_id}
- "Delete a calendar?" -> DELETE /_ml/calendars/{calendar_id}
- "Delete a event?" -> DELETE /_ml/calendars/{calendar_id}/events/{event_id}
- "Update a job?" -> PUT /_ml/calendars/{calendar_id}/jobs/{job_id}
- "Delete a job?" -> DELETE /_ml/calendars/{calendar_id}/jobs/{job_id}
- "Get analytic details?" -> GET /_ml/data_frame/analytics/{id}
- "Update a analytic?" -> PUT /_ml/data_frame/analytics/{id}
- "Delete a analytic?" -> DELETE /_ml/data_frame/analytics/{id}
- "Get datafeed details?" -> GET /_ml/datafeeds/{datafeed_id}
- "Update a datafeed?" -> PUT /_ml/datafeeds/{datafeed_id}
- "Delete a datafeed?" -> DELETE /_ml/datafeeds/{datafeed_id}
- "Delete a _delete_expired_data?" -> DELETE /_ml/_delete_expired_data/{job_id}
- "Get filter details?" -> GET /_ml/filters/{filter_id}
- "Update a filter?" -> PUT /_ml/filters/{filter_id}
- "Delete a filter?" -> DELETE /_ml/filters/{filter_id}
- "Create a _forecast?" -> POST /_ml/anomaly_detectors/{job_id}/_forecast
- "Delete a _forecast?" -> DELETE /_ml/anomaly_detectors/{job_id}/_forecast/{forecast_id}
- "Get anomaly_detector details?" -> GET /_ml/anomaly_detectors/{job_id}
- "Update a anomaly_detector?" -> PUT /_ml/anomaly_detectors/{job_id}
- "Delete a anomaly_detector?" -> DELETE /_ml/anomaly_detectors/{job_id}
- "Get model_snapshot details?" -> GET /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}
- "Delete a model_snapshot?" -> DELETE /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}
- "Get trained_model details?" -> GET /_ml/trained_models/{model_id}
- "Update a trained_model?" -> PUT /_ml/trained_models/{model_id}
- "Delete a trained_model?" -> DELETE /_ml/trained_models/{model_id}
- "Update a model_aliase?" -> PUT /_ml/trained_models/{model_id}/model_aliases/{model_alias}
- "Delete a model_aliase?" -> DELETE /_ml/trained_models/{model_id}/model_aliases/{model_alias}
- "Create a _estimate_model_memory?" -> POST /_ml/anomaly_detectors/_estimate_model_memory
- "Create a _evaluate?" -> POST /_ml/data_frame/_evaluate
- "List all _explain?" -> GET /_ml/data_frame/analytics/_explain
- "Create a _explain?" -> POST /_ml/data_frame/analytics/_explain
- "List all _explain?" -> GET /_ml/data_frame/analytics/{id}/_explain
- "Create a _explain?" -> POST /_ml/data_frame/analytics/{id}/_explain
- "Create a _flush?" -> POST /_ml/anomaly_detectors/{job_id}/_flush
- "Get bucket details?" -> GET /_ml/anomaly_detectors/{job_id}/results/buckets/{timestamp}
- "List all buckets?" -> GET /_ml/anomaly_detectors/{job_id}/results/buckets
- "Create a bucket?" -> POST /_ml/anomaly_detectors/{job_id}/results/buckets
- "List all events?" -> GET /_ml/calendars/{calendar_id}/events
- "Create a event?" -> POST /_ml/calendars/{calendar_id}/events
- "List all calendars?" -> GET /_ml/calendars
- "Create a calendar?" -> POST /_ml/calendars
- "Get category details?" -> GET /_ml/anomaly_detectors/{job_id}/results/categories/{category_id}
- "List all categories?" -> GET /_ml/anomaly_detectors/{job_id}/results/categories
- "Create a category?" -> POST /_ml/anomaly_detectors/{job_id}/results/categories
- "List all analytics?" -> GET /_ml/data_frame/analytics
- "List all _stats?" -> GET /_ml/data_frame/analytics/_stats
- "List all _stats?" -> GET /_ml/data_frame/analytics/{id}/_stats
- "List all _stats?" -> GET /_ml/datafeeds/{datafeed_id}/_stats
- "List all _stats?" -> GET /_ml/datafeeds/_stats
- "List all datafeeds?" -> GET /_ml/datafeeds
- "List all filters?" -> GET /_ml/filters
- "List all influencers?" -> GET /_ml/anomaly_detectors/{job_id}/results/influencers
- "Create a influencer?" -> POST /_ml/anomaly_detectors/{job_id}/results/influencers
- "List all _stats?" -> GET /_ml/anomaly_detectors/_stats
- "List all _stats?" -> GET /_ml/anomaly_detectors/{job_id}/_stats
- "List all anomaly_detectors?" -> GET /_ml/anomaly_detectors
- "List all _stats?" -> GET /_ml/memory/_stats
- "List all _stats?" -> GET /_ml/memory/{node_id}/_stats
- "List all _stats?" -> GET /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_upgrade/_stats
- "List all model_snapshots?" -> GET /_ml/anomaly_detectors/{job_id}/model_snapshots
- "Create a model_snapshot?" -> POST /_ml/anomaly_detectors/{job_id}/model_snapshots
- "List all overall_buckets?" -> GET /_ml/anomaly_detectors/{job_id}/results/overall_buckets
- "Create a overall_bucket?" -> POST /_ml/anomaly_detectors/{job_id}/results/overall_buckets
- "List all records?" -> GET /_ml/anomaly_detectors/{job_id}/results/records
- "Create a record?" -> POST /_ml/anomaly_detectors/{job_id}/results/records
- "List all trained_models?" -> GET /_ml/trained_models
- "List all _stats?" -> GET /_ml/trained_models/{model_id}/_stats
- "List all _stats?" -> GET /_ml/trained_models/_stats
- "Create a _infer?" -> POST /_ml/trained_models/{model_id}/_infer
- "List all info?" -> GET /_ml/info
- "Create a _open?" -> POST /_ml/anomaly_detectors/{job_id}/_open
- "Create a _data?" -> POST /_ml/anomaly_detectors/{job_id}/_data
- "List all _preview?" -> GET /_ml/data_frame/analytics/_preview
- "Create a _preview?" -> POST /_ml/data_frame/analytics/_preview
- "List all _preview?" -> GET /_ml/data_frame/analytics/{id}/_preview
- "Create a _preview?" -> POST /_ml/data_frame/analytics/{id}/_preview
- "List all _preview?" -> GET /_ml/datafeeds/{datafeed_id}/_preview
- "Create a _preview?" -> POST /_ml/datafeeds/{datafeed_id}/_preview
- "List all _preview?" -> GET /_ml/datafeeds/_preview
- "Create a _preview?" -> POST /_ml/datafeeds/_preview
- "Update a definition?" -> PUT /_ml/trained_models/{model_id}/definition/{part}
- "Create a _reset?" -> POST /_ml/anomaly_detectors/{job_id}/_reset
- "Create a _revert?" -> POST /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_revert
- "Create a set_upgrade_mode?" -> POST /_ml/set_upgrade_mode
- "Create a _start?" -> POST /_ml/data_frame/analytics/{id}/_start
- "Create a _start?" -> POST /_ml/datafeeds/{datafeed_id}/_start
- "Create a _start?" -> POST /_ml/trained_models/{model_id}/deployment/_start
- "Create a _stop?" -> POST /_ml/data_frame/analytics/{id}/_stop
- "Create a _stop?" -> POST /_ml/datafeeds/{datafeed_id}/_stop
- "Create a _stop?" -> POST /_ml/trained_models/{model_id}/deployment/_stop
- "Create a _update?" -> POST /_ml/data_frame/analytics/{id}/_update
- "Create a _update?" -> POST /_ml/datafeeds/{datafeed_id}/_update
- "Create a _update?" -> POST /_ml/filters/{filter_id}/_update
- "Create a _update?" -> POST /_ml/anomaly_detectors/{job_id}/_update
- "Create a _update?" -> POST /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_update
- "Create a _update?" -> POST /_ml/trained_models/{model_id}/deployment/_update
- "Create a _upgrade?" -> POST /_ml/anomaly_detectors/{job_id}/model_snapshots/{snapshot_id}/_upgrade
- "List all _msearch?" -> GET /_msearch
- "Create a _msearch?" -> POST /_msearch
- "List all _msearch?" -> GET /{index}/_msearch
- "Create a _msearch?" -> POST /{index}/_msearch
- "List all template?" -> GET /_msearch/template
- "Create a template?" -> POST /_msearch/template
- "List all template?" -> GET /{index}/_msearch/template
- "Create a template?" -> POST /{index}/_msearch/template
- "List all _mtermvectors?" -> GET /_mtermvectors
- "Create a _mtermvector?" -> POST /_mtermvectors
- "List all _mtermvectors?" -> GET /{index}/_mtermvectors
- "Create a _mtermvector?" -> POST /{index}/_mtermvectors
- "Delete a _repositories_metering?" -> DELETE /_nodes/{node_id}/_repositories_metering/{max_archive_version}
- "List all _repositories_metering?" -> GET /_nodes/{node_id}/_repositories_metering
- "List all hot_threads?" -> GET /_nodes/hot_threads
- "List all hot_threads?" -> GET /_nodes/{node_id}/hot_threads
- "List all _nodes?" -> GET /_nodes
- "Get _node details?" -> GET /_nodes/{node_id}
- "Get _node details?" -> GET /_nodes/{metric}
- "Get _node details?" -> GET /_nodes/{node_id}/{metric}
- "Create a reload_secure_setting?" -> POST /_nodes/reload_secure_settings
- "Create a reload_secure_setting?" -> POST /_nodes/{node_id}/reload_secure_settings
- "List all stats?" -> GET /_nodes/stats
- "List all stats?" -> GET /_nodes/{node_id}/stats
- "Get stat details?" -> GET /_nodes/stats/{metric}
- "Get stat details?" -> GET /_nodes/{node_id}/stats/{metric}
- "Get stat details?" -> GET /_nodes/stats/{metric}/{index_metric}
- "Get stat details?" -> GET /_nodes/{node_id}/stats/{metric}/{index_metric}
- "List all usage?" -> GET /_nodes/usage
- "List all usage?" -> GET /_nodes/{node_id}/usage
- "Get usage details?" -> GET /_nodes/usage/{metric}
- "Get usage details?" -> GET /_nodes/{node_id}/usage/{metric}
- "Create a _pit?" -> POST /{index}/_pit
- "Update a _script?" -> PUT /_scripts/{id}/{context}
- "Get _rule details?" -> GET /_query_rules/{ruleset_id}/_rule/{rule_id}
- "Update a _rule?" -> PUT /_query_rules/{ruleset_id}/_rule/{rule_id}
- "Delete a _rule?" -> DELETE /_query_rules/{ruleset_id}/_rule/{rule_id}
- "Get _query_rule details?" -> GET /_query_rules/{ruleset_id}
- "Update a _query_rule?" -> PUT /_query_rules/{ruleset_id}
- "Delete a _query_rule?" -> DELETE /_query_rules/{ruleset_id}
- "List all _query_rules?" -> GET /_query_rules
- "Create a _test?" -> POST /_query_rules/{ruleset_id}/_test
- "List all _rank_eval?" -> GET /_rank_eval
- "Create a _rank_eval?" -> POST /_rank_eval
- "List all _rank_eval?" -> GET /{index}/_rank_eval
- "Create a _rank_eval?" -> POST /{index}/_rank_eval
- "Create a _reindex?" -> POST /_reindex
- "Create a _rethrottle?" -> POST /_reindex/{task_id}/_rethrottle
- "List all template?" -> GET /_render/template
- "Create a template?" -> POST /_render/template
- "Get template details?" -> GET /_render/template/{id}
- "Get job details?" -> GET /_rollup/job/{id}
- "Update a job?" -> PUT /_rollup/job/{id}
- "Delete a job?" -> DELETE /_rollup/job/{id}
- "List all job?" -> GET /_rollup/job
- "Get data details?" -> GET /_rollup/data/{id}
- "List all data?" -> GET /_rollup/data
- "List all data?" -> GET /{index}/_rollup/data
- "Search _rollup_search?" -> GET /{index}/_rollup_search
- "Create a _rollup_search?" -> POST /{index}/_rollup_search
- "Create a _start?" -> POST /_rollup/job/{id}/_start
- "Create a _stop?" -> POST /_rollup/job/{id}/_stop
- "List all _execute?" -> GET /_scripts/painless/_execute
- "Create a _execute?" -> POST /_scripts/painless/_execute
- "Search _search?" -> GET /_search
- "Create a _search?" -> POST /_search
- "Search _search?" -> GET /{index}/_search
- "Create a _search?" -> POST /{index}/_search
- "Get search_application details?" -> GET /_application/search_application/{name}
- "Update a search_application?" -> PUT /_application/search_application/{name}
- "Delete a search_application?" -> DELETE /_application/search_application/{name}
- "Get analytic details?" -> GET /_application/analytics/{name}
- "Update a analytic?" -> PUT /_application/analytics/{name}
- "Delete a analytic?" -> DELETE /_application/analytics/{name}
- "List all analytics?" -> GET /_application/analytics
- "Search search_application?" -> GET /_application/search_application
- "Create a _render_query?" -> POST /_application/search_application/{name}/_render_query
- "List all _search?" -> GET /_application/search_application/{name}/_search
- "Create a _search?" -> POST /_application/search_application/{name}/_search
- "Search _mvt?" -> GET /{index}/_mvt/{field}/{zoom}/{x}/{y}
- "List all _search_shards?" -> GET /_search_shards
- "Create a _search_shard?" -> POST /_search_shards
- "List all _search_shards?" -> GET /{index}/_search_shards
- "Create a _search_shard?" -> POST /{index}/_search_shards
- "List all template?" -> GET /_search/template
- "Create a template?" -> POST /_search/template
- "List all template?" -> GET /{index}/_search/template
- "Create a template?" -> POST /{index}/_search/template
- "List all stats?" -> GET /_searchable_snapshots/cache/stats
- "List all stats?" -> GET /_searchable_snapshots/{node_id}/cache/stats
- "Create a clear?" -> POST /_searchable_snapshots/cache/clear
- "Create a clear?" -> POST /{index}/_searchable_snapshots/cache/clear
- "Create a _mount?" -> POST /_snapshot/{repository}/{snapshot}/_mount
- "List all stats?" -> GET /_searchable_snapshots/stats
- "List all stats?" -> GET /{index}/_searchable_snapshots/stats
- "Create a _activate?" -> POST /_security/profile/_activate
- "List all _authenticate?" -> GET /_security/_authenticate
- "List all role?" -> GET /_security/role
- "Create a role?" -> POST /_security/role
- "Create a _bulk_update?" -> POST /_security/api_key/_bulk_update
- "Create a _password?" -> POST /_security/user/{username}/_password
- "Create a _password?" -> POST /_security/user/_password
- "Create a _clear_cache?" -> POST /_security/api_key/{ids}/_clear_cache
- "Create a _clear_cache?" -> POST /_security/privilege/{application}/_clear_cache
- "Create a _clear_cache?" -> POST /_security/realm/{realms}/_clear_cache
- "Create a _clear_cache?" -> POST /_security/role/{name}/_clear_cache
- "Create a _clear_cache?" -> POST /_security/service/{namespace}/{service}/credential/token/{name}/_clear_cache
- "List all api_key?" -> GET /_security/api_key
- "Create a api_key?" -> POST /_security/api_key
- "Create a api_key?" -> POST /_security/cross_cluster/api_key
- "Update a token?" -> PUT /_security/service/{namespace}/{service}/credential/token/{name}
- "Delete a token?" -> DELETE /_security/service/{namespace}/{service}/credential/token/{name}
- "Create a token?" -> POST /_security/service/{namespace}/{service}/credential/token
- "Create a delegate_pki?" -> POST /_security/delegate_pki
- "Get privilege details?" -> GET /_security/privilege/{application}/{name}
- "Delete a privilege?" -> DELETE /_security/privilege/{application}/{name}
- "Get role details?" -> GET /_security/role/{name}
- "Update a role?" -> PUT /_security/role/{name}
- "Delete a role?" -> DELETE /_security/role/{name}
- "Get role_mapping details?" -> GET /_security/role_mapping/{name}
- "Update a role_mapping?" -> PUT /_security/role_mapping/{name}
- "Delete a role_mapping?" -> DELETE /_security/role_mapping/{name}
- "Get user details?" -> GET /_security/user/{username}
- "Update a user?" -> PUT /_security/user/{username}
- "Delete a user?" -> DELETE /_security/user/{username}
- "Create a _disable?" -> POST /_security/user/{username}/_disable
- "Create a _disable?" -> POST /_security/profile/{uid}/_disable
- "Create a _enable?" -> POST /_security/user/{username}/_enable
- "Create a _enable?" -> POST /_security/profile/{uid}/_enable
- "List all kibana?" -> GET /_security/enroll/kibana
- "List all node?" -> GET /_security/enroll/node
- "List all _builtin?" -> GET /_security/privilege/_builtin
- "List all privilege?" -> GET /_security/privilege
- "Create a privilege?" -> POST /_security/privilege
- "Get privilege details?" -> GET /_security/privilege/{application}
- "List all role_mapping?" -> GET /_security/role_mapping
- "Get service details?" -> GET /_security/service/{namespace}/{service}
- "Get service details?" -> GET /_security/service/{namespace}
- "List all service?" -> GET /_security/service
- "List all credential?" -> GET /_security/service/{namespace}/{service}/credential
- "List all settings?" -> GET /_security/settings
- "List all stats?" -> GET /_security/stats
- "Create a token?" -> POST /_security/oauth2/token
- "List all user?" -> GET /_security/user
- "List all _privileges?" -> GET /_security/user/_privileges
- "Get profile details?" -> GET /_security/profile/{uid}
- "Create a grant?" -> POST /_security/api_key/grant
- "List all _has_privileges?" -> GET /_security/user/_has_privileges
- "Create a _has_privilege?" -> POST /_security/user/_has_privileges
- "List all _has_privileges?" -> GET /_security/user/{user}/_has_privileges
- "Create a _has_privilege?" -> POST /_security/user/{user}/_has_privileges
- "List all _has_privileges?" -> GET /_security/profile/_has_privileges
- "Create a _has_privilege?" -> POST /_security/profile/_has_privileges
- "Create a authenticate?" -> POST /_security/oidc/authenticate
- "Create a logout?" -> POST /_security/oidc/logout
- "Create a prepare?" -> POST /_security/oidc/prepare
- "Search api_key?" -> GET /_security/_query/api_key
- "Create a api_key?" -> POST /_security/_query/api_key
- "Search role?" -> GET /_security/_query/role
- "Create a role?" -> POST /_security/_query/role
- "Search user?" -> GET /_security/_query/user
- "Create a user?" -> POST /_security/_query/user
- "Create a authenticate?" -> POST /_security/saml/authenticate
- "Create a complete_logout?" -> POST /_security/saml/complete_logout
- "Create a invalidate?" -> POST /_security/saml/invalidate
- "Create a logout?" -> POST /_security/saml/logout
- "Create a prepare?" -> POST /_security/saml/prepare
- "Get metadata details?" -> GET /_security/saml/metadata/{realm_name}
- "List all _suggest?" -> GET /_security/profile/_suggest
- "Create a _suggest?" -> POST /_security/profile/_suggest
- "Update a api_key?" -> PUT /_security/api_key/{id}
- "Update a api_key?" -> PUT /_security/cross_cluster/api_key/{id}
- "Create a _data?" -> POST /_security/profile/{uid}/_data
- "List all _simulate?" -> GET /_ingest/_simulate
- "Create a _simulate?" -> POST /_ingest/_simulate
- "List all _simulate?" -> GET /_ingest/{index}/_simulate
- "Create a _simulate?" -> POST /_ingest/{index}/_simulate
- "Get policy details?" -> GET /_slm/policy/{policy_id}
- "Update a policy?" -> PUT /_slm/policy/{policy_id}
- "Delete a policy?" -> DELETE /_slm/policy/{policy_id}
- "Create a _execute_retention?" -> POST /_slm/_execute_retention
- "List all policy?" -> GET /_slm/policy
- "List all stats?" -> GET /_slm/stats
- "List all status?" -> GET /_slm/status
- "Create a start?" -> POST /_slm/start
- "Create a stop?" -> POST /_slm/stop
- "Create a _cleanup?" -> POST /_snapshot/{repository}/_cleanup
- "Update a _clone?" -> PUT /_snapshot/{repository}/{snapshot}/_clone/{target_snapshot}
- "Get _snapshot details?" -> GET /_snapshot/{repository}/{snapshot}
- "Update a _snapshot?" -> PUT /_snapshot/{repository}/{snapshot}
- "Delete a _snapshot?" -> DELETE /_snapshot/{repository}/{snapshot}
- "Get _snapshot details?" -> GET /_snapshot/{repository}
- "Update a _snapshot?" -> PUT /_snapshot/{repository}
- "Delete a _snapshot?" -> DELETE /_snapshot/{repository}
- "List all _snapshot?" -> GET /_snapshot
- "Create a _analyze?" -> POST /_snapshot/{repository}/_analyze
- "Create a _verify_integrity?" -> POST /_snapshot/{repository}/_verify_integrity
- "Create a _restore?" -> POST /_snapshot/{repository}/{snapshot}/_restore
- "List all _status?" -> GET /_snapshot/_status
- "List all _status?" -> GET /_snapshot/{repository}/_status
- "List all _status?" -> GET /_snapshot/{repository}/{snapshot}/_status
- "Create a _verify?" -> POST /_snapshot/{repository}/_verify
- "Create a close?" -> POST /_sql/close
- "Delete a delete?" -> DELETE /_sql/async/delete/{id}
- "Get async details?" -> GET /_sql/async/{id}
- "Get status details?" -> GET /_sql/async/status/{id}
- "Search _sql?" -> GET /_sql
- "Create a _sql?" -> POST /_sql
- "Search translate?" -> GET /_sql/translate
- "Create a translate?" -> POST /_sql/translate
- "List all certificates?" -> GET /_ssl/certificates
- "Create a _disable?" -> POST /_streams/{name}/_disable
- "Create a _enable?" -> POST /_streams/{name}/_enable
- "List all status?" -> GET /_streams/status
- "Get _synonym details?" -> GET /_synonyms/{id}
- "Update a _synonym?" -> PUT /_synonyms/{id}
- "Delete a _synonym?" -> DELETE /_synonyms/{id}
- "Get _synonym details?" -> GET /_synonyms/{set_id}/{rule_id}
- "Update a _synonym?" -> PUT /_synonyms/{set_id}/{rule_id}
- "Delete a _synonym?" -> DELETE /_synonyms/{set_id}/{rule_id}
- "List all _synonyms?" -> GET /_synonyms
- "Create a _cancel?" -> POST /_tasks/_cancel
- "Create a _cancel?" -> POST /_tasks/{task_id}/_cancel
- "Get _task details?" -> GET /_tasks/{task_id}
- "List all _tasks?" -> GET /_tasks
- "List all _terms_enum?" -> GET /{index}/_terms_enum
- "Create a _terms_enum?" -> POST /{index}/_terms_enum
- "Get _termvector details?" -> GET /{index}/_termvectors/{id}
- "List all _termvectors?" -> GET /{index}/_termvectors
- "Create a _termvector?" -> POST /{index}/_termvectors
- "List all find_field_structure?" -> GET /_text_structure/find_field_structure
- "List all find_message_structure?" -> GET /_text_structure/find_message_structure
- "Create a find_message_structure?" -> POST /_text_structure/find_message_structure
- "Create a find_structure?" -> POST /_text_structure/find_structure
- "List all test_grok_pattern?" -> GET /_text_structure/test_grok_pattern
- "Create a test_grok_pattern?" -> POST /_text_structure/test_grok_pattern
- "Get _transform details?" -> GET /_transform/{transform_id}
- "Update a _transform?" -> PUT /_transform/{transform_id}
- "Delete a _transform?" -> DELETE /_transform/{transform_id}
- "List all _node_stats?" -> GET /_transform/_node_stats
- "List all _transform?" -> GET /_transform
- "List all _stats?" -> GET /_transform/{transform_id}/_stats
- "List all _preview?" -> GET /_transform/{transform_id}/_preview
- "Create a _preview?" -> POST /_transform/{transform_id}/_preview
- "List all _preview?" -> GET /_transform/_preview
- "Create a _preview?" -> POST /_transform/_preview
- "Create a _reset?" -> POST /_transform/{transform_id}/_reset
- "Create a _schedule_now?" -> POST /_transform/{transform_id}/_schedule_now
- "Create a set_upgrade_mode?" -> POST /_transform/set_upgrade_mode
- "Create a _start?" -> POST /_transform/{transform_id}/_start
- "Create a _stop?" -> POST /_transform/{transform_id}/_stop
- "Create a _update?" -> POST /_transform/{transform_id}/_update
- "Create a _upgrade?" -> POST /_transform/_upgrade
- "Create a _update_by_query?" -> POST /{index}/_update_by_query
- "Create a _rethrottle?" -> POST /_update_by_query/{task_id}/_rethrottle
- "Create a _ack?" -> POST /_watcher/watch/{watch_id}/_ack
- "Update a _ack?" -> PUT /_watcher/watch/{watch_id}/_ack/{action_id}
- "Create a _activate?" -> POST /_watcher/watch/{watch_id}/_activate
- "Create a _deactivate?" -> POST /_watcher/watch/{watch_id}/_deactivate
- "Get watch details?" -> GET /_watcher/watch/{id}
- "Update a watch?" -> PUT /_watcher/watch/{id}
- "Delete a watch?" -> DELETE /_watcher/watch/{id}
- "Create a _execute?" -> POST /_watcher/watch/{id}/_execute
- "Create a _execute?" -> POST /_watcher/watch/_execute
- "List all settings?" -> GET /_watcher/settings
- "Search watches?" -> GET /_watcher/_query/watches
- "Create a watche?" -> POST /_watcher/_query/watches
- "Create a _start?" -> POST /_watcher/_start
- "List all stats?" -> GET /_watcher/stats
- "Get stat details?" -> GET /_watcher/stats/{metric}
- "Create a _stop?" -> POST /_watcher/_stop
- "List all _xpack?" -> GET /_xpack
- "List all usage?" -> GET /_xpack/usage
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
