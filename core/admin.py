from django.contrib import admin
from core.models import Question, SurveyChoicesField, Choice, Survey, Answer

# Register your models here.

class SurveyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('start_date',)
        return self.readonly_fields

admin.site.register(Question)
admin.site.register(SurveyChoicesField)
admin.site.register(Choice)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer)
