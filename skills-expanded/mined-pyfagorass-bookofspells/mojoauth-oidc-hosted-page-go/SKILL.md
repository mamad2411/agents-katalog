---
name: mojoauth-oidc-hosted-page-go
description: Implement passwordless authentication in Go applications using MojoAuth OIDC Hosted Login Page.
---

# Implement MojoAuth OIDC (Go)

This expert AI assistant guide walks you through integrating passwordless authentication into a Go application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Go application (1.21+).
- Basic knowledge of Go's `net/http` or a web framework like `chi` or `gorilla/mux`.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required packages: `github.com/coreos/go-oidc/v3/oidc`, `golang.org/x/oauth2`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:8080/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

### Step 2: Modify the Existing Go Project

#### Substep 2.1: Install Dependencies

```bash
go get github.com/coreos/go-oidc/v3/oidc
go get golang.org/x/oauth2
```

#### Substep 2.2: Configure Environment Variables

Set the following environment variables (or use a `.env` loader like `godotenv`):

```env
MOJOAUTH_DOMAIN=your-app.mojoauth.com
MOJOAUTH_CLIENT_ID=your_client_id
MOJOAUTH_CLIENT_SECRET=your_client_secret
MOJOAUTH_REDIRECT_URI=http://localhost:8080/auth/callback
```

#### Substep 2.3: Configure OIDC Provider

Create a dedicated file for OIDC configuration (e.g., `internal/auth/oidc.go`):

```go
// internal/auth/oidc.go
package auth

import (
	"context"
	"fmt"
	"os"

	"github.com/coreos/go-oidc/v3/oidc"
	"golang.org/x/oauth2"
)

var (
	OIDCProvider *oidc.Provider
	OAuth2Config oauth2.Config
)

func InitOIDC() error {
	ctx := context.Background()

	issuerURL := fmt.Sprintf("https://%s", os.Getenv("MOJOAUTH_DOMAIN"))
	provider, err := oidc.NewProvider(ctx, issuerURL)
	if err != nil {
		return err
	}
	OIDCProvider = provider

	OAuth2Config = oauth2.Config{
		ClientID:     os.Getenv("MOJOAUTH_CLIENT_ID"),
		ClientSecret: os.Getenv("MOJOAUTH_CLIENT_SECRET"),
		RedirectURL:  os.Getenv("MOJOAUTH_REDIRECT_URI"),
		Endpoint:     provider.Endpoint(),
		Scopes:       []string{oidc.ScopeOpenID, "profile", "email"},
	}

	return nil
}
```

#### Substep 2.4: Update Login Page/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" link**:

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    {{if .Error}}
      <p style="color: red;">{{.Error}}</p>
    {{end}}

    <a href="/auth/login" class="sign-in-button">Sign In with MojoAuth</a>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
  </div>
</body>
</html>
```

#### Substep 2.5: Update Backend Logic

Create the necessary handlers to process the OIDC flow.

**1. Login Handler** (`internal/auth/handlers.go`):

```go
// internal/auth/handlers.go
package auth

import (
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"log"
	"net/http"

	"github.com/coreos/go-oidc/v3/oidc"
)

func generateState() string {
	b := make([]byte, 16)
	rand.Read(b)
	return base64.URLEncoding.EncodeToString(b)
}

