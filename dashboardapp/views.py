
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from authapp.models import CustomUser
from dashboardapp.models import Enrollment

from authapp import models
import re

from .models import Comment, Course, Lesson
# Create your views here.


def dashboard_view(request):

    user = request.user


#   we are fetching IDS of all courses User is enrolled into , ofc teachers wont need this
    if user.role == 'student':
        enrolled_courses = Enrollment.objects.filter(
            student=user).values_list('course_id', flat=True)
        context = {
            'user': user,
            'courses': Course.objects.all(),
            'enrolled_courses': enrolled_courses
        }
    else:
        context = {
            'user': user,
            'courses': Course.objects.all()
        }

    return render(request, 'dashboard_.html', context)


def addCourse_view(request):
    if request.method == 'POST':
        course_name = request.POST.get('coursename')
        description = request.POST.get('description')

        if Course.objects.filter(coursename=course_name).exists():
            messages.error(request, "Name Already Exists")
            return render(request, 'add_course.html', {'coursename': course_name, 'description': description})

        else:

            Course.objects.create(
                coursename=course_name,
                coursedesc=description,
                totalstudents=0,
                createdby=request.user.username
            ).save()

            return redirect('dashboardapp:dashboard')

    return render(request, 'add_course.html')


def view_course(request, course_id=None, lesson_id=None):

    # Fetch the course by id
    course_ = get_object_or_404(Course, id=course_id)
    selected_lesson = None
    comments = None
    lesson = Lesson.objects.filter(course=course_)

    if lesson_id:
        #  get lessons from lesson id
        selected_lesson = get_object_or_404(
            Lesson, id=lesson_id, course=course_)
        comments = Comment.objects.filter(lesson=selected_lesson)
        print(f"lesson selected {selected_lesson.title}")
        # Handle comment submission, if comment was posted we will add into comments of selected lesson
        if request.method == "POST" and "content" in request.POST:
            content_ = request.POST.get("content")
            newcomment = Comment.objects.create(
                name=request.user.username,
                content=content_,
                lesson=selected_lesson
            )
            print(f"Comment added {newcomment.name}")
            newcomment.save()
            comments = Comment.objects.filter(lesson=selected_lesson)

    context = {
        'course': course_,
        'lessons': lesson,
        'selected_lesson': selected_lesson,
        'comments': comments,
    }
    return render(request, 'course_details.html', context)


def add_lesson_view(request, course_id=None):
    # Fetch the course using the course_id
    course_ = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title_ = request.POST.get('title')
        video_ = request.FILES.get('video')
        newlesson = Lesson.objects.create(
            title=title_, video=video_, course=course_)
        print(newlesson.title)
        newlesson.save()
        return redirect('dashboardapp:view_course', course_id=course_.id)
    else:
        return render(request, 'add_lesson.html', {'course': course_})


def enroll_course(request, course_id):
    if request.user.role == 'student':
        course = get_object_or_404(Course, id=course_id)
        # Check if already enrolled
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            Enrollment.objects.create(student=request.user, course=course)
            course.totalstudents += 1
            course.save()
        return redirect('dashboardapp:dashboard')
    else:
        return redirect('dashboardapp:dashboard')


def user_logout(request):
    logout(request)  # Logs out the current user
    return redirect('authapp:login')
def user_settings_view(request ):
     users = CustomUser.objects.exclude(pk=request.user.pk) # Except self all other users
     courses= Course.objects.all()
     return render(request, 'usersettings.html', {'users': users, 'courses':courses})
 
def delete_user(request, user_id):
      user_to_delete = get_object_or_404(CustomUser, pk=user_id)
      user_to_delete.delete()
      messages.success(request, f"User {user_to_delete.username} has been deleted successfully.")
      return redirect('dashboardapp:user_settings')
  
  
def delete_course(request, course_id):
      course_to_delete = get_object_or_404(Course, pk=course_id)
      course_to_delete.delete()
      messages.success(request, f"User {course_to_delete.coursename} has been deleted successfully.")
      return redirect('dashboardapp:user_settings')
    
    
    

def view_profile(request):
    if request.method == 'POST':
        newusername = request.POST.get('username')
        newpassword = request.POST.get('password')
        curpassword = request.POST.get('currentpwd')

        if not request.user.check_password(curpassword):
            messages.error(request, 'Wrong current password.')
            return redirect('dashboardapp:view_profile')

        # Check if the new username is not empty and already exists (excluding the current user)
        if not newusername or newusername.strip() == '' or CustomUser.objects.exclude(pk=request.user.pk).filter(username=newusername).exists():
            messages.error(
                request, 'Username already exists or is invalid. Please choose a different one.')
            return redirect('dashboardapp:view_profile')

        if newpassword and newpassword.strip() != '':
            if len(newpassword) < 8:
                messages.error(
                    request, 'Password must be at least 8 characters long.')
                return redirect('dashboardapp:view_profile')

            if not re.search(r'[A-Za-z]', newpassword) or not re.search(r'[0-9]', newpassword):
                messages.error(
                    request, 'Password must contain at least one letter and one number.')
                return redirect('dashboardapp:view_profile')

            # Set the new password
            request.user.set_password(newpassword)

        # Update the username (only if it's valid)
        request.user.username = newusername
        request.user.save()

        messages.success(
            request, 'Your profile has been updated successfully.')
        return redirect('authapp:login')

    return render(request, 'profilepage.html')
