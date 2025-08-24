from django.urls import path
from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('message_new/', views.MessageCreateView.as_view(), name='message_new'),
    path('message/<int:pk>/', views.MessageDetailView.as_view(), name='message'),
    path('message_list/', views.MessageListView.as_view(), name='message_list'),
    path('message_edit/<int:pk>/', views.MessageUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('recipient_list/', views.RecipientListView.as_view(), name='recipient_list'),
    path('recipient_new', views.RecipientCreateView.as_view(), name='recipient_new'),
    path('recipient/<int:pk>/', views.RecipientDetailView.as_view(), name='recipient'),
    path('recipient_edit/<int:pk>/', views.RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipient_delete/<int:pk>/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
]