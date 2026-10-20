---
description: Enforces best practices for database interactions using ActiveRecord with clear guidelines for raw SQL usage.
globs:
  - "app/models/**/*.rb"
  - "db/**/*.sql"
---

# Database Standards

<rule>
name: database_standards
description: |
  Comprehensive standards for database access, emphasizing ActiveRecord best practices and controlled raw SQL usage.

filters:
  - type: path
    pattern: "^(app/models/.*\\.rb|db/.*\\.sql)$"

actions:
  - type: suggest
    message: |
      Database Interaction Guidelines:

      1. ActiveRecord Query Patterns:
         - Use method chaining for readability
         - Leverage named scopes for reusable queries
         ```ruby
         # ✅ Recommended
         User.active
              .with_profile
              .order(created_at: :desc)
              .limit(10)
         ```

      2. Raw SQL Usage - Strict Guidelines:
         a. Only permitted when:
            - Complex joins impossible in ActiveRecord
            - Proven performance bottlenecks
         b. Requirements for raw SQL:
            - Wrap in class/model method
            - Include performance comments
            - Use ActiveRecord::Base.sanitize_sql for interpolation
         ```ruby
         # 🟢 Acceptable Raw SQL Pattern
         def self.complex_business_report
           sql = sanitize_sql([<<-SQL, start_date, end_date])
             SELECT complex_business_logic
             FROM users
             WHERE created_at BETWEEN ? AND ?
           SQL
           find_by_sql(sql)
         end
         ```

      3. Query Optimization Checklist:
         - Always use eager loading (includes/preload)
         - Add database indexes strategically
         - Use counter caches for frequent count operations
         - Avoid N+1 queries with includes/preload
         ```ruby
         # ✅ Eager Loading Example
         users = User.includes(:posts, :comments)
         ```

      4. Performance Monitoring:
         - Use `explain` to analyze query plans
         - Log and monitor slow queries
         - Consider database-specific optimizations

  references:
    - https://guides.rubyonrails.org/active_record_querying.html
    - https://www.rubydoc.info/gems/rubocop-performance

metadata:
  priority: high
  version: 2.0
  related_rules:
    - models_standards
    - performance_guidelines
  responsibility: "Define and enforce standardized, performant database access patterns"
</rule>