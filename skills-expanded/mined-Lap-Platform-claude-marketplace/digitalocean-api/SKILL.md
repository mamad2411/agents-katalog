---
name: digitalocean-api
description: "DigitalOcean API skill. Use when working with DigitalOcean for 1-clicks, account, actions. Covers 558 endpoints."
version: 1.0.0
generator: lapsh
---

# DigitalOcean API
API version: 2.0

## Auth
Bearer bearer

## Base URL
https://api.digitalocean.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/1-clicks -- verify access
3. POST /v2/1-clicks/kubernetes -- create first kubernetes

## Endpoints

558 endpoints across 39 groups. See references/api-spec.lap for full details.

### 1-clicks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/1-clicks |  |
| POST | /v2/1-clicks/kubernetes |  |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/account |  |
| GET | /v2/account/keys |  |
| POST | /v2/account/keys |  |
| GET | /v2/account/keys/{ssh_key_identifier} |  |
| PUT | /v2/account/keys/{ssh_key_identifier} |  |
| DELETE | /v2/account/keys/{ssh_key_identifier} |  |

### actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/actions |  |
| GET | /v2/actions/{action_id} |  |

### add-ons
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/add-ons/apps |  |
| GET | /v2/add-ons/apps/{app_slug}/metadata |  |
| GET | /v2/add-ons/saas |  |
| POST | /v2/add-ons/saas |  |
| GET | /v2/add-ons/saas/{resource_uuid} |  |
| DELETE | /v2/add-ons/saas/{resource_uuid} |  |
| PATCH | /v2/add-ons/saas/{resource_uuid} |  |
| PATCH | /v2/add-ons/saas/{resource_uuid}/plan |  |

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/apps |  |
| POST | /v2/apps |  |
| DELETE | /v2/apps/{id} |  |
| GET | /v2/apps/{id} |  |
| PUT | /v2/apps/{id} |  |
| POST | /v2/apps/{app_id}/restart |  |
| GET | /v2/apps/{app_id}/components/{component_name}/logs |  |
| GET | /v2/apps/{app_id}/components/{component_name}/exec |  |
| GET | /v2/apps/{app_id}/instances |  |
| GET | /v2/apps/{app_id}/deployments |  |
| POST | /v2/apps/{app_id}/deployments |  |
| GET | /v2/apps/{app_id}/deployments/{deployment_id} |  |
| POST | /v2/apps/{app_id}/deployments/{deployment_id}/cancel |  |
| GET | /v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/logs |  |
| GET | /v2/apps/{app_id}/deployments/{deployment_id}/logs |  |
| GET | /v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/exec |  |
| GET | /v2/apps/{app_id}/logs |  |
| GET | /v2/apps/{app_id}/job-invocations |  |
| GET | /v2/apps/{app_id}/job-invocations/{job_invocation_id} |  |
| POST | /v2/apps/{app_id}/job-invocations/{job_invocation_id}/cancel |  |
| GET | /v2/apps/{app_id}/jobs/{job_name}/invocations/{job_invocation_id}/logs |  |
| GET | /v2/apps/tiers/instance_sizes |  |
| GET | /v2/apps/tiers/instance_sizes/{slug} |  |
| GET | /v2/apps/regions |  |
| POST | /v2/apps/propose |  |
| GET | /v2/apps/{app_id}/alerts |  |
| POST | /v2/apps/{app_id}/alerts/{alert_id}/destinations |  |
| POST | /v2/apps/{app_id}/rollback |  |
| POST | /v2/apps/{app_id}/rollback/validate |  |
| POST | /v2/apps/{app_id}/rollback/commit |  |
| POST | /v2/apps/{app_id}/rollback/revert |  |
| GET | /v2/apps/{app_id}/metrics/bandwidth_daily |  |
| POST | /v2/apps/metrics/bandwidth_daily |  |
| GET | /v2/apps/{app_id}/health |  |

### cdn
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/cdn/endpoints |  |
| POST | /v2/cdn/endpoints |  |
| GET | /v2/cdn/endpoints/{cdn_id} |  |
| PUT | /v2/cdn/endpoints/{cdn_id} |  |
| DELETE | /v2/cdn/endpoints/{cdn_id} |  |
| DELETE | /v2/cdn/endpoints/{cdn_id}/cache |  |

### certificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/certificates |  |
| POST | /v2/certificates |  |
| GET | /v2/certificates/{certificate_id} |  |
| DELETE | /v2/certificates/{certificate_id} |  |

### customers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/customers/my/balance |  |
| GET | /v2/customers/my/billing_history |  |
| GET | /v2/customers/my/invoices |  |
| GET | /v2/customers/my/invoices/{invoice_uuid} |  |
| GET | /v2/customers/my/invoices/{invoice_uuid}/csv |  |
| GET | /v2/customers/my/invoices/{invoice_uuid}/pdf |  |
| GET | /v2/customers/my/invoices/{invoice_uuid}/summary |  |

### billing
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/billing/{account_urn}/insights/{start_date}/{end_date} |  |

### databases
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/databases/options |  |
| GET | /v2/databases |  |
| POST | /v2/databases |  |
| GET | /v2/databases/{database_cluster_uuid} |  |
| DELETE | /v2/databases/{database_cluster_uuid} |  |
| GET | /v2/databases/{database_cluster_uuid}/config |  |
| PATCH | /v2/databases/{database_cluster_uuid}/config |  |
| GET | /v2/databases/{database_cluster_uuid}/ca |  |
| GET | /v2/databases/{database_cluster_uuid}/online-migration |  |
| PUT | /v2/databases/{database_cluster_uuid}/online-migration |  |
| DELETE | /v2/databases/{database_cluster_uuid}/online-migration/{migration_id} |  |
| PUT | /v2/databases/{database_cluster_uuid}/migrate |  |
| PUT | /v2/databases/{database_cluster_uuid}/resize |  |
| GET | /v2/databases/{database_cluster_uuid}/firewall |  |
| PUT | /v2/databases/{database_cluster_uuid}/firewall |  |
| PUT | /v2/databases/{database_cluster_uuid}/maintenance |  |
| PUT | /v2/databases/{database_cluster_uuid}/install_update |  |
| GET | /v2/databases/{database_cluster_uuid}/backups |  |
| GET | /v2/databases/{database_cluster_uuid}/replicas |  |
| POST | /v2/databases/{database_cluster_uuid}/replicas |  |
| GET | /v2/databases/{database_cluster_uuid}/events |  |
| GET | /v2/databases/{database_cluster_uuid}/replicas/{replica_name} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/replicas/{replica_name} |  |
| PUT | /v2/databases/{database_cluster_uuid}/replicas/{replica_name}/promote |  |
| GET | /v2/databases/{database_cluster_uuid}/users |  |
| POST | /v2/databases/{database_cluster_uuid}/users |  |
| GET | /v2/databases/{database_cluster_uuid}/users/{username} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/users/{username} |  |
| PUT | /v2/databases/{database_cluster_uuid}/users/{username} |  |
| POST | /v2/databases/{database_cluster_uuid}/users/{username}/reset_auth |  |
| GET | /v2/databases/{database_cluster_uuid}/dbs |  |
| POST | /v2/databases/{database_cluster_uuid}/dbs |  |
| GET | /v2/databases/{database_cluster_uuid}/dbs/{database_name} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/dbs/{database_name} |  |
| GET | /v2/databases/{database_cluster_uuid}/pools |  |
| POST | /v2/databases/{database_cluster_uuid}/pools |  |
| GET | /v2/databases/{database_cluster_uuid}/pools/{pool_name} |  |
| PUT | /v2/databases/{database_cluster_uuid}/pools/{pool_name} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/pools/{pool_name} |  |
| GET | /v2/databases/{database_cluster_uuid}/eviction_policy |  |
| PUT | /v2/databases/{database_cluster_uuid}/eviction_policy |  |
| GET | /v2/databases/{database_cluster_uuid}/sql_mode |  |
| PUT | /v2/databases/{database_cluster_uuid}/sql_mode |  |
| PUT | /v2/databases/{database_cluster_uuid}/upgrade |  |
| GET | /v2/databases/{database_cluster_uuid}/autoscale |  |
| PUT | /v2/databases/{database_cluster_uuid}/autoscale |  |
| GET | /v2/databases/{database_cluster_uuid}/topics |  |
| POST | /v2/databases/{database_cluster_uuid}/topics |  |
| GET | /v2/databases/{database_cluster_uuid}/topics/{topic_name} |  |
| PUT | /v2/databases/{database_cluster_uuid}/topics/{topic_name} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/topics/{topic_name} |  |
| GET | /v2/databases/{database_cluster_uuid}/logsink |  |
| POST | /v2/databases/{database_cluster_uuid}/logsink |  |
| GET | /v2/databases/{database_cluster_uuid}/logsink/{logsink_id} |  |
| PUT | /v2/databases/{database_cluster_uuid}/logsink/{logsink_id} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/logsink/{logsink_id} |  |
| GET | /v2/databases/{database_cluster_uuid}/schema-registry |  |
| POST | /v2/databases/{database_cluster_uuid}/schema-registry |  |
| GET | /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name} |  |
| DELETE | /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name} |  |
| GET | /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name}/versions/{version} |  |
| GET | /v2/databases/{database_cluster_uuid}/schema-registry/config |  |
| PUT | /v2/databases/{database_cluster_uuid}/schema-registry/config |  |
| GET | /v2/databases/{database_cluster_uuid}/schema-registry/config/{subject_name} |  |
| PUT | /v2/databases/{database_cluster_uuid}/schema-registry/config/{subject_name} |  |
| GET | /v2/databases/metrics/credentials |  |
| PUT | /v2/databases/metrics/credentials |  |
| GET | /v2/databases/{database_cluster_uuid}/indexes |  |
| DELETE | /v2/databases/{database_cluster_uuid}/indexes/{index_name} |  |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/domains |  |
| POST | /v2/domains |  |
| GET | /v2/domains/{domain_name} |  |
| DELETE | /v2/domains/{domain_name} |  |
| GET | /v2/domains/{domain_name}/records |  |
| POST | /v2/domains/{domain_name}/records |  |
| GET | /v2/domains/{domain_name}/records/{domain_record_id} |  |
| PATCH | /v2/domains/{domain_name}/records/{domain_record_id} |  |
| PUT | /v2/domains/{domain_name}/records/{domain_record_id} |  |
| DELETE | /v2/domains/{domain_name}/records/{domain_record_id} |  |

