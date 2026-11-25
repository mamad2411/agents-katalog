---
name: dsar-and-opt-out
description: Technical guidelines for implementing Data Subject Access Requests (DSARs) and "Do Not Sell or Share My Personal Information" workflows for CCPA/CPRA.
---

# DSAR and "Do Not Sell or Share" Workflows

Under the CCPA/CPRA, businesses must provide consumers with mechanisms to exercise their data rights, including the right to know, delete, correct, and opt-out of the "sale" or "sharing" of their personal information.

## "Do Not Sell or Share My Personal Information" Link

1. **Clear and Conspicuous**: The link must be visible and placed in a standard location, such as the website footer.
2. **Actionable**: Clicking the link should immediately present the user with a way to opt-out. This can be a modal, a dedicated preference center page, or an immediate toggle.
3. **No Dark Patterns**: The process to opt-out must not be more difficult than the process to opt-in.

### Technical Implementation
Provide a distinct link in the global footer:
```html
<footer>
  <!-- Other links -->
  <a href="#" id="do-not-sell-link">Do Not Sell or Share My Personal Information</a>
</footer>

<script>
  document.getElementById('do-not-sell-link').addEventListener('click', (e) => {
    e.preventDefault();
    openPrivacyPreferenceCenter(); // Opens a modal to manage preferences
  });
</script>
```

## Data Subject Access Requests (DSARs)

Consumers have the right to request access to the data a business holds on them, request deletion, or correct inaccuracies.

### Core Technical Requirements

1. **Submission Channels**: You must provide at least two methods for users to submit requests (e.g., a web form and an email address).
2. **Verification Mechanism**: You must reasonably verify the identity of the person making the request to prevent unauthorized data disclosures.
3. **Data Mapping**: Technical systems must be able to aggregate a user's data across all databases, CRM platforms, and third-party SaaS tools to fulfill an access or deletion request.

### Implementation Guidelines

- **Web Form Integration**: Build a dedicated `/privacy/requests` page containing a form that captures the necessary information (Name, Email, Type of Request).
- **Backend Automation**: Route the form submissions securely to an internal privacy team dashboard or an automated privacy management platform (like OneTrust, Secuvy, or Transcend).
- **Data Deletion**: When implementing "Right to Delete" workflows, ensure that data is deleted or anonymized securely across primary databases, logs, and backups within the statutory timeframe (typically 45 days).
