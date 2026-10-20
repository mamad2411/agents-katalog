# Security Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x (Spring Security 6, `jakarta.*`),
Spring Data JPA, Bean Validation (`jakarta.validation`). The rules themselves are
framework-agnostic — these examples only show one concrete stack.
**Translation hints:** Quarkus → `quarkus-security`/`@RolesAllowed`; Jakarta EE →
`jakarta.security`/`@RolesAllowed`; plain servlets → a filter enforcing the same
checks. **Version-sensitive:** Spring Security 6 uses the lambda DSL and
`jakarta.*`; Boot 2.x/Security 5 uses `javax.*` and `WebSecurityConfigurerAdapter`.

## Rule 1 — Authenticate then authorize, deny by default
Violation:
```java
@GetMapping("/admin/report")               // no auth annotation, no filter rule
public Report report() { return svc.build(); }
```
Correct:
```java
// SecurityFilterChain: anyRequest().authenticated(), specific rules deny-by-default
@GetMapping("/admin/report")
@PreAuthorize("hasRole('ADMIN')")          // explicit grant; closed until opened
public Report report() { return svc.build(); }
```

## Rule 2 — Object-level authorization (IDOR/BOLA)
Violation:
```java
@GetMapping("/accounts/{id}")
public Account get(@PathVariable long id) {
    return repo.findById(id).orElseThrow();   // any logged-in user reads any account
}
```
Correct:
```java
@GetMapping("/accounts/{id}")
public Account get(@PathVariable long id, @AuthenticationPrincipal User me) {
    return repo.findByIdAndOwnerId(id, me.id())   // scoped to the caller
               .orElseThrow(() -> new AccountNotFoundException(id));
}
```

## Rule 3 — Validate untrusted input at the boundary
Violation:
```java
public void rename(@RequestBody Map<String,Object> body) {
    String name = (String) body.get("name");   // untyped, unbounded, unvalidated
}
```
Correct:
```java
public record RenameRequest(@NotBlank @Size(max = 100) String name) {}
public void rename(@Valid @RequestBody RenameRequest req) { ... }  // @Valid enforced
```

## Rule 4 — Make injection structurally impossible
Violation:
```java
em.createQuery("SELECT t FROM Txn t WHERE t.note = '" + note + "'");   // SQL/JPQL injection
Runtime.getRuntime().exec("sh -c 'convert " + userPath + "'");         // command injection
```
Correct:
```java
em.createQuery("SELECT t FROM Txn t WHERE t.note = :note")
  .setParameter("note", note);                                        // bound param
new ProcessBuilder("convert", userPath).start();                      // arg array, no shell
```

## Rule 5 — Encode output for its sink (XSS)
Violation:
```java
model.addAttribute("html", "<div>" + userComment + "</div>");   // raw into template
// template: <div th:utext="${html}"></div>  <!-- utext = unescaped -->
```
Correct:
```java
model.addAttribute("comment", userComment);
// template: <div th:text="${comment}"></div>  <!-- th:text auto-escapes -->
```

## Rule 6 — No secrets in source
Violation:
```java
private static final String API_KEY = "sk_live_5f3a...";   // credential literal
```
Correct:
```java
private final String apiKey;                               // from config (config-warden)
Client(@Value("${rates.api-key}") String apiKey) { this.apiKey = apiKey; }
```

## Rule 7 — Never leak sensitive data outward
Violation:
```java
return ResponseEntity.status(500).body(ex.toString());   // stack + internals to client
log.info("login user={} pwd={}", email, rawPassword);    // secret in logs
```
Correct:
```java
return ResponseEntity.status(500).body(new ApiError("INTERNAL", "Unexpected error"));
log.info("login attempt user={}", email);                // no secret (see observability-warden)
```

## Rule 8 — Store credentials safely
Violation:
```java
user.setPassword(md5(raw));                    // fast, unsalted hash
if (token.equals(stored)) ...                  // non-constant-time compare
```
Correct:
```java
user.setPassword(passwordEncoder.encode(raw)); // BCryptPasswordEncoder (adaptive)
MessageDigest.isEqual(token.getBytes(), stored.getBytes());   // constant time
```

## Rule 9 — Secure cookies, sessions, CORS
Violation:
```java
cors.setAllowedOrigins(List.of("*"));
cors.setAllowCredentials(true);                // '*' + credentials: forbidden combo
ResponseCookie.from("session", id).build();    // not HttpOnly/Secure/SameSite
```
Correct:
```java
cors.setAllowedOrigins(List.of("https://app.example.com"));   // explicit allow-list
ResponseCookie.from("session", id).httpOnly(true).secure(true).sameSite("Lax").build();
// CSRF protection enabled for state-changing form/session flows
```

## Rule 10 — Third-party responses are untrusted too
Violation:
```java
String html = ratesClient.fetchWidget();       // remote HTML
model.addAttribute("widget", html);            // reflected verbatim into page
```
Correct:
```java
RateDto dto = ratesClient.fetchRate();         // typed, validated at the seam
if (dto.rate() == null) throw new RatesUnavailableException();
model.addAttribute("rate", dto.rate());        // only validated scalar used
```
