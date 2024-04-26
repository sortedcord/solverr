from django.contrib import admin

# Register your models here.
from .models import Question, Solution, Source, Topic

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'question_type')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Solution)
admin.site.register(Source)
admin.site.register(Topic, TopicAdmin)