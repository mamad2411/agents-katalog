---
name: file-storage
description: "Apply when handling file uploads, storage, serving, or processing. Covers: S3-compatible storage, multipart uploads, presigned URLs, image processing, virus scanning patterns. Trigger for: file upload, storage, S3, images, files, media, attachment."
---

# FILE STORAGE — Production Patterns

## Upload Flow (presigned URL pattern)
```python
# Step 1: Client requests upload URL (no file goes through your server)
@app.post("/files/upload-url")
async def get_upload_url(filename: str, content_type: str, user=Depends(auth)):
    file_key = f"uploads/{user.id}/{uuid4()}/{filename}"
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": file_key, "ContentType": content_type},
        ExpiresIn=300,  # 5 minutes
    )
    # Save pending file record
    file_id = await db.create_pending_file(file_key, user.id)
    return {"upload_url": url, "file_id": file_id}

# Step 2: Client uploads directly to S3 (not through API)
# Step 3: Client confirms upload
@app.post("/files/{file_id}/confirm")
async def confirm_upload(file_id: str, user=Depends(auth)):
    await db.mark_file_ready(file_id)
```

## Serving Files (presigned download URL)
```python
@app.get("/files/{file_id}/download")
async def get_download_url(file_id: str, user=Depends(auth)):
    file = await db.get_file(file_id)
    if file.owner_id != user.id:
        raise HTTPException(403)
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": file.s3_key},
        ExpiresIn=3600,
    )
    return {"url": url}
```

## Validation Before Processing
```python
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_upload(file: UploadFile):
    # Check content type (NEVER trust file extension)
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError("content_type", f"Not allowed: {file.content_type}")
    
    # Read first bytes to detect real type (magic bytes)
    header = await file.read(8)
    await file.seek(0)
    real_type = detect_mime(header)  # python-magic
    if real_type != file.content_type:
        raise ValidationError("file", "File type mismatch")
    
    if file.size and file.size > MAX_SIZE:
        raise ValidationError("file", "Exceeds 10MB limit")
```

## Image Processing
```python
from PIL import Image
import io

async def process_image(file_key: str):
    """Generate thumbnails after upload."""
    obj = s3.get_object(Bucket=BUCKET, Key=file_key)
    img = Image.open(io.BytesIO(obj["Body"].read()))
    
    for size in [(200, 200), (800, 800)]:
        thumb = img.copy()
        thumb.thumbnail(size, Image.LANCZOS)
        buf = io.BytesIO()
        thumb.save(buf, format="WEBP", quality=85)
        buf.seek(0)
        thumb_key = file_key.replace("uploads/", f"thumbs/{size[0]}/")
        s3.upload_fileobj(buf, BUCKET, thumb_key)
```

## Forbidden
❌ Storing files in database (use S3/filesystem)
❌ Trusting file extension for type detection
❌ Serving files through your API server (memory + bandwidth)
❌ Public bucket without signed URLs (privacy leak)
❌ No size limit on uploads
❌ Storing original path with user-controlled filename
