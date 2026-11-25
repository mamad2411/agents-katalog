---
name: nextjs-intl-translation-structure-consistency
description: |
  Fix TypeScript type errors in next-intl when translation keys don't match across locale files.
  Use when: (1) Getting "Types of property are incompatible" errors in i18n helper files,
  (2) Adding new translation sections and getting type errors, (3) Property missing errors
  across locale files, (4) Type errors mentioning specific translation keys after adding
  new translations. Covers next-intl with TypeScript in Next.js 13+ App Router projects.
author: Claude Code
version: 1.0.0
date: 2026-01-29
---

# Next.js i18n Translation Structure Consistency

## Problem

When working with next-intl in TypeScript projects, adding new translation sections can cause
cryptic type errors if the structure doesn't match exactly across all locale files. TypeScript
requires all locale files to have identical key structures (including key naming conventions
and nested sections).

## Context / Trigger Conditions

This issue occurs when:

1. **Error message pattern**:
   ```
   error TS2322: Type '{ ... }' is not assignable to type '{ ... }'.
   The types of '"sectionName"["subsection"]' are incompatible between these types.
   Property '"missingKey"' is missing in type '{ ... }' but required in type '{ ... }'.
   ```

2. **Specific scenarios**:
   - Added new translation section to `en.json` but forgot to add to other locale files
   - Used inconsistent key naming (e.g., `camelCase` vs `snake_case`)
   - Added new nested keys but missed them in some locale files
   - Reordered keys differently across locale files (though this alone won't cause errors)

3. **File location**: Errors typically appear in `lib/i18n-helpers.tsx` or similar files that
   import and validate translation types

## Solution

### Step 1: Identify the Exact Mismatch

The error message will tell you:
- Which section has the mismatch (e.g., `"adminVerification"["documentReview"]`)
- Which specific key is missing or incompatible (e.g., `"summary"`, `"pending_revalidation"`)

Example error:
```
Property '"summary"' is missing in type '{ statusBadge: {...}, actions: {...} }'
but required in type '{ statusBadge: {...}, actions: {...}, summary: {...} }'
```

This means the `summary` key exists in `en.json` but is missing in other locale files.

### Step 2: Compare Translation Files

Use grep to find where the section exists:
```bash
grep -n '"sectionName":' apps/web/strings/*.json
```

Check that ALL locale files have the exact same structure.

### Step 3: Fix Key Naming Inconsistencies

**Common pitfall**: Mixing snake_case and camelCase in the same project.

❌ Wrong (inconsistent):
```json
// en.json
"statusBadge": {
  "pendingRevalidation": "Pending Revalidation"
}

// ur.json
"statusBadge": {
  "pending_revalidation": "Pending Revalidation"
}
```

✅ Correct (consistent):
```json
// Both files
"statusBadge": {
  "pending_revalidation": "Pending Revalidation"
}
```

### Step 4: Add Missing Sections

For each locale file (`en.json`, `ur.json`, `ar.json`, etc.), ensure the new section exists
with the EXACT same structure:

```json
"newSection": {
  "subsection": {
    "key1": "[LOCALE] Translation text",
    "key2": "[LOCALE] Translation text"
  }
}
```

Use locale prefixes like `[UR]`, `[AR]`, `[SO]` for non-English translations until proper
translations are available.

### Step 5: Verify with Type Check

```bash
turbo types
```

The error should disappear if all structures match exactly.

## Verification

1. **Type check passes**: `turbo types` runs without errors
2. **All locale files have identical keys**: Use diff to compare structure:
   ```bash
   # Extract keys only (remove translation text)
   jq 'walk(if type == "object" then with_entries(.value = "...") else . end)' \
      apps/web/strings/en.json > /tmp/en-structure.json
   jq 'walk(if type == "object" then with_entries(.value = "...") else . end)' \
      apps/web/strings/ur.json > /tmp/ur-structure.json
   diff /tmp/en-structure.json /tmp/ur-structure.json
   ```
3. **Application loads without i18n errors**: No runtime errors about missing keys

## Example

**Scenario**: Added `documentReview` section to English translations, got type error.

**Error**:
```
lib/i18n-helpers.tsx(15,3): error TS2322: Type '{ ... }' is not assignable to type '{ ... }'.
  The types of '"adminVerification"["documentReview"]' are incompatible between these types.
    Property '"summary"' is missing in type '{ ... }' but required in type '{ ... }'.
```

**Root cause**:
1. Added `documentReview` to `en.json` with `summary` subsection
2. Added `documentReview` to other locale files but forgot `summary` subsection
3. Used `pendingRevalidation` (camelCase) instead of `pending_revalidation` (snake_case)

**Fix**:
```bash
# Check which files have the section
grep -n '"documentReview":' apps/web/strings/*.json

# Compare structure
# Found en.json has "summary" and "pending_revalidation"
# ur.json, ar.json, so.json were missing "summary" and had "pendingRevalidation"

# Edit each file to match en.json structure exactly
```

After adding the missing `summary` section and fixing snake_case consistency, type check passed.

## Notes

### Key Naming Conventions

- **Stick to one convention**: Choose either `camelCase` or `snake_case` and use it consistently
- **Next-intl default**: The library doesn't enforce a convention, but TypeScript type inference
  requires exact matches
- **Status enums**: Database enum values often use `SCREAMING_SNAKE_CASE` (e.g., `PENDING_REVALIDATION`),
  but translation keys typically use lowercase `snake_case` (e.g., `pending_revalidation`)

### Common Mistakes

1. **Adding section to English only**: Always add to ALL locale files simultaneously
2. **Inconsistent nesting depth**: All locales must have the same depth of nesting
3. **Missing optional sections**: Even optional sections must exist in all files (can be empty objects)
4. **Case sensitivity**: `camelCase` ≠ `camelcase` - JavaScript object keys are case-sensitive

### Prevention

1. **Use a script**: Create a script to validate all locale files have matching structures
2. **Git pre-commit hook**: Check structure consistency before allowing commits
3. **Add to CI/CD**: Run structure validation in GitHub Actions
4. **Use i18n linting tools**: Tools like `i18n-unused` can catch missing keys

### Alternative Solutions

If you need truly optional sections, consider:
```typescript
// Type definition that allows undefined
type Translations = {
  section?: {
    key: string;
  };
};
```

However, next-intl's type inference doesn't support this pattern well. It's better to include
all sections in all files.

## References

- [next-intl Type-safe translations](https://next-intl.dev/docs/usage/typescript)
- [next-intl Messages structure](https://next-intl.dev/docs/usage/messages)
- [TypeScript Strict Mode with i18n](https://next-intl.dev/docs/workflows/typescript)
