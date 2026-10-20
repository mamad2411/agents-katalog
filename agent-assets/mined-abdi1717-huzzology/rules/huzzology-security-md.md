---
description: 
globs: 
alwaysApply: true
---
# Security and Privacy Rules

## Authentication and Authorization
- Implement strong authentication mechanisms
- Use multi-factor authentication where appropriate
- Follow principle of least privilege
- Implement proper session management
- Use secure token storage
- Implement proper logout functionality
- Handle password security correctly
- Use OAuth/OIDC for third-party auth

## Input Validation and Sanitization
- Validate all inputs on server side
- Sanitize data before processing
- Use parameterized queries for SQL
- Implement proper encoding/escaping
- Validate file uploads strictly
- Check data types and ranges
- Use allowlist validation approach
- Implement rate limiting

## Data Protection
- Encrypt sensitive data at rest
- Use TLS for data in transit
- Implement proper key management
- Follow data minimization principles
- Implement data retention policies
- Use secure random number generation
- Hash passwords with strong algorithms
- Protect personally identifiable information

## Common Vulnerabilities Prevention
- Prevent SQL injection attacks
- Protect against XSS attacks
- Implement CSRF protection
- Prevent directory traversal
- Protect against XXE attacks
- Implement proper CORS policies
- Prevent command injection
- Protect against deserialization attacks

## Secrets Management
- Never hardcode secrets in source code
- Use environment variables appropriately
- Implement proper secrets rotation
- Use dedicated secrets management tools
- Encrypt secrets at rest
- Implement proper access controls
- Audit secrets access
- Use service accounts appropriately

## API Security
- Implement proper API authentication
- Use API rate limiting
- Validate API inputs thoroughly
- Implement proper error handling
- Use HTTPS for all API endpoints
- Implement API versioning
- Monitor API usage patterns
- Document security requirements

## Logging and Monitoring
- Log security-relevant events
- Never log sensitive information
- Implement centralized logging
- Monitor for suspicious activities
- Implement alerting for security events
- Use structured logging
- Implement log retention policies
- Protect log files appropriately
## Compliance and Standards
- Follow relevant security standards
- Implement privacy by design
- Document security decisions
- Conduct regular security reviews
- Implement vulnerability scanning
- Follow secure development lifecycle
- Maintain security documentation
- Implement incident response procedures
