---
description: an effort to help minimize agent errors
globs: 
---
# MANDATORY PROJECT RULES
These rules MUST be followed for ALL development work without exception

## Core Development Principles
1. INCREMENTAL DEVELOPMENT: Each component builds on previously completed work
2. PRESERVE WORKING FUNCTIONALITY: Never break existing features when implementing new ones
3. HYBRID SYSTEM INTEGRITY: Maintain separation between automated and expert-input systems
4. TIER-BASED FEATURE SEPARATION: Features must respect Free/Premium/Platinum boundaries

## System Architecture
The application consists of these separate systems that MUST work independently:
1. Public Landing Page (root URL): Marketing site for non-authenticated users
2. Dashboard System: Main application for authenticated users
3. Template Analysis Engine: Both automated and expert-input components
4. Admin Interface: For platform management and expert input
5. Authentication & Subscription: User management and tier control
6. API Endpoints: For data access and third-party integrations

## Critical Routes & Files
- `/` (src/app/page.tsx): Landing page - MUST remain a marketing page
- `/dashboard` (src/app/(dashboard)/...): User dashboard - NEVER redirect from root to here
- `/auth` (src/app/auth/...): Authentication system
- `/api/...` (src/app/api/...): API endpoints
- Admin components: Must preserve expert input capabilities

## Development Workflow
1. READ THE PLAN FIRST: Reference the Comprehensive Development Plan before any work
2. FOLLOW TESTING CHECKPOINTS: Use the specified checkpoints for each feature
3. ISOLATE CHANGES: Modify only files directly related to the current task
4. TEST BEFORE SUBMISSION: Verify existing routes still work:
   - Root URL (/) must show landing page
   - /dashboard must show dashboard for authenticated users
   - All API endpoints must remain functional

## Feature-Specific Guidelines
- Template Analysis: Preserve both automated and expert-input capabilities
- Newsletter Integration: Maintain "one-click to editor" functionality
- Admin Interface: Preserve hybrid AI-expert functionality and audit trails
- Trending Templates: Maintain prediction system with expert adjustment fields

## Weekly Development Focus (Per Plan)
- Week 1: Enhance Existing Application & Add Trend Analysis
- Week 2: Premium Features & Backend Integration
- Week 3: Platinum Features & Hybrid AI-Expert Admin Tools
- Week 4: Integration, Polish & Launch Preparation

FINAL CHECK: Before submitting ANY change, verify that ALL existing functionality still works, especially the landing page and dashboard routes. 


--------------------------------


# Consistency Control Protocol - Version 1.0

## Document Reference System

1. **Mandatory Reference Declaration**: At the beginning of any response involving established documentation, plans, or checklists, you MUST include the following declaration:
   ```
   REFERRING TO: [Document Name] (Version [X.X]) - [Creation Date]
   ```

2. **Verbatim Quotation Requirement**: When referencing any previously established checklist, implementation plan, or structured document, you MUST quote the relevant sections verbatim before providing commentary or updates.

3. **Change Notification**: When suggesting or implementing any deviation from established documentation, you MUST explicitly state:
   ```
   PROPOSED CHANGE NOTICE: The following represents a modification to the established [document name]. Original content is quoted verbatim above.
   ```

## Response Templates

1. **Progress Update Template**: When reporting progress against a checklist or plan, use ONLY this format:
   ```
   CHECKLIST ITEM: [Quote original item verbatim]
   STATUS: [Completed/In Progress/Not Started]
   EVIDENCE: [Specific evidence of completion or progress]
   BLOCKERS: [Any issues preventing completion]
   ```

2. **Information Request Template**: When providing information requested from an established source:
   ```
   SOURCE: [Name of exact source document]
   REQUESTED INFORMATION: [User's request verbatim]
   INFORMATION FROM SOURCE: [Quoted information verbatim]
   ADDITIONAL CONTEXT: [Any explanations or clarifications]
   ```

## Memory and Context Management

1. **Hash Verification**: Every conversation will establish a unique "consistency hash" in the format YYYYMMDD-NAME. You MUST reference this hash in every response related to the project.

