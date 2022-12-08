from django.contrib import admin
from .models import Profile, Review

admin.site.register(Profile)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'employer','comment' ,'project','rating', 'created', 'active']
    list_filter = ['freelancer', 'created', 'active']
    list_editable = ['active']