from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from mailing.forms import MessageForm, RecipientForm, MailingForm
from mailing.models import Message, Recipient, Mailing, SendAttempt
from mailing.services import send_message


class HomeView(TemplateView):
    template_name = 'mailing/home.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра сообщения"""
    model = Message
    template_name = 'mailing/message.html'
    context_object_name = 'message'


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка сообщений"""
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
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


class RecipientListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка получателей"""
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания профиля нового получателя рассылки"""
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра профиля получателя рассылки"""
    model = Recipient
    template_name = 'mailing/recipient.html'
    context_object_name = 'recipient'


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования профиля получателя рассылки"""
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin,DeleteView):
    """Контроллер для удаления профиля получателя рассылки"""
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def post(self, request, *args, **kwargs):
        recipient = get_object_or_404(Recipient, id=kwargs.get('pk'))
        user = self.request.user
        if user != recipient.owner:
            return HttpResponseForbidden("У вас нет прав для удаления профиля получателя рассылки")
        recipient.delete()
        return redirect('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка рассылок"""
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра рассылки"""
    model = Mailing
    template_name = 'mailing/mailing.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def post(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, id=kwargs.get('pk'))
        user = self.request.user
        if user != mailing.owner:
            return HttpResponseForbidden("У вас нет прав для удаления рассылки")
        mailing.delete()
        return redirect('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SendAttemptListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка попыток рассылки"""
    model = SendAttempt
    template_name = 'mailing/send_attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempts = self.get_queryset()
        context['total_attempts'] = attempts.count()
        context['successful_attempts'] = attempts.filter(status='успешно').count()
        context['unsucessful_attempts'] = attempts.filter(status='не успешно').count()
        context['sending_mails'] = 0
        context['sending_mails'] = sum(
            attempt.mailing.recipients.count()
            for attempt in attempts.filter(status='успешно')
        )
        return context

    def get_queryset(self):
        queryset = SendAttempt.objects.filter(owner=self.request.user).order_by('attempt_datetime')
        return queryset


class SendAttemptDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения информации о попытке рассылки"""
    model = SendAttempt
    template_name = 'mailing/send_attempt.html'
    context_object_name = 'attempt'


class SendMailingView(View):
    template_name = 'mailing/send_mailing.html'

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)

        success = send_message(mailing.pk, request)

        if success:
            print('Рассылка успешно отправлена')
        else:
            print('Рассылка не отправлена')

        return redirect('mailing:mailing_list')