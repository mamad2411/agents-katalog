---
name: echo-patterns
description: "When to activate: Echo web framework, routing, middleware, request binding, WebSocket, graceful shutdown in Echo"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Echo Framework Patterns

## Server Setup

```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()
    e.HideBanner = true

    // Middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())
    e.Use(middleware.CORS())

    // Custom error handler
    e.HTTPErrorHandler = customErrorHandler

    // Routes
    e.GET("/health", healthCheck)

    api := e.Group("/api/v1")
    api.Use(jwtMiddleware())

    api.GET("/users",     listUsers)
    api.POST("/users",    createUser)
    api.GET("/users/:id", getUser)
    api.PUT("/users/:id", updateUser)

    // Graceful shutdown
    go func() {
        if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
            e.Logger.Fatal(err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    e.Shutdown(ctx)
}
```

## Request Binding and Validation

```go
type CreateUserRequest struct {
    Email    string `json:"email"    validate:"required,email"`
    Name     string `json:"name"     validate:"required,min=2,max=100"`
    Password string `json:"password" validate:"required,min=8"`
}

func createUser(c echo.Context) error {
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }
    if err := c.Validate(&req); err != nil {
        return echo.NewHTTPError(http.StatusUnprocessableEntity, err.Error())
    }
    user, err := userService.Create(c.Request().Context(), req)
    if err != nil { return err }
    return c.JSON(http.StatusCreated, user)
}

// Custom validator using go-playground/validator
type Validator struct{ v *validator.Validate }

func (cv *Validator) Validate(i any) error {
    if err := cv.v.Struct(i); err != nil {
        return echo.NewHTTPError(http.StatusUnprocessableEntity, err.Error())
    }
    return nil
}

e.Validator = &Validator{v: validator.New()}
```

## Middleware

```go
func jwtMiddleware() echo.MiddlewareFunc {
    return middleware.JWTWithConfig(middleware.JWTConfig{
        SigningKey:   []byte(os.Getenv("JWT_SECRET")),
        TokenLookup: "header:Authorization:Bearer ",
        ContextKey:  "user",
    })
}

// Custom middleware
func loggingMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        start := time.Now()
        err := next(c)
        log.Printf("%s %s %d %s",
            c.Request().Method,
            c.Request().URL.Path,
            c.Response().Status,
            time.Since(start),
        )
        return err
    }
}
```

## Custom Error Handler

```go
func customErrorHandler(err error, c echo.Context) {
    var he *echo.HTTPError
    if errors.As(err, &he) {
        c.JSON(he.Code, map[string]any{"error": he.Message})
        return
    }
    if errors.Is(err, ErrNotFound) {
        c.JSON(http.StatusNotFound, map[string]any{"error": "not found"})
        return
    }
    c.Logger().Errorf("unhandled: %v", err)
    c.JSON(http.StatusInternalServerError, map[string]any{"error": "internal server error"})
}
```

## WebSocket

```go
var upgrader = websocket.Upgrader{}

func wsHandler(c echo.Context) error {
    ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
    if err != nil { return err }
    defer ws.Close()

    for {
        mt, msg, err := ws.ReadMessage()
        if err != nil {
            if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway) {
                c.Logger().Error(err)
            }
            break
        }
        if err := ws.WriteMessage(mt, msg); err != nil { break }
    }
    return nil
}
```

## Testing Echo Handlers

```go
func TestGetUser(t *testing.T) {
    e := echo.New()
    req := httptest.NewRequest(http.MethodGet, "/", nil)
    rec := httptest.NewRecorder()
    c := e.NewContext(req, rec)
    c.SetPath("/users/:id")
    c.SetParamNames("id")
    c.SetParamValues("123")

    err := getUser(c)

    require.NoError(t, err)
    assert.Equal(t, http.StatusOK, rec.Code)
}
```

## Common Anti-Patterns

- **Returning `error` without wrapping** — use `echo.NewHTTPError` to control status codes
- **Not calling `e.Shutdown(ctx)`** — in-flight requests get cut off; always graceful shutdown
- **Route-specific middleware applied globally** — use group middleware for scoped routes
- **Ignoring `c.Request().Context()`** — pass it to downstream calls for cancellation support
- **Custom validator not registered** — Echo doesn't validate by default; register `e.Validator`
