"""Script for overiding the user model."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from apps.college.models import CollegeBranch


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
        extra_fields.setdefault('is_active', False)
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
    """User model."""

    Student = 0
    Staff = 1
    TYPE_CHOICES = (
        (Student, 'Student'),
        (Staff, 'Staff'),
    )

    username = None
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    college_branch = models.ForeignKey(
        CollegeBranch,
        on_delete=models.PROTECT,
        default=None, null=True,
        related_name='college_branch'
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    user_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=0
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Return the email as string value ."""
        return self.email

    class Meta:
        """Overiding the table name."""

        db_table = 'auth_user'
        verbose_name_plural = 'User'
