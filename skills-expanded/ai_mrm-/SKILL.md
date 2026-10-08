# MRM AI Platform - Cursor AI Rules

## 🎯 Project Overview
Marketing Resource Management (MRM) platform with AI-first approach for advertising agencies.
- **Tech Stack:** Next.js 14, TypeScript, PostgreSQL, ClickHouse, Vector DB, Claude API
- **Architecture:** Microservices, Event-driven, AI Agents
- **Team:** 8-12 developers + 3-4 AI specialists
- **Primary Market:** Russia & CIS (Россия и СНГ)
- **Documentation Language:** Russian (Русский)

---

## 🌍 КРИТИЧЕСКИ ВАЖНО: Язык и География

### 1. Основной язык документации: РУССКИЙ
**ВСЕГДА используйте русский язык для:**
- ✅ Описаний функций и компонентов
- ✅ Комментариев в документации (Markdown файлы)
- ✅ Пользовательских сообщений и UI текстов
- ✅ Примеров и сценариев использования
- ✅ Названий компаний, брендов, кампаний в примерах

**Английский допустим только для:**
- ❌ Код (названия переменных, функций, классов)
- ❌ Технические термины (если нет устоявшегося русского эквивалента)
- ❌ Названия технологий и библиотек
- ❌ API endpoints и схемы БД

**Примеры:**
```typescript
// ✅ ПРАВИЛЬНО: код на английском, комментарии на русском
/**
 * Генерирует медиаплан на основе брифа клиента
 * 
 * @param brief - Бриф клиента с бюджетом и целями
 * @returns Оптимизированный медиаплан
 */
async function generateMediaPlan(brief: ClientBrief): Promise<MediaPlan> {
  // Проверяем минимальный бюджет
  if (brief.budget < MIN_BUDGET) {
    throw new ValidationError('Бюджет ниже минимального порога');
  }
  // ...
}

// ❌ НЕПРАВИЛЬНО: комментарии на английском
/**
 * Generates media plan based on client brief
 */
async function generateMediaPlan(brief: ClientBrief): Promise<MediaPlan> {
  // Check minimum budget
  if (brief.budget < MIN_BUDGET) {
    throw new ValidationError('Budget below minimum threshold');
  }
}
```

### 2. География: Россия и СНГ

**ВСЕГДА используйте примеры из российского/СНГ рынка:**

✅ **ПРАВИЛЬНО - Российские компании и бренды:**
```typescript
// Примеры клиентов
const exampleClients = [
  'Сбербанк',
  'Яндекс',
  'Газпром',
  'МТС',
  'Магнит',
  'X5 Retail Group',
  'Тинькофф',
  'ВКонтакте',
  'Ozon',
  'Wildberries'
];

// Примеры агентств
const exampleAgencies = [
  'Realweb',
  'iConText',
  'Deltaplan',
  'Red Keds',
  'Grape',
  'Adventum'
];

// Примеры площадок
const platforms = [
  'Яндекс Директ',
  'VK Реклама',
  'myTarget',
  'Яндекс Метрика',
  'Telegram Ads'
];
```

❌ **НЕПРАВИЛЬНО - Западные компании:**
```typescript
// НЕ ИСПОЛЬЗОВАТЬ западные примеры!
const exampleClients = [
  'Coca-Cola',    // ❌
  'Nike',         // ❌
  'Apple',        // ❌
  'Salesforce',   // ❌
  'HubSpot'       // ❌
];
```

**География в примерах:**
```typescript
// ✅ ПРАВИЛЬНО
const campaignExample = {
  client: 'Сбербанк',
  geo: ['Москва', 'Санкт-Петербург', 'Екатеринбург'],
  platforms: ['Яндекс Директ', 'VK Реклама'],
  budget: '₽5,000,000',  // Рубли!
  targetAudience: {
    age: [25, 45],
    interests: ['банковские услуги', 'инвестиции']
  }
};

// ❌ НЕПРАВИЛЬНО
const campaignExample = {
  client: 'Bank of America',  // ❌
  geo: ['New York', 'Los Angeles'],  // ❌
  platforms: ['Google Ads', 'Facebook'],  // ❌
  budget: '$50,000',  // ❌ Доллары вместо рублей!
};
```

**Валюта:**
- ✅ Всегда рубли: `₽`, `руб`, `рублей`
- ❌ Никогда: `$`, `€`, `dollars`, `euros`

