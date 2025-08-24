from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing.forms import MessageForm
from mailing.models import Message, Recipient


class HomeView(TemplateView):
    template_name = 'mailing/home.html'


class MessageCreateView(CreateView):
    """Контроллер для создания сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(DetailView):
    """Контроллер для просмотра сообщения"""
    model = Message
    template_name = 'mailing/message.html'
    context_object_name = 'message'

class MessageListView(ListView):
    """Контроллер для просмотра списка сообщений"""
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

class MessageUpdateView(UpdateView):
    """Контроллер для редактирования сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessageDeleteView(DeleteView):
    """Контроллер для удаления сообщения"""
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def post(self, request, *args, **kwargs):
        message = get_object_or_404(Message, id=kwargs.get('pk'))
        user = self.request.user
        if user != message.owner:
            return HttpResponseForbidden("У вас нет прав для удаления сообщения")
        message.delete()
        return redirect('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipientListView(ListView):
    """Контроллер для просмотра списка сообщений"""
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'