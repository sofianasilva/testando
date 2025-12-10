from .models import (
    AdoptedLevel,
    Statement,
    FeedbackQuestionnaire,
    Questionnaire,
    QuestionnaireExcel,
    Answer,
)
from .serializers import (
    AdoptedLevelReadSerializer, AdoptedLevelWriteSerializer,
    StatementReadSerializer, StatementWriteSerializer,
    FeedbackQuestionnaireReadSerializer, FeedbackQuestionnaireWriteSerializer,
    QuestionnaireReadSerializer, QuestionnaireWriteSerializer,
    QuestionnaireExcelReadSerializer, QuestionnaireExcelWriteSerializer,
    AnswerReadSerializer, AnswerWriteSerializer,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_condition import And, Or
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .pagination import CustomPagination
from rest_framework import generics
from rest_framework import filters
import django_filters.rest_framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class AdoptedLevelViewSet(ModelViewSet):
    queryset = AdoptedLevel.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['percentage']
    ordering_fields = 'percentage'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AdoptedLevelReadSerializer
        return AdoptedLevelWriteSerializer

class StatementViewSet(ModelViewSet):
    queryset = Statement.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['code', 'statement']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return StatementReadSerializer
        return StatementWriteSerializer

class FeedbackQuestionnaireViewSet(ModelViewSet):
    queryset = FeedbackQuestionnaire.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['collected_date']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FeedbackQuestionnaireReadSerializer
        return FeedbackQuestionnaireWriteSerializer

class QuestionnaireViewSet(ModelViewSet):
    queryset = Questionnaire.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = ['applied_date']
    search_fields = ['applied_date']
    ordering_fields = ['applied_date']
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return QuestionnaireReadSerializer
        return QuestionnaireWriteSerializer

class QuestionnaireExcelViewSet(ModelViewSet):
    queryset = QuestionnaireExcel.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = ['applied_date']
    search_fields = ['applied_date']
    ordering_fields = ['applied_date']
    ordering = ["id"]
    
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return QuestionnaireExcelReadSerializer
        return QuestionnaireExcelWriteSerializer

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['comment']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AnswerReadSerializer
        return AnswerWriteSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_questionnaire(request):
    """
    Submit questionnaire answers.
    Expected payload:
    {
        "questionnaire_type": "innovation_system",
        "answers": {
            "IS.01": {"adoption": "fully_adopted", "comment": "We have this implemented"},
            "IS.02": {"adoption": "partially_adopted", "comment": "Work in progress"}
        }
    }
    """
    try:
        data = request.data
        questionnaire_type = data.get('questionnaire_type')
        answers_data = data.get('answers', {})
        
        if not questionnaire_type or not answers_data:
            return Response(
                {'error': 'questionnaire_type and answers are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new questionnaire record
        questionnaire = Questionnaire.objects.create(
            applied_date=timezone.now(),
            employee_questionnaire=None  # Can be linked to user later if needed
        )
        
        # Process each answer
        saved_answers = []
        for question_code, answer_data in answers_data.items():
            adoption_level = answer_data.get('adoption', '')
            comment = answer_data.get('comment', '')
            
            # Find or create the statement
            statement, created = Statement.objects.get_or_create(
                code=question_code,
                defaults={'text': f'Statement for {question_code}'}
            )
            
            # Find or create adoption level based on the adoption string
            adoption_mapping = {
                'not_adopted': {'name': 'Not Adopted', 'percentage': 0},
                'partially_adopted': {'name': 'Partially Adopted', 'percentage': 50},
                'fully_adopted': {'name': 'Fully Adopted', 'percentage': 100},
            }
            
            adoption_info = adoption_mapping.get(adoption_level, adoption_mapping['not_adopted'])
            adopted_level, created = AdoptedLevel.objects.get_or_create(
                name=adoption_info['name'],
                defaults={
                    'description': adoption_info['name'],
                    'percentage': adoption_info['percentage']
                }
            )
            
            # Create the answer
            answer = Answer.objects.create(
                questionnaire_answer=questionnaire,
                adopted_level_answer=adopted_level,
                statement_answer=statement,
                comment_answer=comment,
                organization_answer_id=1  # Default organization, can be made dynamic
            )
            saved_answers.append({
                'question_code': question_code,
                'adoption': adoption_level,
                'comment': comment
            })
        
        return Response({
            'message': 'Questionnaire submitted successfully',
            'questionnaire_id': questionnaire.id,
            'answers_count': len(saved_answers),
            'answers': saved_answers
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to submit questionnaire: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
