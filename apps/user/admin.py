"""Script for  admin interface."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    def get_form(self, request, obj=None, **kwargs):
        """Custom form with excude field ."""
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        """Save methode with user from the currently loggined user ."""
        user = request.user.id
        instance = form.save(commit=False)
        if not change:
            instance.is_staff = True

        instance.save()
        form.save_m2m()
        return instance

    def get_queryset(self, request):
        """Query to list the users with field True."""
        qs = super(UserAdmin, self).get_queryset(request)
        return qs

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'college_branch', 'phone_number',
            'user_type'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('first_name','last_name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# admin.site.register(Permission)
