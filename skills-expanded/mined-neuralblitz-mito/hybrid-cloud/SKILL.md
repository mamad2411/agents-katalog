-----
name: hybrid-cloud
description: >
  Expert in hybrid cloud architecture combining on-premises infrastructure with public 
  cloud services. Use this skill for designing workload migration strategies, implementing 
  hybrid networking, managing unified identity, building disaster recovery solutions, 
  and optimizing workload placement across cloud and on-prem environments.
license: MIT
compatibility: opencode
metadata:
  audience: architect, devops-engineer
  category: devops
  tags: [hybrid-cloud, aws, azure, gcp, migration, networking]

# Hybrid Cloud Architecture and Integration

Covers: **Workload Migration · Hybrid Networking · Unified Identity · Disaster Recovery · Data Synchronization · Cloud Bursting · Multi-Cloud**

-----

## Hybrid Cloud Architecture Patterns

### Reference Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HYBRID CLOUD ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────────────────────────────────────────────────────────┐    │
│    │                     INTERNET / CDN                                │    │
│    └──────────────────────────────────────────────────────────────────┘    │
│                                    │                                       │
│    ┌───────────────────────────────┼───────────────────────────────┐      │
│    │                      GLOBAL LOAD BALANCER                      │      │
│    │                    (Cloudflare, AWS Global Accelerator)       │      │
│    └───────────────────────────────┬───────────────────────────────┘      │
│                                    │                                       │
│         ┌──────────────────────────┼──────────────────────────┐           │
│         │                          │                          │           │
│         ▼                          ▼                          ▼           │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐      │
│  │   ON-PREM   │           │     AWS     │           │   Azure    │      │
│  │  DATA CENTER│           │    (EKS)    │           │   (AKS)    │      │
│  │  K8s Cluster│           │  K8s Cluster│           │ K8s Cluster│      │
│  └──────┬──────┘           └──────┬──────┘           └──────┬──────┘      │
│         │                          │                          │             │
│         │                          │                          │             │
│    ┌────▼────┐               ┌──────▼─────┐             ┌──────▼─────┐       │
│    │ Database│               │   RDS/Aurora│            │  SQL Azure │       │
│    │Primary  │               │  Read Replica│            │  Primary   │       │
│    └────┬────┘               └─────────────┘             └─────────────┘       │
│         │                                                                   │
│         │                    DATA REPLICATION                               │
│         └───────────────────────────┬───────────────────────────────────────┘
│                                     │                                       │
│                              ┌──────▼──────┐                               │
│                              │  DATA GATEWAY│                               │
│                              │  (Replication)│                              │
│                              └─────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Decision Factors

| Factor | On-Premise | Cloud | Hybrid Consideration |
|--------|-----------|-------|---------------------|
| **Latency** | Low, | predictable | Variable Data locality important |
| **Compliance** | Full control | Provider-dependent | Data residency |
| **Cost** | High fixed | Variable | Workload patterns |
| **Scalability** | Limited | Elastic | Burst to cloud |
| **Management** | Full control | Reduced | Unified tools |
| **Security** | Physical + digital | Shared responsibility | Defense in depth |

```python
class HybridCloudArchitect:
    """Hybrid cloud architecture decision support"""
    
    WORKLOAD_PLACEMENT_CRITERIA = {
        'latency_sensitive': {
            'preferred': 'on_prem',
            'max_latency_ms': 10,
            'fallback': 'edge'
        },
        'regulatory': {
            'preferred': 'on_prem',
            'data_residency': 'required',
            'compliance': ['HIPAA', 'GDPR']
        },
        'burstable': {
            'preferred': 'cloud',
            'scaling': 'horizontal',
            'cost_optimization': True
        },
        'standard': {
            'preferred': 'cloud',
            'cost_optimization': True,
            'flexibility': True
        }
    }
    
    def recommend_placement(self, workload_type: str) -> dict:
        """Recommend optimal workload placement"""
        criteria = self.WORKLOAD_PLACEMENT_CRITERIA.get(workload_type)
        
        if not criteria:
            return {'recommendation': 'cloud', 'reason': 'default'}
        
        return {
            'recommendation': criteria.get('preferred', 'cloud'),
            'reason': f"Based on {workload_type} requirements",
            'alternatives': ['cloud', 'on_prem'],
            'criteria': criteria
        }
```

