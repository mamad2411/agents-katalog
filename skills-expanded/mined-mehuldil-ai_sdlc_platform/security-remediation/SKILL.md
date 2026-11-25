---
name: security-remediation
description: Generate security remediation steps, fix strategies, and implementation guidance for vulnerabilities and issues
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Security Remediation Skill

Provides remediation strategies and implementation guidance for security issues detected in security scans.

## Remediation By Severity

### P0 (Critical) - Immediate Action
- **Exposed Secrets**: Rotate immediately, remove from code, use env variables
- **Critical Vulnerabilities**: Update dependency immediately, test thoroughly
- **Memory Leaks**: Fix cleanup, profile heap before/after

### P1 (High) - Fix Before Release
- **Unencrypted Storage**: Move to Keychain (iOS) / Keystore (Android)
- **Unhandled Async**: Add error handling, try-catch blocks
- **Unvalidated Input**: Add validation before use, sanitize input

### P2 (Medium) - Plan Remediation
- **Null Safety**: Add optional chaining, null checks
- **Weak Logging**: Remove PII from logs
- **Documentation**: Document security improvements

### P3 (Low) - Document for Future
- **Code Quality**: Refactor for consistency
- **Logging**: Improve logging patterns
- **Comments**: Add security-related comments

## Implementation Guidance

### Dependency Vulnerabilities
```bash
npm audit                    # Check vulnerabilities
npm audit fix                # Auto-fix available patches
npm audit --json > audit.json # Detailed analysis
npm install <package>@latest # Manual update
npm test                     # Verify no breaking changes
```

### Secrets Removal
```bash
brew install git-secrets     # Install tool
git secrets --install        # Initialize
git secrets --register-aws   # Add pattern
git secrets --scan -r        # Scan history
```

### HTTPS Enforcement
```javascript
const validateHttps = (url) => {
  if (!url.startsWith('https://')) {
    throw new Error(`Only HTTPS allowed: ${url}`);
  }
};
```

### Secure Storage
```typescript
// iOS Keychain
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword(key, value, {
  accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED,
});

// Android Keystore
import { EncryptedSharedPreferences } from '@react-native-encrypted-preferences';
await EncryptedSharedPreferences.setItem(key, value);
```

### Input Validation
```typescript
const validateUserId = (id: unknown): number => {
  const parsed = parseInt(String(id), 10);
  if (isNaN(parsed) || parsed <= 0) {
    throw new Error('Invalid user ID');
  }
  return parsed;
};
```

### Error Handling
```typescript
const safeOperation = async () => {
  try {
    return await riskyOperation();
  } catch (error) {
    logger.error('Operation failed', { error });
    showUserFriendlyError('Something went wrong');
    throw error;
  }
};
```

## Remediation Report

Documents:
- P0 issues and immediate fixes
- P1 issues and timeline
- P2 issues for planning
- P3 issues for documentation
- Implementation timeline
- Sign-off checklist

## Validation After Remediation

Testing Checklist:
- Vulnerabilities no longer present
- Functionality unchanged
- Error handling tested
- Performance impact verified
- Logs contain no PII
- Secrets management working
- Tests passing
- No regressions

Deployment Considerations:
- P0 fixes: Deploy immediately
- P1 fixes: Include in next release
- Security team sign-off required
- Release notes document fixes
- Monitoring alerts configured

## Triggers

Use when:
- Security scan identifies issues
- Vulnerability remediation plan needed
- Implementation guidance required
- Code review flagged security concern
- Post-remediation validation needed

---
