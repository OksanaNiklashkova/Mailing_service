from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, ListView
from .forms import CustomUserCreationForm, CustomUserForm, UserPasswordChangeForm, CustomUserManagerForm
from django.contrib.auth import login

from .models import CustomUser


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomUserDetailView(DetailView):
    """Контроллер для просмотра информации о пользователе"""
    model = CustomUser
    template_name = 'users/user_info.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(CustomUser, pk=pk)
        return user



class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования профиля пользователя"""
    model = CustomUser
    template_name = 'users/user_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        target_user = self.get_object()
        if user == target_user:
            return CustomUserForm
        if user.has_perm('users.can_blocked_user'):
            return CustomUserManagerForm
        else:
            raise PermissionDenied("У вас нет прав для редактирования этого профиля пользователя")

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(CustomUser, pk=pk)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object
        return context


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"
    extra_context = {'title': "Изменение пароля"}


class UserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'