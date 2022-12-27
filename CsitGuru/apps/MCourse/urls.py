from django.urls import path

from . import views

app_name = "Courses"

urlpatterns = [
    #Path Ordering matters
    #----------------------------

    #Events
    path("<slug:slug>/events/", views.EventListApiView.as_view() , name="event_detail"),
    path("<slug:slug>/event/<slug:eslug>/", views.EventDetailApiView.as_view(), name="event_detail"),

    #Semesters
    path("<slug:slug>/semesters/", views.SemesterListApiView, name="semesters"),
   
    #Subjects
    path("<slug:slug>/subjects/", views.SubjectListApiView.as_view() , name="subjects"),
    path("<slug:slug>/subject/<slug:sub_slug>/", views.SubjectDetailApiView, name="subject_detail"),

    path("<slug:slug>/subject/<slug:sub_slug>/notes/<slug:n_slug>/", views.NoteDetailApiView, name="note_detail"),
    path("<slug:slug>/subject/<slug:sub_slug>/books/<slug:b_slug>/", views.BookDetailApiView, name="book_detail"),
    
    #QuestionModels
    path("<slug:slug>/subject/<slug:sub_slug>/questions/", views.ListQuestionModelApiView, name="list_questionmodels"),
    path("<slug:slug>/subject/<slug:sub_slug>/questions/<slug:qm_slug>/", views.QuestionModelDetailApiView, name="questionmodel_detail"),

    path("<slug:slug>/subject/<slug:sub_slug>/question-solutions/<slug:qs_slug>/", views.QuestionModelSolutionDetailApiView, name="questionsolution_detail"),


    #Courses    
    path("list/", views.CourseListApiView.as_view(), name="courses"),
    path("<slug:slug>/", views.CourseDetailApiView.as_view(), name="course_detail"),

 

]
