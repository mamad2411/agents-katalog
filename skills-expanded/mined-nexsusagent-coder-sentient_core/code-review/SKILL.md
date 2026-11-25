# Code Review Skill

SENTIENT'nın derinlemesine kod inceleme yeteneği.

## Özellikler

Bu skill, OpenHarness'ın tool pattern'inden ve OpenClaw'ın review sisteminden adapte edilmiştir.

### İnceleme Alanları

1. **Güvenlik (Security)**
   - SQL injection açıkları
   - XSS vulnerabiliteleri
   - Hard-coded credentials
   - Unsafe memory operations

2. **Performans (Performance)**
   - Unnecessary allocations
   - Inefficient loops
   - Memory leaks
   - N+1 query problems

3. **Kod Stili (Style)**
   - Naming conventions
   - Code organization
   - Documentation coverage
   - Rust clippy compliance

4. **Bug Tespiti**
   - Null/None handling
   - Edge cases
   - Error handling
   - Race conditions

## Kullanım

```
sentient skill run code-review --path ./src --focus security
```

## Örnek Çıktı

```json
{
  "summary": "3 critical, 5 warning, 12 suggestion",
  "issues": [
    {
      "file": "src/auth.rs",
      "line": 45,
      "severity": "critical",
      "type": "security",
      "message": "Potential timing attack in password comparison",
      "suggestion": "Use constant_time_compare"
    }
  ],
  "score": 72
}
```

## Entegrasyon

Bu skill, SENTIENT'nın `oasis-hands` crate'i ile entegre çalışır.
Tool'lar: `read_file`, `grep_tool`, `glob_tool`

---
*SENTIENT - The She-Wolf That Guards Your Empire*
