# AGENTS.md - AI Assistant Guide for Signal Project

**Last Updated**: 2024-03-02  
**Codebase Commit**: 6b6cb671f4d24ace742b0a546336c78883f81464

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Project Overview](#project-overview)
3. [Directory Structure](#directory-structure)
4. [Development Patterns](#development-patterns)
5. [Testing Guide](#testing-guide)
6. [Common Tasks](#common-tasks)
7. [Architecture Quick Reference](#architecture-quick-reference)
8. [API Quick Reference](#api-quick-reference)
9. [Troubleshooting](#troubleshooting)

---

## Quick Reference

### Essential Commands

**Backend**:
```bash
# Start server
cd backend && PYTHONPATH=src uvicorn signal_app.api.app:app --reload --port 8000

# Run tests
cd backend && PYTHONPATH=src pytest tests/ -v

# Run specific test
cd backend && PYTHONPATH=src pytest tests/test_routes_signals.py -v

# Database queries
sqlite3 signal.db "SELECT * FROM signal LIMIT 5;"
```

**Frontend**:
```bash
# Start dev server
cd frontend && npm run dev

# Build
cd frontend && npm run build

# Lint
cd frontend && npm run lint
```

### Key Files to Know

**Backend**:
- `backend/src/signal_app/api/app.py` - FastAPI application entry point
- `backend/src/signal_app/services/pipeline_service.py` - Pipeline orchestration
- `backend/src/signal_app/agents/classifier_agent.py` - LLM classification
- `backend/src/signal_app/models/signal.py` - Main data model

**Frontend**:
- `frontend/src/App.tsx` - Application root with routing
- `frontend/src/pages/Dashboard.tsx` - Main dashboard
- `frontend/src/api/client.ts` - API client
- `frontend/src/types/api.ts` - TypeScript types

### Documentation Files

For detailed information, see `.agents/summary/`:
- `index.md` - Documentation navigation guide
- `architecture.md` - System architecture and design patterns
- `components.md` - Detailed component documentation
- `interfaces.md` - API endpoints and data interfaces
- `data_models.md` - Data structures and models
- `workflows.md` - Key processes and workflows
- `dependencies.md` - External dependencies

---

## Project Overview

### What is Signal?

Signal is an automated customer pain discovery system that:
1. **Ingests** posts from Reddit communities
2. **Detects** customer pain points using LLM analysis
3. **Classifies** signals by severity and category
4. **Routes** for manual review or automatic ticket creation
5. **Tracks** resolution status and metrics

### Technology Stack

**Backend**:
- Python 3.11+ with FastAPI (async web framework)
- SQLModel (SQLAlchemy + Pydantic ORM)
- Strands Agents (AWS Bedrock LLM integration)
- asyncpraw (Reddit API), PyGithub (GitHub API)
- SQLite database (PostgreSQL-ready)

**Frontend**:
- TypeScript with React 18
- Vite (build tool)
- TanStack Query (server state)
- shadcn/ui (Radix UI components)
- Tailwind CSS

### Current Status

- ✅ **Phase 1**: Backend Foundation (Complete)
- ✅ **Phase 2**: Frontend Dashboard (Complete)
- ✅ **Phase 3**: Chat Agent (Complete)
- 🚧 **Phase 4**: Production Deployment (In Progress)

---

## Directory Structure

```
signal/
├── backend/
│   ├── src/signal_app/
│   │   ├── agents/              # LLM agents (classifier, detector, chat)
│   │   │   ├── classifier_agent.py    # Signal classification
│   │   │   ├── detection_agent.py     # Signal detection
│   │   │   └── chat_agent.py          # Chat interface
│   │   ├── api/                 # FastAPI routes and app
│   │   │   ├── app.py                 # Main application
│   │   │   ├── dependencies.py        # Dependency injection
│   │   │   ├── routes/
│   │   │   │   ├── signals.py         # Signal CRUD
│   │   │   │   ├── pipeline.py        # Pipeline control
│   │   │   │   ├── connectors.py      # Connector management
│   │   │   │   ├── chat.py            # Chat SSE endpoint
│   │   │   │   └── health.py          # Health check
│   │   │   └── schemas/               # Request/response schemas
│   │   ├── clients/             # External API clients
│   │   │   ├── reddit_client.py       # Reddit API wrapper
│   │   │   └── github_client.py       # GitHub API wrapper
│   │   ├── connectors/          # Data source connectors
│   │   │   ├── base.py                # Base connector interface
│   │   │   ├── reddit.py              # Reddit connector
│   │   │   ├── github.py              # GitHub connector
│   │   │   └── factory.py             # Connector factory
│   │   ├── models/              # SQLModel database models
│   │   │   ├── signal.py              # Signal entity
│   │   │   ├── raw_post.py            # Raw Reddit post
│   │   │   ├── connector_config.py    # Connector configuration
│   │   │   └── schemas.py             # Pydantic validation schemas
│   │   ├── prompts/             # LLM prompt templates
│   │   │   ├── classification_prompts.py
│   │   │   └── detection_prompt.py
│   │   ├── repositories/        # Data access layer
│   │   │   ├── signal_repository.py
│   │   │   ├── raw_post_repository.py
│   │   │   ├── connector_repository.py
│   │   │   └── pipeline_repository.py
│   │   ├── schemas/             # Additional Pydantic schemas
│   │   ├── services/            # Business logic layer
│   │   │   ├── pipeline_service.py    # Pipeline orchestration
│   │   │   ├── classification_service.py
│   │   │   ├── ingestion_service.py
│   │   │   ├── review_service.py
│   │   │   ├── ticket_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── session_manager.py
│   │   │   └── connector_service.py
│   │   ├── tools/               # Chat agent tools
│   │   │   └── signal_tools.py        # 4 signal analysis tools
│   │   └── utils/               # Utilities
│   │       ├── retry.py               # Retry decorator
│   │       ├── activity_log.py        # Activity logging
│   │       ├── logging.py             # Logging config
│   │       └── prompt_debugger.py     # LLM debug capture
│   ├── tests/                   # 38 test files (226 tests)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                 # API clients
│   │   │   ├── client.ts              # REST API client
│   │   │   └── chatClient.ts          # SSE chat client
│   │   ├── components/          # React components
│   │   │   ├── ui/                    # shadcn/ui primitives (14 components)
│   │   │   ├── Dashboard.tsx          # Main dashboard
│   │   │   ├── SignalsTable.tsx       # Signal list
│   │   │   ├── ReviewModal.tsx        # Review dialog
│   │   │   ├── PipelineRunDialog.tsx  # Pipeline config
│   │   │   ├── NeedsReviewSection.tsx # High-severity signals
│   │   │   ├── PipelineStatusBar.tsx  # Pipeline status
│   │   │   ├── ActivityTimeline.tsx   # Activity log
│   │   │   ├── PipelineRunRow.tsx     # Run list item
│   │   │   ├── ConnectorCard.tsx      # Connector display
│   │   │   ├── RedditConfigPanel.tsx  # Reddit config
│   │   │   └── GitHubConfigPanel.tsx  # GitHub config
│   │   ├── hooks/               # Custom React hooks
│   │   │   └── use-theme.ts           # Dark/light mode
│   │   ├── lib/                 # Utilities
│   │   │   ├── constants.ts           # App constants
│   │   │   ├── styles.ts              # Style utilities
│   │   │   ├── connectors.ts          # Connector metadata
│   │   │   ├── utils.ts               # General utilities
│   │   │   └── queryClient.ts         # React Query config
│   │   ├── pages/               # Page components
│   │   │   ├── Dashboard.tsx          # Dashboard page (duplicate?)
│   │   │   ├── ChatPage.tsx           # Chat interface
│   │   │   ├── PipelineRunsPage.tsx   # Pipeline history
│   │   │   └── ConnectorsPage.tsx     # Connector management
│   │   └── types/               # TypeScript types
│   │       ├── api.ts                 # API types
│   │       ├── pipeline.ts            # Pipeline types
│   │       └── connectors.ts          # Connector types
│   └── package.json
├── .agents/                     # Project documentation
│   ├── summary/                 # Generated documentation
│   │   ├── index.md                   # Documentation index
│   │   ├── architecture.md            # System architecture
│   │   ├── components.md              # Component details
│   │   ├── interfaces.md              # API endpoints
│   │   ├── data_models.md             # Data structures
│   │   ├── workflows.md               # Process flows
│   │   ├── dependencies.md            # External dependencies
│   │   ├── codebase_info.md           # Basic info
│   │   └── review_notes.md            # Documentation review
│   └── planning/                # Project planning docs
├── .kiro/steering/              # AI assistant rules
│   └── signal.md                      # Project-specific rules
└── README.md                    # User-facing documentation
```

### Key Directory Purposes

**Backend**:
- `agents/` - LLM-powered agents for classification, detection, and chat
- `api/` - FastAPI routes, schemas, and application setup
- `clients/` - Wrappers for external APIs (Reddit, GitHub)
- `connectors/` - Pluggable data source connectors
- `models/` - Database models and validation schemas
- `prompts/` - LLM prompt templates
- `repositories/` - Data access layer (CRUD operations)
- `services/` - Business logic and orchestration
- `tools/` - Chat agent tools for signal analysis
- `utils/` - Shared utilities (retry, logging, activity log)

**Frontend**:
- `api/` - API client and SSE chat client
- `components/` - React components (UI primitives + feature components)
- `hooks/` - Custom React hooks
- `lib/` - Utilities and constants
- `pages/` - Page-level components
- `types/` - TypeScript type definitions

---

## Development Patterns

### Backend Patterns

#### 1. Layered Architecture

**Always follow**: API → Service → Repository → Database

```python
# ✅ GOOD: Proper layering
@router.get("/api/signals")
async def list_signals(
    signal_service: SignalService = Depends(get_signal_service)
):
    return await signal_service.list_signals()

# ❌ BAD: Skipping service layer
@router.get("/api/signals")
async def list_signals(
    signal_repo: SignalRepository = Depends(get_signal_repository)
):
    return signal_repo.list()  # Business logic in route
```

#### 2. Dependency Injection

**Use FastAPI `Depends()`** for all dependencies:

```python
# dependencies.py
def get_signal_repository(session: Session = Depends(get_session)):
    return SignalRepository(session)

def get_signal_service(
    signal_repo: SignalRepository = Depends(get_signal_repository)
):
    return SignalService(signal_repo)

# routes/signals.py
@router.get("/api/signals")
async def list_signals(
    service: SignalService = Depends(get_signal_service)
):
    return service.list_signals()
```

#### 3. Async/Await

**Use async/await** for I/O operations:

```python
# ✅ GOOD: Async for I/O
async def fetch_posts(self, subreddit: str):
    async for post in self.reddit.subreddit(subreddit).new(limit=100):
        yield post

# ❌ BAD: Blocking I/O
def fetch_posts(self, subreddit: str):
    for post in self.reddit.subreddit(subreddit).new(limit=100):
        yield post
```

#### 4. Retry Logic

**Use `@async_retry` decorator** for LLM calls:

```python
from ..utils import async_retry, RETRIABLE_EXCEPTIONS

@async_retry(delays=[3.0, 30.0, 60.0], jitter=True, exceptions=RETRIABLE_EXCEPTIONS)
async def classify_signal(self, signal: Signal):
    response = await self.agent.structured_output_async(ClassificationData, prompt)
    return response
```

#### 5. Activity Logging

**Add activity logs** for pipeline operations:

```python
from ..utils import create_activity_entry

pipeline_run.add_activity(
    create_activity_entry("system", "Stage 1: Fetch started")
)
```

#### 6. Structured LLM Output

**Use Pydantic models** for LLM responses:

```python
# Define schema
class ClassificationData(BaseModel):
    category: str
    severity: str
    confidence: float
    summary: str

# Use with Strands
response = await agent.structured_output_async(ClassificationData, prompt)
```

### Frontend Patterns

#### 1. Server State with TanStack Query

**Use TanStack Query** for API data, not useState:

```typescript
// ✅ GOOD: TanStack Query
const { data, isLoading } = useQuery({
  queryKey: ['signals'],
  queryFn: () => signalsApi.list(),
  refetchInterval: POLLING_INTERVAL,
});

// ❌ BAD: useState for server data
const [signals, setSignals] = useState([]);
useEffect(() => {
  signalsApi.list().then(setSignals);
}, []);
```

#### 2. Mutations with Invalidation

**Invalidate queries** after mutations:

```typescript
const mutation = useMutation({
  mutationFn: (id: number) => signalsApi.review(id, reviewData),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['signals'] });
    toast.success('Signal reviewed');
  },
});
```

#### 3. Type Safety

**Use TypeScript types** for all props and state:

```typescript
// ✅ GOOD: Typed props
interface SignalsTableProps {
  signals: Signal[];
  onReview: (signal: Signal) => void;
}

export function SignalsTable({ signals, onReview }: SignalsTableProps) {
  // ...
}

// ❌ BAD: Untyped props
export function SignalsTable({ signals, onReview }) {
  // ...
}
```

#### 4. Form Validation with Zod

**Use Zod schemas** for form validation:

```typescript
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  title: z.string().min(1, 'Title required'),
  description: z.string().min(10, 'Description too short'),
});

const form = useForm({
  resolver: zodResolver(schema),
});
```

#### 5. Component Composition

**Compose from shadcn/ui primitives**, don't reinvent:

```typescript
// ✅ GOOD: Compose from primitives
import { Dialog, DialogContent, DialogHeader } from '@/components/ui/dialog';

export function ReviewModal() {
  return (
    <Dialog>
      <DialogContent>
        <DialogHeader>Review Signal</DialogHeader>
        {/* ... */}
      </DialogContent>
    </Dialog>
  );
}

// ❌ BAD: Custom modal from scratch
export function ReviewModal() {
  return (
    <div className="fixed inset-0 bg-black/50">
      {/* Custom modal implementation */}
    </div>
  );
}
```

---

## Testing Guide

### Backend Testing

#### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures
├── test_routes_*.py         # API endpoint tests
├── test_services.py         # Service layer tests
├── test_repositories.py     # Repository tests
├── test_*_agent.py          # Agent tests
└── test_*.py                # Other unit tests
```

#### Running Tests

```bash
# All tests
cd backend && PYTHONPATH=src pytest tests/ -v

# Specific test file
PYTHONPATH=src pytest tests/test_routes_signals.py -v

# Specific test
PYTHONPATH=src pytest tests/test_routes_signals.py::test_list_signals -v

# With coverage
PYTHONPATH=src pytest tests/ --cov=signal_app --cov-report=term-missing
```

#### Testing Principles

1. **Test behavior, not implementation**
2. **Minimize mocks** - Only mock external dependencies (LLM, Reddit API, GitHub API)
3. **Use real database** - In-memory SQLite for fast, realistic tests
4. **Test business logic** - Focus on service layer

#### Example Test Pattern

```python
# ✅ GOOD: Test with real database
def test_create_signal(session):
    repo = SignalRepository(session)
    signal = Signal(source_type="reddit", source_id="abc123", ...)
    created = repo.create(signal)
    
    assert created.id is not None
    assert session.get(Signal, created.id) == created

# ❌ BAD: Mock repository
def test_service_with_mock_repo(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_by_id.return_value = Signal(...)
    # This tests nothing - just that mocks work
```

#### Mocking External Services

```python
# ✅ GOOD: Mock external LLM API
@pytest.mark.asyncio
async def test_classify_signal(mocker):
    mock_agent = mocker.Mock()
    mock_agent.structured_output_async.return_value = ClassificationData(
        category="bug",
        severity="high",
        confidence=0.95,
        summary="Test summary",
        key_quotes=[],
        reasoning="Test reasoning"
    )
    
    service = ClassificationService(mock_agent)
    result = await service.classify_signal(signal)
    
    assert result.severity == "high"
```

### Frontend Testing

#### Build Validation

```bash
cd frontend

# Type check + build
npm run build

# Lint
npm run lint
```

#### Manual Testing Checklist

After changes, verify:
- [ ] Page loads without errors
- [ ] API calls work (check Network tab)
- [ ] UI updates reflect data changes
- [ ] Forms validate correctly
- [ ] Error states display properly
- [ ] Loading states show during async operations

---

## Common Tasks

### Adding a New API Endpoint

1. **Define route** in `api/routes/`:
```python
@router.post("/api/signals/{id}/action")
async def perform_action(
    id: int,
    request: ActionRequest,
    service: SignalService = Depends(get_signal_service)
):
    result = await service.perform_action(id, request)
    return result
```

2. **Add service method** in `services/`:
```python
async def perform_action(self, signal_id: int, request: ActionRequest):
    signal = self.signal_repo.get_by_id(signal_id)
    # Business logic here
    return self.signal_repo.update(signal)
```

3. **Update frontend client** in `api/client.ts`:
```typescript
export const signalsApi = {
  performAction: async (id: number, request: ActionRequest) => {
    const { data } = await api.post(`/api/signals/${id}/action`, request);
    return data;
  },
};
```

4. **Add TypeScript types** in `types/api.ts`:
```typescript
interface ActionRequest {
  action: string;
  // ...
}
```

### Adding a New Database Field

1. **Update model** in `models/signal.py`:
```python
class Signal(SQLModel, table=True):
    # ... existing fields
    new_field: Optional[str] = None
```

2. **Delete database** (development only):
```bash
rm signal.db
```

3. **Restart server** (tables auto-create):
```bash
cd backend && PYTHONPATH=src uvicorn signal_app.api.app:app --reload
```

4. **Update TypeScript types** in `types/api.ts`:
```typescript
interface Signal {
  // ... existing fields
  new_field?: string;
}
```

### Adding a New Chat Tool

1. **Define tool function** in `tools/signal_tools.py`:
```python
def my_new_tool(param: str) -> dict:
    """Tool description for LLM."""
    # Implementation
    return {"result": "..."}
```

2. **Add to tool list** in `create_signal_tools()`:
```python
def create_signal_tools(db_session):
    return [
        # ... existing tools
        Tool(
            name="my_new_tool",
            description="Tool description",
            func=lambda param: my_new_tool(param)
        )
    ]
```

3. **Update system prompt** in `agents/chat_agent.py`:
```python
def _build_system_prompt(self):
    return f"""...
    Available tools:
    - my_new_tool: Description
    """
```

### Running the Pipeline Manually

**Via API**:
```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"connector_id": 1, "lookback_days": 7}'
```

**Via Python**:
```python
cd backend
PYTHONPATH=src python -c "
from signal_app.database import get_session
from signal_app.repositories import SignalRepository, PipelineRepository
from signal_app.services import PipelineService
import asyncio

session = next(get_session())
signal_repo = SignalRepository(session)
pipeline_repo = PipelineRepository(session)
pipeline_service = PipelineService(signal_repo, pipeline_repo)

asyncio.run(pipeline_service.run_pipeline())
"
```

---

## Architecture Quick Reference

### System Layers

```
┌─────────────────────────────────────┐
│  API Layer (FastAPI Routes)        │  HTTP requests/responses
├─────────────────────────────────────┤
│  Service Layer (Business Logic)    │  Orchestration, workflows
├─────────────────────────────────────┤
│  Repository Layer (Data Access)    │  CRUD operations
├─────────────────────────────────────┤
│  Database Layer (SQLite/SQLModel)  │  Data persistence
└─────────────────────────────────────┘
```

### Pipeline Stages

1. **Fetch**: Reddit API → RawPost table
2. **Detect**: RawPost → Detection Agent → Signal table (if is_signal=True)
3. **Classify**: Signal → Classifier Agent → Update classification + ticket_draft

### Signal Lifecycle

```
new → classified → approved/dismissed → ticket_created
```

### Data Models

- **Signal**: Main entity (customer pain point)
- **RawPost**: Raw Reddit post before detection
- **ConnectorConfig**: Data source configuration
- **PipelineRun**: Execution tracking with activity log

---

## API Quick Reference

### Base URL
`http://localhost:8000`

### Key Endpoints

**Signals**:
- `GET /api/signals` - List signals (filter by status, severity)
- `GET /api/signals/{id}` - Get single signal
- `POST /api/signals/{id}/review` - Review signal (approve/dismiss)
- `POST /api/signals/{id}/create-ticket` - Create GitHub ticket

**Pipeline**:
- `POST /api/pipeline/run` - Start pipeline
- `GET /api/pipeline/status` - Get latest run
- `GET /api/pipeline/runs` - List all runs
- `POST /api/pipeline/runs/{id}/resume` - Resume failed run

**Connectors**:
- `GET /api/connectors` - List connectors
- `POST /api/connectors` - Create connector
- `PUT /api/connectors/{id}` - Update connector
- `POST /api/connectors/{id}/test` - Test connection

**Chat**:
- `POST /api/chat` - SSE streaming chat

**Health**:
- `GET /health` - Health check

---

## Troubleshooting

### Backend Issues

**ModuleNotFoundError**:
```bash
# Always set PYTHONPATH
cd backend && PYTHONPATH=src python ...
```

**Database Issues**:
```bash
# Delete and restart (development only)
rm signal.db
cd backend && PYTHONPATH=src uvicorn signal_app.api.app:app --reload
```

**LLM Errors**:
- Check AWS credentials in `.env`
- Verify region is `us-east-1`
- Check Bedrock model access

**Reddit API Errors**:
- Verify credentials in connector config
- Check rate limits (60 requests/minute)
- Ensure subreddits are accessible

### Frontend Issues

**API Errors**:
- Ensure backend running on port 8000
- Check CORS configuration in `api/app.py`

**Build Errors**:
```bash
# Reinstall dependencies
cd frontend && rm -rf node_modules && npm install
```

**Type Errors**:
- Ensure TypeScript types match API responses
- Run `npm run build` to check types

### Common Errors

**"Cannot retrieve public host/IP"** (Mechanic):
- Use `--remote-transport ssm` flag

**"No bastions found"** (Mechanic):
- Use `--remote-transport ssm` flag

**Pipeline stuck**:
- Check activity log in database
- Resume from last completed stage
- Check error_message field

---

## Additional Resources

### Documentation
- **Detailed Docs**: `.agents/summary/` directory
- **Planning Docs**: `.agents/planning/` directory
- **User Guide**: `README.md`

### External Links
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- SQLModel: https://sqlmodel.tiangolo.com/
- TanStack Query: https://tanstack.com/query/latest
- shadcn/ui: https://ui.shadcn.com/

### Getting Help
- Check `.agents/summary/index.md` for documentation navigation
- Review test files for usage examples
- See `workflows.md` for process flows
- Check `troubleshooting` section above

---

**Built with ❤️ using Kiro AI Assistant**
