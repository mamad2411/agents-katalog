---
name: polaris-accessibility
description: Build inclusive, accessible merchant experiences. Use this when implementing screen reader support, keyboard navigation, focus management, assistive technology compatibility, WCAG 2.1 compliance, alt text, ARIA attributes, disability support, universal design.
---

# Accessibility

Making commerce better for everyone means caring deeply about making quality products. A quality product should have a fantastic user experience (UX) that includes a beautiful and functional design, consistent and useful copy, and principles of universal design and inclusivity.

## Usable for Everyone

It's important that Shopify products are usable and useful to everyone. Everyone includes merchants, their customers, developer partners, employees, and the greater tech community at large. This also includes all members of the community who have disabilities.

Disabilities may affect how people move, see, hear, communicate, learn, understand, and process information. As a result, it's important to consider how to design and develop your product to support a wide range of needs and experiences.

**Disability Statistics:**
- United States: as many as 1 in 4 adults has at least 1 disability
- Canada: approximately 22%
- Worldwide: closer to 1 in 7

## Building Inclusive Experiences

Using Polaris components is a way to improve accessibility and consistency when building products. The component library includes accessible markup, and since this code exists in a single component reused across applications, it's easier to update and fix bugs.

Many accessibility features come free in the components. However, it's important to ensure that components are integrated in a way that doesn't create unforeseen accessibility barriers. Depending on how components are used, there may be more design and implementation considerations. Be sure to test user task flows post integration.

### Managing Focus to Support Merchant Workflows

Don't programmatically move focus to new content without merchant input. Polaris components that use controls to display overlays (such as modals and popovers) manage focus automatically.

**Do:**
- When a merchant activates a link that goes elsewhere on the page, move focus to that content
- When a merchant must access an overlay, move focus to it
- When a merchant submits a form that results in an error, move focus to the error message

**Don't:**
- Move focus when content updates in the background
- Move focus when the user is actively working elsewhere on the page

The only case where focus should be managed without the merchant's consent is when the merchant needs to be interrupted because they cannot continue their current workflow.

### Limiting Non-Standard Interactions

Merchants will expect to interact with controls and content in ways that follow the defaults for their browser, platform, and assistive technologies. Introducing non-standard features can give merchants better ways of accomplishing tasks, but they can also create barriers.

For example, merchants who rely on the keyboard will expect that buttons can be activated with the `enter`/`return` key or the `space` key. If buttons are programmed to use different keys, merchants will need explicit instructions.

Before designing or building custom features that use non-standard controls or interactions, first consider whether the goal can be met using native features.

If non-standard interactions are required:
- Carefully follow guidelines and best practices for designing, building, and testing custom features on your platform
- Give merchants clear instructions for using the custom feature
- Provide an additional, standard way to accomplish the task

### Assistive Technology Support

Polaris components are tested for accessibility with automated and manual techniques. Merchants should expect to be able to access features built with Polaris components using modern assistive technologies including:
- Screen readers
- Speech recognition programs
- Supports for low vision and color blindness
- Alternative keyboards
- Switch devices
- Tools for readability

### Coding Standards

Polaris components start with web standards for HTML, CSS, and JavaScript. Features from the Accessible Rich Internet Applications (WAI-ARIA or ARIA) specification are used to build functionality that is not available in native HTML.

### Alternative Text

To help people who rely on assistive technologies such as screen readers or text-to-speech programs, Polaris components use alternative text for icons and images used to convey information and actions (like buttons and links).

## Meeting WCAG Standards

Polaris targets WCAG 2.1 Level A and Level AA success criteria, and seeks to provide a highly usable experience for everyone.

**Key Standards:**
- WCAG 2.1: https://www.w3.org/TR/WCAG21/
- ARIA 1.1: https://www.w3.org/TR/wai-aria-1.1/
- Shopify's statement of commitment to accessibility: https://www.shopify.com/accessibility
