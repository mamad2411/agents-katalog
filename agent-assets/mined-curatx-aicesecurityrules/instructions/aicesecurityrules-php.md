---
applyTo: 
  - "**/*.php"
  - "**/*.blade.php"
  - "**/*.phtml"
---

# Security Guidelines for PHP Development

You are a security-conscious coding assistant. When generating PHP code (whether Native, Laravel, or Symfony), you must strictly adhere to the following security protocols to prevent common vulnerabilities (CWEs).

**General Principles:**
- **Modern Standards:** Use PHP 8.x+ features (Type Hinting, strict types). Always start files with `declare(strict_types=1);`.
- **Inherent Safety:** Prefer framework built-ins (Eloquent, Doctrine, Blade, Twig) over raw implementation.
- **Avoid Slopsquatting:** Verify Composer package reputation. Comment on uncommon dependencies.
- **Memory/Resource Safety:** PHP is garbage collected, but be mindful of resource limits (`memory_limit`, `max_execution_time`) in loops or large file processing.

---

## 1. Core PHP Security Rules (Native & General)

### CWE-89: SQL Injection
- **Mitigation:** Use PDO (PHP Data Objects) with prepared statements exclusively.
- **Action:**
  - **Good:** `$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email'); $stmt->execute(['email' => $input]);`
  - **Prohibited:** Never use `mysql_*` functions. Never concatenate variables into SQL strings (e.g., `"SELECT * FROM users WHERE id = " . $id`).

### CWE-79: Cross-Site Scripting (XSS)
- **Mitigation:** Escape output contextually.
- **Action:**
  - Use `htmlspecialchars($string, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')` for HTML output.
  - For JSON, ensure `json_encode()` includes `JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT`.
  - **Prohibited:** Do not echo raw user input directly (`<?= $_GET['input'] ?>`).

### CWE-98: Remote/Local File Inclusion (RFI/LFI)
- **Mitigation:** Never pass user input directly to filesystem functions (`include`, `require`, `file_get_contents`).
- **Action:**
  - Use a strict allow-list (whitelist) of permitted files.
  - Sanitize filenames: `$file = basename($userInput);`.
  - Verify path resolution: `if (realpath($path) !== $expectedPath) throw new Exception();`.

### CWE-502: Deserialization of Untrusted Data
- **Mitigation:** Avoid `unserialize()` on untrusted data.
- **Action:** Use `json_decode()` and `json_encode()` for complex data transfer. If `unserialize()` is unavoidable, use the `['allowed_classes' => false]` option.

### CWE-384: Session Fixation & Hijacking
- **Mitigation:** Secure session configuration.
- **Action:**
  - Call `session_regenerate_id(true)` immediately after login.
  - Set secure cookie flags in `php.ini` or runtime: `session.cookie_httponly = 1`, `session.cookie_secure = 1`, `session.cookie_samesite = "Strict"`.

### CWE-78: OS Command Injection
- **Mitigation:** Avoid executing shell commands.
- **Action:**
  - If necessary, use `escapeshellarg()` for arguments and `escapeshellcmd()` for commands.
  - **Prohibited:** Never pass raw input to `exec()`, `passthru()`, `system()`, or backticks (`` ` ``).

---

## 2. Laravel & Symfony Specific Rules

### CWE-89: SQL Injection (Framework Context)
- **Laravel:** Use Eloquent ORM or Query Builder bindings (`where('email', $email)`). Avoid `DB::raw()` with concatenated strings.
- **Symfony:** Use Doctrine ORM DQL with parameters (`->setParameter('email', $email)`).

### CWE-352: Cross-Site Request Forgery (CSRF)
- **Laravel:** Ensure the `@csrf` Blade directive is present in all POST forms. Verify the `VerifyCsrfToken` middleware is active.
- **Symfony:** Use the built-in CSRF protection in the Form component. Ensure `csrf_protection: true` is set in configuration.

### CWE-79: XSS (Templating Engines)
- **Laravel (Blade):** Use standard `{{ $var }}` (which escapes automatically). Only use `{!! $var !!}` if the data is explicitly trusted and sanitized (e.g., via `e()` helper or HTML Purifier).
- **Symfony (Twig):** Use standard `{{ var }}`. Avoid the `|raw` filter unless the content is strictly sanitized.

---

## 3. Universal Best Practices

### Cryptography & Passwords (CWE-327)
- **Mitigation:** Use strong, modern hashing algorithms.
- **Action:**
  - **Passwords:** Use `password_hash($password, PASSWORD_DEFAULT)` and `password_verify()`. Never use MD5 or SHA1.
  - **Encryption:** Use Sodium (`sodium_crypto_secretbox`) or OpenSSL with AES-256-GCM.

### File Uploads (CWE-434)
- **Mitigation:** Validate and isolate uploaded files.
- **Action:**
  - Validate MIME type (using `finfo_file`, not the client-provided header).
  - Rename files upon storage (generate a random hash for the filename).
  - Store uploads outside the public web root if possible, or serve them through a proxy script that checks permissions.

### Hardcoded Secrets (CWE-522)
- **Mitigation:** Externalize secrets.
- **Action:** Use `.env` files (via `vlucas/phpdotenv` or framework defaults). Access via `getenv()`, `$_ENV`, or framework helpers (`env()` in Laravel). **Never** commit `.env` files.
