---
name: file-upload-storage
description: |
  File upload, validation, and storage patterns. Apply when handling file uploads, image processing,
  document storage, or media management. Covers MIME validation, size limits, S3/local storage,
  image resizing, and secure file serving.
---

# File Upload & Storage

## Upload Validation
```python
import magic
from pathlib import Path

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
ALLOWED_DOC_TYPES = {'application/pdf', 'application/msword',
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10MB
MAX_DOC_SIZE = 50 * 1024 * 1024     # 50MB

def validate_upload(file_bytes: bytes, allowed_types: set, max_size: int) -> str:
    if len(file_bytes) > max_size:
        raise ValidationError(f"File too large. Max: {max_size // 1024 // 1024}MB")
    
    # Detect actual MIME type from file content (not client-provided)
    mime = magic.from_buffer(file_bytes, mime=True)
    if mime not in allowed_types:
        raise ValidationError(f"File type not allowed: {mime}")
    
    return mime

def secure_filename(original: str) -> str:
    # Remove path traversal attempts, keep only safe characters
    stem = Path(original).stem
    suffix = Path(original).suffix.lower()
    safe_stem = re.sub(r'[^a-zA-Z0-9_-]', '_', stem)[:50]
    return f"{safe_stem}_{uuid4().hex[:8]}{suffix}"
```

## Image Processing Pipeline
```python
from PIL import Image
import io

def process_image(file_bytes: bytes) -> dict[str, bytes]:
    img = Image.open(io.BytesIO(file_bytes))
    
    # Strip EXIF data (privacy)
    img_clean = Image.new(img.mode, img.size)
    img_clean.putdata(list(img.getdata()))
    
    # Convert to RGB if needed (for JPEG output)
    if img_clean.mode in ('RGBA', 'LA', 'P'):
        img_clean = img_clean.convert('RGB')
    
    sizes = {
        'original': (img_clean.width, img_clean.height),
        'large': (1200, 1200),
        'medium': (600, 600),
        'thumbnail': (150, 150),
    }
    
    result = {}
    for name, (max_w, max_h) in sizes.items():
        resized = img_clean.copy()
        resized.thumbnail((max_w, max_h), Image.LANCZOS)
        buf = io.BytesIO()
        resized.save(buf, format='WEBP', quality=85, optimize=True)
        result[name] = buf.getvalue()
    
    return result
```

## S3-Compatible Storage (MinIO / AWS S3)
```python
import boto3
from botocore.exceptions import ClientError

class StorageService:
    def __init__(self):
        self.s3 = boto3.client('s3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        )
        self.bucket = settings.S3_BUCKET

    async def upload(self, file_bytes: bytes, key: str, content_type: str) -> str:
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type,
                CacheControl='public, max-age=31536000',  # 1 year for immutable files
            )
            return f"{settings.CDN_URL}/{key}"
        except ClientError as e:
            raise StorageError(f"Upload failed: {e.response['Error']['Message']}")

    async def delete(self, key: str) -> None:
        self.s3.delete_object(Bucket=self.bucket, Key=key)

storage = StorageService()
```

## Frontend Upload Component
```tsx
function FileUpload({ onUpload, accept = 'image/*', maxSizeMB = 10 }) {
  const [isDragging, setIsDragging] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    setError(null);
    if (file.size > maxSizeMB * 1024 * 1024) {
      setError(`File too large. Max: ${maxSizeMB}MB`);
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      setProgress(0);
      const result = await api.upload.file(formData, (pct) => setProgress(pct));
      onUpload(result.url);
    } catch (err) {
      setError('Upload failed. Please try again.');
    } finally {
      setProgress(null);
    }
  };

  return (
    <div
      className={cn('upload-zone', isDragging && 'upload-zone--active')}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleFile(e.dataTransfer.files[0]); }}
    >
      <input type="file" accept={accept} onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} className="sr-only" />
      {progress !== null ? <ProgressBar value={progress} /> : <UploadPrompt />}
      {error && <p className="text-error">{error}</p>}
    </div>
  );
}
```
