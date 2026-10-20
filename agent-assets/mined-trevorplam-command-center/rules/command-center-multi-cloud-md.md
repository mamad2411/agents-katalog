---
description: Run Multi-Cloud and Cross-Cloud Deployment Standards Check
globs:
  [
    '**/multi-cloud/**/*.ts',
    '**/cross-cloud/**/*.ts',
    '**/vendor-agnostic/**/*.ts',
    'terraform/**/*.tf',
  ]
---

# Infrastructure: Multi-Cloud & Cross-Cloud Deployment Standards

<audit_rules>

- You MUST implement proper cloud-agnostic architecture to avoid vendor lock-in.
- You MUST configure proper multi-cloud networking and connectivity between cloud providers.
- You MUST ensure proper data synchronization and consistency across multiple clouds.
- You MUST implement proper cost management and optimization across all cloud providers.
- You MUST configure proper disaster recovery and failover strategies across clouds.
- You MUST ensure proper security and compliance controls are consistent across all clouds.
- You MUST implement proper monitoring and observability across multi-cloud environments.
- You MUST configure proper identity and access management across multiple cloud providers.
- You MUST ensure proper workload placement and orchestration across clouds.
- You MUST implement proper governance and policy enforcement across all cloud environments.
  </audit_rules>

<example_good>

