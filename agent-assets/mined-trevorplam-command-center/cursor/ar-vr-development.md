---
description: Run AR/VR Development and Spatial Computing Standards Check
globs: ["**/arvr/**/*.ts", "**/spatial-computing/**/*.ts", "**/xr/**/*.ts", "**/webxr/**/*.ts"]
---
# Future-Proof: AR/VR Development & Spatial Computing Standards

<audit_rules>
- You MUST implement proper WebXR API integration with browser compatibility checks.
- You MUST implement proper spatial tracking and environment understanding for AR applications.
- You MUST implement proper performance optimization for 60+ FPS rendering on mobile devices.
- You MUST implement proper hand tracking and gesture recognition for natural interactions.
- You MUST implement proper 3D asset optimization with compression and LOD management.
- You MUST implement proper spatial audio positioning and audio context management.
- You MUST implement proper cross-platform compatibility for ARCore, ARKit, and WebXR.
- You MUST implement proper accessibility features for VR/AR applications.
- You MUST implement proper motion sickness prevention and comfort settings.
- You MUST implement proper security and privacy for camera/microphone permissions.
</audit_rules>

<example_good>
```typescript
// AR/VR Development Implementation
import { z } from 'zod';
import { WebXRManager } from './webxr';
import { SpatialTracker } from './spatial-tracking';
import { PerformanceOptimizer } from './performance';
import { GestureRecognizer } from './gesture-recognition';

export class ARVRDevelopmentOrchestrator {
  constructor(
    private xrEngine: XREngine,
    private spatialTracker: SpatialTrackingEngine,
    private performanceOptimizer: XRPerformanceOptimizer,
    private gestureRecognizer: GestureRecognitionEngine,
    private assetManager: XRAssetManager,
    private spatialAudio: SpatialAudioEngine,
    private accessibilityManager: XRAccessibilityManager,
    private comfortManager: ComfortSettingsManager
  ) {}

  // WebXR API integration with browser compatibility checks
  async initializeXRSession(config: XRSessionConfig): Promise<XRSession> {
    // Check WebXR support
    const supportCheck = await this.checkWebXRSupport();
    if (!supportCheck.supported) {
      throw new Error(`WebXR not supported: ${supportCheck.reason}`);
    }

    // Request appropriate permissions
    await this.requestPermissions(config.permissions);

    // Initialize XR session
    const session = await this.xrEngine.initializeSession({
      mode: config.mode || 'immersive-vr',
      features: config.features || [],
      options: {
        requiredFeatures: config.requiredFeatures || [],
        optionalFeatures: config.optionalFeatures || [],
      },
    });

    // Setup spatial tracking
    const spatialTracking = await this.spatialTracker.setup(session, {
      trackingMode: config.spatialTracking?.mode || 'world-scale',
      environmentUnderstanding: config.spatialTracking?.environment || true,
      planeDetection: config.spatialTracking?.planeDetection || true,
    });

    // Setup performance optimization
    const performanceConfig = await this.performanceOptimizer.configure(session, {
      targetFPS: config.targetFPS || 60,
      adaptiveQuality: config.adaptiveQuality || true,
      lodManagement: config.lodManagement || true,
    });

    // Setup gesture recognition
    const gestureConfig = await this.gestureRecognizer.setup(session, {
      handTracking: config.gestures?.handTracking || true,
      gestureTypes: config.gestures?.types || ['pinch', 'grab', 'point'],
      confidence: config.gestures?.confidence || 0.7,
    });

    return {
      sessionId: session.id,
      mode: config.mode,
      spatialTracking,
      performanceConfig,
      gestureConfig,
      initializedAt: Date.now(),
    };
  }

  // Performance optimization for 60+ FPS rendering
  async renderXRScene(renderRequest: XRRenderRequest): Promise<XRRenderResult> {
    // Validate render request
    const validation = await this.validateRenderRequest(renderRequest);
    if (!validation.valid) {
      throw new Error(`Invalid render request: ${validation.errors.join(', ')}`);
    }

    // Get current frame
    const frame = await this.xrEngine.getCurrentFrame(renderRequest.sessionId);
    
    // Update spatial tracking
    const spatialData = await this.spatialTracker.update(frame);
    
    // Process gestures
    const gestures = await this.gestureRecognizer.processFrame(frame, spatialData);
    
    // Optimize rendering based on performance
    const optimization = await this.performanceOptimizer.optimizeFrame(frame, {
      spatialData,
      gestures,
      targetFPS: renderRequest.targetFPS,
    });

    // Render scene
    const renderResult = await this.renderScene({
      frame,
      spatialData,
      gestures,
      optimization,
      scene: renderRequest.scene,
    });

    // Apply spatial audio
    if (renderRequest.audio) {
      await this.spatialAudio.update(renderResult.audioContext, spatialData);
    }

    // Check comfort settings
    await this.comfortManager.applyComfortSettings(renderResult, frame);

    return {
      frameId: frame.id,
      renderTime: renderResult.renderTime,
      fps: renderResult.fps,
      spatialData,
      gestures,
      performanceMetrics: optimization.metrics,
      timestamp: Date.now(),
    };
  }

  // 3D asset optimization with compression and LOD management
  async optimizeAssets(assetOptimization: AssetOptimizationRequest): Promise<OptimizedAssets> {
    // Validate asset optimization request
    const validation = await this.validateAssetOptimization(assetOptimization);
    if (!validation.valid) {
      throw new Error(`Invalid asset optimization: ${validation.errors.join(', ')}`);
    }

    const optimizedAssets = {};

    // Optimize 3D models
    for (const model of assetOptimization.models) {
      const optimizedModel = await this.optimizeModel(model, {
        compression: assetOptimization.compression || 'draco',
        lodLevels: assetOptimization.lodLevels || 3,
        targetSize: assetOptimization.targetModelSize || 1024 * 1024, // 1MB
      });
      optimizedAssets[model.id] = optimizedModel;
    }

    // Optimize textures
    for (const texture of assetOptimization.textures) {
      const optimizedTexture = await this.optimizeTexture(texture, {
        compression: assetOptimization.textureCompression || 'astc',
        maxResolution: assetOptimization.maxTextureResolution || 2048,
        mipmaps: assetOptimization.mipmaps || true,
      });
      optimizedAssets[texture.id] = optimizedTexture;
    }

    // Optimize audio
    for (const audio of assetOptimization.audio) {
      const optimizedAudio = await this.optimizeAudio(audio, {
        compression: assetOptimization.audioCompression || 'opus',
        spatialAudio: assetOptimization.spatialAudio || true,
        maxBitrate: assetOptimization.maxAudioBitrate || 128000,
      });
      optimizedAssets[audio.id] = optimizedAudio;
    }

    return {
      assets: optimizedAssets,
      totalSizeReduction: this.calculateSizeReduction(assetOptimization, optimizedAssets),
      optimizationLevel: assetOptimization.optimizationLevel || 'medium',
      optimizedAt: Date.now(),
    };
  }

  // Hand tracking and gesture recognition
  async setupGestureRecognition(config: GestureRecognitionConfig): Promise<GestureRecognitionSetup> {
    // Validate gesture configuration
    const validation = await this.validateGestureConfig(config);
    if (!validation.valid) {
      throw new Error(`Invalid gesture configuration: ${validation.errors.join(', ')}`);
    }

    // Initialize hand tracking
    const handTracking = await this.gestureRecognizer.initializeHandTracking({
      confidence: config.confidence || 0.7,
      trackingMode: config.trackingMode || 'continuous',
      smoothing: config.smoothing || true,
    });

    // Setup gesture classifiers
    const classifiers = await this.gestureRecognizer.setupClassifiers({
      gestures: config.gestures || ['pinch', 'grab', 'point', 'swipe', 'rotate'],
      modelPath: config.modelPath || '/models/gesture-classifier',
    });

    // Configure gesture callbacks
    const callbacks = await this.gestureRecognizer.setupCallbacks({
      onGestureDetected: config.onGestureDetected,
      onGestureLost: config.onGestureLost,
      onHandDetected: config.onHandDetected,
      onHandLost: config.onHandLost,
    });

    return {
      handTracking,
      classifiers,
      callbacks,
      sessionId: config.sessionId,
      setupAt: Date.now(),
    };
  }

  // Spatial audio positioning and audio context management
  async setupSpatialAudio(audioConfig: SpatialAudioConfig): Promise<SpatialAudioSetup> {
    // Validate audio configuration
    const validation = await this.validateAudioConfig(audioConfig);
    if (!validation.valid) {
      throw new Error(`Invalid audio configuration: ${validation.errors.join(', ')}`);
    }

    // Initialize spatial audio engine
    const audioEngine = await this.spatialAudio.initialize({
      sessionId: audioConfig.sessionId,
      audioContextOptions: {
        sampleRate: audioConfig.sampleRate || 48000,
        bufferSize: audioConfig.bufferSize || 512,
      },
      spatialModel: audioConfig.spatialModel || 'hrtf',
    });

    // Setup audio sources
    const audioSources = [];
    for (const source of audioConfig.sources) {
      const audioSource = await this.spatialAudio.createSource(audioEngine, {
        position: source.position,
        orientation: source.orientation,
        cone: source.cone,
        distanceModel: source.distanceModel || 'inverse',
        maxDistance: source.maxDistance || 100,
        refDistance: source.refDistance || 1,
        rolloffFactor: source.rolloffFactor || 1,
      });
      audioSources.push(audioSource);
    }

    // Setup audio listener
    const listener = await this.spatialAudio.setupListener(audioEngine, {
      position: { x: 0, y: 0, z: 0 },
      orientation: { x: 0, y: 0, z: 0, w: 1 },
      up: { x: 0, y: 1, z: 0 },
    });

    return {
      audioEngine,
      audioSources,
      listener,
      sessionId: audioConfig.sessionId,
      setupAt: Date.now(),
    };
  }

  // Accessibility features for VR/AR applications
  async implementAccessibility(accessibilityConfig: XRAccessibilityConfig): Promise<AccessibilitySetup> {
    // Validate accessibility configuration
    const validation = await this.validateAccessibilityConfig(accessibilityConfig);
    if (!validation.valid) {
      throw new Error(`Invalid accessibility configuration: ${validation.errors.join(', ')}`);
    }

    // Setup visual accessibility features
    const visualFeatures = await this.accessibilityManager.setupVisualFeatures({
      highContrast: accessibilityConfig.visual?.highContrast || false,
      textScaling: accessibilityConfig.visual?.textScaling || 1.0,
      colorBlindnessMode: accessibilityConfig.visual?.colorBlindnessMode || 'none',
      reducedMotion: accessibilityConfig.visual?.reducedMotion || false,
    });

    // Setup motor accessibility features
    const motorFeatures = await this.accessibilityManager.setupMotorFeatures({
      simplifiedControls: accessibilityConfig.motor?.simplifiedControls || false,
      voiceControl: accessibilityConfig.motor?.voiceControl || false,
      eyeTracking: accessibilityConfig.motor?.eyeTracking || false,
      gestureSensitivity: accessibilityConfig.motor?.gestureSensitivity || 1.0,
    });

    // Setup audio accessibility features
    const audioFeatures = await this.accessibilityManager.setupAudioFeatures({
      visualIndicators: accessibilityConfig.audio?.visualIndicators || false,
      subtitles: accessibilityConfig.audio?.subtitles || false,
      volumeNormalization: accessibilityConfig.audio?.volumeNormalization || true,
      monoAudio: accessibilityConfig.audio?.monoAudio || false,
    });

    return {
      visualFeatures,
      motorFeatures,
      audioFeatures,
      sessionId: accessibilityConfig.sessionId,
      setupAt: Date.now(),
    };
  }

  // Motion sickness prevention and comfort settings
  async manageComfortSettings(comfortConfig: ComfortSettingsConfig): Promise<ComfortSettingsSetup> {
    // Validate comfort configuration
    const validation = await this.validateComfortConfig(comfortConfig);
    if (!validation.valid) {
      throw new Error(`Invalid comfort configuration: ${validation.errors.join(', ')}`);
    }

    // Setup motion sickness prevention
    const motionSickness = await this.comfortManager.setupMotionSickness({
      vignetteStrength: comfortConfig.motionSickness?.vignetteStrength || 0.3,
      snapTurning: comfortConfig.motionSickness?.snapTurning || true,
      reducedMotion: comfortConfig.motionSickness?.reducedMotion || false,
      comfortFOV: comfortConfig.motionSickness?.comfortFOV || 90,
    });

    // Setup display comfort
    const displayComfort = await this.comfortManager.setupDisplayComfort({
      brightness: comfortConfig.display?.brightness || 0.8,
      IPD: comfortConfig.display?.IPD || 'auto',
      refreshRate: comfortConfig.display?.refreshRate || 90,
      antiAliasing: comfortConfig.display?.antiAliasing || true,
    });

    // Setup interaction comfort
    const interactionComfort = await this.comfortManager.setupInteractionComfort({
      reachDistance: comfortConfig.interaction?.reachDistance || 0.7,
      gestureSpeed: comfortConfig.interaction?.gestureSpeed || 1.0,
      hapticFeedback: comfortConfig.interaction?.hapticFeedback || true,
      autoCentering: comfortConfig.interaction?.autoCentering || true,
    });

    return {
      motionSickness,
      displayComfort,
      interactionComfort,
      sessionId: comfortConfig.sessionId,
      setupAt: Date.now(),
    };
  }

  private async checkWebXRSupport(): Promise<WebXRSupport> {
    if (!navigator.xr) {
      return { supported: false, reason: 'WebXR API not available' };
    }

    const immersiveVRSupported = await navigator.xr.isSessionSupported('immersive-vr');
    const immersiveARSupported = await navigator.xr.isSessionSupported('immersive-ar');
    const inlineSupported = await navigator.xr.isSessionSupported('inline');

    return {
      supported: immersiveVRSupported || immersiveARSupported || inlineSupported,
      immersiveVR: immersiveVRSupported,
      immersiveAR: immersiveARSupported,
      inline: inlineSupported,
      reason: 'WebXR fully supported',
    };
  }

  private async requestPermissions(permissions: XRPermissions): Promise<void> {
    // Request camera permission for AR
    if (permissions.camera && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'camera' });
    }

    // Request microphone permission
    if (permissions.microphone && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'microphone' });
    }

    // Request device orientation/motion permissions
    if (permissions.deviceOrientation && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'device-orientation' });
    }
  }

  private calculateSizeReduction(original: AssetOptimizationRequest, optimized: OptimizedAssets): number {
    let originalSize = 0;
    let optimizedSize = 0;

    // Calculate model sizes
    for (const model of original.models) {
      originalSize += model.size;
      if (optimized[model.id]) {
        optimizedSize += optimized[model.id].optimizedSize;
      }
    }

    // Calculate texture sizes
    for (const texture of original.textures) {
      originalSize += texture.size;
      if (optimized[texture.id]) {
        optimizedSize += optimized[texture.id].optimizedSize;
      }
    }

    // Calculate audio sizes
    for (const audio of original.audio) {
      originalSize += audio.size;
      if (optimized[audio.id]) {
        optimizedSize += optimized[audio.id].optimizedSize;
      }
    }

    return originalSize > 0 ? (originalSize - optimizedSize) / originalSize : 0;
  }
}

// WebXR Manager Implementation
export class WebXRManager {
  constructor(
    private deviceManager: XRDeviceManager,
    private sessionManager: XRSessionManager,
    private renderManager: XRRenderManager
  ) {}

  async initializeSession(config: XRSessionInitConfig): Promise<XRSession> {
    // Request XR session
    const session = await navigator.xr.requestSession(config.mode, config.options);
    
    // Setup render loop
    const renderLoop = await this.renderManager.setupRenderLoop(session);
    
    // Setup input sources
    const inputSources = await this.deviceManager.setupInputSources(session);
    
    // Configure reference space
    const referenceSpace = await this.setupReferenceSpace(session, config.referenceSpace || 'local');

    return {
      id: generateId(),
      session,
      renderLoop,
      inputSources,
      referenceSpace,
      initializedAt: Date.now(),
    };
  }

  private async setupReferenceSpace(session: XRSession, type: string): Promise<XRReferenceSpace> {
    return await session.requestReferenceSpace(type as XRReferenceSpaceType);
  }
}

// Performance Optimizer Implementation
export class XRPerformanceOptimizer {
  constructor(
    private frameAnalyzer: FrameAnalyzer,
    private qualityManager: QualityManager,
    private lodManager: LODManager
  ) {}

  async configure(session: XRSession, config: PerformanceConfig): Promise<PerformanceSetup> {
    // Setup frame analysis
    const frameAnalysis = await this.frameAnalyzer.setup({
      targetFPS: config.targetFPS || 60,
      adaptiveQuality: config.adaptiveQuality || true,
    });

    // Setup quality management
    const qualityManagement = await this.qualityManager.setup({
      initialQuality: config.initialQuality || 'high',
      adaptiveScaling: config.adaptiveScaling || true,
    });

    // Setup LOD management
    const lodManagement = await this.lodManager.setup({
      enabled: config.lodManagement || true,
      distanceThresholds: config.distanceThresholds || [1, 5, 15, 50],
    });

    return {
      frameAnalysis,
      qualityManagement,
      lodManagement,
      sessionId: session.id,
    };
  }

  async optimizeFrame(frame: XRFrame, context: OptimizationContext): Promise<FrameOptimization> {
    // Analyze current frame performance
    const frameMetrics = await this.frameAnalyzer.analyzeFrame(frame);
    
    // Adjust quality based on performance
    const qualityAdjustment = await this.qualityManager.adjustQuality(frameMetrics);
    
    // Update LOD based on distance and performance
    const lodUpdate = await this.lodManager.updateLOD(context.spatialData, frameMetrics);

    return {
      frameMetrics,
      qualityAdjustment,
      lodUpdate,
      optimizations: this.generateOptimizations(frameMetrics, qualityAdjustment, lodUpdate),
    };
  }

  private generateOptimizations(metrics: FrameMetrics, quality: QualityAdjustment, lod: LODUpdate): Optimization[] {
    const optimizations = [];

    if (metrics.fps < 60) {
      optimizations.push({
        type: 'reduce_quality',
        priority: 'high',
        description: 'Reduce render quality to maintain 60 FPS',
      });
    }

    if (quality.newLevel !== quality.currentLevel) {
      optimizations.push({
        type: 'quality_adjustment',
        priority: 'medium',
        description: `Adjust quality from ${quality.currentLevel} to ${quality.newLevel}`,
      });
    }

    if (lod.hasChanges) {
      optimizations.push({
        type: 'lod_update',
        priority: 'low',
        description: 'Update LOD levels based on distance',
      });
    }

    return optimizations;
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No AR/VR development standards
export class BasicXRApp {
  // BAD: No WebXR support check
  async startVR() {
    // BAD: No performance optimization
    // BAD: No spatial tracking
    // BAD: No accessibility features
    return this.render();
  }

  // BAD: No comfort settings
  // BAD: No asset optimization
  // BAD: No spatial audio
  // BAD: No gesture recognition
}
```
</example_bad>
