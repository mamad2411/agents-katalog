---
description: Run AR/VR Development and Spatial Computing Standards Check
globs: ['**/arvr/**/*.ts', '**/spatial-computing/**/*.ts', '**/xr/**/*.ts', '**/webxr/**/*.ts']
---

# Future-Proof: AR/VR Development & Spatial Computing Standards

<audit_rules>

- You MUST implement proper WebXR API integration with browser compatibility checks.
- You MUST ensure proper spatial tracking and environment understanding for AR applications.
- You MUST implement proper performance optimization for 60+ FPS rendering on mobile devices.
- You MUST configure proper hand tracking and gesture recognition for natural interactions.
- You MUST ensure proper 3D asset optimization with compression and LOD management.
- You MUST implement proper spatial audio positioning and audio context management.
- You MUST configure proper cross-platform compatibility for ARCore, ARKit, and WebXR.
- You MUST ensure proper accessibility features for VR/AR applications.
- You MUST implement proper motion sickness prevention and comfort settings.
- You MUST ensure proper security and privacy for camera/microphone permissions.
  </audit_rules>

<example_good>

```typescript
// AR/VR Development Implementation

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

  async initializeXRSession(config: XRSessionConfig): Promise<XRSession> {
    // Check WebXR support
    const supportCheck = await this.checkWebXRSupport()
    if (!supportCheck.supported) {
      throw new Error(`WebXR not supported: ${supportCheck.reason}`)
    }

    // Request appropriate permissions
    await this.requestPermissions(config.permissions)

    // Initialize XR session
    const session = await this.xrEngine.initializeSession({
      mode: config.mode || 'immersive-vr',
      features: config.features || [],
      options: {
        requiredFeatures: config.requiredFeatures || [],
        optionalFeatures: config.optionalFeatures || [],
      },
    })

    // Setup spatial tracking
    const spatialTracking = await this.spatialTracker.setup(session, {
      trackingMode: config.spatialTracking?.mode || 'world-scale',
      environmentUnderstanding: config.spatialTracking?.environment || true,
      planeDetection: config.spatialTracking?.planeDetection || true,
    })

    // Setup performance optimization
    const performanceConfig = await this.performanceOptimizer.configure(session, {
      targetFPS: config.targetFPS || 60,
      adaptiveQuality: config.adaptiveQuality || true,
      lodManagement: config.lodManagement || true,
    })

    // Setup gesture recognition
    const gestureConfig = await this.gestureRecognizer.setup(session, {
      handTracking: config.gestures?.handTracking || true,
      gestureTypes: config.gestures?.types || ['pinch', 'grab', 'point'],
      confidence: config.gestures?.confidence || 0.7,
    })

    return {
      sessionId: session.id,
      mode: config.mode,
      spatialTracking,
      performanceConfig,
      gestureConfig,
      initializedAt: Date.now(),
    }
  }

  async renderXRScene(renderRequest: XRRenderRequest): Promise<XRRenderResult> {
    // Validate render request
    const validation = await this.validateRenderRequest(renderRequest)
    if (!validation.valid) {
      throw new Error(`Invalid render request: ${validation.errors.join(', ')}`)
    }

    // Get current frame
    const frame = await this.xrEngine.getCurrentFrame(renderRequest.sessionId)

    // Update spatial tracking
    const spatialData = await this.spatialTracker.update(frame)

    // Process gestures
    const gestures = await this.gestureRecognizer.processFrame(frame, spatialData)

    // Optimize rendering based on performance
    const optimization = await this.performanceOptimizer.optimizeFrame(frame, {
      spatialData,
      gestures,
      targetFPS: renderRequest.targetFPS,
    })

    // Render scene
    const renderResult = await this.renderScene({
      frame,
      spatialData,
      gestures,
      optimization,
      scene: renderRequest.scene,
    })

    // Apply spatial audio
    if (renderRequest.audio) {
      await this.spatialAudio.update(renderResult.audioContext, spatialData)
    }

    // Check comfort settings
    await this.comfortManager.applyComfortSettings(renderResult, frame)

    return {
      frameId: frame.id,
      renderTime: renderResult.renderTime,
      fps: renderResult.fps,
      spatialData,
      gestures,
      performanceMetrics: optimization.metrics,
      timestamp: Date.now(),
    }
  }

  async optimizeAssets(assetOptimization: AssetOptimizationRequest): Promise<OptimizedAssets> {
    // Validate asset optimization request
    const validation = await this.validateAssetOptimization(assetOptimization)
    if (!validation.valid) {
      throw new Error(`Invalid asset optimization: ${validation.errors.join(', ')}`)
    }

    const optimizedAssets = {}

    // Optimize 3D models
    for (const model of assetOptimization.models) {
      const optimizedModel = await this.optimizeModel(model, {
        compression: assetOptimization.compression || 'draco',
        lodLevels: assetOptimization.lodLevels || 3,
        targetSize: assetOptimization.targetModelSize || 1024 * 1024, // 1MB
      })
      optimizedAssets[model.id] = optimizedModel
    }

    // Optimize textures
    for (const texture of assetOptimization.textures) {
      const optimizedTexture = await this.optimizeTexture(texture, {
        compression: assetOptimization.textureCompression || 'astc',
        maxResolution: assetOptimization.maxTextureResolution || 2048,
        mipmaps: assetOptimization.mipmaps || true,
      })
      optimizedAssets[texture.id] = optimizedTexture
    }

    // Optimize audio
    for (const audio of assetOptimization.audio) {
      const optimizedAudio = await this.optimizeAudio(audio, {
        compression: assetOptimization.audioCompression || 'opus',
        spatialAudio: assetOptimization.spatialAudio || true,
        maxBitrate: assetOptimization.maxAudioBitrate || 128000,
      })
      optimizedAssets[audio.id] = optimizedAudio
    }

    return {
      assets: optimizedAssets,
      totalSizeReduction: this.calculateSizeReduction(assetOptimization, optimizedAssets),
      optimizationLevel: assetOptimization.optimizationLevel || 'medium',
      optimizedAt: Date.now(),
    }
  }

  async setupSpatialAudio(audioConfig: SpatialAudioConfig): Promise<SpatialAudioSetup> {
    // Validate audio configuration
    const validation = await this.validateAudioConfig(audioConfig)
    if (!validation.valid) {
      throw new Error(`Invalid audio configuration: ${validation.errors.join(', ')}`)
    }

    // Initialize spatial audio engine
    const audioEngine = await this.spatialAudio.initialize({
      sessionId: audioConfig.sessionId,
      audioContextOptions: {
        sampleRate: audioConfig.sampleRate || 48000,
        bufferSize: audioConfig.bufferSize || 512,
      },
      spatialModel: audioConfig.spatialModel || 'hrtf',
    })

    // Setup audio sources
    const audioSources = []
    for (const source of audioConfig.sources) {
      const audioSource = await this.spatialAudio.createSource(audioEngine, {
        position: source.position,
        orientation: source.orientation,
        cone: source.cone,
        distanceModel: source.distanceModel || 'inverse',
        maxDistance: source.maxDistance || 100,
        refDistance: source.refDistance || 1,
        rolloffFactor: source.rolloffFactor || 1,
      })
      audioSources.push(audioSource)
    }

    // Setup audio listener
    const listener = await this.spatialAudio.setupListener(audioEngine, {
      position: { x: 0, y: 0, z: 0 },
      orientation: { x: 0, y: 0, z: 0, w: 1 },
      up: { x: 0, y: 1, z: 0 },
    })

    return {
      audioEngine,
      audioSources,
      listener,
      sessionId: audioConfig.sessionId,
      setupAt: Date.now(),
    }
  }

  async implementAccessibility(
    accessibilityConfig: XRAccessibilityConfig
  ): Promise<AccessibilitySetup> {
    // Validate accessibility configuration
    const validation = await this.validateAccessibilityConfig(accessibilityConfig)
    if (!validation.valid) {
      throw new Error(`Invalid accessibility configuration: ${validation.errors.join(', ')}`)
    }

    // Setup visual accessibility features
    const visualFeatures = await this.accessibilityManager.setupVisualFeatures({
      highContrast: accessibilityConfig.visual?.highContrast || false,
      textScaling: accessibilityConfig.visual?.textScaling || 1.0,
      colorBlindnessMode: accessibilityConfig.visual?.colorBlindnessMode || 'none',
      reducedMotion: accessibilityConfig.visual?.reducedMotion || false,
    })

    // Setup motor accessibility features
    const motorFeatures = await this.accessibilityManager.setupMotorFeatures({
      simplifiedControls: accessibilityConfig.motor?.simplifiedControls || false,
      voiceControl: accessibilityConfig.motor?.voiceControl || false,
      eyeTracking: accessibilityConfig.motor?.eyeTracking || false,
      gestureSensitivity: accessibilityConfig.motor?.gestureSensitivity || 1.0,
    })

    // Setup audio accessibility features
    const audioFeatures = await this.accessibilityManager.setupAudioFeatures({
      visualIndicators: accessibilityConfig.audio?.visualIndicators || false,
      subtitles: accessibilityConfig.audio?.subtitles || false,
      volumeNormalization: accessibilityConfig.audio?.volumeNormalization || true,
      monoAudio: accessibilityConfig.audio?.monoAudio || false,
    })

    return {
      visualFeatures,
      motorFeatures,
      audioFeatures,
      sessionId: accessibilityConfig.sessionId,
      setupAt: Date.now(),
    }
  }

  async manageComfortSettings(comfortConfig: ComfortSettingsConfig): Promise<ComfortSettingsSetup> {
    // Validate comfort configuration
    const validation = await this.validateComfortConfig(comfortConfig)
    if (!validation.valid) {
      throw new Error(`Invalid comfort configuration: ${validation.errors.join(', ')}`)
    }

    // Setup motion sickness prevention
    const motionSickness = await this.comfortManager.setupMotionSickness({
      vignetteStrength: comfortConfig.motionSickness?.vignetteStrength || 0.3,
      snapTurning: comfortConfig.motionSickness?.snapTurning || true,
      reducedMotion: comfortConfig.motionSickness?.reducedMotion || false,
      comfortFOV: comfortConfig.motionSickness?.comfortFOV || 90,
    })

    // Setup display comfort
    const displayComfort = await this.comfortManager.setupDisplayComfort({
      brightness: comfortConfig.display?.brightness || 0.8,
      IPD: comfortConfig.display?.IPD || 'auto',
      refreshRate: comfortConfig.display?.refreshRate || 90,
      antiAliasing: comfortConfig.display?.antiAliasing || true,
    })

    // Setup interaction comfort
    const interactionComfort = await this.comfortManager.setupInteractionComfort({
      reachDistance: comfortConfig.interaction?.reachDistance || 0.7,
      gestureSpeed: comfortConfig.interaction?.gestureSpeed || 1.0,
      hapticFeedback: comfortConfig.interaction?.hapticFeedback || true,
      autoCentering: comfortConfig.interaction?.autoCentering || true,
    })

    return {
      motionSickness,
      displayComfort,
      interactionComfort,
      sessionId: comfortConfig.sessionId,
      setupAt: Date.now(),
    }
  }

  private async checkWebXRSupport(): Promise<WebXRSupport> {
    if (!navigator.xr) {
      return { supported: false, reason: 'WebXR API not available' }
    }

    const immersiveVRSupported = await navigator.xr.isSessionSupported('immersive-vr')
    const immersiveARSupported = await navigator.xr.isSessionSupported('immersive-ar')
    const inlineSupported = await navigator.xr.isSessionSupported('inline')

    return {
      supported: immersiveVRSupported || immersiveARSupported || inlineSupported,
      immersiveVR: immersiveVRSupported,
      immersiveAR: immersiveARSupported,
      inline: inlineSupported,
      reason: 'WebXR fully supported',
    }
  }

  private async requestPermissions(permissions: XRPermissions): Promise<void> {
    // Request camera permission for AR
    if (permissions.camera && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'camera' })
    }

    // Request microphone permission
    if (permissions.microphone && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'microphone' })
    }

    // Request device orientation/motion permissions
    if (permissions.deviceOrientation && 'permissions' in navigator) {
      await navigator.permissions.query({ name: 'device-orientation' })
    }
  }

  private async renderScene(renderConfig: SceneRenderConfig): Promise<SceneRenderResult> {
    const startTime = performance.now()

    // Update scene graph
    await this.updateSceneGraph(renderConfig.scene, renderConfig.spatialData)

    // Cull objects outside view frustum
    const culledObjects = await this.frustumCull(renderConfig.scene, renderConfig.frame)

    // Apply LOD selection
    const lodObjects = await this.applyLOD(culledObjects, renderConfig.optimization)

    // Render objects
    const renderPasses = await this.executeRenderPasses(lodObjects, renderConfig.frame)

    const endTime = performance.now()

    return {
      renderTime: endTime - startTime,
      fps: 1000 / (endTime - startTime),
      renderPasses,
      culledObjects: culledObjects.length,
      lodObjects: lodObjects.length,
    }
  }

  private async optimizeModel(
    model: XRModel,
    config: ModelOptimizationConfig
  ): Promise<OptimizedModel> {
    // Apply mesh optimization
    const optimizedMesh = await this.optimizeMesh(model.mesh, {
      decimation: config.decimation || 0.5,
      mergeVertices: true,
      removeUnusedVertices: true,
    })

    // Apply texture optimization
    const optimizedTextures = await this.optimizeModelTextures(model.textures, {
      compression: config.textureCompression || 'astc',
      maxResolution: config.maxTextureResolution || 2048,
    })

    // Generate LOD levels
    const lodLevels = await this.generateLODLevels(optimizedMesh, config.lodLevels)

    return {
      ...model,
      mesh: optimizedMesh,
      textures: optimizedTextures,
      lodLevels,
      originalSize: model.size,
      optimizedSize: optimizedMesh.size + optimizedTextures.reduce((sum, t) => sum + t.size, 0),
    }
  }

  private async optimizeTexture(
    texture: XRTexture,
    config: TextureOptimizationConfig
  ): Promise<OptimizedTexture> {
    // Resize texture if needed
    const resizedTexture = await this.resizeTexture(texture, config.maxResolution)

    // Apply compression
    const compressedTexture = await this.compressTexture(resizedTexture, config.compression)

    // Generate mipmaps if needed
    const mipmappedTexture = config.mipmaps
      ? await this.generateMipmaps(compressedTexture)
      : compressedTexture

    return {
      ...texture,
      data: mipmappedTexture,
      originalSize: texture.size,
      optimizedSize: mipmappedTexture.size,
      compression: config.compression,
    }
  }

  private async optimizeAudio(
    audio: XRAudio,
    config: AudioOptimizationConfig
  ): Promise<OptimizedAudio> {
    // Apply compression
    const compressedAudio = await this.compressAudio(audio, config.compression)

    // Setup spatial audio parameters
    const spatialAudio = await this.setupSpatialAudioParameters(compressedAudio, {
      spatialModel: config.spatialModel || 'hrtf',
      distanceModel: config.distanceModel || 'inverse',
    })

    return {
      ...audio,
      data: compressedAudio,
      spatialAudio,
      originalSize: audio.size,
      optimizedSize: compressedAudio.size,
      compression: config.compression,
    }
  }

  private calculateSizeReduction(
    original: AssetOptimizationRequest,
    optimized: OptimizedAssets
  ): number {
    let originalSize = 0
    let optimizedSize = 0

    // Calculate model sizes
    for (const model of original.models) {
      originalSize += model.size
      if (optimized[model.id]) {
        optimizedSize += optimized[model.id].optimizedSize
      }
    }

    // Calculate texture sizes
    for (const texture of original.textures) {
      originalSize += texture.size
      if (optimized[texture.id]) {
        optimizedSize += optimized[texture.id].optimizedSize
      }
    }

    // Calculate audio sizes
    for (const audio of original.audio) {
      originalSize += audio.size
      if (optimized[audio.id]) {
        optimizedSize += optimized[audio.id].optimizedSize
      }
    }

    return originalSize > 0 ? (originalSize - optimizedSize) / originalSize : 0
  }

  private async updateSceneGraph(scene: XRScene, spatialData: SpatialData): Promise<void> {
    // Update object positions based on spatial tracking
    for (const object of scene.objects) {
      if (object.spatialAnchored && spatialData.anchors) {
        const anchor = spatialData.anchors.find((a) => a.id === object.anchorId)
        if (anchor) {
          object.position = anchor.position
          object.orientation = anchor.orientation
        }
      }
    }

    // Update physics simulation
    if (scene.physics) {
      await this.updatePhysics(scene, spatialData)
    }

    // Update animations
    if (scene.animations) {
      await this.updateAnimations(scene, spatialData)
    }
  }

  private async frustumCull(scene: XRScene, frame: XRFrame): Promise<XRObject[]> {
    const viewTransform = frame.getViewerPose(this.xrEngine.referenceSpace)
    const frustum = this.calculateFrustum(viewTransform)

    return scene.objects.filter((object) => this.isInFrustum(object, frustum))
  }

  private async applyLOD(
    objects: XRObject[],
    optimization: PerformanceOptimization
  ): Promise<XRObject[]> {
    return objects.map((object) => {
      if (object.lodLevels) {
        const lod = this.selectLOD(
          object,
          optimization.cameraDistance,
          optimization.performanceLevel
        )
        return { ...object, currentLOD: lod }
      }
      return object
    })
  }

  private selectLOD(object: XRObject, cameraDistance: number, performanceLevel: number): number {
    if (!object.lodLevels || object.lodLevels.length === 0) return 0

    // Select LOD based on distance and performance
    const distanceLOD = this.calculateDistanceLOD(object, cameraDistance)
    const performanceLOD = this.calculatePerformanceLOD(object, performanceLevel)

    return Math.max(distanceLOD, performanceLOD)
  }

  private calculateDistanceLOD(object: XRObject, cameraDistance: number): number {
    const lodDistances = [1, 5, 15, 50] // Distance thresholds for each LOD level

    for (let i = lodDistances.length - 1; i >= 0; i--) {
      if (cameraDistance <= lodDistances[i]) {
        return i
      }
    }

    return object.lodLevels.length - 1 // Use lowest LOD
  }

  private calculatePerformanceLOD(object: XRObject, performanceLevel: number): number {
    if (performanceLevel > 0.8) return 0 // High performance - use highest LOD
    if (performanceLevel > 0.6) return 1 // Medium performance
    if (performanceLevel > 0.4) return 2 // Low performance
    return object.lodLevels.length - 1 // Very low performance - use lowest LOD
  }

  private isInFrustum(object: XRObject, frustum: Frustum): boolean {
    // Simple bounding sphere test against frustum
    const sphere = object.boundingSphere
    return this.sphereIntersectsFrustum(sphere, frustum)
  }

  private sphereIntersectsFrustum(sphere: BoundingSphere, frustum: Frustum): boolean {
    // Implement sphere-frustum intersection test
    // This is a simplified implementation
    return true // Placeholder
  }

  private calculateFrustum(viewTransform: XRViewTransform): Frustum {
    // Calculate view frustum from view transform
    // This is a simplified implementation
    return {
      near: 0.1,
      far: 1000,
      fov: 90,
      aspect: 16 / 9,
    }
  }
}

// XR Engine Implementation
export class XREngine {
  private session: XRSession | null = null
  private referenceSpace: XRReferenceSpace | null = null

  async initializeSession(config: XRSessionConfig): Promise<XRSession> {
    try {
      this.session = await navigator.xr.requestSession(config.mode, config.options)

      // Setup reference space
      this.referenceSpace = await this.session.requestReferenceSpace('local')

      // Setup render loop
      this.setupRenderLoop()

      return {
        id: generateId(),
        mode: config.mode,
        session: this.session,
        referenceSpace: this.referenceSpace,
        initializedAt: Date.now(),
      }
    } catch (error) {
      throw new Error(`Failed to initialize XR session: ${error.message}`)
    }
  }

  async getCurrentFrame(sessionId: string): Promise<XRFrame> {
    if (!this.session) {
      throw new Error('No active XR session')
    }

    try {
      const frame = await this.session.requestAnimationFrame(this.onXRFrame.bind(this))
      return {
        id: generateId(),
        session: this.session,
        timestamp: performance.now(),
        pose: this.session.requestAnimationFrame(this.onXRFrame),
      }
    } catch (error) {
      throw new Error(`Failed to get XR frame: ${error.message}`)
    }
  }

  private setupRenderLoop(): void {
    if (this.session) {
      this.session.requestAnimationFrame(this.onXRFrame.bind(this))
    }
  }

  private onXRFrame(time: DOMHighResTimeStamp, frame: XRFrame): void {
    // Process frame
    this.processFrame(frame)

    // Request next frame
    if (this.session) {
      this.session.requestAnimationFrame(this.onXRFrame.bind(this))
    }
  }

  private processFrame(frame: XRFrame): void {
    // Get viewer pose
    const pose = frame.getViewerPose(this.referenceSpace)

    if (pose) {
      // Update camera and render
      this.updateCamera(pose)
      this.render(frame)
    }
  }

  private updateCamera(pose: XRViewerPose): void {
    // Update camera based on pose
    // Implementation depends on rendering engine
  }

  private render(frame: XRFrame): void {
    // Render the frame
    // Implementation depends on rendering engine
  }
}

// Spatial Tracking Engine Implementation
export class SpatialTrackingEngine {
  private anchors: Map<string, XRAnchor> = new Map()
  private planes: Map<string, XRPlane> = new Map()

  async setup(session: XRSession, config: SpatialTrackingConfig): Promise<SpatialTrackingSetup> {
    const tracking = {
      session,
      anchors: new Map(),
      planes: new Map(),
      config,
      setupAt: Date.now(),
    }

    // Setup plane detection if enabled
    if (config.planeDetection) {
      await this.setupPlaneDetection(session)
    }

    // Setup anchor tracking
    await this.setupAnchorTracking(session)

    return tracking
  }

  async update(frame: XRFrame): Promise<SpatialData> {
    const spatialData: SpatialData = {
      anchors: [],
      planes: [],
      trackingState: 'tracking',
      timestamp: Date.now(),
    }

    // Update anchors
    for (const [id, anchor] of this.anchors) {
      const pose = frame.getPose(anchor.anchorSpace, this.referenceSpace)
      if (pose) {
        spatialData.anchors.push({
          id,
          position: pose.transform.position,
          orientation: pose.transform.orientation,
        })
      }
    }

    // Update planes
    if (this.planes.size > 0) {
      for (const [id, plane] of this.planes) {
        const pose = frame.getPose(plane.planeSpace, this.referenceSpace)
        if (pose) {
          spatialData.planes.push({
            id,
            position: pose.transform.position,
            orientation: pose.transform.orientation,
            polygon: plane.polygon,
          })
        }
      }
    }

    return spatialData
  }

  private async setupPlaneDetection(session: XRSession): Promise<void> {
    // Setup plane detection
    // Implementation depends on WebXR plane detection API
  }

  private async setupAnchorTracking(session: XRSession): Promise<void> {
    // Setup anchor tracking
    // Implementation depends on WebXR anchor API
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
    return this.render()
  }

  // BAD: No comfort settings
  // BAD: No asset optimization
  // BAD: No spatial audio
  // BAD: No gesture recognition
}
```

</example_bad>
