---
name: gin-patterns
description: "When to activate: Gin web framework, routing groups, middleware, request binding, validation, error handling, Gin context"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Gin Framework Patterns

## Router Setup

```go
package main

import (
    "github.com/gin-gonic/gin"
    "github.com/gin-gonic/gin/binding"
    "github.com/go-playground/validator/v10"
)

func main() {
    r := gin.New()
    r.Use(gin.Logger(), gin.Recovery())

    // Health check (no auth)
    r.GET("/health", healthHandler)

    // API v1 group
    v1 := r.Group("/api/v1")
    v1.Use(authMiddleware())
    {
        users := v1.Group("/users")
        users.GET("",     listUsers)
        users.POST("",    createUser)
        users.GET("/:id", getUser)
        users.PUT("/:id", updateUser)
        users.DELETE("/:id", deleteUser)
    }

    r.Run(":8080")
}
```

## Request Binding and Validation

```go
type CreateUserRequest struct {
    Email    string `json:"email"    binding:"required,email"`
    Name     string `json:"name"     binding:"required,min=2,max=100"`
    Password string `json:"password" binding:"required,min=8"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    user, err := userService.Create(c.Request.Context(), req)
    if err != nil {
        handleError(c, err)
        return
    }
    c.JSON(http.StatusCreated, user)
}

// Query param binding
type ListUsersQuery struct {
    Page     int    `form:"page"     binding:"min=1" default:"1"`
    PageSize int    `form:"pageSize" binding:"min=1,max=100" default:"20"`
    Search   string `form:"search"`
}

func listUsers(c *gin.Context) {
    var q ListUsersQuery
    if err := c.ShouldBindQuery(&q); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // ...
}
```

## Middleware

```go
func authMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing token"})
            return
        }
        claims, err := validateJWT(strings.TrimPrefix(token, "Bearer "))
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            return
        }
        c.Set("userID", claims.UserID)
        c.Next()
    }
}

func requestIDMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        id := c.GetHeader("X-Request-ID")
        if id == "" { id = uuid.New().String() }
        c.Set("requestID", id)
        c.Header("X-Request-ID", id)
        c.Next()
    }
}

// Extract context values set by middleware
func getUser(c *gin.Context) {
    userID, _ := c.Get("userID")
    // ...
}
```

## Centralized Error Handling

```go
type AppError struct {
    Code    int    `json:"-"`
    Message string `json:"error"`
}

func handleError(c *gin.Context, err error) {
    var appErr *AppError
    switch {
    case errors.As(err, &appErr):
        c.JSON(appErr.Code, appErr)
    case errors.Is(err, ErrNotFound):
        c.JSON(http.StatusNotFound, gin.H{"error": "resource not found"})
    case errors.Is(err, ErrForbidden):
        c.JSON(http.StatusForbidden, gin.H{"error": "forbidden"})
    default:
        log.Printf("unhandled error: %v", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
    }
}
```

## File Upload

```go
func uploadFile(c *gin.Context) {
    file, header, err := c.Request.FormFile("file")
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "file required"})
        return
    }
    defer file.Close()

    if header.Size > 10<<20 {  // 10 MB
        c.JSON(http.StatusRequestEntityTooLarge, gin.H{"error": "file too large"})
        return
    }

    dst := filepath.Join("uploads", filepath.Base(header.Filename))
    if err := c.SaveUploadedFile(header, dst); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusOK, gin.H{"path": dst})
}
```

## Testing Gin Handlers

```go
func TestCreateUser(t *testing.T) {
    gin.SetMode(gin.TestMode)
    r := gin.New()
    r.POST("/users", createUser)

    body := `{"email":"alice@example.com","name":"Alice","password":"secret123"}`
    req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    w := httptest.NewRecorder()

    r.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)
    var resp map[string]any
    json.NewDecoder(w.Body).Decode(&resp)
    assert.Equal(t, "alice@example.com", resp["email"])
}
```

## Common Anti-Patterns

- **`c.AbortWithStatus` without JSON** — clients receive empty body; always add a message
- **Route handlers with business logic** — keep handlers thin; delegate to service layer
- **Not using `c.Request.Context()`** — pass request context to DB/HTTP calls for cancellation
- **Global gin instance** — use `gin.New()` not `gin.Default()` in prod; control your own middleware
- **Panic in middleware** — use `c.Abort()` not `panic()`; `gin.Recovery()` catches panics but adds overhead
