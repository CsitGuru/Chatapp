from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import DetailView, TemplateView, View
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import (
    Book,
    Course,
    Event,
    Note,
    QuestionModel,
    QuestionSolution,
    Semester,
    Subject,
)
from .seriaizers import (
    BookSerailizer,
    CourseSerializer,
    EventSerailizer,
    NoteSerailizer,
    QuestionSerailizer,
    QuestionSolutionSerailizer,
    SemesterSerailizer,
    SubjectSerailizer,
)


class CourseListApiView(ListAPIView):
   queryset = Course.objects.all()
   serializer_class= CourseSerializer
   
class CourseDetailApiView(RetrieveAPIView):
   lookup_field = 'slug'
   queryset = Course.objects.all()
   serializer_class= CourseSerializer

@api_view(['GET'])
def SemesterListApiView(request, slug):
   print('slug:', slug)
   course_obj = Course.objects.filter(slug=slug).first()
   semesters = list(Semester.objects.filter(course=course_obj).values())
   for semester in semesters:
      semester_obj =Semester.objects.filter(name=semester['name']).first()
      semester['subjects']= list(Subject.objects.filter(course=course_obj, semester=semester_obj).values())
   return Response(semesters)
    
class EventListApiView(ListAPIView):
   queryset = Event.objects.all()
   serializer_class= EventSerailizer
   
class EventDetailApiView(RetrieveAPIView):
   lookup_field = 'slug'
   queryset = Event.objects.all()
   serializer_class= EventSerailizer


class SubjectListApiView(ListAPIView):
   queryset = Subject.objects.all()
   serializer_class= SubjectSerailizer
   

@api_view(['GET'])
def SubjectDetailApiView(request, slug, sub_slug):
   print('slug:', slug)
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   context = {}
   context['name']=subject_obj.name
   context['syllabus'] =subject_obj.description
   context['notes'] = NoteSerailizer(Note.objects.filter(subject =subject_obj), many=True).data
   context['books'] = BookSerailizer(Book.objects.filter(subject =subject_obj), many=True).data
   context['questionmodels'] = QuestionSerailizer(QuestionModel.objects.filter(subject =subject_obj), many=True).data
   context['questionsolutions'] = QuestionSolutionSerailizer(QuestionSolution.objects.filter(subject =subject_obj), many=True).data
   return Response(context)


@api_view(['GET'])
def NoteDetailApiView(request, slug, sub_slug, n_slug):
   print('slug:', slug)
   current_site = get_current_site(request)
   print(current_site)
   print(current_site.domain)
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   note_obj = Note.objects.filter(subject=subject_obj, n_slug=n_slug).first()
   serializer = NoteSerailizer(note_obj, many=False)

   print(serializer.data)
   return Response(serializer.data)


@api_view(['GET'])
def BookDetailApiView(request, slug, sub_slug, b_slug):
   print('slug:', slug)
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   book_obj = Book.objects.filter(subject=subject_obj, b_slug=b_slug).first()
   serializer = BookSerailizer(book_obj, many=False)
   return Response(serializer.data)


@api_view(['GET'])
def ListQuestionModelApiView(request, slug, sub_slug):
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   questionmodel_objs = QuestionModel.objects.filter(subject=subject_obj)
   serializer = QuestionSerailizer(questionmodel_objs, many=True)
   return Response(serializer.data)

@api_view(['GET'])
def QuestionModelDetailApiView(request, slug, sub_slug, qm_slug):
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   questionmodel_obj = QuestionModel.objects.filter(subject=subject_obj, qm_slug=qm_slug).first()
   serializer = QuestionSerailizer(questionmodel_obj, many=False)
   return Response(serializer.data)


@api_view(['GET'])
def QuestionModelSolutionDetailApiView(request, slug, sub_slug, qs_slug):
   course_obj = Course.objects.filter(slug=slug).first()
   subject_obj = Subject.objects.filter(course=course_obj, sub_slug=sub_slug).first()
   questionsolution_obj = QuestionSolution.objects.filter(subject=subject_obj, qs_slug=qs_slug).first()
   serializer = QuestionSolutionSerailizer(questionsolution_obj, many=False)
   return Response(serializer.data)
