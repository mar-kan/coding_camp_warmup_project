from django.contrib import admin
from .models import Question, Choice, VoterRecord


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "is_open"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "is_open", "was_published_recently"]
    list_filter = ["pub_date", "is_open"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(VoterRecord)
