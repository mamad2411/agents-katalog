---
description: 
globs: 
alwaysApply: true
---
# Error Handling and Debugging Rules

## Error Handling Principles
- Fail fast and fail clearly
- Handle errors at appropriate levels
- Provide meaningful error messages
- Log errors with sufficient context
- Never swallow exceptions silently
- Use appropriate error types
- Implement graceful degradation
- Plan for error recovery

## Exception Handling Patterns
- Use try-catch blocks appropriately
- Catch specific exceptions, not generic ones
- Re-throw exceptions with additional context
- Use finally blocks for cleanup
- Implement proper resource disposal
- Avoid using exceptions for control flow
- Document expected exceptions
- Use error codes when appropriate

## Logging Best Practices
- Use structured logging
- Include relevant context in logs
- Use appropriate log levels
- Never log sensitive information
- Include correlation IDs
- Log at application boundaries
- Use consistent log formats
- Implement log rotation

## Debugging Guidelines
- Use debugger effectively
- Add strategic logging statements
- Reproduce issues systematically
- Use unit tests to isolate problems
- Check error logs thoroughly
- Verify assumptions with data
- Use profiling tools when needed
- Document debugging findings

## Error Recovery Strategies
- Implement retry mechanisms with backoff
- Use circuit breaker patterns
- Implement fallback mechanisms
- Design for partial failures
- Use bulkhead patterns for isolation
- Implement timeout handling
- Plan for cascading failure prevention
- Test failure scenarios
## User-Facing Error Handling
- Provide helpful error messages
- Avoid exposing system internals
- Guide users toward resolution
- Implement proper validation feedback
- Use progressive error disclosure
- Provide error recovery options
- Log user errors for analysis
- Implement error reporting mechanisms

## API Error Handling
- Use appropriate HTTP status codes
- Provide consistent error response format
- Include error codes and messages
- Provide troubleshooting guidance
- Implement rate limiting errors
- Handle timeouts appropriately
- Validate inputs thoroughly
- Document error responses

## Monitoring and Alerting
- Set up error rate monitoring
- Implement alerting thresholds
- Track error patterns and trends
- Monitor system health metrics
- Implement automated error detection
- Use distributed tracing for complex errors
- Set up dashboards for error visibility
- Implement incident response procedures

## Testing Error Conditions
- Test error paths explicitly
- Use fault injection testing
- Test resource exhaustion scenarios
- Verify error message accuracy
- Test error recovery mechanisms
- Use chaos engineering principles
- Test timeout and retry logic
- Validate error logging functionality
