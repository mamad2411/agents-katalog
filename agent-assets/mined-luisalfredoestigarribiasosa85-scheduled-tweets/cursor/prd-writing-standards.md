---
description: Standards for writing effective Product Requirements Documents (PRDs)
globs: "**/*.prd.md"
alwaysApply: false
---
# Product Requirements Document (PRD) Writing Standards

<rule>
name: prd_writing_standards
description: Detailed standards for writing clear, comprehensive, and actionable Product Requirements Documents

filters:
  - type: file_name
    pattern: ".*\\.prd\\.md$"

actions:
  - type: suggest
    message: |
      When writing a Product Requirements Document (PRD), follow these standards:

      ## 1. Document Structure
      Every PRD should include these sections in order:

      ```markdown
      # [Product Name]: [Feature Name]

      ## Overview
      Brief description of the feature and its purpose (2-3 sentences)

      ## Background and Strategic Fit
      - Why we need this feature
      - How it aligns with product strategy
      - Business objectives it addresses

      ## Success Metrics
      - Specific KPIs that will measure success
      - Target values for these metrics

      ## Requirements
      ### User Stories
      - As a [user type], I want [goal] so that [benefit]
      - As a [user type], I want [goal] so that [benefit]

      ### Functional Requirements
      - Detailed descriptions of functionality
      - Acceptance criteria for each requirement

      ### Non-Functional Requirements
      - Performance expectations
      - Security considerations
      - Accessibility requirements
      - Compliance needs

      ## User Experience
      - User flows
      - Wireframes/mockups (or links)
      - Design specifications

      ## Technical Considerations
      - System architecture impacts
      - Third-party dependencies
      - Potential technical challenges

      ## Implementation Plan
      - Phasing strategy (if applicable)
      - Dependencies on other features/teams
      - Timeline estimates

      ## Open Questions
      - List unresolved questions that need answers

      ## Appendix
      - Supporting research
      - Competitive analysis
      - Additional context
      ```

      ## 2. Content Guidelines
      - **Be specific**: Avoid vague language; use concrete details
      - **Quantify**: Use numbers where possible (e.g., "load within 200ms" vs "load quickly")
      - **Distinguish**: Clearly separate "must-have" from "nice-to-have" requirements
      - **Use plain language**: Minimize jargon and acronyms, or define them
      - **Focus on the what, not the how**: Define requirements without prescribing implementation details
      - **Include rationale**: Explain the "why" behind key requirements
      - **Use visuals**: Include diagrams, wireframes, and mockups where helpful

      ## 3. Review Checklist
      Before finalizing your PRD, ensure:
      - All acceptance criteria are testable
      - Requirements are technology-agnostic where appropriate
      - Edge cases and error states are addressed
      - Stakeholders have reviewed and approved
      - Dependencies are clearly identified
      - Scope is realistic and aligned with timeline

examples:
  - input: |
      # User Profile: Edit Feature
      
      This document describes the edit profile feature.
      
      ## Requirements
      - Users should be able to edit their profile
      - Changes should be saved
      - UI should be nice
      
      ## Timeline
      We should finish this in Q2.
    output: |
      This PRD lacks specific details and structure. It should:
      - Include all required sections (Overview, Background, Success Metrics, etc.)
      - Define specific user stories and detailed requirements
      - Include acceptance criteria for each requirement
      - Specify non-functional requirements
      - Include mockups or wireframes for the UI
      - Provide specific timeline estimates rather than general quarters

  - input: |
      # User Profile: Edit Feature
      
      ## Overview
      The Edit Profile feature allows users to update their personal information, preferences, and settings through an intuitive interface accessible from their account dashboard.
      
      ## Background and Strategic Fit
      - Currently, users must contact support to change profile information, creating friction and support overhead
      - This feature aligns with our Q2 goal of increasing user self-service capabilities by 50%
      - Will reduce support tickets related to profile changes by an estimated 70%
      
      ## Success Metrics
      - Reduce profile-related support tickets by 70% within 3 months of launch
      - Achieve 90% task completion rate for profile edits
      - Maintain an average edit completion time under 2 minutes
      
      ## Requirements
      
      ### User Stories
      - As a user, I want to edit my personal information so that my account reflects my current details
      - As a user, I want to change my notification preferences so that I receive only relevant communications
      - As a user, I want to see a confirmation when my changes are saved so that I feel confident they were applied
      
      ### Functional Requirements
      1. User can edit the following fields:
         - Name (First, Last)
         - Email address (with verification)
         - Phone number (with verification)
         - Notification preferences
         - Time zone
         - Language preference
      
      2. Validation requirements:
         - Email must be in valid format
         - Phone must be in valid format with country code
         - Name fields cannot contain special characters
      
      3. Form must autosave changes after 5 seconds of inactivity
      
      4. Show confirmation message after successful save
      
      ### Non-Functional Requirements
      - Changes must be saved within 1 second
      - Interface must be accessible (WCAG AA compliant)
      - Must work across all supported browsers
      - Must be responsive for mobile devices
      
      ## User Experience
      [Link to Figma mockups]
      
      ### User Flow
      1. User navigates to profile from dashboard
      2. User selects "Edit Profile" button
      3. Form fields become editable
      4. User makes changes
      5. Changes autosave or user clicks "Save" button
      6. Confirmation message appears
      
      ## Technical Considerations
      - Will require updates to the User API service
      - Email/phone verification will use existing verification microservice
      - Changes may require cache invalidation
      
      ## Implementation Plan
      - Phase 1 (2 weeks): Basic info editing
      - Phase 2 (2 weeks): Email/phone verification integration
      - Phase 3 (1 week): Preference management
      
      ## Open Questions
      - Should users be logged out after changing email?
      - Do we need approval flows for enterprise accounts?
      
      ## Appendix
      - User feedback summary from support tickets
      - Analysis of competitor profile management features
    output: |
      This is a well-structured PRD that:
      - Follows the recommended structure
      - Includes specific, measurable success metrics
      - Provides detailed functional and non-functional requirements
      - Clearly defines the user flow
      - Breaks implementation into manageable phases
      - Addresses technical considerations
      - Acknowledges open questions that need resolution

metadata:
  priority: high
  version: 1.0
  related_rules:
    - technical_specification_standards
    - feature_documentation_standards
  responsibility: "Product requirements documentation structure and content"
  standard_patterns:
    sections:
      - overview
      - background
      - success_metrics
      - requirements
      - user_experience
      - technical_considerations
      - implementation_plan
      - open_questions
      - appendix
</rule>