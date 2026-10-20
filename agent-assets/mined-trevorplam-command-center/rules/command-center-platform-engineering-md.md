---
description: Run Platform Engineering and Internal Developer Platform Standards Check
globs:
  [
    '**/platform/**/*.ts',
    '**/paaS/**/*.ts',
    '**/developer-portal/**/*.ts',
    '**/internal-tools/**/*.ts',
  ]
---

# Platform Engineering: Internal Developer Platform Standards

<audit_rules>

- You MUST implement proper platform as a product mindset with user experience focus for developers.
- You MUST configure proper self-service capabilities for common developer workflows.
- You MUST implement proper golden paths for common deployment patterns and architectures.
- You MUST ensure proper abstraction of infrastructure complexity from developers.
- You MUST configure proper observability and monitoring for platform services.
- You MUST implement proper governance and compliance controls at platform level.
- You MUST ensure proper documentation and onboarding for platform capabilities.
- You MUST configure proper feedback loops and continuous improvement mechanisms.
- You MUST implement proper security boundaries and access controls for platform services.
- You MUST ensure proper cost management and resource optimization at platform level.
  </audit_rules>

<example_good>

```typescript
// Internal Developer Platform Implementation

export class InternalDeveloperPlatform {
  constructor(
    private selfServicePortal: SelfServicePortal,
    private goldenPathEngine: GoldenPathEngine,
    private observabilityPlatform: ObservabilityPlatform,
    private governanceEngine: GovernanceEngine,
    private costOptimizer: CostOptimizer
  ) {}

  // Self-Service Capabilities
  async provisionService(request: ServiceRequest): Promise<ServiceProvision> {
    // Validate request against governance policies
    await this.governanceEngine.validateRequest(request);

    // Check cost implications
    const costEstimate = await this.costOptimizer.estimateCost(request);
    if (costEstimate.monthlyCost > request.budgetLimit) {
      throw new Error('Cost estimate exceeds budget limit');
    }

    // Provision using golden path
    const provision = await this.goldenPathEngine.provision({
      serviceType: request.serviceType,
      specifications: request.specifications,
      environment: request.environment,
    });

    // Setup observability
    await this.observabilityPlatform.setupMonitoring({
      serviceId: provision.serviceId,
      serviceType: request.serviceType,
      owner: request.requester,
    });

    // Create documentation and onboarding
    await this.createDocumentation(provision);

    return provision;
  }

  // Golden Path for Microservices
  async createMicroservice(request: MicroserviceRequest): Promise<Microservice> {
    const goldenPath = await this.goldenPathEngine.getGoldenPath('microservice');

    // Apply golden path template
    const template = await goldenPath.getTemplate({
      language: request.language,
      framework: request.framework,
      database: request.database,
    });

    // Generate service structure
    const service = await template.generate({
      name: request.name,
      description: request.description,
      team: request.team,
    });

    // Setup CI/CD pipeline
    const pipeline = await this.setupCICD(service, {
      environment: request.environment,
      deploymentStrategy: request.deploymentStrategy,
    });

    // Configure service mesh
    await this.configureServiceMesh(service, {
      trafficManagement: request.trafficManagement,
      security: request.security,
      observability: request.observability,
    });

    return {
      service,
      pipeline,
      documentation: service.documentation,
      monitoring: service.monitoring,
    };
  }

  // Golden Path for Serverless Functions
  async createServerlessFunction(request: ServerlessRequest): Promise<ServerlessFunction> {
    const goldenPath = await this.goldenPathEngine.getGoldenPath('serverless');

    const template = await goldenPath.getTemplate({
      runtime: request.runtime,
      triggerType: request.triggerType,
      permissions: request.permissions,
    });

    const function = await template.generate({
      name: request.name,
      handler: request.handler,
      environment: request.environment,
    });

    // Setup event sources
    await this.setupEventSources(function, request.eventSources);

    // Configure monitoring and logging
    await this.observabilityPlatform.setupFunctionMonitoring(function);

    return function;
  }

  // Developer Experience Portal
  async getDeveloperDashboard(developerId: string): Promise<DeveloperDashboard> {
    const services = await this.getDeveloperServices(developerId);
    const costs = await this.costOptimizer.getDeveloperCosts(developerId);
    const metrics = await this.observabilityPlatform.getDeveloperMetrics(developerId);
    const compliance = await this.governanceEngine.getDeveloperCompliance(developerId);

    return {
      services,
      costs,
      metrics,
      compliance,
      recommendations: await this.generateRecommendations(developerId),
    };
  }

  // Platform Observability
  async getPlatformHealth(): Promise<PlatformHealth> {
    const services = await this.observabilityPlatform.getPlatformServices();
    const resources = await this.observabilityPlatform.getResourceUtilization();
    const costs = await this.costOptimizer.getPlatformCosts();
    const incidents = await this.observabilityPlatform.getActiveIncidents();

    return {
      services,
      resources,
      costs,
      incidents,
      recommendations: await this.generatePlatformRecommendations(),
    };
  }

  // Governance and Compliance
  async enforceCompliance(service: Service): Promise<ComplianceReport> {
    const policies = await this.governanceEngine.getApplicablePolicies(service);
    const violations = [];

    for (const policy of policies) {
      const result = await policy.evaluate(service);
      if (!result.compliant) {
        violations.push({
          policy: policy.name,
          severity: result.severity,
          description: result.description,
          remediation: result.remediation,
        });
      }
    }

    return {
      compliant: violations.length === 0,
      violations,
      score: this.calculateComplianceScore(policies, violations),
    };
  }

  // Cost Management
  async optimizeCosts(teamId: string): Promise<CostOptimization> {
    const currentCosts = await this.costOptimizer.getTeamCosts(teamId);
    const recommendations = await this.costOptimizer.generateRecommendations(teamId);
    const savings = await this.costOptimizer.calculatePotentialSavings(recommendations);

    return {
      currentCosts,
      recommendations,
      potentialSavings: savings,
      implementationPlan: await this.createImplementationPlan(recommendations),
    };
  }

  private async setupCICD(service: Service, config: CICDConfig): Promise<CICDPipeline> {
    return {
      name: `${service.name}-pipeline`,
      stages: [
        {
          name: 'build',
          steps: ['lint', 'test', 'security-scan', 'build'],
        },
        {
          name: 'deploy',
          steps: ['deploy-staging', 'integration-test', 'deploy-production'],
        },
      ],
      triggers: ['push', 'pull-request'],
      approvals: ['security-team', 'platform-team'],
    };
  }

  private async configureServiceMesh(service: Service, config: ServiceMeshConfig): Promise<void> {
    // Configure traffic management, security, and observability
    await this.serviceMesh.configureService(service.id, config);
  }

  private async createDocumentation(service: Service): Promise<void> {
    await this.documentationGenerator.generate({
      serviceId: service.id,
      type: 'service',
      sections: ['overview', 'api', 'deployment', 'monitoring', 'troubleshooting'],
    });
  }

  private async generateRecommendations(developerId: string): Promise<Recommendation[]> {
    const recommendations = [];

    // Cost recommendations
    const costRecommendations = await this.costOptimizer.getRecommendations(developerId);
    recommendations.push(...costRecommendations);

    // Security recommendations
    const securityRecommendations = await this.governanceEngine.getSecurityRecommendations(developerId);
    recommendations.push(...securityRecommendations);

    // Performance recommendations
    const performanceRecommendations = await this.observabilityPlatform.getPerformanceRecommendations(developerId);
    recommendations.push(...performanceRecommendations);

    return recommendations;
  }

  private calculateComplianceScore(policies: Policy[], violations: PolicyViolation[]): number {
    const totalWeight = policies.reduce((sum, policy) => sum + policy.weight, 0);
    const violationWeight = violations.reduce((sum, violation) => sum + violation.weight, 0);
    return Math.max(0, 100 - (violationWeight / totalWeight) * 100);
  }
}

// Golden Path Engine
export class GoldenPathEngine {
  private goldenPaths = new Map<string, GoldenPath>();

  async getGoldenPath(type: string): Promise<GoldenPath> {
    const path = this.goldenPaths.get(type);
    if (!path) {
      throw new Error(`Golden path not found for type: ${type}`);
    }
    return path;
  }

  async provision(request: ProvisionRequest): Promise<ServiceProvision> {
    const goldenPath = await this.getGoldenPath(request.serviceType);
    return await goldenPath.provision(request);
  }
}

// Self-Service Portal
export class SelfServicePortal {
  async createServiceRequest(request: ServiceRequest): Promise<RequestTicket> {
    // Validate request
    await this.validateRequest(request);

    // Create ticket
    const ticket = await this.createTicket(request);

    // Route to appropriate approval workflow
    await this.routeForApproval(ticket);

    return ticket;
  }

  private async validateRequest(request: ServiceRequest): Promise<void> {
    // Validate against policies, quotas, and governance rules
  }

  private async createTicket(request: ServiceRequest): Promise<RequestTicket> {
    return {
      id: generateTicketId(),
      request,
      status: 'pending',
      createdAt: new Date(),
    };
  }

  private async routeForApproval(ticket: RequestTicket): Promise<void> {
    // Route based on request type and risk level
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No platform engineering approach
export class BasicPlatform {
  // BAD: No self-service capabilities
  async createService(request: any) {
    // BAD: Manual process, no golden paths
    // BAD: No governance or compliance checks
    // BAD: No cost optimization
    // BAD: No observability setup
    return { success: true }
  }

  // BAD: No developer experience focus
  // BAD: No golden paths
  // BAD: No abstraction of complexity
  // BAD: No feedback loops
  // BAD: No platform as a product mindset
}
```

</example_bad>
