from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
import os


VALID_EXTENSIONS = [
    '.pdf',
    '.docx',
    '.doc'
]

def validate_file_size(file_object: UploadedFile):
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024
    if file_object.size > MAX_UPLOAD_SIZE:
        raise ValidationError("max file size is 5MB.")


def validate_file_extension(file_object:UploadedFile):
    ext: str = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError("only pdf , docx, doc ias allowed.")