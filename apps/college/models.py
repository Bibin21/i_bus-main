from django.db import models

# Create your models here.


class CollegeBranch(models.Model):
    """Model for Collge Branch table."""

    branch_name = models.CharField(max_length=250)

    def __str__(self):
        return self.branch_name

    class Meta:
        """Override the table name."""

        db_table = 'college_branch'


class CollegeStudent(models.Model):
    """Model for Collge Student table."""

    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        """Override the table name."""

        db_table = 'college_student'


class CollegeStaff(models.Model):
    """Model for Collge Staff table."""

    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        """Override the table name."""

        db_table = 'college_staff'
