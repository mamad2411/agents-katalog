---
name: wordpress-image-editor
description: WordPress image manipulation via WP_Image_Editor — resize, crop, rotate, flip, generate thumbnails and intermediate sizes. Use when generating image sizes for uploads, processing uploaded photos, creating custom image variants (e.g., a hero crop, an avatar), or choosing between the GD and Imagick backends. Covers wp_get_image_editor, image_make_intermediate_size, add_image_size, and quality/output-format controls.
---

# WordPress Image Editor (WP_Image_Editor)

WordPress abstracts image manipulation behind `WP_Image_Editor`. Two backends ship: **Imagick** (preferred when available — better quality, more formats) and **GD** (universal fallback). You don't choose directly; `wp_get_image_editor()` returns the best one for the file.

## The 30-second example

```php
$editor = wp_get_image_editor( '/path/to/photo.jpg' );
if ( is_wp_error( $editor ) ) {
    return $editor;
}

$editor->resize( 1200, 800, $crop = false );      // false = keep aspect, fit within box.
$editor->set_quality( 82 );                        // 0-100. Default ~82 for JPEG.

$result = $editor->save( '/path/to/photo-resized.jpg' );
// $result = array( 'path' => ..., 'file' => 'photo-resized.jpg', 'width' => 1200, 'height' => 800, 'mime-type' => 'image/jpeg' );
```

`wp_get_image_editor()` does:

1. Calls `_wp_image_editor_choose()` to pick GD or Imagick based on `wp_image_editors` filter + `test()` results + which one supports the file's MIME.
2. Calls `load()` on the chosen instance to read the file.
3. Returns it ready to use, or a `WP_Error` if neither backend can open the file.

## What you can do

All editors implement the same API (defined as abstract methods on `WP_Image_Editor`):

```php
$editor->resize(  int $max_w, int $max_h, bool|array $crop = false );
$editor->crop(    int $src_x, int $src_y, int $src_w, int $src_h, int $dst_w = null, int $dst_h = null, bool $src_abs = false );
$editor->rotate(  float $angle );           // Positive = counterclockwise.
$editor->flip(    bool $horz, bool $vert );

// Save (default = current file, current mime):
$editor->save( $destfilename = null, $mime_type = null );

// Or stream to STDOUT (e.g., for an AJAX response):
$editor->stream( $mime_type = null );

// Quality + output format:
$editor->set_quality( int $quality );       // 0-100.
$editor->generate_filename( $suffix, $dest_path, $extension );

// Inspection:
$size = $editor->get_size();                // array( 'width' => ..., 'height' => ... )
$q    = $editor->get_quality();
$mime = $editor->get_mime_type();
```

### Resize modes — the third arg matters

```php
$editor->resize( 1200, 800, false );                       // Fit within box, keep aspect.
$editor->resize( 1200, 800, true );                        // Hard crop centered.
$editor->resize( 1200, 800, array( 'center', 'top' ) );    // Hard crop, anchored top-center.
// Anchors: 'left'/'center'/'right' × 'top'/'center'/'bottom'.
```

### Cropping vs resize-with-crop

`crop()` takes pixel coordinates and is for known-good positions. `resize( w, h, true )` does a "smart" crop that centers (or follows the anchor).

```php
// Resize+crop: I want a 400x400 thumbnail from anywhere in the image.
$editor->resize( 400, 400, true );

// crop(): I know exactly which 400x400 area to extract.
$editor->crop( $src_x = 100, $src_y = 50, $src_w = 400, $src_h = 400 );
```

## Generating intermediate sizes

The way WordPress generates `image-150x150.jpg`, `image-300x200.jpg`, etc. is via `image_make_intermediate_size()`:

```php
$result = image_make_intermediate_size(
    $file,              // Absolute path to source image.
    $width,
    $height,
    $crop = false       // bool or anchor array (see above).
);
// $result = array of metadata, OR false on failure.
```

