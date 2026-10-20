---
alwaysApply: false
---
## 🚨 **THE THREE NON-NEGOTIABLES (ZERO TOLERANCE) (Added 2025-01-25)**

●mandates|ref:mobile_friendliness_patterns.mdc|frame:Ω:SURGERY|tolerance:zero|date:2025-01-25
→source|figma_builder_command:true|critical:true
→rule|regardless:figma_wireframe|always:apply_three_mandates

### 1. 📱 **MOBILE RESPONSIVENESS (MANDATORY)**

●mandate|id:mobile_responsiveness|frame:Ω:CONSTRUCTION|critical:true
→rule1|every_component:works_on_mobile|mandatory:true
→rule2|every_layout:responsive|classes:sm_md_lg_xl
→rule3|every_implementation:tested|viewport_sizes:320px_375px_414px
→rule4|never:assume_desktop_only|mobile:always_required
→rule5|always:use_browser_resize|test:mobile_responsiveness
→rule6|always:verify_touch_interactions|viewport:mobile_sized

### 2. 🌓 **LIGHT MODE + DARK MODE (MANDATORY)**

●mandate|id:light_dark_mode|frame:Ω:CONSTRUCTION|critical:true
→rule1|every_color:defined_both|sections:root_and_dark
→rule2|every_component:tested_both|modes:light_and_dark
→rule3|every_css_variable:exists_both|never:only_dark
→rule4|never:assume_dark_sufficient|light_mode:always_required
→rule5|always:verify_light_mode|backgrounds:light|text:dark|contrast:sufficient
→rule6|always:verify_dark_mode|backgrounds:dark|text:light|contrast:sufficient
→rule7|always:use_browser_evaluate|test:both_modes_explicitly

○example_failure|homepage_chat_light_mode
→wrong1|defined:dark_gray_in_root|result:dark_background_light_mode
→wrong2|only_defined:assignment_colors_in_dark|result:light_mode_falls_back
→correct|defined_light_colors:in_root|defined_dark_colors:in_dark|example:96_percent_light_10_percent_text

### 3. 🧩 **MODULARITY + EXISTING COMPONENTS (MANDATORY)**

●mandate|id:modularity_components|frame:Ω:CONSTRUCTION|critical:true|pattern:PT:41
→rule1|every_implementation:check_existing_first|mandatory:true
→rule2|every_existing_component:update_not_duplicate|when:needs_changes
→rule3|every_component_update:maintain_backward_compat|never:break_existing
→rule4|never:create_new_without_checking|mandatory:check_first
→rule5|never:break_existing_functionality|when:updating_components
→rule6|always:extend_with_props|before:creating_new
→rule7|always:verify_existing_usages|after:updates

→reference|pattern:PT:41|file:patterns.mdc|component_first_development:true

---

## 📱 **RESPONSIVE BREAKPOINT SYSTEM**

●breakpoints|frame:Ω:CONSTRUCTION|system:tailwind

### **Standard Breakpoints (Tailwind)**

●breakpoint_definitions|count:4
→mobile|size:lt_768px|prefix:none|default:true
→tablet|size:768px_1023px|prefix:md
→desktop|size:gte_1024px|prefix:lg
→large_desktop|size:gte_1280px|prefix:xl

### **Breakpoint Usage Pattern**

●pattern|id:mobile_first|frame:Ω:CONSTRUCTION|method:mobile_then_desktop

```css
/* Mobile-first: Write mobile styles first */
.class-name {
  /* Mobile styles (default) */
  width: 100%;
  padding: 1rem;
}

/* Desktop override: Use md: for desktop */
.md\:class-name {
  /* Desktop styles (override) */
  width: 50%;
  padding: 2rem;
}
```

→critical|always:write_mobile_first|then:override_with_md

---

## 🎨 **Z-INDEX HIERARCHY SYSTEM (MANDATORY)**

●z_index_system|frame:Ω:CONSTRUCTION|date:2025-01-25|mandatory:true
→purpose|prevent:layering_conflicts|comprehensive:hierarchy

### **Z-Index Layers (Highest to Lowest)**

