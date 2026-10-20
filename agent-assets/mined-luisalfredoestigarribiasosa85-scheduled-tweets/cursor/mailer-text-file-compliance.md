---
description: 
globs: 
---
---
description: Enforce Text Mailer File Standards 
globs:
  - "app/notifications/**/*.rb"
  - "app/mailers/**/*.rb"
  - "app/views/**/*_mailer/**/*"
---
# Text Mailer File Standards

This rule ensures that plain text mailer templates follow consistent formatting and structure.

<rule>
name: mailer_text_file_compliance
description: Ensure text mailer views maintain content parity with HTML versions while following plain text formatting standards
filters:
  # Match any text mailer view files
  - type: file_name
    pattern: ".*\\.text\\.erb$"
  
  # Check for proper text formatting patterns
  - type: content_structure
    pattern: |
      (?!.*<[^>]+>)                    # No HTML tags allowed
      (?!.*\n{3,})                     # No excessive blank lines
      (?=.*strip_tags.*)                      # Enforces strip_tags only if used
      (?<!^\s*<%= strip_tags.*\.html.*\s*$)   # Avoid overly strict enforcement of .html translations

actions:
  - type: suggest
    message: |
      Please update your text mailer view to follow our standard structure:

      ```erb
      <%= strip_tags t(
        ".header_html",
        inviter: @invited_by&.name || "Unknown",
        account: @account&.name || "Your account"
      ) %>

      <%= strip_tags t(
        ".description_html",
        link: t(".accept_or_decline", default: "Visit our platform")
      ) %>

      <%= t(".view_invitation") %>: <%= account_invitation_url(@account_invitation || "#") %>

      ---
      <%= t(".footer") %>
      <%= Jumpstart.config.business_name %>
      <%= Jumpstart.config.business_address || "123 Default Street" %>
      ```

      Key guidelines:
      1. Use `strip_tags` for any HTML translations
      2. Separate sections with a single blank line
      3. Use clear section breaks (---, ===, etc.) when needed
      4. Include URLs on their own line
      5. Keep lines under 80 characters for better readability
      6. Include a consistent footer section
      7. Avoid special characters that might not render well in plain text

      IMPORTANT: This text template must maintain content parity with its HTML counterpart:
      <%= file_path.sub('.text.erb', '.html.erb') %>

      Elements to keep in sync:
      - All translation keys and their parameters
      - URLs and links
      - Dynamic content (<%= %> blocks)
      - Business logic (if/else conditions)

      Note: Format and structure can differ to suit plain text, but content must match.

    severity: warning

  - type: require
    message: |
      Missing corresponding HTML template. Please create an .html.erb version at:
      <%= file_path.sub('.text.erb', '.html.erb') %>
    condition: |
      File.exist?(Rails.root.join('app', 'views', file_path.sub('.text.erb', '.html.erb')))

examples:
  # Account Invitation Example
  - input: |
      Welcome to our platform!
      Click here to join: http://example.com
    output: |
      <%= strip_tags t(".header_html", inviter: @invited_by.name, account: @account.name) %>

      <%= strip_tags t(".description_html", link: t(".accept_or_decline")) %>

      <%= t(".view_invitation") %>: <%= account_invitation_url(@account_invitation) %>

      ---
      <%= t(".footer") %>
      <%= Jumpstart.config.business_name %>

  # Password Reset Example
  - input: |
      Reset your password
      Click the link below
      http://example.com/reset
    output: |
      <%= strip_tags t(".greeting", recipient: @resource.email) %>

      <%= strip_tags t(".instruction") %>

      <%= edit_password_url(@resource, reset_password_token: @token) %>

      ---
      <%= t(".footer_note") %>
      <%= t(".ignore_text") if @resource.unconfirmed_email %>

metadata:
  priority: high
  version: 1.0
  standard_sections:
    - header
    - main_content
    - call_to_action
    - action_url
    - footer
  line_length: 80
  spacing:
    section_break: "\n\n"
    footer_break: "\n---\n"
  related_rules:
    - mailer_html_file_compliance
  responsibility: "Plain text formatting and structure"
  content_parity: true
</rule> 