---
name: psm-knowledge
description: Provides comprehensive knowledge about ByteDance's PSM (Product, Subsystem, Module) naming convention for microservices. Use when user asks to create a new service, validate PSM names, or needs to understand ByteDance's service naming standards.
---

# PSM Knowledge Skill

## When to Use This Skill

- User asks to create a new service and needs to determine its PSM name
- User mentions "PSM", "service name", or "naming convention" in the context of ByteDance
- User needs to validate existing PSM names for compliance
- User is integrating PSM validation into service deployment processes
- User needs to train team members on ByteDance's service naming conventions

## How It Works

1. **Analyze the Request**
   - Identify if the user needs PSM naming guidance or validation
   - Determine the service type (standard service vs. SaaS-type service)

2. **Apply Naming Rules**
   - Ensure P.S.M three-part format (separated by dots)
   - Validate character set: English characters, numbers, underscores (no hyphens in P.S)
   - Check for prohibited patterns: `..`, `service` prefix, leading/trailing underscores
   - Verify length limit: varchar(64)

3. **Provide Recommendations**
   - Suggest meaningful module names instead of generic ones
   - Recommend lowercase consistency
   - Advise on uniqueness verification through Service Tree

4. **Validate and Confirm**
   - Check against mandatory requirements
   - Verify best practices compliance
   - Recommend official API validation before service creation

## Examples

### Example 1: Creating a New Service

**User Request**: "I'm creating a new article service, what should be its PSM name?"

**Action**:
1. Identify product: `toutiao`
2. Identify subsystem: `article`
3. Identify module: `article` (meaningful name)

**Output**:
```
Recommended PSM: toutiao.article.article

Validation:
✓ Follows P.S.M format
✓ No prohibited patterns
✓ Lowercase consistency
✓ Meaningful module name
✓ Length within limit (21 characters)

Next Step: Verify uniqueness in Service Tree before creating the service.
```

### Example 2: SaaS-Type Service

**User Request**: "I need to create a Redis instance for a user, what PSM format should I use?"

**Action**:
1. Identify service type: SaaS-type (Redis)
2. Apply SaaS naming pattern: P.S prefix with user-defined M

**Output**:
```
Recommended PSM Pattern: toutiao.redis.xxx

Where xxx is user-defined module name.

Example: toutiao.redis.cache
Example: toutiao.redis.session

Note: For SaaS services, use fixed P.S prefix and allow M to be user-defined.
```

### Example 3: PSM Validation

**User Request**: "Is `toutiao.comment.comment_post_service` a valid PSM?"

**Action**:
1. Check P.S.M format: ✓
2. Check character set: ✓
3. Check prohibited patterns:
   - Contains `service` prefix in module: ✗
   - Too verbose and uses generic terms: ✗

**Output**:
```
Validation Result: INVALID

Issues Found:
✗ Module contains 'service' keyword prefix (causes issues with Consul registration)
✗ Too verbose and uses generic terms

Suggested Alternatives:
- toutiao.comment.post
- toutiao.comment.item
- toutiao.comment.thread

Please choose a more concise and meaningful module name.
```

## Core Knowledge

### PSM Definition

PSM stands for Product, Subsystem, and Module, which is the standard naming convention for identifying services at ByteDance. Before developing any service, you must first determine its PSM name following the specified guidelines.

### Naming Specifications

#### Mandatory Requirements

- **Format**: Must follow the P.S.M three-part format (separated by dots)
- **Character Set**: Each part must consist of English characters and/or numbers. Underscores can be used to connect multiple English words
- **Prohibited Patterns**: None of the parts can contain `..`
- **Hyphen Usage**: Product and Subsys cannot contain `-`, but Module can contain `-`
- **Service Keyword**: None of the parts can be prefixed with the `service` keyword (this causes issues with service registration in Consul)
- **Underscore Placement**: No part can start or end with the `_` character
- **Case Sensitivity**: PSM is case-sensitive
- **Length Limit**: Maximum length of varchar(64)
- **Uniqueness**: Must be unique across the entire company (verified through Service Tree)

#### Best Practices

- **Avoid Underscores**: While allowed, it's recommended to avoid using underscores
- **Meaningful Names**: Module should use meaningful names instead of generic ones
- **Lowercase Consistency**: All parts should be in lowercase for uniform naming style

### SaaS-Type Service Naming

For SaaS-type services, it's recommended to use fixed P.S or P prefixes, allowing M or S.M to be user-defined. Examples:
- MySQL instances: `toutiao.mysql.xxx`
- Redis services: `toutiao.redis.xxx`

### Reference Examples

#### Good Examples

- `toutiao.article.article`
- `toutiao.article.item`
- `toutiao.stream.stream`
- `toutiao.stream.impression`
- `toutiao.passport.session`
- `toutiao.user.odin`
- `toutiao.collect.applog`
- `toutiao.collect.monitor`
- `toutiao.user.info`

#### Bad Examples

- `toutiao.pgc.article-service` (unnecessary suffix)
- `toutiao.comment.comment_post_service` (too verbose and uses generic terms)

## Key Considerations

- Always follow the three-part P.S.M format
- Ensure PSM uniqueness across the company
- Use meaningful and concise names
- Adhere to all character and length restrictions
- Validate PSMs using the official API before service creation
