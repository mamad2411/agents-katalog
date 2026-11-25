---
name: oidc-hosted-page-go
description: Implement "Sign in with SSO" in Go applications using SSOJet OIDC Authorization Code flow.
---

# Implement SSOJet OIDC (Go)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Go application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Go application (1.21+) with a login page.
- Basic knowledge of Go's `net/http` or a web framework like `chi` or `gorilla/mux`.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required packages: `github.com/coreos/go-oidc/v3/oidc`, `golang.org/x/oauth2`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyGoApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:8080/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing Go Project

#### Substep 2.1: Install Dependencies

Run the following commands to install the required packages:

```bash
go get github.com/coreos/go-oidc/v3/oidc
go get golang.org/x/oauth2
```

#### Substep 2.2: Configure Environment Variables

Set the following environment variables (or use a `.env` loader like `godotenv`):

```env
SSOJET_ISSUER_URL=https://auth.ssojet.com
SSOJET_CLIENT_ID=your_client_id
SSOJET_CLIENT_SECRET=your_client_secret
SSOJET_REDIRECT_URI=http://localhost:8080/auth/callback
```

#### Substep 2.3: Configure OIDC Provider

Create a dedicated file for OIDC configuration (e.g., `internal/auth/oidc.go`):

```go
// internal/auth/oidc.go
package auth

import (
	"context"
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

	provider, err := oidc.NewProvider(ctx, os.Getenv("SSOJET_ISSUER_URL"))
	if err != nil {
		return err
	}
	OIDCProvider = provider

	OAuth2Config = oauth2.Config{
		ClientID:     os.Getenv("SSOJET_CLIENT_ID"),
		ClientSecret: os.Getenv("SSOJET_CLIENT_SECRET"),
		RedirectURL:  os.Getenv("SSOJET_REDIRECT_URI"),
		Endpoint:     provider.Endpoint(),
		Scopes:       []string{oidc.ScopeOpenID, "profile", "email"},
	}

	return nil
}
```

#### Substep 2.4: Update Login Page/UI

Create or modify your login page template (e.g., `templates/login.html`):

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html>
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Sign In</h1>

    {{if .Error}}
      <p style="color: red;">{{.Error}}</p>
    {{end}}

    <form id="loginForm" method="POST" action="/auth/login">
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
      </div>

      <div id="passwordField">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      </div>

      <input type="hidden" id="isSSO" name="is_sso" value="false" />

      <button type="submit" id="submitBtn">Sign In</button>
    </form>

    <button type="button" id="ssoToggle" onclick="toggleSSO()">
      Sign in with SSO
    </button>
  </div>

  <script>
    function toggleSSO() {
      const isSSO = document.getElementById('isSSO');
      const passwordField = document.getElementById('passwordField');
      const submitBtn = document.getElementById('submitBtn');
      const ssoToggle = document.getElementById('ssoToggle');

      if (isSSO.value === 'false') {
        isSSO.value = 'true';
        passwordField.style.display = 'none';
        document.getElementById('password').removeAttribute('required');
        submitBtn.textContent = 'Continue with SSO';
        ssoToggle.textContent = 'Back to Password Login';
      } else {
        isSSO.value = 'false';
        passwordField.style.display = 'block';
        document.getElementById('password').setAttribute('required', 'true');
        submitBtn.textContent = 'Sign In';
        ssoToggle.textContent = 'Sign in with SSO';
      }
    }
  </script>
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
	"golang.org/x/oauth2"
)

func generateState() string {
	b := make([]byte, 16)
	rand.Read(b)
	return base64.URLEncoding.EncodeToString(b)
}

// LoginHandler handles the login form submission.
func LoginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	r.ParseForm()
	email := r.FormValue("email")
	isSSO := r.FormValue("is_sso")

	if isSSO == "true" {
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

		// Build authorization URL with login_hint
		authURL := OAuth2Config.AuthCodeURL(state,
			oauth2.SetAuthURLParam("login_hint", email),
		)

		http.Redirect(w, r, authURL, http.StatusFound)
		return
	}

	// Existing password login logic here
	log.Println("Processing traditional login...")
	http.Redirect(w, r, "/dashboard", http.StatusFound)
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

### Step 3: Test the Modified Connection

1. Start your application: `go run main.go`.
2. Navigate to your login page (e.g., `http://localhost:8080/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Enhance the callback handler with granular OIDC error parsing.
- **Styling**: Adapt the example HTML/CSS to match your application's design system.
- **Security**: Use a proper session library (e.g., `gorilla/sessions`) instead of raw cookies in production.
- **Environment Variables**: Use a library like `godotenv` for local development and proper secrets management in production.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use server-side logging to debug OIDC flow issues.
- **Library Documentation**: Refer to the [go-oidc documentation](https://github.com/coreos/go-oidc) and [oauth2 documentation](https://pkg.go.dev/golang.org/x/oauth2) for advanced configuration.
