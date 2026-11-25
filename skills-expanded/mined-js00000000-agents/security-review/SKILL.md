---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing sensitive features. Provides comprehensive security checklists and patterns.
---

# Security Review Skill

This skill ensures all code follows security best practices and identifies potential vulnerabilities.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Security Checklist

### 1. Secret Management

#### ❌ Never Do This
```go
const apiKey = "sk-proj-xxxxx"  // Hardcoded secret
const dbPassword = "password123" // In source code
```

#### ✅ Always Do This
```go
apiKey := os.Getenv("OPENAI_API_KEY")
dbURL := os.Getenv("DATABASE_URL")

if apiKey == "" {
    log.Fatal("OPENAI_API_KEY not configured")
}
```

#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env.local` in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets in hosting platform

### 2. Input Validation

#### Go (Gin) Validation
```go
type CreateAssetRequest struct {
    Name     string  `json:"name" binding:"required,min=1,max=100"`
    Ticker   string  `json:"ticker" binding:"required,min=1,max=10"`
    Quantity float64 `json:"quantity" binding:"required,gt=0"`
    Currency string  `json:"currency" binding:"required,oneof=USD TWD JPY EUR"`
}

func (h *Handler) CreateAsset(c *gin.Context) {
    var req CreateAssetRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
        return
    }
    // Process validated input
}
```

#### TypeScript Validation (Zod)
```typescript
import { z } from 'zod'

const CreateAssetSchema = z.object({
  name: z.string().min(1).max(100),
  ticker: z.string().min(1).max(10),
  quantity: z.number().positive(),
  currency: z.enum(['USD', 'TWD', 'JPY', 'EUR'])
})

export async function createAsset(input: unknown) {
  const validated = CreateAssetSchema.parse(input)
  return await db.assets.create(validated)
}
```

#### Verification Steps
- [ ] All user input validated with schemas
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries
- [ ] Whitelist validation (not blacklist)
- [ ] Error messages don't leak sensitive info

### 3. SQL Injection Prevention

```go
// ❌ DANGEROUS: SQL injection vulnerability
query := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", userEmail)
db.Raw(query)

// ✅ SAFE: Parameterized queries with GORM
db.Where("email = ?", userEmail).First(&user)

// ✅ SAFE: GORM methods
db.First(&user, "email = ?", userEmail)
```

### 4. Authentication & Authorization

#### JWT Token Handling
```go
// Generate token
func GenerateToken(userID uint, secret string) (string, error) {
    claims := jwt.MapClaims{
        "user_id": userID,
        "exp":     time.Now().Add(24 * time.Hour).Unix(),
        "iat":     time.Now().Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(secret))
}

// Verify token
func VerifyToken(tokenString, secret string) (*Claims, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return []byte(secret), nil
    })
    if err != nil {
        return nil, err
    }
    // Extract and return claims
}
```

#### Authorization Checks
```go
func (h *Handler) DeleteAsset(c *gin.Context) {
    userID := c.GetUint("userID") // From JWT middleware
    assetID := c.Param("id")

    asset, err := h.service.GetAsset(c, assetID)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Asset not found"})
        return
    }

    // Always check ownership
    if asset.UserID != userID {
        c.JSON(http.StatusForbidden, gin.H{"error": "Not authorized"})
        return
    }

    // Proceed with deletion
}
```

### 5. Sensitive Data Exposure

#### Logging
```go
// ❌ BAD: Logging sensitive data
log.Printf("User login: email=%s password=%s", email, password)

// ✅ GOOD: Redact sensitive data
log.Printf("User login: email=%s userID=%d", email, userID)
```

#### Error Messages
```go
// ❌ BAD: Exposing internals
c.JSON(500, gin.H{"error": err.Error(), "stack": string(debug.Stack())})

// ✅ GOOD: Generic error messages
log.Printf("Internal error: %v", err)  // Log detail server-side
c.JSON(500, gin.H{"error": "An error occurred. Please try again."})
```

### 6. Rate Limiting

```go
// Apply to sensitive endpoints
api.POST("/auth/login", middleware.RateLimit(10, time.Minute), handler.Login)
api.POST("/auth/register", middleware.RateLimit(5, time.Minute), handler.Register)

// More generous for read endpoints
api.GET("/assets", middleware.RateLimit(100, time.Minute), handler.ListAssets)
```

### 7. CORS Configuration

```go
// ❌ BAD: Allow everything
c.Writer.Header().Set("Access-Control-Allow-Origin", "*")

// ✅ GOOD: Restrict to known origins
allowedOrigins := []string{
    "http://localhost:5173",  // Vite dev server
    "https://yourdomain.com",
}
```

### 8. Dependency Security

```bash
# Go
go list -m all | nancy sleuth    # Check for vulnerabilities
go mod verify                     # Verify checksums

# Node.js
npm audit                         # Check for vulnerabilities
npm audit fix                     # Fix automatically
npm outdated                      # Check for updates
```

## Pre-Deployment Security Checklist

- [ ] **Secrets**: No hardcoded secrets, all in environment variables
- [ ] **Input validation**: All user input validated
- [ ] **SQL injection**: All queries parameterized
- [ ] **Authentication**: Proper token handling
- [ ] **Authorization**: Ownership/role checks in place
- [ ] **Rate limiting**: All endpoints rate limited
- [ ] **HTTPS**: Enforced in production
- [ ] **Security headers**: CSP, X-Frame-Options configured
- [ ] **Error handling**: No sensitive data in errors
- [ ] **Logging**: No sensitive data in logs
- [ ] **Dependencies**: Up to date, no vulnerabilities
- [ ] **CORS**: Properly restricted

---

**Remember**: Security is not optional. A single vulnerability can compromise the entire platform. When in doubt, err on the side of caution.
