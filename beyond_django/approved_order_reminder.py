from django.core.mail import send_mail
from django_project.private_settings import SERVER_EMAIL_ADDRESS
from django_project.private_settings import ORDER_MANAGER_EMAIL_ADDRESSES
from django_project.private_settings import ALLOWED_HOSTS
from django.urls import reverse

from order_management.models import Order

orders = Order.objects.all()

# if there are approved orders
try:
    orders.get(status="Approved")
    email_text = '''Dear Order Manager,

There are approved orders pending in the database. Please place the orders at your earliest convenience.
    
You can find them here: https://{}:/order_management/order/?q-l=on&q=status+%3D+%22approved%22+'''.format(ALLOWED_HOSTS[0])

    send_mail(
        subject="Approved orders are pending",
        message=email_text,
        from_email=SERVER_EMAIL_ADDRESS,
        recipient_list=ORDER_MANAGER_EMAIL_ADDRESSES
    )

except:
    pass