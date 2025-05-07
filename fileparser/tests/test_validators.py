from fileparser.validators import validate_file, validate_file_extension
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.core.exceptions import ValidationError

@pytest.mark.parametrize("extension, is_exception_expected", [
    ("CSV", True),
    ("mp4", True),
    ("mp3", True),
    ("pdf", False),
    ("docx", False),
    ("doc", False),
])
def test_validate_file_extension(extension, is_exception_expected):
    file = SimpleUploadedFile(name=f"simple-file.{extension}", content=b"Note")
    
    if is_exception_expected:
        with pytest.raises(ValidationError, match=r"only pdf , docx, doc ias allowed\."):
            validate_file_extension(file)
    else:
        validate_file_extension(file)
        
        
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
import pytest

@pytest.mark.parametrize("file_size, is_exception_expected", [
    (3_097_152, False),    # ~3MB - should pass
    (6_097_152, True),     # ~6MB - should fail
    (2_000_000, False),    # ~2MB - should pass
])
def test_validate_file_size(file_size, is_exception_expected):
    # Create a dummy file with specified size
    content = b"0" * file_size  # Create content of exact size
    file = SimpleUploadedFile(
        name="test_file.pdf",
        content=content,
        content_type="application/pdf"
    )
    
    if is_exception_expected:
        with pytest.raises(ValidationError, match=r"max file size can only be 5MB\."):
            validate_file_size(file)  # Make sure to call the size validator
    else:
        validate_file_size(file)  # Should pass without exception