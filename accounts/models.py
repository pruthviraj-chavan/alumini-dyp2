from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom User model with email as username field and additional fields for the alumni portal"""
    
    # User role choices
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        STUDENT = 'STUDENT', _('Student')
        ALUMNI = 'ALUMNI', _('Alumni')
    
    # Remove username field and use email as the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    branch = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)  # Passed/Current year
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email

class VerificationRequest(models.Model):
    """Model for student verification requests"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_requests')
    student_number = models.CharField(max_length=50, null=True, blank=True)
    verification_document = models.FileField(upload_to='verification_documents/', null=True, blank=True)
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ], default='PENDING')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.email} - {self.status}"
        
    def approve(self, reviewed_by):
        """Approve the verification request and mark the student as verified"""
        self.status = 'APPROVED'
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        self.save()
        
        # Update the student's verification status
        self.student.is_verified = True
        self.student.save()
        
    def reject(self, reviewed_by):
        """Reject the verification request"""
        self.status = 'REJECTED'
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        self.save()
