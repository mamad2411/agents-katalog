---
name: wpcom-api-console
description: Guidance on using the WordPress.com API Console. Trigger when testing endpoints, exploring the API interactively, or trying out REST requests without writing code.
---
# WordPress.com API Console

The API Console is an interactive tool provided by WordPress.com to test and explore REST API endpoints directly from the browser.

## Using the Console
1. **Access**: Visit https://developer.wordpress.com/docs/api/console/
2. **Authentication**: The console automatically authenticates using your currently logged-in WordPress.com account, allowing you to easily test endpoints requiring authorization without manually acquiring tokens.
3. **HTTP Methods**: You can select the HTTP method (GET, POST, PUT, DELETE) depending on the operation.
4. **Path Construction**: Build the path you want to test (e.g., `sites/example.wordpress.com/posts`).
5. **Parameters/Body**: For POST/PUT requests, you can provide a JSON body or form-data directly in the UI.

## When to use it
- To quickly verify the structure of a response payload.
- To test if your account has sufficient permissions to hit an endpoint.
- To debug API behavior before implementing it in your own code.

## Limitations
- The console tests endpoints with your personal user permissions. If your actual app uses a different user or scopes, the results might differ.
- For complex file uploads, you might need a tool like Postman or cURL.

## Reference
API Console: https://developer.wordpress.com/docs/api/console/
