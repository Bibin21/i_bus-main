from django.contrib import admin
from apps.college.models import CollegeBranch, CollegeStudent, CollegeStaff


class CollegeBranchAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'branch_name')
    list_filter = ('branch_name',)
    search_fields = ('branch_name',)

admin.site.register(CollegeBranch, CollegeBranchAdmin)

class CollegeStudentAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'email')
    list_filter = ('email',)
    search_fields = ('email',)

admin.site.register(CollegeStudent, CollegeStudentAdmin)

class CollegeStaffAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'email')
    list_filter = ('email',)
    search_fields = ('email',)

admin.site.register(CollegeStaff, CollegeStaffAdmin)
