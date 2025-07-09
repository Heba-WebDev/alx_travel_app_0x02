# listings/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from listings.models import Review, Listing, Booking, User


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating users...")
        # Create host users
        host1 = User.objects.create_user(
            username='host1',
            email='host1@example.com',
            password='testpass123',
            is_host=True
        )

        # Create regular users
        user1 = User.objects.create_user(
            username='traveler1',
            email='traveler1@example.com',
            password='testpass123',
            is_host=False
        )

        self.stdout.write("Creating listings...")
        listing1 = Listing.objects.create(
            title='Beachfront Villa',
            description='Luxury villa with ocean view',
            location='Malibu, CA',
            price_per_night=350,
            max_guests=6,
            host=host1,
            is_active=True
        )

        listing2 = Listing.objects.create(
            title='Downtown Loft',
            description='Modern apartment in city center',
            location='New York, NY',
            price_per_night=200,
            max_guests=4,
            host=host1,
            is_active=True
        )

        self.stdout.write("Creating bookings...")
        booking1 = Booking.objects.create(
            listing=listing1,
            user=user1,
            check_in_date=datetime.now().date() + timedelta(days=7),
            check_out_date=datetime.now().date() + timedelta(days=14),
            guests=4,
            total_price=350 * 7,
            status='confirmed'
        )

        self.stdout.write("Creating reviews...")
        Review.objects.create(
            listing=listing1,
            user=user1,
            rating=5,
            comment='Amazing place with fantastic views!'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
