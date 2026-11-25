---
name: polaris-pattern-common-actions
description: Standardize merchant actions across your app—predictable icons and placements for add, copy, delete, edit, and more
---

# Common Actions

Standardizing recurring actions gives merchants a predictable way to complete common tasks.

## Add

Inserts existing or new objects, items, or data into the UI. Example: adding an item to a list or element into a layout.

**Do:**
- Default to circle plus icon for add actions
- Use plus icon in secondary and primary button variants
- Place add actions at the bottom of a list (unless list will be long)
- Place add actions at the bottom of selectable options (keep visible, outside scrollable area)
- Place add actions in the header in long lists of resources
- Place add actions associated with a table in card, table, or page header

**Don't:**
- Place add actions at bottom of a table (risks getting lost)
- Include intermediary steps during resource creation (put on new page instead)

## Copy

Duplicates selected content and stores it in merchant's clipboard.

**Do:**
- Use clipboard icon with tertiary icon button for copying text
- Use link icon with tertiary icon button for copying deep links/URLs
- Show copy actions on hover for cursor interactions
- Provide feedback inline using confirmation check icon post-click or tap
- Use "copied to clipboard" toast message when action is within action list

## Delete

Destroys an item or object and completely erases data from the system.

**Do:**
- Use delete icon with destructive item in action list
- Always place delete actions at bottom of action list
- Use delete icon for delete actions in lists
- Place list item delete actions inline to the right (tertiary button with delete icon)
- Display list item delete actions on hover

**Don't:**
- Use x icon for delete actions
- Overuse critical styled buttons in a single view
- Pair primary critical buttons with other button variants that create visual competition

## Edit

Allows merchants to make changes to existing content or objects.

**Do:**
- Use edit for modifying, updating, or managing items/objects
- Default to edit icon with tertiary icon button

**Caution:**
- Avoid too many buttons with filled/shaped containers in close proximity (cluttered feeling)

## More Actions

Displays available or additional actions for an element or item.

**Do:**
- Use menu horizontal icon to indicate available or more actions
- Use secondary or tertiary icon button

**Don't:**
- Group actions in card header by default (consider alternatives that place actions in context)

## Pin

Sticks an object to an easily accessible location within the UI. Allows merchants to keep important items available for quick access.

**Do:**
- Use pin icon with tertiary icon button to show item can be pinned
- Use pin filled icon to show item has been pinned
- Place pinned objects together for clarity
- Make it easy to unpin an item

## Remove

Removes an item from a list or breaks relationship between objects. Item is taken out of context without being deleted from system. Example: removing a product from a collection keeps it in the system.

**Do:**
- Use x icon with tertiary icon button
- Show remove actions on hover for cursor navigation

**Don't:**
- Use delete icon for remove actions
