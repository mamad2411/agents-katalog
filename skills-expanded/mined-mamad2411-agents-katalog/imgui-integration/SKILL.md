---
name: imgui-integration
description: Explains how to integrate and use Dear ImGui (ocornut/imgui), the immediate-mode C++ GUI library, including backend selection (DX9-12, OpenGL2/3, Vulkan, GLFW, SDL2/3, Win32, Metal, Android, etc.), the per-frame render loop, and widget/API usage snippets. Use when a user is writing or debugging C++ code that uses Dear ImGui, asks how to add an in-game/tool debug UI, or needs an ImGui widget code example. Infra-agnostic (C++ desktop/game tooling) — not part of the Build1 Ollama/PocketBase/Cognee/FastMCP/HTMX-Alpine stack; produces code for the user's own native build, not for the Build1 web frontend.
icon: layout-panel-top
color: Teal
---

# Dear ImGui Integration Skill

Dear ImGui (https://github.com/ocornut/imgui) is a bloat-free, immediate-mode GUI
library for C++ with minimal dependencies. It is a **code library integrated into a
user's own C++ project** — this skill produces integration code and widget snippets
for the user to paste into their own codebase; it cannot compile or run C++.

## Core structure to know

- `imgui.h` / `imgui.cpp` — core API and main widget implementations.
- `imgui_widgets.cpp`, `imgui_draw.cpp`, `imgui_tables.cpp`, `imgui_demo.cpp` —
  additional widget/draw/table code and the full interactive demo
  (`ImGui::ShowDemoWindow()` — always point users here for live examples).
- `backends/` — platform/renderer glue, one pair of files per backend, e.g.
  `imgui_impl_opengl3.*`, `imgui_impl_glfw.*`, `imgui_impl_sdl2.*`, `imgui_impl_dx11.*`,
  `imgui_impl_dx12.*`, `imgui_impl_vulkan.*`, `imgui_impl_win32.*`, `imgui_impl_metal.*`,
  `imgui_impl_android.*`, `imgui_impl_allegro5.*`, `imgui_impl_glut.*`,
  `imgui_impl_osx.*`, `imgui_impl_null.*`.
- `examples/` — one buildable example project per platform/renderer combo.
- `docs/` — FAQ, integration notes, changelog.

## How to help a user

1. **Determine their platform + renderer** (e.g. "GLFW + OpenGL3", "Win32 + DirectX11",
   "SDL2 + Vulkan"). Map this to exactly two backend file pairs: one platform backend
   (input/windowing) + one renderer backend (drawing).
2. **Explain the integration shape** (use the real, well-known call sequence — do not
   invent APIs):
   - Add `imgui.cpp`, `imgui_draw.cpp`, `imgui_widgets.cpp`, `imgui_tables.cpp`,
     `imgui_demo.cpp` plus the two chosen backend files to the build.
   - Init once: `ImGui::CreateContext();` then the platform init (e.g.
     `ImGui_ImplGlfw_InitForOpenGL(window, true)`) and renderer init (e.g.
     `ImGui_ImplOpenGL3_Init("#version 130")`).
   - Per-frame loop:
     ```cpp
     ImGui_ImplOpenGL3_NewFrame();
     ImGui_ImplGlfw_NewFrame();
     ImGui::NewFrame();

     // ... build UI here with ImGui:: calls ...

     ImGui::Render();
     ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
     ```
   - Shutdown: call each backend's `_Shutdown()` then `ImGui::DestroyContext()`.
3. **Widget snippets** — give the smallest correct example for the requested widget:
   ```cpp
   ImGui::Begin("My Window");
   ImGui::Text("Hello, world %d", 123);
   if (ImGui::Button("Save")) { /* ... */ }
   ImGui::SliderFloat("float", &my_float, 0.0f, 1.0f);
   ImGui::Checkbox("Demo Window", &show_demo_window);
   ImGui::End();
   ```
   Tables: `ImGui::BeginTable`/`TableNextRow`/`TableNextColumn`/`EndTable`. Menus:
   `BeginMainMenuBar`/`BeginMenu`/`MenuItem`/`EndMenu`/`EndMainMenuBar`.
4. **Point to the demo** for anything non-trivial:
   `ImGui::ShowDemoWindow(&show_demo_window)` in `imgui_demo.cpp` is the canonical
   reference for nearly every widget and pattern.
5. **Never claim to run/build it.** State clearly that the code must be compiled by the
   user in their own project; explain build-system wiring (CMake/Premake/manual) at a
   conceptual level only — do not attempt to invoke a compiler in the sandbox.

## Language bindings note

If the user is not using C++, mention that community bindings exist for other
languages (e.g. Python via `pyimgui`, Rust, C#), but this repo is the canonical C++
implementation.

## Build1 Integration

None. This skill is entirely infra-agnostic native desktop/game tooling and has no
overlap with Ollama, PocketBase, Cognee, FastMCP, or HTMX/Alpine. If a user's actual
goal is a debug UI *for* a Build1 service, redirect them to an HTMX/Alpine-based web
UI instead of ImGui, since ImGui only targets native C++ applications, not the browser.
