---
name: generate-postman-collection
description: Automatically generate or update a Postman API collection by analyzing a Rails application's routes, controllers, and test specs. Use when the user wants a Postman collection created or refreshed for a Rails app's API.
---

# Generate Postman Collection

Automatically generate or update the Postman API collection by analyzing the Rails application routes, controllers, and test specs.

## Task Instructions

You are tasked with generating or updating the Postman collection file `postman_collection.json` based on the current state of the Rails API.

Follow these steps:

If there is no existing Postman collection file `postman_collection.json`, 
skip to Step 2.

1. **Check for API-related changes first** (to avoid unnecessary work):
   - Use `git diff` to check if there are any changes to API-related files compared to the main branch
   - Check these paths: `config/routes.rb`, `app/controllers/api/`, `spec/requests/api/`
   - Also check for staged and unstaged changes in the current working directory
   - If NO changes are found in any of these locations, output "No API changes detected - skipping Postman collection update"
   - If changes ARE found, continue to step 2

2. **Read the Rails routes** from `config/routes.rb` to identify all API endpoints

3. **Analyze each API controller** in `app/controllers/api/` to understand:
   - Request parameters (required and optional)
   - Request body structure
   - Response format
   - Authentication requirements
   - Status codes returned

4. **Review RSpec test files** in `spec/requests/api/v1/` to extract:
   - Example request bodies
   - Example responses
   - Valid parameter values
   - Edge cases and validation rules

5. **Generate or update the Postman collection** with:
   - All API endpoints organized in logical folders
   - Complete request examples with proper HTTP methods
   - Request body examples in JSON format
   - Query parameters where applicable
   - Headers (especially Authorization header for authenticated endpoints)
   - Example responses
   - Clear descriptions for each endpoint
   - Variables for `{{base_url}}` and `{{api_token}}`
   - Test scripts that auto-save the API token after successful login

6. **Maintain the existing structure**:
   - Keep the same collection name: "postman_collection"
   - Preserve the variables: `base_url` and `api_token`
   - Maintain folder organization
   - Keep the login test script that auto-saves the token

7. **Ensure completeness**:
   - Every route in `config/routes.rb` should have a corresponding request
   - Each request should have accurate parameters and examples
   - Descriptions should explain what each endpoint does
   - Authentication requirements should be clearly indicated

8. **Write the updated collection** to `postman_collection.json`

## Important Notes

- Use the RSpec tests as the source of truth for request/response examples
- Maintain proper Postman collection v2.1 format
- Ensure all JSON is properly formatted and valid

## Output

After completing the update, provide a summary of:

- Number of endpoints documented
- Any new endpoints added
- Any endpoints removed or modified
- Any issues or ambiguities found

## Completion

If changes have been made notify the user to commit them.
