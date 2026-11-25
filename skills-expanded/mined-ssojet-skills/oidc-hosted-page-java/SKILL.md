---
name: oidc-hosted-page-java
description: Implement "Sign in with SSO" in Java Spring Boot applications using SSOJet OIDC with Spring Security.
---

# Implement SSOJet OIDC (Java / Spring Boot)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a Java Spring Boot application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing Spring Boot 3.x application with a login page.
- Java 17+ and Maven or Gradle.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required dependency: `spring-boot-starter-oauth2-client`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MySpringApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:8080/login/oauth2/code/ssojet`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing Spring Boot Project

#### Substep 2.1: Add Dependencies

Add the following dependency to your `pom.xml`:

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

Or for Gradle (`build.gradle`):

```groovy
implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
```

#### Substep 2.2: Configure OIDC Properties

Add the SSOJet OIDC configuration to `application.yml`:

```yaml
# src/main/resources/application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          ssojet:
            client-id: your_client_id
            client-secret: your_client_secret
            scope: openid, profile, email
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/ssojet"
        provider:
          ssojet:
            issuer-uri: https://auth.ssojet.com
```

#### Substep 2.3: Configure Security

Create a security configuration class (e.g., `SecurityConfig.java`):

```java
// src/main/java/com/example/config/SecurityConfig.java
package com.example.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login", "/auth/sso", "/css/**", "/js/**").permitAll()
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/dashboard", true)
                .permitAll()
            )
            .oauth2Login(oauth2 -> oauth2
                .loginPage("/login")
                .defaultSuccessUrl("/dashboard", true)
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login")
            );

        return http.build();
    }
}
```

#### Substep 2.4: Update Login Page/UI

Create or modify your login page template (e.g., `src/main/resources/templates/login.html`):

```html
<!-- src/main/resources/templates/login.html -->
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Sign In</h1>

    <div th:if="${param.error}" style="color: red;">
      Authentication failed. Please try again.
    </div>

    <!-- Traditional Login Form -->
    <form id="loginForm" th:action="@{/login}" method="post">
      <div>
        <label for="username">Email</label>
        <input type="email" id="username" name="username" required />
      </div>

      <div id="passwordField">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      </div>

      <input type="hidden" id="isSSO" name="isSSO" value="false" />

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
      const form = document.getElementById('loginForm');

      if (isSSO.value === 'false') {
        isSSO.value = 'true';
        passwordField.style.display = 'none';
        document.getElementById('password').removeAttribute('required');
        submitBtn.textContent = 'Continue with SSO';
        ssoToggle.textContent = 'Back to Password Login';
        // Change form action to SSO initiation endpoint
        form.action = '/auth/sso';
        form.method = 'get';
      } else {
        isSSO.value = 'false';
        passwordField.style.display = 'block';
        document.getElementById('password').setAttribute('required', 'true');
        submitBtn.textContent = 'Sign In';
        ssoToggle.textContent = 'Sign in with SSO';
        form.action = '/login';
        form.method = 'post';
      }
    }
  </script>
</body>
</html>
```

#### Substep 2.5: Update Backend Logic

Create the necessary controller to handle SSO initiation and the dashboard:

**1. Auth Controller** (`AuthController.java`):

```java
// src/main/java/com/example/controller/AuthController.java
package com.example.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AuthController {

    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    @GetMapping("/auth/sso")
    public String ssoRedirect(@RequestParam(required = false) String username) {
        // Redirect to SSOJet's OAuth2 authorization with login_hint
        String redirectUrl = "/oauth2/authorization/ssojet";
        if (username != null && !username.isEmpty()) {
            redirectUrl += "?login_hint=" + username;
        }
        return "redirect:" + redirectUrl;
    }
}
```

**2. Dashboard Controller** (`DashboardController.java`):

```java
// src/main/java/com/example/controller/DashboardController.java
package com.example.controller;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    @GetMapping("/dashboard")
    public String dashboard(@AuthenticationPrincipal OidcUser user, Model model) {
        if (user != null) {
            model.addAttribute("name", user.getFullName());
            model.addAttribute("email", user.getEmail());
            model.addAttribute("claims", user.getClaims());
        }
        return "dashboard";
    }
}
```

**3. Dashboard Template** (`src/main/resources/templates/dashboard.html`):

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head><title>Dashboard</title></head>
<body>
  <h1>Dashboard</h1>
  <p th:if="${name}">Welcome, <span th:text="${name}">User</span>!</p>
  <pre th:text="${claims}"></pre>
  <a th:href="@{/logout}">Logout</a>
</body>
</html>
```

### Step 3: Test the Modified Connection

1. Start your application: `mvn spring-boot:run` or `./gradlew bootRun`.
2. Navigate to your login page (e.g., `http://localhost:8080/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/login/oauth2/code/ssojet` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Customize `AuthenticationFailureHandler` for granular OIDC error handling.
- **Styling**: Adapt the Thymeleaf templates to match your application's design system (e.g., Bootstrap, Vaadin).
- **Security**: Store `client-secret` using Spring Cloud Config, HashiCorp Vault, or environment variables.
- **Session Management**: Configure Spring Session with Redis for distributed session management.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use Spring Boot logging (`application.yml`) to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Spring Security OAuth2 documentation](https://docs.spring.io/spring-security/reference/servlet/oauth2/login/index.html) for advanced configuration.