**Города:**
- ✅ Москва, Санкт-Петербург, Екатеринбург, Новосибирск, Казань
- ❌ New York, London, Berlin, Paris

**Рекламные площадки (приоритет):**
1. Яндекс Директ (не Google Ads)
2. VK Реклама (не Facebook Ads)
3. myTarget
4. Telegram Ads
5. Яндекс Метрика (не Google Analytics)

---

## 📋 Core Principles

### 1. Context First
Always load relevant context before generating code:
- Current feature/module documentation
- Related existing code patterns
- RACI matrix for the workflow
- Integration requirements

### 2. Human-in-the-Loop
All AI-generated artifacts require human review:
- Code review by senior developer
- Functional testing by QA
- Business logic validation by PM/domain expert

### 3. Feedback Loop
Every interaction is learning opportunity:
- Track acceptance rate of AI suggestions
- Store feedback in vector DB
- Iterate on prompts based on data
- Measure and improve continuously

---

## 💻 Code Style & Standards

### TypeScript
```typescript
// ✅ Good: Explicit types, descriptive names
interface MediaPlanInput {
  clientId: string;
  budget: number;
  targetAudience: TargetAudience;
  objectives: CampaignObjective[];
}

// ❌ Bad: Any types, unclear names
function process(data: any): any {
  // ...
}

// ✅ Good: Comprehensive JSDoc
/**
 * Generates media plan based on client brief and historical data
 * 
 * @param input - Client brief with budget and objectives
 * @param context - Historical campaigns for similar clients
 * @returns Optimized media plan with budget allocation
 * @throws {ValidationError} If budget < minimum threshold
 * 
 * @example
 * const plan = await generateMediaPlan({
 *   clientId: 'client-123',
 *   budget: 1000000,
 *   targetAudience: { age: [25, 45], interests: ['tech'] },
 *   objectives: ['awareness', 'conversions']
 * });
 */
async function generateMediaPlan(
  input: MediaPlanInput,
  context: HistoricalContext
): Promise<MediaPlan> {
  // Implementation
}
```

### React Components
```typescript
// ✅ Good: Functional component with types
interface BriefFormProps {
  clientId: string;
  onSubmit: (brief: ClientBrief) => Promise<void>;
  onCancel: () => void;
}

export function BriefForm({ clientId, onSubmit, onCancel }: BriefFormProps) {
  // Use hooks, clear structure
  const [brief, setBrief] = useState<Partial<ClientBrief>>({});
  
  // Early returns for loading/error states
  if (loading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    // JSX
  );
}

// ❌ Bad: Class component, no types
export class BriefForm extends React.Component {
  // Avoid class components
}
```

### File Naming
- Components: `PascalCase.tsx` (e.g., `MediaPlanGenerator.tsx`)
- Utilities: `camelCase.ts` (e.g., `budgetCalculator.ts`)
- Types: `PascalCase.types.ts` (e.g., `Campaign.types.ts`)
- Tests: `*.test.ts` or `*.spec.ts`

---

## 🤖 AI Assistants Architecture

### Standard Pattern
```typescript
/**
 * Base class for all AI assistants in the platform
 * Implements feedback loop and context optimization
 */
abstract class AIAssistant<TInput, TOutput> {
  constructor(
    protected llm: LLMClient,
    protected contextManager: ContextManager,
    protected toolRegistry: ToolRegistry
  ) {}
  
  /**
   * Main entry point for assistant
   * Implements: context gathering → prompt building → LLM call → post-processing
   */
  async process(input: TInput): Promise<TOutput> {
    // 1. Gather relevant context (max 100K tokens)
    const context = await this.contextManager.gather(input, {
      maxTokens: 100000,
      priority: ['current_task', 'project_data', 'historical_data']
    });
    
    // 2. Build optimized prompt
    const prompt = this.buildPrompt(input, context);
    
    // 3. Call LLM with tools
    const response = await this.llm.generate(prompt, {
      tools: this.getTools(),
      temperature: this.getTemperature(),
      maxTokens: 4096
    });
    
    // 4. Post-process and validate
    const output = await this.postProcess(response);
    
    // 5. Store for feedback loop
    await this.storeFeedback(input, output);
    
    return output;
  }
  
  protected abstract buildPrompt(input: TInput, context: Context): string;
  protected abstract postProcess(response: LLMResponse): Promise<TOutput>;
  protected abstract getTools(): Tool[];
}

/**
 * Example: Account Manager AI Assistant
 */
class AccountAssistant extends AIAssistant<ClientRequest, AccountResponse> {
  protected buildPrompt(request: ClientRequest, context: Context): string {
    return `
