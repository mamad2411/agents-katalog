---
description: Standards for implementing Aspire models and API integrations
globs: 
---
 ---
description: Standards for implementing Aspire models and API integrations
globs: 
  - "app/models/aspire_*.rb"
  - "app/services/aspire/*.rb"
  - "app/jobs/sync_aspire_*.rb"
---
# Aspire Model Implementation Standards

<rule>
name: aspire_model_standards
description: |
  Standards for implementing Aspire models and API integrations.
  Enforces consistent patterns for model inheritance, naming conventions,
  and synchronization with the Aspire API. For more details, refer to the official documentation:
  [Aspire API Documentation](mdc:https:/api.aspire.example.com/docs).

filters:
  - type: file_name
    pattern: "aspire_.*\\.rb$"
  - type: content
    pattern: "class Aspire|< AspireRecord"

actions:
  - type: suggest
    message: |
      When implementing Aspire models:

      1. Model Naming & Inheritance:
         ```ruby:app/models/aspire_property.rb
         class AspireProperty < AspireRecord
           self.primary_key = :property_id  # Required based on unique_id_mapping
           
           def self.unique_id_mapping
             { property_id: "id" }  # Maps model attribute to API field
           end

           def self.default_attribute_mappings
             {
               name: "name",
               status: "status"
               # Add other field mappings
             }
           end
         end
         ```

      2. Required Model Methods:
         - `unique_id_mapping`: Maps model primary key to API field
         - `default_attribute_mappings`: Maps model attributes to API fields
         - Set `self.primary_key` explicitly based on unique_id_mapping

      3. Table Naming Convention:
         - Prefix all tables with `aspire_`
         - Use plural form: `aspire_properties`
         - Include all required unique ID columns

      4. Sync Patterns:
         ```ruby:app/models/aspire_record.rb
         # Use create_or_update_by for record sync
         record = AspireProperty.create_or_update_by(
           api_data,
           attribute_mappings: custom_mappings # Optional
         )
         ```

      5. Scope Usage:
         ```ruby
         scope :active, -> { where(active: true) }
         scope :inactive, -> { where(active: false) }
         scope :syncable, -> { all } # Override if needed
         ```

      6. Error Handling:
         - Use proper error classes
         - Implement validation
         - Log sync failures
         - Handle API errors gracefully

examples:
  - input: |
      # Bad - Missing required methods
      class AspireProperty < AspireRecord
        # No unique_id_mapping or default_attribute_mappings
      end

      # Good - Complete implementation
      class AspireProperty < AspireRecord
        self.primary_key = :property_id

        def self.unique_id_mapping
          { property_id: "id" }
        end

        def self.default_attribute_mappings
          {
            name: "name",
            status: "status"
          }
        end
      end
    output: "Properly structured Aspire model with required methods"

metadata:
  priority: high
  version: 1.0
  related_rules:
    - api_standards
    - model_standards
  responsibility: "Aspire model implementation patterns"
  standard_patterns:
    naming:
      models: "Aspire{ResourceName}"
      tables: "aspire_{resource_name}s"
    inheritance:
      base_class: "AspireRecord"
    required_methods:
      - unique_id_mapping
      - default_attribute_mappings
    scopes:
      - active
      - inactive
      - syncable
</rule>