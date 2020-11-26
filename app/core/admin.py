from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ['created_at']
    list_display = ['email', 'first_name', 'last_name', 'created_at']
    readonly_fields = ('id', 'uuid', 'created_at', 'updated_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('id', 'uuid', 'first_name', 'last_name', 'user_name')}),
        (_('Level'), {'fields': ('level',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('created_at', 'updated_at', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


@admin.register(models.Achievement)
class AchievementAdmin(admin.ModelAdmin):
    ordering = ['achievement']
    list_display = ('achievement', 'points',)
    readonly_fields = ('id', 'created_at',)
    fieldsets = ((None, {'fields': ('id', 'created_at', 'achievement', 'points')}),)


@admin.register(models.StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_display = ('achievement', 'student', 'created_at')
    readonly_fields = ('id', 'created_at',)
    fieldsets = ((None, {'fields': ('id', 'created_at', 'achievement', 'student', 'notes')}),)


@admin.register(models.Reward)
class RewardAdmin(admin.ModelAdmin):
    ordering = ['reward']
    list_display = ('reward',)
    readonly_fields = ('id', 'created_at',)
    fieldsets = ((None, {'fields': ('id', 'created_at', 'reward', 'description')}),)


@admin.register(models.StudentReward)
class StudentRewardAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_display = ('reward', 'student', 'created_at')
    readonly_fields = ('id', 'created_at',)
    fieldsets = ((None, {'fields': ('id', 'created_at', 'reward', 'student', 'notes')}),)

#admin.site.register(models.User, UserAdmin)
#admin.site.register(models.Achievement, AchievementAdmin)
#admin.site.register(models.StudentAchievement)
#admin.site.register(models.Reward)
#admin.site.register(models.StudentReward)