You are an AI assistant for Account Manager in advertising agency.

## Your Role
- Help with client communication
- Generate briefs and presentations
- Schedule meetings and follow-ups
- Maintain client relationships

## Current Context
Client: ${context.client.name}
Industry: ${context.client.industry}
History: ${context.previousProjects.length} projects, avg budget ${context.avgBudget}

## Current Request
${request.description}

## Instructions
1. Understand client needs thoroughly
2. Reference past successful projects
3. Propose actionable next steps
4. Be professional but friendly
5. Always include specific dates/numbers

Generate response in JSON format:
{
  "understanding": "your understanding of the request",
  "proposal": "your proposed action",
  "nextSteps": ["step 1", "step 2"],
  "timeline": "estimated timeline"
}
`;
  }
  
  protected getTools(): Tool[] {
    return [
      this.toolRegistry.get('client_database'),
      this.toolRegistry.get('calendar'),
      this.toolRegistry.get('email_composer')
    ];
  }
}
```

---

## 🎯 RACI Implementation

### Always specify RACI for workflows
```typescript
interface Task {
  id: string;
  name: string;
  raci: {
    responsible: Role[];  // R - Who does the work
    accountable: Role;     // A - Who makes final decision (only one!)
    consulted: Role[];     // C - Who provides input
    informed: Role[];      // I - Who needs to know
  };
}

enum Role {
  ACCOUNT_MANAGER = 'account_manager',
  SPECIALIST = 'specialist',
  PROJECT_MANAGER = 'project_manager',
  STRATEGIST = 'strategist',
  CLIENT = 'client',
  // ... other roles
}

// Example: Brief creation workflow
const briefCreationTask: Task = {
  id: 'brief_creation',
  name: 'Create client brief',
  raci: {
    responsible: [Role.ACCOUNT_MANAGER],  // Does the work
    accountable: Role.PROJECT_MANAGER,     // Approves
    consulted: [Role.STRATEGIST, Role.CLIENT],
    informed: [Role.SPECIALIST]
  }
};
```

---

## 🔧 Context Optimization

### Priority Levels
```typescript
enum ContextPriority {
  CRITICAL = 0,   // Current task, client brief
  HIGH = 1,       // RACI matrix, workflow docs
  MEDIUM = 2,     // Historical data, similar projects
  LOW = 3         // General best practices, platform docs
}

class ContextManager {
  async gather(input: any, options: GatherOptions): Promise<Context> {
    const items: ContextItem[] = [];
    
    // 1. Critical: Always include (5-10K tokens)
    items.push(...await this.getCriticalContext(input));
    
    // 2. High: Include if space available (20-30K tokens)
    if (this.hasTokenBudget(items, options.maxTokens, 30000)) {
      items.push(...await this.getHighPriorityContext(input));
    }
    
    // 3. Medium: Include if space available (40-50K tokens)
    if (this.hasTokenBudget(items, options.maxTokens, 50000)) {
      items.push(...await this.getMediumPriorityContext(input));
    }
    
    // 4. Low: Fill remaining budget
    const remaining = options.maxTokens - this.countTokens(items);
    if (remaining > 10000) {
      items.push(...await this.getLowPriorityContext(input, remaining));
    }
    
    return this.buildContext(items);
  }
}
```

### Context Caching
```typescript
// Cache frequently used context to save tokens and time
const contextCache = new LRUCache<string, Context>({
  max: 100,
  ttl: 1000 * 60 * 30, // 30 minutes
});

// Cache keys examples:
// - `client:${clientId}` - client info
// - `workflow:${workflowType}` - RACI matrix
// - `template:${templateId}` - project template
```

---

## 🧪 Testing Requirements

### Unit Tests
```typescript
// Every AI assistant function needs unit test
describe('AccountAssistant', () => {
  it('should generate brief from client request', async () => {
    const assistant = new AccountAssistant(mockLLM, mockContext, mockTools);
    const request = createMockClientRequest();
    
    const response = await assistant.process(request);
    
    expect(response).toMatchObject({
      understanding: expect.any(String),
      proposal: expect.any(String),
      nextSteps: expect.arrayContaining([expect.any(String)]),
      timeline: expect.any(String)
    });
  });
  
  it('should handle errors gracefully', async () => {
    const assistant = new AccountAssistant(mockFailingLLM, mockContext, mockTools);
    
    await expect(assistant.process({})).rejects.toThrow(ValidationError);
  });
});
```

