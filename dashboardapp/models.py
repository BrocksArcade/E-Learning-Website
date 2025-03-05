from django.db import models
from django.utils import timezone
from authapp.models import CustomUser
import datetime
# Create your models here.


class Course(models.Model):
    coursename = models.CharField(max_length=10, unique=True)
    coursedesc = models.CharField(max_length=300)
    createdby = models.CharField(max_length=100)
    totalstudents = models.IntegerField(default=0)
    def __str__(self):
        return self.name

    # Many to one - One Course - many lessons , one lesson - many comments

# lesson is inside each course
class Lesson(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons') 
    title = models.CharField(max_length=50) 
    video = models.FileField(upload_to='videos/', null=False) 
    created_at = models.DateTimeField(default=datetime.datetime.now())  
    def __str__(self):
        return f"Lesson {self.order}: {self.title}"
   
# comments are inside each lesson and loaded up during click

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')  
    name = models.CharField(max_length=255) 
    content = models.TextField() 
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return f"Comment by {self.name} on {self.lesson.title}"
    class Meta:
        ordering = ['created_at']
        
        
class Enrollment(models.Model):
    # student here is user 
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='enrollments')
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
   

    class Meta:
        unique_together = ('student', 'course')  # Prevent duplicate enrollments
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.coursename}"