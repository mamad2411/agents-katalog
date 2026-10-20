---
description: Handling form
globs: 
---
To handle form use always react hook form and zod for the typing.

Use @/components/Form/LabelBlock to wrap the input or select.



### **1. Overall Approach and Code Reuse**  
- **Modular Design:**  
  - Break the form into generic, reusable components (e.g., header, input fields, file uploads, dynamic list sections).  
- **Check for Existing Solutions:**  
  - Before writing new code, search to see if a similar solution already exists.  
  - Reuse and adapt existing code or libraries to avoid duplicating functionality.
  - Use `@/components/Button` for buttons and set non-submit buttons with `type="button"`.  
- **Component Wrapping:**  
  - Wrap every input or select with `@/components/Form/LabelBlock` to ensure consistent styling and error display.

---

### **2. Form Management with React Hook Form and Zod**  
- **Initialization:**  
  - Always use `useForm` to initialize the form.  
  - Set up `defaultValues` appropriately for both creation and update scenarios.  
- **Validation:**  
  - Integrate Zod via a resolver (e.g., `zodResolver`) and define a Zod schema to enforce type safety and validate form inputs.  
- **Error Handling in Form:**  
  - Display clear, generic error messages when validation issues occur.  
- **Database Identification:**  
  - Ensure that every object coming from the database includes a `dbId` key.  
  - Use the `dbId` to distinguish between records that need updating and new records. Do not generate a new `dbId` for existing records; always use the one provided by the database.

---

### **3. Handling Dynamic and Nested Fields**  
- **Nested Structures:**  
  - Use `useFieldArray` (or similar tools) to manage dynamic lists or arrays of objects (e.g., photos, bed configurations, additional options).  
- **Default and Existing Data:**  
  - Initialize nested fields properly, handling existing data gracefully (e.g., marking items for deletion rather than removing them immediately).

---

### **4. Data Retrieval and Update Handling**  
- **Fetching Data with SWR:**  
  - Use SWR to fetch the current data when updating a record.  
  - Ensure that the fetched data includes the `dbId` for each object to identify which items are already in the database.  
- **Update Scenario:**  
  - When updating, ensure the form differentiates between new entries and those that exist (using the `dbId`).  
  - Manage the update process so that only the intended fields are updated without inadvertently creating duplicate records.

---

### **5. File Uploads and External Inputs**  
- **Componentization:**  
  - Create or reuse generic components to handle file uploads and previews.  
  - Integrate these components with React Hook Form so that file data is managed seamlessly.
- **Reusability:**  
  - Always reuse existing file upload logic or components if they are already available in the project.

---

### **6. User Interface and Feedback**  
- **Dynamic Sections:**  
  - Organize the form into clearly defined sections (e.g., general details, photos, description, dynamic lists for beds or equipment).  
- **Submission Handling:**  
  - Implement a submission function that validates data using Zod and processes the form data (including file uploads).  
  - Provide visual feedback (e.g., notifications) to indicate success or failure upon submission.
- **State Management:**  
  - Manage loading and submission states to prevent duplicate submissions and ensure smooth user interactions.

---

### **7. Best Practices for Error and Update Management**  
- **Error Logging:**  
  - Use the `@utils/logger` module to log errors consistently.  
  - Log detailed error messages along with context (e.g., request IDs, user actions) to facilitate debugging.  
- **Error Handling in API Routes (Prisma):**  
  - Wrap routes interacting with Prisma using `@/lib/handlers/withErrorHandling.ts`.  
  - Ensure that these routes catch errors, log them using `@utils/logger`, and return standardized error responses.
- **Structured Error Responses:**  
  - Create structured error objects that include an error code, message, and additional contextual data.
  - Use appropriate HTTP status codes (e.g., 400 for validation errors, 500 for server errors) when sending error responses.
- **Update Handling Best Practices:**  
  - Always fetch data with SWR when an update is required.  
  - Verify that each dynamic object has a `dbId` from the database to avoid confusion between new and existing records.
- **Documentation and Testing:**  
  - Document all error handling and update management strategies.  
  - Test various scenarios (creation, update, error cases) to ensure robust handling and to prevent duplication of code.

---







