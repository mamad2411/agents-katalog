---
name: riscos-graphics-converters
description: Create or update RISC OS image converter modules, especially ImageFileConvert converters that register source-to-destination file type pairs, implement Convert and MiscOp entry points, emit Sprite or sprite-file output, handle ImageFileConvert service startup and shutdown, or call ImageFileConvert SWIs directly to convert image buffers and files.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-amu:*)
---
# RISC OS Graphics Converters

Use this skill when creating, porting, reviewing, or calling RISC OS image
conversion code. Use `riscos-output` as well when the converter emits sprites,
palettes, masks, Draw files, plots, fonts, or any other RISC OS graphics
output format.

## ImageFileConvert Modules

ImageFileConvert converter modules register one or more file type pairs. The
pair word has destination file type in bits 0-11 and source file type in bits
16-27. For example Clear (`&690`) to Sprite (`&FF9`) is:

```c
#define CONVERT_FILETYPE ((0x690 << 16) | 0xFF9)
```

Register with `ImageFileConvert_Register` using a `converterdef_t`:

```c
converterdef_t def;

def.api = CONVERTER_API_VERSION;     /* 100 */
def.flags = CONVERTER_VALID;         /* 0 */
def.type = CONVERT_FILETYPE;
def.name = "Module\t0.01\tAuthor";
def.private = pw;
def.convert = sprite_convert_Entry;
def.miscop = sprite_miscop_Entry;
```

Include these headers when available:

```c
#include "ImageFileConvert/ImageFileConvert.h"
#include "ImageFileConvert/ImageFileConvertSWIs.h"
#include "ImageFileConvert/converters.h"
```

Use the ImageFileConvert include path in the makefile:

```make
INCLUDES = <Lib$Dir>.ImageFileConvert.
```

Converters do not have to target Sprite. A vector converter can register a
pair such as WMF (`&B2F`) to DrawFile (`&AFF`). If the destination format is
renderable through ImageFileRender, ImageFileConvert may expose useful
intermediate routes through that destination. For example, a WMF to DrawFile
converter can allow WMF to Sprite, SVG, PNG, BMP, or JPEG conversions through
existing DrawFile and Sprite converters.

## CMHG And Veneers

Register converter entry points as generic veneers so ImageFileConvert can call
C handlers with a register block:

```cmhg
#include "ImageFileConvert.h"

service-call-handler: Mod_Service Service_ImageFileConvert_Started,
                                  Service_ImageFileConvert_ConverterChanged,
                                  Service_ImageFileConvert_Dying,
                                  Service_ModeChange

generic-veneers: sprite_convert_Entry/sprite_convert_Handler,
                 sprite_miscop_Entry/sprite_miscop_Handler
```

Declare the veneer entry symbols in C:

```c
extern void sprite_convert_Entry(void);
extern void sprite_miscop_Entry(void);
```

The C handlers usually have this shape:

```c
_kernel_oserror *sprite_convert_Handler(_kernel_swi_regs *r, void *pw);
_kernel_oserror *sprite_miscop_Handler(_kernel_swi_regs *r, void *pw);
```

## Registration Lifecycle

Initialisation should try to register if ImageFileConvert is already present,
but failure to register must not prevent the module from loading. Leave the
module quiescent and try again when `Service_ImageFileConvert_Started` is
received.

Recommended behaviour:

- `Mod_Init`: call a helper which attempts registration and returns `NULL`
  even if ImageFileConvert is absent.
- `Service_ImageFileConvert_Started`: attempt registration.
- `Service_ImageFileConvert_Dying`: mark cached registration state as false;
  do not call back into the dying module.
- `Mod_Final`: deregister only if this module believes it is registered.
- Display- or font-dependent converters may also need to listen for
  `Service_ModeChange` and discard cached converted output.

Avoid returning the `ImageFileConvert_Register` SWI error from module
initialisation unless the user explicitly wants the module to require
ImageFileConvert at load time.

## Convert Entry Point

ImageFileConvert calls the converter with registers based on
`ImageFileConvert_Convert`:

