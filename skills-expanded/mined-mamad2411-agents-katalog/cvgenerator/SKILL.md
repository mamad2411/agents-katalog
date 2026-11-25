# AI Cover Letter Generator - Cursor Rules

## Project Overview
This is a full-stack AI application that generates personalized cover letters using Claude and ChatGPT APIs.

## Tech Stack
- **Backend**: FastAPI (Python 3.9+), Pydantic, Anthropic SDK, OpenAI SDK
- **Frontend**: React 18, Vite, Tailwind CSS, Axios, React Hook Form
- **Architecture**: Service layer pattern, RESTful API, Component-based UI

## Code Style Guidelines

### Python (Backend)
- Use type hints for all functions and variables
- Follow PEP 8 style guide
- Use async/await for I/O operations
- Pydantic models for all data validation
- Docstrings for all public functions
- Keep functions under 50 lines when possible

### JavaScript (Frontend)
- Use functional components with hooks (no class components)
- Follow ESLint rules
- Use arrow functions
- Destructure props
- Keep components under 200 lines
- Use const/let (never var)

### General
- Use meaningful variable names
- Write comments for complex logic
- Keep files focused on single responsibility
- DRY principle (Don't Repeat Yourself)

## Project Structure Rules

### Backend
```
app/
├── api/          # HTTP endpoints only
├── services/     # Business logic, external API calls
├── models.py     # Data models (request/response)
├── config.py     # Configuration management
└── utils/        # Helper functions
```

### Frontend
```
src/
├── components/   # React components (one per file)
├── services/     # API client, external services
└── utils/        # Helper functions
```

## Development Conventions

### Adding New Features
1. Backend first: Create models → service → routes
2. Test with Swagger UI (/docs)
3. Frontend: API client → component
4. Test in browser

### File Naming
- Python: `snake_case.py`
- JavaScript: `PascalCase.jsx` for components, `camelCase.js` for utilities
- Use descriptive names: `cover_letter_form.jsx` not `form.jsx`

### Import Order
**Python:**
```python
# 1. Standard library
import os
from typing import Optional

# 2. Third-party
from fastapi import APIRouter
from pydantic import BaseModel

# 3. Local
from ..models import CoverLetterRequest
from ..services import ai_service
```

**JavaScript:**
```javascript
// 1. React
import { useState, useEffect } from 'react';

// 2. Third-party
import axios from 'axios';
import toast from 'react-hot-toast';

// 3. Local
import { coverLetterAPI } from '../services/api';
import Header from './Header';
```

### Error Handling
- Always use try-catch for async operations
- Provide user-friendly error messages
- Log errors for debugging
- Use appropriate HTTP status codes

### Environment Variables
- Never commit secrets
- Use `.env` for local development
- Document all required env vars in `.env.example`
- Validate env vars at startup

## API Design Principles
- RESTful endpoints
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return consistent response formats
- Include proper status codes
- Validate all inputs with Pydantic

## UI/UX Guidelines
- Mobile-first responsive design
- Loading states for all async operations
- Error messages should be helpful
- Use toast notifications for feedback
- Maintain consistent spacing (Tailwind)
- Accessible (semantic HTML, ARIA labels)

## Testing Strategy (when adding tests)
- Unit tests for services and utils
- Integration tests for API endpoints
- Component tests for React components
- Mock external API calls
- Test error cases

## Git Workflow
- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Meaningful commit messages
- Keep commits focused and atomic

## Performance Considerations
- Use async/await in backend
- Minimize API calls
- Implement caching where appropriate
- Lazy load components when possible
- Optimize images and assets

## Security Best Practices
- Validate all user inputs
- Sanitize data before displaying
- Use environment variables for secrets
- Implement rate limiting (future)
- Keep dependencies updated

## Documentation
- Update README when adding features
- Comment complex algorithms
- Use docstrings/JSDoc
- Keep API documentation current

## Deployment Checklist
- [ ] Update ENVIRONMENT to 'production'
- [ ] Set secure SECRET_KEY
- [ ] Configure ALLOWED_ORIGINS
- [ ] Test all features
- [ ] Check for console errors
- [ ] Verify API keys are working

## Common Commands
```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Full setup
./setup.sh
```

## Dependencies Management
- Pin versions in requirements.txt and package.json
- Update dependencies monthly
- Test after updating dependencies
- Document breaking changes

## AI Integration Notes
- Always handle API timeouts
- Implement retry logic for failures
- Monitor API usage/costs
- Cache repeated requests (future)
- Validate AI responses

## React Patterns
- Use hooks (useState, useEffect, custom hooks)
- Keep state close to where it's used
- Lift state up when sharing between components
- Use controlled components for forms
- Memoize expensive calculations

## Tailwind Best Practices
- Use utility classes directly
- Custom components in @layer components
- Use theme colors from config
- Responsive design: mobile-first with sm/md/lg breakpoints

## Future Enhancements Priority
1. User authentication (JWT)
2. Database integration (PostgreSQL)
3. Cover letter history
4. A/B testing of generated letters
5. LinkedIn profile integration
6. Email sending capability

## Getting Help
- Check SETUP_GUIDE.md for setup issues
- See FEATURES.md for feature documentation
- Review INTERVIEW_PREP.md for technical deep-dives
- Use /docs endpoint for API reference

---

**Remember**: This project demonstrates full-stack skills, AI integration, and modern web development practices. Keep code clean, documented, and maintainable!

