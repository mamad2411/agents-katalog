# Testing & Quality Assurance

## 🧪 Testing Strategy Overview

### Testing Pyramid
1. **Unit Tests** (70%) - Fast, isolated, comprehensive
2. **Integration Tests** (20%) - Service interactions, database operations
3. **End-to-End Tests** (10%) - User workflows, critical paths

### Testing Types by Technology

#### Frontend Testing
- **Unit Tests**: Component testing, utility functions
- **Integration Tests**: API integration, state management
- **E2E Tests**: User workflows, cross-browser compatibility
- **Visual Tests**: UI regression testing, design consistency

#### Backend Testing
- **Unit Tests**: Business logic, utility functions
- **Integration Tests**: API endpoints, database operations
- **Contract Tests**: API contracts, service interfaces
- **Performance Tests**: Load testing, stress testing

#### Mobile Testing
- **Unit Tests**: Business logic, utility functions
- **Integration Tests**: API integration, local storage
- **E2E Tests**: User workflows, device compatibility
- **Device Tests**: Cross-device testing, platform-specific features

## 🛠️ Testing Tools & Frameworks

### JavaScript/TypeScript Testing
- **Jest**: Unit testing, mocking, code coverage
- **React Testing Library**: Component testing, user behavior
- **Playwright**: E2E testing, cross-browser compatibility
- **Cypress**: E2E testing, visual regression testing

### Python Testing
- **pytest**: Unit testing, fixtures, parametrization
- **unittest**: Standard library testing framework
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking and patching

### Java Testing
- **JUnit 5**: Unit testing, parameterized tests
- **Mockito**: Mocking and stubbing
- **TestContainers**: Integration testing with containers
- **Selenium**: Web application testing

### Go Testing
- **testing**: Standard library testing package
- **testify**: Assertions and mocking
- **gomock**: Interface mocking
- **httptest**: HTTP testing utilities

## 📋 Testing Implementation Guidelines

### 1. Unit Testing
- **Coverage Target**: Minimum 80% code coverage
- **Test Isolation**: Each test should be independent
- **Mocking Strategy**: Mock external dependencies
- **Assertion Quality**: Test behavior, not implementation

### 2. Integration Testing
- **Database Testing**: Use test databases or containers
- **API Testing**: Test service interactions
- **External Services**: Mock or use test environments
- **Data Setup**: Use fixtures and test data

### 3. End-to-End Testing
- **Critical Paths**: Focus on user workflows
- **Cross-Browser**: Test major browsers
- **Mobile Testing**: Test responsive design
- **Performance**: Monitor test execution time

## 🚀 Testing Workflow

### 1. Test-Driven Development (TDD)
```bash
# Red: Write failing test
# Green: Write minimal code to pass
# Refactor: Improve code quality
```

### 2. Test Execution
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test files
npm test -- --testPathPattern=user
```

### 3. Continuous Integration
- Run tests on every commit
- Block merges on test failures
- Generate coverage reports
- Track test performance metrics

## 📊 Quality Metrics

### Code Quality Metrics
- **Code Coverage**: Minimum 80% target
- **Test Execution Time**: Fast feedback loop
- **Test Reliability**: Flaky test detection
- **Code Complexity**: Cyclomatic complexity tracking

### Performance Metrics
- **Response Time**: API response times
- **Throughput**: Requests per second
- **Resource Usage**: Memory and CPU utilization
- **Scalability**: Performance under load

### Security Metrics
- **Vulnerability Scanning**: Automated security testing
- **Code Analysis**: Static application security testing
- **Dependency Scanning**: Known vulnerability detection
- **Penetration Testing**: Manual security assessment

## 🔍 Testing Best Practices

### Test Organization
- **Test Structure**: Mirror source code structure
- **Naming Convention**: Descriptive test names
- **Test Data**: Use factories and fixtures
- **Test Categories**: Group by functionality

### Test Maintenance
- **Regular Updates**: Keep tests current with code
- **Refactoring**: Improve test quality over time
- **Documentation**: Document complex test scenarios
- **Review Process**: Include tests in code reviews

### Performance Testing
- **Load Testing**: Test under expected load
- **Stress Testing**: Test beyond capacity limits
- **Spike Testing**: Test sudden load increases
- **Endurance Testing**: Test over extended periods

## 🧹 Quality Assurance Process

### 1. Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Error handling is implemented
- [ ] Security considerations are addressed
- [ ] Performance implications are considered

### 2. Pre-commit Hooks
- Run linting tools
- Execute unit tests
- Check code formatting
- Validate commit messages
- Scan for sensitive data

### 3. Automated Quality Gates
- Code coverage thresholds
- Test execution time limits
- Security vulnerability checks
- Performance regression detection
- Documentation completeness

## 🔧 Testing Tools Configuration

### Jest Configuration
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

### pytest Configuration
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=html
    --cov-report=term-missing
```

## 📚 Reference Materials

### Documentation
- [README.md](mdc:README.md) - Project overview
- [FOLDER_STRUCTURE.md](mdc:FOLDER_STRUCTURE.md) - Project structure
- [FRAMEWORK_SUMMARY.md](mdc:FRAMEWORK_SUMMARY.md) - Framework capabilities

### Testing Tools
- `npm test` - Run JavaScript tests
- `python -m pytest` - Run Python tests
- `go test ./...` - Run Go tests
- `mvn test` - Run Java tests

### Quality Tools
- `npm run lint` - Code linting
- `npm run format` - Code formatting
- `npm run validate` - Project validation
- Coverage reports in `coverage/` directory

## 🎯 When to Apply Testing Standards

- Writing new code or features
- Refactoring existing code
- Setting up new projects
- Implementing CI/CD pipelines
- Conducting code reviews
- Planning testing strategies
description:
globs:
alwaysApply: true
---
