---
alwaysApply: false
---
# Performance Rules: Stay 6x Faster Than Gemini CLI

## 🚨 PERFORMANCE KILLERS - NEVER DO THESE

### Synchronous Operations (Gemini CLI Mistake)
```typescript
// ❌ FORBIDDEN - Blocks event loop like Gemini CLI
import { execSync, readFileSync } from 'fs';
const result = execSync('command');  // Blocks everything
const content = readFileSync('file.txt');  // Blocks everything

// ✅ REQUIRED - Async operations
import { exec } from 'child_process';
import { readFile } from 'fs/promises';
const result = await exec('command');
const content = await readFile('file.txt');
```

### Console Pollution (Gemini CLI Has 100+)
```typescript
// ❌ FORBIDDEN - Slows down execution
console.log('debug info');
console.error('error details');
console.warn('warning message');

// ✅ REQUIRED - Use proper logging
import { logger } from '../utils/logger.js';
logger.debug('debug info');
logger.error('error details');
logger.warn('warning message');
```

### Memory Leaks (Gemini CLI Pattern)
```typescript
// ❌ FORBIDDEN - Memory leaks like Gemini CLI
let globalCache = new Map();  // Never cleaned up
setInterval(() => {}, 1000);  // Never cleared

// ✅ REQUIRED - Proper cleanup
class CacheManager {
  private cache = new Map();
  private cleanupInterval: NodeJS.Timeout;
  
  constructor() {
    this.cleanupInterval = setInterval(() => this.cleanup(), 60000);
  }
  
  cleanup(): void {
    this.cache.clear();
  }
  
  destroy(): void {
    clearInterval(this.cleanupInterval);
    this.cache.clear();
  }
}
```

## ⚡ PERFORMANCE PATTERNS - ALWAYS USE THESE

### 1. Lazy Loading (Beat Gemini CLI Startup)
```typescript
// ✅ REQUIRED - Lazy load heavy modules
async function getAIClient(): Promise<UnifiedClaudeClient> {
  // Only import when needed
  const { createUnifiedClient } = await import('../ai/unified-client.js');
  return createUnifiedClient();
}

// ❌ WRONG - Heavy imports at startup like Gemini CLI
import { heavyModule } from './heavy-module.js';  // Slows startup
```

### 2. Efficient Data Structures
```typescript
// ✅ REQUIRED - Use appropriate data structures
const userLookup = new Map<string, User>();  // O(1) lookup
const uniqueItems = new Set<string>();       // O(1) contains

// ❌ WRONG - Inefficient structures like Gemini CLI
const userLookup: User[] = [];  // O(n) lookup
const uniqueItems: string[] = [];  // O(n) contains check
```

### 3. Stream Processing (Large Files)
```typescript
// ✅ REQUIRED - Stream large data
import { createReadStream } from 'fs';
import { pipeline } from 'stream/promises';

async function processLargeFile(filePath: string): Promise<void> {
  const readStream = createReadStream(filePath);
  await pipeline(
    readStream,
    new TransformStream(),
    new WritableStream()
  );
}

// ❌ WRONG - Load everything into memory like Gemini CLI
const content = await readFile(filePath);  // Memory intensive
```

### 4. Debounced Operations
```typescript
// ✅ REQUIRED - Debounce expensive operations
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): T {
  let timeout: NodeJS.Timeout;
  return ((...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  }) as T;
}

const debouncedSave = debounce(saveConfig, 1000);
```

### 5. Efficient Async Patterns
```typescript
// ✅ REQUIRED - Parallel execution when possible
const [userProfile, userSettings, userHistory] = await Promise.all([
  fetchUserProfile(userId),
  fetchUserSettings(userId),
  fetchUserHistory(userId)
]);

// ❌ WRONG - Sequential execution like Gemini CLI
const userProfile = await fetchUserProfile(userId);
const userSettings = await fetchUserSettings(userId);  // Waits unnecessarily
const userHistory = await fetchUserHistory(userId);    // Waits unnecessarily
```

## 📊 PERFORMANCE MONITORING

### Startup Time Targets
```bash
# Target: <50ms (vs Gemini CLI's ~200ms)
time node dist/cli.js --version

# If > 50ms, check these:
# 1. Heavy imports at startup
# 2. Synchronous operations
# 3. Large dependency tree
```

### Memory Usage Targets
```bash
# Target: <40MB baseline (vs Gemini CLI's ~80MB)
node --max-old-space-size=100 dist/cli.js test

# If > 40MB, check these:
# 1. Memory leaks
# 2. Large object retention
# 3. Inefficient data structures
```

### Bundle Size Targets
```bash
# Target: <5MB (vs Gemini CLI's ~20MB+)
du -sh dist/

# If > 5MB, check these:
# 1. Unnecessary dependencies
# 2. Large assets included
# 3. Poor tree-shaking
```

## 🔧 OPTIMIZATION TECHNIQUES

### 1. Function Optimization
```typescript
// ✅ OPTIMIZED - Early returns
function processUser(user: User | null): ProcessResult {
  if (!user) {
    return { success: false, reason: 'No user' };
  }
  
  if (!user.isActive) {
    return { success: false, reason: 'Inactive user' };
  }
  
  // Continue processing only if needed
  return processActiveUser(user);
}

// ❌ SLOW - Deep nesting like Gemini CLI
function processUser(user: User | null): ProcessResult {
  if (user) {
    if (user.isActive) {
      // Deep nesting continues...
    }
  }
}
```

