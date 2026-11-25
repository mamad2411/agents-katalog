---
name: scaleway-deploy-check
description: Verify Scaleway production deployment health by checking instances, containers, kubernetes clusters, load balancers, databases (RDB/Redis), networking (VPC), and monitoring (Cockpit) using Scaleway CLI commands when user asks to check deployment status or verify production environment
allowed-tools: Bash, Read
---

# Scaleway Deployment Verification Skill

## Objective
Comprehensively verify the health and operational status of Scaleway infrastructure deployments by systematically checking all critical resources and services.

## When to Use
Activate this skill when the user:
- Asks to check Scaleway deployment status
- Requests production environment verification
- Needs a health check or status report
- Troubleshoots deployment issues
- Mentions "Scaleway", "deployment", "production check", or "infrastructure status"

## Instructions

### 1. Verify Compute Instances
```bash
scw instance server list
```
- Check all instances are in "running" state
- Verify IP addresses are assigned
- Note availability zones
- Identify any stopped, error, or locked states

### 2. Check Kubernetes Clusters
```bash
scw k8s cluster list
scw k8s pool list cluster-id=<cluster-id>
scw k8s node list cluster-id=<cluster-id>
```
- Verify cluster status is "ready"
- Check node pool health
- Validate node count and status
- Review Kubernetes version

### 3. Verify Container Resources
```bash
scw container namespace list
scw container container list
```
- Check namespace status
- Verify container deployments are running
- Review container configurations
- Check registry accessibility

### 4. Check Load Balancers
```bash
scw lb lb list
scw lb backend list lb-id=<lb-id>
```
- Verify load balancer status
- Check backend health
- Review routing rules
- Validate SSL/TLS configuration

### 5. Verify Databases
```bash
scw rdb instance list
scw redis cluster list
```
- Check database instance status (ready/available)
- Verify connection endpoints
- Review backup status
- Check database versions

### 6. Check Networking
```bash
scw vpc private-network list
scw vpc gateway list
```
- Verify VPC configuration
- Check private network connectivity
- Validate gateway status
- Review security group rules

### 7. Verify Container Registry
```bash
scw registry namespace list
scw registry image list namespace-id=<namespace-id>
```
- Check registry accessibility
- Verify image availability
- Review namespace configuration

### 8. Check Monitoring (Cockpit)
```bash
scw cockpit get
```
- Verify monitoring endpoints
- Check metrics collection status
- Review alerting configuration

For detailed CLI command reference, see [reference.md](reference.md).

## Architecture Documentation

For detailed architecture information and deployment guides, see:

**Internal Architecture** (`.agents/` - gitignored for agentic workflows):
- **Load Balancer Setup**: `.agents/architecture/load-balancer-setup.md`
- **Deployment Workflows Status**: `.agents/architecture/DEPLOYMENT-WORKFLOWS-STATUS.md`
- **Golden Volume + JuiceFS**: `.agents/architecture/DEPLOYMENT-GOLDEN-JUICEFS.md`
- **Implementation Reports**: `.agents/reports/ansible-infrastructure-test-report.md`

**Deployment Resources**:
- **Terraform Configurations**: `deployment/scaleway/terraform/*.tf`
- **Ansible Playbooks**: `deployment/scaleway/ansible/playbooks/`
- **Deployment Scripts**:
  - `deployment/scaleway/scripts/deploy-golden-vm-prod.sh`
  - `deployment/scaleway/scripts/deploy-scaleway-infrastructure.sh`
- **Deployment Guides**:
  - `docs/deployment/MULTI-METHOD-DEPLOYMENT.md`
  - `docs/deployment/BRANCH-SPECIFIC-DEPLOYMENT.md`

**Configuration**:
- **Environment Configs**: `deployment/config/deployments/{dev,staging,production}.yaml`
- **Validation Scripts**: `deployment/config/validation/*.sh`

## Health Check Criteria

For each resource type, verify:
- **Status**: Must be "running", "ready", or "available" (not stopped/error/locked)
- **Configuration**: Matches expected deployment specifications
- **Connectivity**: Endpoints are accessible and properly configured
- **Security**: Appropriate security groups, firewall rules, and access controls
- **Performance**: No resource constraints or bottlenecks

## Expected Output

Provide a comprehensive report with:

1. **Executive Summary**
   - Overall deployment health score (healthy/degraded/critical)
   - Total resources checked
   - Issues count by severity

2. **Resource Status by Category**
   - Instances: count, running/stopped, IP assignments
   - Kubernetes: cluster status, node health, pod counts
   - Containers: namespace status, container states
   - Load Balancers: status, backend health
   - Databases: instance status, connectivity
   - Networking: VPC config, gateway status
   - Registry: accessibility, image availability

3. **Issues and Warnings**
   - Critical: Resources in error state, failed health checks
   - Warning: Degraded performance, approaching limits
   - Info: Configuration recommendations

4. **Recommendations**
   - Immediate actions for critical issues
   - Optimization suggestions
   - Security improvements

## Troubleshooting

If issues are detected:
- Use `scw <resource> <type> get <id>` for detailed resource information
- Check logs: `scw instance server logs <id>` for instances
- Review events: `scw k8s cluster get <id>` shows cluster events
- Verify quotas: `scw account project list` to check limits
- Check recent changes: review deployment history

## Error Handling

If commands fail:
- Verify scw CLI is authenticated (session already initialized)
- Check API permissions and project access
- Validate resource IDs are correct
- Report authentication or permission errors to user