### droplets
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/droplets |  |
| POST | /v2/droplets |  |
| DELETE | /v2/droplets |  |
| GET | /v2/droplets/{droplet_id} |  |
| DELETE | /v2/droplets/{droplet_id} |  |
| GET | /v2/droplets/{droplet_id}/backups |  |
| GET | /v2/droplets/{droplet_id}/backups/policy |  |
| GET | /v2/droplets/backups/policies |  |
| GET | /v2/droplets/backups/supported_policies |  |
| GET | /v2/droplets/{droplet_id}/snapshots |  |
| GET | /v2/droplets/{droplet_id}/actions |  |
| POST | /v2/droplets/{droplet_id}/actions |  |
| POST | /v2/droplets/actions |  |
| GET | /v2/droplets/{droplet_id}/actions/{action_id} |  |
| GET | /v2/droplets/{droplet_id}/kernels |  |
| GET | /v2/droplets/{droplet_id}/firewalls |  |
| GET | /v2/droplets/{droplet_id}/neighbors |  |
| GET | /v2/droplets/{droplet_id}/destroy_with_associated_resources |  |
| DELETE | /v2/droplets/{droplet_id}/destroy_with_associated_resources/selective |  |
| DELETE | /v2/droplets/{droplet_id}/destroy_with_associated_resources/dangerous |  |
| GET | /v2/droplets/{droplet_id}/destroy_with_associated_resources/status |  |
| POST | /v2/droplets/{droplet_id}/destroy_with_associated_resources/retry |  |
| GET | /v2/droplets/autoscale |  |
| POST | /v2/droplets/autoscale |  |
| GET | /v2/droplets/autoscale/{autoscale_pool_id} |  |
| PUT | /v2/droplets/autoscale/{autoscale_pool_id} |  |
| DELETE | /v2/droplets/autoscale/{autoscale_pool_id} |  |
| DELETE | /v2/droplets/autoscale/{autoscale_pool_id}/dangerous |  |
| GET | /v2/droplets/autoscale/{autoscale_pool_id}/members |  |
| GET | /v2/droplets/autoscale/{autoscale_pool_id}/history |  |

### firewalls
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/firewalls |  |
| POST | /v2/firewalls |  |
| GET | /v2/firewalls/{firewall_id} |  |
| PUT | /v2/firewalls/{firewall_id} |  |
| DELETE | /v2/firewalls/{firewall_id} |  |
| POST | /v2/firewalls/{firewall_id}/droplets |  |
| DELETE | /v2/firewalls/{firewall_id}/droplets |  |
| POST | /v2/firewalls/{firewall_id}/tags |  |
| DELETE | /v2/firewalls/{firewall_id}/tags |  |
| POST | /v2/firewalls/{firewall_id}/rules |  |
| DELETE | /v2/firewalls/{firewall_id}/rules |  |

### floating_ips
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/floating_ips |  |
| POST | /v2/floating_ips |  |
| GET | /v2/floating_ips/{floating_ip} |  |
| DELETE | /v2/floating_ips/{floating_ip} |  |
| GET | /v2/floating_ips/{floating_ip}/actions |  |
| POST | /v2/floating_ips/{floating_ip}/actions |  |
| GET | /v2/floating_ips/{floating_ip}/actions/{action_id} |  |

### functions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/functions/namespaces |  |
| POST | /v2/functions/namespaces |  |
| GET | /v2/functions/namespaces/{namespace_id} |  |
| DELETE | /v2/functions/namespaces/{namespace_id} |  |
| GET | /v2/functions/namespaces/{namespace_id}/triggers |  |
| POST | /v2/functions/namespaces/{namespace_id}/triggers |  |
| GET | /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name} |  |
| PUT | /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name} |  |
| DELETE | /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name} |  |

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/images |  |
| POST | /v2/images |  |
| GET | /v2/images/{image_id} |  |
| PUT | /v2/images/{image_id} |  |
| DELETE | /v2/images/{image_id} |  |
| GET | /v2/images/{image_id}/actions |  |
| POST | /v2/images/{image_id}/actions |  |
| GET | /v2/images/{image_id}/actions/{action_id} |  |

### kubernetes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/kubernetes/clusters |  |
| POST | /v2/kubernetes/clusters |  |
| GET | /v2/kubernetes/clusters/{cluster_id} |  |
| PUT | /v2/kubernetes/clusters/{cluster_id} |  |
| DELETE | /v2/kubernetes/clusters/{cluster_id} |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources |  |
| DELETE | /v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/selective |  |
| DELETE | /v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/dangerous |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/kubeconfig |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/credentials |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/upgrades |  |
| POST | /v2/kubernetes/clusters/{cluster_id}/upgrade |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/node_pools |  |
| POST | /v2/kubernetes/clusters/{cluster_id}/node_pools |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id} |  |
| PUT | /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id} |  |
| DELETE | /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id} |  |
| DELETE | /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/nodes/{node_id} |  |
| POST | /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/recycle |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/user |  |
| GET | /v2/kubernetes/options |  |
| POST | /v2/kubernetes/clusters/{cluster_id}/clusterlint |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/clusterlint |  |
| POST | /v2/kubernetes/registry |  |
| DELETE | /v2/kubernetes/registry |  |
| POST | /v2/kubernetes/registries |  |
| DELETE | /v2/kubernetes/registries |  |
| GET | /v2/kubernetes/clusters/{cluster_id}/status_messages |  |

### load_balancers
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/load_balancers |  |
| GET | /v2/load_balancers |  |
| GET | /v2/load_balancers/{lb_id} |  |
| PUT | /v2/load_balancers/{lb_id} |  |
| DELETE | /v2/load_balancers/{lb_id} |  |
| DELETE | /v2/load_balancers/{lb_id}/cache |  |
| POST | /v2/load_balancers/{lb_id}/droplets |  |
| DELETE | /v2/load_balancers/{lb_id}/droplets |  |
| POST | /v2/load_balancers/{lb_id}/forwarding_rules |  |
| DELETE | /v2/load_balancers/{lb_id}/forwarding_rules |  |

### monitoring
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/monitoring/alerts |  |
| POST | /v2/monitoring/alerts |  |
| GET | /v2/monitoring/alerts/{alert_uuid} |  |
| PUT | /v2/monitoring/alerts/{alert_uuid} |  |
| DELETE | /v2/monitoring/alerts/{alert_uuid} |  |
| GET | /v2/monitoring/metrics/droplet/bandwidth |  |
| GET | /v2/monitoring/metrics/droplet/cpu |  |
| GET | /v2/monitoring/metrics/droplet/filesystem_free |  |
| GET | /v2/monitoring/metrics/droplet/filesystem_size |  |
| GET | /v2/monitoring/metrics/droplet/load_1 |  |
| GET | /v2/monitoring/metrics/droplet/load_5 |  |
| GET | /v2/monitoring/metrics/droplet/load_15 |  |
| GET | /v2/monitoring/metrics/droplet/memory_cached |  |
| GET | /v2/monitoring/metrics/droplet/memory_free |  |
| GET | /v2/monitoring/metrics/droplet/memory_total |  |
| GET | /v2/monitoring/metrics/droplet/memory_available |  |
| GET | /v2/monitoring/metrics/apps/memory_percentage |  |
| GET | /v2/monitoring/metrics/apps/cpu_percentage |  |
| GET | /v2/monitoring/metrics/apps/restart_count |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_connections_current |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_connections_limit |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_cpu_utilization |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_firewall_dropped_bytes |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_firewall_dropped_packets |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_http_responses |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_http_requests_per_second |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_network_throughput_http |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_network_throughput_udp |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_network_throughput_tcp |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_nlb_tcp_network_throughput |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_nlb_udp_network_throughput |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_tls_connections_current |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_tls_connections_limit |  |
| GET | /v2/monitoring/metrics/load_balancer/frontend_tls_connections_exceeding_rate_limit |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_avg |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_50p |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_95p |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_response_time_avg |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_response_time_50p |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_response_time_95p |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_response_time_99p |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_queue_size |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_http_responses |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_connections |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_health_checks |  |
| GET | /v2/monitoring/metrics/load_balancer/droplets_downtime |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/current_instances |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/target_instances |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/current_cpu_utilization |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/target_cpu_utilization |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/current_memory_utilization |  |
| GET | /v2/monitoring/metrics/droplet_autoscale/target_memory_utilization |  |
| GET | /v2/monitoring/metrics/database/mysql/cpu_usage |  |
| GET | /v2/monitoring/metrics/database/mysql/load |  |
| GET | /v2/monitoring/metrics/database/mysql/memory_usage |  |
| GET | /v2/monitoring/metrics/database/mysql/disk_usage |  |
| GET | /v2/monitoring/metrics/database/mysql/threads_connected |  |
| GET | /v2/monitoring/metrics/database/mysql/threads_created_rate |  |
| GET | /v2/monitoring/metrics/database/mysql/threads_active |  |
| GET | /v2/monitoring/metrics/database/mysql/index_vs_sequential_reads |  |
| GET | /v2/monitoring/metrics/database/mysql/op_rates |  |
| GET | /v2/monitoring/metrics/database/mysql/schema_throughput |  |
| GET | /v2/monitoring/metrics/database/mysql/schema_latency |  |
| POST | /v2/monitoring/sinks/destinations |  |
| GET | /v2/monitoring/sinks/destinations |  |
| GET | /v2/monitoring/sinks/destinations/{destination_uuid} |  |
| POST | /v2/monitoring/sinks/destinations/{destination_uuid} |  |
| DELETE | /v2/monitoring/sinks/destinations/{destination_uuid} |  |
| POST | /v2/monitoring/sinks |  |
| GET | /v2/monitoring/sinks |  |
| GET | /v2/monitoring/sinks/{sink_uuid} |  |
| DELETE | /v2/monitoring/sinks/{sink_uuid} |  |

