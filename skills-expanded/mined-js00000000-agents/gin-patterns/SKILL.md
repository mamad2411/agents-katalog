---
name: gin-patterns
description: Gin web framework best practices for routing, middleware, JWT authentication, request validation, and structured API responses.
---

# Gin Framework Patterns

Best practices for building RESTful APIs with the Gin web framework, as used in the Asset Diary backend.

## When to Activate

- Building APIs with the Gin framework
- Working on Asset Diary backend
- Implementing middleware or JWT authentication
- Designing REST endpoints
- Working with GORM + Gin

## Project Structure

```text
backend/
├── cmd/
│   └── server/
│       └── main.go              # Entry point, server bootstrap
├── internal/
│   ├── config/
│   │   └── config.go            # Configuration loading
│   ├── handler/
│   │   ├── asset.go             # Asset HTTP handlers
│   │   ├── auth.go              # Auth HTTP handlers
│   │   └── health.go            # Health check handler
│   ├── middleware/
│   │   ├── auth.go              # JWT auth middleware
│   │   ├── cors.go              # CORS middleware
│   │   └── logger.go            # Request logging middleware
│   ├── model/
│   │   ├── asset.go             # GORM models
│   │   └── user.go              # User model
│   ├── repository/
│   │   ├── asset_repo.go        # Asset data access
│   │   └── user_repo.go         # User data access
│   └── service/
│       ├── asset_service.go     # Asset business logic
│       └── auth_service.go      # Auth business logic
├── pkg/
│   └── response/
│       └── response.go          # Standardized API responses
├── go.mod
├── go.sum
└── Dockerfile
```

## Router Setup

```go
func SetupRouter(db *gorm.DB, cfg *config.Config) *gin.Engine {
    r := gin.New()

    // Global middleware
    r.Use(gin.Recovery())
    r.Use(middleware.Logger())
    r.Use(middleware.CORS())

    // Health check
    r.GET("/health", handler.HealthCheck)

    // Public routes
    auth := r.Group("/api/auth")
    {
        auth.POST("/register", handler.Register)
        auth.POST("/login", handler.Login)
        auth.POST("/refresh", handler.RefreshToken)
    }

    // Protected routes
    api := r.Group("/api")
    api.Use(middleware.JWTAuth(cfg.JWTSecret))
    {
        assets := api.Group("/assets")
        {
            assets.GET("", handler.ListAssets)
            assets.GET("/:id", handler.GetAsset)
            assets.POST("", handler.CreateAsset)
            assets.PUT("/:id", handler.UpdateAsset)
            assets.DELETE("/:id", handler.DeleteAsset)
        }
    }

    return r
}
```

## Handler Patterns

### Standard Handler Structure

```go
type AssetHandler struct {
    service *service.AssetService
}

func NewAssetHandler(s *service.AssetService) *AssetHandler {
    return &AssetHandler{service: s}
}

func (h *AssetHandler) List(c *gin.Context) {
    userID := c.GetString("userID") // From JWT middleware

    // Parse query parameters
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    limit, _ := strconv.Atoi(c.DefaultQuery("limit", "20"))

    assets, total, err := h.service.ListByUser(c.Request.Context(), userID, page, limit)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, "Failed to fetch assets")
        return
    }

    response.Success(c, gin.H{
        "assets": assets,
        "total":  total,
        "page":   page,
        "limit":  limit,
    })
}

func (h *AssetHandler) Create(c *gin.Context) {
    var req CreateAssetRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        response.Error(c, http.StatusBadRequest, "Invalid request body")
        return
    }

    userID := c.GetString("userID")
    asset, err := h.service.Create(c.Request.Context(), userID, &req)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, "Failed to create asset")
        return
    }

    response.Success(c, asset)
}
```

### Request Validation with Binding Tags

```go
type CreateAssetRequest struct {
    Name     string  `json:"name" binding:"required,min=1,max=100"`
    Ticker   string  `json:"ticker" binding:"required,min=1,max=10"`
    Quantity float64 `json:"quantity" binding:"required,gt=0"`
    Price    float64 `json:"price" binding:"required,gte=0"`
    Currency string  `json:"currency" binding:"required,oneof=USD TWD JPY EUR"`
}

type UpdateAssetRequest struct {
    Name     *string  `json:"name" binding:"omitempty,min=1,max=100"`
    Quantity *float64 `json:"quantity" binding:"omitempty,gt=0"`
    Price    *float64 `json:"price" binding:"omitempty,gte=0"`
}
```

### Custom Validators

```go
import "github.com/go-playground/validator/v10"

func registerCustomValidators(v *validator.Validate) {
    v.RegisterValidation("ticker", validateTicker)
}

func validateTicker(fl validator.FieldLevel) bool {
    ticker := fl.Field().String()
    // Only uppercase letters and numbers
    matched, _ := regexp.MatchString(`^[A-Z0-9]+$`, ticker)
    return matched
}
```

## Middleware Patterns

### JWT Authentication Middleware

