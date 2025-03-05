
from django.urls import path, include
from .views import login_view, register_view, dashboard_view
app_name = 'authapp'

urlpatterns = [
    # Example paths

    path('', login_view, name='login'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', login_view, name='login_view'),
    path('signup/', register_view, name='signup'),
    path('dashboard/',dashboard_view)
  

]
