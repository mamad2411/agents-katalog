# Claude Code Context for OrdnungsHub

## Project Overview

OrdnungsHub is an AI-powered desktop application designed to help users organize their digital workspace efficiently. It combines local AI processing with intelligent file management and system optimization tools.

### Tech Stack
- **Frontend**: Electron + React + TypeScript + Webpack
- **Backend**: Python FastAPI with async support
- **AI Integration**: Enhanced AI service with sklearn support
- **Testing**: Jest (frontend), pytest (backend), Playwright (e2e)
- **Development**: Docker support, CI/CD pipelines

## Architecture

```
ordnungshub/
├── src/
│   ├── backend/          # Python FastAPI backend
│   │   ├── api/         # API endpoints
│   │   ├── services/    # Business logic (AI, file management)
│   │   └── models/      # Data models
│   ├── frontend/        # Electron + React frontend
│   │   ├── components/  # React components
│   │   ├── services/    # Frontend services
│   │   └── main.js      # Electron main process
│   └── core/           # Shared utilities
├── tests/              # Test suites
└── .claude/           # Claude Code configuration
```

## Key Features

1. **Smart File Categorization**: AI-powered automatic file organization
2. **Intelligent Search**: Semantic search with vector embeddings
3. **Automation Suggestions**: Pattern recognition for workflow optimization
4. **Cross-Platform**: Electron ensures Windows/Mac/Linux compatibility

## Development Patterns

### Backend Patterns

```python
# Service pattern with AI fallback
class EnhancedService:
    def __init__(self):
        self.ai_available = self._check_ai_deps()
    
    def process(self, data):
        if self.ai_available:
            return self._ai_process(data)
        return self._fallback_process(data)
```

### Frontend Patterns

```typescript
// Component pattern with TypeScript
interface ComponentProps {
    data: DataType;
    onAction: (result: ResultType) => void;
}

const SmartComponent: React.FC<ComponentProps> = ({ data, onAction }) => {
    // Implementation
};
```

### API Patterns

```python
# FastAPI async endpoint pattern
@router.post("/api/categorize")
async def categorize_files(request: CategorizeRequest):
    result = await ai_service.categorize_async(request.files)
    return {"categories": result}
```

## Coding Standards

### Python
- Use type hints for all functions
- Async/await for I/O operations
- Handle sklearn availability gracefully
- Follow PEP 8 with 88-char line limit (Black formatter)

### TypeScript/React
- Functional components with hooks
- Strict TypeScript mode enabled
- Props interfaces for all components
- CSS modules for styling

### Testing
- Minimum 85% coverage for new features
- Unit tests for all services
- Integration tests for API endpoints
- E2E tests for critical user flows

## Security Considerations

- All file operations must respect `allowedDirectories` configuration
- Authentication required for sensitive endpoints
- Input validation on all user data
- Secrets stored in environment variables only

## Performance Requirements

- File scanning: < 1000ms for 10,000 files
- API response time: < 200ms average
- UI rendering: 60fps target
- Memory usage: < 500MB idle

## Common Tasks

### Adding a New Feature
1. Design API contract first
2. Implement backend service with tests
3. Create frontend components
4. Add integration tests
5. Update documentation

### Debugging Issues
1. Check logs in `ordnungshub.log`
2. Use test backend for isolation: `python test_backend.py`
3. Frontend debugging: Chrome DevTools in Electron

### Deployment
1. Run all tests: `npm test && python -m pytest`
2. Build frontend: `npm run build`
3. Package Electron: `npm run build:electron`
4. Docker deployment: `docker-compose up`

## Environment Variables

```env
# Backend
PYTHONPATH=.
DATABASE_URL=sqlite:///ordnungshub.db
AI_MODEL_PATH=./models
LOG_LEVEL=INFO

# Frontend
NODE_ENV=development
REACT_APP_API_URL=http://localhost:8001
```

## Important Files

- `src/backend/services/enhanced_ai_service.py` - Core AI logic
- `src/frontend/components/FileManager.tsx` - Main UI component
- `test_backend.py` - Mock backend for development
- `.claude/workflows/claude-code-flow.json` - Workflow configuration

## Known Issues & Constraints

1. Large file scanning can block UI - needs worker thread
2. AI models are optional - always provide fallbacks
3. Electron security - follow best practices for IPC
4. Cross-platform paths - use Path objects

## Future Enhancements

1. Real-time collaboration features
2. Cloud sync capabilities
3. Plugin system for extensibility
4. Advanced ML models for better categorization

## Testing Strategy

### Unit Tests
```bash
# Backend
python -m pytest tests/unit/ -v

# Frontend
npm run test:unit
```

### Integration Tests
```bash
# Full stack
npm run test:integration
```

### Manual Testing
1. File upload and categorization flow
2. Search functionality across file types
3. Performance with large datasets
4. Cross-platform compatibility

## Debugging Commands

```bash
# Quick backend test
python test_backend.py

# Frontend only
npm run dev:react

# Check AI service
python -c "from src.backend.services.enhanced_ai_service import EnhancedAIService; print(EnhancedAIService().test())"

# Reset everything
pkill -f uvicorn && pkill -f webpack
```

## Claude Code Specific Instructions

When implementing features:
1. Always check existing patterns in similar files
2. Maintain consistent error handling
3. Add appropriate logging for debugging
4. Consider both AI-available and fallback scenarios
5. Write tests alongside implementation
6. Update this document when adding major features

For file operations:
- Use `pathlib.Path` for cross-platform compatibility
- Check permissions before operations
- Provide progress feedback for long operations
- Handle errors gracefully with user-friendly messages

For AI integration:
- Check model availability before use
- Provide meaningful fallbacks
- Log AI decisions for debugging
- Monitor performance impact
