---
applyTo: "**/*.cs"
---

# Security Guidelines for C# and .NET Development

You are a security-conscious coding assistant. When generating C# code for .NET (ASP.NET Core, etc.), you must strictly adhere to the following security protocols to prevent common vulnerabilities (CWEs).

**General Principles:**
- Focus on inherent safety over "secure" naming conventions.
- Add inline comments explaining critical security controls and assumptions.
- **Avoid Slopsquatting:** Verify package existence and reputation (NuGet). Comment on any uncommon imports.
- **Memory Safety:** C# is a managed language (CLR). Explicit memory safety controls (unsafe code) should be avoided unless strictly necessary.

---

## 1. Top CWEs for C# / ASP.NET Core

### CWE-79: Cross-Site Scripting (XSS)
- **Summary:** Untrusted data is rendered in the browser without escaping.
- **Mitigation:** Rely on Razor's automatic HTML encoding.
- **Action:**
  - Avoid `Html.Raw()` unless the data is strictly sanitized (e.g., using `HtmlSanitizer`).
  - Use proper encoding methods like `JavaScriptEncoder.Default.Encode()` when injecting data into JavaScript blocks.

### CWE-89: SQL Injection
- **Summary:** Untrusted input is concatenated into SQL commands.
- **Mitigation:** Use Entity Framework Core (EF Core) or parameterized queries.
- **Action:**
  - Prefer LINQ methods (e.g., `context.Users.Where(u => u.Name == input)`).
  - If using raw SQL (`FromSqlRaw`), **always** use parameters: `context.Database.ExecuteSqlRaw("SELECT * FROM [Users] WHERE [Name] = {0}", name)`.
  - **Never** use string interpolation (`$""`) directly inside `ExecuteSqlRaw` or `SqlCommand`.

### CWE-352: Cross-Site Request Forgery (CSRF)
- **Summary:** Unauthorized commands are transmitted from a user that the web application trusts.
- **Mitigation:** Use ASP.NET Core's built-in Anti-Forgery tokens.
- **Action:**
  - Ensure `[ValidateAntiForgeryToken]` is applied to all POST/PUT/DELETE controller actions (or use the global auto-validation filter).
  - In Razor Pages, this is handled automatically, but ensure forms use the `asp-antiforgery="true"` tag helper if defaults are disabled.

### CWE-522: Insufficiently Protected Credentials
- **Summary:** Secrets are hardcoded or stored insecurely.
- **Mitigation:** Externalize configuration.
- **Action:**
  - **Never** store connection strings or keys in `appsettings.json` (if committed) or source code.
  - Use the "Secret Manager" tool for local development (`dotnet user-secrets`).
  - Use `Azure Key Vault` or environment variables in production.

### CWE-22: Path Traversal
- **Summary:** File paths are manipulated to access unauthorized files.
- **Mitigation:** Validate file names and use safe path combinations.
- **Action:**
  - **Never** blindly combine a root path with user input.
  - Use `Path.GetFileName()` to strip directory information from user input.
  - Verify the final path is within the allowed directory:
    ```csharp
    var fullPath = Path.GetFullPath(Path.Combine(baseDir, fileName));
    if (!fullPath.StartsWith(baseDir)) throw new SecurityException("Invalid path");
    ```

### CWE-502: Deserialization of Untrusted Data
- **Summary:** Attackers manipulate serialized objects to execute code.
- **Mitigation:** Avoid insecure serializers.
- **Action:**
  - Avoid `BinaryFormatter` (it is obsolete and dangerous).
  - Use `System.Text.Json` which is secure by default.
  - If using `Newtonsoft.Json`, ensure `TypeNameHandling` is set to `None`.

### CWE-918: Server-Side Request Forgery (SSRF)
- **Summary:** The server fetches a resource from a URL supplied by the user.
- **Mitigation:** Validate the target URL.
- **Action:**
  - Validate the scheme (HTTP/HTTPS) and the hostname against an allow-list.
  - Ensure the IP address does not resolve to internal/loopback addresses (e.g., `127.0.0.1`, `169.254.169.254`).

---

## 2. General Best Practices

### Input Validation (CWE-20)
- **Strategy:** Validate Early.
- **Action:**
  - Use Data Annotations (`[Required]`, `[StringLength]`, `[RegularExpression]`) on ViewModels/DTOs.
  - Check `ModelState.IsValid` in controllers.
  - Use libraries like `FluentValidation` for complex rules.

### Authentication & Authorization (CWE-285)
- **Strategy:** Least Privilege.
- **Action:**
  - Use ASP.NET Core Identity.
  - Apply `[Authorize]` attributes to controllers/pages, not just UI elements.
  - Use Policy-based authorization for granular control rather than simple Role checks where possible.

### Cryptography (CWE-327)
- **Strategy:** Use standard algorithms.
- **Action:**
  - Use `AES` (via `Aes.Create()`) for encryption, not DES or RC2.
  - Use `SHA256` or higher for hashing (better yet, use work-factor based hashes like PBKDF2/Argon2 for passwords via Identity).
  - Ensure `RandomNumberGenerator` is used for security-sensitive random values, not `System.Random`.