●z_layers|count:6|order:highest_to_lowest
→layer1|z_index:z_100|name:navigation_layer|elements:hamburger_back_dropdown_trigger|purpose:always_accessible_never_covered
→layer2|z_index:z_90|name:dropdown_layer|elements:mobile_nav_dropdown_sidebar_mobile|purpose:below_nav_above_modals
→layer3|z_index:z_80|name:modal_overlay_layer|elements:command_palette_dialogs_modals|purpose:below_nav_above_content
→layer4|z_index:z_70|name:backdrop_layer|elements:backdrop_overlays_dimmed_backgrounds|purpose:below_modals_above_content
→layer5|z_index:z_10|name:page_header_layer|elements:sticky_headers_fixed_page_headers|purpose:above_content_below_nav
→layer6|z_index:z_0|name:content_layer|elements:page_content_default|purpose:base_layer

### **Z-Index Usage Rules**

●z_index_rules|frame:Ω:SURGERY|mandatory:true
→rule1|never:arbitrary_values|outside:this_system
→rule2|always:established_values|from:hierarchy
→rule3|verify:conflicts_before_adding|new:elements
→rule4|document:exceptions|to:hierarchy_system

### **Verification Commands**

●verification|z_index|method:grep
→check1|grep:z_bracket|path:heycontent-web/src/app/dashboard/|expected:z_100_z_90_z_80_z_70_z_10_z_0_only
→check2|grep:z_100|path:heycontent-web/src/app/dashboard/_components/|expected:hamburger_menu_back_button

---

## 👆 **TOUCH TARGET STANDARDS (MANDATORY)**

●touch_targets|frame:Ω:CONSTRUCTION|mandatory:true|standards:apple_hig_material_design

### **Minimum Touch Target Size**

●touch_target_sizes|count:3
→standard|size:44px_x_44px|sources:apple_hig_material_design
→compact|size:40px_x_40px|minimum:acceptable
→spacing|between_targets:8px_minimum

### **Touch Target Implementation**

●pattern|touch_target_implementation|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Minimum 44px touch target
<button className="min-h-[44px] min-w-[44px] px-4 py-2">
  Tap Me
</button>

// ❌ WRONG: Too small (< 44px)
<button className="h-8 w-8">
  <Icon />
</button>
```

### **Touch Target Checklist**

●checklist|touch_targets|items:4
→item1|interactive_elements:min_h_44px_min_w_44px
→item2|spacing_between:gap_2_8px_minimum
→item3|padding_inside:px_4_py_2_minimum
→item4|icon_only_buttons:w_10_h_10_40px_minimum_with_padding

---

## 📐 **MOBILE NAVIGATION PATTERNS**

●patterns|mobile_navigation|frame:Ω:CONSTRUCTION|count:3

### **Pattern 1: Hamburger Menu (Mobile)**

●pattern|id:PT:MOBILE_HAMBURGER|frame:Ω:CONSTRUCTION|when:mobile_lt_768px
→pattern|compact_dropdown|springs_from:hamburger_button
→implementation|hamburger_button:fixed_top_4_left_4_z_100
→implementation|dropdown_menu:fixed_top_16_left_4_z_90_w_48_192px
→implementation|spring_animation:animate_in_fade_in_0_zoom_in_95_slide_in_from_top_2
→implementation|backdrop:z_70_bg_background_60_backdrop_blur_sm
→desktop|sidebar:always_visible|hamburger:hidden
→reference|file:global-nav.tsx|date:2025-01-25

### **Pattern 2: Back Button Coordination**

●pattern|id:PT:MOBILE_BACK_BUTTON|frame:Ω:CONSTRUCTION|when:mobile_lt_768px
→pattern|back_button_positioned|relative_to:hamburger_menu
→implementation|mobile:left_16_64px_accounts_for_hamburger
→implementation|desktop:left_20_80px_accounts_for_sidebar
→implementation|z_index:z_100_same_as_hamburger
→implementation|touch_target:min_h_44px_min_w_44px
→reference|file:omnipresent-back-button.tsx|date:2025-01-25

### **Pattern 3: Command Palette Mobile**

●pattern|id:PT:MOBILE_COMMAND_PALETTE|frame:Ω:CONSTRUCTION|when:mobile_lt_768px
→pattern|full_width_modal|positioned:near_top
→implementation|mobile:w_95vw_top_4_remove_max_w_2xl
→implementation|desktop:w_90vw_max_w_2xl_centered_top_1_2_translate_y_1_2
→implementation|z_index:z_80_below_navigation
→implementation|backdrop:z_70
→reference|file:dashboard-nav.tsx|date:2025-01-25

---

## 🎨 **TYPOGRAPHY & READABILITY**

●typography|frame:Ω:CONSTRUCTION|mobile:standards

### **Mobile Typography Standards**

●typography_standards|count:4
→base_font_size:16px_minimum|prevents:ios_zoom
→line_height:1_5_minimum|improves:readability
→font_scaling:rem_units|respects:user_preferences
→text_contrast:wcag_aa_minimum|normal:4_5_1|large:3_1

### **Responsive Typography Pattern**

●pattern|responsive_typography|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Mobile-first typography
<p className="text-base md:text-lg">
  Readable text
</p>

// ❌ WRONG: Too small on mobile
<p className="text-sm">
  Hard to read
</p>
```