### 2. Object Creation Optimization
```typescript
// ✅ OPTIMIZED - Reuse objects when possible
const objectPool = new Map<string, any>();

function getPooledObject(type: string): any {
  if (!objectPool.has(type)) {
    objectPool.set(type, createObject(type));
  }
  return objectPool.get(type);
}

// ❌ SLOW - Create new objects repeatedly
function getObject(type: string): any {
  return createObject(type);  // Always creates new
}
```

### 3. String Operations Optimization
```typescript
// ✅ OPTIMIZED - Template literals for concatenation
const message = `User ${userId} performed ${action} at ${timestamp}`;

// ❌ SLOW - String concatenation
const message = 'User ' + userId + ' performed ' + action + ' at ' + timestamp;
```

### 4. Array Operations Optimization
```typescript
// ✅ OPTIMIZED - Use appropriate array methods
const activeUsers = users.filter(user => user.isActive);
const userNames = users.map(user => user.name);

// ❌ SLOW - Manual loops like Gemini CLI
const activeUsers = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].isActive) {
    activeUsers.push(users[i]);
  }
}
```

## 🛡️ PERFORMANCE CHECKS

### Pre-Commit Performance Audit
```bash
#!/bin/bash
# Add to .git/hooks/pre-commit

echo "🚀 Performance audit..."

# 1. Check startup time
STARTUP_TIME=$(time node dist/cli.js --version 2>&1 | grep real | awk '{print $2}')
echo "Startup time: $STARTUP_TIME"

# 2. Check bundle size
BUNDLE_SIZE=$(du -sh dist/ | awk '{print $1}')
echo "Bundle size: $BUNDLE_SIZE"

# 3. Check for sync operations
SYNC_OPS=$(grep -r "Sync(" src/ | wc -l)
if [ $SYNC_OPS -gt 0 ]; then
  echo "❌ Found $SYNC_OPS synchronous operations"
  exit 1
fi

# 4. Check for console usage
CONSOLE_USAGE=$(grep -r "console\." src/ | grep -v ".test." | grep -v "cli.ts" | wc -l)
if [ $CONSOLE_USAGE -gt 0 ]; then
  echo "⚠️  Found $CONSOLE_USAGE console statements"
fi

echo "✅ Performance audit passed"
```

### Runtime Performance Monitoring
```typescript
// ✅ REQUIRED - Performance timing for critical paths
export class PerformanceMonitor {
  private static timers = new Map<string, number>();
  
  static start(label: string): void {
    this.timers.set(label, performance.now());
  }
  
  static end(label: string): number {
    const start = this.timers.get(label);
    if (!start) {
      throw createUserError(`Timer ${label} not found`);
    }
    
    const duration = performance.now() - start;
    this.timers.delete(label);
    
    // Log slow operations
    if (duration > 100) {
      logger.warn(`Slow operation: ${label} took ${duration.toFixed(2)}ms`);
    }
    
    return duration;
  }
}

// Usage in critical paths
PerformanceMonitor.start('ai-query');
const result = await aiClient.query(prompt);
PerformanceMonitor.end('ai-query');
```

## 🎯 CRITICAL PERFORMANCE AREAS

### AI Operations
```typescript
// ✅ OPTIMIZED - Efficient AI client usage
class OptimizedAIClient {
  private responseCache = new Map<string, CachedResponse>();
  
  async query(prompt: string): Promise<AIResponse> {
    // Check cache first
    const cacheKey = this.getCacheKey(prompt);
    const cached = this.responseCache.get(cacheKey);
    
    if (cached && !this.isExpired(cached)) {
      return cached.response;
    }
    
    // Make request with timeout
    const response = await Promise.race([
      this.makeRequest(prompt),
      this.timeoutPromise(30000)  // 30s timeout
    ]);
    
    // Cache successful responses
    this.responseCache.set(cacheKey, {
      response,
      timestamp: Date.now()
    });
    
    return response;
  }
}
```

### File Operations
```typescript
// ✅ OPTIMIZED - Efficient file handling
async function readFileOptimized(filePath: string): Promise<string> {
  const stats = await stat(filePath);
  
  // Handle large files differently
  if (stats.size > 10 * 1024 * 1024) {  // 10MB
    return readFileStream(filePath);
  }
  
  return readFile(filePath, 'utf8');
}
```

### Command Execution
```typescript
// ✅ OPTIMIZED - Efficient command execution
async function executeCommand(command: string): Promise<ExecutionResult> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);
  
  try {
    const result = await exec(command, { signal: controller.signal });
    return { success: true, output: result.stdout };
  } catch (error) {
    if (error.name === 'AbortError') {
      throw createUserError('Command timed out', {
        category: ErrorCategory.TIMEOUT
      });
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}
```

## ⚡ QUICK PERFORMANCE FIXES

**Slow startup?** → Check for heavy imports, use lazy loading
**High memory usage?** → Look for memory leaks, optimize data structures
**Slow operations?** → Add performance monitoring, optimize hot paths
**Large bundle?** → Remove unused dependencies, improve tree-shaking
**Blocking operations?** → Convert to async, use streams for large data
**Console spam?** → Replace with proper logging
**Inefficient loops?** → Use appropriate array methods

**Remember: Every millisecond matters. Our 6x speed advantage over Gemini CLI is our competitive edge.**
