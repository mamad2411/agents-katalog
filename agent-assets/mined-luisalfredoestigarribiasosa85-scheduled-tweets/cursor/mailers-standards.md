---
description: Enforces standards for creating and managing Action Mailers and associated email templates in a Rails project.
globs:
  - "app/mailers/**/*.rb"
  - "app/views/mailer/**/*.erb"
---

# Mailers

<rule>
name: mailers_standard
description: Ensures that Action Mailers and their email templates adhere to Rails conventions, including proper layout usage, naming conventions, and error handling.

filters:
  - type: path
    pattern: "^app/mailers/.*\\.rb$"
    # Applies to all mailer Ruby files

actions:
  - type: suggest
    message: |
      Mailers should:
      1. Inherit from ApplicationMailer.
      2. Use descriptive names that reflect the purpose of the email.
      3. Include proper layout usage and localization where needed.
      4. Handle errors gracefully, especially when sending emails.
      5. Keep email templates simple and maintainable.

examples:
  - input: |
      # Bad example: Mailer not inheriting from ApplicationMailer and missing error handling.
      class NotificationMailer
        def welcome_email(user)
          # code to send email
        end
      end
    output: "Mailers should inherit from ApplicationMailer and handle errors appropriately."
  - input: |
      # Good example
      class NotificationMailer < ApplicationMailer
        def welcome_email(user)
          @user = user
          mail(to: @user.email, subject: 'Welcome!')
        end
      end
    output: "Mailer follows Rails conventions with proper inheritance, naming, and usage."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standards
    - noticed_notification_standards
    - mailer_html_file_compliance
    - mailer_text_file_compliance
  responsibility: "Standardize the implementation of Action Mailers and email templates"
</rule>
