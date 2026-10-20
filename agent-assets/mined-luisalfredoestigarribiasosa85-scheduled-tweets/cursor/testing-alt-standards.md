---
description: Enforces best practices for writing tests using RSpec or Minitest, with emphasis on using the factory pattern.
globs:
  - "spec/**/*.rb"
  - "test/**/*.rb"
---

# Testing

<rule>
name: testing_standard
description: Provides guidelines for writing maintainable tests that adhere to Rails conventions, including proper usage of the factory pattern for test data.

filters:
  - type: path
    pattern: "^(spec|test)/.*\\.rb$"
    # Applies to test files in spec or test directories

actions:
  - type: suggest
    message: |
      Test files should:
      1. Follow a clear structure for unit, integration, and system tests.
      2. Use factories or fixtures appropriately for test data.
      3. Be concise and focused on a single behavior or unit of logic.
      4. Include descriptive test names and comments.
      5. Avoid duplicating setup code; leverage shared contexts or helpers.

examples:
  - input: |
      # Bad example: Overly complex test setup with repeated code.
      describe User do
        it "creates a user" do
          user = User.new(name: "Test User")
          expect(user.save).to be_truthy
        end
      end
    output: "Consider using a factory to generate test data and shared setup for similar tests."
  - input: |
      # Good example using FactoryBot.
      describe User, type: :model do
        let(:user) { create(:user) }
        it "saves a valid user" do
          expect(user).to be_valid
        end
      end
    output: "Test follows Rails conventions with clear structure and uses a factory for test data."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize testing practices and promote maintainable test code"
</rule>
