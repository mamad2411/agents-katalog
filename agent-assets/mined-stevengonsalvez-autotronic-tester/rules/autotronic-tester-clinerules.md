# Project Intelligence and Patterns

## Code Style
- Python 3.9+ syntax is used throughout the project
- Black formatting is applied for consistent code style
- Type hints are used for better code documentation and IDE support
- Docstrings follow Google style with parameter descriptions

## Key Patterns

### Agent Creation Pattern
- Agents should be instantiated with specific roles and responsibilities
- Each agent should have a clear system message defining its purpose
- Tool registration should be done directly with assistant agents

### Error Handling Pattern
- All browser operations should have proper try/except blocks
- Errors should be captured and reported in the test report
- Recovery mechanisms should be attempted where appropriate
- Screenshots should be taken on failures for debugging

### Browser Automation Pattern
- Browser operations should be encapsulated in the PlaywrightSkill class
- All selectors should be properly validated before use
- Timeouts should be configurable and handled gracefully
- Element visibility should be verified before interaction

### Reporting Pattern
- All operations should be logged in the test report
- Screenshots should be taken at key points in test execution
- Test reports should include success/failure status for each step
- Test reports should be saved in a consistent location

## Implementation Guidelines

### AutoGen 0.4 Migration
- Use async/await pattern consistently throughout the codebase
- Replace llm_config with direct model client instantiation
- Use the new message types instead of dictionaries
- Leverage SelectorGroupChat for custom speaker selection

### PlaywrightSkill Integration
- Keep the skill implementation as a standalone class
- Adapt method signatures if needed to work as tools
- Maintain comprehensive error handling
- Keep the reporting integration

### Configuration Management
- Use environment variables for sensitive information like API keys
- Load environment from .env file when available
- Make timeouts and other parameters configurable

## User Preferences
- Console output should be detailed enough to track progress
- Error messages should be clear and actionable
- Screenshots should be taken automatically on failures
- Test reports should be comprehensive but readable

## Known Challenges
- Selectors can be brittle when websites change
- LLM tokens can be exceeded with long conversations
- Browser automation can be flaky with dynamic websites
- Error recovery can sometimes lead to unexpected states
