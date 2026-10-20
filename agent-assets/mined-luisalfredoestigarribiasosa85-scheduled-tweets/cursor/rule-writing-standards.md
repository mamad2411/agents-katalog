---
description: Standards for writing and formatting Cursor rules
globs: "**/*.mdc"
---
# Rule Writing Standards

<rule>
name: rule_writing_standards
description: Detailed standards for writing and formatting Cursor rule content

filters:
  - type: file_extension
    pattern: "\\.mdc$"
  - type: content
    pattern: "(?s)<rule>.*?</rule>"

actions:
  - type: suggest
    message: |
      When writing a Cursor rule:

      1. Required Frontmatter Structure:
         ```markdown
          ---
          description: Clear, concise purpose of the rule
          globs: 
            - "pattern/to/match/**/*.rb"    # Primary file pattern
            - "other/pattern/**/*.erb"      # Additional patterns if needed
          ---

      2. Required Sections (in order):
         ```markdown
         # Title in Title Case

         <rule>
         name: rule_name_in_snake_case
         description: Detailed description of rule's purpose and scope

         filters:
           - type: file_extension|file_name|path|content|event
             pattern: "regex_pattern"
             # Add comments explaining complex patterns
         
         actions:
           - type: suggest|reject|require
             message: |
               Clear guidance with:
               
               1. Context or Purpose
               2. Code Examples
               3. Best Practices
               4. Common Pitfalls
               5. Related Documentation

         examples:
           - input: |
               # Bad example
               example_of_bad_code
               
               # Good example
               example_of_good_code
             output: "Explanation of why the good example is preferred"

         metadata:
           priority: high|medium|low
           version: 1.0
           related_rules:
             - other_relevant_rule
           responsibility: "What this rule enforces"
         </rule>
         ```

      3. Code Block Standards:
         - Use proper language identifiers
         - Include file paths for file-specific examples
         - Use descriptive comments
         - Show both good and bad examples
         - Include expected output

      4. Message Formatting:
         - Use numbered lists for steps
         - Use bullet points for related items
         - Include code examples in backticks
         - Use proper markdown formatting
         - Keep line length under 80 characters

      5. Metadata Requirements:
         - priority: Importance level
         - version: Rule version number
         - related_rules: Other relevant rules
         - responsibility: Rule's specific focus
         - standard_patterns: Common patterns to reference

examples:
  - input: |
      # Bad - Missing sections
      ---
      description: A rule
      ---
      <rule>
      name: incomplete_rule
      </rule>

      # Good - Complete structure
      ---
      description: Standards for API response formats
      globs: 
        - "app/controllers/api/**/*.rb"  # Primary file pattern
      ---
      # API Response Format Standards

      <rule>
      name: api_response_format
      description: Ensures consistent API response structure

      filters:
        - type: path
          pattern: "app/controllers/api/"

      actions:
        - type: suggest
          message: |
            When formatting API responses...

      examples:
        - input: |
            # Example code
        - output: "Explanation"

      metadata:
        priority: high
        version: 1.0
        related_rules:
          - api_standards
        responsibility: "API response formatting"
      </rule>
    output: "Complete rule structure with all required sections"

metadata:
  priority: high
  version: 1.0
  related_rules:
    - cursor_rules_location
  responsibility: "Rule content structure and formatting"
  standard_patterns:
    frontmatter:
      description: "Clear, concise description"
      globs: "Array of file patterns"
    sections:
      - title
      - rule_block
      - filters
      - actions
      - examples
      - metadata
</rule>