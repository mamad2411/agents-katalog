---
applyTo: "**/*.{ts,js}"
---

# Security Guidelines for Express Boilerplate

## Core Security Libraries
- **Helmet**: Security headers middleware (already configured in `src/app/app.ts`)
- **CORS**: Cross-origin resource sharing control (configured for GraphQL and REST)
- **Celebrate/Joi**: Input validation and sanitization
- **TypeORM**: Built-in SQL injection protection with parameterized queries
- **Body-parser**: Request body parsing with size limits

## Authentication & Authorization

### JWT Implementation
- Use JWT tokens for stateless authentication across REST and GraphQL endpoints
- Store JWT secret in environment variables (never in code)
- Implement token expiration (access) and refresh token mechanisms
- Extract user information from validated JWT tokens in middleware

### Authentication Patterns
```typescript
// Example authentication middleware
export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    throw new HttpError('Unauthorized', StatusCodes.UNAUTHORIZED);
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    throw new HttpError('Invalid token', StatusCodes.UNAUTHORIZED);
  }
};
```

### Authorization Patterns
- Implement role-based access control (RBAC) using user roles from JWT payload
- Create authorization middleware for different permission levels
- Use route-level authorization guards in routing files

### Authentication Endpoints
Authentication endpoints must return structured token responses:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### User Profile Endpoints
- Always implement `/me` endpoint for authenticated user profile retrieval
- Return sanitized user data (exclude passwords, internal IDs)
- Support profile updates with proper validation

## Input Validation & Sanitization

### Celebrate/Joi Validation
All endpoints must use Celebrate validation middleware:
```typescript
export const createUserValidation = celebrate({
  body: Joi.object().keys({
    email: Joi.string().email().required(),
    password: Joi.string().min(8).required(),
    firstName: Joi.string().trim().min(1).max(50).required(),
    lastName: Joi.string().trim().min(1).max(50).required(),
  }),
});
```

### Validation Security Rules
- Sanitize all string inputs using `Joi.string().trim()`
- Set maximum lengths for all string fields to prevent DoS
- Use strict type validation (no implicit type conversion)
- Validate nested objects and arrays with specific schemas
- Implement custom validation for business rules

### File Upload Security
- Validate file types using MIME type checking
- Implement file size limits
- Scan uploaded files for malware
- Store files outside the web root
- Use secure file naming conventions

## Password Security

### Password Hashing
- **Never store passwords in plain text**
- Use bcrypt with minimum 12 rounds for password hashing
- Implement password strength requirements (minimum 8 characters, complexity)
- Use secure password reset mechanisms with time-limited tokens

### Example Password Handling
```typescript
import bcrypt from 'bcrypt';

// Hashing password
const hashPassword = async (password: string): Promise<string> => {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
};

// Verifying password
const verifyPassword = async (password: string, hash: string): Promise<boolean> => {
  return bcrypt.compare(password, hash);
};
```

## Security Headers Configuration

### Helmet Configuration
Helmet is configured in `src/app/app.ts` with Content Security Policy:
```typescript
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        scriptSrc: ["'self'", "https: 'unsafe-inline'"],
      },
    },
  }),
);
```

### Additional Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (for HTTPS)
- `Referrer-Policy: no-referrer`

## CORS Configuration

### CORS Setup
Configure CORS for both REST API and GraphQL endpoints:
```typescript
// Basic CORS for REST API
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
  optionsSuccessStatus: 200,
}));

// GraphQL CORS
app.use('/graphql', cors<cors.CorsRequest>());
```

### CORS Best Practices
- Define explicit allowed origins (avoid wildcard `*` in production)
- Enable credentials only when necessary
- Configure allowed methods and headers specifically
- Use environment variables for origin configuration

## Environment Variables Security

### Sensitive Data Management
- Store all secrets in environment variables, never in code
- Use `.env.dist` as template, never commit actual `.env` files
- Validate all environment variables using Joi schemas in config files
- Use different environments for development, staging, and production

### Required Security Environment Variables
```bash
# Authentication
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=3600

# API Security
AUTH_API_KEY=your_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Database (use separate credentials for each environment)
RDS_USERNAME=your_db_user
RDS_PASSWORD=your_secure_db_password
```

## Database Security

### TypeORM Security
- Use parameterized queries (TypeORM default behavior)
- Implement proper indexing for performance and security
- Use database connection pooling with limits
- Enable query logging only in development environments

### Entity Security
```typescript
@Entity('users')
export class User {
  @PrimaryColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column({ select: false }) // Exclude from default selections
  password: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

## API Security

### Rate Limiting
- Implement rate limiting for all public endpoints
- Use different limits for authenticated vs. anonymous users
- Implement progressive delays for failed authentication attempts

### API Key Management
- Use API keys for service-to-service communication
- Rotate API keys regularly
- Implement API key scoping for different access levels

### Request Security
- Implement request size limits using body-parser configuration
- Validate Content-Type headers
- Log and monitor suspicious request patterns

## Container Security

### Docker Security
The production Dockerfile implements security best practices:
- Uses non-root user (`USER node`)
- Sets proper file ownership (`--chown=node:node`)
- Uses Alpine Linux base images for smaller attack surface
- Implements multi-stage builds to reduce final image size

### Container Best Practices
- Run applications as non-privileged user
- Use specific image tags, not `latest`
- Regularly update base images
- Scan images for vulnerabilities
- Use read-only file systems when possible

## Logging & Monitoring

### Security Logging
- Log all authentication attempts (success and failure)
- Log authorization failures
- Log input validation failures
- Monitor for unusual patterns or potential attacks
- Use structured logging format for easier analysis

### Log Security
- Never log sensitive information (passwords, tokens, personal data)
- Use log rotation and retention policies
- Secure log storage and access
- Implement log integrity checks

## Security Testing

### Security Test Requirements
- Test authentication and authorization flows
- Validate input sanitization and validation
- Test error handling for security scenarios
- Implement penetration testing for critical endpoints

### Example Security Tests
```typescript
describe('Authentication Security', () => {
  it('should reject invalid JWT tokens', async () => {
    const response = await request(app)
      .get('/api/protected')
      .set('Authorization', 'Bearer invalid_token')
      .expect(401);
  });

  it('should prevent SQL injection in user input', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    const response = await request(app)
      .post('/api/users')
      .send({ name: maliciousInput })
      .expect(400);
  });
});
```

## Security Checklist

### Pre-deployment Security Checks
- [ ] All secrets stored in environment variables
- [ ] Input validation implemented for all endpoints
- [ ] Authentication and authorization working correctly
- [ ] Security headers configured properly
- [ ] CORS configured for production origins
- [ ] Database queries use parameterized statements
- [ ] Passwords are properly hashed
- [ ] API rate limiting implemented
- [ ] Security tests passing
- [ ] Container runs as non-root user
- [ ] Dependencies scanned for vulnerabilities

### Regular Security Maintenance
- [ ] Update dependencies regularly
- [ ] Rotate secrets and API keys
- [ ] Review and update CORS origins
- [ ] Monitor security logs
- [ ] Conduct security audits
- [ ] Update security headers as needed
- [ ] Test backup and recovery procedures