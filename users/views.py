from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm
from django.contrib.auth import login

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
