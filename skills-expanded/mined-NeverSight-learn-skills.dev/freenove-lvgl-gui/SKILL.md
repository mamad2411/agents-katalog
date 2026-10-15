---
name: freenove-lvgl-gui
description: Build graphical user interfaces with LVGL (Light and Versatile Graphics Library) on the Freenove Media Kit. Create buttons, labels, sliders, images, lists, and complex UIs with touch/input support. Use this skill when creating interactive interfaces, menus, control panels, or any GUI application for the ESP32-S3.
---

# Freenove LVGL GUI

Build professional graphical user interfaces with LVGL on the ESP32-S3. Create interactive controls, visual feedback, and polished user experiences.

## What You'll Learn

- **LVGL Basics**: Library setup and core concepts
- **Widgets**: Buttons, labels, sliders, images, lists, charts
- **Layouts**: Flexbox and grid layouts for responsive design
- **Styling**: Customize appearance with themes and styles
- **Events**: Handle user input and touch interactions
- **Advanced**: Animations, transitions, and complex UIs

## What is LVGL?

**LVGL (Light and Versatile Graphics Library)** is an open-source embedded GUI library:
- **Lightweight**: Runs on microcontrollers with limited resources
- **Versatile**: Supports various displays and input devices
- **Rich Widgets**: 30+ built-in widgets
- **Styling**: CSS-like styling system
- **Animations**: Hardware-accelerated animations
- **Touch**: Multi-touch and gesture support

## Hardware Requirements

