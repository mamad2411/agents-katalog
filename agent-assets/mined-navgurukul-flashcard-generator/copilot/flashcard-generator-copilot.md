# Copilot Instructions for Flashcard Generator

## Overview
This is a React + Vite + AWS Amplify application for generating interactive flashcards using the Gemini API. The application allows users to enter topics or term-definition pairs and generates flashcards with a flippable interface.

## Development Guidelines

### Code Quality & Testing Requirements
**ALWAYS follow these testing requirements for any code changes:**

1. **Add Comprehensive Test Cases**: For every new feature, component, or hook added:
   - Write unit tests covering all functions and edge cases
   - Create integration tests for component interactions
   - Add regression tests to prevent future bugs
   - Test both success and error scenarios
   - Verify accessibility requirements

2. **Test Coverage Standards**:
   - All new components must have >90% test coverage
   - All new hooks must have >95% test coverage
   - All new utility functions must have 100% test coverage
   - API integration tests must cover error handling

3. **Testing Patterns to Follow**:
   - Use `@testing-library/react` for component testing
   - Use `vitest` for unit testing
   - Mock external dependencies appropriately
   - Test user interactions and accessibility
   - Verify proper error states and loading states

### Documentation Requirements
**ALWAYS update documentation when making changes:**

1. **Update `docs/updates.md`**: Document every change made including:
   - What was changed and why
   - New features or bug fixes
   - Breaking changes or migration notes
   - Testing approach used
   - Performance implications

2. **Code Documentation**:
   - Add JSDoc comments for all new functions
   - Update README.md if setup instructions change
   - Document any new environment variables or configuration

### Architecture Guidelines

#### Component Structure
- Keep components small and focused (single responsibility)
- Use custom hooks for complex state logic
- Separate business logic from UI components
- Follow React best practices for performance

#### State Management
- Use React hooks for local state
- Custom hooks for shared logic
- Context API for global state (if needed in future)

#### Styling
- Use CSS custom properties for theming
- Maintain responsive design principles
- Follow existing design system patterns
- Ensure light/dark mode compatibility

#### API Integration
- Handle all error states gracefully
- Implement proper loading states
- Use proper TypeScript types for API responses
- Validate API responses before processing

### File Organization
```
src/
├── components/          # React components
├── hooks/              # Custom React hooks  
├── utils/              # Utility functions
├── __tests__/          # Test files
└── assets/             # Static assets
```

### Code Review Checklist
Before submitting any PR, ensure:
- [ ] All tests pass (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] New features have comprehensive tests
- [ ] Documentation is updated in `docs/updates.md`
- [ ] No console errors or warnings
- [ ] Accessibility standards are met
- [ ] Performance impact is considered

### Performance Guidelines
- Lazy load components when appropriate
- Optimize bundle size
- Use React.memo for expensive components
- Implement proper error boundaries
- Monitor Core Web Vitals

### Security Guidelines
- Validate all user inputs
- Sanitize data before display
- Handle API keys securely (client-side storage)
- Follow OWASP security guidelines
- Regular dependency updates and security audits

### AWS Amplify Deployment
- Use the provided `amplify.yml` for build configuration
- Test builds locally before deploying
- Monitor deployment logs for issues
- Ensure environment variables are properly configured

## Current Tech Stack
- **Frontend**: React 19.1.1, Vite 7.1.7
- **Testing**: Vitest, @testing-library/react
- **Styling**: CSS with custom properties
- **API**: Gemini API integration
- **Deployment**: AWS Amplify
- **CI/CD**: GitHub Actions

## API Integration
The app integrates with Google's Gemini API for flashcard generation:
- API key is stored in localStorage
- Proper error handling for API failures
- Parsing and validation of API responses
- Rate limiting considerations

## Contributing
1. Create feature branch from main
2. Make changes following these guidelines
3. Add comprehensive tests
4. Update documentation
5. Submit PR with detailed description
6. Ensure CI passes before merge

Remember: **Quality over speed**. Always prioritize proper testing and documentation over rapid feature delivery.