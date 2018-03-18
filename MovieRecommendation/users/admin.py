from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from .models import CustomUser
from movie.models import Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'latent_factor')}),
        (_('Permissions'), {'fields': ('is_real', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    #inlines = [RatingInline]
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_real')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-is_real',)

admin.site.register(CustomUser, CustomUserAdmin)