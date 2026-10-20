---
description: "Fixture standards and best practices for test data"
globs: ['test/fixtures/**/*.{yml,yaml}']
alwaysApply: false
---
---
description: "Fixture standards and best practices for test data in Rails applications"
globs: 
  - 'test/fixtures/**/*.{yml,yaml}'
  - 'test/**/*_test.rb'
  - 'spec/**/*_spec.rb'
---

# Fixture Standards and Best Practices

<rule>
name: fixture_standards
description: >
  This rule ensures that all test fixtures are stored exclusively within the
  test/fixtures folder and strictly match the current database schema. Fixtures 
  must be maintained according to changes reflected in the db/schema.rb file, with
  particular attention to column names and types. All tests must rely on these 
  fixtures to guarantee data consistency and reproducibility across test environments.
  
filters:
  - type: path
    pattern: "^test/fixtures(/.*)?\\.(yml|yaml)$"
  - type: content
    pattern: "fixtures|fixture_file_upload|file_fixture"

actions:
  - type: error
    message: |
      Fixture files must be located under the 'test/fixtures' directory only and
      must exactly match the current database schema. Common errors include:
      - Using column names that don't exist in the schema
      - Missing required columns (null: false)
      - Incorrect data types for columns
      
  - type: suggest
    message: |
      # Fixture Best Practices
      
      1. **Directory Structure and Naming**:
         - Store all fixtures in `test/fixtures/` directory
         - Name fixture files to EXACTLY match the corresponding database table name in schema.rb
         - For tables with prefixes (e.g., `safety_report_*`), include the FULL prefix in the file name
         - Use nested folders ONLY when the model itself has a namespaced structure
         - Always verify fixture names match table names with `grep -r "create_table" db/schema.rb`
      
      2. **Schema Synchronization**:
         - After each schema change (`db/schema.rb`), update affected fixtures immediately
         - Include ALL required attributes (those with `null: false` in schema)
         - Set appropriate data for foreign key relationships
         - Match data types in fixtures to those in schema (strings, integers, booleans, etc.)
         - Use ERB for dynamic values: `<%= Time.current.iso8601 %>`
         - IMPORTANT: Verify all column names exist in schema before using them
      
      3. **Schema Validation Steps**:
         - Before adding a column to a fixture:
           1. Check schema.rb: `grep -A 20 "create_table \\"table_name\\"" db/schema.rb`
           2. Verify the column exists and note its type
           3. Ensure the value matches the column type
         - After schema migrations:
           1. Run `bin/rails db:schema:load RAILS_ENV=test`
           2. Run `bin/rails test:prepare` to verify fixtures
           3. Fix any fixture load errors before proceeding
      
      4. **Common Fixture Errors and Solutions**:
         ```ruby
         # Error: table "X" has no column named "Y"
         # Solution: Check schema.rb for actual column names
         
         # Error: Validation failed: X can't be blank
         # Solution: Add missing required field to fixture
         
         # Error: wrong type for column "X"
         # Solution: Match schema.rb data type
         ```
      
      5. **Polymorphic Associations**:
         - For polymorphic relationships, use the proper class name format in `*_type` fields
         - Ensure `*_type` and `*_id` fields correctly pair together
         - Example for polymorphic witness association:
           ```yaml
           # safety_report_witnesses.yml
           witness_one:
             witnessable_type: "SafetyReportAutoIncident"
             witnessable_id: 1
             name: "John Doe"
           ```
      
      6. **Organization and References**:
         - Use meaningful names for fixture records (e.g., `admin_user` not `one`)
         - Group related fixtures together with comments
         - Use explicit IDs to ensure stable associations between related fixtures
         - Reference associations directly by ID or with ActiveRecord helpers:
           ```yaml
           # Using explicit IDs
           post_comment:
             post_id: 1
             author_id: 2
             
           # Using ActiveRecord helpers
           post_comment:
             post_id: <%= ActiveRecord::FixtureSet.identify(:featured_post) %>
             author_id: <%= ActiveRecord::FixtureSet.identify(:admin_user) %>
           ```
      
      7. **Data Type Consistency**:
         - Strings: Use quotes for clarity `"Example string"`
         - Booleans: Use true/false (not strings)
         - Integers: Use unquoted numbers
         - Null values: Use null or ~ (not empty strings)
         - Enums: Use the string/symbol representation, not the integer value
         - Dates/Times: Use ISO format or ERB helpers
      
      8. **Fixture Validation Process**:
         - Periodically validate fixtures against schema with these steps:
           1. Check table existence: `grep -r "create_table" db/schema.rb`
           2. Verify fixture matches table: Compare file name with table name
           3. Validate required fields: Check all `null: false` fields are present
           4. Test fixture loading: `bin/rails test:prepare` should run without errors
         - Run a smoke test loading fixtures: `bin/rails runner 'puts ModelName.first.inspect'`
         - When tests fail with fixture errors:
           1. Check the exact error message (e.g., missing column)
           2. Verify schema.rb for the correct structure
           3. Update fixtures to match current schema
           4. Run tests again to verify fix
      
      9. **Usage in Tests**:
         - Reference fixtures using the `fixtures :users, :posts` syntax
         - Access fixture data via `users(:admin)` or `posts(:published)`
         - Avoid creating test data outside of fixtures where possible
         - Use transactional fixtures to maintain test isolation

examples:
  - input: |
      # INCORRECT: Using non-existent column
      test/fixtures/property_service_reports.yml
      ---
      report_one:
        service_type: "maintenance"  # Error: column doesn't exist!
        
      # CORRECT: Using actual schema columns
      test/fixtures/property_service_reports.yml
      ---
      report_one:
        property_id: 1
        completed_at: <%= Time.current.iso8601 %>
        
      # INCORRECT: Wrong fixture name (doesn't match table name)
      test/fixtures/other_driver_details.yml
      ---
      driver_one:
        safety_report_auto_incident_id: 1
        name: "John Smith"
        
      # CORRECT: Fixture name matches table name exactly
      test/fixtures/safety_report_other_driver_details.yml
      ---
      driver_one:
        safety_report_auto_incident_id: 1
        name: "John Smith"
        license_number: "S12345678"
        
      # CORRECT: Proper polymorphic relationship
      test/fixtures/safety_report_witnesses.yml
      ---
      auto_incident_witness:
        witnessable_type: "SafetyReportAutoIncident"
        witnessable_id: 1
        name: "Jane Doe"
        phone: "202-555-1234"
    output: |
      Fixture files must exactly match the current database schema structure.
      Always verify column names and types in schema.rb before creating or updating fixtures.

metadata:
  priority: high
  version: 1.3
  responsibility: "Ensure fixtures are organized according to the schema and used consistently by all tests."
  related_rules:
    - testing_standards
    - models_standards
    - database_standards
  standard_patterns:
    - folder_structure: "Place fixtures in test/fixtures/ with appropriate nesting"
    - schema_reference: "Maintain fixture attributes according to db/schema.rb"
    - fixture_usage: "Reference fixtures in tests using the fixtures method"
    - naming_convention: "Name fixture files to EXACTLY match table names in schema.rb"
    - data_consistency: "Match data types in fixtures to those in schema"
    - required_fields: "Include all fields marked as null: false in schema"
    - polymorphic_associations: "Use proper *_type/*_id pairs for polymorphic relationships"
    - schema_validation: "Verify all columns exist before using them in fixtures"
  tools:
    - minitest
    - rspec
    - fixture_loader
    - active_record
    - schema_validation: "grep -r 'create_table' db/schema.rb"
</rule>