-----

## Workload Migration

### Migration Strategies

| Strategy | Description | Use Case | Downtime |
|----------|-------------|----------|----------|
| **Rehost (Lift & Shift)** | Move as-is | Quick migration | Medium |
| **Replatform** | Minor optimizations | AWS/Azure | Low |
| **Repurchase** | Move to SaaS | CRM, HR | Low |
| **Refactor** | Re-architect | Modernization | High |
| **Retire** | Decommission | Legacy systems | N/A |
| **Retain** | Keep on-prem | Not ready | N/A |

```python
class MigrationPlanner:
    """Plan and execute workload migration"""
    
    def __init__(self):
        self.workloads = []
        self.migration_waves = []
    
    def assess_workloads(self, inventory: list) -> list:
        """Assess workloads for migration readiness"""
        
        assessments = []
        
        for workload in inventory:
            assessment = {
                'workload_id': workload['id'],
                'name': workload['name'],
                'complexity': self._assess_complexity(workload),
                'dependencies': self._map_dependencies(workload),
                'migration_strategy': self._recommend_strategy(workload),
                'estimated_duration_days': self._estimate_duration(workload),
                'risks': self._identify_risks(workload)
            }
            assessments.append(assessment)
        
        return assessments
    
    def _assess_complexity(self, workload: dict) -> str:
        """Assess workload complexity"""
        
        score = 0
        
        # Custom code
        if workload.get('custom_code', False):
            score += 2
        
        # Database dependencies
        if workload.get('has_database', False):
            score += 2
        
        # Integration points
        if workload.get('integration_count', 0) > 5:
            score += 2
        
        # Legacy systems
        if workload.get('is_legacy', False):
            score += 1
        
        if score <= 2:
            return 'low'
        elif score <= 4:
            return 'medium'
        return 'high'
    
    def _recommend_strategy(self, workload: dict) -> str:
        """Recommend migration strategy"""
        
        complexity = self._assess_complexity(workload)
        
        if complexity == 'low':
            return 'rehost'
        elif complexity == 'medium':
            return 'replatform'
        return 'refactor'
    
    def _estimate_duration(self, workload: dict) -> int:
        """Estimate migration duration in days"""
        
        base = workload.get('vm_count', 1) * 2
        
        complexity = self._assess_complexity(workload)
        if complexity == 'high':
            base *= 2
        
        return base
    
    def _map_dependencies(self, workload: dict) -> list:
        """Map workload dependencies"""
        
        return workload.get('dependencies', [])
    
    def _identify_risks(self, workload: dict) -> list:
        """Identify migration risks"""
        
        risks = []
        
        if workload.get('integration_count', 0) > 10:
            risks.append('High integration complexity')
        
        if workload.get('has_database', False):
            risks.append('Data migration complexity')
        
        if workload.get('custom_code', False):
            risks.append('Application compatibility')
        
        return risks
    
    def create_migration_waves(self, assessments: list) -> list:
        """Create migration waves"""
        
        # Sort by complexity
        sorted_assessments = sorted(
            assessments, 
            key=lambda x: ['low', 'medium', 'high'].index(x['complexity'])
        )
        
        waves = []
        wave_size = 5
        
        for i in range(0, len(sorted_assessments), wave_size):
            wave = {
                'wave_number': i // wave_size + 1,
                'workloads': sorted_assessments[i:i+wave_size],
                'estimated_duration_days': sum(
                    w['estimated_duration_days'] 
                    for w in sorted_assessments[i:i+wave_size]
                )
            }
            waves.append(wave)
        
        self.migration_waves = waves
        return waves
```

-----

## Hybrid Networking

### VPN Connection (AWS)