| Register | Meaning |
|----------|---------|
| R0 | conversion flags |
| R1 | file type pair |
| R2 | input buffer |
| R3 | input buffer length |
| R4 | output buffer, or 0 to query required size |
| R5 | output buffer length, or returned used/required size |
| R6 | background colour, often ignored |
| R7-R9 | passed through for converter-specific use |
| R12 | private word from the converter definition |

For Sprite destinations, bit 0 of R0 is
`Converter_Convert_Sprite_CreateSprite`. If set, return a bare sprite. If
clear, return a sprite file with the 12-byte sprite-area header before the
sprite.

For non-Sprite destinations, do not apply Sprite destination flags. If the
destination defines no flags, reject any set bits:

```c
#define CONVERT_RESERVED (~0u)
```

Reject unsupported flags with `err_ConverterBadFlags`. Use a narrow mask such
as:

```c
#define CONVERT_RESERVED (~Converter_Convert_Sprite_CreateSprite)
```

On successful size query (`R4 == 0`), set `r->r[5]` to the required byte
count. On successful conversion, set `r->r[5]` to the byte count used.

If the conversion engine streams output and discovers the final size by
running once, it is acceptable for the low-level writer to signal
`err_ConverterOutputBufferTooSmall` during a size query, provided the public
converter handler converts that into success once `R5` contains the required
size.


## Calling ImageFileConvert

Callers that use `ImageFileConvert_Convert` directly should use the same pair
word layout as converter registration: source file type in bits 16-27 and
destination file type in bits 0-11.

When building a caller that offers export choices to the user, enumerate the
available converter pairs first rather than hard-coding destination types.
`ImageFileConvert_EnumerateConverters` returns packed type pairs in the same
layout used by registration and conversion calls, so the caller can filter for
the current source type by comparing the high 16 bits:

```c
unsigned long pair = -1;

do
{
    _kernel_oserror *err;
    err = _swix(ImageFileConvert_EnumerateConverters,
                _INR(0,1) | _OUT(1),
                0, pair, &pair);
    if (err)
        pair = -1;
    else if (pair != (unsigned long)-1 &&
             (pair & 0xFFFF0000u) == (source_type << 16))
    {
        unsigned int destination_type = pair & 0xFFF;
        /* Offer this destination to the user. */
    }
} while (pair != (unsigned long)-1);
```

Practical points:

- Treat the packed pair as the durable identity of an export choice. If the UI
  needs to remember which menu entry or button the user picked, store the full
  pair and derive the destination type from it later.
- Derive the displayed name of the destination from the destination file type
  at UI-update time, for example through `OS_FSControl 18`, rather than keeping
  a private list of names.
- If enumeration fails or no pair matches the source type, present no export
  choices rather than guessing. An empty export list is safer than offering a
  conversion route that is not actually registered.

Recommended caller sequence:

- First call `ImageFileConvert_Convert` with `R4 == 0` and `R5 == 0` to query
  the required output size.
- Allocate an output buffer of the returned size and call again with `R4`
  pointing at the buffer and `R5` set to the buffer length.
- On success, use the returned `R5` as the actual output byte count; it may be
  smaller than the allocated size.
- Pass `-1` as the background colour when the conversion should use its natural
  background.

Some converters cannot know the output size cheaply. A successful size query
may return `R5 == -1`; in that case, retry conversion with a guessed buffer
size and grow it if ImageFileConvert returns the public "output buffer too
small" error (`&81ACCA`). A common fallback is to start with the input size and
increase geometrically, freeing failed buffers because their contents are not
useful.

To obtain a dynamic sprite area from a Sprite destination conversion, request
destination file type Sprite (`&FF9`) with Sprite flags clear so the converter
returns a sprite file. Allocate four extra bytes before the returned data and
store the total area size in the first word; the sprite-file header then follows
at word 1.

Use the same packed file type pair:

```c
unsigned int pair = (source_type << 16) | destination_type;
```

Caller-side register use is:

