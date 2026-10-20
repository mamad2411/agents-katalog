# Skill: Ansible Playbook Generation

## Purpose

Generate production-ready Ansible playbooks for network infrastructure automation across Azure, AWS, and GCP. Provides idempotent, role-based playbook patterns for provisioning, configuring, and managing networking resources.

---

## Core Conventions

### Collection Requirements

```yaml
# requirements.yml
collections:
  - name: azure.azcollection
    version: ">=2.4.0"
  - name: amazon.aws
    version: ">=7.0.0"
  - name: google.cloud
    version: ">=1.3.0"
  - name: ansible.netcommon
    version: ">=6.0.0"
  - name: community.general
    version: ">=8.0.0"
```

Install: `ansible-galaxy collection install -r requirements.yml`

### Directory Structure

```
ansible/
├── inventory/
│   ├── dev/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       └── all.yml
│   ├── staging/
│   └── prod/
├── roles/
│   ├── azure_vnet/
│   ├── azure_firewall/
│   ├── azure_vpn_gateway/
│   ├── aws_vpc/
│   ├── aws_transit_gateway/
│   └── gcp_vpc/
├── playbooks/
│   ├── deploy-hub-spoke.yml
│   ├── deploy-firewall.yml
│   └── deploy-vpn.yml
├── group_vars/
│   └── all.yml
├── requirements.yml
└── ansible.cfg
```

### Variable Naming

```yaml
# Prefix variables with cloud and resource type
azure_vnet_hub_name: "contoso-vnet-hub-prod-eus2"
azure_vnet_hub_address_space: "10.0.0.0/16"
azure_firewall_sku: "Standard"
aws_vpc_cidr: "10.10.0.0/16"
gcp_vpc_name: "contoso-vpc-prod"
```

---

## Azure Networking Playbooks

### 1. Hub-Spoke VNet Deployment

```yaml
---
- name: Deploy Azure Hub-Spoke Network
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    resource_group: "rg-network-{{ environment }}-{{ region_code }}"
    location: "{{ azure_region }}"
    tags:
      Environment: "{{ environment }}"
      ManagedBy: "Ansible"
      Project: "NetworkInfra"

  tasks:
    - name: Create resource group
      azure.azcollection.azure_rm_resourcegroup:
        name: "{{ resource_group }}"
        location: "{{ location }}"
        tags: "{{ tags }}"

    - name: Create Hub VNet
      azure.azcollection.azure_rm_virtualnetwork:
        resource_group: "{{ resource_group }}"
        name: "{{ prefix }}-vnet-hub-{{ environment }}-{{ region_code }}"
        address_prefixes_cidr:
          - "{{ hub_address_space }}"
        tags: "{{ tags }}"

    - name: Create Hub Subnets
      azure.azcollection.azure_rm_subnet:
        resource_group: "{{ resource_group }}"
        virtual_network_name: "{{ prefix }}-vnet-hub-{{ environment }}-{{ region_code }}"
        name: "{{ item.name }}"
        address_prefix_cidr: "{{ item.prefix }}"
      loop: "{{ hub_subnets }}"
      loop_control:
        label: "{{ item.name }}"

    - name: Create Spoke VNets
      azure.azcollection.azure_rm_virtualnetwork:
        resource_group: "{{ resource_group }}"
        name: "{{ prefix }}-vnet-{{ item.name }}-{{ environment }}-{{ region_code }}"
        address_prefixes_cidr:
          - "{{ item.address_space }}"
        tags: "{{ tags }}"
      loop: "{{ spokes }}"
      loop_control:
        label: "{{ item.name }}"

    - name: Create VNet Peering (Spoke → Hub)
      azure.azcollection.azure_rm_virtualnetworkpeering:
        resource_group: "{{ resource_group }}"
        virtual_network: "{{ prefix }}-vnet-{{ item.name }}-{{ environment }}-{{ region_code }}"
        name: "peer-to-hub"
        remote_virtual_network:
          resource_group: "{{ resource_group }}"
          name: "{{ prefix }}-vnet-hub-{{ environment }}-{{ region_code }}"
        allow_forwarded_traffic: true
        use_remote_gateways: "{{ deploy_vpn_gateway | default(false) }}"
      loop: "{{ spokes }}"
      loop_control:
        label: "{{ item.name }}"

    - name: Create VNet Peering (Hub → Spoke)
      azure.azcollection.azure_rm_virtualnetworkpeering:
        resource_group: "{{ resource_group }}"
        virtual_network: "{{ prefix }}-vnet-hub-{{ environment }}-{{ region_code }}"
        name: "peer-to-{{ item.name }}"
        remote_virtual_network:
          resource_group: "{{ resource_group }}"
          name: "{{ prefix }}-vnet-{{ item.name }}-{{ environment }}-{{ region_code }}"
        allow_gateway_transit: "{{ deploy_vpn_gateway | default(false) }}"
      loop: "{{ spokes }}"
      loop_control:
        label: "{{ item.name }}"
```