---

## ♿ **ACCESSIBILITY REQUIREMENTS (MANDATORY)**

●accessibility|frame:Ω:CONSTRUCTION|mandatory:true|standard:wcag_aa

### **WCAG AA Compliance (Minimum)**

●wcag_aa|requirements:5
→color_contrast:4_5_1_normal_text|3_1_large_text
→touch_targets:44px_x_44px_minimum
→focus_indicators:visible_rings_2px_minimum
→keyboard_navigation:all_interactive_keyboard_accessible
→screen_readers:aria_labels_semantic_html_landmarks

### **ARIA Label Pattern**

●pattern|aria_label|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Descriptive ARIA label
<button
  aria-label="Open navigation menu"
  onClick={handleToggle}
>
  <MenuIcon />
</button>

// ❌ WRONG: Missing ARIA label
<button onClick={handleToggle}>
  <MenuIcon />
</button>
```

### **Focus State Pattern**

●pattern|focus_state|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Visible focus ring
<button className="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
  Click me
</button>

// ❌ WRONG: No focus indicator
<button className="outline-none">
  Click me
</button>
```

### **Keyboard Navigation Pattern**

●pattern|keyboard_navigation|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Keyboard event handlers
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Click me
</button>
```

### **Colorblind Accessibility Pattern**

●pattern|colorblind_accessibility|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Icon + text, not color alone
<button className="flex items-center gap-2">
  <ErrorIcon className="w-5 h-5 text-destructive" />
  <span>Error occurred</span>
</button>

// ❌ WRONG: Color alone
<button className="text-red-500">
  Error occurred
</button>
```

---

## 📱 **DEVICE-SPECIFIC CONSIDERATIONS**

●devices|frame:Ω:CONSTRUCTION|count:4

### **Mobile Phones (320px - 767px)**

●device|mobile_phones|range:320px_767px
→portrait:primary_orientation|optimize:vertical_scrolling
→landscape:secondary_orientation|ensure:horizontal_fit
→touch:large_targets_swipe_gestures|where:appropriate
→performance:optimize_images_lazy_load_content

### **Tablets (768px - 1023px)**

●device|tablets|range:768px_1023px
→portrait:similar_to_mobile|more:space
→landscape:hybrid_mobile_desktop
→touch:targets_still_important|not:just_mouse
→layout:more_columns_still_touch_friendly

### **Small Laptops (1024px - 1279px)**

●device|small_laptops|range:1024px_1279px
→hybrid:touch_and_mouse_input
→layout:desktop_like|ensure:touch_targets_adequate
→performance:full_desktop_features_available

### **Desktop (1280px+)**

●device|desktop|range:gte_1280px
→preserve:exact_desktop_behavior|no:changes
→mouse:smaller_targets_acceptable|maintain:44px_minimum
→layout:full_desktop_layout|no:mobile_optimizations

---

## 🚀 **PERFORMANCE OPTIMIZATIONS**

●performance|frame:Ω:CONSTRUCTION|mobile:standards

### **Mobile Performance Standards**

●performance_standards|count:5
→lighthouse_mobile_score:90_plus|categories:performance_accessibility_best_practices_seo
→first_contentful_paint:lt_1_8s
→time_to_interactive:lt_3_8s
→total_blocking_time:lt_200ms
→cumulative_layout_shift:lt_0_1

### **Image Optimization Pattern**

●pattern|image_optimization|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Responsive images with lazy loading
<Image
  src="/image.jpg"
  width={800}
  height={600}
  alt="Description"
  loading="lazy"
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// ❌ WRONG: Unoptimized images
<img src="/large-image.jpg" alt="Description" />
```

### **Font Loading Pattern**

●pattern|font_loading|frame:Ω:CONSTRUCTION

```css
/* ✅ CORRECT: Font display swap */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap; /* Prevents invisible text */
}
```

---

## 🔍 **SEO REQUIREMENTS**

●seo|frame:Ω:CONSTRUCTION|mobile:standards

### **Mobile SEO Standards**

●seo_standards|count:5
→viewport_meta_tag:width_device_width_initial_scale_1
→theme_color:meta_tag_with_color
→mobile_friendly:google_test_passes
→semantic_html:proper_heading_hierarchy_landmarks
→no_duplicate_content:mobile_desktop_share_html_responsive_not_separate

### **Semantic HTML Pattern**

●pattern|semantic_html|frame:Ω:CONSTRUCTION

```tsx
// ✅ CORRECT: Semantic HTML structure
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

