# Deed Reader Pro - Cursor Development Rules

## Project Context
You are working on Deed Reader Pro, an AI-powered deed parsing and visualization application for land surveyors. The app processes property deed documents, extracts bearing/distance data, and creates visual plots.

## Current Tech Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Flask (migrating to FastAPI) + Python 3.11+
- **AI**: Anthropic Claude API for document analysis
- **Database**: SQLite (migrating to PostgreSQL)
- **File Storage**: Local (migrating to Cloudflare R2)

## Development Guidelines

### Always Follow These Rules
1. **Use TypeScript** for all frontend code with strict mode enabled
2. **Use Python type hints** for all backend code
3. **Test every feature** - aim for 80% code coverage
4. **Document complex logic** inline with clear comments
5. **Handle errors gracefully** with user-friendly messages

### Code Style
- Frontend: Follow React best practices, use functional components with hooks
- Backend: Follow PEP 8, use async/await for I/O operations
- Use meaningful variable names that reflect deed/surveying domain

### When Writing Code
- Always consider surveyor workflows and terminology
- Optimize for accuracy in deed parsing (bearings, distances, monuments)
- Ensure UI is intuitive for non-technical users
- Keep API responses under 200ms for good UX

### AI Integration Best Practices
- Cache Claude API responses to reduce costs
- Implement retry logic with exponential backoff
- Always have fallback options when AI fails
- Use structured prompts for consistent results

### Common Patterns
```python
# Backend: Always validate deed data
def parse_bearing(bearing_str: str) -> float:
    """Parse bearing string to decimal degrees.
    Handles formats: N45°30'E, 45.5, N45-30-00E
    """
    # Implementation here

# Frontend: Always show loading states
const DeedUpload: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Component logic
};
```

### Domain Knowledge
- **Bearings**: Directions from north (0-360° or quadrant format)
- **Distances**: Measurements in feet, chains, varas, etc.
- **Monuments**: Physical markers (iron pins, trees, stones)
- **Closure**: When deed boundary forms a closed polygon
- **Metes and Bounds**: Legal description using bearings/distances

### Current Development Phase
Refer to CURSOR_RULES_TASKS.md for current phase and active tasks.

### Testing Requirements
- Unit tests for all parsing functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Manual testing with real deed documents

### Performance Targets
- Deed processing: <30 seconds
- Plot rendering: <2 seconds
- API response: <200ms
- 99.9% uptime

### Security Considerations
- Validate all file uploads (PDF, PNG, JPG, TIFF)
- Sanitize user inputs to prevent injection
- Use environment variables for API keys
- Implement rate limiting on endpoints

### When You're Stuck
1. Check existing code patterns in the codebase
2. Refer to deed surveying documentation
3. Ask about surveyor workflows and needs
4. Consider edge cases in deed formats

### Remember
This tool is for professional surveyors who need accurate, fast deed processing. Every feature should save them time and reduce errors in their daily work. 