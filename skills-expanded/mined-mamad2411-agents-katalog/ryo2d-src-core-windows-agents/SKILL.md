# Dev Window Agents

This document describes the development tool windows available in Ryo2D and provides guidance for creating new ones.

## Architecture Overview

Dev windows in Ryo2D are standalone winit windows that share GPU resources with the main game renderer. This architecture provides several benefits:

- **Zero performance impact**: Each window renders independently with its own surface and throttled frame rate
- **Live data sharing**: Windows can read engine state via shared references and message channels
- **Focus-aware throttling**: The main game only throttles when ALL windows (game + dev tools) lose focus

### Resource Sharing

All dev windows receive `Arc` references to:
- `wgpu::Device` - Shared GPU device for buffer/texture creation
- `wgpu::Queue` - Shared command queue for rendering

Each window creates its own:
- `wgpu::Surface` - Independent swap chain
- Pixel buffer - CPU-side rendering for full control

## Available Windows

### Profiler Window (`profiler_window`)

**Feature flag**: `profiler` (requires `--features profiler`)

**Configuration**: `Ryo.toml`
```toml
[debug]
enable_profiler = true
```

A real-time flamegraph profiler showing:
- CPU timing per frame phase (input, update, physics, render)
- GPU timing for draw calls
- Frame time histogram
- Scope hierarchy from `puffin` instrumentation

**Usage in code**:
```rust
puffin::profile_scope!("my_expensive_operation");
// ... code to profile
```

### Logger Window (`logger_window`)

**Configuration**: `Ryo.toml`
```toml
[debug]
logger_window = true
```

A live log viewer showing runtime messages with:
- Log levels: Trace, Debug, Info, Warn, Error
- Context labels: Engine, Game, External
- Filtering by level (click buttons)
- Auto-scroll with manual override
- Timestamps for each entry

**Usage in code**:
```rust
use ryo2d::core::dev_log::{engine_info, game_debug, external_warn};

// Engine context (core systems)
engine_info!("Renderer initialized with {} shaders", count);
engine_debug!("Frame timing: {:?}", delta);

// Game context (gameplay code)
game_info!("Player spawned at {:?}", position);
game_warn!("Low health: {}", hp);

// External context (plugins, mods, third-party)
external_info!("Plugin loaded: {}", name);
```

## Creating New Dev Windows

Use the `DevWindowRenderer` framework to create new tool windows.

### Basic Structure

```rust
use crate::core::windows::{colors, DevWindowConfig, DevWindowRenderer, CHAR_WIDTH, CHAR_HEIGHT};
use std::sync::Arc;
use winit::event_loop::ActiveEventLoop;

pub struct MyToolWindow {
    renderer: DevWindowRenderer,
    // Your window-specific state
    data: Vec<MyData>,
}

impl MyToolWindow {
    pub fn new(
        event_loop: &ActiveEventLoop,
        device: Arc<wgpu::Device>,
        queue: Arc<wgpu::Queue>,
        instance: &wgpu::Instance,
        adapter: &wgpu::Adapter,
    ) -> Option<Self> {
        let config = DevWindowConfig {
            title: "My Tool".to_string(),
            width: 800,
            height: 600,
            render_throttle_ms: 100, // 10 FPS
        };

        let renderer = DevWindowRenderer::new(
            event_loop, device, queue, instance, adapter, config
        ).ok()?;

        Some(Self {
            renderer,
            data: Vec::new(),
        })
    }

    pub fn window_id(&self) -> winit::window::WindowId {
        self.renderer.window_id()
    }

    pub fn render(&mut self) {
        if !self.renderer.should_render() {
            return;
        }

        self.renderer.clear(colors::BACKGROUND);

        // Draw your content
        self.renderer.draw_text("My Tool Window", 10, 10, colors::TEXT);
        self.renderer.draw_rect(10, 30, 100, 20, colors::ACCENT);

        self.renderer.present();
        self.renderer.mark_rendered();
    }

    pub fn handle_event(&mut self, event: &winit::event::WindowEvent) -> bool {
        // Handle window events (resize, input, etc.)
        // Return true if the event was consumed
        false
    }
}
```

### Integration with Engine

Add your window to `engine.rs`:

1. Add field to `Engine` struct:
```rust
my_tool_window: Option<super::windows::my_tool_window::MyToolWindow>,
```

2. Create window in `create_dev_windows()`:
```rust
if self.config.debug.my_tool_window
    && let Some(ref renderer) = self.renderer
{
    self.my_tool_window = super::windows::my_tool_window::MyToolWindow::new(
        event_loop,
        renderer.device_arc(),
        renderer.queue_arc(),
        renderer.instance(),
        renderer.adapter(),
    );
}
```

3. Handle events in `window_event()`:
```rust
if let Some(ref mut window) = self.my_tool_window {
    if window.window_id() == window_id {
        window.handle_event(event);
        return;
    }
}
```

4. Render in `about_to_wait()`:
```rust
if let Some(ref mut window) = self.my_tool_window {
    window.render();
}
```

### Drawing API

`DevWindowRenderer` provides these drawing primitives:

| Method | Description |
|--------|-------------|
| `clear(color)` | Fill entire buffer with color |
| `draw_pixel(x, y, color)` | Set single pixel |
| `draw_rect(x, y, w, h, color)` | Filled rectangle |
| `draw_rect_outline(x, y, w, h, color)` | Rectangle outline (1px border) |
| `draw_text(text, x, y, color)` | Render text using bitmap font |
| `draw_char(c, x, y, color)` | Render single character |
| `present()` | Copy buffer to GPU and present |

### Color Palette

The `colors` module provides a consistent dark theme:

| Constant | Usage |
|----------|-------|
| `BACKGROUND` | Window background (dark gray) |
| `PANEL` | Raised panel background |
| `TEXT` | Primary text (white) |
| `TEXT_DIM` | Secondary/disabled text |
| `ACCENT` | Highlights, active elements (blue) |
| `SUCCESS` | Positive indicators (green) |
| `WARNING` | Caution indicators (yellow) |
| `ERROR` | Error indicators (red) |
| `GRID` | Grid lines, separators |

### Best Practices

1. **Throttle rendering**: Use `render_throttle_ms` to limit FPS (50-100ms for most tools)

2. **Check should_render()**: Always call before drawing to respect throttle

3. **Handle resize**: The renderer auto-handles resize, but you may need to adjust layout

4. **Use consistent colors**: Stick to the `colors` module for visual consistency

5. **Keep it lightweight**: Dev tools should have minimal impact on the main game

6. **Document your window**: Add it to this file and update the README

## Future Window Ideas

- **ECS Inspector**: Entity browser with component values
- **Asset Browser**: Preview loaded textures, sounds, shaders
- **Console**: Interactive REPL for runtime debugging
- **Network Monitor**: Connection status, packet inspector
- **Memory Profiler**: Allocation tracking, leak detection
- **Scene Graph**: Visual hierarchy of entities
- **Shader Debugger**: Live shader editing with hot reload
