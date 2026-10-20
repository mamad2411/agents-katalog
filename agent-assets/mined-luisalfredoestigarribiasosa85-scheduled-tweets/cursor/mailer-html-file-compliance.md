---
description: Enforce HTML Mailer File Standards
globs: 
---
# Enforce Mailer File Standards

This rule ensures that all mailer view templates follow consistent styling and structure.

<rule>
name: mailer_html_file_compliance
description: Ensure HTML mailer views adhere to consistent styling and structure standards, with awareness of text counterparts
filters:
  # Match mailer view files
  - type: file_name
    pattern: ".*\\.html\\.erb$"
  
  # Ensure proper table-based structure and valid inline styles
  - type: content_structure
    pattern: |
      style="(?!(color|font-size|font-weight|text-align|line-height|margin|padding|background-color):)"                                        # Catch inline styles

actions:
  - type: suggest
    message: |
      Please update your mailer view to follow our standard structure:

      ```html
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td>
            <!-- For headings -->
            <h1 style="color: #1F2937; font-size: 24px; font-weight: 500; margin-bottom: 16px; text-align: center;">
              <%= t(".your_heading") %>
            </h1>

            <!-- For paragraphs -->
            <p style="color: #4B5563; font-size: 16px; line-height: 24px; margin-bottom: 16px;">
              <%= t(".your_content") %>
            </p>

            <!-- For buttons/links -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 24px 0;">
              <tr>
                <td align="center">
                  <%= link_to t(".button_text"), 
                      your_path,
                      style: "background-color: #38b2ac; border-radius: 4px; color: #ffffff; display: inline-block; font-size: 16px; font-weight: 500; padding: 12px 24px; text-decoration: none;" %>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
      ```

      Key guidelines:
      1. Use tables instead of `<div>` tags for layout.
      2. Center content using:
         - Table cell alignment (`<td align="center">`)
         - Inline styles on headings or specific elements (e.g., `<h1 style="text-align: center;">`).
      3. Avoid centering using `<div style="text-align: center;">`.
      4. Include all styles inline with our standard values.
      5. Use consistent colors, spacing, and typography.
      6. Use proper heading hierarchy and spacing between elements.

      IMPORTANT: When updating content in this HTML template, you MUST also update the 
      corresponding .text.erb version with the same content:
      <%= file_path.sub('.html.erb', '.text.erb') %>

      Content changes to update in both files:
      - Translations and their parameters
      - URLs and links
      - Dynamic content (<%= %> blocks)
      - Business logic (if/else conditions)

      Note: Styling remains HTML-specific and should not affect the text version.

    severity: warning

  - type: require
    message: |
      Missing corresponding text template. Please create a .text.erb version at:
      <%= file_path.sub('.html.erb', '.text.erb') %>
    condition: |
      text_path = Rails.root.join('app/views', file_path.sub('.html.erb', '.text.erb'))
      text_path.to_s.start_with?(Rails.root.join('app/views').to_s) && File.exist?(text_path)

examples:
  # Account Invitation Example with both HTML and Text versions
  - input: |
      # HTML Version (invite.html.erb)
      <div style="text-align: center;">
        <h1>Welcome <%= @user.name %></h1>
        <%= link_to "Accept", url %>
      </div>

      # Text Version (invite.text.erb)
      Welcome <%= @user.name %>

      To accept, visit: <%= url %>
    output: |
      # HTML Version (invite.html.erb)
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td align="center">
            <h1 style="color: #1F2937; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
              Welcome <%= @user.name %>
            </h1>
            <table border="0" cellpadding="0" cellspacing="0">
              <tr>
                <td align="center">
                  <%= link_to "Accept",
                      url,
                      style: "background-color: #38b2ac; border-radius: 4px; color: #ffffff; display: inline-block; font-size: 16px; font-weight: 500; padding: 12px 24px; text-decoration: none;" %>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

  # Notification Example
  - input: |
      <h1>New Report</h1>
      <p><strong>Branch:</strong> <%= @branch %></p>
    output: |
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td>
            <h1 style="color: #1F2937; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
              New Report
            </h1>
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td style="color: #4B5563; font-size: 16px; line-height: 24px;">
                  <strong style="color: #1F2937;">Branch:</strong> <%= @branch %>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

metadata:
  priority: high
  version: 1.0
  standard_styles:
    colors:
      primary: "#38b2ac"
      text: "#1F2937"
      text_secondary: "#4B5563"
    typography:
      heading: "color: #1F2937; font-size: 24px; font-weight: 500; margin-bottom: 16px;"
      body: "color: #4B5563; font-size: 16px; line-height: 24px;"
      button: "background-color: #38b2ac; border-radius: 4px; color: #ffffff; display: inline-block; font-size: 16px; font-weight: 500; padding: 12px 24px; text-decoration: none;"
  text_template:
    required: true
    naming_convention: "Replace .html.erb with .text.erb"
    content_parity: true
  related_rules: 
    - mailer_text_file_compliance
  responsibility: "HTML structure and styling"
</rule> 