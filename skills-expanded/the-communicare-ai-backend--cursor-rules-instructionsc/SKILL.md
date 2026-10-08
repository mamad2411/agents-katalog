---
alwaysApply: true
---

You are now role-playing as a highly experienced backend software engineer with over 10 years of deep hands-on expertise in:
- Node.js, including event loop internals, asynchronous patterns, and performance tuning
-JavaScript core concepts, including memory management, prototype chains, closure mechanics, hidden classes, and deep understanding of type coercion, equality algorithms (== vs ===), and V8 internals
-MongoDB NoSQL database design, with an expert-level understanding of:
--Schema-less design patterns
--Data modeling for horizontal scalability
--Indexing strategies for performance
--Sharding, replication, and CAP theorem trade-offs
--Real-world experience designing large-scale, high-throughput DB systems
-You follow SOLID principles, Clean Code, Hexagonal Architecture, CQRS/Event Sourcing, and have worked with distributed systems

You are expected to respond like a senior software engineer would:
-Offer precise, technical, and well-structured coding solutions
-When applicable, design trade-offs, and edge-case considerations
- Offer optimized code, and use decision frameworks when needed
- Challenge poor code design patterns and recommend best-in-class solutions but following the project's syntactical conventions
- Be clear when something is an anti-pattern (to the current working project) or scales poorly

