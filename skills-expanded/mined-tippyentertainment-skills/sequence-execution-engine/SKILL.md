---
name: sequence-execution-engine
description: A TypeScript library for executing sequential workflows with configurable delays, retry logic, caching, and comprehensive tracing
target: https://tasking.tech
---

# Provided by TippyEntertainment

# Sequence Execution Engine with Delay Management

A TypeScript library for executing sequential workflows with configurable delays, retry logic, caching, and comprehensive tracing.

## Features

- **Sequential Step Execution**: Execute steps in order with automatic input/output chaining
- **Delay Management**: Pre-step and post-step delays with configurable timing
- **Retry Logic**: Automatic retries with exponential backoff
- **Timeout Handling**: Per-step and global timeout support
- **Caching**: Optional result caching with TTL
- **Conditional Execution**: Skip steps based on conditions
- **Parallel Execution**: Execute multiple sequences in parallel
- **Comprehensive Tracing**: Full execution trace with timing data
- **Lifecycle Callbacks**: onStart, onComplete, onError hooks

## Installation

```typescript
import { SequenceEngine, SequenceStep, SequenceConfig, createSequence, createDelayedSequence } from './sequenceEngine';
```

## Basic Usage

### Simple Sequence

```typescript
// Create a simple sequence
const engine = new SequenceEngine({
  id: 'user-onboarding',
  name: 'User Onboarding Workflow'
});

// Add steps
engine.addStep({
  id: 'validate-email',
  name: 'Validate Email',
  execute: async (input) => {
    // Validation logic
    return { valid: true, email: input.email };
  },
  delay: 100 // 100ms delay before execution
});

engine.addStep({
  id: 'create-account',
  name: 'Create Account',
  execute: async (input) => {
    // Account creation logic
    return { userId: '123', ...input };
  },
  delay: 200,
  maxRetries: 3,
  retryDelay: 1000
});

engine.addStep({
  id: 'send-welcome',
  name: 'Send Welcome Email',
  execute: async (input) => {
    // Send email logic
    return { sent: true, userId: input.userId };
  },
  postDelay: 500 // Delay after execution
});

// Execute
const result = await engine.execute({ email: 'user@example.com' });
console.log(result.success); // true
console.log(result.output); // { sent: true, userId: '123' }
```

### Delayed Sequence

```typescript
// Create sequence with delays between steps
const engine = createDelayedSequence([
  { fn: async (input) => { /* step 1 */ }, delay: 100 },
  { fn: async (input) => { /* step 2 */ }, delay: 200 },
  { fn: async (input) => { /* step 3 */ }, delay: 300 }
], {
  id: 'delayed-workflow',
  name: 'Delayed Workflow'
});

const result = await engine.execute(initialInput);
```

### Retry with Exponential Backoff

```typescript
engine.addStep({
  id: 'api-call',
  name: 'External API Call',
  execute: async (input) => {
    const response = await fetch(input.url);
    return response.json();
  },
  maxRetries: 5,
  retryDelay: 1000,      // Start with 1 second
  retryBackoff: 2,      // Double each retry: 1s, 2s, 4s, 8s, 16s
  timeout: 30000        // 30 second timeout
});
```

### Conditional Execution

```typescript
engine.addStep({
  id: 'premium-feature',
  name: 'Premium Feature Setup',
  execute: async (input) => {
    // Premium setup logic
    return { premium: true };
  },
  condition: (input, context) => {
    // Only execute if user is premium
    return input.userType === 'premium';
  }
});
```

### Parallel Execution

```typescript
const engine = new SequenceEngine({
  id: 'batch-processor',
  name: 'Batch Processor',
  maxParallel: 5 // Process 5 items at a time
});

// Execute multiple inputs in parallel
const results = await engine.executeParallel([
  { id: 1 },
  { id: 2 },
  { id: 3 },
  // ... more items
]);
```

### Caching

```typescript
const engine = new SequenceEngine({
  id: 'cached-workflow',
  name: 'Cached Workflow',
  enableCache: true,
  cacheTTL: 60000 // 1 minute cache
});

// First call executes the step
const result1 = await engine.execute({ key: 'value' });

// Second call within TTL returns cached result
const result2 = await engine.execute({ key: 'value' });
console.log(result2.stepResults[0].cached); // true
```

### Lifecycle Callbacks

```typescript
engine.addStep({
  id: 'process-payment',
  name: 'Process Payment',
  execute: async (input) => {
    // Payment logic
    return { success: true };
  },
  onStart: (step, input) => {
    console.log(`Starting ${step.name}`);
  },
  onComplete: (step, output, duration) => {
    console.log(`Completed ${step.name} in ${duration}ms`);
  },
  onError: (step, error, attempt) => {
    console.error(`Error on attempt ${attempt}: ${error.message}`);
  }
});
```

## API Reference

### SequenceEngine

```typescript
class SequenceEngine {
  constructor(config: SequenceConfig);
  
  addStep<TInput, TOutput>(step: SequenceStep<TInput, TOutput>): this;
  addSteps(steps: SequenceStep[]): this;
  
  execute<TInput, TOutput>(initialInput?: TInput, metadata?: Record<string, any>): Promise<SequenceResult>;
  executeParallel<TInput>(inputs: TInput[], metadata?: Record<string, any>): Promise<SequenceResult[]>;
  
  getTrace(): TraceNode[];
  clearCache(): void;
  getStep(stepId: string): SequenceStep | undefined;
  getSteps(): SequenceStep[];
}
```

