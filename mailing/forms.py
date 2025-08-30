from django.core.exceptions import ValidationError
from django import forms
from django.http import request

from mailing.models import Message, Recipient, Mailing

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class MessageForm(forms.ModelForm):
    """Форма для создания нового сообщения"""
    class Meta:
        model = Message
        fields = ['topik', 'text',]
        exclude = ['owner',]


    def __init__(self, *args, **kwargs):
        super(MessageForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['topik'].widget.attrs.update({'placeholder': 'Тема письма',})
        self.fields['text'].widget.attrs.update({'placeholder': 'Текст письма'})

class RecipientForm(forms.ModelForm):
    """Форма для создания нового получателя рассылки"""
    class Meta:
        model = Recipient
        fields = ['email', 'recipient_name', 'comment',]
        exclude = ['owner',]


    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs.update({'placeholder': 'Почта получателя',})
        self.fields['recipient_name'].widget.attrs.update({'placeholder': 'ФИО получателя'})
        self.fields['comment'].widget.attrs.update({'placeholder': 'Комментарий'})


class MailingForm(forms.ModelForm):
    """Форма для создания новой рассылки"""
    message = forms.ModelChoiceField(queryset=Message.objects.all())
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'status', 'started_at', 'finished_at',]
        exclude = []


class MailingManagerForm(forms.ModelForm):
    """Форма редактирования рассылки для менеджера"""
    class Meta:
        model = Mailing
        fields = ['status',]