### Integration Tests
```typescript
// Test full workflows with multiple components
describe('Brief Creation Workflow', () => {
  it('should complete full cycle: input → AI → human review → output', async () => {
    const workflow = new BriefCreationWorkflow();
    
    // 1. Client submits request
    const requestId = await workflow.submitRequest(mockRequest);
    
    // 2. AI generates draft
    const draft = await workflow.generateDraft(requestId);
    expect(draft.status).toBe('pending_review');
    
    // 3. Human reviews and approves
    await workflow.review(draft.id, { approved: true, feedback: 'Good' });
    
    // 4. Final brief generated
    const final = await workflow.getFinalBrief(requestId);
    expect(final.status).toBe('approved');
  });
});
```

---

## 📊 Error Handling

### Standard Error Types
```typescript
// Custom error classes for domain-specific errors
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

class AIGenerationError extends Error {
  constructor(message: string, public context: any) {
    super(message);
    this.name = 'AIGenerationError';
  }
}

class RateLimitError extends Error {
  constructor(public retryAfter: number) {
    super(`Rate limit exceeded. Retry after ${retryAfter}s`);
    this.name = 'RateLimitError';
  }
}

// Always use try-catch with specific error handling
async function processWithAI(input: any): Promise<any> {
  try {
    const result = await aiAssistant.process(input);
    return result;
  } catch (error) {
    if (error instanceof ValidationError) {
      logger.warn('Validation failed', { field: error.field });
      throw new UserFacingError('Please check your input');
    }
    
    if (error instanceof RateLimitError) {
      logger.info('Rate limited, retrying...', { retryAfter: error.retryAfter });
      await sleep(error.retryAfter * 1000);
      return processWithAI(input); // Retry
    }
    
    if (error instanceof AIGenerationError) {
      logger.error('AI generation failed', { context: error.context });
      // Fallback to template or human intervention
      return fallbackHandler.handle(input);
    }
    
    // Unknown error
    logger.error('Unexpected error', { error });
    throw error;
  }
}
```

---

## 📝 Documentation Standards

### README for each module
```markdown
# Account Assistant Module

## Purpose
AI-powered assistant for Account Managers to handle client communication and brief creation.

## Features
- Generate client briefs from conversations
- Schedule follow-ups automatically
- Maintain client relationship history
- Suggest upsell opportunities

## Usage
\`\`\`typescript
const assistant = new AccountAssistant(llm, context, tools);
const response = await assistant.process({
  clientId: 'client-123',
  request: 'Create brief for new campaign'
});
\`\`\`

## API
See [API.md](./API.md) for detailed API documentation.

## Testing
\`\`\`bash
npm test src/ai/assistants/account/
\`\`\`

## Feedback Loop
This assistant tracks:
- Acceptance rate (target: >80%)
- Edit distance (target: <20% of generated content)
- Time saved (target: 60min → 10min per brief)

See metrics dashboard: /admin/ai/metrics/account-assistant
```

---

## 🚫 Anti-Patterns (What NOT to Do)

### ❌ Don't: Trust AI blindly
```typescript
// BAD
const code = await ai.generate('Create user auth system');
await deployToProduction(code); // NO REVIEW!

// GOOD
const code = await ai.generate('Create user auth system');
await createPullRequest(code); // Human review required
```

### ❌ Don't: Overload context
```typescript
// BAD - loading entire codebase
const context = await loadAllFiles(); // 500K tokens!

// GOOD - selective context
const context = await loadRelevantFiles(task, { maxTokens: 100000 });
```

### ❌ Don't: Ignore TypeScript errors
```typescript
// BAD
const result = await someFunction(); // Type error! Ignoring...

// GOOD
const result: ExpectedType = await someFunction();
// Or fix the function signature
```

### ❌ Don't: Skip error handling
```typescript
// BAD
async function fetchData() {
  const data = await api.get('/data');
  return data;
}

// GOOD
async function fetchData(): Promise<Data> {
  try {
    const data = await api.get('/data');
    return data;
  } catch (error) {
    if (error instanceof NetworkError) {
      // Retry logic
    }
    throw new DataFetchError('Failed to fetch data', { cause: error });
  }
}
```

