---
description: Run Advanced Automation and Autonomous Systems Standards Check
globs: ["**/automation/**/*.ts", "**/autonomous/**/*.ts", "**/robotics/**/*.ts", "**/ai-automation/**/*.ts"]
---
# Future-Proof: Advanced Automation & Autonomous Systems Standards

<audit_rules>
- You MUST implement proper autonomous decision-making with ethical constraints and safety boundaries.
- You MUST ensure proper human-in-the-loop controls with override mechanisms.
- You MUST implement proper sensor fusion and environmental perception systems.
- You MUST configure proper fail-safe mechanisms and emergency stop procedures.
- You MUST ensure proper explainable AI for autonomous system decisions.
- You MUST implement proper continuous learning with safe exploration policies.
- You MUST configure proper multi-agent coordination and communication protocols.
- You MUST ensure proper system resilience and graceful degradation.
- You MUST implement proper cybersecurity for autonomous systems against adversarial attacks.
- You MUST ensure proper regulatory compliance and certification for autonomous operations.
</audit_rules>

<example_good>
```typescript
// Advanced Automation Implementation

export class AutonomousSystemOrchestrator {
  constructor(
    private decisionEngine: AutonomousDecisionEngine,
    private perceptionSystem: MultiSensorPerception,
    private safetyManager: SafetyManager,
    private humanInterface: HumanInLoopInterface,
    private learningEngine: ContinuousLearningEngine,
    private coordinationManager: MultiAgentCoordinator,
    private resilienceManager: ResilienceManager,
    private complianceManager: ComplianceManager
  ) {}

  async initializeAutonomousSystem(config: AutonomousSystemConfig): Promise<AutonomousSystem> {
    // Validate system configuration
    const validation = await this.validateSystemConfig(config);
    if (!validation.valid) {
      throw new Error(`Invalid system configuration: ${validation.errors.join(', ')}`);
    }

    // Setup perception system
    const perceptionSetup = await this.perceptionSystem.initialize({
      sensors: config.sensors,
      fusionAlgorithm: config.sensorFusion || 'kalman',
      environmentModel: config.environmentModel || '3d_occupancy_grid',
      updateRate: config.perceptionUpdateRate || 30,
    });

    // Setup decision engine with ethical constraints
    const decisionSetup = await this.decisionEngine.initialize({
      algorithm: config.decisionAlgorithm || 'hierarchical_rl',
      ethicalFramework: config.ethicalFramework || 'utilitarian_with_constraints',
      safetyConstraints: config.safetyConstraints || this.getDefaultSafetyConstraints(),
      explainability: config.explainability || true,
    });

    // Setup safety manager
    const safetySetup = await this.safetyManager.initialize({
      emergencyStop: config.emergencyStop || true,
      failSafeMode: config.failSafeMode || true,
      riskAssessment: config.riskAssessment || true,
      monitoringRate: config.safetyMonitoringRate || 100,
    });

    // Setup human-in-the-loop interface
    const humanInterfaceSetup = await this.humanInterface.initialize({
      overrideMechanism: config.overrideMechanism || true,
      monitoringDashboard: config.monitoringDashboard || true,
      alertSystem: config.alertSystem || true,
      communicationProtocol: config.communicationProtocol || 'websocket',
    });

    // Setup continuous learning
    const learningSetup = await this.learningEngine.initialize({
      learningRate: config.learningRate || 0.001,
      explorationPolicy: config.explorationPolicy || 'epsilon_greedy',
      safeExploration: config.safeExploration || true,
      knowledgeRetention: config.knowledgeRetention || true,
    });

    return {
      systemId: config.systemId,
      perceptionSetup,
      decisionSetup,
      safetySetup,
      humanInterfaceSetup,
      learningSetup,
      status: 'initialized',
      initializedAt: Date.now(),
    };
  }

  async executeAutonomousTask(task: AutonomousTask): Promise<TaskExecutionResult> {
    // Validate task
    const validation = await this.validateTask(task);
    if (!validation.valid) {
      throw new Error(`Invalid task: ${validation.errors.join(', ')}`);
    }

    // Assess task risk
    const riskAssessment = await this.safetyManager.assessTaskRisk(task);
    if (riskAssessment.level === 'critical') {
      throw new Error(`Task risk too high: ${riskAssessment.reasons.join(', ')}`);
    }

    // Get human approval if required
    if (task.requiresHumanApproval) {
      const approval = await this.humanInterface.requestApproval(task, riskAssessment);
      if (!approval.granted) {
        throw new Error(`Human approval denied: ${approval.reason}`);
      }
    }

    // Execute task with continuous monitoring
    const execution = await this.executeTaskWithMonitoring(task, riskAssessment);

    return {
      taskId: task.id,
      execution,
      riskAssessment,
      humanApproval: task.requiresHumanApproval ? await this.humanInterface.getApproval(task.id) : null,
      timestamp: Date.now(),
    };
  }

  private async executeTaskWithMonitoring(task: AutonomousTask, riskAssessment: RiskAssessment): Promise<TaskExecution> {
    const execution = {
      taskId: task.id,
      status: 'running',
      startTime: Date.now(),
      steps: [],
      decisions: [],
      safetyEvents: [],
    };

    try {
      // Initialize task context
      const context = await this.initializeTaskContext(task);
      
      // Execute task steps
      for (const step of task.steps) {
        const stepResult = await this.executeTaskStep(step, context, execution);
        execution.steps.push(stepResult);

        // Check safety after each step
        const safetyCheck = await this.safetyManager.checkSafety(context, stepResult);
        if (!safetyCheck.safe) {
          await this.handleSafetyEvent(safetyCheck, execution);
          if (safetyCheck.requiresStop) {
            break;
          }
        }

        // Update context
        context.update(stepResult);
      }

      execution.status = 'completed';
      execution.endTime = Date.now();
      
    } catch (error) {
      execution.status = 'failed';
      execution.error = error.message;
      execution.endTime = Date.now();
      
      // Trigger safety response
      await this.safetyManager.handleExecutionError(error, execution);
    }

    return execution;
  }

  async executeTaskStep(step: TaskStep, context: TaskContext, execution: TaskExecution): Promise<StepResult> {
    // Get perception data
    const perceptionData = await this.perceptionSystem.getPerception(context.environment);
    
    // Make autonomous decision
    const decision = await this.decisionEngine.makeDecision({
      step,
      context,
      perception: perceptionData,
      previousDecisions: execution.decisions,
    });

    // Validate decision against safety constraints
    const safetyValidation = await this.safetyManager.validateDecision(decision, context);
    if (!safetyValidation.safe) {
      throw new Error(`Decision unsafe: ${safetyValidation.reasons.join(', ')}`);
    }

    // Execute decision
    const actionResult = await this.executeAction(decision.action, context);
    
    // Record decision for explainability
    const explanation = await this.decisionEngine.explainDecision(decision, context, perceptionData);

    const stepResult = {
      stepId: step.id,
      decision,
      actionResult,
      explanation,
      perceptionData,
      safetyValidation,
      timestamp: Date.now(),
    };

    execution.decisions.push(decision);

    return stepResult;
  }

  async handleHumanOverride(override: HumanOverride): Promise<OverrideResult> {
    // Validate override request
    const validation = await this.validateOverride(override);
    if (!validation.valid) {
      throw new Error(`Invalid override: ${validation.errors.join(', ')}`);
    }

    // Check override authority
    const authorityCheck = await this.humanInterface.checkAuthority(override.userId, override.level);
    if (!authorityCheck.authorized) {
      throw new Error(`User not authorized for override level: ${override.level}`);
    }

    // Apply override
    const overrideResult = await this.applyOverride(override);

    // Log override for compliance
    await this.complianceManager.logOverride(override, overrideResult);

    // Update learning system
    await this.learningEngine.processOverride(override, overrideResult);

    return overrideResult;
  }

  async coordinateMultiAgents(coordination: MultiAgentCoordination): Promise<CoordinationResult> {
    // Validate coordination request
    const validation = await this.validateCoordination(coordination);
    if (!validation.valid) {
      throw new Error(`Invalid coordination: ${validation.errors.join(', ')}`);
    }

    // Setup communication protocols
    const communication = await this.coordinationManager.setupCommunication({
      agents: coordination.agents,
      protocol: coordination.protocol || 'p2p_encrypted',
      reliability: coordination.reliability || 'high',
    });

    // Execute coordinated task
    const execution = await this.executeCoordinatedTask(coordination, communication);

    return {
      coordinationId: coordination.id,
      execution,
      communication,
      timestamp: Date.now(),
    };
  }

  async learnFromExperience(experience: LearningExperience): Promise<LearningResult> {
    // Validate learning experience
    const validation = await this.validateLearningExperience(experience);
    if (!validation.valid) {
      throw new Error(`Invalid learning experience: ${validation.errors.join(', ')}`);
    }

    // Process experience
    const processed = await this.learningEngine.processExperience(experience);
    
    // Update models
    const modelUpdate = await this.learningEngine.updateModels(processed);
    
    // Validate updated models
    const validationResults = await this.learningEngine.validateModels(modelUpdate);

    return {
      experienceId: experience.id,
      modelUpdate,
      validationResults,
      improvement: this.calculateImprovement(experience, modelUpdate),
      timestamp: Date.now(),
    };
  }

  private async initializeTaskContext(task: AutonomousTask): Promise<TaskContext> {
    // Get initial perception
    const perception = await this.perceptionSystem.getPerception(task.environment);
    
    // Initialize context
    const context = {
      taskId: task.id,
      environment: task.environment,
      perception,
      startTime: Date.now(),
      objectives: task.objectives,
      constraints: task.constraints,
      history: [],
    };

    return context;
  }

  private async executeAction(action: AutonomousAction, context: TaskContext): Promise<ActionResult> {
    // Validate action safety
    const safetyCheck = await this.safetyManager.validateAction(action, context);
    if (!safetyCheck.safe) {
      throw new Error(`Action unsafe: ${safetyCheck.reasons.join(', ')}`);
    }

    // Execute action
    const result = await this.performAction(action, context);

    // Update environment model
    await this.perceptionSystem.updateEnvironmentModel(action, result, context);

    return result;
  }

  private async performAction(action: AutonomousAction, context: TaskContext): Promise<ActionResult> {
    switch (action.type) {
      case 'navigation':
        return await this.executeNavigationAction(action, context);
      case 'manipulation':
        return await this.executeManipulationAction(action, context);
      case 'communication':
        return await this.executeCommunicationAction(action, context);
      case 'monitoring':
        return await this.executeMonitoringAction(action, context);
      default:
        throw new Error(`Unknown action type: ${action.type}`);
    }
  }

  private async executeNavigationAction(action: NavigationAction, context: TaskContext): Promise<ActionResult> {
    // Plan path
    const path = await this.planPath(action.destination, context);
    
    // Execute navigation
    const navigation = await this.navigatePath(path, context);
    
    return {
      actionType: 'navigation',
      success: navigation.success,
      result: navigation,
      timestamp: Date.now(),
    };
  }

  private async executeManipulationAction(action: ManipulationAction, context: TaskContext): Promise<ActionResult> {
    // Plan manipulation
    const plan = await this.planManipulation(action.target, action.operation, context);
    
    // Execute manipulation
    const manipulation = await this.performManipulation(plan, context);
    
    return {
      actionType: 'manipulation',
      success: manipulation.success,
      result: manipulation,
      timestamp: Date.now(),
    };
  }

  private async handleSafetyEvent(safetyCheck: SafetyCheck, execution: TaskExecution): Promise<void> {
    const safetyEvent = {
      eventId: generateId(),
      type: safetyCheck.severity,
      reasons: safetyCheck.reasons,
      context: execution,
      timestamp: Date.now(),
    };

    execution.safetyEvents.push(safetyEvent);

    // Apply safety response
    await this.safetyManager.respondToSafetyEvent(safetyEvent);

    // Notify human operator
    await this.humanInterface.notifySafetyEvent(safetyEvent);
  }

  private calculateImprovement(experience: LearningExperience, modelUpdate: ModelUpdate): number {
    // Calculate improvement based on experience and model update
    const beforePerformance = experience.metrics.performance;
    const afterPerformance = modelUpdate.performance;
    
    if (beforePerformance && afterPerformance) {
      return (afterPerformance - beforePerformance) / beforePerformance;
    }
    
    return 0;
  }

  private getDefaultSafetyConstraints(): SafetyConstraint[] {
    return [
      {
        type: 'collision_avoidance',
        threshold: 0.5, // meters
        priority: 'critical',
      },
      {
        type: 'speed_limit',
        threshold: 2.0, // m/s
        priority: 'high',
      },
      {
        type: 'energy_consumption',
        threshold: 0.8, // 80% of capacity
        priority: 'medium',
      },
      {
        type: 'communication_range',
        threshold: 100, // meters
        priority: 'medium',
      },
    ];
  }
}

// Autonomous Decision Engine Implementation
export class AutonomousDecisionEngine {
  constructor(
    private ethicalFramework: EthicalFramework,
    private explainabilityEngine: ExplainabilityEngine,
    private riskAssessor: DecisionRiskAssessor
  ) {}

  async makeDecision(request: DecisionRequest): Promise<AutonomousDecision> {
    // Analyze current situation
    const situationAnalysis = await this.analyzeSituation(request);
    
    // Generate possible actions
    const possibleActions = await this.generateActions(situationAnalysis);
    
    // Evaluate actions against ethical framework
    const ethicalEvaluation = await this.evaluateActionsEthically(possibleActions, request);
    
    // Assess risks of each action
    const riskAssessment = await this.assessActionRisks(possibleActions, situationAnalysis);
    
    // Select best action
    const selectedAction = await this.selectBestAction(
      possibleActions,
      ethicalEvaluation,
      riskAssessment,
      request
    );

    // Generate explanation
    const explanation = await this.explainabilityEngine.explainDecision(
      selectedAction,
      situationAnalysis,
      ethicalEvaluation,
      riskAssessment
    );

    return {
      action: selectedAction,
      explanation,
      ethicalScore: ethicalEvaluation[selectedAction.id].score,
      riskScore: riskAssessment[selectedAction.id].score,
      confidence: this.calculateConfidence(situationAnalysis),
      timestamp: Date.now(),
    };
  }

  async explainDecision(decision: AutonomousDecision, context: TaskContext, perception: PerceptionData): Promise<DecisionExplanation> {
    return await this.explainabilityEngine.generateExplanation({
      decision,
      context,
      perception,
      includeReasoning: true,
      includeAlternatives: true,
      includeUncertainty: true,
    });
  }

  private async analyzeSituation(request: DecisionRequest): Promise<SituationAnalysis> {
    return {
      environment: request.context.environment,
      objectives: request.context.objectives,
      constraints: request.context.constraints,
      risks: await this.identifyRisks(request),
      opportunities: await this.identifyOpportunities(request),
      uncertainty: await this.assessUncertainty(request),
    };
  }

  private async generateActions(situation: SituationAnalysis): Promise<AutonomousAction[]> {
    const actions = [];

    // Generate navigation actions
    if (situation.environment.requiresNavigation) {
      actions.push(...await this.generateNavigationActions(situation));
    }

    // Generate manipulation actions
    if (situation.environment.requiresManipulation) {
      actions.push(...await this.generateManipulationActions(situation));
    }

    // Generate communication actions
    if (situation.environment.requiresCommunication) {
      actions.push(...await this.generateCommunicationActions(situation));
    }

    return actions;
  }

  private async evaluateActionsEthically(actions: AutonomousAction[], request: DecisionRequest): Promise<EthicalEvaluation> {
    const evaluation = {};

    for (const action of actions) {
      evaluation[action.id] = await this.ethicalFramework.evaluateAction({
        action,
        context: request.context,
        principles: request.ethicalPrinciples || ['do_no_harm', 'fairness', 'transparency'],
      });
    }

    return evaluation;
  }

  private async assessActionRisks(actions: AutonomousAction[], situation: SituationAnalysis): Promise<RiskAssessment> {
    const assessment = {};

    for (const action of actions) {
      assessment[action.id] = await this.riskAssessor.assessRisk({
        action,
        situation,
        riskFactors: ['collision', 'equipment_damage', 'mission_failure', 'human_safety'],
      });
    }

    return assessment;
  }

  private async selectBestAction(
    actions: AutonomousAction[],
    ethicalEval: EthicalEvaluation,
    riskAssess: RiskAssessment,
    request: DecisionRequest
  ): Promise<AutonomousAction> {
    let bestAction = null;
    let bestScore = -Infinity;

    for (const action of actions) {
      const ethicalScore = ethicalEval[action.id].score;
      const riskScore = 1 - riskAssess[action.id].score; // Lower risk is better
      const utilityScore = await this.calculateUtility(action, request);
      
      // Weighted score
      const score = (
        ethicalScore * 0.4 +
        riskScore * 0.3 +
        utilityScore * 0.3
      );

      if (score > bestScore) {
        bestScore = score;
        bestAction = action;
      }
    }

    return bestAction || actions[0];
  }

  private calculateConfidence(situation: SituationAnalysis): number {
    // Calculate confidence based on situation uncertainty and data quality
    const uncertainty = situation.uncertainty.level;
    const dataQuality = this.assessDataQuality(situation);
    
    return (1 - uncertainty) * dataQuality;
  }

  private assessDataQuality(situation: SituationAnalysis): number {
    // Assess quality of perception data and context information
    return 0.8; // Placeholder
  }
}

// Safety Manager Implementation
export class SafetyManager {
  constructor(
    private riskAssessor: SafetyRiskAssessor,
    private emergencyHandler: EmergencyHandler,
    private monitoringSystem: SafetyMonitoringSystem
  ) {}

  async initialize(config: SafetyConfig): Promise<SafetySetup> {
    // Setup emergency handlers
    await this.emergencyHandler.setup({
      emergencyStop: config.emergencyStop,
      failSafeMode: config.failSafeMode,
      recoveryProcedures: config.recoveryProcedures || [],
    });

    // Setup safety monitoring
    await this.monitoringSystem.setup({
      monitoringRate: config.monitoringRate,
      alertThresholds: config.alertThresholds || this.getDefaultThresholds(),
      loggingLevel: config.loggingLevel || 'detailed',
    });

    return {
      config,
      emergencyHandler: this.emergencyHandler,
      monitoringSystem: this.monitoringSystem,
      initializedAt: Date.now(),
    };
  }

  async assessTaskRisk(task: AutonomousTask): Promise<RiskAssessment> {
    const riskFactors = await this.identifyRiskFactors(task);
    const riskLevel = this.calculateRiskLevel(riskFactors);
    const mitigationStrategies = await this.generateMitigationStrategies(riskFactors);

    return {
      taskId: task.id,
      level: riskLevel,
      factors: riskFactors,
      mitigation: mitigationStrategies,
      requiresHumanApproval: riskLevel === 'critical' || riskLevel === 'high',
      assessedAt: Date.now(),
    };
  }

  async checkSafety(context: TaskContext, stepResult: StepResult): Promise<SafetyCheck> {
    // Monitor system state
    const systemState = await this.monitoringSystem.getSystemState(context);
    
    // Check safety constraints
    const constraintViolations = await this.checkConstraints(systemState, context);
    
    // Assess immediate risks
    const immediateRisks = await this.assessImmediateRisks(systemState, stepResult);
    
    const isSafe = constraintViolations.length === 0 && immediateRisks.length === 0;
    const requiresStop = constraintViolations.some(v => v.severity === 'critical') ||
                       immediateRisks.some(r => r.severity === 'critical');

    return {
      safe: isSafe,
      requiresStop,
      violations: constraintViolations,
      risks: immediateRisks,
      systemState,
      timestamp: Date.now(),
    };
  }

  async validateDecision(decision: AutonomousDecision, context: TaskContext): Promise<SafetyValidation> {
    // Simulate decision outcome
    const simulation = await this.simulateDecision(decision, context);
    
    // Check for safety violations in simulation
    const violations = await this.checkSimulationSafety(simulation);
    
    // Assess decision risk
    const risk = await this.assessDecisionRisk(decision, simulation);

    return {
      safe: violations.length === 0 && risk.level !== 'critical',
      violations,
      risk,
      simulation,
      timestamp: Date.now(),
    };
  }

  async validateAction(action: AutonomousAction, context: TaskContext): Promise<SafetyValidation> {
    // Similar to decision validation but for individual actions
    const actionDecision = { action, explanation: null, ethicalScore: 0, riskScore: 0, confidence: 0 };
    return await this.validateDecision(actionDecision, context);
  }

  async handleExecutionError(error: Error, execution: TaskExecution): Promise<void> {
    // Classify error severity
    const severity = this.classifyErrorSeverity(error);
    
    // Trigger appropriate response
    switch (severity) {
      case 'critical':
        await this.emergencyHandler.emergencyStop();
        break;
      case 'high':
        await this.emergencyHandler.failSafeMode();
        break;
      case 'medium':
        await this.emergencyHandler.safeRecovery();
        break;
      case 'low':
        await this.emergencyHandler.logAndContinue();
        break;
    }

    // Notify human operator
    await this.notifyError(error, severity, execution);
  }

  async respondToSafetyEvent(event: SafetyEvent): Promise<void> {
    // Implement safety response based on event type and severity
    switch (event.type) {
      case 'collision_risk':
        await this.handleCollisionRisk(event);
        break;
      case 'equipment_failure':
        await this.handleEquipmentFailure(event);
        break;
      case 'communication_loss':
        await this.handleCommunicationLoss(event);
        break;
      case 'human_safety_risk':
        await this.handleHumanSafetyRisk(event);
        break;
    }
  }

  private getDefaultThresholds(): SafetyThresholds {
    return {
      collisionDistance: 0.5,
      maxSpeed: 2.0,
      maxAcceleration: 1.0,
      batteryLevel: 0.2,
      communicationDelay: 1000,
      temperature: 60,
    };
  }

  private calculateRiskLevel(riskFactors: RiskFactor[]): RiskLevel {
    const criticalFactors = riskFactors.filter(f => f.severity === 'critical');
    const highFactors = riskFactors.filter(f => f.severity === 'high');
    const mediumFactors = riskFactors.filter(f => f.severity === 'medium');

    if (criticalFactors.length > 0) return 'critical';
    if (highFactors.length > 1) return 'critical';
    if (highFactors.length > 0) return 'high';
    if (mediumFactors.length > 2) return 'high';
    if (mediumFactors.length > 0) return 'medium';
    return 'low';
  }

  private classifyErrorSeverity(error: Error): ErrorSeverity {
    // Classify error based on type and message
    if (error.message.includes('collision') || error.message.includes('safety')) {
      return 'critical';
    }
    if (error.message.includes('equipment') || error.message.includes('hardware')) {
      return 'high';
    }
    if (error.message.includes('communication') || error.message.includes('sensor')) {
      return 'medium';
    }
    return 'low';
  }

  private async handleCollisionRisk(event: SafetyEvent): Promise<void> {
    // Immediate stop
    await this.emergencyHandler.emergencyStop();
    
    // Notify operator
    await this.notifySafetyEvent(event);
  }

  private async handleEquipmentFailure(event: SafetyEvent): Promise<void> {
    // Switch to fail-safe mode
    await this.emergencyHandler.failSafeMode();
    
    // Notify operator
    await this.notifySafetyEvent(event);
  }

  private async handleCommunicationLoss(event: SafetyEvent): Promise<void> {
    // Enter autonomous mode with limited capabilities
    await this.emergencyHandler.limitedAutonomousMode();
    
    // Notify operator
    await this.notifySafetyEvent(event);
  }

  private async handleHumanSafetyRisk(event: SafetyEvent): Promise<void> {
    // Immediate stop and safe shutdown
    await this.emergencyHandler.emergencyStop();
    
    // Notify operator with highest priority
    await this.notifySafetyEvent(event);
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No advanced automation standards
export class BasicAutomation {
  // BAD: No safety constraints
  async executeTask(task: any) {
    // BAD: No ethical framework
    // BAD: No human-in-the-loop
    // BAD: No explainability
    return this.performAction(task);
  }

  // BAD: No multi-agent coordination
  // BAD: No continuous learning
  // BAD: No resilience management
  // BAD: No compliance checking
}
```
</example_bad>