| Register | Meaning |
|----------|---------|
| R0 | conversion flags |
| R1 | file type pair |
| R2 | input buffer |
| R3 | input buffer length |
| R4 | output buffer, or 0 to query size |
| R5 | output buffer length, or returned output size |
| R6 | background colour, often `-1` for natural background |

Typical call:

```c
_swix(ImageFileConvert_Convert, _INR(0,6) | _OUT(5),
      flags, pair, src, srclen, dest, destlen, background, &used);
```

For file-to-file conversion:

1. Use `OS_File 20` to read the source file type and length.
2. Load the source file into memory.
3. Resolve a textual destination type with `OS_FSControl 31` if needed.
4. Pack the source and destination file types into `R1`.
5. Call `ImageFileConvert_Convert` first with `R4 = 0` and `R5 = 0` to query
   the required size.
6. If `R5` returns a concrete size, allocate that many bytes and call again.
7. Save the converted data with `OS_File 10` using the destination file type.

For a save or export dialogue driven by a shared UI object:

- use the stored converter pair to recover the destination file type when the
  user finally confirms the save
- set the save dialogue's file type from `pair & 0xFFF`
- derive the suggested leafname from the destination file type name, not from
  the current source filename alone
- when calling the conversion, pass the current source file type separately as
  a sanity check and prefer the destination from the enumerated pair rather
  than a free-form user-entered type

This keeps the eventual conversion consistent with the specific registered
route that was offered to the user.

Do not assume the size query always returns a usable final length. In practice,
some converters return `R5 == -1` to mean that the final size is not yet
known. In that case:

- start with a reasonable output buffer, commonly the input length
- call `ImageFileConvert_Convert`
- if the SWI returns public error `&81ACCA`, treat it as output buffer too
  small
- enlarge the buffer, commonly by doubling it
- retry until the conversion succeeds or a different error is returned

Use `-1` in `R6` unless the conversion specifically needs composition against
a chosen background colour.

For Sprite destinations, bit 0 of `R0` is still
`Converter_Convert_Sprite_CreateSprite`:

- set it to request a bare sprite
- clear it to request a sprite file, including the 12-byte sprite-area header

For non-Sprite destinations, do not set Sprite-specific flags.

## MiscOp Entry Point

For Sprite output converters, implement operation
`Converter_MiscOp_Sprite_ReadInfo` (`&400`) where possible. It allows callers
and render proxies to get image details without converting the full image.

For non-Sprite destinations, there may be no useful generic MiscOp. Returning
`err_ConverterUnknownMiscOp` is valid when no operation is supported.

Entry:

| Register | Meaning |
|----------|---------|
| R0 | flags |
| R1 | file type pair |
| R2 | input buffer |
| R3 | input buffer length |
| R4 | operation number |

Exit for `ReadInfo`:

| Register | Meaning |
|----------|---------|
| R0 | width in pixels |
| R1 | height in pixels |
| R2 | bits per pixel |
| R3 | image flags |
| R4 | X DPI |
| R5 | Y DPI |

Image flags include:

- `Converter_MiscOp_Sprite_ReadInfo_Palette` if the image has a palette.
- `Converter_MiscOp_Sprite_ReadInfo_Colour` for colour images.
- `Converter_MiscOp_Sprite_ReadInfo_Mask` if there is a mask or alpha channel.
- `Converter_MiscOp_Sprite_ReadInfo_Interlace_None` for normal non-interlaced
  images.

Return `err_ConverterUnknownMiscOp` for unrecognised operation numbers.

## Calling ImageFileConvert_MiscOp

Client code can call `ImageFileConvert_MiscOp` when only lightweight
image metadata is needed.

Use entry registers:

| Register | Meaning |
|----------|---------|
| R0 | flags |
| R1 | file type pair |
| R2 | input buffer |
| R3 | input buffer length |
| R4 | miscellaneous operation number |

For `Converter_MiscOp_Sprite_ReadInfo` (`&400`), expect:

| Register | Meaning |
|----------|---------|
| R0 | width in pixels |
| R1 | height in pixels |
| R2 | bits per pixel |
| R3 | image flags |
| R4 | X DPI |
| R5 | Y DPI |

