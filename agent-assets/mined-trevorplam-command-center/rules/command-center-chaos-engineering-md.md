---
description: Run Chaos Engineering and Resilience Testing Standards Check
globs:
  [
    '**/chaos/**/*.ts',
    '**/resilience/**/*.ts',
    '**/fault-injection/**/*.ts',
    '**/gremlin/**/*.yaml',
  ]
---

# Reliability: Chaos Engineering & Resilience Testing Standards

<audit_rules>

- You MUST implement proper chaos engineering experiments to test system resilience.
- You MUST ensure chaos experiments are conducted in non-production environments first.
- You MUST configure proper blast radius controls for chaos experiments.
- You MUST implement proper monitoring and alerting during chaos experiments.
- You MUST ensure chaos experiments are automated and integrated into CI/CD pipelines.
- You MUST implement proper game days exercises for team training.
- You MUST ensure proper rollback and recovery procedures are tested.
- You MUST configure proper failure injection mechanisms for various failure modes.
- You MUST ensure chaos experiments are documented and results are analyzed.
- You MUST implement proper steady-state metrics and hypothesis validation.
  </audit_rules>

<example_good>

```typescript
// Chaos Engineering Implementation

export class ChaosEngineeringOrchestrator {
  constructor(
    private chaosEngine: ChaosEngine,
    private monitoringService: MonitoringService,
    private alertingService: AlertingService,
    private recoveryService: RecoveryService
  ) {}

  async runChaosExperiment(experiment: ChaosExperiment): Promise<ExperimentResult> {
    // Validate experiment configuration
    await this.validateExperiment(experiment)

    // Establish steady-state metrics
    const steadyState = await this.establishSteadyState(experiment)

    // Set up blast radius controls
    const blastRadius = await this.configureBlastRadius(experiment)

    // Start monitoring
    const monitoringSession = await this.monitoringService.startSession({
      experimentId: experiment.id,
      metrics: experiment.steadyStateMetrics,
      duration: experiment.duration,
    })

    try {
      // Inject chaos
      await this.injectChaos(experiment)

      // Monitor system behavior
      const behavior = await this.monitorBehavior(experiment, steadyState)

      // Validate hypothesis
      const validation = await this.validateHypothesis(experiment.hypothesis, behavior)

      // Cleanup and recovery
      await this.cleanup(experiment)

      return {
        experimentId: experiment.id,
        steadyState,
        behavior,
        validation,
        blastRadius,
        duration: Date.now() - experiment.startTime,
        success: validation.passed,
      }
    } catch (error) {
      // Emergency recovery
      await this.emergencyRecovery(experiment)
      throw error
    } finally {
      await this.monitoringService.endSession(monitoringSession.id)
    }
  }

  async runLatencyInjection(service: string, latency: number, duration: number): Promise<void> {
    const experiment: ChaosExperiment = {
      id: generateId(),
      type: 'latency-injection',
      target: service,
      configuration: {
        latency,
        duration,
        affectedEndpoints: ['/api/*'],
      },
      steadyStateMetrics: ['response_time_p95', 'error_rate', 'throughput'],
      hypothesis: 'System maintains acceptable performance with increased latency',
      blastRadius: {
        services: [service],
        users: 'internal-only',
        regions: ['us-east-1'],
      },
    }

    await this.runChaosExperiment(experiment)
  }

  async runPodDeletion(namespace: string, count: number): Promise<void> {
    const experiment: ChaosExperiment = {
      id: generateId(),
      type: 'pod-deletion',
      target: namespace,
      configuration: {
        podCount: count,
        deletionStrategy: 'random',
        gracePeriod: 0,
      },
      steadyStateMetrics: ['availability', 'response_time', 'error_rate'],
      hypothesis: 'System maintains availability with pod failures',
      blastRadius: {
        namespaces: [namespace],
        services: await this.getServicesInNamespace(namespace),
        users: 'all',
      },
    }

    await this.runChaosExperiment(experiment)
  }

  async runNetworkPartition(serviceA: string, serviceB: string): Promise<void> {
    const experiment: ChaosExperiment = {
      id: generateId(),
      type: 'network-partition',
      target: `${serviceA}-${serviceB}`,
      configuration: {
        sourceService: serviceA,
        targetService: serviceB,
        direction: 'bidirectional',
        duration: 300000, // 5 minutes
      },
      steadyStateMetrics: ['connection_errors', 'circuit_breaker_trips', 'fallback_usage'],
      hypothesis: 'Circuit breakers prevent cascade failures during network partitions',
      blastRadius: {
        services: [serviceA, serviceB],
        users: 'all',
        regions: ['us-east-1'],
      },
    }

    await this.runChaosExperiment(experiment)
  }

  async runDiskPressure(service: string, pressure: number): Promise<void> {
    const experiment: ChaosExperiment = {
      id: generateId(),
      type: 'disk-pressure',
      target: service,
      configuration: {
        pressurePercentage: pressure,
        duration: 600000, // 10 minutes
        path: '/var/log',
      },
      steadyStateMetrics: ['disk_usage', 'write_latency', 'error_rate'],
      hypothesis: 'System degrades gracefully under disk pressure',
      blastRadius: {
        services: [service],
        users: 'internal-only',
        regions: ['us-east-1'],
      },
    }

    await this.runChaosExperiment(experiment)
  }

  private async validateExperiment(experiment: ChaosExperiment): Promise<void> {
    // Validate experiment doesn't exceed blast radius
    const blastRadiusValidation = await this.validateBlastRadius(experiment)
    if (!blastRadiusValidation.valid) {
      throw new Error(`Blast radius validation failed: ${blastRadiusValidation.reason}`)
    }

    // Validate experiment is safe for current time
    const timeValidation = await this.validateExperimentTiming(experiment)
    if (!timeValidation.valid) {
      throw new Error(`Timing validation failed: ${timeValidation.reason}`)
    }

    // Validate monitoring capabilities
    const monitoringValidation = await this.validateMonitoring(experiment)
    if (!monitoringValidation.valid) {
      throw new Error(`Monitoring validation failed: ${monitoringValidation.reason}`)
    }
  }

  private async establishSteadyState(experiment: ChaosExperiment): Promise<SteadyState> {
    const metrics = {}

    for (const metric of experiment.steadyStateMetrics) {
      const data = await this.monitoringService.getMetricHistory(metric, {
        duration: 3600000, // 1 hour
        target: experiment.target,
      })

      metrics[metric] = {
        mean: this.calculateMean(data),
        stddev: this.calculateStdDev(data),
        min: Math.min(...data),
        max: Math.max(...data),
      }
    }

    return {
      metrics,
      timestamp: Date.now(),
      duration: 3600000,
    }
  }

  private async configureBlastRadius(experiment: ChaosExperiment): Promise<BlastRadius> {
    return {
      affectedServices: experiment.blastRadius.services,
      affectedUsers: experiment.blastRadius.users,
      affectedRegions: experiment.blastRadius.regions,
      maxImpact: await this.calculateMaxImpact(experiment),
      rollbackPlan: await this.generateRollbackPlan(experiment),
    }
  }

  private async injectChaos(experiment: ChaosExperiment): Promise<void> {
    switch (experiment.type) {
      case 'latency-injection':
        await this.chaosEngine.injectLatency(experiment.target, experiment.configuration)
        break
      case 'pod-deletion':
        await this.chaosEngine.deletePods(experiment.target, experiment.configuration)
        break
      case 'network-partition':
        await this.chaosEngine.createNetworkPartition(experiment.configuration)
        break
      case 'disk-pressure':
        await this.chaosEngine.createDiskPressure(experiment.target, experiment.configuration)
        break
      default:
        throw new Error(`Unknown experiment type: ${experiment.type}`)
    }
  }

  private async monitorBehavior(
    experiment: ChaosExperiment,
    steadyState: SteadyState
  ): Promise<SystemBehavior> {
    const behavior = {}

    for (const metric of experiment.steadyStateMetrics) {
      const data = await this.monitoringService.getMetricHistory(metric, {
        duration: experiment.duration,
        target: experiment.target,
      })

      behavior[metric] = {
        mean: this.calculateMean(data),
        stddev: this.calculateStdDev(data),
        min: Math.min(...data),
        max: Math.max(...data),
        deviation: this.calculateDeviation(data, steadyState.metrics[metric]),
      }
    }

    return {
      metrics: behavior,
      alerts: await this.monitoringService.getAlerts(experiment.duration),
      errors: await this.monitoringService.getErrors(experiment.duration),
    }
  }

  private async validateHypothesis(
    hypothesis: string,
    behavior: SystemBehavior
  ): Promise<HypothesisValidation> {
    // Analyze if system behavior validates the hypothesis
    const deviations = Object.values(behavior.metrics).map((m) => m.deviation)
    const maxDeviation = Math.max(...deviations)

    return {
      hypothesis,
      passed: maxDeviation < 0.2, // 20% deviation threshold
      maxDeviation,
      confidence: this.calculateConfidence(behavior),
      recommendations: this.generateRecommendations(behavior),
    }
  }

  private async cleanup(experiment: ChaosExperiment): Promise<void> {
    await this.chaosEngine.cleanup(experiment.id)
    await this.alertingService.clearAlerts(experiment.id)
  }

  private async emergencyRecovery(experiment: ChaosExperiment): Promise<void> {
    await this.recoveryService.emergencyRecovery(experiment.target)
    await this.alertingService.sendEmergencyAlert(experiment.id)
  }

  // Game Day Exercise
  async runGameDay(scenario: GameDayScenario): Promise<GameDayResult> {
    const results = []

    for (const experiment of scenario.experiments) {
      try {
        const result = await this.runChaosExperiment(experiment)
        results.push(result)
      } catch (error) {
        results.push({
          experimentId: experiment.id,
          success: false,
          error: error.message,
        })
      }
    }

    return {
      scenarioId: scenario.id,
      results,
      teamPerformance: await this.evaluateTeamPerformance(scenario),
      lessonsLearned: await this.generateLessonsLearned(results),
    }
  }

  private calculateMean(data: number[]): number {
    return data.reduce((sum, value) => sum + value, 0) / data.length
  }

  private calculateStdDev(data: number[]): number {
    const mean = this.calculateMean(data)
    const variance = data.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / data.length
    return Math.sqrt(variance)
  }

  private calculateDeviation(data: number[], baseline: any): number {
    const currentMean = this.calculateMean(data)
    return Math.abs(currentMean - baseline.mean) / baseline.mean
  }

  private calculateConfidence(behavior: SystemBehavior): number {
    // Calculate confidence based on metric stability
    const deviations = Object.values(behavior.metrics).map((m) => m.stddev / m.mean)
    const avgDeviation = deviations.reduce((sum, d) => sum + d, 0) / deviations.length
    return Math.max(0, 1 - avgDeviation)
  }
}

// Chaos Engine Implementation
export class ChaosEngine {
  async injectLatency(target: string, config: LatencyConfig): Promise<void> {
    // Implement latency injection using service mesh or sidecar
    await this.serviceMesh.addLatency(target, {
      delay: config.latency,
      percentage: 100,
      endpoints: config.affectedEndpoints,
    })
  }

  async deletePods(namespace: string, config: PodDeletionConfig): Promise<void> {
    const pods = await this.kubernetes.getPods(namespace)
    const selectedPods = this.selectPods(pods, config.podCount, config.deletionStrategy)

    for (const pod of selectedPods) {
      await this.kubernetes.deletePod(pod.name, namespace, { gracePeriod: config.gracePeriod })
    }
  }

  async createNetworkPartition(config: NetworkPartitionConfig): Promise<void> {
    await this.serviceMesh.createNetworkPolicy({
      sourceSelector: { app: config.sourceService },
      targetSelector: { app: config.targetService },
      direction: config.direction,
    })
  }

  async createDiskPressure(target: string, config: DiskPressureConfig): Promise<void> {
    await this.nodeAgent.createDiskPressure(target, {
      path: config.path,
      pressure: config.pressurePercentage,
      duration: config.duration,
    })
  }

  async cleanup(experimentId: string): Promise<void> {
    await this.serviceMesh.cleanup(experimentId)
    await this.kubernetes.cleanup(experimentId)
    await this.nodeAgent.cleanup(experimentId)
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No chaos engineering practices
export class BasicSystem {
  // BAD: No resilience testing
  async handleRequest(request: any) {
    // BAD: No failure injection
    // BAD: No circuit breakers
    // BAD: No fallback mechanisms
    return await this.processRequest(request)
  }

  // BAD: No chaos experiments
  // BAD: No resilience testing
  // BAD: No blast radius controls
  // BAD: No steady-state monitoring
  // BAD: No hypothesis validation
}
```

</example_bad>
