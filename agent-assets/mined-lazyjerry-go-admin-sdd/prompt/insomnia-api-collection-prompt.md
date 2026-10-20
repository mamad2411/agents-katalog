# Generate Insomnia 5.0 API Collection

Generate a comprehensive Insomnia 5.0 format API collection for testing RESTful APIs.

This prompt creates standardized API testing collections that are fully compatible with Insomnia REST Client.

---

## Context Analysis

1. **Identify the API service** and its core functionality
2. **Analyze existing API endpoints** from routes, controllers, or documentation
3. **Determine authentication requirements** (if any)
4. **Review data models** to understand request/response structures
5. **Check existing API documentation** or OpenAPI specs

---

## Collection Generation Steps

### Step 1: Initialize Collection Structure

Create the base YAML structure with:

- Collection metadata (name, description, timestamps)
- Environment variables for different deployment targets
- Proper Insomnia 5.0 format compliance

### Step 2: Generate Core CRUD Requests

For each primary resource, create:

1. **List/Index** - GET all resources with pagination support
2. **Create** - POST new resource with validation
3. **Show** - GET single resource by ID
4. **Update (PUT)** - Complete resource replacement
5. **Update (PATCH)** - Partial resource update
6. **Delete** - Remove resource by ID

### Step 3: Add System Health Checks

Include:

- API health/status endpoint
- Version information endpoint
- Database connectivity check (if available)

### Step 4: Create Error Handling Tests

Add requests that trigger:

- **422 Validation Errors** - Invalid input data
- **404 Not Found** - Non-existent resource access
- **401 Unauthorized** - Authentication failures (if applicable)
- **500 Server Errors** - Server-side error conditions

### Step 5: Configure Environment Variables

Set up multiple environments:

- **Local Development** (localhost with appropriate port)
- **Staging** (staging server URL)
- **Production** (production server URL)

### Step 6: Add Request Documentation

For each request, include:

- Clear description of functionality
- Expected response format
- Required parameters explanation
- Usage examples and notes

---

## Request Configuration Standards

### Headers Setup

Every request should include:

```yaml
headers:
  - name: Accept
    value: application/json
  - name: Content-Type
    value: application/json
```

### URL Parameterization

Use environment variables:

```yaml
url: "{{ _.base_url }}/api/endpoint"
```

### Request Body Examples

Provide realistic test data:

- Use meaningful example values
- Cover different data types
- Avoid sensitive information
- Include edge cases where appropriate

### Settings Configuration

Use consistent settings:

```yaml
settings:
  renderRequestBody: true
  encodeUrl: true
  followRedirects: global
  cookies:
    send: true
    store: true
  rebuildPath: true
```

---

## Naming Conventions

### Collection Naming

Format: `{Service Name} API`
Example: `Laravel TODO List API`

### Request Naming (Chinese)

Use clear, descriptive Chinese names:

- "獲取所有{資源}"
- "建立新{資源}"
- "更新{資源}"
- "刪除{資源}"
- "驗證錯誤測試"

### ID Conventions

- Collection: `wrk_{service}_{type}_collection`
- Requests: `req_{action}_{resource}`
- Environments: `env_{environment_name}`

---

## Test Coverage Requirements

### Functional Testing

- [ ] Complete CRUD operations
- [ ] Data validation scenarios
- [ ] Relationship management (if applicable)
- [ ] Filtering and pagination
- [ ] Sorting capabilities

### Error Handling

- [ ] Input validation failures
- [ ] Resource not found scenarios
- [ ] Server error conditions
- [ ] Authentication/authorization failures

### Performance Testing

- [ ] Large dataset handling
- [ ] Concurrent request scenarios
- [ ] Timeout configurations

---

## Documentation Requirements

### Collection Description

Include:

- API purpose and functionality overview
- Version information
- Base URL configurations
- Authentication requirements
- Rate limiting information (if applicable)

### Request Documentation

For each request:

- Functional description
- Parameter explanations
- Expected response format
- Error response examples
- Usage notes and tips

### Usage Instructions

Provide:

- Import instructions for Insomnia
- Environment setup steps
- Test execution sequence
- Troubleshooting common issues

---

## Quality Assurance Checklist

### Format Compliance

- [ ] Valid Insomnia 5.0 YAML structure
- [ ] Proper metadata with timestamps
- [ ] Correct request object formatting
- [ ] Environment variables properly defined

### Content Quality

- [ ] All CRUD operations covered
- [ ] Comprehensive error testing
- [ ] Realistic test data
- [ ] Clear Chinese descriptions
- [ ] Proper parameterization

### Usability

- [ ] Easy import process
- [ ] Intuitive request organization
- [ ] Clear environment setup
- [ ] Comprehensive documentation
- [ ] Logical test flow sequence

---

## Output Requirements

Generate the following files:

1. **Main Collection File**

   - Path: `docs/insomnia/{service}-api-collection.yaml`
   - Complete Insomnia 5.0 format collection
   - All CRUD operations and error tests
   - Multiple environment configurations

2. **Documentation File**

   - Path: `docs/insomnia/README.md`
   - Import and usage instructions
   - Environment setup guide
   - Testing workflow recommendations

3. **Update Project Documentation**
   - Add Insomnia collection information to main README
   - Include API testing tools section
   - Reference collection usage in project structure

---

## Example Commands

If this is being executed as part of a larger workflow:

```bash
# Generate collection for Laravel TODO API
generate_insomnia_collection --service="todo" --base_url="http://localhost:80" --format="5.0"

# Validate generated collection
validate_insomnia_yaml docs/insomnia/todo-api-collection.yaml

# Test import compatibility
test_insomnia_import docs/insomnia/todo-api-collection.yaml
```

---

## Success Criteria

The generated collection should:

1. **Import successfully** into Insomnia without errors
2. **Execute all requests** against a running API instance
3. **Provide comprehensive testing** of all API functionality
4. **Include proper error handling** for common failure scenarios
5. **Be easily configurable** for different environments
6. **Have clear documentation** for immediate usability

---

_This prompt ensures generation of production-ready Insomnia API collections that follow best practices and provide comprehensive API testing capabilities._