Prefer `MiscOp` over full conversion when the user only needs dimensions, bit
depth, palette presence, mask presence, or interlace state.

## Converter Pseudo-Errors

Converter handlers may return ImageFileConvert pseudo-error pointers from
`converters.h`. ImageFileConvert maps them to its own public errors:

| Pseudo-error | Meaning |
|--------------|---------|
| `err_ConverterOutputBufferTooSmall` | output buffer too small |
| `err_ConverterBadFlags` | unsupported flags |
| `err_ConverterUnknownMiscOp` | unrecognised miscellaneous operation |
| `err_ConverterOutOfMemory` | conversion workspace allocation failed |
| `err_ConverterCorruptData` | source image is invalid or truncated |

Use these rather than inventing local error blocks for ordinary converter
failures.

For SWI callers, treat ordinary `_kernel_oserror` returns as the main
failure path. Special-case `&81ACCA` only inside the resize-and-retry path for
output buffers.

## Caching And Repeated Conversion

ImageFileRender proxying and intermediate conversions may cause the same source
data to be converted repeatedly. A common sequence is a size or bounding-box
request followed by a real conversion. Expensive converters, especially vector
or metafile converters, can cache the most recent converted output.

Practical cache guidance:

- Key the cache by input pointer, input length, and a checksum or content
  signature; pointer and length alone are not enough if buffers are reused.
- Clear the cache on failed conversion so stale output is never returned.
- If the cache grows dynamically, impose a sensible limit or use a dynamic area
  with a maximum size.
- If the conversion depends on display mode, font mapping, palettes, or other
  global rendering state, clear the cache on the relevant services such as
  `Service_ModeChange`.
- Always fall back to direct conversion if cache allocation or extension fails.

## DrawFile Destination Reminders

When emitting DrawFiles, use `riscos-output` Draw and DrawFile references for
object layout, coordinates, paths, text, sprites, and bounding boxes.

Useful patterns from WMF-style converters:

- Write the `draw_fileheader` first, then patch it again after all object
  bounding boxes have been accumulated.
- Initialise document and object bounding boxes to extreme values and merge
  each emitted object into the document bbox.
- Keep all object sizes word-aligned, including text strings and font tables.
- For path objects, emit MOVE, LINE, CURVE, CLOSE, and TERM elements exactly
  as required by DrawFile, and patch the path header after the element count
  and bbox are known.
- Convert embedded bitmap records into sprites and wrap them in
  `draw_OBJSPRITE` objects when a suitable bitmap-to-sprite converter is
  available.
- If text is emitted, maintain a DrawFile font table and use font mapping
  where possible; rotated text needs a transform and a transformed bbox.
- Document unsupported source primitives explicitly. Vector formats often
  contain operations that cannot be represented directly or are not worth
  supporting initially, such as clipping, raster operations, patterned fills,
  opacity, or complex brush modes.

## Sprite Output Reminders

When emitting a Sprite or sprite file, use `riscos-output` for the sprite
layout details. Important points:

- The sprite-file header is three words: sprite count, first sprite offset
  usually 16, and free offset.
- A bare sprite starts at the sprite header, without those 12 bytes.
- Paletted sprite palette entries are double words in `&BBGGRR00` style.
- Set `image` and `mask` offsets relative to the start of the sprite header.
- If there is no mask, set `mask == image`.
- Preserve exact row stride and `lbit`/`rbit` semantics; do not assume
  byte-width rows for packed low-depth sprites.

## Validation

Before declaring a converter complete:

- Build 32-bit with `riscos-amu`.
- Build 64-bit with `riscos-amu BUILD64=1` when the project supports it.
- Test that the converter module loads successfully without ImageFileConvert
  present, if it is intended to be quiescent.
- Test with ImageFileConvert loaded and call both `MiscOp &400` and
  `Convert`.
- Include at least one size-query call and one real output-buffer conversion.
- Check output headers and raw sizes, not only whether a renderer displays an
  image.