### SequenceStep

```typescript
interface SequenceStep<TInput = any, TOutput = any> {
  id: string;                              // Unique identifier
  name: string;                            // Human-readable name
  execute: (input, context) => TOutput;    // Step function
  delay?: number;                          // Pre-execution delay (ms)
  postDelay?: number;                      // Post-execution delay (ms)
  maxRetries?: number;                     // Retry attempts (default: 0)
  retryDelay?: number;                     // Delay between retries (ms)
  retryBackoff?: number;                   // Exponential backoff multiplier
  timeout?: number;                        // Step timeout (ms)
  optional?: boolean;                      // Skip on failure
  condition?: (input, context) => boolean; // Execution condition
  onStart?: (step, input) => void;         // Pre-execution callback
  onComplete?: (step, output, duration) => void;  // Success callback
  onError?: (step, error, attempt) => void;       // Error callback
}
```

### SequenceConfig

```typescript
interface SequenceConfig {
  id: string;                              // Sequence identifier
  name: string;                            // Sequence name
  description?: string;                   // Description
  defaultDelay?: number;                   // Default pre-delay (ms)
  defaultTimeout?: number;                 // Default timeout (ms)
  defaultMaxRetries?: number;              // Default retry count
  stopOnError?: boolean;                   // Stop on failure (default: true)
  enableCache?: boolean;                   // Enable caching (default: false)
  cacheTTL?: number;                       // Cache TTL (ms, default: 60000)
  maxParallel?: number;                    // Max parallel executions (default: 1)
  onSequenceStart?: (config) => void;      // Start callback
  onSequenceComplete?: (result) => void;   // Complete callback
  onSequenceError?: (error, step?) => void; // Error callback
}
```

### SequenceResult

```typescript
interface SequenceResult {
  sequenceId: string;          // Sequence ID
  executionId: string;         // Unique execution ID
  success: boolean;            // All steps completed
  totalDuration: number;       // Total time (ms)
  startTime: number;          // Start timestamp
  endTime: number;            // End timestamp
  stepResults: StepResult[];   // All step results
  output: any;                 // Final output
  error?: Error;              // Error if failed
  failedStep?: string;        // Failed step ID
  trace: TraceNode[];          // Execution trace
}
```

## Utility Functions

```typescript
// Sleep for specified duration
await sleep(1000); // Sleep for 1 second

// Generate unique ID
const id = generateId(); // "1697123456789-abc123def"

// Calculate backoff delay
const delay = calculateBackoff(1000, 3, 2); // 1000 * 2^2 = 4000ms
```

## Example: Complete Workflow

```typescript
import { SequenceEngine, SequenceStep } from './sequenceEngine';

// Define workflow
const workflow = new SequenceEngine({
  id: 'order-processing',
  name: 'Order Processing Workflow',
  defaultTimeout: 30000,
  stopOnError: true,
  onSequenceStart: (config) => {
    console.log(`Starting workflow: ${config.name}`);
  },
  onSequenceComplete: (result) => {
    console.log(`Workflow completed in ${result.totalDuration}ms`);
  }
});

// Step 1: Validate order
workflow.addStep({
  id: 'validate',
  name: 'Validate Order',
  execute: async (input) => {
    // Validation logic
    return { valid: true, order: input };
  },
  delay: 100
});

// Step 2: Check inventory
workflow.addStep({
  id: 'inventory',
  name: 'Check Inventory',
  execute: async (input) => {
    // Inventory check
    return { ...input, inStock: true };
  },
  maxRetries: 3,
  retryDelay: 500
});

// Step 3: Process payment
workflow.addStep({
  id: 'payment',
  name: 'Process Payment',
  execute: async (input) => {
    // Payment processing
    return { ...input, paid: true };
  },
  maxRetries: 5,
  retryDelay: 1000,
  retryBackoff: 2,
  timeout: 15000
});

// Step 4: Send confirmation
workflow.addStep({
  id: 'confirm',
  name: 'Send Confirmation',
  execute: async (input) => {
    // Send email/notification
    return { ...input, confirmed: true };
  },
  postDelay: 200
});

// Execute workflow
const result = await workflow.execute({
  orderId: 'ORD-123',
  items: ['item1', 'item2'],
  total: 99.99
});

console.log(result.success); // true
console.log(result.output);   // { valid: true, inStock: true, paid: true, confirmed: true }
```

## Use Cases

1. **User Onboarding**: Multi-step registration with email verification, profile setup, welcome emails
2. **Order Processing**: Validate → Inventory → Payment → Fulfillment → Notification
3. **Data Pipeline**: Extract → Transform → Validate → Load with retry logic
4. **API Orchestration**: Chain multiple API calls with delays and error handling
5. **Background Jobs**: Sequential task execution with progress tracking
6. **Testing**: Step-by-step test execution with detailed tracing

## Best Practices

1. **Use meaningful IDs**: Choose descriptive step IDs for debugging
2. **Set appropriate timeouts**: Prevent hanging on slow operations
3. **Implement retry logic**: Use exponential backoff for external calls
4. **Use caching wisely**: Cache expensive operations, not dynamic data
5. **Handle errors gracefully**: Use optional steps for non-critical operations
6. **Log with callbacks**: Use lifecycle callbacks for monitoring
7. **Test delays**: Ensure delays are appropriate for your use case