```hcl
# AWS VPN Connection
resource "aws_vpn_connection" "onprem" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.onprem.id
  type                = "ipsec.1"
  static_routes_only  = false
  
  tunnel1_preshared_key = var.vpn_tunnel1_psk
  tunnel1_dip_address     = var.tunnel1_ip
  
  tunnel2_preshared_key = var.vpn_tunnel2_psk
  tunnel2_dip_address     = var.tunnel2_ip
  
  static_routes {
    destination_cidr_block = var.onprem_cidr
  }
  
  tags = {
    Name = "hybrid-vpn"
  }
}

# Customer Gateway
resource "aws_customer_gateway" "onprem" {
  bgp_asn    = 65001
  ip_address = var.onprem_gateway_ip
  type       = "ipsec.1"
  
  tags = {
    Name = "onprem-cgw"
  }
}

# VPN Gateway
resource "aws_vpn_gateway" "main" {
  amazon_side_asn = "64512"
  
  tags = {
    Name = "hybrid-vpn-gateway"
  }
}

# VPN Gateway Attachment
resource "aws_vpn_gateway_attachment" "main" {
  vpc_id     = aws_vpc.main.id
  vpn_gateway_id = aws_vpn_gateway.main.id
}
```

### Azure ExpressRoute

```hcl
# ExpressRoute Circuit
resource "azurerm_express_route_circuit" "main" {
  name                  = "hybrid-expressroute"
  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  
  sku {
    tier   = "Standard"
    family = "MeteredData"
  }
  
  service_provider_name = "Equinix"
  peering_location      = "Silicon Valley"
  bandwidth_in_mbps    = 1000
  
  allow_classic_operations = false
  
  tags = {
    Environment = "Production"
  }
}

# ExpressRoute Gateway
resource "azurerm_virtual_network_gateway" "expressroute" {
  name                = "expressroute-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.location
  
  type   = "ExpressRoute"
  vpn_type = "RouteBased"
  
  sku {
    tier  = "Standard"
    family = "VPNGw1"
  }
  
  ip_configuration {
    name                 = "default"
    public_ip_address_id = azurerm_public_ip.main.id
  }
}

# ExpressRoute Connection
resource "azurerm_express_route_connection" "main" {
  name                          = "onprem-connection"
  express_route_circuit_peering_id = azurerm_express_route_circuit.main.id
  virtual_network_gateway_id     = azurerm_virtual_network_gateway.expressroute.id
  
  enable_private_link_fast_path = true
}
```

### Google Cloud Interconnect

```hcl
# Dedicated Interconnect
resource "google_compute_interconnect_attachment" "onprem" {
  name         = "hybrid-interconnect"
  region       = "us-central1"
  router       = google_compute_router.main.name
  interconnect = "interconnect-1"
  candidate_subnets = ["169.254.0.0/29"]
  vlan_tag8021q = 100
}

# Cloud Router
resource "google_compute_router" "main" {
  name    = "hybrid-router"
  region  = "us-central1"
  network = google_compute_network.main.name
  
  bgp {
    asn = 65001
    advertise_mode = "CUSTOM"
    advertised_prefixes = [var.onprem_cidr]
  }
}
```

-----

## Unified Identity Management

### Cross-Cloud Identity Federation

```yaml
# AWS IAM Roles Anywhere
apiVersion: v1
kind: ConfigMap
metadata:
  name: identity-config
data:
  rolesanywhere-config.yaml: |
    # Trust anchor for cross-cloud identity
    trustAnchor:
      source:
        certificateAuthorities:
        - certificate: |
            -----BEGIN CERTIFICATE-----
            # CA certificate from identity provider
            -----END CERTIFICATE-----
    
    # Role definitions
    roles:
    - name: CrossCloudReader
      roleArn: arn:aws:iam::123456789012:role/CrossCloudReader
      principalArn: arn:aws:iam::123456789012:assumed-role/Reader/*
    
    # Session policy
    sessionPolicy: |
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
              "s3:GetObject",
              "s3:ListBucket"
            ],
            "Resource": "*"
          }
        ]
      }

---
# Azure AD Enterprise Application
apiVersion: azure.microsoft.com/v1
kind: EnterpriseApplication
metadata:
  name: aws-sso-federation
spec:
  displayName: "AWS Single Sign-On"
  sso:
    protocol: SAML
    metadata:
      entityId: "https://signin.aws.amazon.com/saml"
      ssoUrl: "https://signin.aws.amazon.com/saml"
  claims:
    - name: "email"
      source: "user.mail"
    - name: "groups"
      source: "user.groups"
```

### Active Directory Integration

