---
description:
globs:
alwaysApply: false
---
# Git Commit Message Rules for Kiwoom REST API

## Commit Message Format

### Required Format
```
[Type] short description [file {number of staged files} - lines {number of staged lines}]
- detailed description line 1
- detailed description line 2
- detailed description line 3
- detailed description line 4
- detailed description line 5
```

### Commit Types
- **Feat**: Implement new feature
- **Add**: Add asset files
- **Fix**: Fix bugs
- **Docs**: Add or update documentation
- **Style**: Styling work (no code logic changes)
- **Refactor**: Code refactoring (no functional changes)
- **Test**: Add or modify tests
- **Deploy**: Deployment-related changes
- **Conf**: Build or environment configuration
- **Chore**: Miscellaneous tasks

### Rules
1. **First Line**: Must start with a tag and short description (under 30 characters)
2. **File/Line Count**: Include at the end of first line: `[file {count} - lines {count}]`
3. **Detailed Descriptions**: Up to 5 lines starting with hyphen `-`
4. **Character Limits**: First line under 30 characters, detailed descriptions under 50 characters each

### Examples

#### Feature Implementation
```
[Feat] add account API methods [file 1 - lines 45]
- add filled_position_request_kt00005 method
- add account_order_execution_detail_request_kt00007 method
- add next_day_settlement_schedule_request_kt00008 method
- add account_order_execution_status_request_kt00009 method
- add withdrawable_order_amount_request_kt00010 method
```

#### Bug Fix
```
[Fix] resolve API parameter validation [file 1 - lines 12]
- fix stock_code parameter validation
- add proper error handling for invalid codes
- update docstring with parameter constraints
```

#### Documentation Update
```
[Docs] update API documentation [file 2 - lines 8]
- add comprehensive method descriptions
- include Korean field descriptions
- update usage examples
```

#### Test Addition
```
[Test] add test cases for new APIs [file 1 - lines 15]
- add test for kt00005 API method
- add test for kt00007 API method
- add test for kt00008 API method
```

#### Refactoring
```
[Refactor] improve code structure [file 1 - lines 25]
- extract common parameter validation
- standardize method signatures
- improve error handling consistency
```

### Staging Information
- Count only staged files and lines
- Use `git status` and `git diff --cached --stat` to get accurate counts
- Include all modified files in the count

### Best Practices
1. Use descriptive but concise commit messages
2. Include relevant API IDs in descriptions when applicable
3. Group related changes in single commits
4. Test changes before committing
5. Follow the established pattern consistently
