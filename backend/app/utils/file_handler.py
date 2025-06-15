from fastapi import UploadFile, HTTPException, status
import imghdr

# Define allowed image types
ALLOWED_TYPES = {"jpeg", "png", "jpg", "gif", "webp"}
MAX_FILE_SIZE_MB = 10


async def validate_file(file: UploadFile):
    """
    Validate uploaded image:
    - Check MIME type & extension
    - Check file size
    """
    filename = file.filename.lower()

    # Validate extension
    if not any(filename.endswith(ext) for ext in ALLOWED_TYPES):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file extension"
        )

    # Read small part of file to guess type
    contents = await file.read()
    await file.seek(0)  # Reset pointer

    file_type = imghdr.what(None, h=contents)
    if file_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or unsupported image format"
        )

    # Validate file size (in-memory)
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds maximum allowed size of 10MB"
        )
