---
name: riscos-output
description: Details of how the RISC OS output system works. Use when creating text and graphics output using text positioning, graphics, drawing shapes, sprites, fonts, sprite areas, palette programming, ImageFileRender, or ColourTrans translation tables. It is not needed for plain textual output.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS text and graphics output

This skill covers writing text, graphics, and fonts to the screen or other
output devices on RISC OS.

For graphical text, font, rectangle, and line rendering, the GContext library
can be used.

## Boundaries

Use this skill when the task involves:

* VDU output and control sequences
* `OS_Plot` graphics
* Draw and DrawFile rendering
* Font Manager usage
* sprite creation, plotting, redirection, or file layout
* palette programming or `ColourTrans`
* screen mode selection or mode decoding
* `ImageFileRender`

It is not needed for plain textual output that does not involve positioning,
graphics, fonts, sprites, or palette handling.

## Terminology

* VDU output covers character and control codes written through `OS_WriteC`,
  `OS_WriteN`, and `OS_Write0`.
* Graphics output covers `OS_Plot`, sprite rendering, font rendering, and
  related drawing systems.
* Draw provides path-based vector graphics through `Draw_*` SWIs.
* Outline fonts are provided through the Font Manager via `Font_*` SWIs.
* Sprites are raster images rendered through `OS_SpriteOp`.
* Sprite areas are in-memory collections of sprites; sprite files are their
  on-disc representation.
* `ImageFileRender` renders complete image files without the caller needing to
  know whether the source is JPEG, DrawFile, Sprite, PNG, or another supported
  format.
* Modes define resolutions, pixel geometry, and colour depth.
* `ColourTrans` is used for colour selection and translation in mode-independent
  code and for sprite translation tables.

## Coordinate system

### Graphics

Graphics coordinates on RISC OS use:

* Y=0 at the bottom, positive upwards
* X=0 at the left, positive rightwards
* units which are usually double the screen resolution

Before declaring graphics code complete, check that the coordinates really are
correct.

### Text

Text coordinates on RISC OS use:

* Y=0 at the top, positive downwards
* X=0 at the left, positive rightwards

To write text at a specific text-cell position, use `VDU 31, <xchar>, <ychar>`.
Text characters are 8 pixels by 8 pixels.

## Common gotchas

* Text and graphics coordinates do not share the same origin.
* Sprite plotting normally needs a `ColourTrans` translation table to match the
  destination mode correctly.
* Sprite row 0 is the bottom row, not the top row.
* If code reads or writes the framebuffer directly, remove cursors first and
  restore them afterwards.
* While output is redirected to a sprite, do not call `Wimp_Poll`.
* If a saved screen image is paletted, preserve and restore the palette block
  as well as the pixel data.

## Task selection

Choose the smallest useful subsystem for the task:

* For VDU control sequences and textual cursor movement, read
  [references/vdu-codes.md](references/vdu-codes.md).
* For simple line, point, rectangle, and shape plotting, read
  [references/os_plot.md](references/os_plot.md).
* For Draw paths, filled shapes, and DrawFile object layout, read
  [references/draw.md](references/draw.md) and
  [references/drawfile.md](references/drawfile.md).
  If the task is a viewer or plug-in that must fit a DrawFile into a Wimp redraw box, read `references/drawfile.md` early.
* For Font Manager usage, sizing, rendering, and colour handling, start with
  [references/fonts-overview.md](references/fonts-overview.md), then read the
  focused font references listed there.
* For `ColourTrans`, start with
  [references/colourtrans-overview.md](references/colourtrans-overview.md),
  then read the focused colour references listed there.
* For screen modes and mode decoding, start with
  [references/modes-overview.md](references/modes-overview.md), then read the
  focused mode references listed there.
* For sprites, start with
  [references/sprites-overview.md](references/sprites-overview.md), then read
  the focused sprite references listed there.
* For framebuffer access, pointer-driver quirks, or palette restoration, read
  [references/framebuffer-and-palettes.md](references/framebuffer-and-palettes.md).
* For general image-file rendering, read
  [references/imagefilerender.md](references/imagefilerender.md).

## Cross-skill routing

* When implementing image converter modules, use
  `riscos-graphics-converters` as well as this skill.
* When using the Toolbox ImageFileGadget, use
  `using-toolbox-imagefilegadget` as well as this skill.
* For higher-level graphics primitives and font handling through a library
  rather than raw SWIs, consider `using-libgcontext`.

## Image File Converters

This skill covers the sprite, palette, mode, and rendering details needed by
image converters, but it does not define the `ImageFileConvert` registration
interface. When creating modules which convert image formats to Sprite, use the
`riscos-graphics-converters` skill as well.

When creating converters whose destination is DrawFile, use the Draw and
DrawFile references in this skill for object layout, coordinate conversion,
paths, text objects, sprite objects, font tables, and bounding-box handling.
Use `riscos-graphics-converters` for registration, converter entry points,
caching, and validation workflow.

## ImageFileRender

Use `ImageFileRender` for general image files that should be drawn to the
screen, printer, or a Wimp redraw context without the caller needing to know
whether the file is a JPEG, DrawFile, Sprite, PNG, or a third-party format.

For direct screen rendering, load the file into memory, derive the RISC OS
filetype from the load address, choose one of the transform modes, and call
`ImageFileRender_Render`. Use `ImageFileRender_BBox` when layout code needs the
natural or transformed extent first, and set a graphics window (`VDU 24`) or
use redraw rectangles for clipping.

For new renderers, implement and register an ImageFileRender renderer. Read
[references/imagefilerender.md](references/imagefilerender.md) for the calling
sequences, structures, flags, and renderer registration workflow. For Toolbox
ImageFileGadget method usage, use the `using-toolbox-imagefilegadget` skill.

The public master documentation is:
https://gerph.github.io/riscos-prminxml-staging/prm/html/select/graphics/imagefilerender.html

## Reference index

* VDU control codes: [references/vdu-codes.md](references/vdu-codes.md)
* `OS_Plot` operations: [references/os_plot.md](references/os_plot.md)
* Draw paths: [references/draw.md](references/draw.md)
* DrawFiles: [references/drawfile.md](references/drawfile.md)
* Font quick reference: [references/fonts-overview.md](references/fonts-overview.md)
* `ColourTrans` quick reference: [references/colourtrans-overview.md](references/colourtrans-overview.md)
* Mode quick reference: [references/modes-overview.md](references/modes-overview.md)
* Sprite quick reference: [references/sprites-overview.md](references/sprites-overview.md)
* Framebuffer and palette handling: [references/framebuffer-and-palettes.md](references/framebuffer-and-palettes.md)
* ImageFileRender: [references/imagefilerender.md](references/imagefilerender.md)
