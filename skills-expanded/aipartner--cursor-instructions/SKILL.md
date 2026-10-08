# Cursor AI Coding Instructions

## 🚨 CRITICAL RULES

### BEFORE ANY CODE SUGGESTION:

1. **ANALYZE EXISTING CODE FIRST**

   ```bash
   # Always check what exists
   - Read the entire function/component
   - Understand current patterns
   - Find similar implementations
   - Check existing types/interfaces
   ```

2. **ASK THE RIGHT QUESTIONS**
   - What problem are we solving exactly?
   - How is this currently handled?
   - What's the minimal change needed?
   - Where will this code be called?

## 🎯 PROJECT-SPECIFIC PATTERNS

### Token Management System:

```typescript
// ✅ FOLLOW THIS PATTERN
export async function someTokenFunction() {
  const user = await currentUser()
  if (!user) return

  const { data, error } = await supabaseAdmin
    .from('users')
    .update({ tokens_balance: newValue })
    .eq('clerk_user_id', user.id)
}
```

### React Components:

```typescript
// ✅ FOLLOW THIS PATTERN
'use client'
import { useTokens } from '@/contexts/TokensContext'

export default function Component() {
  const { tokens, decrementTokens } = useTokens()
  // Minimal implementation
}
```

### API Routes:

```typescript
// ✅ FOLLOW THIS PATTERN
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  // Minimal validation
  // Single responsibility
  // Error handling
}
```

## ❌ ANTI-PATTERNS TO AVOID

### Don't Create Unused Code:

```typescript
// ❌ BAD: Creating functions "just in case"
interface TokensContextType {
  tokens: number
  decrementTokens: () => Promise<void>
  refreshTokens: () => Promise<void> // ← NOT USED ANYWHERE
  incrementTokens: () => Promise<void> // ← NOT NEEDED YET
}

// ✅ GOOD: Only what's actually used
interface TokensContextType {
  tokens: number
  decrementTokens: () => Promise<void>
}
```

### Don't Over-Engineer:

```typescript
// ❌ BAD: Complex abstraction for simple task
class TokenManager {
  private strategies: Map<string, TokenStrategy>
  constructor() {
    /* complex setup */
  }
  async processTokens(user: User, plan: Plan) {
    /* over-engineered */
  }
}

// ✅ GOOD: Simple function for simple task
async function resetTokensForPlan(userId: string, plan: string) {
  const tokens = TOKENS_PER_PLAN[plan]
  await updateUserTokens(userId, tokens)
}
```

## 🔍 CODE REVIEW CHECKLIST

Before suggesting ANY code:

```markdown
- [ ] Is this the simplest solution?
- [ ] Does it follow existing patterns in the project?
- [ ] Will all created functions actually be called?
- [ ] Are there any similar functions already?
- [ ] Does it handle errors like existing code?
- [ ] Does it use the same naming conventions?
- [ ] Is it consistent with project architecture?
- [ ] Can I explain why every line is necessary?
```

## 📁 FILE STRUCTURE RULES

- Follow existing directory structure
- Use same naming conventions (`kebab-case` for directories)
- Put similar functionality together
- Don't create new patterns without justification

## 🎯 COMMON PROJECT PATTERNS

### Database Operations:

```typescript
// Always use supabaseAdmin for server operations
const { data, error } = await supabaseAdmin
  .from('table_name')
  .operation()
  .eq('clerk_user_id', userId)
```

### Error Handling:

```typescript
// Log errors but don't throw unless critical
if (error) {
  console.error('Descriptive error message:', error)
  return // or handle gracefully
}
```

### Type Safety:

```typescript
// Use existing types, create new ones only if needed
import { User } from '@/lib/ai/supabase/types'
```

## 🚨 EMERGENCY STOPS

**STOP CODING IF:**

- You're creating more than 3 new functions
- You're changing existing working logic
- You're adding dependencies
- You're creating "optional" features
- You can't explain why each line exists

## 💡 GOLDEN RULE

**The user pays for solutions that work correctly from the first attempt.**

Every line of code should be:

- **Necessary** - serves a specific purpose
- **Tested** - logic verified mentally
- **Consistent** - follows project patterns
- **Minimal** - no extra complexity

Remember: It's better to ask for clarification than to create unnecessary code that needs to be removed later.
