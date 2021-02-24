from django.db import models

# Create your models here.


class Choice(models.Model):
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text


class Survey(models.Model):
    name = models.CharField(max_length=64, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class SurveyChoicesField(models.Model):
    multiple = models.BooleanField(default=False)
    choices = models.ManyToManyField(Choice)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    use_choices = models.BooleanField(default=False)
    choices = models.ForeignKey(SurveyChoicesField, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.CharField(max_length=32)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
    answ_txt = models.TextField(blank=True, null=True)
    answ_choices = models.ManyToManyField(Choice, blank=True)

    class Meta:
        unique_together = [['user_id', 'question', 'survey']]