```python
import ldap3
from ldap3 import Server, Connection, SUBTREE

class ActiveDirectoryIntegration:
    """Active Directory integration for hybrid identity"""
    
    def __init__(self, server: str, base_dn: str):
        self.server = Server(server, get_info=ldap3.ALL)
        self.base_dn = base_dn
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user against AD"""
        
        try:
            conn = Connection(
                self.server,
                user=f"{username}@{self.base_dn}",
                password=password,
                auto_bind=True
            )
            
            return conn.bound
        
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def get_user_groups(self, username: str) -> list:
        """Get user's AD groups for authorization"""
        
        conn = Connection(self.server)
        conn.bind()
        
        search_filter = f"(sAMAccountName={username})"
        
        conn.search(
            search_base=self.base_dn,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['memberOf']
        )
        
        groups = []
        for entry in conn.entries:
            if hasattr(entry, 'memberOf'):
                groups.extend(entry.memberOf.values)
        
        return groups
    
    def sync_to_cloud_provider(self, users: list, provider: str):
        """Sync users to cloud identity provider"""
        
        if provider == 'aws':
            self._sync_to_iam(users)
        elif provider == 'azure':
            self._sync_to_azure_ad(users)
    
    def _sync_to_iam(self, users: list):
        """Sync users to AWS IAM"""
        pass
    
    def _sync_to_azure_ad(self, users: list):
        """Sync users to Azure AD"""
        pass
```

-----

## Data Synchronization

### Hybrid Data Sync

```python
import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable
import hashlib

@dataclass
class SyncRecord:
    """Data synchronization record"""
    id: str
    source_id: str
    destination: str
    data: dict
    timestamp: datetime
    checksum: str
    status: str  # pending, syncing, completed, failed


class HybridDataSynchronizer:
    """Synchronize data between on-prem and cloud"""
    
    def __init__(self):
        self.sync_queue = []
        self.sync_history = []
    
    def add_to_sync(self, data: Any, source: str, destination: str) -> str:
        """Add data to synchronization queue"""
        
        record = SyncRecord(
            id=self._generate_id(data),
            source_id=source,
            destination=destination,
            data=data,
            timestamp=datetime.now(),
            checksum=self._calculate_checksum(data),
            status='pending'
        )
        
        self.sync_queue.append(record)
        return record.id
    
    def process_sync_queue(self, batch_size: int = 100) -> dict:
        """Process synchronization queue"""
        
        batch = self.sync_queue[:batch_size]
        
        results = {
            'processed': 0,
            'succeeded': 0,
            'failed': 0,
            'details': []
        }
        
        for record in batch:
            try:
                # Sync to destination
                self._sync_record(record)
                
                record.status = 'completed'
                results['succeeded'] += 1
                
            except Exception as e:
                record.status = 'failed'
                results['failed'] += 1
                results['details'].append({
                    'record_id': record.id,
                    'error': str(e)
                })
            
            results['processed'] += 1
        
        # Update history
        self.sync_history.extend(batch)
        self.sync_queue = self.sync_queue[batch_size:]
        
        return results
    
    def resolve_conflicts(self, local_data: dict, 
                        cloud_data: dict, 
                        strategy: str = 'last_write_wins') -> dict:
        """Resolve data conflicts"""
        
        if strategy == 'last_write_wins':
            if local_data.get('updated_at', '') > cloud_data.get('updated_at', ''):
                return local_data
            return cloud_data
        
        elif strategy == 'local_wins':
            return local_data
        
        elif strategy == 'cloud_wins':
            return cloud_data
        
        elif strategy == 'merge':
            return self._merge_data(local_data, cloud_data)
        
        raise ValueError(f"Unknown conflict resolution strategy: {strategy}")
    
    def _merge_data(self, local: dict, cloud: dict) -> dict:
        """Merge conflicting data"""
        
        merged = {}
        
        all_keys = set(local.keys()) | set(cloud.keys())
        
        for key in all_keys:
            if key in local and key in cloud:
                # Both have this key
                if isinstance(local[key], dict) and isinstance(cloud[key], dict):
                    merged[key] = self._merge_data(local[key], cloud[key])
                else:
                    # Last write wins for non-dict values
                    merged[key] = local[key] if local.get(f'{key}_updated', '') > cloud.get(f'{key}_updated', '') else cloud[key]
            elif key in local:
                merged[key] = local[key]
            else:
                merged[key] = cloud[key]
        
        return merged
    
    def _generate_id(self, data: Any) -> str:
        """Generate unique ID for data"""
        content = str(data)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _calculate_checksum(self, data: Any) -> str:
        """Calculate checksum for data integrity"""
        content = str(data)
        return hashlib.md5(content.encode()).hexdigest()
    
    def _sync_record(self, record: SyncRecord):
        """Sync single record to destination"""
        # Implementation depends on destination
        pass
```

