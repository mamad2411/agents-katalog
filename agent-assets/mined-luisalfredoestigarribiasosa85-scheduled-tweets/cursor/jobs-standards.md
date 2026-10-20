---
description: Enforces comprehensive standards for writing, managing, and monitoring background jobs in a Rails project, ensuring reliability, maintainability, and performance.
globs:
  - "app/jobs/**/*.rb"
---

# Jobs

<rule>
name: jobs_standard
description: Ensures that background job classes (using ActiveJob) adhere to naming conventions, proper error handling, scheduling best practices, and implementation standards for reliable asynchronous processing.

Key Requirements:
- Must be safely idempotent (can be run multiple times without side effects)
- Must include comprehensive error handling and retries
- Must be monitored and observable
- Must handle job arguments safely
- Must follow consistent naming conventions
- Must include proper documentation
- Must be testable and include tests

filters:
  - type: path
    pattern: "^app/jobs/.*\\.rb$"
    # Applies to all Ruby files in the app/jobs directory

actions:
  - type: suggest
    message: |
      Background job classes must follow these guidelines:

      1. Class Structure and Naming:
         - Inherit from ApplicationJob
         - Use descriptive names ending in 'Job' (e.g., UserOnboardingJob)
         - Follow single responsibility principle
         - Keep methods small and focused

      2. Arguments and Data Handling:
         - Pass IDs instead of entire objects
         - Serialize arguments appropriately
         - Validate arguments in perform method
         - Handle missing or invalid data gracefully

      3. Error Handling and Retries:
         - Implement retry strategies for transient failures
         - Use appropriate rescue blocks
         - Log errors with context
         - Set max_attempts based on business requirements
         - Consider using retry_on for specific exceptions

      4. Queue Configuration:
         - Set appropriate queue name
         - Configure priority if needed
         - Set proper timeouts
         - Consider rate limiting for external services

      5. Monitoring and Observability:
         - Include instrumentation
         - Add appropriate logging
         - Track job metrics (success, failure, duration)
         - Set up alerts for critical jobs

      6. Testing:
         - Include unit tests
         - Test retry behavior
         - Test error conditions
         - Use appropriate test helpers

      7. Documentation:
         - Document purpose and responsibilities
         - List all arguments and their types
         - Document retry strategy
         - Include usage examples
         - Document queue configuration

examples:
  - input: |
      # Bad example: Poor implementation with multiple issues
      class SendEmails
        def perform
          User.all.each do |user|
            UserMailer.welcome(user).deliver_now
          end
        end
      end
    output: "Multiple issues: Missing inheritance, no error handling, potential performance problems with User.all, using deliver_now in a job"

  - input: |
      # Bad example: Poor error handling and argument passing
      class ProcessUserJob < ApplicationJob
        def perform(user)
          user.process_data
        rescue => e
          retry
        end
      end
    output: "Issues: Passing full object instead of ID, overly broad rescue, infinite retries"

  - input: |
      # Good example: Well-structured job with proper practices
      class UserOnboardingJob < ApplicationJob
        queue_as :default
        retry_on NetworkError, wait: :exponentially_longer, attempts: 3
        discard_on InvalidUserError

        def perform(user_id)
          # Validate arguments
          raise ArgumentError, "user_id is required" if user_id.blank?

          # Load and validate data
          user = User.find(user_id)
          raise InvalidUserError unless user.can_onboard?

          # Instrument the job
          ActiveSupport::Notifications.instrument("user.onboarding", user_id: user_id) do
            # Main processing with detailed logging
            Rails.logger.info("Starting onboarding for user #{user_id}")
            
            process_user_onboarding(user)
            
            Rails.logger.info("Completed onboarding for user #{user_id}")
          end

        rescue ActiveRecord::RecordNotFound => e
          Rails.logger.error("Failed to find user #{user_id}: #{e.message}")
          raise
        rescue StandardError => e
          Rails.logger.error("Onboarding failed for user #{user_id}: #{e.message}")
          raise
        end

        private

        def process_user_onboarding(user)
          # Implementation details...
        end
      end
    output: "Excellent implementation with proper inheritance, error handling, logging, instrumentation, and organization"

  - input: |
      # Good example: Job with rate limiting and monitoring
      class ExternalApiJob < ApplicationJob
        queue_as :external_apis
        retry_on ApiRateLimitError, wait: 30.seconds, attempts: 3

        def perform(api_request_id)
          with_rate_limiting do
            process_api_request(api_request_id)
          end
        end

        private

        def with_rate_limiting
          RedisRateLimiter.with_limit(
            key: "external_api_calls",
            limit: 100,
            period: 1.minute
          ) { yield }
        end

        def process_api_request(request_id)
          # Implementation with proper monitoring
          ActiveSupport::Notifications.instrument("external_api.request",
            request_id: request_id) do
            # Implementation details...
          end
        end
      end
    output: "Well-implemented job with rate limiting, monitoring, and proper error handling"

metadata:
  priority: high
  version: 1.1
  related_rules:
    - rails_project
    - monitoring_standards
    - error_handling_standards
  responsibility: "Standardize and optimize background job implementations"
  categories:
    - Performance
    - Reliability
    - Maintainability
    - Observability
</rule>