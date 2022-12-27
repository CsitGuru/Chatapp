import black
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Course(models.Model):
    name = models.CharField(null=True, max_length=100)
    slug = models.SlugField(null=True, editable=False)
    description = RichTextUploadingField(
        null=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="sourcecode",
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)
   
    def get_absolute_url(self):
        return reverse("Courses:course_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.name)
        
class Year(models.Model):
    year = models.IntegerField(null=True )
    y_slug = models.CharField(max_length=50, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.year)
        super(Year, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.year}"

class Semester(models.Model):
    INTEGER_CHOICES=(
        ('a', 1),
        ('b', 2),
        ('c', 3),
        ('d', 4),
        ('e', 5),
        ('f', 6),
        ('g', 7),
        ('h', 8),
    )
    name = models.CharField(null=True, max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    order = models.CharField(choices=INTEGER_CHOICES, null=True, max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"  

    class Meta:
        ordering=('order',)              

class Subject(models.Model):
    name = models.CharField(null=True, max_length=200)
    sub_slug = models.SlugField(null=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null= True)
    description = RichTextUploadingField(
        null=True,
        blank=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="default",
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse("Courses:subject_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.sub_slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    name = models.CharField(null=True, max_length=200)
    n_slug = models.SlugField(null=True, editable=False)
    files = models.FileField(null=True ,blank=True)
    link = models.URLField(null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        self.n_slug = slugify(self.name)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


  
class QuestionModel(models.Model):
    name = models.CharField(null=True, max_length=200)
    qm_slug = models.SlugField(null=True, editable=False)
    description = RichTextUploadingField(
        null=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="default",
        blank=True
    )
    link = models.URLField(null=True,blank=True)
    files = models.FileField(null=True ,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.name}"  

    def save(self, *args, **kwargs):
        self.qm_slug = slugify(self.name)
        super(QuestionModel, self).save(*args, **kwargs)

class QuestionSolution(models.Model):
    name = models.CharField(null=True, max_length=200)
    qs_slug = models.SlugField(null=True, editable=False)
    files = models.FileField(blank=True)
    description = RichTextUploadingField(
        null=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="default",
        blank=True
    )
    link = models.URLField(null=True,blank=True)    
    files = models.FileField(null=True ,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"     

    def save(self, *args, **kwargs):
        self.qs_slug = slugify(self.name)
        super(QuestionSolution, self).save(*args, **kwargs)



class Book(models.Model):
    name = models.CharField(null=True, max_length=200)
    b_slug = models.SlugField(null=True, editable=False)
    files = models.FileField(null=True ,blank=True)
    link = models.URLField(null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"       

    def save(self, *args, **kwargs):
        self.b_slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)

class Event(models.Model):
    EVENT_CHOICES = (
        ("Notice", "Notice"),
        ("Exam Routine", "Exam Routine"),
    )
    name = models.CharField(null=True, max_length=200)
    e_slug = models.SlugField(null=True, editable=False)
    category = models.CharField(choices=EVENT_CHOICES , max_length=50, null=True)
    description = RichTextUploadingField(
        null=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="default",
        blank=True
    )
    link = models.URLField(null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posted_on =  models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    semseter = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"        
    
    def save(self, *args, **kwargs):
        self.e_slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