### 2. Azure Firewall Deployment

```yaml
---
- name: Deploy Azure Firewall
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    fw_name: "{{ prefix }}-fw-{{ environment }}-{{ region_code }}"
    fw_policy_name: "{{ prefix }}-fwpol-{{ environment }}-{{ region_code }}"
    fw_pip_name: "{{ prefix }}-pip-fw-{{ environment }}-{{ region_code }}"

  tasks:
    - name: Create Firewall Public IP
      azure.azcollection.azure_rm_publicipaddress:
        resource_group: "{{ resource_group }}"
        name: "{{ fw_pip_name }}"
        allocation_method: "Static"
        sku: "Standard"
        tags: "{{ tags }}"
      register: fw_pip

    - name: Create Firewall Policy
      azure.azcollection.azure_rm_firewallpolicy:
        resource_group: "{{ resource_group }}"
        name: "{{ fw_policy_name }}"
        sku: "{{ azure_firewall_sku }}"
        threat_intel_mode: "Alert"
        dns:
          proxy_enabled: true
        tags: "{{ tags }}"
      register: fw_policy

    - name: Deploy Azure Firewall
      azure.azcollection.azure_rm_azurefirewall:
        resource_group: "{{ resource_group }}"
        name: "{{ fw_name }}"
        sku:
          name: "AZFW_VNet"
          tier: "{{ azure_firewall_sku }}"
        firewall_policy:
          id: "{{ fw_policy.id }}"
        ip_configurations:
          - name: "fw-ipconfig"
            subnet:
              id: "{{ azure_firewall_subnet_id }}"
            public_ip_address:
              id: "{{ fw_pip.state.id }}"
        tags: "{{ tags }}"
      register: firewall

    - name: Output Firewall Private IP
      ansible.builtin.debug:
        msg: "Firewall private IP: {{ firewall.ip_configurations[0].private_ip_address }}"
```

### 3. NSG Deployment with Rules

```yaml
---
- name: Deploy Network Security Groups
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create NSGs
      azure.azcollection.azure_rm_securitygroup:
        resource_group: "{{ resource_group }}"
        name: "{{ prefix }}-nsg-{{ item.purpose }}-{{ environment }}-{{ region_code }}"
        rules: "{{ item.rules }}"
        tags: "{{ tags }}"
      loop: "{{ nsgs }}"
      loop_control:
        label: "{{ item.purpose }}"
```

---

## AWS Networking Playbooks

### 1. VPC with Subnets

```yaml
---
- name: Deploy AWS VPC
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create VPC
      amazon.aws.ec2_vpc_net:
        name: "{{ prefix }}-vpc-{{ environment }}"
        cidr_block: "{{ vpc_cidr }}"
        region: "{{ aws_region }}"
        dns_support: true
        dns_hostnames: true
        tags: "{{ common_tags }}"
        state: present
      register: vpc

    - name: Create Private Subnets
      amazon.aws.ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: "{{ item.cidr }}"
        az: "{{ item.az }}"
        region: "{{ aws_region }}"
        tags: "{{ common_tags | combine({'Name': prefix + '-' + item.name}) }}"
        state: present
      loop: "{{ private_subnets }}"
      register: private_subnet_results

    - name: Create Internet Gateway
      amazon.aws.ec2_vpc_igw:
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        tags: "{{ common_tags | combine({'Name': prefix + '-igw'}) }}"
        state: present
      register: igw

    - name: Create NAT Gateway
      amazon.aws.ec2_vpc_nat_gateway:
        subnet_id: "{{ public_subnet_results.results[0].subnet.id }}"
        region: "{{ aws_region }}"
        if_exist_do_not_create: true
        tags: "{{ common_tags | combine({'Name': prefix + '-natgw'}) }}"
        state: present
      register: nat_gw

    - name: Create Route Table (Private)
      amazon.aws.ec2_vpc_route_table:
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        subnets: "{{ private_subnet_results.results | map(attribute='subnet.id') | list }}"
        routes:
          - dest: "0.0.0.0/0"
            gateway_id: "{{ nat_gw.nat_gateway_id }}"
        tags: "{{ common_tags | combine({'Name': prefix + '-rt-private'}) }}"
        state: present
```

