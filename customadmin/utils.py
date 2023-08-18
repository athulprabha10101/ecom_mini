from datetime import datetime, timedelta
from django.utils import timezone
from random import choice, randint
from customadmin.models import UserProfile, Orders  # Replace with your actual model imports

def generate_sample_orders():
    users = UserProfile.objects.exclude(name='GUEST')
    order_status_choices = ['complete']  # Order status is always 'complete'

    start_date = timezone.now() - timedelta(days=3 * 365)
    end_date = timezone.now()

    for _ in range(100):  # Generate 100 sample orders
        user = choice(users)
        order_date = start_date + timedelta(
            seconds=randint(0, int((end_date - start_date).total_seconds()))
        )
        order_total_price = randint(10000, 100000)  # Adjust the price range as needed

        order = Orders.objects.create(
            user=user,
            order_address=user.addresses.first(),  
            order_date=order_date,
            order_status=choice(order_status_choices),
            order_total_price=order_total_price
        )

    print("Sample orders generated successfully!")

# Call the function to generate orders
\
