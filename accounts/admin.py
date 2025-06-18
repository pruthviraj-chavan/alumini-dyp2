from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import User, VerificationRequest

class UserAdmin(BaseUserAdmin):
    """Custom admin interface for User model"""
    list_display = ('email', 'first_name', 'last_name', 'role', 'branch', 'year', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'branch', 'year', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'branch')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'bio')}),
        (_('Academic info'), {'fields': ('role', 'branch', 'year')}),
        (_('Status'), {'fields': ('is_verified',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'branch', 'year'),
        }),
    )

class VerificationRequestAdmin(admin.ModelAdmin):
    """Admin interface for VerificationRequest model"""
    list_display = ('student', 'student_number', 'status', 'created_at', 'reviewed_by', 'reviewed_at')
    list_filter = ('status', 'created_at', 'reviewed_at')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'student_number')
    ordering = ('-created_at',)
    actions = ['approve_requests', 'reject_requests']
    
    readonly_fields = ('created_at',)
    
    def approve_requests(self, request, queryset):
        """Admin action to approve selected verification requests"""
        for verification_request in queryset:
            if verification_request.status == 'PENDING':
                verification_request.approve(request.user)
        
        self.message_user(request, f"{queryset.count()} verification request(s) approved successfully.")
    approve_requests.short_description = "Approve selected verification requests"
    
    def reject_requests(self, request, queryset):
        """Admin action to reject selected verification requests"""
        for verification_request in queryset:
            if verification_request.status == 'PENDING':
                verification_request.reject(request.user)
        
        self.message_user(request, f"{queryset.count()} verification request(s) rejected.")
    reject_requests.short_description = "Reject selected verification requests"
    
    def save_model(self, request, obj, form, change):
        # Set the reviewer to the current admin user if status is changed
        if change and 'status' in form.changed_data:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
            
            # Update user verification status if approved
            if obj.status == 'APPROVED':
                obj.student.is_verified = True
                obj.student.save()
            
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(VerificationRequest, VerificationRequestAdmin)
