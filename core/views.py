import datetime

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from core.models import Survey, Answer, Question
from core.serializers import SurveySerializer, AnswerSerializer, QuestionSerializer, SurveyByIdSerializer, \
    MyAnswersQuerySerializer, UserIdQuerySerializer


class SurveysViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(end_date__gt=datetime.date.today())

    @action(detail=False, methods=['GET'])
    def passed_surveys(self, request):
        query_serializer = UserIdQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        user_id = query_serializer.validated_data['user_id']
        qs = Survey.objects.all().filter(answer__user_id=user_id)

        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class QuestionsBySurveyViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def list(self, request, *args, **kwargs):
        query_serializer = SurveyByIdSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        survey = query_serializer.validated_data['survey_id']
        serializer = self.serializer_class(self.get_queryset().filter(survey=survey), many=True)
        return Response(serializer.data)


class MyAnswersViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def list(self, request, *args, **kwargs):
        query_serializer = MyAnswersQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        user_id = query_serializer.validated_data['user_id']
        survey = query_serializer.validated_data['survey_id']

        serializer = self.serializer_class(self.get_queryset().filter(user_id=user_id, survey=survey), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        text_ans = serializer.validated_data['answ_txt']
        answ_choices = serializer.validated_data['answ_choices']

        if question.use_choices:
            if text_ans != '':
                raise ValidationError('Answer should contain only choices, not text answer')
            elif not answ_choices:
                raise ValidationError('Answer should contain some choices')
            elif len(answ_choices) > 1 and not question.choices.multiple:
                raise ValidationError('Answer should only one choice')
        else:
            if text_ans == '':
                raise ValidationError('Answer should contain some text')
            if answ_choices:
                raise ValidationError('Answer should contain only text')


        serializer.save()


