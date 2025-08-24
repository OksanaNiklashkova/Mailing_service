from django.core.exceptions import ValidationError
from django import forms

from mailing.models import Message


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
