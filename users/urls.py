from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeDoneView,
)
from django.urls import path, reverse_lazy
from users.apps import UsersConfig
from users import views
from users.forms import CustomAuthenticationForm

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            form_class=CustomAuthenticationForm, template_name="registration/login.html"
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("user_info/<int:pk>/", views.CustomUserDetailView.as_view(), name="user_info"),
    path("user_form/<int:pk>/", views.CustomUserUpdateView.as_view(), name="user_form"),
    path("user_form/password/", views.UserPasswordChange.as_view(), name="password"),
    path(
        "password_change/", views.UserPasswordChange.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("user_list/", views.UserListView.as_view(), name="user_list"),
]
