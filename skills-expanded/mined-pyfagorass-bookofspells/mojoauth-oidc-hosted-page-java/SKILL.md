---
name: mojoauth-oidc-hosted-page-java
description: Implement passwordless authentication in Java Spring Boot applications using MojoAuth OIDC with Spring Security.
---

# Implement MojoAuth OIDC (Java / Spring Boot)

This expert AI assistant guide walks you through integrating passwordless authentication into a Java Spring Boot application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Spring Boot 3.x application.
- Java 17+ and Maven or Gradle.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required dependency: `spring-boot-starter-oauth2-client`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:8080/login/oauth2/code/mojoauth`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

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

Add the MojoAuth OIDC configuration to `application.yml`:

```yaml
# src/main/resources/application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          mojoauth:
            client-id: your_client_id
            client-secret: your_client_secret
            scope: openid, profile, email
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/mojoauth"
        provider:
          mojoauth:
            issuer-uri: https://your-app.mojoauth.com
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
                .requestMatchers("/login", "/css/**", "/js/**").permitAll()
                .anyRequest().authenticated()
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

Since MojoAuth handles all authentication on its Hosted Login Page, your login page only needs a **"Sign In" link**:

```html
<!-- src/main/resources/templates/login.html -->
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head><title>Sign In</title></head>
<body>
  <div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    <div th:if="${param.error}" style="color: red;">
      Authentication failed. Please try again.
    </div>

    <a th:href="@{/oauth2/authorization/mojoauth}" class="sign-in-button">
      Sign In with MojoAuth
    </a>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
  </div>
</body>
</html>
```

#### Substep 2.5: Update Backend Logic

Create the necessary controllers:

**1. Auth Controller** (`AuthController.java`):

```java
// src/main/java/com/example/controller/AuthController.java
package com.example.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AuthController {

    @GetMapping("/login")
    public String loginPage() {
        return "login";
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

### Step 3: Test the Implementation

1. Start your application: `mvn spring-boot:run` or `./gradlew bootRun`.
2. Navigate to `http://localhost:8080/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/login/oauth2/code/mojoauth` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Customize `AuthenticationFailureHandler` for granular OIDC error handling.
- **Styling**: Adapt the Thymeleaf templates to match your application's design system (e.g., Bootstrap, Vaadin).
- **Security**: Store `client-secret` using Spring Cloud Config, HashiCorp Vault, or environment variables.
- **Session Management**: Configure Spring Session with Redis for distributed session management.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use Spring Boot logging (`application.yml`) to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Spring Security OAuth2 documentation](https://docs.spring.io/spring-security/reference/servlet/oauth2/login/index.html) for advanced configuration.
