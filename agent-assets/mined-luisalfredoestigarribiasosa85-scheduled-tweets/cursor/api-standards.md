---
description: API design and implementation standards
globs: app/controllers/api/**/*.rb
---
 ---
description: API design and implementation standards
globs: ["app/controllers/api/**/*.rb"]
---
# API Standards and Patterns

<rule>
name: api_standards
description: Standards for designing and implementing APIs

filters:
  - type: path
    pattern: "app/controllers/api/"
  - type: file_extension
    pattern: "\\.rb$"

actions:
  - type: suggest
    message: |
      When building APIs:

      1. Controller Structure:
         - Implement authorization scopes to ensure users only access allowed resources.

         Example:
         ```ruby
         module Api
           class ResourcesController < ApiController
             def index
               @resources = authorized_scope(Resource.all)
               render json: @resources
             end

             private

             def resource_params
               params.require(:resource).permit(:allowed_field)
             end
           end
         end
         ```

      2. Versioning:
         - Use namespace versioning
         - Implement proper documentation
         - Handle deprecations gracefully

      3. Response Format:
         - **Consistent JSON Structure**:
           Ensure responses follow a predictable format with keys for `data`, `errors`, and `meta`.

           Example:
           ```json
           {
             "data": {
               "id": 1,
               "type": "resource",
               "attributes": {
                 "name": "Example Resource",
                 "description": "A sample resource object."
               }
             },
             "meta": {
               "pagination": {
                 "current_page": 1,
                 "total_pages": 10
               }
             },
             "errors": null
           }
           ```

         - **Error Responses**:
           Use the `errors` key to communicate failures. Include status, code, title, and details where applicable.

           Example:
           ```json
           {
             "errors": [
               {
                 "status": "404",
                 "code": "not_found",
                 "title": "Resource Not Found",
                 "detail": "The requested resource with ID 123 could not be found."
               }
             ]
           }
           ```

         - **Status Code Mappings**:
           Map actions to appropriate HTTP status codes:

           | Action              | Status Code |
           |---------------------|-------------|
           | Successful GET      | 200 (OK)    |
           | Successful POST     | 201 (Created) |
           | No Content (DELETE) | 204 (No Content) |
           | Validation Errors   | 422 (Unprocessable Entity) |
           | Unauthorized Access | 401 (Unauthorized) |
           | Forbidden Access    | 403 (Forbidden) |
           | Not Found           | 404 (Not Found) |
           | Server Errors       | 500 (Internal Server Error) |

         - **Pagination**:
           Include pagination metadata in responses for collections.
           Example:
           ```json
           {
             "data": [...],
             "meta": {
               "pagination": {
                 "current_page": 2,
                 "next_page": 3,
                 "total_pages": 5,
                 "total_count": 50
               }
             }
           }
           ```

         - **Consistent Status Codes**:
           Ensure controllers return the correct status codes for success, errors, and redirects.

           Example in Rails:
           ```ruby
           def show
             resource = Resource.find(params[:id])
             render json: resource, status: :ok
           rescue ActiveRecord::RecordNotFound
             render json: { errors: [{ status: "404", title: "Not Found", detail: "Resource not found." }] }, status: :not_found
           end
           ```

examples:
  - input: |
      def show
        render json: @resource, status: :ok
      end
    output: "Proper API response pattern"

metadata:
  priority: high
  version: 1.0
</rule>