
from django.urls import path, include
from . import views

app_name = 'dashboardapp'
urlpatterns = [
    # Example paths
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_course/', views.addCourse_view, name='add_course'),
    path('add_lesson/<int:course_id>', views.add_lesson_view, name='add_lesson'),
    path('view_course/<int:course_id>/<int:lesson_id>/',
         views.view_course, name='view_course'),
    path('view_course/<int:course_id>/', views.view_course, name='view_course'),
    path('view_profile/', views.view_profile, name='view_profile'),

    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_settings/', views.user_settings_view, name='user_settings'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('enroll_course/<int:course_id>',
         views.enroll_course, name='enroll_course'),

]
