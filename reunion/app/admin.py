from django.contrib import admin
from app.models import *
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'following', 'followers']
    search_fields = ['id']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','description', 'likes']
    search_fields = ['id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)