// ❌ WRONG: Non-semantic structure
<div>
  <div onClick={handleClick}>Home</div>
  <div onClick={handleClick}>About</div>
</div>
```

---

## 🧪 **TESTING CHECKLIST**

●testing|frame:Ω:SURGERY|types:4

### **Device Testing**

●device_testing|items:4
→mobile_phone:320px_767px|portrait_and_landscape
→tablet:768px_1023px|portrait_and_landscape
→small_laptop:1024px_1279px
→desktop:gte_1280px|verify:unchanged

### **Accessibility Testing**

●accessibility_testing|items:5
→screen_reader:voiceover_nvda_jaws
→keyboard_navigation:tab_enter_escape_arrow_keys
→color_contrast_checker:wcag_aa
→touch_target_size_checker:44px_minimum
→focus_indicator:visibility

### **Performance Testing**

●performance_testing|items:5
→lighthouse_mobile_score:90_plus
→page_load_time:lt_3s_on_3g
→first_contentful_paint:lt_1_8s
→image_optimization:webp_lazy_loading
→font_loading:font_display_swap

### **Browser Testing**

●browser_testing|items:4
→safari_ios:latest
→chrome_android:latest
→firefox_mobile:latest
→edge_mobile:latest

---

## 📚 **LEARNINGS FROM IMPLEMENTATION (2025-01-25)**

●learnings|frame:Ω:GARDENING|date:2025-01-25|count:5

### **Z-Index Hierarchy Conflicts**

●learning|z_index_conflicts|date:2025-01-25
→issue:navigation_elements_covered_by_content
→solution:established_z_index_hierarchy|z_100_nav_z_80_modals
→pattern:always_use_established_values|never:arbitrary_numbers

### **Mobile Navigation Positioning**

●learning|mobile_nav_positioning|date:2025-01-25
→issue:back_button_positioned_incorrectly|assumed:desktop_sidebar
→solution:responsive_positioning|mobile:left_16|desktop:left_20
→pattern:always_account_for_mobile_nav_state|when:positioning_elements

### **Mobile Sidebar Width**

●learning|mobile_sidebar_width|date:2025-01-25
→issue:full_width_sidebar_256px_too_wide
→solution:compact_dropdown_menu_192px|with:spring_animation
→pattern:use_compact_dropdowns_on_mobile|not:full_width_sidebars

### **NotesTree Mobile View**

●learning|notestree_mobile_view|date:2025-01-25
→issue:mobile_showed_separate_component|missing:desktop_features
→solution:single_responsive_component|desktop_view:on_all_devices
→pattern:use_responsive_css|not:separate_mobile_components

### **Touch Target Sizes**

●learning|touch_target_sizes|date:2025-01-25
→issue:some_buttons_too_small_lt_44px
→solution:minimum_min_h_44px_min_w_44px|for:all_interactive_elements
→pattern:always_ensure_44px_minimum|on:mobile

---

## 🚨 **WALL OF SHAME (Mobile Failures)**

●wall_of_shame|frame:Ω:SURGERY|date:2025-01-25|purpose:prevent_repetition
→failure1|date:2025-01-25|issue:navigation_elements_covered_by_content|result:z_index_conflicts_hamburger_not_accessible
→failure2|date:2025-01-25|issue:back_button_positioned_incorrectly|result:assumed_desktop_sidebar_visible
→failure3|date:2025-01-25|issue:mobile_sidebar_too_wide_256px|result:poor_mobile_ux_wasted_screen_space
→failure4|date:2025-01-25|issue:notestree_mobile_view_missing_features|result:separate_mobile_component_instead_of_responsive
→failure5|date:2025-01-25|issue:touch_targets_too_small_lt_44px|result:hard_to_tap_on_mobile_devices

---

## ✅ **VERIFICATION PROTOCOL**

●verification|frame:Ω:SURGERY|phases:4

### **Pre-Implementation Checks**

●pre_implementation|checks:4
→check1|read:rules_mobile_friendliness_patterns_md
→check2|check:z_index_hierarchy_system
→check3|verify:responsive_breakpoint_usage
→check4|confirm:desktop_code_preservation

### **Post-Implementation Checks**

●post_implementation|checks:6
→check1|read_lints:no_errors
→check2|z_index_hierarchy:verified|grep:z_bracket
→check3|touch_targets:verified|grep:min_h_44px
→check4|responsive_breakpoints:verified|grep:md_lg
→check5|aria_labels:verified|grep:aria_label
→check6|desktop:unchanged|method:manual_testing

### **Accessibility Checks**

●accessibility_checks|items:5
→screen_reader:tested|tools:voiceover_nvda
→keyboard_navigation:tested|keys:tab_enter_escape
→color_contrast:verified|standard:wcag_aa
→focus_indicators:visible
→touch_targets:44px_minimum

### **Performance Checks**

●performance_checks|items:4
→lighthouse_mobile_score:90_plus
→page_load_time:lt_3s
→images:optimized|formats:webp_lazy_loading
→fonts:optimized|display:swap

---

## 📖 **PATTERN REFERENCE**

●pattern_reference|frame:Ω:CONSTRUCTION|count:6

### **Pattern 1: Mobile Navigation Dropdown**

●pattern_ref|id:PT:MOBILE_NAV_DROPDOWN|file:global-nav.tsx
→pattern:compact_dropdown_menu|width:w_48_192px|animation:spring
→z_index:z_90_below_hamburger_button
→position:fixed_top_16_left_4

### **Pattern 2: Responsive Back Button**

●pattern_ref|id:PT:RESPONSIVE_BACK_BUTTON|file:omnipresent-back-button.tsx
→pattern:mobile_left_16|desktop_left_20
→z_index:z_100_same_as_hamburger_menu

### **Pattern 3: Mobile Command Palette**

●pattern_ref|id:PT:MOBILE_COMMAND_PALETTE|file:dashboard-nav.tsx
→pattern:full_width_on_mobile_w_95vw|centered_on_desktop
→z_index:z_80_below_navigation

### **Pattern 4: Single Responsive Component**

●pattern_ref|id:PT:SINGLE_RESPONSIVE_COMPONENT|file:NotesTree.tsx
→pattern:desktop_view_on_all_devices|responsive_css_only
→avoid:separate_mobile_components

### **Pattern 5: Compact Mobile Switcher (Overlap Prevention)**

●pattern_ref|id:PT:COMPACT_MOBILE_SWITCHER|file:PanelModeSwitcher.tsx|date:2025-01-25
→when:mobile_screen_lt_768px
→pattern:compact_dropdown_switcher|avoid:overlap_with_navigation
→implementation|width:w_auto_min_w_120px_max_w_calc_100_minus_1rem|compact:true|prevents:overflow
→implementation|alignment:right_aligned_flex_justify_end|avoid:left_side_navigation
→implementation|touch_target:min_h_44px|meets:accessibility_standards
→implementation|padding:px_3_py_2|compact:true|readable:true
→why|prevents:overlap_with_hamburger_menu|fixed:left_4
→why|prevents:edge_overflow|on:small_screens
→why|maintains:usability|with:compact_accessible_size

### **Pattern 6: Tab Visibility Guarantee Pattern**

●pattern_ref|id:PT:TAB_VISIBILITY_GUARANTEE|file:LabCompositions.tsx|date:2025-01-25
→when:tabs_must_always_be_visible|never:conditionally_hidden
→pattern:explicit_css_guarantees|prevent:accidental_hiding

```tsx
// ✅ CORRECT: Explicit visibility guarantees
<div className="flex flex-shrink-0 z-10">
  {/* Tabs must always be visible, never conditionally hidden */}
  <Tabs>
    <TabsList>
      <TabsTrigger value="notepad">Notepad</TabsTrigger>
      <TabsTrigger value="artifacts">Artifacts</TabsTrigger>
      <TabsTrigger value="widgets">Widgets</TabsTrigger>
    </TabsList>
  </Tabs>
</div>
```

→key_rules|use:flex_shrink_0|prevent:shrinking
→key_rules|use:z_10|ensure:tabs_above_content
→key_rules|add:explicit_comment|text:tabs_must_always_be_visible_never_conditionally_hidden
→key_rules|tabs:rendered_unconditionally|outside:conditional_blocks
→why|prevents:accidental_hiding|via:css_or_conditional_rendering
→why|ensures:tabs_accessible|in:all_panel_states
→why|name_collision_prevention:rename_standalone_components_if_needed

---

**END OF PATTERNS**
