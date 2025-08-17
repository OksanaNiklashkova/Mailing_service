from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users import views
from users.forms import CustomAuthenticationForm

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(form_class=CustomAuthenticationForm,template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='#'), name='logout'),
]