from dennych_dvesto.models import Topic, Category, Comment
from django.contrib import admin

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class TopicAdmin(admin.ModelAdmin):
    fields = [ 'topic', 'topic_type', 'category', 'inserted', 'ip', 'user_agent' ]
    inlines = [ CommentInline ]
    readonly_fields = ( 'ip', 'user_agent' )

class CategoryAdmin(admin.ModelAdmin):
    fields = [ 'category', 'color' ]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)