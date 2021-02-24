from rest_framework import serializers

from core.models import Survey, Answer, Question, SurveyChoicesField, Choice


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_date', 'end_date',)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')


class SurveyChoicesFieldSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = SurveyChoicesField
        fields = ('id', 'multiple', 'choices')


class QuestionSerializer(serializers.ModelSerializer):
    choices = SurveyChoicesFieldSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'survey', 'text', 'use_choices', 'choices')


class AnswerSerializer(serializers.ModelSerializer):
    answ_choices_set = ChoiceSerializer(source='answ_choices', read_only=True, many=True)
    question_details = QuestionSerializer(source='question', read_only=True)
    class Meta:
        model = Answer
        fields = ('id', 'user_id', 'question', 'question_details', 'survey', 'answ_txt', 'answ_choices', 'answ_choices_set')


class SurveyByIdSerializer(serializers.Serializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all())


class UserIdQuerySerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=32)


class MyAnswersQuerySerializer(serializers.Serializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all())
    user_id = serializers.CharField(max_length=32)