---

## 🎓 When to Ask for Human Help

AI should request human assistance when:
1. **Ambiguous requirements** - unclear what user wants
2. **Architectural decisions** - impacts multiple modules
3. **Breaking changes** - changes public APIs
4. **Security-sensitive code** - auth, payments, data access
5. **Performance-critical** - query optimization, caching strategy
6. **Business logic** - domain-specific rules
7. **RACI conflicts** - unclear who is accountable
8. **Budget decisions** - trade-offs between cost and quality

Example:
```typescript
if (requiresHumanDecision(task)) {
  await notifications.send({
    to: task.accountable,
    message: 'AI needs your input on: ' + task.name,
    priority: 'high'
  });
}
```

---

## 📈 Metrics to Track

### Code Quality
- **Test Coverage:** Target 80%+
- **Type Coverage:** Target 95%+ (no `any` types)
- **Linter Errors:** Zero tolerance
- **Bundle Size:** Monitor and optimize

### AI Performance
- **Acceptance Rate:** % of AI suggestions accepted (target 75%+)
- **Edit Distance:** How much humans edit AI output (target <25%)
- **Time Saved:** Hours saved per week (target 20h+ per developer)
- **Bug Rate:** Bugs in AI code vs human code (should be similar or better)

### User Satisfaction
- **NPS Score:** For AI-assisted features (target 40+)
- **Task Completion Time:** With AI vs without (target 3x faster)
- **User Adoption:** % of team using AI tools (target 90%+)

---

## 🔄 Workflow Example

### Creating a new feature with AI

```
1. Read requirement
   ↓
2. Search codebase for similar patterns
   → `grep -r "similar_feature" src/`
   ↓
3. Load relevant context (max 100K tokens)
   → Current module docs
   → Related interfaces
   → RACI for this workflow
   ↓
4. Generate code + tests
   → Ask AI to implement
   → Include error handling
   → Add JSDoc comments
   ↓
5. Run linters and tests
   → `npm run lint`
   → `npm test`
   ↓
6. Human review
   → Code review by senior
   → Test execution by QA
   ↓
7. Iterate based on feedback
   → Address review comments
   → Improve prompts for next time
   ↓
8. Commit with descriptive message
   → `git commit -m "feat(account): add AI brief generator"`
   ↓
9. Update metrics dashboard
   → Log time saved
   → Log acceptance rate
   → Store feedback
```

---

## 🎯 Prompting Best Practices

### Be Specific
```
❌ "Create a form"
✅ "Create a TypeScript React form component for client brief input with:
   - Fields: company name, industry, budget, objectives
   - Validation: Zod schema
   - Submit: async POST to /api/briefs
   - Error handling: toast notifications
   - Accessibility: ARIA labels"
```

### Provide Context
```
❌ "Fix this bug"
✅ "Fix this bug in AccountAssistant.ts line 45:
   Error: TypeError: Cannot read property 'name' of undefined
   Context: This happens when client object is missing from context
   Expected: Should handle missing client gracefully
   Related code: ClientContext.ts, ContextManager.ts"
```

### Request Tests
```
❌ "Create a function to calculate budget"
✅ "Create a function to calculate budget allocation across channels:
   - Input: total budget, channel weights
   - Output: budget per channel
   - Include: unit tests, edge cases (0 budget, negative, etc)
   - Use: TypeScript, strict mode"
```

---

## 🏁 Quick Reference

### Common Commands
```bash
# Start development
npm run dev

# Run tests
npm test

# Type check
npm run type-check

# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build

# Run AI metrics dashboard
npm run ai:metrics
```

### Project Structure
```
mrm-ai/
├── src/
│   ├── ai/                  # AI assistants and agents
│   │   ├── assistants/      # Domain-specific assistants
│   │   ├── agents/          # Autonomous agents
│   │   ├── prompts/         # Prompt library
│   │   └── tools/           # AI tools (API wrappers)
│   ├── features/            # Feature modules
│   ├── shared/              # Shared utilities
│   └── types/               # TypeScript types
├── prompts/                 # Prompt templates
├── context/                 # Context for AI
├── tests/                   # Test files
└── docs/                    # Documentation
```

---

**Version:** 1.0  
**Last Updated:** 2025-10-23  
**Maintainer:** MRM AI Team

