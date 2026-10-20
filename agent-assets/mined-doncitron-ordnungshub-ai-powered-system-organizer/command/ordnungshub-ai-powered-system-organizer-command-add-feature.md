// Command: /add-feature
// Description: Add a new feature with full test coverage

You are implementing a new feature for OrdnungsHub. Follow these steps:

1. **Requirements Analysis**
   - Understand the feature requirements completely
   - Identify affected components (frontend/backend/both)
   - List any new dependencies needed

2. **Design Phase**
   - Create API contract if backend is involved
   - Design component structure for frontend
   - Plan data flow and state management

3. **Implementation**
   - Start with backend API endpoints (if applicable)
   - Write comprehensive tests FIRST (TDD approach)
   - Implement the feature to pass tests
   - Add frontend components with TypeScript
   - Include proper error handling

4. **Testing**
   - Unit tests with >85% coverage
   - Integration tests for API endpoints
   - Frontend component tests with React Testing Library
   - Manual testing checklist

5. **Documentation**
   - Update API documentation
   - Add JSDoc/docstrings
   - Update CLAUDE.md if major feature
   - Create user-facing documentation

Example structure for a file upload feature:
```
Backend:
- POST /api/files/upload
- File validation service
- Storage service with progress tracking
- Comprehensive test suite

Frontend:
- FileUploadComponent.tsx
- useFileUpload hook
- Progress indicator
- Error handling UI
```

Remember:
- Always provide AI and non-AI implementations
- Follow existing patterns in the codebase
- Consider security implications
- Test edge cases thoroughly
