---
name: "security-http-headers-spring-boot"
description: "Configure all mandatory security HTTP response headers in LeadPerfection Spring Boot 3.2.x microservices — HSTS, CSP, X-Frame-Options, X-Content-Type-Options, CORS, and rate limiting via Azure APIM — to harden APIs against common web attacks detected by OWASP ZAP DAST."
version: 1
created: "2026-06-21"
updated: "2026-06-26"
---
## When to Use
Use after DAST scan reports missing security headers (ZAP rules 10016, 10020, 10021, 10038). Use when setting up a new microservice SecurityConfig. Use when APIM policies need hardening. Directly resolves ZAP FAIL findings from the dast-owasp-zap-spring-boot skill.

## Procedure
1. STEP 1 — SPRING SECURITY HEADER CONFIG: Add to SecurityConfig.java. All LP services are REST APIs (no browser UI) so CSP and frame options are still required for defence in depth.

@Configuration @EnableWebSecurity
public class SecurityConfig {
  @Bean
  public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
      .headers(headers -> headers
        .httpStrictTransportSecurity(hsts -> hsts
          .includeSubDomains(true).maxAgeInSeconds(31536000))
        .frameOptions(frame -> frame.deny())
        .contentTypeOptions(Customizer.withDefaults())
        .contentSecurityPolicy(csp -> csp
          .policyDirectives("default-src 'none'; frame-ancestors 'none'"))
        .referrerPolicy(ref -> ref
          .policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.NO_REFERRER))
        .permissionsPolicy(pp -> pp
          .policy("geolocation=(), microphone=(), camera=()")))
      .sessionManagement(s -> s
        .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
      .csrf(csrf -> csrf.disable())  // REST API — CSRF not applicable (JWT auth)
      .cors(cors -> cors.configurationSource(corsConfigurationSource()))
      .authorizeHttpRequests(auth -> auth
        .requestMatchers("/actuator/health", "/actuator/info").permitAll()
        .requestMatchers("/v3/api-docs/**", "/swagger-ui/**").permitAll()
        .anyRequest().authenticated())
      .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
    return http.build();
  }
2. STEP 2 — CORS CONFIGURATION BEAN: Restrict CORS to known BFF origins only. Never use allowedOrigins("*") on domain services.

  @Bean
  CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration cfg = new CorsConfiguration();
    // Only allow BFF origin — domain services are never called directly from browser
    cfg.setAllowedOrigins(List.of(
      "https://sales-bff.${environment}.renuity.com"));
    cfg.setAllowedMethods(List.of("GET", "POST", "OPTIONS"));
    cfg.setAllowedHeaders(List.of(
      "Authorization", "Content-Type",
      "X-Tenant-Ids", "X-Correlation-ID"));
    cfg.setMaxAge(3600L);
    cfg.setAllowCredentials(false);  // JWT in header, not cookie
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", cfg);
    return source;
  }
}
3. STEP 3 — AZURE APIM RATE LIMITING POLICY: Apply rate limiting at APIM layer for all LP APIs. Add to APIM inbound policy.

<inbound>
  <!-- Rate limiting: 100 calls per minute per client IP -->
  <rate-limit-by-key calls='100' renewal-period='60'
    counter-key='@(context.Request.IpAddress)'
    increment-condition='@(context.Response.StatusCode >= 200 && context.Response.StatusCode < 300)'/>
  <!-- Rate limiting: 1000 calls per minute per tenant -->
  <rate-limit-by-key calls='1000' renewal-period='60'
    counter-key='@(context.Request.Headers.GetValueOrDefault("X-Tenant-Ids","unknown"))'/>
  <!-- JWT Validation -->
  <validate-jwt header-name='Authorization' failed-validation-httpcode='401'
    failed-validation-error-message='Unauthorized'>
    <openid-config url='https://login.microsoftonline.com/${TENANT_ID}/v2.0/.well-known/openid-configuration'/>
    <required-claims>
      <claim name='aud'><value>${API_AUDIENCE}</value></claim>
    </required-claims>
  </validate-jwt>
  <!-- Remove internal headers before forwarding -->
  <set-header name='X-Powered-By' exists-action='delete'/>
  <set-header name='Server' exists-action='delete'/>
</inbound>
4. STEP 4 — REMOVE SERVER FINGERPRINT HEADERS: Prevent version disclosure. Add to application.yml:
server:
  error:
    include-stacktrace: never
    include-message: never  # do not expose exception messages in error responses
  servlet:
    encoding:
      charset: UTF-8

# Suppress default Spring Boot error details in responses
spring:
  mvc:
    problemdetails:
      enabled: true  # Use RFC 7807 Problem Details (no stack traces)
5. STEP 5 — PII REDACTION IN LOGS: Per common_patterns Pattern 12. Add a Log4j2 PatternLayout rewrite rule to redact sensitive fields.

# log4j2.xml — add RewriteAppender with PII redaction:
<Rewrite name='PiiRedactAppender'>
  <PiiRewritePolicy/>  # custom plugin that masks fields matching: name, address, phone, email, ssn
  <AppenderRef ref='ConsoleAppender'/>
</Rewrite>

# Alternatively, use MDC filtering in the JSON template:
# In LogstashEncoder config, add a custom MaskingJsonGeneratorDecorator
# that replaces values of keys matching /phone|address|email|ssn/i with '***REDACTED***'

## Pitfalls
- csrf().disable() is correct for stateless JWT REST APIs. Do NOT enable CSRF for REST services — it breaks all POST endpoints from non-browser clients.
- CORS allowedOrigins must be environment-specific (dev/uat/prod BFF hostname). Never use wildcard '*' even in dev. Wildcard CORS on a JWT-authenticated API is a ZAP FAIL finding.
- HSTS header is only effective over HTTPS. Ensure TLS 1.2+ is enforced at Azure Front Door before the HSTS header has any effect. Setting HSTS on HTTP-only endpoints is a no-op.
- Spring Boot includes X-Content-Type-Options and X-Frame-Options by default in Spring Security 6.x — verify they are not being overridden or removed by a custom header filter.
- Rate limiting at APIM is the first line of defence but domain services should also implement @RateLimiter from Resilience4j for secondary protection when calls bypass APIM (e.g., service-to-service).

## Verification
1. curl -I https://{dev-host}/api/v1/sales/appointments/detail | grep -E 'Strict-Transport|X-Frame|X-Content-Type|Content-Security' — all four headers present
2. ZAP DAST re-scan: rules 10016, 10020, 10021, 10038 should now show PASS
3. curl -X OPTIONS https://{dev-host}/api/v1/sales/appointments/detail -H 'Origin: https://evil.com' — response should NOT contain Access-Control-Allow-Origin: https://evil.com
4. curl https://{dev-host}/api/v1/sales/appointments/detail (no auth) — response body must NOT contain stack trace or Spring error details
5. Send 200 rapid requests to same endpoint — request 101+ should return HTTP 429 Too Many Requests from APIM