// LoginHandler initiates the MojoAuth OIDC flow.
func LoginHandler(w http.ResponseWriter, r *http.Request) {
	// Generate a random state for CSRF protection
	state := generateState()

	// Store state in a cookie
	http.SetCookie(w, &http.Cookie{
		Name:     "oidc_state",
		Value:    state,
		Path:     "/",
		HttpOnly: true,
		Secure:   true,
		SameSite: http.SameSiteLaxMode,
		MaxAge:   3600,
	})

	// Build authorization URL — redirects to MojoAuth Hosted Login Page
	authURL := OAuth2Config.AuthCodeURL(state)

	http.Redirect(w, r, authURL, http.StatusFound)
}
```

**2. Callback Handler** (add to `internal/auth/handlers.go`):

```go
// CallbackHandler handles the OIDC callback.
func CallbackHandler(w http.ResponseWriter, r *http.Request) {
	// Retrieve stored state from cookie
	stateCookie, err := r.Cookie("oidc_state")
	if err != nil {
		log.Println("State cookie not found:", err)
		http.Redirect(w, r, "/login?error=state_missing", http.StatusFound)
		return
	}

	// Verify state
	if r.URL.Query().Get("state") != stateCookie.Value {
		log.Println("State mismatch")
		http.Redirect(w, r, "/login?error=state_mismatch", http.StatusFound)
		return
	}

	// Exchange authorization code for token
	code := r.URL.Query().Get("code")
	token, err := OAuth2Config.Exchange(r.Context(), code)
	if err != nil {
		log.Println("Token exchange failed:", err)
		http.Redirect(w, r, "/login?error=token_exchange_failed", http.StatusFound)
		return
	}

	// Extract and verify ID token
	rawIDToken, ok := token.Extra("id_token").(string)
	if !ok {
		log.Println("No id_token in response")
		http.Redirect(w, r, "/login?error=no_id_token", http.StatusFound)
		return
	}

	verifier := OIDCProvider.Verifier(&oidc.Config{ClientID: OAuth2Config.ClientID})
	idToken, err := verifier.Verify(r.Context(), rawIDToken)
	if err != nil {
		log.Println("ID token verification failed:", err)
		http.Redirect(w, r, "/login?error=token_verification_failed", http.StatusFound)
		return
	}

	// Extract user claims
	var claims map[string]interface{}
	if err := idToken.Claims(&claims); err != nil {
		log.Println("Failed to parse claims:", err)
		http.Redirect(w, r, "/login?error=claims_parse_failed", http.StatusFound)
		return
	}

	// Clear the state cookie
	http.SetCookie(w, &http.Cookie{
		Name:   "oidc_state",
		Value:  "",
		Path:   "/",
		MaxAge: -1,
	})

	// TODO: Create a session for the user based on claims
	claimsJSON, _ := json.Marshal(claims)
	http.SetCookie(w, &http.Cookie{
		Name:     "user_session",
		Value:    base64.URLEncoding.EncodeToString(claimsJSON),
		Path:     "/",
		HttpOnly: true,
		MaxAge:   3600,
	})

	log.Println("Authenticated User:", claims)

	// Redirect to the dashboard or intended page
	http.Redirect(w, r, "/dashboard", http.StatusFound)
}
```

**3. Main Application Setup** (`main.go`):

```go
// main.go
package main

import (
	"log"
	"net/http"
	"html/template"

	"yourmodule/internal/auth"
)

func main() {
	// Initialize OIDC
	if err := auth.InitOIDC(); err != nil {
		log.Fatal("Failed to initialize OIDC:", err)
	}

	// Routes
	http.HandleFunc("/login", func(w http.ResponseWriter, r *http.Request) {
		tmpl := template.Must(template.ParseFiles("templates/login.html"))
		data := map[string]string{"Error": r.URL.Query().Get("error")}
		tmpl.Execute(w, data)
	})

	http.HandleFunc("/auth/login", auth.LoginHandler)
	http.HandleFunc("/auth/callback", auth.CallbackHandler)
	http.HandleFunc("/dashboard", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("<h1>Dashboard</h1><p>Welcome!</p>"))
	})

	log.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### Step 3: Test the Implementation

1. Start your application: `go run main.go`.
2. Navigate to `http://localhost:8080/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback handler with granular OIDC error parsing.
- **Styling**: Adapt the example HTML/CSS to match your application's design system.
- **Security**: Use a proper session library (e.g., `gorilla/sessions`) instead of raw cookies in production.
- **Environment Variables**: Use a library like `godotenv` for local development and proper secrets management in production.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [go-oidc documentation](https://github.com/coreos/go-oidc) and [oauth2 documentation](https://pkg.go.dev/golang.org/x/oauth2) for advanced configuration.
