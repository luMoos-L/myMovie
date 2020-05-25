from django.contrib import admin
from .models import  users,movies,comments,collections
# Register your models here.
admin.site.register(users)
admin.site.register(movies)
admin.site.register(collections)
@admin.register(comments)
class CommentAdmin(admin.ModelAdmin):
    list_display=('co_text','user_name')