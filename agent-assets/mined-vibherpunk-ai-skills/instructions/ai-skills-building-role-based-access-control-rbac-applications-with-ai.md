# Copilot Instructions: Building Role Based Access Control (Rbac) Applications With Ai
Description: A systematic approach to building RBAC applications using AI for initial scaffolding and visual editors for refinement, focusing on permission models, database relationships, and workflow automation.

# Building RBAC Applications with AI

## Overview
This skill teaches you to efficiently build Role-Based Access Control (RBAC) applications using a hybrid AI/visual development approach. Key concepts are covered in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Define Requirements**
   - Identify all user roles (e.g., organizers, regular users)
   - List permissions for each role (create/edit vs. view)
   - Outline key data entities and relationships

2. **Initial Prompt**
   ```
   Build an event management app. Organizers can create and edit events with name, date, and description. Regular users can view events and sign up.
   ```

3. **Permission Modeling** (before generation)
   - Use visual tools to define access rules
   - Create permission groups with checkboxes
   - See [Practical Guide](references/practical_guide.md) for details

4. **Database Inspection**
   - Verify proper table relationships exist
   - Check for:
     - Events table (name, date, description)
     - Users table (with role differentiation)
     - Sign-ups table (linking users to events)

5. **Workflow Automation**
   - Set triggers (e.g., new sign-up)
   - Define actions (send emails, update status)
   - Add conditions (check capacity)

6. **Custom UI Logic**
   - Use AI only for specific components like:
   ```
   Create a live capacity counter that shows 'Only X spots left' and turns red when below 5.
   ```

## Best Practices
- Always model permissions first
- Use visual tools for workflows and permissions
- Reserve AI for small, custom UI components
- Inspect database relationships carefully

## Common Pitfalls
Avoid these mistakes documented in [Common Pitfalls](references/common_pitfalls.md):
- Generating before defining permissions
- Using flattened data structures
- Overusing AI for simple configuration

## Validation Steps
1. Test each role's permissions thoroughly
2. Verify database relationships handle real-world usage
3. Check workflows execute correctly
4. Confirm UI components respect permissions
5. Stress test edge cases (concurrent sign-ups, etc.)

## Implementation Notes
- This approach works best for business applications (internal tools, CRMs)
- For consumer UI-focused apps, consider different tools
- Always use the right tool for the job scope

## Reference Guides

### Common Pitfalls

# Common Pitfalls in AI-Assisted RBAC Development

1. **Premature Generation**: Building the app before defining permissions leads to expensive rework. Example: Generating a UI where organizer vs. regular user is just a button label rather than a true permission.

2. **Flattened Data Structures**: Using comma-separated strings instead of proper relational tables. This breaks when users sign up for multiple events.

3. **Over-Reliance on AI**: Using AI for everything, including tasks better suited to visual tools. This runs up token costs for simple permission changes.

4. **Fragile Automations**: Creating workflows that break when the data model changes, requiring constant AI regeneration.

5. **Incomplete Testing**: Not verifying that permission rules work at all levels (UI, API, database).

6. **Scope Mismatch**: Using the wrong tool for the job (e.g., trying to build a consumer UI app with a business tool).

## Anti-Pattern Examples
- Storing sign-ups as "user1,user2" in an events table
- Reprompting AI to fix permission issues instead of using visual permission editors
- Building complex workflows through sequential AI prompts rather than integrated automation tools
- Not considering edge cases like concurrent sign-ups or permission changes

## Prevention Strategies
- Always define permissions before generation
- Inspect the generated database schema for proper relationships
- Use visual tools for permissions and workflows
- Reserve AI for specific custom UI components
- Test all permission scenarios thoroughly

### Core Concepts

# Core Concepts of RBAC with AI

Role-Based Access Control (RBAC) is a method of restricting system access to authorized users based on their roles within an organization. When building RBAC applications with AI, several core concepts are critical:

1. **Permission Modeling**: Defining what each user role can see and do in the system before any code is generated. This prevents costly rework later.

2. **Database Relationships**: Properly modeling relationships between tables (e.g., users, events, sign-ups) rather than using flattened structures that break under real usage.

3. **Hybrid Development Approach**: Using AI for initial scaffolding and specific custom logic components, while relying on visual editors for permission models, workflows, and refinements.

4. **Workflow Automation**: Creating automated processes (like email notifications) that are tightly integrated with the data model and don't require constant AI regeneration.

5. **Credit Efficiency**: Understanding which parts of development should use AI (custom UI logic) and which should use visual tools (permissions, workflows) to minimize token usage.

A key insight is that AI should be used surgically for specific tasks where it excels, not as a blanket solution for all development needs. The most common mistake is generating first and asking about permission models later, which leads to expensive rework.

### Practical Guide

# Practical Guide to Building RBAC Apps

## Initial Setup
1. Start with a clear prompt describing your application's core functionality and user roles. For example:
   "Build an event management app. Organizers can create and edit events with name, date, and description. Regular users can view events and sign up."

2. Before any generation occurs, define:
   - All user roles (e.g., organizers, regular users)
   - Permissions for each role (create/edit vs. view)
   - Key data entities and their relationships

## Database Design
- Ensure your tool creates proper relational tables, not flattened structures
- Verify relationships are modeled correctly (e.g., sign-ups should link users to events via a join table)
- Check that all necessary fields exist for each entity

## Permission Implementation
- Use visual tools to assign permissions rather than prompting AI
- Create clear permission groups with checkboxes for each capability
- Test each role's access thoroughly

## Workflow Automation
- Set up triggers based on data changes (e.g., new sign-up)
- Define actions (send email, update status)
- Add conditions (check capacity before allowing sign-up)
- Ensure workflows update automatically when data model changes

## Custom Logic
- Use AI only for specific UI components (like a capacity counter)
- Keep these components self-contained and permission-aware
- Avoid using AI for core permission or workflow logic

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Role-Based Access Control: How to Build an RBAC App with AI](https://www.youtube.com/watch?v=OFO8r0-EgyY)** by AI Master