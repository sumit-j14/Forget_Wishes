# Import date class from datetime module
from datetime import datetime

from celery import shared_task
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule

# main related imports
from django.core.mail import send_mail
from core import settings
from django.utils import timezone
from datetime import timedelta


@shared_task(bind=True)
def store_in_db(self, user, date, month, wish_who, custom_wish, recipient_email):
    print("inside celery function ")

    # converting to int type as per integer serializer model field
    date = int("".join(date.split()))
    month = int("".join(month.split()))

    entry = {"user": user, "birth_date": date, "birth_month": month, "wish_who": wish_who, "custom_wish": custom_wish,
             "recipient_email": recipient_email}
    serializer = ScheduleSerializer(data=entry)

    # saving the entry inside database upon serializer validation
    if serializer.is_valid():
        print("valid entry")
        serializer.save()
    else:
        print("invalid")


@shared_task(bind=True)
def send_mail_celery(self):
    users = Schedule.objects.all()
    current_date = datetime.now()
    for current_user in users:
        # checking whether to wish today or not
        if current_date.day == current_user and current_date.month == current_user.month:
            mail_subject = "Hi " + current_user.wish_who + " "
            message = "" + current_user.custom_wish + "from" + current_user.user
            to_email = current_user.recipient_email
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        else:
            pass
    return "done"
