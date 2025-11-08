from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "is_open")
    list_filter = ["pub_date", "is_open"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
