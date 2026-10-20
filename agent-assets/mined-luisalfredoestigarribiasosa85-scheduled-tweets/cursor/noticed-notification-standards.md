---
description: Implementation standards for Noticed notifications with required email delivery setup, following official Noticed gem patterns
globs: 
alwaysApply: false
---
# Noticed Notification Implementation Standards

<rule>
name: noticed_notification_standards
description: |
  Standards for implementing notifications using the Noticed gem (v2+).
  Enforces consistent patterns for database and email delivery methods.

  Key Requirements:
  - Notifier class inherits from Noticed::Base
  - Email delivery configuration
  - Recipients defined within notifier
  - Required parameters specified
  - I18n integration for all text
  - Error handling with Honeybadger
  - Comprehensive test coverage

  Official Documentation:
  - [Noticed Gem Documentation](mdc:https:/github.com/excid3/noticed)
  - [Upgrade Guide](mdc:https:/github.com/excid3/noticed/blob/main/UPGRADE.md)
  - [Rails Integration Guide](mdc:https:/github.com/excid3/noticed/wiki/Rails-Integration)

filters:
  - type: file_extension
    pattern: "\\.rb$"
  - type: content
    pattern: "class.*?<.*?Noticed::Base"
  - type: path
    pattern: "(app/notifiers/|app/mailers/|app/views/.*_mailer/).*"

actions:
  - type: suggest
    message: |
      When implementing notifications:

      1. Required Notifier Structure:
         ```ruby:app/notifiers/your_notifier.rb
         class YourNotifier < Noticed::Base
           deliver_by :email,
                     mailer: "YourMailer",
                     method: :notification_method,
                     if: :email_notifications?

           required_params :record  # The record triggering the notification

           # Define recipients within the notifier
           def recipients
             # Return an array of recipients who should receive this notification
             record.relevant_recipients.select { |recipient| recipient.email.present? }
           end
           
           def email_notifications?
             Rails.application.config.x.enable_email_delivery
           end

           def message
             t(".message", record_type: record.class.model_name.human)
           end
         end
         ```

      2. Required Mailer Structure:
         ```ruby:app/mailers/your_mailer.rb
         class YourMailer < ApplicationMailer
           def notification_method
             @record = params[:record]
             
             mail(
               to: recipient.email,
               subject: t(".subject", record: @record.name)
             )
           end
         end
         ```

      3. Calling the Notifier:
         ```ruby
         # The notifier handles recipient determination internally
         YourNotifier.with(record: @record).deliver_later
         ```

      4. Required Locale Structure:
         ```yaml:config/locales/notifications.en.yml
         en:
           notifiers:
             your_notifier:
               message: "A new %{record_type} has been created"
           mailers:
             your_mailer:
               notification_method:
                 subject: "New notification for %{record}"
         ```

      5. Implementation Checklist:
         - [ ] Create Notifier class with email delivery configuration
         - [ ] Define recipients method in the notifier
         - [ ] Specify required parameters
         - [ ] Implement email_notifications? method
         - [ ] Create mailer and views
         - [ ] Add all required translations
         - [ ] Add error handling with Honeybadger
         - [ ] Add tests for notification logic

      6. Testing Structure:
         ```ruby:spec/notifiers/your_notifier_spec.rb
         RSpec.describe YourNotifier, type: :notifier do
           let(:record) { create(:your_model) }
           let(:notification) { described_class.with(record: record) }

           describe "#recipients" do
             it "returns recipients with email addresses" do
               recipients = notification.recipients
               expect(recipients).to all(have_attributes(email: be_present))
             end
           end

           describe "email delivery" do
             context "when email notifications enabled" do
               before { allow(Rails.application.config.x).to receive(:enable_email_delivery).and_return(true) }

               it "delivers email to all recipients" do
                 expect { notification.deliver_later }
                   .to have_enqueued_job.on_queue("default")
               end
             end
           end
         end
         ```

      7. Error Handling:
         ```ruby
         class YourNotifier < Noticed::Base
           deliver_by :email do |config|
             config.error_handler = ->(error, recipient) {
               Honeybadger.notify(error, context: {
                 notification_type: self.class.name,
                 recipient: recipient.id,
                 record: record.id
               })
             }
           end
         end
         ```

examples:
  - input: |
      # Bad - Recipients passed from outside
      class BadNotifier < Noticed::Base
        deliver_by :email
      end

      # Good - Recipients determined internally
      class GoodNotifier < Noticed::Base
        deliver_by :email
        required_params :record
        
        def recipients
          record.contacts.with_email
        end
      end
    output: "Complete notification implementation with recipients handled internally"

metadata:
  priority: high
  version: 2.0
  related_rules:
    - mailer_html_file_compliance
    - mailer_text_file_compliance
    - i18n_standards
    - testing_standards
  responsibility: "Notification system implementation standards"
  standard_patterns:
    notification:
      - database_delivery
      - email_delivery
      - parameters
      - email_methods
    mailer:
      - notification_email
      - view_templates
    testing:
      - notification_specs
      - delivery_specs
      - error_handling
    locales:
      - translations
      - interpolation
</rule> 