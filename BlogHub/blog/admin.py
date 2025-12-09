from django.contrib import admin
from .models import signUpModel, Category, Tag, Post, Comment
# Register your models here.


admin.site.register(signUpModel)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)