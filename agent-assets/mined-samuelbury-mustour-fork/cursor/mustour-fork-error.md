---
description: handle errors
globs: 
---
### **1. Error Logging with @utils/logger**

- **Centralized Logging:**  
  - Always log errors using the `@utils/logger` module.  
  - Use it inside catch blocks to capture and log error details along with any relevant context (e.g., request IDs, user data, or operation context).

- **Contextual Information:**  
  - Ensure that you include meaningful details with every log entry. This could include the error message, stack trace (if available), and any additional parameters that help diagnose the issue.

- **Environment Considerations:**  
  - In development, consider logging full error details and stack traces.  
  - In production, avoid logging sensitive information while still capturing enough context to troubleshoot issues.

---

### **2. Error Handling with Prisma**

- **Wrapping Prisma Routes:**  
  - For any routes interacting with Prisma, wrap them using the `@/lib/handlers/withErrorHandling.ts` middleware.  
  - This middleware should catch errors thrown during Prisma operations, log them using `@utils/logger`, and return a consistent error response to the client.

- **Consistent Error Responses:**  
  - Ensure that your middleware returns standardized error objects with clear error messages and appropriate HTTP status codes.

---

### **3. Best Practices for Error Management**

- **Centralized Error Management:**  
  - Use a global error handler where possible to catch unhandled errors and prevent the application from crashing.  
  - Implement middleware or higher-order functions to capture errors in asynchronous operations.

- **Structured Error Objects:**  
  - Create structured error responses that include an error code, message, and any additional data that may help the client or debugging process.
  - Ensure that client-facing error messages are clear and do not expose internal details.

- **HTTP Status Codes:**  
  - Return appropriate HTTP status codes based on the error type (e.g., 400 for validation errors, 404 for not found, 500 for server errors).

- **Try-Catch Blocks:**  
  - Wrap asynchronous operations in try-catch blocks, especially around API calls and database operations.
  - Always log the caught error with the context to help trace the source.

- **Error Notification:**  
  - Consider integrating error tracking tools (like Sentry) to monitor and alert on errors in production environments.

- **Documentation and Comments:**  
  - Document your error handling strategy within your codebase. Include comments where errors are logged or handled to clarify why and how the error management works.

- **Testing:**  
  - Test error handling scenarios to ensure that errors are correctly caught, logged, and that the proper responses are sent to the client.

ies and middleware to maintain consistency and avoid duplicate code.