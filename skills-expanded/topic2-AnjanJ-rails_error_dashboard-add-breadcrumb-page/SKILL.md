---
description: Scaffold a full breadcrumb aggregate page — query, view, route, controller action, and specs
user-invocable: true
disable-model-invocation: true
---

# /add-breadcrumb-page — Scaffold Breadcrumb Aggregate Page

Create a complete breadcrumb aggregate page following the pattern established by deprecations, N+1 queries, and cache health pages.

## Usage

`/add-breadcrumb-page <name>` — e.g., `/add-breadcrumb-page slow_queries`

## What Gets Created

1. **Query**: `lib/rails_error_dashboard/queries/<name>.rb`
2. **View**: `app/views/rails_error_dashboard/errors/<name>.html.erb`
3. **Route**: Added to `config/routes.rb` (collection GET)
4. **Controller action**: Added to `app/controllers/rails_error_dashboard/errors_controller.rb`
5. **Query spec**: `spec/queries/rails_error_dashboard/<name>_spec.rb`
6. **Controller spec**: Added to existing controller spec or integration test

## Reference Files (Read These First)

Before creating anything, read the existing breadcrumb page implementations as reference:

### Query Pattern
Read `lib/rails_error_dashboard/queries/deprecation_warnings.rb` or `n_plus_one_summary.rb`:
- `self.call(params = {})` factory method
- `days` parameter (default 30, options: 7/30/90)
- `page` and `per_page` for pagination via Pagy
- Aggregation by breadcrumb category/message
- Returns `{ items:, pagy:, stats: { unique_count:, total_occurrences:, affected_errors: } }`

### View Pattern
Read `app/views/rails_error_dashboard/errors/deprecations.html.erb` or `n_plus_one_summary.html.erb`:
- Time-range filter buttons (7/30/90 days) with active state
- Three metric cards (unique count, total occurrences, affected errors)
- Pagination via `@pagy`
- Empty state with descriptive guide
- Data table with breadcrumb details and links to affected errors
- Guide links section at the bottom

### Route Pattern
In `config/routes.rb`, breadcrumb pages are collection GET routes:
```ruby
collection do
  get :deprecations, :n_plus_one_summary, :cache_health_summary
  get :<new_name>  # Add here
end
```

### Controller Action Pattern
Read the `deprecations` or `n_plus_one_summary` action in `errors_controller.rb`:
```ruby
def <name>
  result = RailsErrorDashboard::Queries::<ClassName>.call(
    days: params[:days],
    page: params[:page],
    per_page: 25
  )
  @items = result[:items]
  @pagy = result[:pagy]
  @stats = result[:stats]
end
```

### Sidebar Navigation
The sidebar in the layout (`app/views/layouts/rails_error_dashboard.html.erb`) has a "Breadcrumb Aggregates" section. Add a link for the new page.

## After Creating

1. Run the new specs:
   ```bash
   bundle exec rspec spec/queries/rails_error_dashboard/<name>_spec.rb
   ```
2. Run RuboCop on new files
3. Verify the page loads in the dummy app or a test app
4. Check the sidebar link works