### nfs
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/nfs |  |
| GET | /v2/nfs |  |
| GET | /v2/nfs/{nfs_id} |  |
| DELETE | /v2/nfs/{nfs_id} |  |
| POST | /v2/nfs/{nfs_id}/actions |  |
| GET | /v2/nfs/snapshots |  |
| GET | /v2/nfs/snapshots/{nfs_snapshot_id} |  |
| DELETE | /v2/nfs/snapshots/{nfs_snapshot_id} |  |

### partner_network_connect
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/partner_network_connect/attachments |  |
| POST | /v2/partner_network_connect/attachments |  |
| GET | /v2/partner_network_connect/attachments/{pa_id} |  |
| PATCH | /v2/partner_network_connect/attachments/{pa_id} |  |
| DELETE | /v2/partner_network_connect/attachments/{pa_id} |  |
| GET | /v2/partner_network_connect/attachments/{pa_id}/bgp_auth_key |  |
| GET | /v2/partner_network_connect/attachments/{pa_id}/remote_routes |  |
| GET | /v2/partner_network_connect/attachments/{pa_id}/service_key |  |
| POST | /v2/partner_network_connect/attachments/{pa_id}/service_key |  |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/projects |  |
| POST | /v2/projects |  |
| GET | /v2/projects/default |  |
| PUT | /v2/projects/default |  |
| PATCH | /v2/projects/default |  |
| GET | /v2/projects/{project_id} |  |
| PUT | /v2/projects/{project_id} |  |
| PATCH | /v2/projects/{project_id} |  |
| DELETE | /v2/projects/{project_id} |  |
| GET | /v2/projects/{project_id}/resources |  |
| POST | /v2/projects/{project_id}/resources |  |
| GET | /v2/projects/default/resources |  |
| POST | /v2/projects/default/resources |  |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/regions |  |

### registries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/registries |  |
| POST | /v2/registries |  |
| GET | /v2/registries/{registry_name} |  |
| DELETE | /v2/registries/{registry_name} |  |
| GET | /v2/registries/{registry_name}/docker-credentials |  |
| GET | /v2/registries/subscription |  |
| POST | /v2/registries/subscription |  |
| GET | /v2/registries/options |  |
| GET | /v2/registries/{registry_name}/garbage-collection |  |
| POST | /v2/registries/{registry_name}/garbage-collection |  |
| GET | /v2/registries/{registry_name}/garbage-collections |  |
| PUT | /v2/registries/{registry_name}/garbage-collection/{garbage_collection_uuid} |  |
| GET | /v2/registries/{registry_name}/repositoriesV2 |  |
| DELETE | /v2/registries/{registry_name}/repositories/{repository_name} |  |
| GET | /v2/registries/{registry_name}/repositories/{repository_name}/tags |  |
| DELETE | /v2/registries/{registry_name}/repositories/{repository_name}/tags/{repository_tag} |  |
| GET | /v2/registries/{registry_name}/repositories/{repository_name}/digests |  |
| DELETE | /v2/registries/{registry_name}/repositories/{repository_name}/digests/{manifest_digest} |  |
| POST | /v2/registries/validate-name |  |

### registry
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/registry |  |
| POST | /v2/registry |  |
| DELETE | /v2/registry |  |
| GET | /v2/registry/subscription |  |
| POST | /v2/registry/subscription |  |
| GET | /v2/registry/docker-credentials |  |
| POST | /v2/registry/validate-name |  |
| GET | /v2/registry/{registry_name}/repositories |  |
| GET | /v2/registry/{registry_name}/repositoriesV2 |  |
| GET | /v2/registry/{registry_name}/repositories/{repository_name}/tags |  |
| DELETE | /v2/registry/{registry_name}/repositories/{repository_name}/tags/{repository_tag} |  |
| GET | /v2/registry/{registry_name}/repositories/{repository_name}/digests |  |
| DELETE | /v2/registry/{registry_name}/repositories/{repository_name}/digests/{manifest_digest} |  |
| POST | /v2/registry/{registry_name}/garbage-collection |  |
| GET | /v2/registry/{registry_name}/garbage-collection |  |
| GET | /v2/registry/{registry_name}/garbage-collections |  |
| PUT | /v2/registry/{registry_name}/garbage-collection/{garbage_collection_uuid} |  |
| GET | /v2/registry/options |  |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/reports/droplet_neighbors_ids |  |

### reserved_ips
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/reserved_ips |  |
| POST | /v2/reserved_ips |  |
| GET | /v2/reserved_ips/{reserved_ip} |  |
| DELETE | /v2/reserved_ips/{reserved_ip} |  |
| GET | /v2/reserved_ips/{reserved_ip}/actions |  |
| POST | /v2/reserved_ips/{reserved_ip}/actions |  |
| GET | /v2/reserved_ips/{reserved_ip}/actions/{action_id} |  |

### reserved_ipv6
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/reserved_ipv6 |  |
| POST | /v2/reserved_ipv6 |  |
| GET | /v2/reserved_ipv6/{reserved_ipv6} |  |
| DELETE | /v2/reserved_ipv6/{reserved_ipv6} |  |
| POST | /v2/reserved_ipv6/{reserved_ipv6}/actions |  |

### byoip_prefixes
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/byoip_prefixes |  |
| GET | /v2/byoip_prefixes |  |
| GET | /v2/byoip_prefixes/{byoip_prefix_uuid} |  |
| DELETE | /v2/byoip_prefixes/{byoip_prefix_uuid} |  |
| PATCH | /v2/byoip_prefixes/{byoip_prefix_uuid} |  |
| GET | /v2/byoip_prefixes/{byoip_prefix_uuid}/ips |  |

### sizes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/sizes |  |

### snapshots
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/snapshots |  |
| GET | /v2/snapshots/{snapshot_id} |  |
| DELETE | /v2/snapshots/{snapshot_id} |  |

### spaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/spaces/keys |  |
| POST | /v2/spaces/keys |  |
| GET | /v2/spaces/keys/{access_key} |  |
| DELETE | /v2/spaces/keys/{access_key} |  |
| PUT | /v2/spaces/keys/{access_key} |  |
| PATCH | /v2/spaces/keys/{access_key} |  |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/tags |  |
| POST | /v2/tags |  |
| GET | /v2/tags/{tag_id} |  |
| DELETE | /v2/tags/{tag_id} |  |
| POST | /v2/tags/{tag_id}/resources |  |
| DELETE | /v2/tags/{tag_id}/resources |  |

### volumes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/volumes |  |
| POST | /v2/volumes |  |
| DELETE | /v2/volumes |  |
| POST | /v2/volumes/actions |  |
| GET | /v2/volumes/snapshots/{snapshot_id} |  |
| DELETE | /v2/volumes/snapshots/{snapshot_id} |  |
| GET | /v2/volumes/{volume_id} |  |
| DELETE | /v2/volumes/{volume_id} |  |
| GET | /v2/volumes/{volume_id}/actions |  |
| POST | /v2/volumes/{volume_id}/actions |  |
| GET | /v2/volumes/{volume_id}/actions/{action_id} |  |
| GET | /v2/volumes/{volume_id}/snapshots |  |
| POST | /v2/volumes/{volume_id}/snapshots |  |

### vpcs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/vpcs |  |
| POST | /v2/vpcs |  |
| GET | /v2/vpcs/{vpc_id} |  |
| PUT | /v2/vpcs/{vpc_id} |  |
| PATCH | /v2/vpcs/{vpc_id} |  |
| DELETE | /v2/vpcs/{vpc_id} |  |
| GET | /v2/vpcs/{vpc_id}/members |  |
| GET | /v2/vpcs/{vpc_id}/peerings |  |
| POST | /v2/vpcs/{vpc_id}/peerings |  |
| PATCH | /v2/vpcs/{vpc_id}/peerings/{vpc_peering_id} |  |

### vpc_peerings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/vpc_peerings |  |
| POST | /v2/vpc_peerings |  |
| GET | /v2/vpc_peerings/{vpc_peering_id} |  |
| PATCH | /v2/vpc_peerings/{vpc_peering_id} |  |
| DELETE | /v2/vpc_peerings/{vpc_peering_id} |  |

### vpc_nat_gateways
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/vpc_nat_gateways |  |
| POST | /v2/vpc_nat_gateways |  |
| GET | /v2/vpc_nat_gateways/{id} |  |
| PUT | /v2/vpc_nat_gateways/{id} |  |
| DELETE | /v2/vpc_nat_gateways/{id} |  |

### uptime
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/uptime/checks |  |
| POST | /v2/uptime/checks |  |
| GET | /v2/uptime/checks/{check_id} |  |
| PUT | /v2/uptime/checks/{check_id} |  |
| DELETE | /v2/uptime/checks/{check_id} |  |
| GET | /v2/uptime/checks/{check_id}/state |  |
| GET | /v2/uptime/checks/{check_id}/alerts |  |
| POST | /v2/uptime/checks/{check_id}/alerts |  |
| GET | /v2/uptime/checks/{check_id}/alerts/{alert_id} |  |
| PUT | /v2/uptime/checks/{check_id}/alerts/{alert_id} |  |
| DELETE | /v2/uptime/checks/{check_id}/alerts/{alert_id} |  |

