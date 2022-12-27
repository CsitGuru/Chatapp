from django.contrib import admin

from .models import (
    Book,
    Course,
    Event,
    Note,
    QuestionModel,
    QuestionSolution,
    Semester,
    Subject,
    Year,
)

admin.site.register(Year)
class SuperCourseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "date_added",
        "date_updated",
    )
    search_fields = ["name", ]

admin.site.register(Course, SuperCourseAdmin)

class NoteAlbum(admin.TabularInline):
   model = Note
   extra = 5

class BookAlbum(admin.TabularInline):
    model = Book
    extra = 2  
class QuestionAlbum(admin.TabularInline):
    model = QuestionModel
    extra =1

class QuestionSolutionAblum(admin.TabularInline):
    model = QuestionSolution
    extra = 1      
  
class SubjectAdmin(admin.ModelAdmin):
   list_filter = ["semester", "course"]
   inlines = [NoteAlbum, BookAlbum ,QuestionAlbum, QuestionSolutionAblum]   
   
admin.site.register(Subject, SubjectAdmin)

admin.site.register(Event)


class SuperSemesterAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "course",
        "date_updated",
    )
admin.site.register(Semester, SuperSemesterAdmin)


