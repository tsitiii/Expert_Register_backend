from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.forms import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('super_admin', 'Super Admin'),
]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Expert(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cv_file = models.FileField()
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    cv_language = models.CharField(max_length=20, choices=[("English", "English"), ("Amharic", "Amharic")], default="English")
    country = CountryField(blank=True)
    expertise_area = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = now()
        self.save()
    
    def __str__(self):
        return self.first_name
    


class PersonalDetail(models.Model):
    expert = models.OneToOneField(Expert, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=30, choices=[('female', 'Female'),
            ('male', 'Male') ])
    country = models.CharField(max_length=120, blank= True)
    phone_number = PhoneNumberField(blank=True,region = 'ET' )
    email = models.EmailField(unique = True, blank = False)
    cv_language = models.CharField(
        max_length=20,
        choices=[("English", "English"), ("Amharic", "Amharic")],
        help_text="Language for generated CV documents"
    )
    
    def __str__(self):
        return self.email


class EducationalBackground(models.Model):
    LEVEL = (('diploma', 'Diploma'), ('degree', 'Degree'), ('masters', 'Masters'), ('phd', 'PHD'))
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    institution_name = models.TextField()
    education_level = models.CharField(max_length=50, choices=LEVEL)
    field_of_study = models.CharField(max_length=255)
    year_of_grad = models.DateField()
    class Meta:
        ordering = ['-year_of_grad']

    def __str__(self):
        return self.education_level
    
    
class WorkExperience(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField()
    
    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")

    class Meta:
        ordering = ['-start_date']

class Expertise(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    specialization = models.TextField()
    key_words = models.JSONField(
        default = list
    )
    def __str__(self):
        return f"Expertise of: {self.expert.id}"
