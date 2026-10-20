---
applyTo: '**'
---

# Malaysia Government Design System (MYDS) AI Development Instructions (2025)

_Last updated: August 2025_

- This file defines repository-specific rules for AI assistants when generating UI code that must comply with the Malaysia Government Design System (MYDS).
- Do not rely on out-of-date knowledge — fetch the official MYDS docs when in doubt:
  - MYDS Home: https://design.digital.gov.my/en
  - Design Guidelines: https://design.digital.gov.my/en/docs/design
  - Development Docs: https://design.digital.gov.my/en/docs/develop
  - Colour guidance: https://design.digital.gov.my/en/docs/design/color
  - Icon guidance: https://design.digital.gov.my/en/docs/design/icon

## About This File

applyTo: '**.blade.php|**.js|**.jsx|**.ts|**.tsx|**.vue|**.php|**.md|**.css|**.scss|**.sass|**.less|**.json|**.yml|\*\*.yaml'
fileType: 'MYDS-Instructions'
lastUpdated: '2025-09-21'
mydsVersion: '2025.2'
compatibleWith: 'Laravel 12, Filament v4, Livewire 3, TailwindCSS 4, PHP 8.2'

---

# Malaysia Government Design System (MYDS) — AI & Developer Instructions

> **This file is the authoritative MYDS implementation guide for ICTServe.**
> It is optimized for AI agents (Copilot, VS Code, LLMs) and human contributors.

## Version & Compatibility

- **MYDS Version:** 2025.2
- **Last Updated:** 21 September 2025
- **Compatible With:** Laravel 12, Filament v4, Livewire 3, TailwindCSS 4, PHP 8.2

---

## 1. Purpose & Scope

