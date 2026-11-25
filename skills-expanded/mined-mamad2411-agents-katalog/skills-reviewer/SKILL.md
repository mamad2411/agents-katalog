## Skills Reviewer

Use this skill when you need to validate that a Skill follows the required format and setup conventions.

## Validation Checklist

### Required Frontmatter

Every user-created Skill must have YAML frontmatter at the top of SKILL.md with these fields:

-   `name`: The skill name (string, required)
    
-   `description`: When to load the skill (string, required, max 500 characters, non-empty)
    

Do not include `visibility` or `defaultEnabled` in user-created Skills.

### Frontmatter Format

Frontmatter must be valid YAML enclosed between `---` lines:

```
---
name: my-skill
description: Load this skill when ...
---
```

### Directory Structure

-   Skill directory must be at `skills/<slug>/` where `<slug>` matches the skill name in lowercase with hyphens
    
-   Directory must contain at least `SKILL.md`
    
-   Support files (Markdown, plain text, CSV, JSON, YAML) are optional and should only be added when they provide useful, durable information
    

### Content Requirements

-   `description` must be non-empty and at most 500 characters
    
-   `description` should clearly state when to load the Skill for routing purposes
    
-   SKILL.md body contains the instructions loaded after Skill selection
    
-   Keep Skills concise; put durable instructions in SKILL.md
    

## Review Process

1.  Check that the Skill directory exists at `skills/<name>/`
    
2.  Verify `SKILL.md` exists in the directory
    
3.  Validate the YAML frontmatter:
    
    -   Opens and closes with \`---\`
    -   Contains required \`name\` and \`description\` fields
    -   \`description\` is 1-500 characters
    -   No prohibited fields (\`visibility\`, \`defaultEnabled\`)
4.  Verify the skill name in frontmatter matches the directory name (case-insensitive)
    
5.  Check that support files are relevant and not excessive
    
6.  Ensure the Markdown body provides clear, actionable instructions
    

## Common Issues and Fixes

-   Missing frontmatter: Add YAML frontmatter with name and description
    
-   Missing description: Add a clear, routing-focused description
    
-   Description too long: Condense to 500 characters or less
    
-   Prohibited fields: Remove `visibility` and `defaultEnabled` from user-created Skills
    
-   Directory name mismatch: Rename directory to match the skill name in lowercase with hyphens
    
-   Empty SKILL.md body: Add instructions for when the Skill is loaded
    
-   Excessive support files: Remove unnecessary files; keep only those that provide durable value
    

## Validation Commands

To manually verify a Skill:

```
# Check directory exists
test -d skills/<name>/

# Check SKILL.md exists
test -f skills/<name>/SKILL.md

# Extract and validate frontmatter
grep -A 2 '^---$' skills/<name>/SKILL.md | head -n 4

# Count description length
sed -n '/^description: /s/description: //p' skills/<name>/SKILL.md | wc -c
```

## Final Output

When reviewing, report:

-   Validation status (pass/fail)
    
-   Specific issues found
    
-   Required fixes for each issue
    
-   Overall compliance score