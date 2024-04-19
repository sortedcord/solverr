from django.contrib import admin

# Register your models here.
from .models import Question, Solution, Source

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'question_type')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Solution)
admin.site.register(Source)