- **Display**: TFT LCD (1.14" or 3.5")
- **Input**: Button navigation or touch screen (3.5" only)
- **Memory**: PSRAM recommended for complex UIs
- **Storage**: SD card for images and resources

## Quick Start Decision Tree

| Goal | Start Here |
|------|------------|
| First LVGL project | [Basic Setup](#lvgl-setup) |
| Create buttons/controls | [Basic Widgets](#basic-widgets) |
| Build complex layout | [Layouts and Styling](#layouts-and-styling) |
| Handle user input | [Events and Input](#events-and-input) |
| Polished UI with animations | [Advanced Features](#advanced-features) |

## Prerequisites

- Completed [Camera & Display](../freenove-camera-display/SKILL.md)
- Install **lvgl** library (from kit's Libraries folder)
- Understanding of TFT display basics

## LVGL Setup

### Library Configuration

**Important**: Configure LVGL before use!

**Edit lv_conf.h** (in lvgl library folder):
```cpp
/* Enable/Disable features */
#define LV_USE_LOG 1
#define LV_LOG_LEVEL LV_LOG_LEVEL_WARN

/* Display settings */
#define LV_HOR_RES_MAX 240    // or 320 for 3.5"
#define LV_VER_RES_MAX 240    // or 480 for 3.5"
#define LV_COLOR_DEPTH 16     // RGB565

/* Memory settings */
#define LV_MEM_SIZE (64U * 1024U)  // 64KB for LVGL heap

/* Enable widgets */
#define LV_USE_BTN 1
#define LV_USE_LABEL 1
#define LV_USE_SLIDER 1
#define LV_USE_IMG 1
#define LV_USE_LIST 1
#define LV_USE_CHART 1
#define LV_USE_ANIMATION 1

/* Enable input devices */
#define LV_USE_INDEV_KEYPAD 1
#define LV_USE_INDEV_BUTTON 1
```

### Display Driver Setup

```cpp
#include <lvgl.h>
#include "display.h"  // Kit's display driver

Display screen;  // Display instance

/* Display buffer */
static lv_disp_draw_buf_t draw_buf;
static lv_color_t buf1[LV_HOR_RES_MAX * 10];  // 10 lines buffer
static lv_color_t buf2[LV_HOR_RES_MAX * 10];  // Optional second buffer

/* Display flush callback */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p) {
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);
  
  tft.startWrite();
  tft.setAddrWindow(area->x1, area->y1, w, h);
  tft.pushColors((uint16_t *)&color_p->full, w * h, true);
  tft.endWrite();
  
  lv_disp_flush_ready(disp);
}

void setup() {
  Serial.begin(115200);
  
  // Initialize display hardware
  screen.init(TFT_DIRECTION);
  
  // Initialize LVGL
  lv_init();
  
  // Initialize display buffer
  lv_disp_draw_buf_init(&draw_buf, buf1, buf2, LV_HOR_RES_MAX * 10);
  
  // Initialize display driver
  static lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res = LV_HOR_RES_MAX;
  disp_drv.ver_res = LV_VER_RES_MAX;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.draw_buf = &draw_buf;
  lv_disp_drv_register(&disp_drv);
}

void loop() {
  lv_timer_handler();  // Handle LVGL tasks
  delay(5);
}
```

### Using Kit's Display Class

The kit provides a simplified Display class:

```cpp
#include "display.h"
#include <lvgl.h>

Display screen;  // Handles LVGL setup internally

void setup() {
  Serial.begin(115200);
  screen.init(TFT_DIRECTION);  // Initializes LVGL + TFT
  
  // Your UI code here
}

void loop() {
  screen.routine();  // Handles lv_timer_handler()
  delay(5);
}
```

## Basic Widgets

### Labels

```cpp
// Create a label on the current screen
lv_obj_t *label = lv_label_create(lv_scr_act());

// Set text
lv_label_set_text(label, "Hello LVGL!");

// Set position
lv_obj_set_pos(label, 10, 10);

// Set size (auto-size by default)
lv_obj_set_size(label, 100, 50);

// Text alignment
lv_obj_set_style_text_align(label, LV_TEXT_ALIGN_CENTER, 0);

// Long text modes
lv_label_set_long_mode(label, LV_LABEL_LONG_WRAP);  // Wrap text
lv_label_set_long_mode(label, LV_LABEL_LONG_DOT);   // Show dots if too long
lv_label_set_long_mode(label, LV_LABEL_LONG_SCROLL); // Scroll text

// Format with printf-style
lv_label_set_text_fmt(label, "Value: %d", 42);
```

### Buttons

```cpp
// Create a button
lv_obj_t *btn = lv_btn_create(lv_scr_act());

// Set position and size
lv_obj_set_pos(btn, 10, 50);
lv_obj_set_size(btn, 100, 40);

// Create label on button
lv_obj_t *label = lv_label_create(btn);
lv_label_set_text(label, "Click Me");
lv_obj_center(label);  // Center label on button

// Add click event
lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);

// Event callback
void btn_event_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    Serial.println("Button clicked!");
  }
}
```

### Sliders

```cpp
// Create a slider
lv_obj_t *slider = lv_slider_create(lv_scr_act());
lv_obj_set_width(slider, 150);
lv_obj_set_pos(slider, 10, 100);

// Set range
lv_slider_set_range(slider, 0, 100);
lv_slider_set_value(slider, 50, LV_ANIM_OFF);

// Add value changed event
lv_obj_add_event_cb(slider, slider_event_cb, LV_EVENT_VALUE_CHANGED, NULL);

// Event callback
void slider_event_cb(lv_event_t * e) {
  lv_obj_t * slider = lv_event_get_target(e);
  int32_t value = lv_slider_get_value(slider);
  Serial.printf("Slider value: %d\n", value);
}
```

### Switches

```cpp
// Create a switch
lv_obj_t *sw = lv_switch_create(lv_scr_act());
lv_obj_set_pos(sw, 10, 150);

// Check state
bool is_on = lv_obj_has_state(sw, LV_STATE_CHECKED);

// Event callback
lv_obj_add_event_cb(sw, switch_event_cb, LV_EVENT_VALUE_CHANGED, NULL);
```

### Checkboxes

```cpp
// Create a checkbox
lv_obj_t *cb = lv_checkbox_create(lv_scr_act());
lv_checkbox_set_text(cb, "Enable feature");
lv_obj_set_pos(cb, 10, 200);

// Check state
bool is_checked = lv_obj_has_state(cb, LV_STATE_CHECKED);
```

### Progress Bars

```cpp
// Create a progress bar
lv_obj_t *bar = lv_bar_create(lv_scr_act());
lv_obj_set_size(bar, 150, 20);
lv_obj_set_pos(bar, 10, 250);

// Set range and value
lv_bar_set_range(bar, 0, 100);
lv_bar_set_value(bar, 75, LV_ANIM_ON);  // Animate to 75%
```

### Images

```cpp
// Display an image from C array
LV_IMG_DECLARE(my_image);  // Declare image from header
lv_obj_t *img = lv_img_create(lv_scr_act());
lv_img_set_src(img, &my_image);

// Display from file (requires LV_USE_FS_STDIO)
lv_img_set_src(img, "S:/path/to/image.png");

// Set position
lv_obj_set_pos(img, 50, 50);

// Image transformations
lv_img_set_angle(img, 900);      // Rotate 90 degrees (in 0.1 deg units)
lv_img_set_zoom(img, 256);       // Zoom 2x (256 = 1x, 512 = 2x)
```

## Layouts and Styling

### Flexbox Layout

```cpp
// Create a container with flex layout
lv_obj_t *cont = lv_obj_create(lv_scr_act());
lv_obj_set_size(cont, 220, 120);
lv_obj_set_pos(cont, 10, 10);

// Enable flex layout
lv_obj_set_flex_flow(cont, LV_FLEX_FLOW_ROW_WRAP);
lv_obj_set_flex_align(cont, LV_FLEX_ALIGN_SPACE_EVENLY, 
                      LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

// Add items - they auto-arrange
for(int i = 0; i < 8; i++) {
  lv_obj_t *btn = lv_btn_create(cont);
  lv_obj_set_size(btn, 50, 30);
  lv_obj_t *label = lv_label_create(btn);
  lv_label_set_text_fmt(label, "%d", i);
  lv_obj_center(label);
}
```

### Grid Layout

```cpp
// Create a grid container
lv_obj_t *cont = lv_obj_create(lv_scr_act());
lv_obj_set_size(cont, 220, 220);

// Define grid columns and rows
static lv_coord_t col_dsc[] = {50, 50, 50, LV_GRID_TEMPLATE_LAST};
static lv_coord_t row_dsc[] = {50, 50, 50, LV_GRID_TEMPLATE_LAST};
lv_obj_set_grid_dsc_array(cont, col_dsc, row_dsc);

// Place items in grid
lv_obj_t *btn = lv_btn_create(cont);
lv_obj_set_grid_cell(btn, LV_GRID_ALIGN_STRETCH, 0, 2,  // Col 0, span 2
                            LV_GRID_ALIGN_STRETCH, 0, 1); // Row 0, span 1
```

### Styling

```cpp
// Create a style
static lv_style_t style_btn;
lv_style_init(&style_btn);

// Set style properties
lv_style_set_bg_color(&style_btn, lv_color_hex(0x2196F3));  // Blue
lv_style_set_bg_opa(&style_btn, LV_OPA_COVER);
lv_style_set_border_width(&style_btn, 2);
lv_style_set_border_color(&style_btn, lv_color_hex(0x1976D2));
lv_style_set_radius(&style_btn, 10);
lv_style_set_text_color(&style_btn, lv_color_white());

// Apply style to object
lv_obj_t *btn = lv_btn_create(lv_scr_act());
lv_obj_add_style(btn, &style_btn, 0);

// Apply style only in certain states
lv_obj_add_style(btn, &style_btn_pressed, LV_STATE_PRESSED);
```

### Themes

```cpp
// Apply a built-in theme
lv_theme_t *th = lv_theme_default_init(
  NULL,  // display
  lv_palette_main(LV_PALETTE_BLUE),  // primary color
  lv_palette_main(LV_PALETTE_RED),    // secondary color
  true,                               // dark mode
  &lv_font_montserrat_14              // font
);
lv_disp_set_theme(NULL, th);
```

## Events and Input

### Button Input (Navigation)

For kits without touch screen:

```cpp
// Create input device driver
static lv_indev_drv_t indev_drv;
lv_indev_drv_init(&indev_drv);
indev_drv.type = LV_INDEV_TYPE_KEYPAD;
indev_drv.read_cb = keypad_read;
lv_indev_t *indev = lv_indev_drv_register(&indev_drv);

// Create a group for focusable objects
lv_group_t *group = lv_group_create();
lv_indev_set_group(indev, group);

// Add objects to group
lv_group_add_obj(group, btn1);
lv_group_add_obj(group, btn2);
lv_group_add_obj(group, slider);

// Enable editing for sliders
lv_group_set_editing(group, true);

// Keypad read callback
void keypad_read(lv_indev_drv_t *drv, lv_indev_data_t *data) {
  static uint32_t last_key = 0;
  
  if (digitalRead(BUTTON_PIN) == LOW) {
    data->key = LV_KEY_ENTER;
    data->state = LV_INDEV_STATE_PRESSED;
  } else {
    // Check other keys (use analog button reading or GPIO expander)
    data->state = LV_INDEV_STATE_RELEASED;
  }
}
```

### Event Types

```cpp
LV_EVENT_CLICKED      // Object clicked
LV_EVENT_PRESSED      // Object pressed
LV_EVENT_RELEASED     // Object released
LV_EVENT_VALUE_CHANGED // Value changed (slider, switch, etc.)
LV_EVENT_KEY          // Key event
LV_EVENT_FOCUSED      // Object focused
LV_EVENT_DEFOCUSED    // Object lost focus
LV_EVENT_DRAW_MAIN    // Object being drawn
```

### Event Data

```cpp
void my_event_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  lv_obj_t * obj = lv_event_get_target(e);
  
  // Get user data
  void * user_data = lv_event_get_user_data(e);
  
  // For key events
  if(code == LV_EVENT_KEY) {
    uint32_t key = lv_event_get_key(e);
    if(key == LV_KEY_ENTER) {
      // Handle enter key
    }
  }
}
```

## Advanced Features

### Animations

```cpp
// Create animation
lv_anim_t a;
lv_anim_init(&a);

// Set target
lv_anim_set_var(&a, obj);

// Set values
lv_anim_set_values(&a, 0, 100);  // From, To

// Set property to animate
lv_anim_set_exec_cb(&a, (lv_anim_exec_xcb_t)lv_obj_set_x);

// Set duration and easing
lv_anim_set_time(&a, 1000);  // 1 second
lv_anim_set_ease(&a, LV_ANIM_EASE_OUT);

// Start animation
lv_anim_start(&a);

// Built-in animations
lv_obj_fade_in(obj, 500, 0);     // Fade in over 500ms
lv_obj_fade_out(obj, 500, 0);    // Fade out over 500ms
lv_obj_move_to(obj, 100, 100, LV_ANIM_ON);
```

### Screens and Navigation

```cpp
// Create multiple screens
lv_obj_t *scr1 = lv_obj_create(NULL);
lv_obj_t *scr2 = lv_obj_create(NULL);

// Load first screen
lv_scr_load(scr1);

// Switch to second screen with animation
lv_scr_load_anim(scr2, LV_SCR_LOAD_ANIM_MOVE_LEFT, 500, 0, false);
```

### Lists

```cpp
// Create a list
lv_obj_t *list = lv_list_create(lv_scr_act());
lv_obj_set_size(list, 200, 150);

// Add buttons to list
lv_obj_t *btn1 = lv_list_add_btn(list, LV_SYMBOL_FILE, "File 1");
lv_obj_t *btn2 = lv_list_add_btn(list, LV_SYMBOL_FILE, "File 2");
lv_obj_t *btn3 = lv_list_add_btn(list, LV_SYMBOL_DIRECTORY, "Folder");

// Add event to list buttons
lv_obj_add_event_cb(list, list_event_cb, LV_EVENT_CLICKED, NULL);
```

### Roller (Selector)

```cpp
// Create a roller
lv_obj_t *roller = lv_roller_create(lv_scr_act());
lv_roller_set_options(roller, 
  "Option 1\nOption 2\nOption 3\nOption 4", 
  LV_ROLLER_MODE_NORMAL);

// Set selected
lv_roller_set_selected(roller, 2, LV_ANIM_ON);

// Get selected
uint16_t sel = lv_roller_get_selected(roller);
const char *txt = lv_roller_get_options(roller);
```

### Dropdown

```cpp
// Create dropdown
lv_obj_t *dd = lv_dropdown_create(lv_scr_act());
lv_dropdown_set_options(dd, "Apple\nBanana\nCherry\nDate");

// Event
lv_obj_add_event_cb(dd, dropdown_event_cb, LV_EVENT_VALUE_CHANGED, NULL);
```

### Charts

```cpp
// Create a chart
lv_obj_t *chart = lv_chart_create(lv_scr_act());
lv_obj_set_size(chart, 200, 150);
lv_obj_set_pos(chart, 10, 10);

// Set type and range
lv_chart_set_type(chart, LV_CHART_TYPE_LINE);
lv_chart_set_range(chart, LV_CHART_AXIS_PRIMARY_Y, 0, 100);

// Add data series
lv_chart_series_t *ser = lv_chart_add_series(chart, 
  lv_palette_main(LV_PALETTE_BLUE), LV_CHART_AXIS_PRIMARY_Y);

// Set data points
lv_chart_set_next_value(chart, ser, 10);
lv_chart_set_next_value(chart, ser, 30);
lv_chart_set_next_value(chart, ser, 20);
lv_chart_set_next_value(chart, ser, 50);

// Refresh chart
lv_chart_refresh(chart);
```

## Best Practices

### Memory Management

```cpp
// Check free memory
Serial.printf("Free heap: %d\n", ESP.getFreeHeap());

// Clean up objects when switching screens
lv_obj_clean(scr);  // Remove all children

// Delete object
lv_obj_del(obj);

// Create objects statically when possible
static lv_obj_t *my_btn;  // Global or static
```

### Performance Tips

```cpp
// Use double buffering for smooth updates
static lv_color_t buf1[LV_HOR_RES_MAX * 10];
static lv_color_t buf2[LV_HOR_RES_MAX * 10];

// Reduce refresh rate for static screens
lv_disp_set_refr_timer(disp, 30);  // 30ms refresh

// Disable animations on low-memory systems
#define LV_USE_ANIMATION 0

// Use simple styles (less memory than complex ones)
```

### Responsive Design

```cpp
// Get screen dimensions
lv_coord_t w = lv_disp_get_hor_res(NULL);
lv_coord_t h = lv_disp_get_ver_res(NULL);

// Percentage-based sizing
lv_obj_set_width(obj, w * 0.8);  // 80% of screen width

// Use flexbox for responsive layouts
lv_obj_set_flex_flow(cont, LV_FLEX_FLOW_ROW_WRAP);
```

## Troubleshooting

### Screen Flickering

**Problem**: UI flickers or tears

**Solutions:**
1. Enable double buffering (2 buffers)
2. Check `lv_timer_handler()` called regularly
3. Use `tft.startWrite()`/`tft.endWrite()` in flush callback
4. Lower display SPI frequency

### Out of Memory

**Problem**: Crash or no UI displayed

**Solutions:**
1. Reduce buffer size
2. Enable PSRAM
3. Simplify UI (fewer objects)
4. Delete unused screens
5. Use static allocation where possible

### Touch Not Working

**Problem**: Touch input not detected

**Solutions:**
1. Verify touch driver configuration
2. Calibrate touch screen
3. Check LV_USE_INDEV_TOUCHSCREEN enabled
4. Use button navigation as fallback

### Slow Performance

**Problem**: UI sluggish or unresponsive

**Solutions:**
1. Reduce screen resolution
2. Use simpler widgets
3. Disable animations
4. Increase `lv_timer_handler()` frequency
5. Optimize display flush callback

## Example Projects

### Project 1: Settings Menu

Create a settings interface:
```cpp
// Screen with multiple settings controls
// Brightness slider
// Volume slider
// WiFi enable switch
// Theme selector (roller)
// Save/Cancel buttons
```

### Project 2: Media Player UI

Music player interface:
```cpp
// Album art display
// Song title and artist labels
// Progress bar
// Play/Pause button
// Previous/Next buttons
// Volume slider
```

### Project 3: Smart Home Dashboard

Control panel for IoT devices:
```cpp
// Grid of device cards
// Toggle switches for lights
// Temperature display with chart
// Camera preview window
// Notification list
```

## Next Steps

- **Complete Projects**: Integrate GUI with full application logic
- **Custom Widgets**: Create your own LVGL widgets
- **Internationalization**: Multi-language support
- **Fonts**: Custom fonts and icon fonts

## Reference Tables

### LVGL Widgets

| Widget | Use Case | Key Functions |
|--------|----------|---------------|
| Label | Text display | `lv_label_set_text()` |
| Button | Click actions | `lv_obj_add_event_cb()` |
| Slider | Value selection | `lv_slider_set_value()` |
| Switch | Toggle on/off | `lv_obj_has_state()` |
| Checkbox | Multiple options | `lv_checkbox_set_text()` |
| Progress Bar | Progress indication | `lv_bar_set_value()` |
| Image | Display images | `lv_img_set_src()` |
| List | Menu items | `lv_list_add_btn()` |
| Roller | Single selection | `lv_roller_set_selected()` |
| Dropdown | Compact selection | `lv_dropdown_set_options()` |
| Chart | Data visualization | `lv_chart_add_series()` |
| Text Area | Text input | `lv_textarea_set_text()` |
| Keyboard | Virtual keyboard | `lv_keyboard_set_textarea()` |

### Built-in Symbols

```cpp
LV_SYMBOL_AUDIO      // Audio
LV_SYMBOL_VIDEO      // Video
LV_SYMBOL_LIST       // List
LV_SYMBOL_OK         // OK
LV_SYMBOL_CLOSE      // Close
LV_SYMBOL_POWER      // Power
LV_SYMBOL_SETTINGS   // Settings
LV_SYMBOL_HOME       // Home
LV_SYMBOL_DIRECTORY  // Folder
LV_SYMBOL_FILE       // File
LV_SYMBOL_WIFI       // WiFi
LV_SYMBOL_BATTERY    // Battery
LV_SYMBOL_BLUETOOTH  // Bluetooth
// ... many more
```

Use with labels: `lv_label_set_text(label, LV_SYMBOL_HOME " Home");`
