import random
import datetime
from django.utils import timezone
from .models import UserProfile, Orders


def random_datetime(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_sample_orders():
    users = UserProfile.objects.exclude(name='GUEST')
    order_status_choices = ['complete']  # Order status is always 'complete'

    start_date = timezone.now() - datetime.timedelta(days=3 * 365)
    end_date = timezone.now()

    for _ in range(100):  # Generate 100 sample orders
        user = random.choice(users)
        order_date = random_datetime(start_date, end_date)
        order_total_price = random.randint(10000, 100000)  # Adjust the price range as needed

        order = Orders.objects.create(
            user=user,
            order_address=user.addresses.first(),  
            order_date=order_date,
            order_status=random.choice(order_status_choices),
            order_total_price=order_total_price
        )

    print("Sample orders generated successfully!")