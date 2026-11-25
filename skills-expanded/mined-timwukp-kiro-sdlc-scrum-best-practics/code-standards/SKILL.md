---
name: code-standards
description: Validate Java and TypeScript code against banking naming conventions, style rules, quality standards, and secure coding practices
---

# Code Standards Skill

## When to Use
Invoke when reviewing code for standards compliance, setting up new modules, or validating secure coding patterns.

## Secure Coding Defaults

### Never Trust Input
- All external input is untrusted until validated server-side
- Deny by default: reject any input that does not match expected format
- Validate at the boundary (controller/handler layer), not deep in business logic

### Input Validation Patterns
- Prefer whitelist (allowlist) over blacklist (denylist)
- Validate type, length, range, and format for every input field
- Use strong typing: parse inputs into domain objects immediately
- Reject unexpected fields in request bodies (strict deserialization)

### Output Encoding Requirements
- HTML encode all user-supplied content rendered in web pages
- JSON encode all user-supplied content in API responses
- URL encode all user-supplied content placed in URLs
- Never build SQL, HTML, or shell commands by string concatenation

### Secure Error Handling
- Never expose stack traces in API responses
- Return generic error messages to clients (e.g., "An error occurred")
- Log detailed error information server-side only
- Never include sensitive data (credentials, tokens, PII) in error messages
- Use correlation IDs to link client errors to server-side logs

## Java Standards (Google Java Style + Banking Extensions)
- Class names: PascalCase (AccountService, TransactionController)
- Methods: camelCase (getAccountBalance, processTransfer)
- Constants: UPPER_SNAKE_CASE (MAX_TRANSFER_AMOUNT, DEFAULT_CURRENCY)
- Packages: com.bank.{domain}.{layer} (com.bank.account.service)

## License Header (Required for all Java files)
```java
/*
 * Copyright (c) 2025 [Your Bank Name]. All rights reserved.
 * Licensed under the terms of your organization's software license.
 */
```

## TypeScript Standards
- Components: PascalCase (AccountCard.tsx, TransactionList.tsx)
- Hooks: camelCase with use prefix (useAccountBalance, useTransferForm)
- Types/Interfaces: PascalCase with descriptive suffix (AccountCardProps, TransferFormState)
- Constants: UPPER_SNAKE_CASE in dedicated constants files

## Import Ordering
1. Java standard library (java.*, javax.*)
2. Third-party libraries (org.*, com.*)
3. Internal packages (com.bank.*)
4. Static imports last

## Documentation Requirements
- All public classes: Javadoc with @author, @since
- All public methods: Javadoc with @param, @return, @throws
- Complex algorithms: inline comments explaining the "why"
- API endpoints: OpenAPI annotations (@Operation, @ApiResponse)