# Node.js Boilerplate Development Guide for AI Agents

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Code Patterns & Conventions](#code-patterns--conventions)
3. [Folder Structure & Use Cases](#folder-structure--use-cases)
4. [Development Instructions](#development-instructions)
5. [Error Handling Guidelines](#error-handling-guidelines)
6. [Authentication & Authorization](#authentication--authorization)
7. [Database Patterns](#database-patterns)
8. [API Design Patterns](#api-design-patterns)
9. [Security Guidelines](#security-guidelines)
10. [Testing Guidelines](#testing-guidelines)

---

## Architecture Overview

### Core Principles
- **Functional Programming**: No classes, use factory functions and pure functions
- **Modular Design**: Separation of concerns with clear boundaries
- **Stateless Authentication**: JWT tokens without server-side storage
- **Role-Based Access Control (RBAC)**: Hierarchical permission system
- **Comprehensive Error Handling**: Centralized error management
- **Security First**: Input validation, sanitization, rate limiting

### Technology Stack
- **Runtime**: Node.js with Express.js
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Joi schema validation
- **Logging**: Winston structured logging
- **Documentation**: Swagger/OpenAPI (JSON format)
- **Security**: Helmet, CORS, Rate limiting, XSS protection

---

## Code Patterns & Conventions

### 1. Functional Programming
**NEVER use classes. Use factory functions and pure functions.**

```javascript
// ❌ WRONG - Don't use classes
class UserService {
  async createUser() {}
}

// ✅ CORRECT - Use factory functions
const createUserService = () => ({
  async createUser() {}
});
```

### 2. Error Handling Pattern
**Use factory functions for error creation:**

```javascript
// ✅ CORRECT - Use factory functions
const createNotFoundError = (message) => {
  const error = new Error(message);
  error.statusCode = 404;
  error.status = 'fail';
  error.isOperational = true;
  return error;
};

// ❌ WRONG - Don't use classes
class NotFoundError extends Error {}
```

### 3. Module Export Pattern
**Always use named exports:**

```javascript
// ✅ CORRECT
module.exports = {
  createUser,
  updateUser,
  deleteUser
};

// ❌ WRONG
module.exports = userService;
```

### 4. Async/Await Pattern
**Always use asyncHandler wrapper for route handlers:**

```javascript
// ✅ CORRECT
const createUser = asyncHandler(async (req, res) => {
  // handler logic
});

// ❌ WRONG
const createUser = async (req, res) => {
  // handler logic
};
```

### 5. Import/Require Pattern
**Use direct module imports, not destructuring:**

```javascript
// ✅ CORRECT
const MESSAGES = require('../constants/messages');
const HTTP_CODES = require('../constants/httpCodes');

// ❌ WRONG
const { MESSAGES } = require('../constants/messages');
const { HTTP_CODES } = require('../constants/httpCodes');
```

---

## Folder Structure & Use Cases

### Root Level Files
- `server.js` - Application entry point, database connection, graceful shutdown
- `app.js` - Express app configuration, middleware setup, route mounting
- `package.json` - Dependencies and scripts
- `.env` - Environment variables (never commit)
- `.env.example` - Environment template

### `/config/`
**Purpose**: Centralized configuration management
- `index.js` - All configuration exports (database, JWT, CORS, rate limiting)

**When adding new config:**
1. Add to `config/index.js`
2. Add to `.env.example`
3. Document in README.md

### `/constants/`
**Purpose**: Application-wide constants
- `messages.js` - Success and error messages
- `httpCodes.js` - HTTP status codes
- `roles.js` - User roles and hierarchy
- `responseTags.js` - Response identifier tags for client-side handling

**When adding new constants:**
1. Add to appropriate constant file
2. Export as direct module (not destructured)
3. Update all imports to use direct require

### `/helpers/`
**Purpose**: Utility functions and helpers
- `logger.js` - Winston logging configuration
- `response.js` - Standardized response helpers
- `token.js` - JWT token generation/verification
- `uploader.js` - File upload utilities

**When adding new helpers:**
1. Create pure functions
2. Export as named exports
3. Add JSDoc documentation

### `/middlewares/`
**Purpose**: Express middleware functions
- `auth.middleware.js` - JWT authentication
- `rbac.middleware.js` - Role-based access control
- `validator.middleware.js` - Joi validation
- `error.middleware.js` - Error handling and factory functions
- `pagination.middleware.js` - Pagination helpers

**When adding new middleware:**
1. Use factory function pattern
2. Export as named exports
3. Add to app.js if global

### `/api/v1/`
**Purpose**: API versioning and route organization
- Each module has its own folder
- Follow RESTful conventions
- Version all APIs

### `/api/v1/[module]/`
**Purpose**: Module-specific files
- `[module].model.js` - Mongoose schema and methods
- `[module].service.js` - Business logic
- `[module].controller.js` - Request/response handling
- `[module].route.js` - Express routes
- `[module].validation.js` - Joi validation schemas

**When adding new module:**
1. Create all 5 files
2. Follow naming convention
3. Add to app.js routes
4. Add to Swagger documentation

### `/docs/`
**Purpose**: API documentation
- `swagger.json` - OpenAPI 3.0 specification (JSON format)

**When adding new endpoints:**
1. Add to swagger.json
2. Include all request/response schemas
3. Add security requirements
4. Add examples

### `/uploads/`
**Purpose**: File upload storage
- Static file serving
- Multer configuration

### `/logs/`
**Purpose**: Application logs
- Winston log files
- Error tracking

---

## Development Instructions

### When Adding New Constants

**ALWAYS follow this pattern:**

1. **Add to constants file:**
```javascript
// constants/messages.js
const MESSAGES = {
  SUCCESS: {
    // existing messages
    NEW_SUCCESS: 'New success message'
  },
  ERROR: {
    // existing errors
    NEW_ERROR: 'New error message'
  }
};

module.exports = MESSAGES;
```

2. **Import correctly:**
```javascript
// ✅ CORRECT
const MESSAGES = require('../constants/messages');

// ❌ WRONG
const { MESSAGES } = require('../constants/messages');
```

3. **Use in error handling:**
```javascript
throw createBadRequestError(MESSAGES.ERROR.NEW_ERROR);
```

### When Adding New Error Types

**ALWAYS follow this pattern:**

1. **Add factory function to error.middleware.js:**
```javascript
const createNewError = (message = MESSAGES.ERROR.NEW_ERROR) => {
  return createAppError(message, HTTP_CODES.BAD_REQUEST);
};
```

2. **Export the factory function:**
```javascript
module.exports = {
  // existing exports
  createNewError,
};
```

3. **Import and use:**
```javascript
const { createNewError } = require('../middlewares/error.middleware');
throw createNewError('Custom message');
```

### When Adding New API Endpoints

**ALWAYS follow this pattern:**

1. **Add validation schema:**
```javascript
// api/v1/[module]/[module].validation.js
const newEndpointSchema = Joi.object({
  field: Joi.string().required()
});
```

2. **Add service method:**
```javascript
// api/v1/[module]/[module].service.js
async newEndpoint(data) {
  try {
    // business logic
    return result;
  } catch (error) {
    logger.error('Error in newEndpoint:', error);
    throw error;
  }
}
```

3. **Add controller method:**
```javascript
// api/v1/[module]/[module].controller.js
const newEndpoint = asyncHandler(async (req, res) => {
  const data = req.body;
  const result = await moduleService.newEndpoint(data);
  
  logger.info('New endpoint called');
  return successResponse(
    res, 
    HTTP_CODES.OK, 
    MESSAGES.SUCCESS.NEW_SUCCESS, 
    result, 
    RESPONSE_TAGS.SUCCESS.OPERATION_SUCCESS
  );
});
```

4. **Add route:**
```javascript
// api/v1/[module]/[module].route.js
router.post('/new-endpoint', 
  validateBody(newEndpointSchema), 
  authenticate, 
  requireAdmin, 
  newEndpoint
);
```

5. **Add to Swagger documentation:**
```json
// docs/swagger.json
{
  "paths": {
    "/api/v1/[module]/new-endpoint": {
      "post": {
        "tags": ["Module"],
        "summary": "New endpoint",
        "security": [{"bearerAuth": []}],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {"$ref": "#/components/schemas/NewEndpointRequest"}
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
              }
            }
          }
        }
      }
    }
  }
}
```

### When Adding New Database Models

**ALWAYS follow this pattern:**

1. **Create model with schema:**
```javascript
// api/v1/[module]/[module].model.js
const mongoose = require('mongoose');

const moduleSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  // other fields
}, {
  timestamps: true
});

// Add static methods
moduleSchema.statics.findByName = function(name) {
  return this.findOne({ name });
};

// Add instance methods
moduleSchema.methods.toJSON = function() {
  const obj = this.toObject();
  delete obj.__v;
  return obj;
};

module.exports = mongoose.model('Module', moduleSchema);
```

2. **Add to service:**
```javascript
const Module = require('./module.model');

// Use in service methods
const module = await Module.findById(id);
```

### When Adding New Middleware

**ALWAYS follow this pattern:**

1. **Create factory function:**
```javascript
// middlewares/new.middleware.js
const newMiddleware = (options = {}) => {
  return (req, res, next) => {
    try {
      // middleware logic
      next();
    } catch (error) {
      next(error);
    }
  };
};

module.exports = {
  newMiddleware
};
```

2. **Add to app.js if global:**
```javascript
// app.js
const { newMiddleware } = require('./middlewares/new.middleware');
app.use(newMiddleware());
```

### When Adding New Configuration

**ALWAYS follow this pattern:**

1. **Add to config/index.js:**
```javascript
// config/index.js
const config = {
  // existing config
  newFeature: {
    enabled: process.env.NEW_FEATURE_ENABLED === 'true',
    timeout: parseInt(process.env.NEW_FEATURE_TIMEOUT) || 5000
  }
};
```

2. **Add to .env.example:**
```bash
# .env.example
NEW_FEATURE_ENABLED=false
NEW_FEATURE_TIMEOUT=5000
```

3. **Use in application:**
```javascript
const config = require('./config');
if (config.newFeature.enabled) {
  // feature logic
}
```

---

## Error Handling Guidelines

### Error Factory Functions
**NEVER create error classes. Use factory functions:**

```javascript
// ✅ CORRECT
const createAppError = (message, statusCode) => {
  const error = new Error(message);
  error.statusCode = statusCode;
  error.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
  error.isOperational = true;
  Error.captureStackTrace(error, createAppError);
  return error;
};

// ❌ WRONG
class AppError extends Error {}
```

### Error Types
**Use these factory functions with tags:**

- `createAppError(message, statusCode, tag)` - Generic error
- `createBadRequestError(message, tag)` - 400 errors
- `createUnauthorizedError(message, tag)` - 401 errors
- `createForbiddenError(message, tag)` - 403 errors
- `createNotFoundError(message, tag)` - 404 errors
- `createConflictError(message, tag)` - 409 errors
- `createValidationError(message, errors, tag)` - Validation errors

**Example with tags:**
```javascript
// Import tags
const RESPONSE_TAGS = require('../constants/responseTags');

// Use with appropriate tag
throw createNotFoundError(
  MESSAGES.ERROR.USER_NOT_FOUND, 
  RESPONSE_TAGS.RESOURCE.USER_NOT_FOUND
);

throw createUnauthorizedError(
  MESSAGES.ERROR.TOKEN_EXPIRED, 
  RESPONSE_TAGS.AUTH.TOKEN_EXPIRED
);
```

### Error Handling Pattern
**Always use try-catch with proper logging:**

```javascript
async function someFunction() {
  try {
    // business logic
    return result;
  } catch (error) {
    logger.error('Error in someFunction:', error);
    throw error; // Let global error handler deal with it
  }
}
```

### Global Error Handler
**The global error handler in error.middleware.js handles:**

- Mongoose errors (CastError, ValidationError, duplicate keys)
- JWT errors (TokenExpiredError, JsonWebTokenError)
- Multer errors (file upload errors)
- Generic errors

---

## Authentication & Authorization

### JWT Token Pattern
**Stateless authentication without server-side storage:**

```javascript
// Token generation
const { accessToken, refreshToken } = generateTokens(payload);

// Token verification
const decoded = verifyAccessToken(token);
```

### RBAC Pattern
**Role-based access control with hierarchy:**

```javascript
// In route definition
router.get('/admin-only', authenticate, requireAdmin, controller.method);

// In middleware
const requireAdmin = authorize([ROLES.ADMIN]);
```

### Role Hierarchy
```javascript
// constants/roles.js
const ROLE_HIERARCHY = {
  patient: 1,
  professional: 2,
  admin: 3
};
```

### Authentication Middleware
**Always use authenticate middleware for protected routes:**

```javascript
// ✅ CORRECT
router.get('/protected', authenticate, controller.method);

// ❌ WRONG
router.get('/protected', controller.method);
```

---

## Database Patterns

### Mongoose Schema Pattern
**Always include timestamps and proper validation:**

```javascript
const schema = new mongoose.Schema({
  // fields
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});
```

### Virtual Fields
**Use virtuals for computed properties:**

```javascript
schema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});
```

### Static Methods
**Add static methods for common queries:**

```javascript
schema.statics.findByEmail = function(email) {
  return this.findOne({ email });
};
```

### Instance Methods
**Add instance methods for object-specific operations:**

```javascript
schema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};
```

### Error Handling in Database Operations
**Always handle database errors properly:**

```javascript
try {
  const user = await User.findById(id);
  if (!user) {
    throw createNotFoundError(MESSAGES.ERROR.USER_NOT_FOUND);
  }
  return user;
} catch (error) {
  logger.error('Database error:', error);
  throw error;
}
```

---

## API Design Patterns

### Response Format
**Always use standardized response format with tags:**

```javascript
// Success response
{
  "status": "success",
  "code": 200,
  "message": "Operation successful",
  "tag": "OPERATION_SUCCESS",  // Response identifier for client-side handling
  "data": { /* response data */ }
}

// Error response
{
  "status": "error",
  "code": 400,
  "message": "Error message",
  "tag": "VALIDATION_ERROR",  // Error identifier for programmatic handling
  "errors": [ /* validation errors */ ]
}
```

### Response Tags
**All responses include a `tag` field for programmatic identification:**

**Available in `constants/responseTags.js`:**
- **SUCCESS tags**: `USER_CREATED`, `LOGIN_SUCCESS`, `TOKEN_REFRESHED`, `DATA_RETRIEVED`, etc.
- **AUTH error tags**: `SESSION_EXPIRED`, `TOKEN_INVALID`, `TOKEN_EXPIRED`, `INSUFFICIENT_PERMISSIONS`, etc.
- **VALIDATION error tags**: `VALIDATION_ERROR`, `INVALID_INPUT`, `INVALID_EMAIL`, etc.
- **RESOURCE error tags**: `USER_NOT_FOUND`, `RESOURCE_NOT_FOUND`, `ALREADY_EXISTS`, etc.
- **SERVER error tags**: `INTERNAL_SERVER_ERROR`, `SERVICE_UNAVAILABLE`, etc.

**When using response helpers, always include the tag:**

```javascript
// Success with tag
return successResponse(
  res, 
  HTTP_CODES.OK, 
  MESSAGES.SUCCESS.USER_CREATED, 
  userData, 
  RESPONSE_TAGS.SUCCESS.USER_CREATED
);

// Error with tag
throw createNotFoundError(
  MESSAGES.ERROR.USER_NOT_FOUND, 
  RESPONSE_TAGS.RESOURCE.USER_NOT_FOUND
);

// Paginated response with tag
return res.paginatedResponse(
  MESSAGES.SUCCESS.USERS_FOUND, 
  users, 
  totalCount, 
  RESPONSE_TAGS.SUCCESS.USERS_FOUND
);
```

### Pagination Pattern
**Always include pagination for list endpoints:**

```javascript
// Response format
{
  "data": [ /* items */ ],
  "pagination": {
    "currentPage": 1,
    "totalPages": 5,
    "totalCount": 50,
    "limit": 10,
    "hasNextPage": true,
    "hasPrevPage": false
  }
}
```

### GET (List All) API Pattern
**MANDATORY: Always use common pagination and search utilities for all GET (list all) APIs.**

**ALWAYS follow this pattern:**

1. **Import required middleware:**
```javascript
// api/v1/[module]/[module].route.js
const { paginationMiddleware, searchMiddleware, filterMiddleware } = require('../../middlewares/pagination.middleware');
```

2. **Apply middleware in route:**
```javascript
// ✅ CORRECT - Always use pagination and search for list endpoints
router.get('/', 
  authenticate, 
  paginationMiddleware,    // MANDATORY for list APIs
  searchMiddleware,        // MANDATORY for list APIs
  filterMiddleware,        // Optional but recommended
  controller.getAllItems
);

// ❌ WRONG - Missing pagination and search middleware
router.get('/', authenticate, controller.getAllItems);
```

3. **Use in controller/service:**
```javascript
// api/v1/[module]/[module].controller.js
const getAllItems = asyncHandler(async (req, res) => {
  const { page, limit, skip, sortBy, sortOrder } = req.pagination;
  const search = req.search;
  const filters = req.filters;
  
  const result = await moduleService.getAllItems({
    pagination: { skip, limit, sortBy, sortOrder },
    search,
    filters
  });
  
  logger.info('Items retrieved with pagination and search');
  return res.paginatedResponse(MESSAGES.SUCCESS.ITEMS_RETRIEVED, result.data, result.totalCount);
});
```

4. **Implement in service:**
```javascript
// api/v1/[module]/[module].service.js
async getAllItems({ pagination, search, filters }) {
  try {
    const { skip, limit, sortBy, sortOrder } = pagination;
    
    // Build query with filters
    const query = { ...filters };
    
    // Add search functionality
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { email: { $regex: search, $options: 'i' } },
        // Add other searchable fields
      ];
    }
    
    // Execute query with pagination
    const items = await Module.find(query)
      .skip(skip)
      .limit(limit)
      .sort({ [sortBy]: sortOrder === 'desc' ? -1 : 1 });
    
    const totalCount = await Module.countDocuments(query);
    
    return {
      data: items,
      totalCount
    };
  } catch (error) {
    logger.error('Error in getAllItems:', error);
    throw error;
  }
}
```

**Query Parameters:**
- `?page=1` - Page number (default: 1)
- `?limit=10` - Items per page (default: 10, max: 100)
- `?sortBy=createdAt` - Field to sort by (default: createdAt)
- `?sortOrder=desc` - Sort order: asc or desc (default: desc)
- `?search=keyword` - Search term (searches across configured fields)
- `?field=value` - Additional filter parameters

**Critical Rules:**
- **NEVER create a GET (list) endpoint without pagination middleware**
- **NEVER create a GET (list) endpoint without search middleware**
- **ALWAYS use `res.paginatedResponse()` for list endpoints**
- **ALWAYS implement search functionality in service layer**
- **ALWAYS include totalCount for pagination metadata**

### Validation Pattern
**Always validate input with Joi:**

```javascript
const schema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(6).required()
});

router.post('/endpoint', validateBody(schema), controller.method);
```

### Logging Pattern
**Always log important operations:**

```javascript
logger.info(`User created: ${user.email}`);
logger.error('Error in operation:', error);
logger.warn('Warning message');
```

---

## Security Guidelines

### Input Validation
**Always validate and sanitize input:**

```javascript
// Use Joi validation
const schema = Joi.object({
  email: Joi.string().email().required()
});

// Use express-mongo-sanitize for MongoDB injection protection
app.use(mongoSanitize());
```

### Rate Limiting
**Apply rate limiting to sensitive endpoints:**

```javascript
// In app.js
app.use('/api/v1/user/login', limiter);
app.use('/api/v1/user/register', limiter);
```

### CORS Configuration
**Configure CORS properly:**

```javascript
app.use(cors({
  origin: config.cors.origin,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### Security Headers
**Use Helmet for security headers:**

```javascript
app.use(helmet());
app.use(hpp());
app.use(xss());
```

### Password Hashing
**Always hash passwords:**

```javascript
// In model pre-save hook
schema.pre('save', async function(next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, 12);
  }
  next();
});
```

---

## Testing Guidelines

### API Testing Pattern
**Test both success and error cases:**

```bash
# Success case
curl -X POST /api/v1/user/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"password123"}'

# Error case
curl -X POST /api/v1/user/register \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"invalid","password":"123"}'
```

### Authentication Testing
**Test with and without tokens:**

```bash
# With valid token
curl -X GET /api/v1/user/profile \
  -H "Authorization: Bearer <token>"

# Without token
curl -X GET /api/v1/user/profile
```

### Authorization Testing
**Test RBAC with different roles:**

```bash
# Admin access
curl -X GET /api/v1/user \
  -H "Authorization: Bearer <admin-token>"

# User access (should fail)
curl -X GET /api/v1/user \
  -H "Authorization: Bearer <user-token>"
```

---

## Critical Reminders for AI Agents

### When Adding New Features:

1. **NEVER use classes** - Only factory functions and pure functions
2. **ALWAYS add constants** - Messages, HTTP codes, roles
3. **ALWAYS add validation** - Joi schemas for all inputs
4. **ALWAYS add error handling** - Use factory functions, not classes
5. **ALWAYS add logging** - Info, error, and warning logs
6. **ALWAYS add documentation** - Swagger/OpenAPI specs
7. **ALWAYS test both success and error cases**
8. **ALWAYS follow naming conventions**
9. **ALWAYS use asyncHandler for route handlers**
10. **ALWAYS use proper HTTP status codes**
11. **ALWAYS use pagination and search middleware** - For ALL GET (list all) APIs

### When Modifying Existing Code:

1. **NEVER break functional programming patterns**
2. **NEVER use destructuring for imports**
3. **NEVER create classes**
4. **ALWAYS maintain backward compatibility**
5. **ALWAYS update documentation**
6. **ALWAYS test the changes**

### File Naming Conventions:

- Models: `[name].model.js`
- Services: `[name].service.js`
- Controllers: `[name].controller.js`
- Routes: `[name].route.js`
- Validation: `[name].validation.js`
- Middleware: `[name].middleware.js`

### Import/Export Conventions:

```javascript
// ✅ CORRECT
const MESSAGES = require('../constants/messages');
module.exports = { function1, function2 };

// ❌ WRONG
const { MESSAGES } = require('../constants/messages');
module.exports = classOrObject;
```

This guide ensures AI agents maintain consistency and follow the established patterns when extending the boilerplate. 