### 2. Security Groups

```yaml
    - name: Create Security Group
      amazon.aws.ec2_security_group:
        name: "{{ prefix }}-sg-{{ item.purpose }}"
        description: "{{ item.description }}"
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        rules: "{{ item.inbound_rules }}"
        rules_egress: "{{ item.outbound_rules | default(default_egress) }}"
        tags: "{{ common_tags }}"
        state: present
      loop: "{{ security_groups }}"
```

---

## GCP Networking Playbooks

### 1. VPC with Subnets

```yaml
---
- name: Deploy GCP VPC Network
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create VPC
      google.cloud.gcp_compute_network:
        name: "{{ prefix }}-vpc"
        auto_create_subnetworks: false
        routing_config:
          routing_mode: "GLOBAL"
        project: "{{ gcp_project }}"
        state: present
      register: vpc

    - name: Create Subnets
      google.cloud.gcp_compute_subnetwork:
        name: "{{ prefix }}-subnet-{{ item.name }}"
        ip_cidr_range: "{{ item.cidr }}"
        region: "{{ item.region }}"
        network: "{{ vpc }}"
        private_ip_google_access: true
        project: "{{ gcp_project }}"
        state: present
      loop: "{{ subnets }}"

    - name: Create Cloud Router
      google.cloud.gcp_compute_router:
        name: "{{ prefix }}-router"
        network: "{{ vpc }}"
        region: "{{ gcp_primary_region }}"
        bgp:
          asn: "{{ bgp_asn }}"
        project: "{{ gcp_project }}"
        state: present
```

---

## Inventory Variables Example

```yaml
# inventory/prod/group_vars/all.yml
---
prefix: "contoso"
environment: "prod"
region_code: "eus2"
azure_region: "eastus2"
aws_region: "us-east-1"
gcp_project: "contoso-network-prod"
gcp_primary_region: "us-east1"

hub_address_space: "10.0.0.0/16"
hub_subnets:
  - name: AzureFirewallSubnet
    prefix: "10.0.1.0/26"
  - name: GatewaySubnet
    prefix: "10.0.255.0/27"
  - name: AzureBastionSubnet
    prefix: "10.0.2.0/26"
  - name: snet-shared
    prefix: "10.0.10.0/24"

spokes:
  - name: workload-a
    address_space: "10.1.0.0/16"
  - name: workload-b
    address_space: "10.2.0.0/16"

azure_firewall_sku: "Standard"
deploy_vpn_gateway: true

common_tags:
  Environment: prod
  ManagedBy: Ansible
  Project: NetworkInfra
```

---

## Ansible Role Structure

```yaml
# roles/azure_vnet/tasks/main.yml
---
- name: Create Virtual Network
  azure.azcollection.azure_rm_virtualnetwork:
    resource_group: "{{ azure_vnet_resource_group }}"
    name: "{{ azure_vnet_name }}"
    address_prefixes_cidr: "{{ azure_vnet_address_prefixes }}"
    tags: "{{ azure_vnet_tags | default(omit) }}"

- name: Create Subnets
  azure.azcollection.azure_rm_subnet:
    resource_group: "{{ azure_vnet_resource_group }}"
    virtual_network_name: "{{ azure_vnet_name }}"
    name: "{{ item.name }}"
    address_prefix_cidr: "{{ item.prefix }}"
    security_group: "{{ item.nsg | default(omit) }}"
    route_table: "{{ item.route_table | default(omit) }}"
  loop: "{{ azure_vnet_subnets }}"
```

---

## Validation Commands

```bash
# Check syntax
ansible-playbook --syntax-check playbooks/deploy-hub-spoke.yml

# Dry-run (check mode)
ansible-playbook --check playbooks/deploy-hub-spoke.yml -i inventory/prod/

# Run with verbose output
ansible-playbook playbooks/deploy-hub-spoke.yml -i inventory/prod/ -v

# Run specific tags only
ansible-playbook playbooks/deploy-hub-spoke.yml -i inventory/prod/ --tags "vnet,peering"

# Limit to specific hosts/groups
ansible-playbook playbooks/deploy-hub-spoke.yml -i inventory/prod/ --limit "azure"
```

**Analysis only — verify against vendor documentation before applying.**