- **Audience:** AI agents, developers, and reviewers working on ICTServe
- **Mandate:** All UI code must strictly follow MYDS and MyGovEA principles
- **Integration:** This file cross-references:
  - [`myds-color-reference.md`](myds-color-reference.md) — All color tokens
  - [`myds-components.md`](myds-components.md) — All component usage patterns
  - [`mygovea.principles.instructions.md`](mygovea.principles.instructions.md) — MyGovEA design principles
  - [Official MYDS Docs](https://design.digital.gov.my/en/docs/design)

---

## 2. Quick Reference Cheat Sheets

### 2.1. Color Tokens

- **Never use raw hex codes.**
- Use only tokens from [`myds-color-reference.md`](myds-color-reference.md)
- Example:
  ```blade
  <button class="bg-primary-600 text-white">Submit</button>
  <span class="text-danger-600">*</span>
  ```

### 2.2. Component Usage

- Use only patterns from [`myds-components.md`](myds-components.md)
- Example (Blade):
  ```blade
  <x-myds.button variant="primary" size="md" wire:click="submit">
    Submit
  </x-myds.button>
  ```
- Example (Filament v4):
  ```php
  Forms\Components\TextInput::make('purpose')
      ->label('Purpose of Loan')
      ->required()
      ->columnSpanFull()
  ```

### 2.3. Grid & Layout

- Use the 12-8-4 grid (desktop-tablet-mobile)
- Use Tailwind gap utilities for spacing
- Example:
  ```blade
  <div class="grid grid-cols-12 gap-6">
    <div class="col-span-8">Main</div>
    <div class="col-span-4">Sidebar</div>
  </div>
  ```

### 2.4. Icon System

- Use only official MYDS icons (see [MYDS Icon Gallery](https://design.digital.gov.my/en/icon))
- Example:
  ```blade
  <x-myds.icon
    name="check-circle"
    class="text-success-600"
    aria-label="Success"
  />
  ```

---

## 3. AI Directives for MYDS Tasks

- **Always** reference [`myds-color-reference.md`](myds-color-reference.md) and [`myds-components.md`](myds-components.md) for tokens and patterns
- **Never** use hardcoded colors, custom icons, or ad-hoc components
- **Validate** all UI for:
  - Color token usage
  - Component anatomy
  - Accessibility (see below)
- **If unsure**, fetch the latest [official docs](https://design.digital.gov.my/en/docs/design)
- **For new patterns**, update the referenced files and cross-link

---

## 4. Compliance Checklist (PR/Review)

- [ ] All colors use tokens from `myds-color-reference.md`
- [ ] All UI uses patterns from `myds-components.md`
- [ ] Only official MYDS icons are used
- [ ] 12-8-4 grid and spacing conventions are followed
- [ ] All forms have inline validation and ARIA attributes
- [ ] All interactive elements are keyboard accessible
- [ ] No custom styles or hex codes
- [ ] All code is compatible with Laravel 12, Filament v4, Livewire 3
- [ ] Accessibility: WCAG 2.2 AA (≥4.5:1 contrast, focus, ARIA, touch targets)
- [ ] No duplication of content from referenced files

---

## 5. Common Mistakes to Avoid

- ❌ Using raw hex codes (e.g. `#2563EB`) — use `bg-primary-600` instead
- ❌ Custom icons or icon libraries — use only MYDS icons
- ❌ Inline validation in controllers — use Form Requests
- ❌ Ignoring ARIA/keyboard/focus for forms/buttons
- ❌ Not using the 12-8-4 grid for layout
- ❌ Duplicating component code instead of referencing `myds-components.md`

---

## 6. Accessibility & WCAG Guidance

- **All forms:**
  - Use ARIA attributes (`aria-label`, `aria-describedby`)
  - Provide inline error messages (see `myds-components.md`)
  - Ensure keyboard navigation (tab order, focus ring)
- **All icons:**
  - Use `aria-label` for meaningful icons
  - Use `aria-hidden="true"` for decorative icons
- **Contrast:**
  - Use only tokens with ≥4.5:1 contrast (see `myds-color-reference.md`)
- **Touch targets:**
  - Minimum 48×48px for all interactive elements
- **Skip links:**
  - Provide skip links at the top of every page

---

## 7. Performance Optimization Tips

- Use semantic tokens for theme switching (light/dark)
- Prefer lazy-loading for heavy components
- Minimize DOM nesting and avoid unnecessary wrappers
- Use Tailwind gap utilities for spacing, not margin hacks
- Optimize SVG icons (use sprite or inline, not external requests)

---

## 8. Error Prevention & Validation Rules

- **Automated validation:**
  - Lint for color token usage
  - Lint for component anatomy (see `myds-components.md`)
  - Run accessibility checks (axe, Lighthouse)
- **Manual review:**
  - Use the checklist above for every PR
- **AI agents:**
  - Refuse to generate code that violates any MYDS rule
  - If a referenced file is missing, halt and request it

---

## 9. Update & Contribution Process

- Update this file when MYDS, Laravel, or Filament versions change
- Update referenced files (`myds-color-reference.md`, `myds-components.md`) as new tokens/components are added
- Cross-link new patterns and examples
- Keep all references current and accurate

---

## 10. External References

- [Official MYDS Docs](https://design.digital.gov.my/en/docs/design)
- [MYDS Icon Gallery](https://design.digital.gov.my/en/icon)
- [MYDS Figma Kit](https://www.figma.com/design/svmWSPZarzWrJ116CQ8zpV/MYDS--Beta-)

---

> **This file is optimized for AI and human use.**
> For full color and component details, always reference the linked files above.

- **Stroke scaling**: Proportional adjustment for all sizes
- **Style variants**:
  - **Outline**: Primary style with stroke outlining the glyph
  - **Filled**: Solid fill style for emphasis or active states
- **Consistency**: Maintain stroke width ratios when exporting SVGs

#### Visual Characteristics

- **Corner radius**: 2px radius for rounded elements within icons
- **Line caps**: Rounded caps for all stroke endings
- **Optical alignment**: Icons optically centered within their bounding box
- **Negative space**: Adequate spacing between elements for clarity

### Accessibility Guidelines

#### Color Contrast

- Ensure minimum contrast ratio of 4.5:1 against background
- Icons should work in both light and dark themes
- Never rely on color alone to convey meaning

#### ARIA and Screen Reader Support

```html
<!-- Decorative icons -->
<svg aria-hidden="true" role="presentation">...</svg>

<!-- Functional icons with meaning -->
<svg role="img" aria-label="Search">
  <title>Search</title>
  ...
</svg>

<!-- Icons with text labels -->
<button>
  <svg aria-hidden="true">...</svg>
  <span>Submit Form</span>
</button>
```

#### Keyboard Navigation

- Ensure all interactive icons are keyboard accessible
- Provide clear focus indicators
- Include tooltips for icon-only buttons
- Support standard keyboard shortcuts where applicable

#### Text Pairing

- Always pair icons with text labels in critical interfaces
- Use tooltips for icon-only buttons
- Provide alternative text for informational icons
- Consider cultural differences in icon interpretation

### Usage Examples

#### In Buttons

```html
<!-- Primary button with leading icon -->
<button class="btn btn-primary">
  <svg aria-hidden="true"><!-- download icon --></svg>
  Download Report
</button>

<!-- Icon-only button with accessible label -->
<button class="btn btn-icon" aria-label="Close dialog">
  <svg aria-hidden="true"><!-- close icon --></svg>
</button>
```

#### In Forms

```html
<!-- Input field with trailing icon -->
<div class="input-group">
  <input type="search" placeholder="Search..." />
  <svg class="input-icon" aria-hidden="true"><!-- search icon --></svg>
</div>

<!-- Status indicator with icon -->
<div class="form-message form-message--success">
  <svg aria-hidden="true"><!-- check-circle icon --></svg>
  Form submitted successfully
</div>
```

#### In Navigation

```html
<!-- Navigation with icons -->
<nav>
  <a href="/dashboard">
    <svg aria-hidden="true"><!-- dashboard icon --></svg>
    Dashboard
  </a>
  <a href="/profile">
    <svg aria-hidden="true"><!-- user icon --></svg>
    Profile
  </a>
</nav>
```

#### In Alerts and Notifications

```html
<!-- Alert with status icon -->
<div class="alert alert--warning" role="alert">
  <svg aria-hidden="true"><!-- warning-triangle icon --></svg>
  <div>
    <h4>Session Expiring</h4>
    <p>Your session will expire in 5 minutes.</p>
  </div>
</div>
```

### Integration and Implementation

#### React/MYDS Components

```jsx
// Using MYDS React icon components
import { Icon } from '@govtechmy/myds-react';

// Standard icon usage
<Icon name="search" size={20} />

// Icon with custom props
<Icon
  name="download"
  size={24}
  variant="filled"
  className="text-primary-600"
/>

// Icon in button component
<Button variant="primary" iconLeading="download">
  Download Report
</Button>
```

#### SVG Direct Usage

```html
<!-- Inline SVG with proper accessibility -->
<svg width="20" height="20" viewBox="0 0 20 20" role="img" aria-label="Search">
  <title>Search</title>
  <path d="..." stroke="currentColor" stroke-width="1.5" fill="none" />
</svg>
```

#### CSS Custom Properties

```css
/* Icon sizing variables */
:root {
  --icon-size-sm: 16px;
  --icon-size-md: 20px;
  --icon-size-lg: 24px;
  --icon-size-xl: 32px;
  --icon-size-2xl: 42px;

  --icon-stroke-width: 1.5px;
}

/* Responsive icon sizing */
.icon {
  width: var(--icon-size-md);
  height: var(--icon-size-md);
  stroke-width: var(--icon-stroke-width);
}
```

#### Figma Kit Integration

- Access the official MYDS Figma icon library
- Use the icon components directly in prototypes
- Maintain consistency with development implementation
- Export icons as SVG when creating custom components

### Performance Considerations

#### Optimization

- Use SVG sprites for frequently used icons
- Implement icon lazy loading for large sets
- Minimize SVG file sizes through proper optimization
- Consider icon fonts for simple implementations

#### Caching

- Implement proper caching strategies for icon assets
- Use CDN for icon delivery when appropriate
- Version icon assets to enable cache busting

### Contribution Guidelines

#### Requesting New Icons

1. **Assessment**: Verify the icon doesn't already exist in current sets
2. **Justification**: Provide clear use case and context for the new icon
3. **Specification**: Include desired meaning, context, and references
4. **Review**: Submit request through official MYDS channels

#### Icon Submission Process

1. **Design**: Follow established grid, stroke, and style guidelines
2. **Variants**: Provide both outline and filled versions
3. **Documentation**: Include usage guidelines and accessibility notes
4. **Testing**: Verify icon works across required sizes and contexts
5. **Review**: Submit for official design system review and approval

#### Quality Standards

- Maintain visual consistency with existing icon library
- Ensure accessibility compliance (contrast, screen reader support)
- Follow naming conventions and organizational structure
- Provide comprehensive documentation for usage

### Official Resources

- **Icon Guidelines**: https://design.digital.gov.my/en/docs/design/icon
- **Icon Gallery**: https://design.digital.gov.my/en/icon
- **Figma Kit**: Official MYDS design files with complete icon library
- **Developer Docs**: https://design.digital.gov.my/en/docs/develop

## MYDS Icon Reference

This section provides a comprehensive reference of all official MYDS icons organized by category. Each icon is available in both outline and filled variants at standard sizes.

### Generic Icons

Essential interface and action icons for common functionality:

| Icon Name             | Description          | Usage Context                        | ARIA Label Example   |
| --------------------- | -------------------- | ------------------------------------ | -------------------- |
| **Navigation**        |                      |                                      |                      |
| `home`                | Home/main page       | Navigation, breadcrumbs              | "Go to home page"    |
| `arrow-left`          | Back/previous        | Back buttons, pagination             | "Go back"            |
| `arrow-right`         | Forward/next         | Next buttons, progression            | "Continue"           |
| `arrow-up`            | Up direction         | Scroll to top, move up               | "Scroll to top"      |
| `arrow-down`          | Down direction       | Dropdown menus, move down            | "Expand menu"        |
| `chevron-left`        | Left navigation      | Carousel controls, collapse          | "Previous"           |
| `chevron-right`       | Right navigation     | Carousel controls, expand            | "Next"               |
| `chevron-up`          | Up chevron           | Collapse sections                    | "Collapse"           |
| `chevron-down`        | Down chevron         | Expand sections                      | "Expand"             |
| `menu`                | Hamburger menu       | Mobile navigation toggle             | "Open menu"          |
| `close`               | Close/dismiss        | Modal dialogs, alerts                | "Close"              |
| **Actions**           |                      |                                      |                      |
| `plus`                | Add/create           | Add buttons, new items               | "Add new item"       |
| `minus`               | Remove/subtract      | Remove items, decrease               | "Remove item"        |
| `edit`                | Edit/modify          | Edit buttons, modify content         | "Edit item"          |
| `trash`               | Delete/remove        | Delete buttons, remove items         | "Delete item"        |
| `search`              | Search/find          | Search inputs, find functionality    | "Search"             |
| `filter`              | Filter/sort          | Filter controls, refine results      | "Filter results"     |
| `refresh`             | Reload/update        | Refresh buttons, sync                | "Refresh page"       |
| `save`                | Save/store           | Save buttons, store data             | "Save changes"       |
| `copy`                | Copy/duplicate       | Copy buttons, duplicate content      | "Copy to clipboard"  |
| `share`               | Share/send           | Share buttons, social sharing        | "Share content"      |
| **Status & Feedback** |                      |                                      |                      |
| `check`               | Success/confirm      | Success states, confirmations        | "Success"            |
| `check-circle`        | Completed/verified   | Completed tasks, verification        | "Completed"          |
| `x-circle`            | Error/failed         | Error states, failed actions         | "Error"              |
| `alert-triangle`      | Warning/caution      | Warning states, important notices    | "Warning"            |
| `info`                | Information          | Info states, help content            | "Information"        |
| `help`                | Help/support         | Help buttons, support links          | "Get help"           |
| `question`            | Question/unknown     | FAQ, unclear states                  | "More information"   |
| `exclamation`         | Alert/urgent         | Urgent alerts, critical notices      | "Important alert"    |
| **Utilities**         |                      |                                      |                      |
| `settings`            | Settings/preferences | Settings pages, configuration        | "Open settings"      |
| `gear`                | Configuration        | System settings, admin tools         | "Configure"          |
| `download`            | Download/get         | Download buttons, file retrieval     | "Download file"      |
| `upload`              | Upload/send          | Upload buttons, file submission      | "Upload file"        |
| `print`               | Print/output         | Print buttons, document output       | "Print document"     |
| `mail`                | Email/message        | Contact forms, messaging             | "Send email"         |
| `phone`               | Phone/call           | Contact information, calling         | "Make phone call"    |
| `external-link`       | External link        | Links to external sites              | "Open in new window" |
| `calendar`            | Date/time            | Date pickers, event scheduling       | "Select date"        |
| `clock`               | Time/duration        | Time inputs, scheduling              | "Select time"        |
| `eye`                 | View/show            | Show password, view details          | "Show content"       |
| `eye-off`             | Hide/conceal         | Hide password, conceal content       | "Hide content"       |
| `star`                | Favorite/rating      | Bookmarks, ratings, favorites        | "Add to favorites"   |
| `heart`               | Like/favorite        | Social interactions, preferences     | "Like item"          |
| `thumbs-up`           | Approve/positive     | Approval actions, positive feedback  | "Approve"            |
| `thumbs-down`         | Disapprove/negative  | Rejection actions, negative feedback | "Disapprove"         |

### WYSIWYG Icons

Text editor and content formatting tools:

| Icon Name             | Description        | Usage Context                       | ARIA Label Example      |
| --------------------- | ------------------ | ----------------------------------- | ----------------------- |
| **Text Formatting**   |                    |                                     |                         |
| `bold`                | Bold text          | Text editors, formatting toolbar    | "Make text bold"        |
| `italic`              | Italic text        | Text editors, formatting toolbar    | "Make text italic"      |
| `underline`           | Underlined text    | Text editors, formatting toolbar    | "Underline text"        |
| `strikethrough`       | Strikethrough text | Text editors, formatting toolbar    | "Strikethrough text"    |
| `subscript`           | Subscript text     | Text editors, scientific notation   | "Make text subscript"   |
| `superscript`         | Superscript text   | Text editors, mathematical notation | "Make text superscript" |
| **Alignment**         |                    |                                     |                         |
| `align-left`          | Left align         | Text editors, alignment controls    | "Align text left"       |
| `align-center`        | Center align       | Text editors, alignment controls    | "Center text"           |
| `align-right`         | Right align        | Text editors, alignment controls    | "Align text right"      |
| `align-justify`       | Justify text       | Text editors, alignment controls    | "Justify text"          |
| **Lists & Structure** |                    |                                     |                         |
| `list-bullet`         | Bullet points      | Text editors, list formatting       | "Create bullet list"    |
| `list-numbered`       | Numbered list      | Text editors, ordered lists         | "Create numbered list"  |
| `indent`              | Increase indent    | Text editors, list nesting          | "Increase indent"       |
| `outdent`             | Decrease indent    | Text editors, list nesting          | "Decrease indent"       |
| `quote`               | Quote/blockquote   | Text editors, quotations            | "Add quote"             |
| **Media & Links**     |                    |                                     |                         |
| `image`               | Insert image       | Text editors, media insertion       | "Insert image"          |
| `video`               | Insert video       | Text editors, media insertion       | "Insert video"          |
| `link`                | Insert link        | Text editors, hyperlink creation    | "Insert link"           |
| `unlink`              | Remove link        | Text editors, hyperlink removal     | "Remove link"           |
| `table`               | Insert table       | Text editors, table creation        | "Insert table"          |
| `code`                | Code block         | Text editors, code formatting       | "Format as code"        |

### Social Media Icons

Platform-specific icons for external connections:

| Icon Name           | Description    | Usage Context                    | ARIA Label Example       |
| ------------------- | -------------- | -------------------------------- | ------------------------ |
| **Major Platforms** |                |                                  |                          |
| `facebook`          | Facebook       | Social media links, sharing      | "Share on Facebook"      |
| `twitter`           | Twitter/X      | Social media links, sharing      | "Share on Twitter"       |
| `instagram`         | Instagram      | Social media links, sharing      | "Follow on Instagram"    |
| `linkedin`          | LinkedIn       | Professional networking, sharing | "Share on LinkedIn"      |
| `youtube`           | YouTube        | Video sharing, channel links     | "Watch on YouTube"       |
| `tiktok`            | TikTok         | Short video sharing              | "Follow on TikTok"       |
| **Messaging**       |                |                                  |                          |
| `whatsapp`          | WhatsApp       | Instant messaging, contact       | "Contact via WhatsApp"   |
| `telegram`          | Telegram       | Secure messaging                 | "Contact via Telegram"   |
| `wechat`            | WeChat         | Messaging platform               | "Connect on WeChat"      |
| **Professional**    |                |                                  |                          |
| `github`            | GitHub         | Code repository, development     | "View on GitHub"         |
| `stackoverflow`     | Stack Overflow | Developer community              | "View on Stack Overflow" |

### Media Icons

File type and document format indicators:

| Icon Name         | Description                      | Usage Context                     | ARIA Label Example        |
| ----------------- | -------------------------------- | --------------------------------- | ------------------------- |
| **Documents**     |                                  |                                   |                           |
| `file-pdf`        | PDF document                     | File upload, document links       | "PDF document"            |
| `file-doc`        | Word document                    | File upload, document links       | "Word document"           |
| `file-docx`       | Word document (modern)           | File upload, document links       | "Word document"           |
| `file-xls`        | Excel spreadsheet                | File upload, data files           | "Excel spreadsheet"       |
| `file-xlsx`       | Excel spreadsheet (modern)       | File upload, data files           | "Excel spreadsheet"       |
| `file-ppt`        | PowerPoint presentation          | File upload, presentation files   | "PowerPoint presentation" |
| `file-pptx`       | PowerPoint presentation (modern) | File upload, presentation files   | "PowerPoint presentation" |
| `file-txt`        | Text file                        | File upload, plain text           | "Text file"               |
| `file-rtf`        | Rich text format                 | File upload, formatted text       | "Rich text document"      |
| **Images**        |                                  |                                   |                           |
| `file-jpg`        | JPEG image                       | File upload, image files          | "JPEG image"              |
| `file-png`        | PNG image                        | File upload, image files          | "PNG image"               |
| `file-gif`        | GIF image                        | File upload, animated images      | "GIF image"               |
| `file-svg`        | SVG vector image                 | File upload, scalable graphics    | "SVG image"               |
| `file-webp`       | WebP image                       | File upload, web-optimized images | "WebP image"              |
| **Audio & Video** |                                  |                                   |                           |
| `file-mp3`        | MP3 audio                        | File upload, audio files          | "MP3 audio"               |
| `file-wav`        | WAV audio                        | File upload, audio files          | "WAV audio"               |
| `file-mp4`        | MP4 video                        | File upload, video files          | "MP4 video"               |
| `file-avi`        | AVI video                        | File upload, video files          | "AVI video"               |
| `file-mov`        | QuickTime video                  | File upload, video files          | "QuickTime video"         |
| **Archives**      |                                  |                                   |                           |
| `file-zip`        | ZIP archive                      | File upload, compressed files     | "ZIP archive"             |
| `file-rar`        | RAR archive                      | File upload, compressed files     | "RAR archive"             |
| `file-7z`         | 7-Zip archive                    | File upload, compressed files     | "7-Zip archive"           |
| **Generic**       |                                  |                                   |                           |
| `file`            | Generic file                     | Unknown file types, general files | "File"                    |
| `folder`          | Folder/directory                 | File organization, navigation     | "Folder"                  |
| `folder-open`     | Open folder                      | Active folder, current directory  | "Open folder"             |

### Agency/Legacy Icons

Government-specific and Malaysian administrative icons:

| Icon Name                 | Description             | Usage Context                       | ARIA Label Example       |
| ------------------------- | ----------------------- | ----------------------------------- | ------------------------ |
| **Malaysian Government**  |                         |                                     |                          |
| `coat-of-arms`            | Malaysian coat of arms  | Official documents, headers         | "Malaysian coat of arms" |
| `flag-malaysia`           | Malaysian flag          | National identity, official pages   | "Malaysian flag"         |
| `parliament`              | Parliament building     | Legislative information             | "Parliament"             |
| `government`              | Government building     | Administrative services             | "Government services"    |
| **Digital Services**      |                         |                                     |                          |
| `mykad`                   | MyKad identity card     | Identity verification, registration | "MyKad"                  |
| `mysejahtera`             | MySejahtera app         | Health services, check-in           | "MySejahtera"            |
| `e-filing`                | Electronic filing       | Tax services, submissions           | "Electronic filing"      |
| `e-services`              | Electronic services     | Digital government services         | "Electronic services"    |
| `digital-signature`       | Digital signature       | Document authentication             | "Digital signature"      |
| **Ministries & Agencies** |                         |                                     |                          |
| `ministry`                | Government ministry     | Ministry services, departments      | "Ministry"               |
| `agency`                  | Government agency       | Agency services, departments        | "Government agency"      |
| `local-council`           | Local government        | Municipal services, local authority | "Local council"          |
| `state-government`        | State government        | State-level services                | "State government"       |
| **Services**              |                         |                                     |                          |
| `license`                 | License/permit          | Licensing services, permits         | "License application"    |
| `tax`                     | Taxation                | Tax services, revenue               | "Tax services"           |
| `healthcare`              | Healthcare services     | Medical services, health ministry   | "Healthcare services"    |
| `education`               | Education services      | Educational resources, schools      | "Education services"     |
| `immigration`             | Immigration services    | Border control, visas               | "Immigration services"   |
| `police`                  | Police services         | Law enforcement, safety             | "Police services"        |
| `fire-department`         | Fire and rescue         | Emergency services, safety          | "Fire and rescue"        |
| `court`                   | Judicial services       | Legal system, courts                | "Court services"         |
| **Legacy Systems**        |                         |                                     |                          |
| `legacy-system`           | Legacy system indicator | Old system integration              | "Legacy system"          |
| `migration`               | System migration        | Data transfer, upgrades             | "System migration"       |
| `compatibility`           | Compatibility mode      | Backward compatibility              | "Compatibility mode"     |

### Usage Notes

#### Accessibility Requirements

- All icons must include appropriate `aria-label` or `aria-labelledby` attributes when conveying meaning
- Use `aria-hidden="true"` for purely decorative icons
- Provide text alternatives for critical information
- Ensure minimum 4.5:1 contrast ratio against backgrounds

#### Implementation Standards

- Always use semantic naming conventions
- Maintain consistent sizing across similar contexts
- Test icons at multiple screen resolutions
- Verify compatibility with assistive technologies

#### Customization Guidelines

- Icons can be styled using CSS `currentColor` for theme consistency
- Stroke width should scale proportionally with icon size
- Maintain visual hierarchy through appropriate sizing
- Consider cultural context when selecting icons for Malaysian users

For the most up-to-date icon library and additional icons, always reference the official MYDS documentation and Figma design kit.

## Colour Reference

This appendix contains the full colour reference used across the project. It mirrors the `MYDS-Colour-Reference.md` content so agents can consult colours directly from the instruction file.

### Colour Reference List

This document lists all specified colours, organized by category, usage, and mode (Light/Dark). Each entry includes the name, variable, and associated shade/code.

This system uses two layers of tokens:

1. **Primitive Tokens**: Foundational color values (e.g., `primary-600`, `#2563EB`). These are the raw color swatches.
2. **Semantic Tokens**: Tokens that describe a color's purpose (e.g., `bg-primary-600`, `txt-primary`). These semantic tokens map to different primitive tokens depending on the active theme (Light or Dark).

_Citations: Token structure and mapping confirmed by reference images and design system visual guides._

---

## White & Neutral Backgrounds

### White & Neutral Backgrounds – Light Mode

| Name           | Variable            | Shade/Code     | HEX     | Notes |
| -------------- | ------------------- | -------------- | ------- | ----- |
| White          | `bg-white`          | white          | #FFFFFF |       |
| White Hover    | `bg-white-hover`    | gray-50        | #FAFAFA |       |
| White Disabled | `bg-white-disabled` | gray-100 (40%) | #F4F4F5 |       |
| Washed         | `bg-washed`         | gray-100       | #F4F4F5 |       |
| Washed Active  | `bg-washed-active`  | gray-100       | #F4F4F5 |       |
| Contrast       | `bg-contrast`       | white          | #FFFFFF |       |
| Dialog         | `bg-dialog`         | white          | #FFFFFF |       |
| Dialog Active  | `bg-dialog-active`  | white          | #FFFFFF |       |
| Gray 50        | `bg-gray-50`        | gray-50        | #FAFAFA |       |

#### White & Neutral Backgrounds – Dark Mode

| Name           | Variable            | Shade/Code     | HEX     | Notes |
| -------------- | ------------------- | -------------- | ------- | ----- |
| White          | `bg-white`          | gray-900       | #18181B |       |
| White Hover    | `bg-white-hover`    | gray-800       | #27272A |       |
| White Disabled | `bg-white-disabled` | gray-800 (40%) | #27272A |       |
| Washed         | `bg-washed`         | gray-850       | #1D1D21 |       |
| Washed Active  | `bg-washed-active`  | gray-800       | #27272A |       |
| Contrast       | `bg-contrast`       | gray-930       | #161619 |       |
| Dialog         | `bg-dialog`         | gray-850       | #1D1D21 |       |
| Dialog Active  | `bg-dialog-active`  | gray-800       | #27272A |       |
| Gray 50        | `bg-gray-50`        | gray-930       | #161619 |       |

---

## Primitive Gray Scale

This is the foundational gray palette.

### Primitive Gray Scale – Light Mode

| Name     | Variable   | Shade/Code | HEX     |
| :------- | :--------- | :--------- | :------ |
| Gray 50  | `gray-50`  | gray-50    | #FAFAFA |
| Gray 100 | `gray-100` | gray-100   | #F4F4F5 |
| Gray 200 | `gray-200` | gray-200   | #E4E4E7 |
| Gray 300 | `gray-300` | gray-300   | #D4D4D8 |
| Gray 400 | `gray-400` | gray-400   | #A1A1AA |
| Gray 500 | `gray-500` | gray-500   | #71717A |
| Gray 600 | `gray-600` | gray-600   | #52525B |
| Gray 700 | `gray-700` | gray-700   | #3F3F46 |
| Gray 800 | `gray-800` | gray-800   | #27272A |
| Gray 850 | `gray-850` | gray-850   | #1D1D21 |
| Gray 900 | `gray-900` | gray-900   | #18181B |
| Gray 930 | `gray-930` | gray-930   | #161619 |
| Gray 950 | `gray-950` | gray-950   | #09090B |

#### Primitive Gray Scale – Dark Mode

This table shows how the primitive gray tokens are re-mapped in dark mode. For instance, requesting `gray-100` in dark mode will return the hex code for `gray-900`.

| Name     | Light Mode Variable | Dark Mode Maps To | HEX     |
| :------- | :------------------ | :---------------- | :------ |
| Gray 50  | `gray-50`           | gray-950          | #09090B |
| Gray 100 | `gray-100`          | gray-900          | #18181B |
| Gray 200 | `gray-200`          | gray-800          | #27272A |
| Gray 300 | `gray-300`          | gray-700          | #3F3F46 |
| Gray 400 | `gray-400`          | gray-600          | #52525B |
| Gray 500 | `gray-500`          | gray-500          | #71717A |
| Gray 600 | `gray-600`          | gray-400          | #A1A1AA |
| Gray 700 | `gray-700`          | gray-300          | #D4D4D8 |
| Gray 800 | `gray-800`          | gray-200          | #E4E4E7 |
| Gray 850 | `gray-850`          | gray-850          | #1D1D21 |
| Gray 930 | `gray-930`          | gray-930          | #161619 |

## Semantic Black Backgrounds

These tokens are used for neutral backgrounds throughout the UI.

### Semantic Black Backgrounds – Light Mode

| Name      | Variable       | Maps to Shade |
| :-------- | :------------- | :------------ |
| Black 50  | `bg-black-50`  | gray-50       |
| Black 100 | `bg-black-100` | gray-100      |
| Black 200 | `bg-black-200` | gray-200      |
| Black 300 | `bg-black-300` | gray-300      |
| Black 400 | `bg-black-400` | gray-400      |
| Black 500 | `bg-black-500` | gray-500      |
| Black 600 | `bg-black-600` | gray-600      |
| Black 700 | `bg-black-700` | gray-700      |
| Black 800 | `bg-black-800` | gray-800      |
| Black 900 | `bg-black-900` | gray-900      |
| Black 950 | `bg-black-950` | gray-950      |

#### Semantic Black Backgrounds – Dark Mode

| Name      | Variable       | Maps to Shade |
| :-------- | :------------- | :------------ |
| Black 50  | `bg-black-50`  | gray-950      |
| Black 100 | `bg-black-100` | gray-900      |
| Black 200 | `bg-black-200` | gray-800      |
| Black 300 | `bg-black-300` | gray-700      |
| Black 400 | `bg-black-400` | gray-600      |
| Black 500 | `bg-black-500` | gray-500      |
| Black 600 | `bg-black-600` | gray-400      |
| Black 700 | `bg-black-700` | gray-300      |
| Black 800 | `bg-black-800` | gray-200      |
| Black 900 | `bg-black-900` | white         |
| Black 950 | `bg-black-950` | white         |

---

## Primary Colour Scale

### Primary Colour Primitive Scale – Light Mode

| Name        | Variable      | Shade/Code  | HEX     |
| :---------- | :------------ | :---------- | :------ |
| Primary 50  | `primary-50`  | primary-50  | #EFF6FF |
| Primary 100 | `primary-100` | primary-100 | #DBEAFE |
| Primary 200 | `primary-200` | primary-200 | #C2D5FF |
| Primary 300 | `primary-300` | primary-300 | #96B7FF |
| Primary 400 | `primary-400` | primary-400 | #6394FF |
| Primary 500 | `primary-500` | primary-500 | #3A75F6 |
| Primary 600 | `primary-600` | primary-600 | #2563EB |
| Primary 700 | `primary-700` | primary-700 | #1D4ED8 |
| Primary 800 | `primary-800` | primary-800 | #1E40AF |
| Primary 900 | `primary-900` | primary-900 | #1E3A8A |
| Primary 950 | `primary-950` | primary-950 | #172554 |

#### Primary Colour Primitive Scale – Dark Mode

| Name        | Light Mode Variable | Dark Mode Maps To | HEX     |
| :---------- | :------------------ | :---------------- | :------ |
| Primary 50  | `primary-50`        | primary-950       | #172554 |
| Primary 100 | `primary-100`       | primary-900       | #1E3A8A |
| Primary 200 | `primary-200`       | primary-800       | #1E40AF |
| Primary 300 | `primary-300`       | primary-700       | #1D4ED8 |
| Primary 400 | `primary-400`       | primary-600       | #2563EB |
| Primary 500 | `primary-500`       | primary-500       | #3A75F6 |
| Primary 600 | `primary-600`       | primary-400       | #6394FF |
| Primary 700 | `primary-700`       | primary-300       | #96B7FF |
| Primary 800 | `primary-800`       | primary-200       | #C2D5FF |
| Primary 900 | `primary-900`       | primary-100       | #DBEAFE |
| Primary 950 | `primary-950`       | primary-50        | #EFF6FF |

### Primary Colour Semantic Backgrounds

| Name        | Variable         | Light Mode Shade | Dark Mode Shade |
| :---------- | :--------------- | :--------------- | :-------------- |
| Primary 50  | `bg-primary-50`  | primary-50       | primary-950     |
| Primary 100 | `bg-primary-100` | primary-100      | primary-900     |
| Primary 200 | `bg-primary-200` | primary-200      | primary-800     |
| Primary 300 | `bg-primary-300` | primary-300      | primary-700     |
| Primary 400 | `bg-primary-400` | primary-400      | primary-600     |
| Primary 500 | `bg-primary-500` | primary-500      | primary-500     |
| Primary 600 | `bg-primary-600` | primary-600      | primary-400     |
| Primary 700 | `bg-primary-700` | primary-700      | primary-300     |
| Primary 800 | `bg-primary-800` | primary-800      | primary-200     |
| Primary 900 | `bg-primary-900` | primary-900      | primary-100     |
| Primary 950 | `bg-primary-950` | primary-950      | primary-50      |

---

## Danger Colour Scale

### Danger Colour Scale – Light Mode

| Name       | Variable     | Shade/Code | HEX     |
| ---------- | ------------ | ---------- | ------- |
| Danger 50  | `danger-50`  | danger-50  | #FEF2F2 |
| Danger 100 | `danger-100` | danger-100 | #FEE2E2 |
| Danger 200 | `danger-200` | danger-200 | #FECACA |
| Danger 300 | `danger-300` | danger-300 | #FCA5A5 |
| Danger 400 | `danger-400` | danger-400 | #F87171 |
| Danger 500 | `danger-500` | danger-500 | #EF4444 |
| Danger 600 | `danger-600` | danger-600 | #DC2626 |
| Danger 700 | `danger-700` | danger-700 | #B91C1C |
| Danger 800 | `danger-800` | danger-800 | #991B1B |
| Danger 900 | `danger-900` | danger-900 | #7F1D1D |
| Danger 950 | `danger-950` | danger-950 | #450A0A |

#### Danger Colour Scale – Dark Mode

| Name       | Variable     | Shade/Code | HEX     |
| ---------- | ------------ | ---------- | ------- |
| Danger 50  | `danger-950` | danger-950 | #450A0A |
| Danger 100 | `danger-900` | danger-900 | #7F1D1D |
| Danger 200 | `danger-800` | danger-800 | #991B1B |
| Danger 300 | `danger-700` | danger-700 | #B91C1C |
| Danger 400 | `danger-600` | danger-600 | #DC2626 |
| Danger 500 | `danger-500` | danger-500 | #EF4444 |
| Danger 600 | `danger-400` | danger-400 | #F87171 |
| Danger 700 | `danger-300` | danger-300 | #FCA5A5 |
| Danger 800 | `danger-200` | danger-200 | #FECACA |
| Danger 900 | `danger-100` | danger-100 | #FEE2E2 |
| Danger 950 | `danger-50`  | danger-50  | #FEF2F2 |

---

## Success Colour Scale

### Success Colour Primitive Scale – Light Mode

| Name        | Variable      | Shade/Code  | HEX     |
| :---------- | :------------ | :---------- | :------ |
| Success 50  | `success-50`  | success-50  | #F0FDF4 |
| Success 100 | `success-100` | success-100 | #DCFCE7 |
| Success 200 | `success-200` | success-200 | #BBF7D0 |
| Success 300 | `success-300` | success-300 | #83DAA3 |
| Success 400 | `success-400` | success-400 | #4ADE80 |
| Success 500 | `success-500` | success-500 | #22C55E |
| Success 600 | `success-600` | success-600 | #16A34A |
| Success 700 | `success-700` | success-700 | #15803D |
| Success 800 | `success-800` | success-800 | #166534 |
| Success 900 | `success-900` | success-900 | #14532D |
| Success 950 | `success-950` | success-950 | #052E16 |

#### Success Colour Primitive Scale – Dark Mode

| Name        | Light Mode Variable | Dark Mode Maps To | HEX     |
| :---------- | :------------------ | :---------------- | :------ |
| Success 50  | `success-50`        | success-950       | #052E16 |
| Success 100 | `success-100`       | success-900       | #14532D |
| Success 200 | `success-200`       | success-800       | #166534 |
| Success 300 | `success-300`       | success-700       | #15803D |
| Success 400 | `success-400`       | success-600       | #16A34A |
| Success 500 | `success-500`       | success-500       | #22C55E |
| Success 600 | `success-600`       | success-400       | #4ADE80 |
| Success 700 | `success-700`       | success-300       | #83DAA3 |
| Success 800 | `success-800`       | success-200       | #BBF7D0 |
| Success 900 | `success-900`       | success-100       | #DCFCE7 |
| Success 950 | `success-950`       | success-50        | #F0FDF4 |

### Success Colour Semantic Backgrounds

| Name        | Variable         | Light Mode Shade | Dark Mode Shade |
| :---------- | :--------------- | :--------------- | :-------------- |
| Success 50  | `bg-success-50`  | success-50       | success-950     |
| Success 100 | `bg-success-100` | success-100      | success-900     |
| Success 200 | `bg-success-200` | success-200      | success-800     |
| Success 300 | `bg-success-300` | success-300      | success-700     |
| Success 400 | `bg-success-400` | success-400      | success-600     |
| Success 500 | `bg-success-500` | success-500      | success-500     |
| Success 600 | `bg-success-600` | success-600      | success-400     |
| Success 700 | `bg-success-700` | success-700      | success-300     |
| Success 800 | `bg-success-800` | success-800      | success-200     |
| Success 900 | `bg-success-900` | success-900      | success-100     |
| Success 950 | `bg-success-950` | success-950      | success-50      |

_Citations: Success semantic background tokens confirmed by bg-token-6.png and bg-token-6-dark.png images._

---

## Warning Colour Scale

### Warning Colour Primitive Scale – Light Mode

| Name        | Variable      | Shade/Code  | HEX     |
| :---------- | :------------ | :---------- | :------ |
| Warning 50  | `warning-50`  | warning-50  | #FEFCE8 |
| Warning 100 | `warning-100` | warning-100 | #FEF9C3 |
| Warning 200 | `warning-200` | warning-200 | #FEF08A |
| Warning 300 | `warning-300` | warning-300 | #FDE047 |
| Warning 400 | `warning-400` | warning-400 | #FACC15 |
| Warning 500 | `warning-500` | warning-500 | #EAB308 |
| Warning 600 | `warning-600` | warning-600 | #CA8A04 |
| Warning 700 | `warning-700` | warning-700 | #A16207 |
| Warning 800 | `warning-800` | warning-800 | #854D0E |
| Warning 900 | `warning-900` | warning-900 | #713F12 |
| Warning 950 | `warning-950` | warning-950 | #422006 |

#### Warning Colour Primitive Scale – Dark Mode

| Name        | Light Mode Variable | Dark Mode Maps To | HEX     |
| :---------- | :------------------ | :---------------- | :------ |
| Warning 50  | `warning-50`        | warning-950       | #422006 |
| Warning 100 | `warning-100`       | warning-900       | #713F12 |
| Warning 200 | `warning-200`       | warning-800       | #854D0E |
| Warning 300 | `warning-300`       | warning-700       | #A16207 |
| Warning 400 | `warning-400`       | warning-600       | #CA8A04 |
| Warning 500 | `warning-500`       | warning-500       | #EAB308 |
| Warning 600 | `warning-600`       | warning-400       | #FACC15 |
| Warning 700 | `warning-700`       | warning-300       | #FDE047 |
| Warning 800 | `warning-800`       | warning-200       | #FEF08A |
| Warning 900 | `warning-900`       | warning-100       | #FEF9C3 |
| Warning 950 | `warning-950`       | warning-50        | #FEFCE8 |

### Warning Colour Semantic Backgrounds

| Name        | Variable         | Light Mode Shade | Dark Mode Shade |
| :---------- | :--------------- | :--------------- | :-------------- |
| Warning 50  | `bg-warning-50`  | warning-50       | warning-950     |
| Warning 100 | `bg-warning-100` | warning-100      | warning-900     |
| Warning 200 | `bg-warning-200` | warning-200      | warning-800     |
| Warning 300 | `bg-warning-300` | warning-300      | warning-700     |
| Warning 400 | `bg-warning-400` | warning-400      | warning-600     |
| Warning 500 | `bg-warning-500` | warning-500      | warning-500     |
| Warning 600 | `bg-warning-600` | warning-600      | warning-400     |
| Warning 700 | `bg-warning-700` | warning-700      | warning-300     |
| Warning 800 | `bg-warning-800` | warning-800      | warning-200     |
| Warning 900 | `bg-warning-900` | warning-900      | warning-100     |
| Warning 950 | `bg-warning-950` | warning-950      | warning-50      |

_Citations: Warning semantic background tokens confirmed by bg-token-7.png and bg-token-7-dark.png images. Typo corrected to use bg-warning-400._

---

## Disabled State Colours

### Disabled State Colours – Light Mode

| Name             | Variable              | Shade/Code     | Notes |
| ---------------- | --------------------- | -------------- | ----- |
| Primary Disabled | `bg-primary-disabled` | primary-200    |       |
| Danger Disabled  | `bg-danger-disabled`  | danger-200     |       |
| Success Disabled | `bg-success-disabled` | success-200    |       |
| Warning Disabled | `bg-warning-disabled` | warning-200    |       |
| Black Disabled   | `bg-black-disabled`   | gray-900 (40%) |       |

#### Disabled State Colours – Dark Mode

| Name             | Variable              | Shade/Code  | Notes |
| ---------------- | --------------------- | ----------- | ----- |
| Primary Disabled | `bg-primary-disabled` | primary-950 |       |
| Danger Disabled  | `bg-danger-disabled`  | danger-950  |       |
| Success Disabled | `bg-success-disabled` | success-950 |       |
| Warning Disabled | `bg-warning-disabled` | warning-950 |       |
| Black Disabled   | `bg-black-disabled`   | white (40%) |       |

---

## Primitive Colours & Usage

Primitive colours are the foundational colour values used in the design system.  
Below are examples of how primitive colours map to UI roles and variables.

| Colour  | Shade     | HEX Code | Variable          | Usage/Example               |
| ------- | --------- | -------- | ----------------- | --------------------------- |
| Primary | 600       | #2563EB  | `primary-600`     | bg-primary-600 (background) |
| Primary | 600       | #2563EB  | `txt-primary`     | Text                        |
| Primary | 300       | #96B7FF  | `otl-primary-300` | Outline                     |
| Primary | 300 (40%) | #96B7FF  | `fr-primary`      | Focus ring                  |
| Danger  | 300 (40%) | #FCA5A5  | `fr-danger`       | Focus ring                  |

---

## Outline Colours

Outline colours are used for borders and dividers in the UI.

_Citations: Outline token structure confirmed by reference images._

### Outline Colours – Light Mode

| Name             | Variable               | Shade/Code        | HEX     | Usage              |
| ---------------- | ---------------------- | ----------------- | ------- | ------------------ |
| Divider          | `otl-divider`          | gray-100          | #F4F4F5 | Divider            |
| Gray 200         | `otl-gray-200`         | gray-200          | #E4E4E7 | Outline            |
| Gray 300         | `otl-gray-300`         | gray-300          | #D4D4D8 | Outline            |
| Primary 200      | `otl-primary-200`      | primary-200       | #C2D5FF | Outline            |
| Primary 300      | `otl-primary-300`      | primary-300       | #96B7FF | Outline            |
| Primary Disabled | `otl-primary-disabled` | primary-200 (40%) | #C2D5FF | Outline (disabled) |
| Danger 200       | `otl-danger-200`       | danger-200        | #FECACA | Outline            |
| Danger 300       | `otl-danger-300`       | danger-300        | #FCA5A5 | Outline            |
| Danger Disabled  | `otl-danger-disabled`  | danger-200 (40%)  | #FECACA | Outline (disabled) |
| Success 200      | `otl-success-200`      | success-200       | #BBF7D0 | Outline            |
| Success 300      | `otl-success-300`      | success-300       | #83DAA3 | Outline            |
| Success Disabled | `otl-success-disabled` | success-200 (40%) | #BBF7D0 | Outline (disabled) |
| Warning 200      | `otl-warning-200`      | warning-200       | #FEF08A | Outline            |
| Warning 300      | `otl-warning-300`      | warning-300       | #FDE047 | Outline            |
| Warning Disabled | `otl-warning-disabled` | warning-200 (40%) | #FEF08A | Outline (disabled) |

#### Outline Colours – Dark Mode

| Name             | Variable               | Shade/Code        | HEX     | Usage              |
| ---------------- | ---------------------- | ----------------- | ------- | ------------------ |
| Divider          | `otl-divider`          | gray-850          | #1D1D21 | Divider            |
| Gray 200         | `otl-gray-200`         | gray-800          | #27272A | Outline            |
| Gray 300         | `otl-gray-300`         | gray-700          | #3F3F46 | Outline            |
| Primary 200      | `otl-primary-200`      | primary-800       | #1E40AF | Outline            |
| Primary 300      | `otl-primary-300`      | primary-700       | #1D4ED8 | Outline            |
| Primary Disabled | `otl-primary-disabled` | primary-800 (40%) | #1E40AF | Outline (disabled) |
| Danger 200       | `otl-danger-200`       | danger-800        | #991B1B | Outline            |
| Danger 300       | `otl-danger-300`       | danger-700        | #B91C1C | Outline            |
| Danger Disabled  | `otl-danger-disabled`  | danger-800 (40%)  | #991B1B | Outline (disabled) |
| Success 200      | `otl-success-200`      | success-800       | #166534 | Outline            |
| Success 300      | `otl-success-300`      | success-700       | #15803D | Outline            |
| Success Disabled | `otl-success-disabled` | success-800 (40%) | #166534 | Outline (disabled) |
| Warning 200      | `otl-warning-200`      | warning-800       | #854D0E | Outline            |
| Warning 300      | `otl-warning-300`      | warning-700       | #A16207 | Outline            |
| Warning Disabled | `otl-warning-disabled` | warning-800 (40%) | #854D0E | Outline (disabled) |

---

## Focus Ring Colours

Focus ring colours are used to indicate element focus (accessibility/UI feedback).

_Citations: Focus ring token structure confirmed by reference images._

| Name    | Variable     | Shade/Code        | HEX     | Notes                          |
| ------- | ------------ | ----------------- | ------- | ------------------------------ |
| Primary | `fr-primary` | primary-300 (40%) | #96B7FF | Focus ring colour (light mode) |
| Primary | `fr-primary` | primary-700 (40%) | #1D4ED8 | Focus ring colour (dark mode)  |
| Danger  | `fr-danger`  | danger-300 (40%)  | #FCA5A5 | Focus ring colour (light mode) |
| Danger  | `fr-danger`  | danger-700 (40%)  | #B91C1C | Focus ring colour (dark mode)  |

---

## Colour HEX Reference

This section documents the hex codes for each major colour scale for quick copy-paste/reference.  
If you use these variables in CSS, you can reference either the variable name or the hex code.

### Primary Colour Scale – HEX Reference

| Shade | HEX     |
| ----- | ------- |
| 50    | #EFF6FF |
| 100   | #DBEAFE |
| 200   | #C2D5FF |
| 300   | #96B7FF |
| 400   | #6394FF |
| 500   | #3A75F6 |
| 600   | #2563EB |
| 700   | #1D4ED8 |
| 800   | #1E40AF |
| 900   | #1E3A8A |
| 950   | #172554 |

### Danger Colour Scale – HEX Reference

| Shade | HEX     |
| ----- | ------- |
| 50    | #FEF2F2 |
| 100   | #FEE2E2 |
| 200   | #FECACA |
| 300   | #FCA5A5 |
| 400   | #F87171 |
| 500   | #EF4444 |
| 600   | #DC2626 |
| 700   | #B91C1C |
| 800   | #991B1B |
| 900   | #7F1D1D |
| 950   | #450A0A |

### Success Colour Scale – HEX Reference

| Shade | HEX     |
| ----- | ------- |
| 50    | #F0FDF4 |
| 100   | #DCFCE7 |
| 200   | #BBF7D0 |
| 300   | #83DAA3 |
| 400   | #4ADE80 |
| 500   | #22C55E |
| 600   | #16A34A |
| 700   | #15803D |
| 800   | #166534 |
| 900   | #14532D |
| 950   | #052E16 |

### Warning Colour Scale – HEX Reference

| Shade | HEX     |
| ----- | ------- |
| 50    | #FEFCE8 |
| 100   | #FEF9C3 |
| 200   | #FEF08A |
| 300   | #FDE047 |
| 400   | #FACC15 |
| 500   | #EAB308 |
| 600   | #CA8A04 |
| 700   | #A16207 |
| 800   | #854D0E |
| 900   | #713F12 |
| 950   | #422006 |

### Gray Colour Scale – HEX Reference

| Shade | HEX     |
| ----- | ------- |
| 50    | #FAFAFA |
| 100   | #F4F4F5 |
| 200   | #E4E4E7 |
| 300   | #D4D4D8 |
| 400   | #A1A1AA |
| 500   | #71717A |
| 600   | #52525B |
| 700   | #3F3F46 |
| 800   | #27272A |
| 850   | #1D1D21 |
| 900   | #18181B |
| 930   | #161619 |
| 950   | #09090B |

---

## Text Colours

Text colour variables for white, disabled white, black/gray, and theme accent text.

### Text Colours – Light Mode

| Name             | Variable               | Shade/Code        | HEX     | Usage    |
| ---------------- | ---------------------- | ----------------- | ------- | -------- |
| White            | `txt-white`            | white             | #FFFFFF | Text     |
| White Disabled   | `txt-white-disabled`   | white (40%)       | #FFFFFF | Disabled |
| Black 900        | `txt-black-900`        | gray-900          | #18181B | Text     |
| Black 700        | `txt-black-700`        | gray-700          | #3F3F46 | Text     |
| Black 500        | `txt-black-500`        | gray-500          | #71717A | Text     |
| Primary          | `txt-primary`          | primary-600       | #2563EB | Text     |
| Danger           | `txt-danger`           | danger-600        | #DC2626 | Text     |
| Success          | `txt-success`          | success-700       | #15803D | Text     |
| Warning          | `txt-warning`          | warning-700       | #A16207 | Text     |
| Primary Disabled | `txt-primary-disabled` | primary-600 (40%) | #2563EB | Disabled |
| Danger Disabled  | `txt-danger-disabled`  | danger-600 (40%)  | #DC2626 | Disabled |
| Success Disabled | `txt-success-disabled` | success-700 (40%) | #15803D | Disabled |
| Warning Disabled | `txt-warning-disabled` | warning-700 (40%) | #A16207 | Disabled |
| Black Disabled   | `txt-black-disabled`   | gray-600 (20%)    | #52525B | Disabled |

#### Text Colours – Dark Mode

| Name             | Variable               | Shade/Code        | HEX     | Usage    |
| ---------------- | ---------------------- | ----------------- | ------- | -------- |
| White            | `txt-white`            | black-900         | #18181B | Text     |
| White Disabled   | `txt-white-disabled`   | white (40%)       | #FFFFFF | Disabled |
| Black 900        | `txt-black-900`        | white             | #FFFFFF | Text     |
| Black 700        | `txt-black-700`        | gray-300          | #D4D4D8 | Text     |
| Black 500        | `txt-black-500`        | gray-400          | #A1A1AA | Text     |
| Primary          | `txt-primary`          | primary-400       | #6394FF | Text     |
| Danger           | `txt-danger`           | danger-400        | #F87171 | Text     |
| Success          | `txt-success`          | success-500       | #22C55E | Text     |
| Warning          | `txt-warning`          | warning-500       | #EAB308 | Text     |
| Primary Disabled | `txt-primary-disabled` | primary-400 (40%) | #6394FF | Disabled |
| Danger Disabled  | `txt-danger-disabled`  | danger-400 (40%)  | #F87171 | Disabled |
| Success Disabled | `txt-success-disabled` | success-500 (40%) | #22C55E | Disabled |
| Warning Disabled | `txt-warning-disabled` | warning-500 (40%) | #EAB308 | Disabled |
| Black Disabled   | `txt-black-disabled`   | gray-400 (40%)    | #A1A1AA | Disabled |

---

# MYDS Icons Overview

This document provides a comprehensive reference and guidance for all icons in the Malaysia Government Design System (MYDS). It covers icon types, design rules, accessibility, integration, best practices, and a complete list of available icons grouped by category.

---

## 1. Introduction

Icons in MYDS are designed to communicate meaning quickly, aid navigation, clarify actions, and support accessibility for all Malaysians. Every icon adheres to MYDS and MyGovEA principles: citizen-centricity, inclusivity, clarity, and technical consistency.

---

## 2. Icon Types & Groups

MYDS icons are organized into the following main groups:

| Group             | Description / Typical Usage                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| **Generic**       | Common UI actions and system controls (search, add, edit, delete, settings, etc.)     |
| **WYSIWYG**       | Content formatting tools for text editors (bold, italic, underline, lists, etc.)      |
| **Social Media**  | Official social platform logos (Facebook, Instagram, LinkedIn, YouTube, etc.)         |
| **Media**         | File type indicators (PDF, Word, Excel, PowerPoint, etc.)                             |
| **Agency/Legacy** | Government, department, and legacy symbols (malaysia-flag, jata-negara, agency icons) |

---

## 3. Icon Design Guidelines

- **Grid Size:** All icons are drawn on a 20×20px grid for pixel-perfect alignment.
- **Stroke Width:** Standard stroke width is 1.5px at base size. Strokes scale proportionally for other sizes.
- **Sizes:** Recommended:
  - 16×16px (small buttons)
  - 20×20px (medium buttons, default)
  - 24×24px (large buttons)
  - 32×32px, 42×42px (alerts/dialogs)
- **Variants:** Outline (stroke only) and Filled (solid).
- **Format:** SVG, with clear, scalable paths.
- **Visual Consistency:** Icons should be visually balanced, clear at all sizes, and easily recognizable.

---

## 4. Accessibility & Usage Best Practices

- **Pair with text:** Icons must not be the sole indicator of status/action. Always pair with labels or tooltips.
- **ARIA:** For interactive icons, use `aria-label` or descriptive text.
- **Contrast:** Ensure icons meet at least 4.5:1 contrast ratio (WCAG AA).
- **Keyboard navigation:** All interactive icons must be focusable and operable via keyboard.
- **Do not use color alone:** Use shape or text for status, not color-only.
- **Consistent meaning:** Use standard iconography for common actions.

---

## 5. Integration

- **React:** Import from `@govtechmy/myds-react/icon` (e.g., `import { SearchIcon } from "@govtechmy/myds-react/icon";`)
- **Figma:** Official Figma Kit contains all icons for design teams.
- **SVG:** Download and use SVG directly for any framework.

---

## 6. Icon Reference List (Grouped)

Below is the complete list of MYDS icons grouped by category.  
_Note: Icon names are case-sensitive and match their official SVG/component names._

### 6.1 Generic Icons

| Icon Name           | Notes / Usage                |
| ------------------- | ---------------------------- |
| malaysia-flag       | Malaysia flag                |
| jata-negara         | National emblem              |
| hamburger-menu      | Navigation menu              |
| sun                 | Theme (light)                |
| moon                | Theme (dark)                 |
| home                | Homepage                     |
| search              | Search functions             |
| bell                | Notifications                |
| user                | User profile                 |
| user-group          | Group of users               |
| edit                | Edit action                  |
| trash               | Delete/remove                |
| plus                | Add/create                   |
| plus-circle         | Add (circle background)      |
| zoom-in             | Zoom in                      |
| minus               | Subtract/remove              |
| minus-circle        | Subtract (circle background) |
| zoom-out            | Zoom out                     |
| table               | Table/grid                   |
| grid                | Grid view                    |
| list                | List view                    |
| upload              | Upload file                  |
| download            | Download file                |
| check               | Confirm/select               |
| check-circle        | Confirm (circle)             |
| cross               | Cancel/close                 |
| cross-circle        | Cancel (circle)              |
| govt-office         | Government office            |
| putrajaya           | Putrajaya city               |
| lock                | Locked                       |
| lock-2              | Alternative lock icon        |
| expand              | Expand/collapse              |
| flag                | Flag                         |
| thumbs-up           | Like/upvote                  |
| thumbs-down         | Dislike/downvote             |
| cursor              | Pointer/cursor               |
| accessible          | Accessibility indicator      |
| heart               | Favorite/like                |
| component           | Components                   |
| copy                | Copy to clipboard            |
| duplicate           | Duplicate/clone              |
| link                | Link/hyperlink               |
| link-diagonal       | External link                |
| eye-show            | Show/reveal                  |
| eye-hide            | Hide/conceal                 |
| ellipsis            | More options (horizontal)    |
| ellipsis-vertical   | More options (vertical)      |
| calendar            | Calendar/date                |
| clock               | Time                         |
| filter              | Filter                       |
| filter-desc         | Descending filter            |
| filter-asc          | Ascending filter             |
| map                 | Map/location                 |
| direction           | Directions                   |
| pin                 | Pin/location marker          |
| warning             | Warning/alert                |
| warning-diamond     | Warning (diamond shape)      |
| warning-circle      | Warning (circle shape)       |
| info                | Information                  |
| question-circle     | Help/question                |
| printer             | Print                        |
| book                | Book/manual                  |
| globe               | Global/world                 |
| money               | Money/currency               |
| qr-code             | QR code                      |
| share               | Share                        |
| folder              | Folder                       |
| folder-plus         | Add folder                   |
| folder-minus        | Remove folder                |
| document-filled     | Filled document              |
| document            | Outline document             |
| document-add        | Add document                 |
| document-minus      | Remove document              |
| excel               | Excel file                   |
| pdf                 | PDF file                     |
| word                | Word file                    |
| attachment          | File attachment              |
| play                | Play media                   |
| pause               | Pause media                  |
| email               | Email/message                |
| phone               | Phone/call                   |
| mobile              | Mobile device                |
| tablet              | Tablet device                |
| desktop             | Desktop device               |
| bolt                | Lightning/flash              |
| setting             | Settings/configuration       |
| chat-bubble         | Chat/message                 |
| chevron-right       | Next/right navigation        |
| chevron-left        | Previous/left navigation     |
| chevron-down        | Down navigation/expand       |
| chevron-up          | Up navigation/collapse       |
| column-expand       | Expand table column          |
| column-collapse     | Collapse table column        |
| arrow-up            | Arrow up                     |
| arrow-down          | Arrow down                   |
| arrow-incoming      | Incoming arrow               |
| arrow-outgoing      | Outgoing arrow               |
| arrow-back          | Back arrow                   |
| arrow-forward       | Forward arrow                |
| arrow-forward-close | Forward with close           |
| arrow-back-close    | Back with close              |
| undo                | Undo action                  |
| redo                | Redo action                  |
| logout              | Logout/session end           |
| drop-arrow-down     | Dropdown arrow               |
| check-shield        | Verified/secure              |
| check-star          | Starred/important            |
| trophy              | Achievement/trophy           |
| star                | Favorite/star                |
| swap                | Swap/exchange                |
| reload              | Reload/refresh               |
| megaphone           | Announcement                 |
| section             | Section divider              |
| text                | Text input                   |
| button              | Button                       |
| gallery             | Gallery/photos               |
| carousel            | Carousel/slider              |
| video               | Video/media                  |
| forms               | Forms                        |
| input-field         | Input field                  |
| database            | Database/server              |
| org-chart           | Organization chart           |

#### Filled Generic Icons (Suffix `-fill`)

| Icon Name          | Notes / Usage        |
| ------------------ | -------------------- |
| chevron-down-fill  | Filled chevron down  |
| chevron-right-fill | Filled chevron right |
| chevron-left-fill  | Filled chevron left  |
| chevron-up-fill    | Filled chevron up    |
| warning-fill       | Filled warning       |
| check-circle-fill  | Filled check circle  |
| lock-fill          | Filled lock          |
| star-fill          | Filled star          |
| cross-fill         | Filled cross         |

---

### 6.2 WYSIWYG Icons

| Icon Name     | Notes / Usage      |
| ------------- | ------------------ |
| font          | Font style         |
| bold          | Bold text          |
| italic        | Italic text        |
| underline     | Underline text     |
| strikethrough | Strikethrough text |
| link          | Insert link        |
| unlink        | Remove link        |
| numbered-list | Numbered list      |
| bulleted-list | Bulleted list      |
| align-left    | Align left         |
| align-center  | Align center       |
| align-right   | Align right        |
| align-justify | Justify text       |
| reset-style   | Reset formatting   |

---

### 6.3 Social Media Icons

| Icon Name | Notes / Usage        |
| --------- | -------------------- |
| rss       | RSS feed             |
| facebook  | Facebook             |
| x         | X (formerly Twitter) |
| linkedin  | LinkedIn             |
| instagram | Instagram            |
| youtube   | YouTube              |
| whatsapp  | WhatsApp             |
| tiktok    | TikTok               |
| figma     | Figma                |
| telegram  | Telegram             |
| github    | GitHub               |
| google    | Google               |

---

### 6.4 Media/File Type Icons

| Icon Name        | Notes / Usage   |
| ---------------- | --------------- |
| powerpoint-media | PowerPoint file |
| excel-media      | Excel file      |
| word-media       | Word document   |
| pdf-media        | PDF file        |

---

### 6.5 Agency/Legacy Icons

| Icon Name                  | Notes / Usage                         |
| -------------------------- | ------------------------------------- |
| dosm                       | Department of Statistics              |
| identity-jpn               | National Registration Department      |
| car-jpj                    | Road Transport Department             |
| book-moe                   | Ministry of Education                 |
| internet-mcmc              | MCMC (Communications & Multimedia)    |
| money-kwap                 | KWAP (Retirement Fund)                |
| helmet-jpa                 | JPA (Public Service Department)       |
| train-mot                  | Ministry of Transport                 |
| unhcr                      | UNHCR                                 |
| ribbon-ntrc                | National Transformation Ribbon        |
| weather-met                | Meteorological Department             |
| flood-jps                  | JPS (Drainage & Irrigation)           |
| jakoa                      | JAKOA                                 |
| blood-pdn                  | National Blood Bank                   |
| ballot-spr                 | SPR (Election Commission)             |
| fire-bomba                 | Bomba (Fire Dept)                     |
| ambulance-mers             | MERS (Emergency Response)             |
| hospital-moh               | MOH (Health Ministry)                 |
| phcorp                     | Pharmacy Corp                         |
| passport-imigresen         | Immigration (Passport)                |
| bnm                        | Bank Negara Malaysia                  |
| money-epf                  | EPF (Employees Provident Fund)        |
| money-lhdn                 | Inland Revenue Board                  |
| mampu                      | MAMPU                                 |
| socso-perkeso              | SOCSO (Social Security)               |
| light-bulb-ipr-epu         | IPR/EPU (Innovation, Planning Unit)   |
| police-pdrm                | PDRM (Royal Malaysia Police)          |
| helping-hand-icu-jpm       | ICU/JPM (Implementation Coordination) |
| document-mof               | MOF (Finance Ministry)                |
| mini-phcorp                | Mini Pharmacy Corp                    |
| mini-mampu                 | Mini MAMPU                            |
| mini-ribbon-ntrc           | Mini National Transformation          |
| mini-bnm                   | Mini BNM                              |
| mini-dosm                  | Mini DOSM                             |
| mini-helmet-jpa            | Mini JPA                              |
| mini-document-mof          | Mini MOF                              |
| mini-train-mot             | Mini MOT                              |
| mini-ambulance-mers        | Mini MERS                             |
| mini-hospital-moh          | Mini MOH                              |
| mini-police-pdrm           | Mini Police                           |
| mini-weather-climate       | Mini Meteorology                      |
| mini-fire-bomba            | Mini Bomba                            |
| mini-flood-warning         | Mini Flood warning                    |
| mini-light-bulb-ipr-epu    | Mini Innovation/Planning              |
| mini-helping-hands-icu-jpm | Mini ICU/JPM                          |
| mini-money-kwap            | Mini KWAP                             |
| mini-ballot-spr            | Mini SPR                              |
| mini-money-epf             | Mini EPF                              |
| mini-book-moe              | Mini MOE                              |
| mini-passport-imigresen    | Mini Passport                         |
| mini-internet-mcmc         | Mini MCMC                             |
| mini-blood-pdn             | Mini Blood Bank                       |
| mini-car-jpj               | Mini JPJ                              |
| mini-identity-jpn          | Mini JPN                              |
| mini-socso                 | Mini SOCSO                            |
| mini-money-lhdn            | Mini LHDN                             |
| mini-unhcr                 | Mini UNHCR                            |
| mini-jakoa                 | Mini JAKOA                            |
| mini-website               | Mini Website                          |

---

## 7. Icon Usage Examples

### React Example

```jsx
import { Button, ButtonIcon } from '@govtechmy/myds-react/button';
import { SearchIcon } from '@govtechmy/myds-react/icon';

<Button>
  <ButtonIcon>
    <SearchIcon />
  </ButtonIcon>
  Search
</Button>;
```

### HTML Example

```html
<button aria-label="Search">
  <svg width="20" height="20" ...><!-- Search icon SVG --></svg>
  Search
</button>
```

---

## 8. Contribution & Extension

- **Request New Icon:** Submit a request via GitHub or Figma feedback.
- **Contribution Requirements:** Use 20×20 grid, 1.5px stroke, clear symbolism, outline and filled variants.
- **Review:** All submissions are checked for clarity, accessibility, and consistency.

---

## 9. References & Resources

- [MYDS Official Icon Gallery](https://design.digital.gov.my/en/icon)
- [MYDS Design Guidelines: Icon](https://design.digital.gov.my/en/docs/design/icon)
- [MYDS React Icons (npm)](https://www.npmjs.com/package/@govtechmy/myds-react)
- [MYDS Figma Kit](https://www.figma.com/design/svmWSPZarzWrJ116CQ8zpV/MYDS--Beta-)
- [MyGovEA Principles](https://mygovea.jdn.gov.my/page-prinsip-reka-bentuk/)

---

> This document ensures all icon usage in MYDS is citizen-centric, inclusive, and technically robust. For the latest updates and downloads, always refer to the official gallery above.

<!--
This file is auto-generated from reference images and source context.
To update, edit the source or images and regenerate.

## Comments
- All headings are unique (no duplicate heading errors per MD024).
- All tables and sections are organized for clarity and specification compliance.
- HEX codes are referenced for all major scales for quick copy-paste for CSS/JS usage.
- Text colour variables for white, black/gray, accent, and disabled text are included and organized by mode.
- Outline colours for both light and dark modes include disabled variants for all scales.
-->