2. **No Independent Framework Creation**: You are EXPLICITLY FORBIDDEN from creating new frameworks, checklists, or organizational structures without specific user authorization. If you believe a new framework is needed, request permission using this format:
   ```
   FRAMEWORK REQUEST: I believe a new [type of framework] would assist with [specific purpose]. Would you authorize its creation?
   ```

3. **Implementation Discipline**: You must NOT implement any feature or change without referencing the specific section of the established plan that authorizes it.

## Violation Handling

If at any point you detect that you are about to violate these consistency requirements, you MUST:

1. Stop immediately
2. Issue a "Consistency Violation Alert"
3. Quote the specific instruction you were about to violate
4. Request user guidance before proceeding

This protocol supersedes any general tendencies to create new organizational structures and ensures rigid adherence to established documentation and frameworks.
```

This structured approach would force me to:
1. Always reference specific documents
2. Quote items verbatim before providing commentary
3. Use strict templates for progress updates
4. Explicitly flag any deviations or changes
5. Never create new frameworks without permission
6. Maintain consistent reference points across conversations

Implementing these instructions would significantly reduce the risk of inconsistency and create clear warning signs when I might be deviating from established plans or documentation.

$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Critical Implementation Requirements

1. ALL changes, enhancements, refactoring, or new features MUST be reflected in the actual working user interface of the application.

2. Before suggesting or implementing any change, verify that it will be visible and functional to end users in the actual application interface.

3. Code-only changes that don't manifest in the UI are NOT considered complete unless specifically requested for backend purposes only.

4. When asked to create or modify features, you MUST:
   - Consider how users will access and interact with the feature
   - Ensure navigation paths to the feature are clear and functional
   - Verify that UI components described actually appear in the rendered application
   - Test that interactive elements (buttons, drag/drop, etc.) function as described

5. ALL responses about implementation should reference where and how to see the feature in the actual running application.

6. NEVER claim a feature is implemented if it only exists in code but isn't accessible in the actual user interface.

7. When showing examples or instructions, they must relate to the ACTUAL state of the application, not theoretical implementations.

8. Always prioritize end-user experience over code abstractions.

-------------------------

# The "Unicorn" UX/UI Philosophy

## Core Vision
Our goal is to create an interface so intuitive and seamless that it feels almost magical - what we call a "unicorn" UX/UI experience. This isn't just about aesthetics or functionality; it's about creating an emotional connection through an interface that disappears, leaving only the experience.

## Why This Matters
When building Trendzo, remember this critical insight: the best interfaces are invisible. Consider how a 4-year-old can pick up an iPad and instantly know what to do. This isn't an accident - it's deliberate design that feels natural to the human mind.

The difference between good software and exceptional software isn't just features - it's how those features make people feel. Our users don't want to "use a template management tool" - they want to create compelling content that drives engagement without friction.

## Guiding Principles

1. **Emotional Design Over Functional Design**
   - Every interaction should evoke a positive emotion
   - Delight should be found in small moments throughout the experience
   - The interface should anticipate needs before users recognize them

2. **Invisible Complexity**
   - Complex functionality should be progressively revealed
   - Users should never wonder "how do I do this?"
   - Power should be accessible without overwhelming

3. **Contextual Intelligence**
   - The interface should adapt to what the user is trying to accomplish
   - Related actions should flow naturally from one to another
   - Navigation should feel like following a conversation, not using a tool

4. **Sensory Harmony**
   - Visual elements, motion, and feedback should work in concert
   - Animations should have purpose - to orient, guide, or provide feedback
   - The rhythm of interaction should feel natural and responsive

## Implementation Focus
When implementing any feature or component, ask:
- Could a child understand how to use this without instruction?
- Does this feel like a natural extension of the user's intent?
- Have we removed every unnecessary element?
- Does using this create a moment of joy?

Remember: We're not building software; we're crafting experiences that feel like magic. The measure of our success is not what users can do with our platform, but how they feel while using it.

$$$$$$$$$$$$$$$$$$$$$$$$$
