---
description: Standards for writing commit messages based on staged files
globs: ".git/COMMIT_EDITMSG", "**/.git/COMMIT_EDITMSG"
---
# Commit Message Standards

<rule>
name: commit_message_standards
description: |
  Standards for writing clear, descriptive commit messages following conventional commits.
  Messages should be based on the types of files staged and changes made.

filters:
  - type: file_extension
    pattern: "COMMIT_EDITMSG$"
  - type: content
    pattern: "^\s*(feat|fix|docs|style|refactor|test|chore|build|ci|perf).*:"

actions:
  - type: suggest
    message: |
      When writing commit messages:

      1. Commit Message Structure:
         ```git
         type(scope): subject line

         [optional body]

         [optional footer]
         ```

      2. Type Categories:
         - feat: New feature or significant enhancement
         - fix: Bug fix
         - docs: Documentation changes
         - style: Code style/formatting changes
         - refactor: Code refactoring
         - test: Adding/modifying tests
         - chore: Maintenance tasks
         - build: Build system changes
         - ci: CI configuration changes
         - perf: Performance improvements

      3. Scope Guidelines (based on staged files):
         ```git
         # For model changes (app/models/*)
         feat(user): add email verification

         # For controller changes (app/controllers/*)
         fix(auth): handle invalid token error

         # For view changes (app/views/*)
         style(ui): update button styling

         # For multiple areas
         refactor(auth,user): simplify login flow
         ```

      4. Subject Line Rules:
         - Use imperative mood ("add" not "added")
         - Max 50 characters
         - No period at end
         - Start with lowercase
         - Be specific and descriptive

      5. Body Guidelines:
         - Separate from subject with blank line
         - Wrap at 72 characters
         - Explain what and why, not how
         - Use bullet points for multiple items

      6. Footer Guidelines:
         - Reference issues: "Fixes #123"
         - Breaking changes: "BREAKING CHANGE:"
         - Co-authors: "Co-authored-by: name <email>"

examples:
  - input: |
      # Bad commit messages
      fixed stuff
      updated code
      WIP

      # Good commit messages
      feat(user): add email verification system
      
      Implement email verification flow using noticed gem.
      - Add EmailVerificationMailer
      - Add verification token to users
      - Add verification endpoints
      
      Fixes #123
    output: "Clear, descriptive commit message following conventions"

metadata:
  priority: high
  version: 1.0
  related_rules:
    - branch_naming_standards
    - pull_request_standards
  responsibility: "Commit message formatting and clarity"
  standard_patterns:
    types:
      - feat
      - fix
      - docs
      - style
      - refactor
      - test
      - chore
      - build
      - ci
      - perf
    scopes:
      models: "user|post|comment"
      controllers: "auth|api|admin"
      views: "ui|layout|components"
    footers:
      - "Fixes #"
      - "Refs #"
      - "BREAKING CHANGE:"
      - "Co-authored-by:"
</rule>