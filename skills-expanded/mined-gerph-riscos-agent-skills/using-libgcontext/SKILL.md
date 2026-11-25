---
name: using-libgcontext
description: Guidance for using the GContext graphics library on RISC OS for drawing primitives and rendering text. Use when the agent needs to implement screen output, handle font metrics, or manage graphics contexts.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(curl:*) Bash(python3:*)
---

# Using GContext

The GContext library provides an abstracted interface for 2D graphics operations.

## Core Concepts

### Graphics Context
All operations require a `gcontext_t` pointer.

Use one of these initialisers depending on the backend you need:

* `gcontext_initvdu(2)` for normal rendering through VDU/Font output.
* `gcontext_initdrawfile(filename)` to construct a DrawFile and write it on finalisation.
* `gcontext_initdrawfilememory(memory, memorysize)` to construct a DrawFile in memory.

When finished with any backend, release it with `gcontext_destroy(gc)`.

### Coordinate System
- Coordinates are standard RISC OS OS-units.
- Y-axis typically increases upwards.
- For text painting, the coordinates specified are for the **baseline** of the string.

### Colours
- Use `colour_t` for all colour parameters.
- Use `COLOUR_RGB(r, g, b)` to create a colour value.
- Use `COLOUR_NONE` to skip drawing (e.g., for transparent backgrounds).

## Workflows

### VDU Rendering
1.  Initialise the context with `gcontext_initvdu(...)`.
2.  Draw shapes and text through the function pointers in `gcontext_t`.
3.  Release the context with `gcontext_destroy(gc)`.

### DrawFile Rendering
1.  Initialise the context with `gcontext_initdrawfile(...)` or `gcontext_initdrawfilememory(...)`.
2.  Draw through the normal `gcontext_t` plotting and text interfaces.
3.  Finalise the DrawFile with `gcontext_drawfile_finalise(gc)`.
4.  Release the context with `gcontext_destroy(gc)`.

The DrawFile backend accumulates the generated content in memory until finalisation.
Even file-backed output is serialised in memory first and only written to the destination
file during `gcontext_drawfile_finalise(gc)`.

If you need to size a memory buffer before rendering, create a sizing context with
`gcontext_initdrawfilememory(NULL, 0)`, perform the drawing, call
`gcontext_drawfile_datasize(gc)`, destroy that context, then create a second memory-backed
context with a buffer of the required size and render again before finalising.

### Drawing Primitives
1.  Initialize the context.
2.  Use `rectangle_fill` or `rectangle_outline` for boxes.
3.  For lines, use the sequence: `line_start(gc, colour)`, then one or more `line_line(gc, x0, y0, x1, y1)`, and finally `line_end(gc)`.
4.  Filled polygons can use `fill_start`, `fill_move`, `fill_line`, `fill_close`, and `fill_end` when the backend supports them.

### Rendering Text
1.  Find a font using `text_findfont(gc, name, xsize, ysize)`.
2.  Calculate dimensions if needed using `text_getstringsize`. **Crucial**: Use the `xoffset` field of `stringbounds_t` for advancing the cursor horizontally, as it accounts for character spacing correctly. The total width of the string is `bounds.xoffset + bounds.rbearing`.
3.  Paint text using `text_paint(gc, font, xb, yb, bg, fg, str, len)`. Use `GCONTEXT_ZEROTERM` for the length if the string is null-terminated.
4.  Release the font when finished using `text_losefont(gc, font)`.

For aligned text in a bounding box, use `text_paintattrib` with `FONTATTRIB_ALIGN_*`
and `FONTATTRIB_UNDERLINE`.

### Clipping
Use `clip_rectangle(gc, &bbox)` to request clipping and `clip_rectangle(gc, NULL)` to reset it.

For DrawFile output this is not represented as a Draw clipping object; the backend only
suppresses objects that are wholly outside the requested clip area.

## Installation and Setup

### Linking
Link against the GContext library in your `Makefile,fe1`:
```makefile
LIBS = ${CLIB} C:GContext.o.libGContext
```

The DrawFile backend is implemented in a separate object inside the library so code which
only uses the VDU entry points does not need to reference the DrawFile initialisers or
finalisation routines.

### Environment
Ensure `C$Path` includes the directory containing the GContext library. In `.robuild.yaml`, you can add:
```yaml
- Set C$Path @.Lib.,<C$Path>
```
(Assuming the library is extracted to a `Lib` directory in your project root).

### Continuous Integration (GitHub Actions)
To use GContext in CI, download and extract the library:
```yaml
- name: Obtain the GContext library
  run: |
    curl -s -L -o libgcontext.zip https://github.com/gerph/riscos-gcontext/releases/download/v0.05/GContext-0.05.zip
    python3 -m rozipfile --verbose --extract libgcontext.zip
    rm libgcontext.zip
```

## API Reference

See [api.md](references/api.md) for detailed structure definitions and function pointer signatures.