For the multi-size case (e.g., generating all of an attachment's sizes at once), use `multi_resize`:

```php
$sizes = $editor->multi_resize( array(
    'thumbnail'  => array( 'width' => 150, 'height' => 150, 'crop' => true ),
    'medium'     => array( 'width' => 300, 'height' => 300, 'crop' => false ),
    'large'      => array( 'width' => 1024, 'height' => 1024, 'crop' => false ),
    'hero-wide'  => array( 'width' => 1920, 'height' => 600,  'crop' => array( 'center', 'top' ) ),
) );
// Returns an array keyed by size name with file/width/height/mime-type for each generated file.
```

## Registering a custom image size

The integration point with the rest of WordPress (so the size shows in the editor and `wp_get_attachment_image_src()` knows about it):

```php
add_action( 'after_setup_theme', function () {
    add_image_size( 'hero-wide',     1920, 600, array( 'center', 'top' ) );
    add_image_size( 'square-medium', 600,  600, true );
} );

// Make it selectable in the media library "Image size" dropdown:
add_filter( 'image_size_names_choose', function ( $sizes ) {
    return array_merge( $sizes, array(
        'hero-wide'     => __( 'Hero Wide', 'mytheme' ),
        'square-medium' => __( 'Square Medium', 'mytheme' ),
    ) );
} );
```

After registering a new size, **existing uploads aren't regenerated automatically.** Re-trigger generation with `wp media regenerate` (WP-CLI) or `wp_create_image_subsizes()`.

## Quality and output format

WordPress sets sensible per-mime defaults, but you can override per-call or globally:

```php
// Global (all JPEGs at 75 quality):
add_filter( 'wp_editor_set_quality', fn( $q, $mime ) => 'image/jpeg' === $mime ? 75 : $q, 10, 2 );

// Per-mime output format — e.g., always save uploaded HEIC/PNG as JPEG:
add_filter( 'image_editor_output_format', fn() => array(
    'image/heic' => 'image/jpeg',
    'image/png'  => 'image/jpeg',
) );

// WebP/AVIF: WordPress (6.x+) supports both via Imagick. To make WebP the default for JPEGs:
add_filter( 'image_editor_output_format', fn() => array(
    'image/jpeg' => 'image/webp',
) );
```

## Choosing GD vs Imagick

Imagick is preferred because it preserves more metadata, supports more formats (TIFF, PSD, HEIC depending on build), and produces better-quality resizes. The default order is `WP_Image_Editor_Imagick`, then `WP_Image_Editor_GD`.

```php
// Force GD (rarely a good idea):
add_filter( 'wp_image_editors', fn() => array( 'WP_Image_Editor_GD' ) );

// Probe at runtime:
$ok_imagick = WP_Image_Editor_Imagick::test();
$ok_gd      = WP_Image_Editor_GD::test();
WP_Image_Editor_Imagick::supports_mime_type( 'image/heic' );
```

Both backends have their own `test()` static (host has the extension AND can read the file format) and `supports_mime_type()`.

## Reading EXIF orientation

iPhone photos are often saved rotated with an EXIF orientation flag. WordPress auto-rotates on upload via `maybe_exif_rotate()`. If you're processing an image outside that flow:

```php
$editor = wp_get_image_editor( $file );
$editor->maybe_exif_rotate();        // Defined on the base class.
$editor->save( ... );
```

## Where to look in this codebase

- `wp-includes/class-wp-image-editor.php` — abstract base class with the full method signature list.
- `wp-includes/class-wp-image-editor-gd.php` — GD backend.
- `wp-includes/class-wp-image-editor-imagick.php` — Imagick backend.
- `wp-includes/media.php` — `wp_get_image_editor()`, `_wp_image_editor_choose()`, `image_make_intermediate_size()`, `wp_get_image_editor_output_format()`.
- `wp-admin/includes/image.php` — `wp_create_image_subsizes()`, `wp_generate_attachment_metadata()`, the upload-time integration.
- `wp-includes/class-avif-info.php` — AVIF metadata parsing (since WP 6.5).

## Common pitfalls

- Calling `save()` without a destination — it overwrites the source file in place. Pass a path for new files.
- Not checking `is_wp_error( $editor )` — `wp_get_image_editor()` returns a `WP_Error` if neither backend can handle the file.
- Forgetting `add_image_size()` and then wondering why a custom size never appears in `wp_get_attachment_image_src( $id, 'my-size' )` — it has to be registered before uploads, or you need to regenerate.
- Editing a freshly resized image that's still loaded in memory in the same object — internally GD holds a resource; after `save()`, call `load()` again or instantiate a fresh editor.
- Resizing huge originals on tiny PHP memory limits — a 10MP JPEG can need 200MB+ of GD memory. Either raise `WP_MAX_MEMORY_LIMIT` or use Imagick (more memory-efficient).
- Assuming Imagick supports a format because the binary does — the *PHP extension* must support it too. Always `supports_mime_type()`.
