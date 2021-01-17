from django.contrib import admin 
from .models import *
from mptt.admin import MPTTModelAdmin

from mptt.admin import DraggableMPTTAdmin
from django_summernote.admin import SummernoteModelAdmin 
from import_export.admin import ImportExportModelAdmin
# Apply summernote to all TextField in model.


class CategoryAdmin(DraggableMPTTAdmin,SummernoteModelAdmin,ImportExportModelAdmin): 
    pass

admin.site.register(Category, CategoryAdmin )

# @admin.register(Post)
# class AuthorAdmin(admin.ModelAdmin,SummernoteModelAdmin ):
#     list_display = ('title', 'id', 'status', 'slug', 'author')
#     prepopulated_fields = {'slug': ('title',), }

 

class post2(SummernoteModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }
    summernote_fields = ('content',)
admin.site.register(Post, post2 )


admin.site.register(Vote)

admin.site.register(Comment, MPTTModelAdmin)