-----

## Disaster Recovery

### Multi-Cloud DR Architecture

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dr-config
data:
  dr-architecture.yaml: |
    # DR Tier Definitions
    tiers:
      rto_1h:
        name: "Mission Critical"
        rpo: 15m
        rto: 1h
        replication: "synchronous"
        active_active: true
    
      rto_4h:
        name: "Business Critical"
        rpo: 1h
        rto: 4h
        replication: "asynchronous"
        active_passive: true
    
      rto_24h:
        name: "Standard"
        rpo: 24h
        rto: 24h
        replication: "backup"
        recovery: "restore"
    
    # Replication Links
    replication:
      - source: "onprem"
        target: "aws"
        type: "async"
        bandwidth_mbps: 1000
      
      - source: "onprem"
        target: "azure"
        type: "async"
        bandwidth_mbps: 500
    
    # Failover Procedures
    failover_procedures:
      - name: "primary-to-aws"
        steps:
          - "Update DNS to point to AWS"
          - "Scale up AWS workloads"
          - "Verify application health"
          - "Enable write to AWS databases"
      
      - name: "aws-to-azure"
        steps:
          - "Promote Azure standby"
          - "Update global load balancer"
          - "Verify connectivity"
          - "Resume operations"
```

### DR Testing

```python
class DisasterRecoveryTester:
    """Test disaster recovery procedures"""
    
    def __init__(self):
        self.test_results = []
    
    def test_failover(self, source: str, target: str) -> dict:
        """Test failover from source to target"""
        
        results = {
            'source': source,
            'target': target,
            'start_time': datetime.now(),
            'steps': []
        }
        
        try:
            # Step 1: Verify initial state
            results['steps'].append(self._verify_initial_state(source))
            
            # Step 2: Trigger failover
            results['steps'].append(self._trigger_failover(target))
            
            # Step 3: Verify application health
            results['steps'].append(self._verify_health(target))
            
            # Step 4: Test data integrity
            results['steps'].append(self._verify_data_integrity(source, target))
            
            results['status'] = 'passed'
        
        except Exception as e:
            results['status'] = 'failed'
            results['error'] = str(e)
        
        results['end_time'] = datetime.now()
        results['duration'] = (results['end_time'] - results['start_time']).seconds
        
        self.test_results.append(results)
        return results
    
    def test_failback(self, source: str, target: str) -> dict:
        """Test failback to original site"""
        
        # Similar to failover but in reverse
        pass
    
    def generate_dr_report(self) -> dict:
        """Generate DR testing report"""
        
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'passed')
        failed = total_tests - passed
        
        return {
            'summary': {
                'total_tests': total_tests,
                'passed': passed,
                'failed': failed,
                'pass_rate': f"{(passed/total_tests)*100:.1f}%" if total_tests > 0 else "N/A"
            },
            'tests': self.test_results,
            'recommendations': self._generate_recommendations()
        }
    
    def _verify_initial_state(self, site: str) -> dict:
        """Verify initial site state"""
        return {'step': 'verify_initial_state', 'status': 'success'}
    
    def _trigger_failover(self, target: str) -> dict:
        """Trigger failover to target"""
        return {'step': 'trigger_failover', 'status': 'success'}
    
    def _verify_health(self, site: str) -> dict:
        """Verify application health"""
        return {'step': 'verify_health', 'status': 'success'}
    
    def _verify_data_integrity(self, source: str, target: str) -> dict:
        """Verify data integrity after failover"""
        return {'step': 'verify_data_integrity', 'status': 'success'}
    
    def _generate_recommendations(self) -> list:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if r['status'] == 'failed']
        
        if failed_tests:
            recommendations.append({
                'priority': 'high',
                'action': 'Review and fix failed DR tests',
                'details': [t.get('error') for t in failed_tests]
            })
        
        return recommendations
```