```go
func JWTAuth(secret string) gin.HandlerFunc {
    return func(c *gin.Context) {
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "Authorization header required",
            })
            return
        }

        tokenString := strings.TrimPrefix(authHeader, "Bearer ")
        if tokenString == authHeader {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "Bearer token required",
            })
            return
        }

        claims, err := jwt.ParseToken(tokenString, secret)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "Invalid or expired token",
            })
            return
        }

        c.Set("userID", claims.UserID)
        c.Set("email", claims.Email)
        c.Next()
    }
}
```

### Request Logging Middleware

```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()

        latency := time.Since(start)
        statusCode := c.Writer.Status()

        log.Printf("[%d] %s %s %v",
            statusCode,
            c.Request.Method,
            path,
            latency,
        )
    }
}
```

### CORS Middleware

```go
func CORS() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
        c.Writer.Header().Set("Access-Control-Max-Age", "86400")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(http.StatusNoContent)
            return
        }

        c.Next()
    }
}
```

### Rate Limiting Middleware

```go
func RateLimit(maxRequests int, window time.Duration) gin.HandlerFunc {
    type client struct {
        count    int
        lastSeen time.Time
    }

    var (
        mu      sync.Mutex
        clients = make(map[string]*client)
    )

    return func(c *gin.Context) {
        ip := c.ClientIP()

        mu.Lock()
        cl, exists := clients[ip]
        if !exists || time.Since(cl.lastSeen) > window {
            clients[ip] = &client{count: 1, lastSeen: time.Now()}
            mu.Unlock()
            c.Next()
            return
        }

        if cl.count >= maxRequests {
            mu.Unlock()
            c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{
                "error": "Rate limit exceeded",
            })
            return
        }

        cl.count++
        mu.Unlock()
        c.Next()
    }
}
```

## Standardized API Responses

```go
package response

import "github.com/gin-gonic/gin"

type APIResponse struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
    Meta    *Meta       `json:"meta,omitempty"`
}

type Meta struct {
    Total int `json:"total"`
    Page  int `json:"page"`
    Limit int `json:"limit"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, APIResponse{
        Success: true,
        Data:    data,
    })
}

func Created(c *gin.Context, data interface{}) {
    c.JSON(http.StatusCreated, APIResponse{
        Success: true,
        Data:    data,
    })
}

func Error(c *gin.Context, statusCode int, message string) {
    c.JSON(statusCode, APIResponse{
        Success: false,
        Error:   message,
    })
}

func Paginated(c *gin.Context, data interface{}, total, page, limit int) {
    c.JSON(http.StatusOK, APIResponse{
        Success: true,
        Data:    data,
        Meta:    &Meta{Total: total, Page: page, Limit: limit},
    })
}
```

## Error Handling

### Centralized Error Handler

```go
type AppError struct {
    Code    int    `json:"-"`
    Message string `json:"message"`
    Err     error  `json:"-"`
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return e.Err.Error()
    }
    return e.Message
}

func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last()

            var appErr *AppError
            if errors.As(err.Err, &appErr) {
                c.JSON(appErr.Code, gin.H{"error": appErr.Message})
                return
            }

            c.JSON(http.StatusInternalServerError, gin.H{
                "error": "Internal server error",
            })
        }
    }
}
```

## GORM Integration

### Model Definition

```go
type Asset struct {
    ID        uint           `gorm:"primaryKey" json:"id"`
    UserID    uint           `gorm:"index;not null" json:"user_id"`
    Name      string         `gorm:"size:100;not null" json:"name"`
    Ticker    string         `gorm:"size:10;not null" json:"ticker"`
    Quantity  float64        `gorm:"not null" json:"quantity"`
    Price     float64        `gorm:"not null" json:"price"`
    Currency  string         `gorm:"size:3;not null;default:USD" json:"currency"`
    CreatedAt time.Time      `json:"created_at"`
    UpdatedAt time.Time      `json:"updated_at"`
    DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}
```

### Repository Pattern with GORM

```go
type AssetRepository struct {
    db *gorm.DB
}

func NewAssetRepository(db *gorm.DB) *AssetRepository {
    return &AssetRepository{db: db}
}

func (r *AssetRepository) FindByUser(ctx context.Context, userID uint, page, limit int) ([]Asset, int64, error) {
    var assets []Asset
    var total int64

    query := r.db.WithContext(ctx).Where("user_id = ?", userID)

    if err := query.Model(&Asset{}).Count(&total).Error; err != nil {
        return nil, 0, fmt.Errorf("count assets: %w", err)
    }

    offset := (page - 1) * limit
    if err := query.Offset(offset).Limit(limit).
        Order("created_at DESC").Find(&assets).Error; err != nil {
        return nil, 0, fmt.Errorf("find assets: %w", err)
    }

    return assets, total, nil
}
```

---

**Remember**: Gin's strength is its simplicity. Keep handlers thin, push business logic to services, and use middleware for cross-cutting concerns.