### gen-ai
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/gen-ai/agents |  |
| POST | /v2/gen-ai/agents |  |
| GET | /v2/gen-ai/agents/{agent_uuid}/api_keys |  |
| POST | /v2/gen-ai/agents/{agent_uuid}/api_keys |  |
| PUT | /v2/gen-ai/agents/{agent_uuid}/api_keys/{api_key_uuid} |  |
| DELETE | /v2/gen-ai/agents/{agent_uuid}/api_keys/{api_key_uuid} |  |
| PUT | /v2/gen-ai/agents/{agent_uuid}/api_keys/{api_key_uuid}/regenerate |  |
| POST | /v2/gen-ai/agents/{agent_uuid}/functions |  |
| PUT | /v2/gen-ai/agents/{agent_uuid}/functions/{function_uuid} |  |
| DELETE | /v2/gen-ai/agents/{agent_uuid}/functions/{function_uuid} |  |
| POST | /v2/gen-ai/agents/{agent_uuid}/guardrails |  |
| DELETE | /v2/gen-ai/agents/{agent_uuid}/guardrails/{guardrail_uuid} |  |
| POST | /v2/gen-ai/agents/{agent_uuid}/knowledge_bases |  |
| POST | /v2/gen-ai/agents/{agent_uuid}/knowledge_bases/{knowledge_base_uuid} |  |
| DELETE | /v2/gen-ai/agents/{agent_uuid}/knowledge_bases/{knowledge_base_uuid} |  |
| POST | /v2/gen-ai/agents/{parent_agent_uuid}/child_agents/{child_agent_uuid} |  |
| PUT | /v2/gen-ai/agents/{parent_agent_uuid}/child_agents/{child_agent_uuid} |  |
| DELETE | /v2/gen-ai/agents/{parent_agent_uuid}/child_agents/{child_agent_uuid} |  |
| GET | /v2/gen-ai/agents/{uuid} |  |
| PUT | /v2/gen-ai/agents/{uuid} |  |
| DELETE | /v2/gen-ai/agents/{uuid} |  |
| GET | /v2/gen-ai/agents/{uuid}/child_agents |  |
| PUT | /v2/gen-ai/agents/{uuid}/deployment_visibility |  |
| GET | /v2/gen-ai/agents/{uuid}/usage |  |
| GET | /v2/gen-ai/agents/{uuid}/versions |  |
| PUT | /v2/gen-ai/agents/{uuid}/versions |  |
| GET | /v2/gen-ai/anthropic/keys |  |
| POST | /v2/gen-ai/anthropic/keys |  |
| GET | /v2/gen-ai/anthropic/keys/{api_key_uuid} |  |
| PUT | /v2/gen-ai/anthropic/keys/{api_key_uuid} |  |
| DELETE | /v2/gen-ai/anthropic/keys/{api_key_uuid} |  |
| GET | /v2/gen-ai/anthropic/keys/{uuid}/agents |  |
| POST | /v2/gen-ai/evaluation_datasets |  |
| POST | /v2/gen-ai/evaluation_datasets/file_upload_presigned_urls |  |
| GET | /v2/gen-ai/evaluation_metrics |  |
| POST | /v2/gen-ai/evaluation_runs |  |
| GET | /v2/gen-ai/evaluation_runs/{evaluation_run_uuid} |  |
| GET | /v2/gen-ai/evaluation_runs/{evaluation_run_uuid}/results |  |
| GET | /v2/gen-ai/evaluation_runs/{evaluation_run_uuid}/results/{prompt_id} |  |
| GET | /v2/gen-ai/evaluation_test_cases |  |
| POST | /v2/gen-ai/evaluation_test_cases |  |
| GET | /v2/gen-ai/evaluation_test_cases/{evaluation_test_case_uuid}/evaluation_runs |  |
| GET | /v2/gen-ai/evaluation_test_cases/{test_case_uuid} |  |
| PUT | /v2/gen-ai/evaluation_test_cases/{test_case_uuid} |  |
| GET | /v2/gen-ai/indexing_jobs |  |
| POST | /v2/gen-ai/indexing_jobs |  |
| GET | /v2/gen-ai/indexing_jobs/{indexing_job_uuid}/data_sources |  |
| GET | /v2/gen-ai/indexing_jobs/{indexing_job_uuid}/details_signed_url |  |
| GET | /v2/gen-ai/indexing_jobs/{uuid} |  |
| PUT | /v2/gen-ai/indexing_jobs/{uuid}/cancel |  |
| GET | /v2/gen-ai/knowledge_bases |  |
| POST | /v2/gen-ai/knowledge_bases |  |
| POST | /v2/gen-ai/knowledge_bases/data_sources/file_upload_presigned_urls |  |
| GET | /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources |  |
| POST | /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources |  |
| PUT | /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources/{data_source_uuid} |  |
| DELETE | /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources/{data_source_uuid} |  |
| GET | /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/indexing_jobs |  |
| GET | /v2/gen-ai/knowledge_bases/{uuid} |  |
| PUT | /v2/gen-ai/knowledge_bases/{uuid} |  |
| DELETE | /v2/gen-ai/knowledge_bases/{uuid} |  |
| GET | /v2/gen-ai/models |  |
| GET | /v2/gen-ai/models/api_keys |  |
| POST | /v2/gen-ai/models/api_keys |  |
| PUT | /v2/gen-ai/models/api_keys/{api_key_uuid} |  |
| DELETE | /v2/gen-ai/models/api_keys/{api_key_uuid} |  |
| PUT | /v2/gen-ai/models/api_keys/{api_key_uuid}/regenerate |  |
| POST | /v2/gen-ai/oauth2/dropbox/tokens |  |
| GET | /v2/gen-ai/oauth2/url |  |
| GET | /v2/gen-ai/openai/keys |  |
| POST | /v2/gen-ai/openai/keys |  |
| GET | /v2/gen-ai/openai/keys/{api_key_uuid} |  |
| PUT | /v2/gen-ai/openai/keys/{api_key_uuid} |  |
| DELETE | /v2/gen-ai/openai/keys/{api_key_uuid} |  |
| GET | /v2/gen-ai/openai/keys/{uuid}/agents |  |
| GET | /v2/gen-ai/regions |  |
| POST | /v2/gen-ai/scheduled-indexing |  |
| GET | /v2/gen-ai/scheduled-indexing/knowledge-base/{knowledge_base_uuid} |  |
| DELETE | /v2/gen-ai/scheduled-indexing/{uuid} |  |
| GET | /v2/gen-ai/workspaces |  |
| POST | /v2/gen-ai/workspaces |  |
| GET | /v2/gen-ai/workspaces/{workspace_uuid} |  |
| PUT | /v2/gen-ai/workspaces/{workspace_uuid} |  |
| DELETE | /v2/gen-ai/workspaces/{workspace_uuid} |  |
| GET | /v2/gen-ai/workspaces/{workspace_uuid}/agents |  |
| PUT | /v2/gen-ai/workspaces/{workspace_uuid}/agents |  |
| GET | /v2/gen-ai/workspaces/{workspace_uuid}/evaluation_test_cases |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all 1-clicks?" -> GET /v2/1-clicks
- "Create a kubernete?" -> POST /v2/1-clicks/kubernetes
- "List all account?" -> GET /v2/account
- "List all keys?" -> GET /v2/account/keys
- "Create a key?" -> POST /v2/account/keys
- "Get key details?" -> GET /v2/account/keys/{ssh_key_identifier}
- "Update a key?" -> PUT /v2/account/keys/{ssh_key_identifier}
- "Delete a key?" -> DELETE /v2/account/keys/{ssh_key_identifier}
- "List all actions?" -> GET /v2/actions
- "Get action details?" -> GET /v2/actions/{action_id}
- "List all apps?" -> GET /v2/add-ons/apps
- "List all metadata?" -> GET /v2/add-ons/apps/{app_slug}/metadata
- "List all saas?" -> GET /v2/add-ons/saas
- "Create a saa?" -> POST /v2/add-ons/saas
- "Get saa details?" -> GET /v2/add-ons/saas/{resource_uuid}
- "Delete a saa?" -> DELETE /v2/add-ons/saas/{resource_uuid}
- "Partially update a saa?" -> PATCH /v2/add-ons/saas/{resource_uuid}
- "List all apps?" -> GET /v2/apps
- "Create a app?" -> POST /v2/apps
- "Delete a app?" -> DELETE /v2/apps/{id}
- "Get app details?" -> GET /v2/apps/{id}
- "Update a app?" -> PUT /v2/apps/{id}
- "Create a restart?" -> POST /v2/apps/{app_id}/restart
- "List all logs?" -> GET /v2/apps/{app_id}/components/{component_name}/logs
- "List all exec?" -> GET /v2/apps/{app_id}/components/{component_name}/exec
- "List all instances?" -> GET /v2/apps/{app_id}/instances
- "List all deployments?" -> GET /v2/apps/{app_id}/deployments
- "Create a deployment?" -> POST /v2/apps/{app_id}/deployments
- "Get deployment details?" -> GET /v2/apps/{app_id}/deployments/{deployment_id}
- "Create a cancel?" -> POST /v2/apps/{app_id}/deployments/{deployment_id}/cancel
- "List all logs?" -> GET /v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/logs
- "List all logs?" -> GET /v2/apps/{app_id}/deployments/{deployment_id}/logs
- "List all exec?" -> GET /v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/exec
- "List all logs?" -> GET /v2/apps/{app_id}/logs
- "List all job-invocations?" -> GET /v2/apps/{app_id}/job-invocations
- "Get job-invocation details?" -> GET /v2/apps/{app_id}/job-invocations/{job_invocation_id}
- "Create a cancel?" -> POST /v2/apps/{app_id}/job-invocations/{job_invocation_id}/cancel
- "List all logs?" -> GET /v2/apps/{app_id}/jobs/{job_name}/invocations/{job_invocation_id}/logs
- "List all instance_sizes?" -> GET /v2/apps/tiers/instance_sizes
- "Get instance_size details?" -> GET /v2/apps/tiers/instance_sizes/{slug}
- "List all regions?" -> GET /v2/apps/regions
- "Create a propose?" -> POST /v2/apps/propose
- "List all alerts?" -> GET /v2/apps/{app_id}/alerts
- "Create a destination?" -> POST /v2/apps/{app_id}/alerts/{alert_id}/destinations
- "Create a rollback?" -> POST /v2/apps/{app_id}/rollback
- "Create a validate?" -> POST /v2/apps/{app_id}/rollback/validate
- "Create a commit?" -> POST /v2/apps/{app_id}/rollback/commit
- "Create a revert?" -> POST /v2/apps/{app_id}/rollback/revert
- "List all bandwidth_daily?" -> GET /v2/apps/{app_id}/metrics/bandwidth_daily
- "Create a bandwidth_daily?" -> POST /v2/apps/metrics/bandwidth_daily
- "List all health?" -> GET /v2/apps/{app_id}/health
- "List all endpoints?" -> GET /v2/cdn/endpoints
- "Create a endpoint?" -> POST /v2/cdn/endpoints
- "Get endpoint details?" -> GET /v2/cdn/endpoints/{cdn_id}
- "Update a endpoint?" -> PUT /v2/cdn/endpoints/{cdn_id}
- "Delete a endpoint?" -> DELETE /v2/cdn/endpoints/{cdn_id}
- "List all certificates?" -> GET /v2/certificates
- "Create a certificate?" -> POST /v2/certificates
- "Get certificate details?" -> GET /v2/certificates/{certificate_id}
- "Delete a certificate?" -> DELETE /v2/certificates/{certificate_id}
- "List all balance?" -> GET /v2/customers/my/balance
- "List all billing_history?" -> GET /v2/customers/my/billing_history
- "List all invoices?" -> GET /v2/customers/my/invoices
- "Get invoice details?" -> GET /v2/customers/my/invoices/{invoice_uuid}
- "List all csv?" -> GET /v2/customers/my/invoices/{invoice_uuid}/csv
- "List all pdf?" -> GET /v2/customers/my/invoices/{invoice_uuid}/pdf
- "List all summary?" -> GET /v2/customers/my/invoices/{invoice_uuid}/summary
- "Get insight details?" -> GET /v2/billing/{account_urn}/insights/{start_date}/{end_date}
- "List all options?" -> GET /v2/databases/options
- "List all databases?" -> GET /v2/databases
- "Create a database?" -> POST /v2/databases
- "Get database details?" -> GET /v2/databases/{database_cluster_uuid}
- "Delete a database?" -> DELETE /v2/databases/{database_cluster_uuid}
- "List all config?" -> GET /v2/databases/{database_cluster_uuid}/config
- "List all ca?" -> GET /v2/databases/{database_cluster_uuid}/ca
- "List all online-migration?" -> GET /v2/databases/{database_cluster_uuid}/online-migration
- "Delete a online-migration?" -> DELETE /v2/databases/{database_cluster_uuid}/online-migration/{migration_id}
- "List all firewall?" -> GET /v2/databases/{database_cluster_uuid}/firewall
- "List all backups?" -> GET /v2/databases/{database_cluster_uuid}/backups
- "List all replicas?" -> GET /v2/databases/{database_cluster_uuid}/replicas
- "Create a replica?" -> POST /v2/databases/{database_cluster_uuid}/replicas
- "List all events?" -> GET /v2/databases/{database_cluster_uuid}/events
- "Get replica details?" -> GET /v2/databases/{database_cluster_uuid}/replicas/{replica_name}
- "Delete a replica?" -> DELETE /v2/databases/{database_cluster_uuid}/replicas/{replica_name}
- "List all users?" -> GET /v2/databases/{database_cluster_uuid}/users
- "Create a user?" -> POST /v2/databases/{database_cluster_uuid}/users
- "Get user details?" -> GET /v2/databases/{database_cluster_uuid}/users/{username}
- "Delete a user?" -> DELETE /v2/databases/{database_cluster_uuid}/users/{username}
- "Update a user?" -> PUT /v2/databases/{database_cluster_uuid}/users/{username}
- "Create a reset_auth?" -> POST /v2/databases/{database_cluster_uuid}/users/{username}/reset_auth
- "List all dbs?" -> GET /v2/databases/{database_cluster_uuid}/dbs
- "Create a db?" -> POST /v2/databases/{database_cluster_uuid}/dbs
- "Get db details?" -> GET /v2/databases/{database_cluster_uuid}/dbs/{database_name}
- "Delete a db?" -> DELETE /v2/databases/{database_cluster_uuid}/dbs/{database_name}
- "List all pools?" -> GET /v2/databases/{database_cluster_uuid}/pools
- "Create a pool?" -> POST /v2/databases/{database_cluster_uuid}/pools
- "Get pool details?" -> GET /v2/databases/{database_cluster_uuid}/pools/{pool_name}
- "Update a pool?" -> PUT /v2/databases/{database_cluster_uuid}/pools/{pool_name}
- "Delete a pool?" -> DELETE /v2/databases/{database_cluster_uuid}/pools/{pool_name}
- "List all eviction_policy?" -> GET /v2/databases/{database_cluster_uuid}/eviction_policy
- "List all sql_mode?" -> GET /v2/databases/{database_cluster_uuid}/sql_mode
- "List all autoscale?" -> GET /v2/databases/{database_cluster_uuid}/autoscale
- "List all topics?" -> GET /v2/databases/{database_cluster_uuid}/topics
- "Create a topic?" -> POST /v2/databases/{database_cluster_uuid}/topics
- "Get topic details?" -> GET /v2/databases/{database_cluster_uuid}/topics/{topic_name}
- "Update a topic?" -> PUT /v2/databases/{database_cluster_uuid}/topics/{topic_name}
- "Delete a topic?" -> DELETE /v2/databases/{database_cluster_uuid}/topics/{topic_name}
- "List all logsink?" -> GET /v2/databases/{database_cluster_uuid}/logsink
- "Create a logsink?" -> POST /v2/databases/{database_cluster_uuid}/logsink
- "Get logsink details?" -> GET /v2/databases/{database_cluster_uuid}/logsink/{logsink_id}
- "Update a logsink?" -> PUT /v2/databases/{database_cluster_uuid}/logsink/{logsink_id}
- "Delete a logsink?" -> DELETE /v2/databases/{database_cluster_uuid}/logsink/{logsink_id}
- "List all schema-registry?" -> GET /v2/databases/{database_cluster_uuid}/schema-registry
- "Create a schema-registry?" -> POST /v2/databases/{database_cluster_uuid}/schema-registry
- "Get schema-registry details?" -> GET /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name}
- "Delete a schema-registry?" -> DELETE /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name}
- "Get version details?" -> GET /v2/databases/{database_cluster_uuid}/schema-registry/{subject_name}/versions/{version}
- "List all config?" -> GET /v2/databases/{database_cluster_uuid}/schema-registry/config
- "Get config details?" -> GET /v2/databases/{database_cluster_uuid}/schema-registry/config/{subject_name}
- "Update a config?" -> PUT /v2/databases/{database_cluster_uuid}/schema-registry/config/{subject_name}
- "List all credentials?" -> GET /v2/databases/metrics/credentials
- "List all indexes?" -> GET /v2/databases/{database_cluster_uuid}/indexes
- "Delete a indexe?" -> DELETE /v2/databases/{database_cluster_uuid}/indexes/{index_name}
- "List all domains?" -> GET /v2/domains
- "Create a domain?" -> POST /v2/domains
- "Get domain details?" -> GET /v2/domains/{domain_name}
- "Delete a domain?" -> DELETE /v2/domains/{domain_name}
- "List all records?" -> GET /v2/domains/{domain_name}/records
- "Create a record?" -> POST /v2/domains/{domain_name}/records
- "Get record details?" -> GET /v2/domains/{domain_name}/records/{domain_record_id}
- "Partially update a record?" -> PATCH /v2/domains/{domain_name}/records/{domain_record_id}
- "Update a record?" -> PUT /v2/domains/{domain_name}/records/{domain_record_id}
- "Delete a record?" -> DELETE /v2/domains/{domain_name}/records/{domain_record_id}
- "List all droplets?" -> GET /v2/droplets
- "Create a droplet?" -> POST /v2/droplets
- "Get droplet details?" -> GET /v2/droplets/{droplet_id}
- "Delete a droplet?" -> DELETE /v2/droplets/{droplet_id}
- "List all backups?" -> GET /v2/droplets/{droplet_id}/backups
- "List all policy?" -> GET /v2/droplets/{droplet_id}/backups/policy
- "List all policies?" -> GET /v2/droplets/backups/policies
- "List all supported_policies?" -> GET /v2/droplets/backups/supported_policies
- "List all snapshots?" -> GET /v2/droplets/{droplet_id}/snapshots
- "List all actions?" -> GET /v2/droplets/{droplet_id}/actions
- "Create a action?" -> POST /v2/droplets/{droplet_id}/actions
- "Create a action?" -> POST /v2/droplets/actions
- "Get action details?" -> GET /v2/droplets/{droplet_id}/actions/{action_id}
- "List all kernels?" -> GET /v2/droplets/{droplet_id}/kernels
- "List all firewalls?" -> GET /v2/droplets/{droplet_id}/firewalls
- "List all neighbors?" -> GET /v2/droplets/{droplet_id}/neighbors
- "List all destroy_with_associated_resources?" -> GET /v2/droplets/{droplet_id}/destroy_with_associated_resources
- "List all status?" -> GET /v2/droplets/{droplet_id}/destroy_with_associated_resources/status
- "Create a retry?" -> POST /v2/droplets/{droplet_id}/destroy_with_associated_resources/retry
- "List all autoscale?" -> GET /v2/droplets/autoscale
- "Create a autoscale?" -> POST /v2/droplets/autoscale
- "Get autoscale details?" -> GET /v2/droplets/autoscale/{autoscale_pool_id}
- "Update a autoscale?" -> PUT /v2/droplets/autoscale/{autoscale_pool_id}
- "Delete a autoscale?" -> DELETE /v2/droplets/autoscale/{autoscale_pool_id}
- "List all members?" -> GET /v2/droplets/autoscale/{autoscale_pool_id}/members
- "List all history?" -> GET /v2/droplets/autoscale/{autoscale_pool_id}/history
- "List all firewalls?" -> GET /v2/firewalls
- "Create a firewall?" -> POST /v2/firewalls
- "Get firewall details?" -> GET /v2/firewalls/{firewall_id}
- "Update a firewall?" -> PUT /v2/firewalls/{firewall_id}
- "Delete a firewall?" -> DELETE /v2/firewalls/{firewall_id}
- "Create a droplet?" -> POST /v2/firewalls/{firewall_id}/droplets
- "Create a tag?" -> POST /v2/firewalls/{firewall_id}/tags
- "Create a rule?" -> POST /v2/firewalls/{firewall_id}/rules
- "List all floating_ips?" -> GET /v2/floating_ips
- "Create a floating_ip?" -> POST /v2/floating_ips
- "Get floating_ip details?" -> GET /v2/floating_ips/{floating_ip}
- "Delete a floating_ip?" -> DELETE /v2/floating_ips/{floating_ip}
- "List all actions?" -> GET /v2/floating_ips/{floating_ip}/actions
- "Create a action?" -> POST /v2/floating_ips/{floating_ip}/actions
- "Get action details?" -> GET /v2/floating_ips/{floating_ip}/actions/{action_id}
- "List all namespaces?" -> GET /v2/functions/namespaces
- "Create a namespace?" -> POST /v2/functions/namespaces
- "Get namespace details?" -> GET /v2/functions/namespaces/{namespace_id}
- "Delete a namespace?" -> DELETE /v2/functions/namespaces/{namespace_id}
- "List all triggers?" -> GET /v2/functions/namespaces/{namespace_id}/triggers
- "Create a trigger?" -> POST /v2/functions/namespaces/{namespace_id}/triggers
- "Get trigger details?" -> GET /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}
- "Update a trigger?" -> PUT /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}
- "Delete a trigger?" -> DELETE /v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}
- "List all images?" -> GET /v2/images
- "Create a image?" -> POST /v2/images
- "Get image details?" -> GET /v2/images/{image_id}
- "Update a image?" -> PUT /v2/images/{image_id}
- "Delete a image?" -> DELETE /v2/images/{image_id}
- "List all actions?" -> GET /v2/images/{image_id}/actions
- "Create a action?" -> POST /v2/images/{image_id}/actions
- "Get action details?" -> GET /v2/images/{image_id}/actions/{action_id}
- "List all clusters?" -> GET /v2/kubernetes/clusters
- "Create a cluster?" -> POST /v2/kubernetes/clusters
- "Get cluster details?" -> GET /v2/kubernetes/clusters/{cluster_id}
- "Update a cluster?" -> PUT /v2/kubernetes/clusters/{cluster_id}
- "Delete a cluster?" -> DELETE /v2/kubernetes/clusters/{cluster_id}
- "List all destroy_with_associated_resources?" -> GET /v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources
- "List all kubeconfig?" -> GET /v2/kubernetes/clusters/{cluster_id}/kubeconfig
- "List all credentials?" -> GET /v2/kubernetes/clusters/{cluster_id}/credentials
- "List all upgrades?" -> GET /v2/kubernetes/clusters/{cluster_id}/upgrades
- "Create a upgrade?" -> POST /v2/kubernetes/clusters/{cluster_id}/upgrade
- "List all node_pools?" -> GET /v2/kubernetes/clusters/{cluster_id}/node_pools
- "Create a node_pool?" -> POST /v2/kubernetes/clusters/{cluster_id}/node_pools
- "Get node_pool details?" -> GET /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}
- "Update a node_pool?" -> PUT /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}
- "Delete a node_pool?" -> DELETE /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}
- "Delete a node?" -> DELETE /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/nodes/{node_id}
- "Create a recycle?" -> POST /v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/recycle
- "List all user?" -> GET /v2/kubernetes/clusters/{cluster_id}/user
- "List all options?" -> GET /v2/kubernetes/options
- "Create a clusterlint?" -> POST /v2/kubernetes/clusters/{cluster_id}/clusterlint
- "List all clusterlint?" -> GET /v2/kubernetes/clusters/{cluster_id}/clusterlint
- "Create a registry?" -> POST /v2/kubernetes/registry
- "Create a registry?" -> POST /v2/kubernetes/registries
- "List all status_messages?" -> GET /v2/kubernetes/clusters/{cluster_id}/status_messages
- "Create a load_balancer?" -> POST /v2/load_balancers
- "List all load_balancers?" -> GET /v2/load_balancers
- "Get load_balancer details?" -> GET /v2/load_balancers/{lb_id}
- "Update a load_balancer?" -> PUT /v2/load_balancers/{lb_id}
- "Delete a load_balancer?" -> DELETE /v2/load_balancers/{lb_id}
- "Create a droplet?" -> POST /v2/load_balancers/{lb_id}/droplets
- "Create a forwarding_rule?" -> POST /v2/load_balancers/{lb_id}/forwarding_rules
- "List all alerts?" -> GET /v2/monitoring/alerts
- "Create a alert?" -> POST /v2/monitoring/alerts
- "Get alert details?" -> GET /v2/monitoring/alerts/{alert_uuid}
- "Update a alert?" -> PUT /v2/monitoring/alerts/{alert_uuid}
- "Delete a alert?" -> DELETE /v2/monitoring/alerts/{alert_uuid}
- "List all bandwidth?" -> GET /v2/monitoring/metrics/droplet/bandwidth
- "List all cpu?" -> GET /v2/monitoring/metrics/droplet/cpu
- "List all filesystem_free?" -> GET /v2/monitoring/metrics/droplet/filesystem_free
- "List all filesystem_size?" -> GET /v2/monitoring/metrics/droplet/filesystem_size
- "List all load_1?" -> GET /v2/monitoring/metrics/droplet/load_1
- "List all load_5?" -> GET /v2/monitoring/metrics/droplet/load_5
- "List all load_15?" -> GET /v2/monitoring/metrics/droplet/load_15
- "List all memory_cached?" -> GET /v2/monitoring/metrics/droplet/memory_cached
- "List all memory_free?" -> GET /v2/monitoring/metrics/droplet/memory_free
- "List all memory_total?" -> GET /v2/monitoring/metrics/droplet/memory_total
- "List all memory_available?" -> GET /v2/monitoring/metrics/droplet/memory_available
- "List all memory_percentage?" -> GET /v2/monitoring/metrics/apps/memory_percentage
- "List all cpu_percentage?" -> GET /v2/monitoring/metrics/apps/cpu_percentage
- "List all restart_count?" -> GET /v2/monitoring/metrics/apps/restart_count
- "List all frontend_connections_current?" -> GET /v2/monitoring/metrics/load_balancer/frontend_connections_current
- "List all frontend_connections_limit?" -> GET /v2/monitoring/metrics/load_balancer/frontend_connections_limit
- "List all frontend_cpu_utilization?" -> GET /v2/monitoring/metrics/load_balancer/frontend_cpu_utilization
- "List all frontend_firewall_dropped_bytes?" -> GET /v2/monitoring/metrics/load_balancer/frontend_firewall_dropped_bytes
- "List all frontend_firewall_dropped_packets?" -> GET /v2/monitoring/metrics/load_balancer/frontend_firewall_dropped_packets
- "List all frontend_http_responses?" -> GET /v2/monitoring/metrics/load_balancer/frontend_http_responses
- "List all frontend_http_requests_per_second?" -> GET /v2/monitoring/metrics/load_balancer/frontend_http_requests_per_second
- "List all frontend_network_throughput_http?" -> GET /v2/monitoring/metrics/load_balancer/frontend_network_throughput_http
- "List all frontend_network_throughput_udp?" -> GET /v2/monitoring/metrics/load_balancer/frontend_network_throughput_udp
- "List all frontend_network_throughput_tcp?" -> GET /v2/monitoring/metrics/load_balancer/frontend_network_throughput_tcp
- "List all frontend_nlb_tcp_network_throughput?" -> GET /v2/monitoring/metrics/load_balancer/frontend_nlb_tcp_network_throughput
- "List all frontend_nlb_udp_network_throughput?" -> GET /v2/monitoring/metrics/load_balancer/frontend_nlb_udp_network_throughput
- "List all frontend_tls_connections_current?" -> GET /v2/monitoring/metrics/load_balancer/frontend_tls_connections_current
- "List all frontend_tls_connections_limit?" -> GET /v2/monitoring/metrics/load_balancer/frontend_tls_connections_limit
- "List all frontend_tls_connections_exceeding_rate_limit?" -> GET /v2/monitoring/metrics/load_balancer/frontend_tls_connections_exceeding_rate_limit
- "List all droplets_http_session_duration_avg?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_avg
- "List all droplets_http_session_duration_50p?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_50p
- "List all droplets_http_session_duration_95p?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_session_duration_95p
- "List all droplets_http_response_time_avg?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_response_time_avg
- "List all droplets_http_response_time_50p?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_response_time_50p
- "List all droplets_http_response_time_95p?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_response_time_95p
- "List all droplets_http_response_time_99p?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_response_time_99p
- "List all droplets_queue_size?" -> GET /v2/monitoring/metrics/load_balancer/droplets_queue_size
- "List all droplets_http_responses?" -> GET /v2/monitoring/metrics/load_balancer/droplets_http_responses
- "List all droplets_connections?" -> GET /v2/monitoring/metrics/load_balancer/droplets_connections
- "List all droplets_health_checks?" -> GET /v2/monitoring/metrics/load_balancer/droplets_health_checks
- "List all droplets_downtime?" -> GET /v2/monitoring/metrics/load_balancer/droplets_downtime
- "List all current_instances?" -> GET /v2/monitoring/metrics/droplet_autoscale/current_instances
- "List all target_instances?" -> GET /v2/monitoring/metrics/droplet_autoscale/target_instances
- "List all current_cpu_utilization?" -> GET /v2/monitoring/metrics/droplet_autoscale/current_cpu_utilization
- "List all target_cpu_utilization?" -> GET /v2/monitoring/metrics/droplet_autoscale/target_cpu_utilization
- "List all current_memory_utilization?" -> GET /v2/monitoring/metrics/droplet_autoscale/current_memory_utilization
- "List all target_memory_utilization?" -> GET /v2/monitoring/metrics/droplet_autoscale/target_memory_utilization
- "List all cpu_usage?" -> GET /v2/monitoring/metrics/database/mysql/cpu_usage
- "List all load?" -> GET /v2/monitoring/metrics/database/mysql/load
- "List all memory_usage?" -> GET /v2/monitoring/metrics/database/mysql/memory_usage
- "List all disk_usage?" -> GET /v2/monitoring/metrics/database/mysql/disk_usage
- "List all threads_connected?" -> GET /v2/monitoring/metrics/database/mysql/threads_connected
- "List all threads_created_rate?" -> GET /v2/monitoring/metrics/database/mysql/threads_created_rate
- "List all threads_active?" -> GET /v2/monitoring/metrics/database/mysql/threads_active
- "List all index_vs_sequential_reads?" -> GET /v2/monitoring/metrics/database/mysql/index_vs_sequential_reads
- "List all op_rates?" -> GET /v2/monitoring/metrics/database/mysql/op_rates
- "List all schema_throughput?" -> GET /v2/monitoring/metrics/database/mysql/schema_throughput
- "List all schema_latency?" -> GET /v2/monitoring/metrics/database/mysql/schema_latency
- "Create a destination?" -> POST /v2/monitoring/sinks/destinations
- "List all destinations?" -> GET /v2/monitoring/sinks/destinations
- "Get destination details?" -> GET /v2/monitoring/sinks/destinations/{destination_uuid}
- "Delete a destination?" -> DELETE /v2/monitoring/sinks/destinations/{destination_uuid}
- "Create a sink?" -> POST /v2/monitoring/sinks
- "List all sinks?" -> GET /v2/monitoring/sinks
- "Get sink details?" -> GET /v2/monitoring/sinks/{sink_uuid}
- "Delete a sink?" -> DELETE /v2/monitoring/sinks/{sink_uuid}
- "Create a nf?" -> POST /v2/nfs
- "List all nfs?" -> GET /v2/nfs
- "Get nf details?" -> GET /v2/nfs/{nfs_id}
- "Delete a nf?" -> DELETE /v2/nfs/{nfs_id}
- "Create a action?" -> POST /v2/nfs/{nfs_id}/actions
- "List all snapshots?" -> GET /v2/nfs/snapshots
- "Get snapshot details?" -> GET /v2/nfs/snapshots/{nfs_snapshot_id}
- "Delete a snapshot?" -> DELETE /v2/nfs/snapshots/{nfs_snapshot_id}
- "List all attachments?" -> GET /v2/partner_network_connect/attachments
- "Create a attachment?" -> POST /v2/partner_network_connect/attachments
- "Get attachment details?" -> GET /v2/partner_network_connect/attachments/{pa_id}
- "Partially update a attachment?" -> PATCH /v2/partner_network_connect/attachments/{pa_id}
- "Delete a attachment?" -> DELETE /v2/partner_network_connect/attachments/{pa_id}
- "List all bgp_auth_key?" -> GET /v2/partner_network_connect/attachments/{pa_id}/bgp_auth_key
- "List all remote_routes?" -> GET /v2/partner_network_connect/attachments/{pa_id}/remote_routes
- "List all service_key?" -> GET /v2/partner_network_connect/attachments/{pa_id}/service_key
- "Create a service_key?" -> POST /v2/partner_network_connect/attachments/{pa_id}/service_key
- "List all projects?" -> GET /v2/projects
- "Create a project?" -> POST /v2/projects
- "List all default?" -> GET /v2/projects/default
- "Get project details?" -> GET /v2/projects/{project_id}
- "Update a project?" -> PUT /v2/projects/{project_id}
- "Partially update a project?" -> PATCH /v2/projects/{project_id}
- "Delete a project?" -> DELETE /v2/projects/{project_id}
- "List all resources?" -> GET /v2/projects/{project_id}/resources
- "Create a resource?" -> POST /v2/projects/{project_id}/resources
- "List all resources?" -> GET /v2/projects/default/resources
- "Create a resource?" -> POST /v2/projects/default/resources
- "List all regions?" -> GET /v2/regions
- "List all registries?" -> GET /v2/registries
- "Create a registry?" -> POST /v2/registries
- "Get registry details?" -> GET /v2/registries/{registry_name}
- "Delete a registry?" -> DELETE /v2/registries/{registry_name}
- "List all docker-credentials?" -> GET /v2/registries/{registry_name}/docker-credentials
- "List all subscription?" -> GET /v2/registries/subscription
- "Create a subscription?" -> POST /v2/registries/subscription
- "List all options?" -> GET /v2/registries/options
- "List all garbage-collection?" -> GET /v2/registries/{registry_name}/garbage-collection
- "Create a garbage-collection?" -> POST /v2/registries/{registry_name}/garbage-collection
- "List all garbage-collections?" -> GET /v2/registries/{registry_name}/garbage-collections
- "Update a garbage-collection?" -> PUT /v2/registries/{registry_name}/garbage-collection/{garbage_collection_uuid}
- "List all repositoriesV2?" -> GET /v2/registries/{registry_name}/repositoriesV2
- "Delete a repository?" -> DELETE /v2/registries/{registry_name}/repositories/{repository_name}
- "List all tags?" -> GET /v2/registries/{registry_name}/repositories/{repository_name}/tags
- "Delete a tag?" -> DELETE /v2/registries/{registry_name}/repositories/{repository_name}/tags/{repository_tag}
- "List all digests?" -> GET /v2/registries/{registry_name}/repositories/{repository_name}/digests
- "Delete a digest?" -> DELETE /v2/registries/{registry_name}/repositories/{repository_name}/digests/{manifest_digest}
- "Create a validate-name?" -> POST /v2/registries/validate-name
- "List all registry?" -> GET /v2/registry
- "Create a registry?" -> POST /v2/registry
- "List all subscription?" -> GET /v2/registry/subscription
- "Create a subscription?" -> POST /v2/registry/subscription
- "List all docker-credentials?" -> GET /v2/registry/docker-credentials
- "Create a validate-name?" -> POST /v2/registry/validate-name
- "List all repositories?" -> GET /v2/registry/{registry_name}/repositories
- "List all repositoriesV2?" -> GET /v2/registry/{registry_name}/repositoriesV2
- "List all tags?" -> GET /v2/registry/{registry_name}/repositories/{repository_name}/tags
- "Delete a tag?" -> DELETE /v2/registry/{registry_name}/repositories/{repository_name}/tags/{repository_tag}
- "List all digests?" -> GET /v2/registry/{registry_name}/repositories/{repository_name}/digests
- "Delete a digest?" -> DELETE /v2/registry/{registry_name}/repositories/{repository_name}/digests/{manifest_digest}
- "Create a garbage-collection?" -> POST /v2/registry/{registry_name}/garbage-collection
- "List all garbage-collection?" -> GET /v2/registry/{registry_name}/garbage-collection
- "List all garbage-collections?" -> GET /v2/registry/{registry_name}/garbage-collections
- "Update a garbage-collection?" -> PUT /v2/registry/{registry_name}/garbage-collection/{garbage_collection_uuid}
- "List all options?" -> GET /v2/registry/options
- "List all droplet_neighbors_ids?" -> GET /v2/reports/droplet_neighbors_ids
- "List all reserved_ips?" -> GET /v2/reserved_ips
- "Create a reserved_ip?" -> POST /v2/reserved_ips
- "Get reserved_ip details?" -> GET /v2/reserved_ips/{reserved_ip}
- "Delete a reserved_ip?" -> DELETE /v2/reserved_ips/{reserved_ip}
- "List all actions?" -> GET /v2/reserved_ips/{reserved_ip}/actions
- "Create a action?" -> POST /v2/reserved_ips/{reserved_ip}/actions
- "Get action details?" -> GET /v2/reserved_ips/{reserved_ip}/actions/{action_id}
- "List all reserved_ipv6?" -> GET /v2/reserved_ipv6
- "Create a reserved_ipv6?" -> POST /v2/reserved_ipv6
- "Get reserved_ipv6 details?" -> GET /v2/reserved_ipv6/{reserved_ipv6}
- "Delete a reserved_ipv6?" -> DELETE /v2/reserved_ipv6/{reserved_ipv6}
- "Create a action?" -> POST /v2/reserved_ipv6/{reserved_ipv6}/actions
- "Create a byoip_prefixe?" -> POST /v2/byoip_prefixes
- "List all byoip_prefixes?" -> GET /v2/byoip_prefixes
- "Get byoip_prefixe details?" -> GET /v2/byoip_prefixes/{byoip_prefix_uuid}
- "Delete a byoip_prefixe?" -> DELETE /v2/byoip_prefixes/{byoip_prefix_uuid}
- "Partially update a byoip_prefixe?" -> PATCH /v2/byoip_prefixes/{byoip_prefix_uuid}
- "List all ips?" -> GET /v2/byoip_prefixes/{byoip_prefix_uuid}/ips
- "List all sizes?" -> GET /v2/sizes
- "List all snapshots?" -> GET /v2/snapshots
- "Get snapshot details?" -> GET /v2/snapshots/{snapshot_id}
- "Delete a snapshot?" -> DELETE /v2/snapshots/{snapshot_id}
- "List all keys?" -> GET /v2/spaces/keys
- "Create a key?" -> POST /v2/spaces/keys
- "Get key details?" -> GET /v2/spaces/keys/{access_key}
- "Delete a key?" -> DELETE /v2/spaces/keys/{access_key}
- "Update a key?" -> PUT /v2/spaces/keys/{access_key}
- "Partially update a key?" -> PATCH /v2/spaces/keys/{access_key}
- "List all tags?" -> GET /v2/tags
- "Create a tag?" -> POST /v2/tags
- "Get tag details?" -> GET /v2/tags/{tag_id}
- "Delete a tag?" -> DELETE /v2/tags/{tag_id}
- "Create a resource?" -> POST /v2/tags/{tag_id}/resources
- "List all volumes?" -> GET /v2/volumes
- "Create a volume?" -> POST /v2/volumes
- "Create a action?" -> POST /v2/volumes/actions
- "Get snapshot details?" -> GET /v2/volumes/snapshots/{snapshot_id}
- "Delete a snapshot?" -> DELETE /v2/volumes/snapshots/{snapshot_id}
- "Get volume details?" -> GET /v2/volumes/{volume_id}
- "Delete a volume?" -> DELETE /v2/volumes/{volume_id}
- "List all actions?" -> GET /v2/volumes/{volume_id}/actions
- "Create a action?" -> POST /v2/volumes/{volume_id}/actions
- "Get action details?" -> GET /v2/volumes/{volume_id}/actions/{action_id}
- "List all snapshots?" -> GET /v2/volumes/{volume_id}/snapshots
- "Create a snapshot?" -> POST /v2/volumes/{volume_id}/snapshots
- "List all vpcs?" -> GET /v2/vpcs
- "Create a vpc?" -> POST /v2/vpcs
- "Get vpc details?" -> GET /v2/vpcs/{vpc_id}
- "Update a vpc?" -> PUT /v2/vpcs/{vpc_id}
- "Partially update a vpc?" -> PATCH /v2/vpcs/{vpc_id}
- "Delete a vpc?" -> DELETE /v2/vpcs/{vpc_id}
- "List all members?" -> GET /v2/vpcs/{vpc_id}/members
- "List all peerings?" -> GET /v2/vpcs/{vpc_id}/peerings
- "Create a peering?" -> POST /v2/vpcs/{vpc_id}/peerings
- "Partially update a peering?" -> PATCH /v2/vpcs/{vpc_id}/peerings/{vpc_peering_id}
- "List all vpc_peerings?" -> GET /v2/vpc_peerings
- "Create a vpc_peering?" -> POST /v2/vpc_peerings
- "Get vpc_peering details?" -> GET /v2/vpc_peerings/{vpc_peering_id}
- "Partially update a vpc_peering?" -> PATCH /v2/vpc_peerings/{vpc_peering_id}
- "Delete a vpc_peering?" -> DELETE /v2/vpc_peerings/{vpc_peering_id}
- "List all vpc_nat_gateways?" -> GET /v2/vpc_nat_gateways
- "Create a vpc_nat_gateway?" -> POST /v2/vpc_nat_gateways
- "Get vpc_nat_gateway details?" -> GET /v2/vpc_nat_gateways/{id}
- "Update a vpc_nat_gateway?" -> PUT /v2/vpc_nat_gateways/{id}
- "Delete a vpc_nat_gateway?" -> DELETE /v2/vpc_nat_gateways/{id}
- "List all checks?" -> GET /v2/uptime/checks
- "Create a check?" -> POST /v2/uptime/checks
- "Get check details?" -> GET /v2/uptime/checks/{check_id}
- "Update a check?" -> PUT /v2/uptime/checks/{check_id}
- "Delete a check?" -> DELETE /v2/uptime/checks/{check_id}
- "List all state?" -> GET /v2/uptime/checks/{check_id}/state
- "List all alerts?" -> GET /v2/uptime/checks/{check_id}/alerts
- "Create a alert?" -> POST /v2/uptime/checks/{check_id}/alerts
- "Get alert details?" -> GET /v2/uptime/checks/{check_id}/alerts/{alert_id}
- "Update a alert?" -> PUT /v2/uptime/checks/{check_id}/alerts/{alert_id}
- "Delete a alert?" -> DELETE /v2/uptime/checks/{check_id}/alerts/{alert_id}
- "List all agents?" -> GET /v2/gen-ai/agents
- "Create a agent?" -> POST /v2/gen-ai/agents
- "List all api_keys?" -> GET /v2/gen-ai/agents/{agent_uuid}/api_keys
- "Create a api_key?" -> POST /v2/gen-ai/agents/{agent_uuid}/api_keys
- "Update a api_key?" -> PUT /v2/gen-ai/agents/{agent_uuid}/api_keys/{api_key_uuid}
- "Delete a api_key?" -> DELETE /v2/gen-ai/agents/{agent_uuid}/api_keys/{api_key_uuid}
- "Create a function?" -> POST /v2/gen-ai/agents/{agent_uuid}/functions
- "Update a function?" -> PUT /v2/gen-ai/agents/{agent_uuid}/functions/{function_uuid}
- "Delete a function?" -> DELETE /v2/gen-ai/agents/{agent_uuid}/functions/{function_uuid}
- "Create a guardrail?" -> POST /v2/gen-ai/agents/{agent_uuid}/guardrails
- "Delete a guardrail?" -> DELETE /v2/gen-ai/agents/{agent_uuid}/guardrails/{guardrail_uuid}
- "Create a knowledge_base?" -> POST /v2/gen-ai/agents/{agent_uuid}/knowledge_bases
- "Delete a knowledge_base?" -> DELETE /v2/gen-ai/agents/{agent_uuid}/knowledge_bases/{knowledge_base_uuid}
- "Update a child_agent?" -> PUT /v2/gen-ai/agents/{parent_agent_uuid}/child_agents/{child_agent_uuid}
- "Delete a child_agent?" -> DELETE /v2/gen-ai/agents/{parent_agent_uuid}/child_agents/{child_agent_uuid}
- "Get agent details?" -> GET /v2/gen-ai/agents/{uuid}
- "Update a agent?" -> PUT /v2/gen-ai/agents/{uuid}
- "Delete a agent?" -> DELETE /v2/gen-ai/agents/{uuid}
- "List all child_agents?" -> GET /v2/gen-ai/agents/{uuid}/child_agents
- "List all usage?" -> GET /v2/gen-ai/agents/{uuid}/usage
- "List all versions?" -> GET /v2/gen-ai/agents/{uuid}/versions
- "List all keys?" -> GET /v2/gen-ai/anthropic/keys
- "Create a key?" -> POST /v2/gen-ai/anthropic/keys
- "Get key details?" -> GET /v2/gen-ai/anthropic/keys/{api_key_uuid}
- "Update a key?" -> PUT /v2/gen-ai/anthropic/keys/{api_key_uuid}
- "Delete a key?" -> DELETE /v2/gen-ai/anthropic/keys/{api_key_uuid}
- "List all agents?" -> GET /v2/gen-ai/anthropic/keys/{uuid}/agents
- "Create a evaluation_dataset?" -> POST /v2/gen-ai/evaluation_datasets
- "Create a file_upload_presigned_url?" -> POST /v2/gen-ai/evaluation_datasets/file_upload_presigned_urls
- "List all evaluation_metrics?" -> GET /v2/gen-ai/evaluation_metrics
- "Create a evaluation_run?" -> POST /v2/gen-ai/evaluation_runs
- "Get evaluation_run details?" -> GET /v2/gen-ai/evaluation_runs/{evaluation_run_uuid}
- "List all results?" -> GET /v2/gen-ai/evaluation_runs/{evaluation_run_uuid}/results
- "Get result details?" -> GET /v2/gen-ai/evaluation_runs/{evaluation_run_uuid}/results/{prompt_id}
- "List all evaluation_test_cases?" -> GET /v2/gen-ai/evaluation_test_cases
- "Create a evaluation_test_case?" -> POST /v2/gen-ai/evaluation_test_cases
- "List all evaluation_runs?" -> GET /v2/gen-ai/evaluation_test_cases/{evaluation_test_case_uuid}/evaluation_runs
- "Get evaluation_test_case details?" -> GET /v2/gen-ai/evaluation_test_cases/{test_case_uuid}
- "Update a evaluation_test_case?" -> PUT /v2/gen-ai/evaluation_test_cases/{test_case_uuid}
- "List all indexing_jobs?" -> GET /v2/gen-ai/indexing_jobs
- "Create a indexing_job?" -> POST /v2/gen-ai/indexing_jobs
- "List all data_sources?" -> GET /v2/gen-ai/indexing_jobs/{indexing_job_uuid}/data_sources
- "List all details_signed_url?" -> GET /v2/gen-ai/indexing_jobs/{indexing_job_uuid}/details_signed_url
- "Get indexing_job details?" -> GET /v2/gen-ai/indexing_jobs/{uuid}
- "List all knowledge_bases?" -> GET /v2/gen-ai/knowledge_bases
- "Create a knowledge_base?" -> POST /v2/gen-ai/knowledge_bases
- "Create a file_upload_presigned_url?" -> POST /v2/gen-ai/knowledge_bases/data_sources/file_upload_presigned_urls
- "List all data_sources?" -> GET /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources
- "Create a data_source?" -> POST /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources
- "Update a data_source?" -> PUT /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources/{data_source_uuid}
- "Delete a data_source?" -> DELETE /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/data_sources/{data_source_uuid}
- "List all indexing_jobs?" -> GET /v2/gen-ai/knowledge_bases/{knowledge_base_uuid}/indexing_jobs
- "Get knowledge_base details?" -> GET /v2/gen-ai/knowledge_bases/{uuid}
- "Update a knowledge_base?" -> PUT /v2/gen-ai/knowledge_bases/{uuid}
- "Delete a knowledge_base?" -> DELETE /v2/gen-ai/knowledge_bases/{uuid}
- "List all models?" -> GET /v2/gen-ai/models
- "List all api_keys?" -> GET /v2/gen-ai/models/api_keys
- "Create a api_key?" -> POST /v2/gen-ai/models/api_keys
- "Update a api_key?" -> PUT /v2/gen-ai/models/api_keys/{api_key_uuid}
- "Delete a api_key?" -> DELETE /v2/gen-ai/models/api_keys/{api_key_uuid}
- "Create a token?" -> POST /v2/gen-ai/oauth2/dropbox/tokens
- "List all url?" -> GET /v2/gen-ai/oauth2/url
- "List all keys?" -> GET /v2/gen-ai/openai/keys
- "Create a key?" -> POST /v2/gen-ai/openai/keys
- "Get key details?" -> GET /v2/gen-ai/openai/keys/{api_key_uuid}
- "Update a key?" -> PUT /v2/gen-ai/openai/keys/{api_key_uuid}
- "Delete a key?" -> DELETE /v2/gen-ai/openai/keys/{api_key_uuid}
- "List all agents?" -> GET /v2/gen-ai/openai/keys/{uuid}/agents
- "List all regions?" -> GET /v2/gen-ai/regions
- "Create a scheduled-indexing?" -> POST /v2/gen-ai/scheduled-indexing
- "Get knowledge-base details?" -> GET /v2/gen-ai/scheduled-indexing/knowledge-base/{knowledge_base_uuid}
- "Delete a scheduled-indexing?" -> DELETE /v2/gen-ai/scheduled-indexing/{uuid}
- "List all workspaces?" -> GET /v2/gen-ai/workspaces
- "Create a workspace?" -> POST /v2/gen-ai/workspaces
- "Get workspace details?" -> GET /v2/gen-ai/workspaces/{workspace_uuid}
- "Update a workspace?" -> PUT /v2/gen-ai/workspaces/{workspace_uuid}
- "Delete a workspace?" -> DELETE /v2/gen-ai/workspaces/{workspace_uuid}
- "List all agents?" -> GET /v2/gen-ai/workspaces/{workspace_uuid}/agents
- "List all evaluation_test_cases?" -> GET /v2/gen-ai/workspaces/{workspace_uuid}/evaluation_test_cases
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
