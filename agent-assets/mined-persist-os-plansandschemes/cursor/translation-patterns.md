---
alwaysApply: false
---
# Translation System Patterns

●patterns|ref:translation_patterns.mdc|frame:Ω:CONSTRUCTION|persona:P:EXEC
→purpose|ssot:translation_implementation|reference:this_file|never:repeat_content

## Core Principles

●principles|frame:Ω:CONSTRUCTION|count:4
→principle1|progressive_translation|cache_first:true|translates:on_demand
→principle2|component_pattern|visible_text:T_component|attributes:useTranslation_hook
→principle3|context_required|all_translations:must_include_context|quality:improved
→principle4|a2a_optimized|brief:true|directive_focused:true

## Pattern: Visible Text Translation

●pattern|id:PT:TRANSLATION_VISIBLE|frame:Ω:CONSTRUCTION|component:T
→rule|use:T_component|for:all_user_facing_text
→implementation|import:from_components_translation|wrap:text_strings|context:required

○code_example|basic:T_component

```tsx
import { T } from '@/components/translation'

// Basic
<T>Hello, world!</T>

// With context (REQUIRED)
<T context="button.save">Save</T>
<T context="nav.notifications">Notifications</T>
<T context="notifications.empty">No notifications</T>
```


→rules|wrap:all_visible_text|context:always_provide|semantic_html:when_needed

## Pattern: Attribute Translation

●pattern|id:PT:TRANSLATION_ATTRIBUTE|frame:Ω:CONSTRUCTION|hook:useTranslation
→rule|use:useTranslation_hook|for:aria_labels_titles_placeholders
→implementation|import:from_hooks_useTranslation|extract:text_property|context:required

○code_example|attribute_translation

```tsx
import { useTranslation } from '@/hooks/useTranslation'

const { text: ariaLabel } = useTranslation('Notifications', {
  context: 'aria.notifications'
})

<button aria-label={ariaLabel}>...</button>
```


→rules|hook:for_string_attributes|extract:text_property|context:always_provide

## Context Naming Convention

●convention|id:context_naming|format:category_subcategory_item|mandatory:true
→format|pattern:[category].[subcategory].[item]|hierarchical:true
→categories|nav:navigation|button:button_labels|aria:accessibility|notifications:notification_ui|error:error_messages|status:status_messages

○examples|nav.command_palette:Command_Palette|nav.notifications:Notifications|aria.notifications:Notifications_aria_label|notifications.empty:No_notifications|button.save:Save

## Verification Checklist

●verification|frame:Ω:SURGERY|types:2

### Automated Checks

●automated|checks:4|method:grep
→check1|grep:from_components_translation|verify:all_import_T
→check2|grep:useTranslation|verify:attributes_use_hook
→check3|grep:context=|verify:all_have_context
→check4|grep:hardcoded_strings|verify:no_english_in_jsx

### Manual Checks

●manual|checks:4|method:visual_review
→check1|visible_text:wrapped_in_T|status:verified
→check2|aria_labels:use_hook|status:verified
→check3|contexts:follow_convention|status:verified
→check4|untranslated_strings:none_visible|status:verified

## Common Contexts Reference

●contexts|reference:common_usage|frame:Ω:CONSTRUCTION

### Navigation Contexts

●nav_contexts|category:nav|count:5
→nav.command_palette:Command_Palette
→nav.notifications:Notifications
→nav.files:Files
→nav.thinking_lab:Thinking_Lab
→nav.settings:Settings

### Accessibility Contexts

●aria_contexts|category:aria|count:7
→aria.notifications:Notifications_button
→aria.close_notifications:Close_notifications
→aria.command_palette:Open_command_palette
→aria.files:Files_button
→aria.thinking_lab:Thinking_Lab_button
→aria.profile_settings:Profile_Settings
→aria.toggle_nav:Toggle_navigation_menu

### Notification Contexts

●notification_contexts|category:notifications|count:2
→notifications.title:Notifications_heading
→notifications.empty:No_notifications_empty_state

## Anti-Patterns (Wall of Shame)

●anti_patterns|frame:Ω:SURGERY|purpose:prevent_repetition
→pattern1|❌hardcoded_english:in_jsx|violation:no_translation
→pattern2|❌missing_context:no_context_prop|violation:quality_degraded
→pattern3|❌T_for_aria_labels:wrong_component|violation:use_hook_instead
→pattern4|❌inconsistent_naming:dash_vs_dot|violation:convention_broken

○examples|wrong:span_Notifications|wrong:T_no_context|wrong:T_in_aria_label|wrong:button-save_vs_button.save