```typescript
// Multi-Cloud Architecture Implementation

export class MultiCloudOrchestrator {
  constructor(
    private cloudProviders: Map<string, CloudProvider>,
    private workloadPlacer: WorkloadPlacer,
    private costOptimizer: MultiCloudCostOptimizer,
    private disasterRecovery: DisasterRecoveryManager,
    private governanceEngine: MultiCloudGovernance
  ) {}

  async deployWorkload(
    workload: Workload,
    strategy: DeploymentStrategy
  ): Promise<DeploymentResult> {
    // Validate workload against multi-cloud policies
    await this.governanceEngine.validateWorkload(workload)

    // Determine optimal cloud placement
    const placement = await this.workloadPlacer.optimizePlacement(workload, strategy)

    // Deploy across multiple clouds
    const deployments = []

    for (const target of placement.targets) {
      const cloudProvider = this.cloudProviders.get(target.cloud)
      if (!cloudProvider) {
        throw new Error(`Cloud provider not found: ${target.cloud}`)
      }

      const deployment = await this.deployToCloud(cloudProvider, workload, target)
      deployments.push(deployment)
    }

    // Setup cross-cloud networking
    await this.setupCrossCloudNetworking(deployments)

    // Configure multi-cloud monitoring
    await this.setupMultiCloudMonitoring(deployments)

    // Setup disaster recovery
    await this.disasterRecovery.configure(workload, deployments)

    return {
      workloadId: workload.id,
      deployments,
      placement,
      costEstimate: await this.costOptimizer.estimateCost(workload, placement),
    }
  }

  async deployToCloud(
    cloudProvider: CloudProvider,
    workload: Workload,
    target: DeploymentTarget
  ): Promise<CloudDeployment> {
    // Cloud-agnostic deployment
    const resources = await this.generateCloudResources(workload, target)

    // Apply cloud-specific optimizations
    const optimizedResources = await cloudProvider.optimizeResources(resources)

    // Deploy resources
    const deployment = await cloudProvider.deploy(optimizedResources)

    // Configure cloud-specific monitoring
    await cloudProvider.setupMonitoring(deployment)

    return deployment
  }

  async setupCrossCloudNetworking(deployments: CloudDeployment[]): Promise<void> {
    // Create VPN connections between clouds
    const connections = []

    for (let i = 0; i < deployments.length; i++) {
      for (let j = i + 1; j < deployments.length; j++) {
        const connection = await this.createVPNConnection(deployments[i], deployments[j])
        connections.push(connection)
      }
    }

    // Configure global load balancing
    await this.setupGlobalLoadBalancer(deployments)

    // Configure DNS failover
    await this.setupDNSFailover(deployments)
  }

  async handleCloudFailure(failedCloud: string, workloadId: string): Promise<FailoverResult> {
    // Detect cloud failure
    const failure = await this.detectCloudFailure(failedCloud)

    if (!failure.isFailed) {
      throw new Error(`Cloud ${failedCloud} is not failed`)
    }

    // Get workload deployments
    const deployments = await this.getWorkloadDeployments(workloadId)

    // Filter out failed cloud deployments
    const healthyDeployments = deployments.filter((d) => d.cloud !== failedCloud)

    if (healthyDeployments.length === 0) {
      throw new Error('No healthy deployments available for failover')
    }

    // Update DNS to point to healthy clouds
    await this.updateDNSFailover(workloadId, healthyDeployments)

    // Scale up healthy deployments if needed
    await this.scaleUpDeployments(healthyDeployments, deployments)

    // Notify stakeholders
    await this.notifyCloudFailure(failedCloud, workloadId)

    return {
      failedCloud,
      failoverClouds: healthyDeployments.map((d) => d.cloud),
      downtime: Date.now() - failure.startTime,
      impact: await this.calculateImpact(failedCloud, workloadId),
    }
  }

  async optimizeMultiCloudCosts(): Promise<CostOptimizationResult> {
    // Get current costs across all clouds
    const currentCosts = await this.getCurrentCosts()

    // Analyze cost optimization opportunities
    const opportunities = await this.costOptimizer.findOptimizationOpportunities(currentCosts)

    // Implement optimizations
    const results = []

    for (const opportunity of opportunities) {
      try {
        const result = await this.implementCostOptimization(opportunity)
        results.push(result)
      } catch (error) {
        console.error(`Failed to implement optimization: ${error.message}`)
      }
    }

    // Calculate total savings
    const totalSavings = results.reduce((sum, result) => sum + result.savings, 0)

    return {
      optimizations: results,
      totalSavings,
      nextReviewDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
    }
  }

  async enforceMultiCloudCompliance(): Promise<ComplianceReport> {
    const deployments = await this.getAllDeployments()
    const violations = []

    for (const deployment of deployments) {
      const compliance = await this.governanceEngine.checkCompliance(deployment)

      if (!compliance.compliant) {
        violations.push({
          deploymentId: deployment.id,
          cloud: deployment.cloud,
          violations: compliance.violations,
        })
      }
    }

    return {
      totalDeployments: deployments.length,
      compliantDeployments: deployments.length - violations.length,
      violations,
      complianceScore: this.calculateComplianceScore(deployments, violations),
    }
  }

  private async generateCloudResources(
    workload: Workload,
    target: DeploymentTarget
  ): Promise<CloudResources> {
    // Generate cloud-agnostic resource definitions
    return {
      compute: {
        instances: workload.resources.compute.map((c) => ({
          type: target.computeInstanceTypes[c.type] || c.type,
          count: c.count,
          configuration: c.configuration,
        })),
      },
      storage: {
        volumes: workload.resources.storage.map((s) => ({
          type: target.storageTypes[s.type] || s.type,
          size: s.size,
          performance: s.performance,
        })),
      },
      networking: {
        vpc: {
          cidr: target.networkCidr,
          subnets: target.subnets,
        },
        loadBalancer: {
          type: 'application',
          configuration: workload.networking.loadBalancer,
        },
      },
      security: {
        securityGroups: workload.security.securityGroups,
        iamRoles: workload.security.iamRoles,
      },
    }
  }

  private async createVPNConnection(
    deploymentA: CloudDeployment,
    deploymentB: CloudDeployment
  ): Promise<VPNConnection> {
    const providerA = this.cloudProviders.get(deploymentA.cloud)
    const providerB = this.cloudProviders.get(deploymentB.cloud)

    // Create VPN gateway in both clouds
    const gatewayA = await providerA.createVPNGateway(deploymentA.vpcId)
    const gatewayB = await providerB.createVPNGateway(deploymentB.vpcId)

    // Create VPN connection
    const connection = await providerA.createVPNConnection({
      gatewayId: gatewayA.id,
      remoteGatewayId: gatewayB.id,
      remoteVpcCidr: deploymentB.vpcCidr,
    })

    return {
      id: connection.id,
      cloudA: deploymentA.cloud,
      cloudB: deploymentB.cloud,
      gatewayA: gatewayA.id,
      gatewayB: gatewayB.id,
    }
  }

  private async setupGlobalLoadBalancer(deployments: CloudDeployment[]): Promise<void> {
    // Configure global load balancer across all clouds
    const loadBalancerConfig = {
      name: 'global-lb',
      backends: deployments.map((d) => ({
        cloud: d.cloud,
        endpoint: d.loadBalancerEndpoint,
        weight: d.capacity,
        healthCheck: d.healthCheckEndpoint,
      })),
      routingPolicy: 'weighted-round-robin',
      healthCheck: {
        path: '/health',
        interval: 30,
        timeout: 5,
        healthyThreshold: 2,
        unhealthyThreshold: 3,
      },
    }

    await this.globalLoadBalancer.configure(loadBalancerConfig)
  }

  private async setupDNSFailover(deployments: CloudDeployment[]): Promise<void> {
    // Configure DNS with failover to multiple clouds
    const dnsConfig = {
      domain: 'example.com',
      records: deployments.map((d) => ({
        name: 'api',
        type: 'A',
        value: d.publicIP,
        ttl: 60,
        healthCheck: d.healthCheckEndpoint,
        priority: d.priority,
      })),
      failoverPolicy: 'round-robin',
    }

    await this.dnsProvider.configure(dnsConfig)
  }

  private async detectCloudFailure(cloud: string): Promise<CloudFailure> {
    const provider = this.cloudProviders.get(cloud)
    const healthChecks = await provider.getHealthChecks()

    const failedChecks = healthChecks.filter((check) => !check.healthy)

    if (failedChecks.length > healthChecks.length * 0.5) {
      return {
        isFailed: true,
        startTime: failedChecks[0].failureTime,
        affectedServices: failedChecks.map((c) => c.service),
      }
    }

    return { isFailed: false }
  }

  private calculateComplianceScore(
    deployments: CloudDeployment[],
    violations: ComplianceViolation[]
  ): number {
    const totalChecks = deployments.length * 10 // Assume 10 checks per deployment
    const failedChecks = violations.reduce((sum, v) => sum + v.violations.length, 0)
    return Math.max(0, 100 - (failedChecks / totalChecks) * 100)
  }
}

// Cloud Provider Interface
export interface CloudProvider {
  deploy(resources: CloudResources): Promise<CloudDeployment>
  optimizeResources(resources: CloudResources): Promise<CloudResources>
  setupMonitoring(deployment: CloudDeployment): Promise<void>
  createVPNGateway(vpcId: string): Promise<VPNGateway>
  createVPNConnection(config: VPNConfig): Promise<VPNConnection>
  getHealthChecks(): Promise<HealthCheck[]>
  getCosts(): Promise<CloudCosts>
}

// AWS Provider Implementation
export class AWSProvider implements CloudProvider {
  constructor(
    private ec2: EC2,
    private rds: RDS,
    private elb: ELB
  ) {}

  async deploy(resources: CloudResources): Promise<CloudDeployment> {
    // Deploy to AWS using CloudFormation or Terraform
    const deployment = await this.deployWithCloudFormation(resources)

    return {
      cloud: 'aws',
      id: deployment.stackId,
      vpcId: deployment.vpcId,
      publicIP: deployment.publicIP,
      loadBalancerEndpoint: deployment.loadBalancerDNS,
      healthCheckEndpoint: deployment.healthCheckURL,
      capacity: this.calculateCapacity(resources),
      priority: 1,
    }
  }

  async optimizeResources(resources: CloudResources): Promise<CloudResources> {
    // AWS-specific optimizations
    return {
      ...resources,
      compute: {
        instances: resources.compute.instances.map((instance) => ({
          ...instance,
          type: this.optimizeInstanceType(instance.type),
        })),
      },
      storage: {
        volumes: resources.storage.volumes.map((volume) => ({
          ...volume,
          type: this.optimizeStorageType(volume.type),
        })),
      },
    }
  }

  private optimizeInstanceType(type: string): string {
    // AWS instance type optimization
    const optimizations: Record<string, string> = {
      't3.medium': 't3a.medium',
      'm5.large': 'm6a.large',
      'c5.xlarge': 'c6a.xlarge',
    }

    return optimizations[type] || type
  }

  private optimizeStorageType(type: string): string {
    // AWS storage type optimization
    const optimizations: Record<string, string> = {
      gp2: 'gp3',
      standard: 'gp3',
    }

    return optimizations[type] || type
  }
}

// Azure Provider Implementation
export class AzureProvider implements CloudProvider {
  constructor(
    private compute: ComputeManagementClient,
    private network: NetworkManagementClient
  ) {}

  async deploy(resources: CloudResources): Promise<CloudDeployment> {
    // Deploy to Azure using ARM templates
    const deployment = await this.deployWithARMTemplate(resources)

    return {
      cloud: 'azure',
      id: deployment.deploymentId,
      vpcId: deployment.vnetId,
      publicIP: deployment.publicIP,
      loadBalancerEndpoint: deployment.loadBalancerFQDN,
      healthCheckEndpoint: deployment.healthCheckURL,
      capacity: this.calculateCapacity(resources),
      priority: 2,
    }
  }

  async optimizeResources(resources: CloudResources): Promise<CloudResources> {
    // Azure-specific optimizations
    return {
      ...resources,
      compute: {
        instances: resources.compute.instances.map((instance) => ({
          ...instance,
          type: this.optimizeVMSize(instance.type),
        })),
      },
    }
  }

  private optimizeVMSize(size: string): string {
    // Azure VM size optimization
    const optimizations: Record<string, string> = {
      Standard_B2s: 'Standard_B2ms',
      Standard_D2s_v3: 'Standard_D2as_v5',
      Standard_F4s_v2: 'Standard_F4s_v2',
    }

    return optimizations[size] || size
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: Single-cloud, vendor-locked implementation
export class SingleCloudApp {
  // BAD: Hardcoded to single cloud provider
  async deployApp(app: any) {
    // BAD: No multi-cloud strategy
    // BAD: No vendor lock-in prevention
    // BAD: No cross-cloud networking
    // BAD: No multi-cloud cost optimization
    return await this.awsDeploy(app)
  }

  // BAD: No disaster recovery across clouds
  // BAD: No multi-cloud compliance
  // BAD: No cloud-agnostic architecture
  // BAD: No workload placement optimization
}
```

</example_bad>
