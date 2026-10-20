# Coding & Development Skill

Professional software development with multi-language expertise.

## Core Languages

### Python (Primary)
```
Best for: Data analysis, automation, ML/AI, scripting
Frameworks: FastAPI, Django, Flask, NumPy, Pandas
Pattern: Functional + OOP hybrid
```

### JavaScript/TypeScript
```
Best for: Web apps, Node.js backends, React/Vue frontend
Modern: ES6+, async/await, modules
Pattern: Async-first, event-driven
```

### Rust
```
Best for: Systems, performance-critical, blockchain
Features: Memory safety, zero-cost abstractions
Pattern: Ownership + borrowing
```

### Go
```
Best for: Microservices, cloud-native, networking
Features: Goroutines, channels, fast compile
Pattern: C-like simplicity + concurrency
```

### C/C++
```
Best for: Low-level systems, embedded, trading engines
Pattern: Manual memory management, performance first
```

## Development Protocol

### Code Quality Ladder
1. **Working** → It runs
2. **Clean** → Readable, DRY, tested
3. **Fast** → Optimized, profiled
4. **Resilient** → Handles edge cases

### Multi-Agent Coding
```
Kimi (me): Architecture, integration, review
GLM5 (Deep): Algorithms, research, optimization
MiniMax (Scan): Quick review, patterns, common issues

Flow:
Task → Design → Delegate heavy lifting → Synthesize → Review
```

### Security First
- Never commit secrets (use .env)
- Input validation on all boundaries
- Output encoding to prevent injection
- Principle of least privilege

## Libraries by Use Case

| Use Case | Python | JS/TS | Rust | Go |
|----------|--------|-------|------|-----|
| Web API | FastAPI | Express | actix-web | Gin |
| Database | SQLAlchemy | Prisma | sqlx | GORM |
| HTTP/Async | aiohttp | Axios | reqwest | net/http |
| Crypto | cryptography | ethers.js | ethers-rs | go-ethereum |
| ML/AI | PyTorch, TF | tfjs | tch-rs | - |

## Code Patterns

### Error Handling
```python
# Rust-style Result/Option
from typing import Optional

def parse_config(path: str) -> tuple[bool, Optional[dict]]:
    try:
        with open(path) as f:
            return (True, json.load(f))
    except Exception as e:
        return (False, None)  # Or detailed error
```

### Concurrency
```python
# Async-first for IO
async def fetch_prices(symbols: list) -> dict:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, s) for s in symbols]
        return await asyncio.gather(*tasks)
```

## Commands

- `/code` - Generate code from description
- `/review` - Review code for issues
- `/optimize` - Performance optimization
- `/test` - Generate tests
- `/debug` - Find and fix bugs
- `/refactor` - Suggest improvements

## Memory Keys

- `code:patterns` - Common patterns by language
- `code:snippets` - Reusable code blocks
- `code:projects` - Active project context
