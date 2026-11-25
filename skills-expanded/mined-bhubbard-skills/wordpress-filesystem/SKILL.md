---
name: wordpress-filesystem
description: WordPress filesystem abstraction (WP_Filesystem) for read/write that works across direct, SSH2, FTP, and FTP-sockets transports. Use when a plugin needs to write to wp-content, install/extract files, modify files on hosts where PHP can't write directly, or interact with the upgrader. Covers FS_METHOD, request_filesystem_credentials, the $wp_filesystem global, and the difference vs raw fopen/file_put_contents.
---

# WordPress Filesystem API (WP_Filesystem)

PHP's `fopen`/`file_put_contents` only work when the web user owns the file. On shared hosts where uploads are owned by the FTP user but PHP runs as `www-data`, direct writes fail. WordPress's filesystem abstraction solves this by routing writes through whichever transport works on the host (direct, FTP, FTPS, SSH2).

Use it for anything that writes inside `wp-content/` from the admin context — plugin/theme installers, file editors, custom export-to-disk features, anything that touches user-owned files.

## The big picture

There's one abstract base class and four concrete transports:

- `WP_Filesystem_Base` — abstract API every transport implements.
- `WP_Filesystem_Direct` — uses native PHP `fopen` etc. Used when PHP owns the files.
- `WP_Filesystem_SSH2` — connects over SSH2 (requires libssh2).
- `WP_Filesystem_FTPext` — connects over FTP using the PHP FTP extension.
- `WP_Filesystem_FTPSockets` — connects over FTP using raw sockets (fallback if FTPext isn't compiled).

All of them are in `wp-admin/includes/`, not `wp-includes/` — they're admin-context-only because they require credentials.

## Initialization — three lines

```php
// 1. Pull in the function-level API (it's not autoloaded).
require_once ABSPATH . 'wp-admin/includes/file.php';

// 2. Initialize the global $wp_filesystem.
if ( ! WP_Filesystem() ) {
    return new WP_Error( 'fs_init_failed', 'Could not initialize the filesystem.' );
}

// 3. Use the global.
global $wp_filesystem;
$wp_filesystem->put_contents( WP_CONTENT_DIR . '/myplugin/data.json', wp_json_encode( $data ), FS_CHMOD_FILE );
```

`WP_Filesystem()` (note: capital W and F — yes, that's the actual name) handles credential prompting when needed, instantiates the right transport, and assigns it to `$GLOBALS['wp_filesystem']`. It returns `true` on success, `false` if the user needs to enter credentials first.

## Forcing or detecting the transport — FS_METHOD

Add to `wp-config.php`:

```php
define( 'FS_METHOD', 'direct' );           // Force direct PHP writes (most common in modern setups).
// Other valid values: 'ssh2', 'ftpext', 'ftpsockets'.

// Optional credential defaults (avoid the credential prompt on FTP/SSH):
define( 'FTP_USER',    'username' );
define( 'FTP_PASS',    'password' );
define( 'FTP_HOST',    'example.com' );
define( 'FTP_SSL',     true );             // For FTP over TLS.
define( 'FTP_PUBKEY',  '/home/user/.ssh/id_rsa.pub' );
define( 'FTP_PRIKEY',  '/home/user/.ssh/id_rsa' );
define( 'FTP_BASE',    '/var/www/html/' ); // Path on the remote server.
define( 'FTP_CONTENT_DIR', '/var/www/html/wp-content/' );
define( 'FTP_PLUGIN_DIR',  '/var/www/html/wp-content/plugins/' );
```

If you don't define `FS_METHOD`, WordPress probes:

1. Direct — if the current PHP user owns `wp-content/`.
2. FTPext — if the `ftp_*` PHP extension is loaded.
3. FTPSockets — fallback.

`get_filesystem_method()` returns which one it picked.

## The credentials prompt

If WordPress can't write directly and no credentials are defined, it shows a form asking the user. To trigger that flow correctly:

```php
$method = get_filesystem_method( array(), WP_CONTENT_DIR );
$creds  = request_filesystem_credentials( $form_url, $method, false, false, null );

if ( false === $creds ) {
    // The form was just printed. Stop and let the user submit it.
    return;
}

if ( ! WP_Filesystem( $creds ) ) {
    // Bad credentials — re-print the form with an error.
    request_filesystem_credentials( $form_url, $method, true, false, null );
    return;
}

// Now safe to use $wp_filesystem.
```

This is the dance every WordPress installer does. `request_filesystem_credentials()` either prints a form (returns `false`) or returns the credential array.

## The API — what $wp_filesystem can do

All transports implement the same methods (defined in `class-wp-filesystem-base.php`):

```php
global $wp_filesystem;

// Read
$contents = $wp_filesystem->get_contents( $file );
$lines    = $wp_filesystem->get_contents_array( $file );
$exists   = $wp_filesystem->exists( $file );
$is_dir   = $wp_filesystem->is_dir( $path );
$is_file  = $wp_filesystem->is_file( $file );
$ok       = $wp_filesystem->is_readable( $file );
$ok       = $wp_filesystem->is_writable( $file );
$size     = $wp_filesystem->size( $file );
$mtime    = $wp_filesystem->mtime( $file );

// Write
$wp_filesystem->put_contents( $file, $contents, FS_CHMOD_FILE );    // FS_CHMOD_FILE = 0644.
$wp_filesystem->copy( $src, $dst, $overwrite = false, $mode = false );
$wp_filesystem->move( $src, $dst, $overwrite = false );
$wp_filesystem->delete( $path, $recursive = false, $type = false ); // type: 'f' or 'd'.
$wp_filesystem->touch( $file, $time = 0, $atime = 0 );

// Directories
$wp_filesystem->mkdir( $path, FS_CHMOD_DIR );    // FS_CHMOD_DIR = 0755.
$wp_filesystem->rmdir( $path, $recursive = false );
$wp_filesystem->dirlist( $path, $include_hidden = true, $recursive = false );

// Permissions
$wp_filesystem->chmod( $file, $mode = false, $recursive = false );
$wp_filesystem->chown( $file, $owner, $recursive = false );
$wp_filesystem->chgrp( $file, $group, $recursive = false );

// Path helpers
$wp_filesystem->abspath();           // ABSPATH on the remote.
$wp_filesystem->wp_content_dir();
$wp_filesystem->wp_plugins_dir();
$wp_filesystem->wp_themes_dir();
$wp_filesystem->find_folder( $local );   // Translate local path to remote path.
```

`FS_CHMOD_FILE` and `FS_CHMOD_DIR` are the constants you should pass for new files/dirs — defined in `wp-includes/default-constants.php` (defaults: 0644 and 0755, overridable in `wp-config.php`).

## When NOT to use WP_Filesystem

For files that aren't meant to be user-editable — your plugin's own cache files, tempfiles, log files — just use PHP's native functions. WP_Filesystem is for the *content directory* and code installs.

Roughly:

- **Use WP_Filesystem**: writing into `wp-content/plugins/`, `wp-content/themes/`, modifying core, anything an FTP/SSH-locked-down host would block via direct PHP.
- **Use raw PHP**: `wp-content/uploads/` (PHP can always write there because that's where user uploads go), `/tmp/`, your own plugin's data dir if it's PHP-writable by design.

## Extracting a zip

```php
require_once ABSPATH . 'wp-admin/includes/file.php';
WP_Filesystem();
$result = unzip_file( $zip_path, $destination_dir );    // Uses ZipArchive or PclZip via WP_Filesystem.
if ( is_wp_error( $result ) ) { /* ... */ }
```

`unzip_file()` is the canonical way to extract uploaded archives — it uses ZipArchive when available, falls back to PclZip (vendored in WordPress), and writes through WP_Filesystem.

## Downloading a remote file to disk

```php
require_once ABSPATH . 'wp-admin/includes/file.php';
$tmp_file = download_url( 'https://example.com/file.zip', $timeout = 300 );
if ( is_wp_error( $tmp_file ) ) { /* ... */ }
// $tmp_file is in sys_get_temp_dir(). Remember to wp_delete_file() after use.
wp_delete_file( $tmp_file );
```

`download_url()` uses the HTTP API but writes the result to a tmpfile. Pair with `unzip_file()` to download-and-extract.

## Where to look in this codebase

- `wp-admin/includes/file.php` — the function-level API: `WP_Filesystem()`, `get_filesystem_method()`, `request_filesystem_credentials()`, `download_url()`, `unzip_file()`, `wp_handle_upload()`, `wp_tempnam()`.
- `wp-admin/includes/class-wp-filesystem-base.php` — the abstract base class. Read this for the full method list.
- `wp-admin/includes/class-wp-filesystem-direct.php` — direct PHP writes.
- `wp-admin/includes/class-wp-filesystem-ssh2.php` — SSH2 transport.
- `wp-admin/includes/class-wp-filesystem-ftpext.php` — FTP via the ftp extension.
- `wp-admin/includes/class-wp-filesystem-ftpsockets.php` — FTP via raw sockets.

## Common pitfalls

- Skipping the `require_once ABSPATH . 'wp-admin/includes/file.php';` and getting "undefined function `WP_Filesystem`" — these are not auto-loaded outside the admin context.
- Calling `WP_Filesystem()` but not checking its return value, then using the global on a host that needs credentials → null pointer.
- Hardcoding `0644` / `0755` instead of `FS_CHMOD_FILE` / `FS_CHMOD_DIR`. The constants are user-overridable in `wp-config.php`.
- Using WP_Filesystem from a frontend request (e.g., a non-admin AJAX). It's designed for the admin context where the credential dialog can be shown.
- Mixing PHP file functions with WP_Filesystem on the same files — paths can differ (especially under chrooted FTP). Use one or the other for a given operation.
- Writing to `wp-content/plugins/` from a plugin's own code is usually wrong. Plugins should treat their own folder as read-only.
