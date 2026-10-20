---
description: Run Streaming Architecture and Real-Time Processing Standards Check
globs: ["**/streaming/**/*.ts", "**/kafka/**/*.ts", "**/pulsar/**/*.ts", "**/realtime/**/*.ts"]
---
# Architecture: Streaming & Real-Time Processing Standards

<audit_rules>
- You MUST implement proper stream processing architecture with event sourcing patterns.
- You MUST configure proper message brokers with durability and ordering guarantees.
- You MUST implement proper backpressure handling to prevent system overload.
- You MUST ensure proper stream processing with exactly-once semantics where required.
- You MUST configure proper windowing strategies for time-based aggregations.
- You MUST implement proper state management for stream processing applications.
- You MUST ensure proper monitoring and alerting for stream processing pipelines.
- You MUST configure proper fault tolerance and recovery mechanisms.
- You MUST implement proper security and encryption for streaming data.
- You MUST ensure proper scalability and partitioning strategies for high throughput.
</audit_rules>

<example_good>
```typescript
// Streaming Architecture Implementation

export class StreamingOrchestrator {
  constructor(
    private messageBroker: MessageBroker,
    private streamProcessor: StreamProcessor,
    private stateStore: StateStore,
    private monitoringService: StreamingMonitoringService
  ) {}

  async createStreamPipeline(config: StreamPipelineConfig): Promise<StreamPipeline> {
    // Validate pipeline configuration
    await this.validatePipelineConfig(config);
    
    // Create stream topics
    const topics = await this.createTopics(config.topics);
    
    // Setup stream processors
    const processors = await this.setupProcessors(config.processors);
    
    // Configure state stores
    const stateStores = await this.setupStateStores(config.stateStores);
    
    // Setup monitoring
    await this.setupPipelineMonitoring(config, topics, processors);

    return {
      id: config.id,
      topics,
      processors,
      stateStores,
      config,
    };
  }

  async processRealTimeEvents(stream: EventStream): Promise<void> {
    // Setup consumer with proper configuration
    const consumer = await this.messageBroker.createConsumer({
      groupId: stream.consumerGroup,
      topics: [stream.topic],
      config: {
        enableAutoCommit: false,
        autoOffsetReset: 'earliest',
        sessionTimeoutMs: 30000,
        heartbeatIntervalMs: 3000,
        maxPollRecords: 100,
        maxPollIntervalMs: 300000,
      },
    });

    // Process events with backpressure handling
    await this.processEventsWithBackpressure(consumer, stream);
  }

  private async processEventsWithBackpressure(
    consumer: Consumer,
    stream: EventStream
  ): Promise<void> {
    let processing = true;
    const queue = new PriorityQueue<Event>();
    const maxQueueSize = 10000;
    const batchSize = 100;
    const processingTimeout = 5000;

    while (processing) {
      try {
        // Fetch messages with backpressure
        const messages = await consumer.fetch({
          maxMessages: batchSize,
          timeout: 1000,
        });

        // Check queue size for backpressure
        if (queue.size() >= maxQueueSize) {
          await this.handleBackpressure(stream);
          continue;
        }

        // Add messages to processing queue
        for (const message of messages) {
          const event = await this.deserializeEvent(message.value);
          queue.enqueue(event, event.priority);
        }

        // Process batch of events
        const batch = queue.dequeueBatch(batchSize);
        if (batch.length > 0) {
          await this.processBatch(batch, stream);
          
          // Commit offsets after successful processing
          await consumer.commitOffsets(batch.map(m => m.offset));
        }

      } catch (error) {
        await this.handleProcessingError(error, stream);
      }
    }
  }

  private async processBatch(events: Event[], stream: EventStream): Promise<ProcessingResult> {
    const startTime = Date.now();
    const results = [];

    // Process events with exactly-once semantics
    for (const event of events) {
      try {
        // Check for duplicate processing
        const processed = await this.stateStore.getEventProcessingStatus(event.id);
        if (processed) {
          continue;
        }

        // Process event
        const result = await this.streamProcessor.processEvent(event, stream);
        
        // Store processing status
        await this.stateStore.setEventProcessingStatus(event.id, 'processed');
        
        results.push(result);

      } catch (error) {
        // Handle processing error
        await this.stateStore.setEventProcessingStatus(event.id, 'failed');
        results.push({ eventId: event.id, success: false, error: error.message });
      }
    }

    const duration = Date.now() - startTime;
    
    // Record metrics
    await this.monitoringService.recordBatchMetrics({
      streamId: stream.id,
      batchSize: events.length,
      successCount: results.filter(r => r.success).length,
      errorCount: results.filter(r => !r.success).length,
      duration,
    });

    return {
      processed: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      duration,
    };
  }

  async createWindowedAggregation(config: WindowedAggregationConfig): Promise<WindowedAggregation> {
    const windowStrategy = this.createWindowStrategy(config.windowType);
    
    return {
      id: config.id,
      sourceTopic: config.sourceTopic,
      targetTopic: config.targetTopic,
      windowStrategy,
      aggregationFunction: config.aggregationFunction,
      triggerStrategy: config.triggerStrategy,
      stateStore: await this.stateStore.createWindowStateStore(config.id),
    };
  }

  private createWindowStrategy(windowType: WindowType): WindowStrategy {
    switch (windowType) {
      case 'tumbling':
        return new TumblingWindowStrategy();
      case 'sliding':
        return new SlidingWindowStrategy();
      case 'session':
        return new SessionWindowStrategy();
      case 'global':
        return new GlobalWindowStrategy();
      default:
        throw new Error(`Unsupported window type: ${windowType}`);
    }
  }

  async setupExactlyOnceProcessing(config: ExactlyOnceConfig): Promise<void> {
    // Configure transactional producer
    const producer = await this.messageBroker.createTransactionalProducer({
      transactionalId: config.transactionalId,
      enableIdempotence: true,
      acks: 'all',
      retries: 3,
    });

    // Setup consumer with read_committed isolation
    const consumer = await this.messageBroker.createConsumer({
      groupId: config.consumerGroup,
      isolationLevel: 'read_committed',
      enableAutoCommit: false,
    });

    return { producer, consumer };
  }

  async handleStreamFailure(stream: EventStream, failure: StreamFailure): Promise<void> {
    // Pause processing
    await this.pauseStreamProcessing(stream.id);
    
    // Analyze failure
    const analysis = await this.analyzeStreamFailure(failure);
    
    // Implement recovery strategy
    switch (analysis.recoveryStrategy) {
      case 'restart':
        await this.restartStreamProcessing(stream);
        break;
      case 'reset_offset':
        await this.resetStreamOffsets(stream, analysis.safeOffset);
        break;
      case 'scale_resources':
        await this.scaleStreamResources(stream, analysis.requiredResources);
        break;
      case 'manual_intervention':
        await this.requestManualIntervention(stream, analysis);
        break;
    }

    // Resume processing
    await this.resumeStreamProcessing(stream.id);
  }

  private async validatePipelineConfig(config: StreamPipelineConfig): Promise<void> {
    // Validate topic configurations
    for (const topic of config.topics) {
      if (!topic.name || !topic.partitions || !topic.replicationFactor) {
        throw new Error(`Invalid topic configuration: ${JSON.stringify(topic)}`);
      }
    }

    // Validate processor configurations
    for (const processor of config.processors) {
      if (!processor.name || !processor.inputTopic || !processor.outputTopic) {
        throw new Error(`Invalid processor configuration: ${JSON.stringify(processor)}`);
      }
    }

    // Validate state store configurations
    for (const stateStore of config.stateStores) {
      if (!stateStore.name || !stateStore.type || !stateStore.configuration) {
        throw new Error(`Invalid state store configuration: ${JSON.stringify(stateStore)}`);
      }
    }
  }

  private async createTopics(topics: TopicConfig[]): Promise<Topic[]> {
    const createdTopics = [];

    for (const topicConfig of topics) {
      const topic = await this.messageBroker.createTopic({
        name: topicConfig.name,
        partitions: topicConfig.partitions,
        replicationFactor: topicConfig.replicationFactor,
        config: {
          'retention.ms': topicConfig.retentionMs?.toString() || '604800000', // 7 days
          'segment.ms': topicConfig.segmentMs?.toString() || '86400000', // 1 day
          'cleanup.policy': topicConfig.cleanupPolicy || 'delete',
          'compression.type': topicConfig.compressionType || 'lz4',
          'max.message.bytes': topicConfig.maxMessageBytes?.toString() || '1048576', // 1MB
        },
      });

      createdTopics.push(topic);
    }

    return createdTopics;
  }

  private async setupProcessors(processors: ProcessorConfig[]): Promise<StreamProcessor[]> {
    const setupProcessors = [];

    for (const processorConfig of processors) {
      const processor = await this.streamProcessor.createProcessor({
        name: processorConfig.name,
        inputTopic: processorConfig.inputTopic,
        outputTopic: processorConfig.outputTopic,
        processingLogic: processorConfig.processingLogic,
        parallelism: processorConfig.parallelism || 1,
        config: processorConfig.config || {},
      });

      setupProcessors.push(processor);
    }

    return setupProcessors;
  }

  private async setupStateStores(stateStores: StateStoreConfig[]): Promise<StateStore[]> {
    const setupStores = [];

    for (const storeConfig of stateStores) {
      const stateStore = await this.stateStore.createStore({
        name: storeConfig.name,
        type: storeConfig.type,
        configuration: storeConfig.configuration,
        changelogTopic: `${storeConfig.name}-changelog`,
      });

      setupStores.push(stateStore);
    }

    return setupStores;
  }

  private async setupPipelineMonitoring(
    config: StreamPipelineConfig,
    topics: Topic[],
    processors: StreamProcessor[]
  ): Promise<void> {
    // Setup topic monitoring
    for (const topic of topics) {
      await this.monitoringService.setupTopicMonitoring(topic);
    }

    // Setup processor monitoring
    for (const processor of processors) {
      await this.monitoringService.setupProcessorMonitoring(processor);
    }

    // Setup pipeline-level monitoring
    await this.monitoringService.setupPipelineMonitoring(config.id);
  }

  private async handleBackpressure(stream: EventStream): Promise<void> {
    // Implement backpressure strategy
    switch (stream.backpressureStrategy) {
      case 'drop_oldest':
        await this.dropOldestEvents(stream);
        break;
      case 'buffer':
        await this.increaseBufferSize(stream);
        break;
      case 'throttle_producer':
        await this.throttleProducer(stream);
        break;
      case 'scale_consumer':
        await this.scaleConsumer(stream);
        break;
    }
  }

  private async deserializeEvent(data: Buffer): Promise<Event> {
    try {
      return JSON.parse(data.toString());
    } catch (error) {
      throw new Error(`Failed to deserialize event: ${error.message}`);
    }
  }
}

// Window Strategy Implementations
export class TumblingWindowStrategy implements WindowStrategy {
  createWindow(windowSize: number): Window {
    return {
      type: 'tumbling',
      size: windowSize,
      slide: windowSize,
      events: [],
      startTime: Date.now(),
    };
  }

  shouldTrigger(window: Window, event: Event): boolean {
    const eventTime = event.timestamp || Date.now();
    return eventTime >= window.startTime + window.size;
  }

  resetWindow(window: Window): void {
    window.events = [];
    window.startTime = Date.now();
  }
}

export class SlidingWindowStrategy implements WindowStrategy {
  createWindow(windowSize: number, slideSize: number): Window {
    return {
      type: 'sliding',
      size: windowSize,
      slide: slideSize,
      events: [],
      startTime: Date.now(),
    };
  }

  shouldTrigger(window: Window, event: Event): boolean {
    const eventTime = event.timestamp || Date.now();
    return eventTime >= window.startTime + window.slide;
  }

  resetWindow(window: Window): void {
    // Remove events outside the window
    const cutoffTime = Date.now() - window.size;
    window.events = window.events.filter(e => (e.timestamp || Date.now()) > cutoffTime);
    window.startTime = Date.now();
  }
}

// Stream Processor Implementation
export class StreamProcessor {
  async processEvent(event: Event, stream: EventStream): Promise<ProcessingResult> {
    const startTime = Date.now();

    try {
      // Apply business logic
      const result = await this.applyBusinessLogic(event, stream);

      // Produce output event
      if (result.outputEvent) {
        await this.produceOutputEvent(result.outputEvent, stream);
      }

      // Update state
      if (result.stateUpdate) {
        await this.updateState(event.id, result.stateUpdate, stream);
      }

      const duration = Date.now() - startTime;

      return {
        eventId: event.id,
        success: true,
        duration,
        outputEvent: result.outputEvent,
      };

    } catch (error) {
      const duration = Date.now() - startTime;

      return {
        eventId: event.id,
        success: false,
        duration,
        error: error.message,
      };
    }
  }

  private async applyBusinessLogic(event: Event, stream: EventStream): Promise<BusinessLogicResult> {
    // Implement stream-specific business logic
    switch (event.type) {
      case 'user_action':
        return await this.processUserAction(event, stream);
      case 'sensor_data':
        return await this.processSensorData(event, stream);
      case 'transaction':
        return await this.processTransaction(event, stream);
      default:
        throw new Error(`Unknown event type: ${event.type}`);
    }
  }

  private async processUserAction(event: Event, stream: EventStream): Promise<BusinessLogicResult> {
    // Process user action events
    const action = event.data as UserAction;
    
    // Validate action
    if (!action.userId || !action.action) {
      throw new Error('Invalid user action event');
    }

    // Process action
    const outputEvent: Event = {
      id: generateId(),
      type: 'action_processed',
      timestamp: Date.now(),
      data: {
        userId: action.userId,
        action: action.action,
        processedAt: Date.now(),
      },
    };

    return {
      outputEvent,
      stateUpdate: {
        key: `user:${action.userId}:actions`,
        value: action,
      },
    };
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No streaming architecture best practices
export class BasicEventProcessor {
  // BAD: No backpressure handling
  async processEvents(events: any[]) {
    // BAD: Synchronous processing
    for (const event of events) {
      await this.processEvent(event);
    }
  }

  // BAD: No exactly-once semantics
  // BAD: No windowing strategies
  // BAD: No state management
  // BAD: No fault tolerance
  // BAD: No monitoring
  // BAD: No proper error handling
}
```
</example_bad>
