---
description: "camofox-browser anti-patterns — common mistakes to avoid"
alwaysApply: true
---

# Anti-Patterns (Avoid These)

## 1) Skipping snapshot before actions
```bash
# BAD
camofox click e4

# GOOD
camofox snapshot
camofox click e4
```

## 2) Reusing refs after navigation/rerender
```bash
# BAD
camofox click e9
camofox navigate https://another-page.com
camofox click e9

# GOOD
camofox click e9
camofox navigate https://another-page.com
camofox snapshot
camofox click e3
```

## 3) Mixing `userId` across same tab flow
```bash
# BAD
camofox open https://x.com --user alice
camofox snapshot --user bob

# GOOD
camofox open https://x.com --user alice
camofox snapshot --user alice
```

## 4) Parsing text output in automation
```bash
# BAD
camofox get-url | awk '{print $2}'

# GOOD
camofox get-url --format json
```

## 5) Hardcoded query URLs instead of macros
```bash
# BAD
# manually composing search URL every time

# GOOD
# API macro use
# {"macro":"@google_search","query":"my query"}
```

## 6) Embedding plaintext credentials in scripts
```bash
# BAD
type e2 "my-secret-password"

# GOOD
camofox auth save profile
camofox auth load profile --inject --username-ref e2 --password-ref e3
```

## 7) Forgetting tab invalidation after display toggle
```bash
# BAD
# toggle display then keep using old tabId

# GOOD
# toggle display, then create a new tab
```

## 8) Assuming `download` command performs server-side direct fetch
```bash
# BAD
camofox download https://files.example.com/a.zip

# GOOD
camofox downloads --format json
# or call /tabs/:tabId/batch-download
```
