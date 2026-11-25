---
name: using-toolbox-imagefilegadget
description: Use when writing, reviewing, or debugging RISC OS Toolbox applications that use the ImageFileGadget object or its methods, including ImageFileGadget_SetValue, SetTransform, SetQuality, SetColourMap, SetScroll, GetBounds, and ImageFileGadget_MouseClick events.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Toolbox ImageFileGadget

Use this skill when application code uses the Toolbox ImageFileGadget object to
display image files in a Toolbox Window. ImageFileGadget is a client of
ImageFileRender: the application supplies image file bytes and metadata, and
the gadget performs redraws by calling `ImageFileRender_Render`.

For direct image rendering or for implementing new filetype renderers, use the
`riscos-output` skill and read its `references/imagefilerender.md` reference.
New image file format support is registered with ImageFileRender, not with
ImageFileGadget. Once a renderer is registered for a filetype, ImageFileGadget
can render that filetype through its normal `SetValue` method.

## Application Workflow

1. Include the ImageFileGadget Toolbox headers and use a Toolbox resource which
   contains an ImageFileGadget component.
2. Load the image file into memory and determine its RISC OS filetype, normally
   from `(load_address >> 8) & &FFF`.
3. Call `ImageFileGadget_SetValue` with the filetype, data pointer, and data
   length.
4. Optionally call `ImageFileGadget_SetIndex`, `SetQuality`, `SetColourMap`,
   `SetTransform`, or `SetScroll` to configure how the image is displayed.
5. Register a Toolbox handler for `ImageFileGadget_MouseClick` if the
   application needs image-coordinate mouse interaction.

Applications do not need to register the gadget type with the Toolbox Window
object. That is internal module setup done by ImageFileGadget itself.

## Template and Flags

The ImageFileGadget template extends a normal Toolbox `GadgetHeader`:

```c
typedef struct {
    GadgetHeader hdr;
    int event;
    unsigned int unused;
    unsigned int background;
} ImageFileGadget;
```

Useful gadget flags:

| Flag | Meaning |
|------|---------|
| `ImageFileGadget_NoBorder` | Disable the gadget border |
| `ImageFileGadget_ColourMapWhole` | Apply colour mapping to the whole gadget area |

## Public Methods

| Method | Purpose |
|--------|---------|
| `ImageFileGadget_SetValue(flags, window, component, filetype, data, length)` | Set the image bytes and filetype |
| `ImageFileGadget_GetValue(flags, window, component, &filetype, &data, &length)` | Read the current filetype, data pointer, and length |
| `ImageFileGadget_SetColour` / `GetColour` | Set or read the background colour |
| `ImageFileGadget_SetState` / `GetState` | Set or read gadget state bits |
| `ImageFileGadget_SetIndex` / `GetIndex` | Select or read the image sequence number |
| `ImageFileGadget_SetQuality` / `GetQuality` | Select or read the ImageFileRender quality level |
| `ImageFileGadget_SetColourMap` | Supply a colour map descriptor |
| `ImageFileGadget_SetTransform` | Set the ImageFileRender transform type and transform data |
| `ImageFileGadget_SetScroll` / `GetScroll` | Set or read the scroll position |
| `ImageFileGadget_GetBounds` | Read bounds for the current image and transform |

`ImageFileGadget_DesktopColours` is used with colour methods when the colour is
a desktop colour. `ImageFileGadget_ImageCoords` is used with scroll methods
when scroll positions are in image coordinates.

## Transform and Display

`ImageFileGadget_SetTransform` uses the same transform types and data blocks as
ImageFileRender:

| Transform type | Data |
|----------------|------|
| `TRANSFORMTYPE_SIZE` | 16-byte to-fit block: width, height, border, angle |
| `TRANSFORMTYPE_SCALE` | Standard 16-byte scale block: xmult, ymult, xdiv, ydiv |
| `TRANSFORMTYPE_TRANSFORM` | Six-word standard transform matrix |

The gadget computes display size with `ImageFileRender_BBox`, then redraws
inside Wimp redraw rectangles using `ImageFileRender_Render`. It normally uses
`FLAG_IGNORE_DOCUMENT_OFFSET`, optional `FLAG_COLOURMAP`, and
`quality << FLAG_QUALITY_SHIFT`.

If code needs the actual ImageFileRender register contract or transform block
formats, read the `riscos-output` ImageFileRender reference.

## Mouse Events

Mouse events are raised as `ImageFileGadget_MouseClick`. The event block is:

```c
typedef struct {
    ToolboxEventHeader hdr;
    unsigned int flags;
    int smousex;
    int smousey;
    int imousex;
    int imousey;
} ImageFileGadgetMouseClickEvent;
```

`smousex` and `smousey` are screen coordinates within the gadget. `imousex` and
`imousey` are image coordinates computed by inverting the ImageFileRender
transform.

Mouse event flags:

| Flag | Meaning |
|------|---------|
| `ImageFileGadget_MouseClick_Flags_DoubleClick` | Double-click |
| `ImageFileGadget_MouseClick_Flags_AdjustClick` | Adjust button was used |
| `ImageFileGadget_MouseClick_Flags_StartDrag` | Drag start |
| `ImageFileGadget_MouseClick_Flags_MenuClick` | Menu button was used |
| `ImageFileGadget_MouseClick_Flags_XInImage` | X coordinate is inside image bounds |
| `ImageFileGadget_MouseClick_Flags_XLow` | X coordinate is below image bounds |
| `ImageFileGadget_MouseClick_Flags_XHigh` | X coordinate is above image bounds |
| `ImageFileGadget_MouseClick_Flags_YInImage` | Y coordinate is inside image bounds |
| `ImageFileGadget_MouseClick_Flags_YLow` | Y coordinate is below image bounds |
| `ImageFileGadget_MouseClick_Flags_YHigh` | Y coordinate is above image bounds |

## Debugging

Use `*ImageFileRenderers` to confirm that a renderer is registered for the
filetype being supplied to `ImageFileGadget_SetValue`.

If the image is blank, check:

* The file data pointer remains valid for as long as the gadget needs it.
* The filetype matches the image data.
* A renderer exists for that filetype.
* The transform data matches the selected transform type.
* The quality value is in the ImageFileRender range 0-15.
* Scroll values are using the expected coordinate system.
