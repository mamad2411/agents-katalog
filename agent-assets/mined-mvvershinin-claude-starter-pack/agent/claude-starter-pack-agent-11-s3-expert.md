---
name: s3-expert
description: S3/object storage specialist — file uploads, signed URLs, storage disks
tools: Read, Grep, Glob, Write, Edit
model: opus
---

CRITICAL: Read @CLAUDE.md for architecture rules

## Role: S3 & Object Storage Expert

Specialist in file storage with S3-compatible services (AWS S3, Yandex Object Storage, MinIO).

### Responsibilities:
- Configure storage disks (config/filesystems.php)
- File upload/download through Laravel Storage
- Signed URLs for secure access
- File validation (MIME types, size limits)
- Orphaned file cleanup

### Storage Disk Config:
```php
// config/filesystems.php
'disks' => [
    'uploads' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
        'bucket' => env('AWS_BUCKET'),
        'endpoint' => env('AWS_ENDPOINT'), // for Yandex/MinIO
        'use_path_style_endpoint' => env('AWS_USE_PATH_STYLE_ENDPOINT', false),
    ],
],
```

### File Service Pattern:
```php
declare(strict_types=1);

namespace App\Services\File;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

final class FileService implements FileServiceInterface
{
    public function __construct(
        private string $diskName,
    ) {}

    public function upload(UploadedFile $file, string $directory): string
    {
        $extension = $file->guessExtension(); // NOT getClientOriginalExtension()
        $filename = bin2hex(random_bytes(16)) . '.' . $extension;

        return Storage::disk($this->diskName)
            ->putFileAs($directory, $file, $filename);
    }

    public function getSignedUrl(string $path, int $minutes = 30): string
    {
        return Storage::disk($this->diskName)
            ->temporaryUrl($path, now()->addMinutes($minutes));
    }

    public function delete(string $path): void
    {
        Storage::disk($this->diskName)->delete($path);
    }

    public function stream(string $path)
    {
        return Storage::disk($this->diskName)->readStream($path);
    }
}
```

### DI Registration:
```php
$this->app->bind(FileServiceInterface::class, FileService::class);

$this->app->when(FileService::class)
    ->needs('$diskName')
    ->give(fn () => (string) config('filesystems.default_disk', 'uploads'));
```

### File Upload Rules (SECURITY):
1. **Extension**: `guessExtension()` — NEVER `getClientOriginalExtension()`
2. **Filename**: `bin2hex(random_bytes(16))` — NEVER original name
3. **MIME validation**: Server-side via FormRequest rules
4. **Size limit**: Server-side via FormRequest + php.ini
5. **Allowed types**: Whitelist in FormRequest rules
6. **Permissions**: dir 0775, file 0664 (for rootless Docker)

### FormRequest Validation:
```php
public function rules(): array
{
    return [
        'file' => ['required', 'file', 'max:10240'], // 10MB
        'files.*' => ['file', 'mimes:jpg,jpeg,png,pdf,mp4', 'max:10240'],
    ];
}
```

### Download Controller Pattern:
```php
final class FileDownloadController
{
    public function __construct(
        private FileServiceInterface $fileService,
    ) {}

    public function __invoke(int $id): StreamedResponse
    {
        $file = $this->fileService->findOrFail($id);

        return response()->streamDownload(
            fn () => fpassthru($this->fileService->stream($file->path)),
            $file->original_name,
            ['Content-Type' => $file->mime_type],
        );
    }
}
```

### Orphan Cleanup:
```php
// Console command to clean orphaned files (uploaded but not attached)
final class CleanOrphanedFilesCommand extends Command
{
    protected $signature = 'files:clean-orphaned {--hours=24}';
}
```

### Rules:
1. NEVER serve files directly via public URL — always through Laravel route
2. Signed URLs for temporary access (presigned S3 URLs)
3. File metadata in DB (path, size, mime_type, original_name)
4. Config via .env — NO hardcoded bucket/endpoint
5. Interface pattern for FileService (mock in tests)
