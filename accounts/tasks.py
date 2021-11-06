from celery import Celery
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from config.celery import celery_app
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@celery_app.task
def task_auth_send_mail(subject, message, from_email, recipient_list):
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)