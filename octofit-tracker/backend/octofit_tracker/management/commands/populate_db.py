from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data safely (one by one)
        for obj in get_user_model().objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Team.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Activity.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Leaderboard.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()
        for obj in octo_models.Workout.objects.all():
            if getattr(obj, 'id', None):
                obj.delete()

        # Create teams
        marvel = octo_models.Team.objects.create(name='Team Marvel')
        dc = octo_models.Team.objects.create(name='Team DC')

        # Create users
        ironman = get_user_model().objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel)
        captain = get_user_model().objects.create_user(username='captainamerica', email='cap@marvel.com', password='password', team=marvel)
        batman = get_user_model().objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc)
        superman = get_user_model().objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc)

        # Create activities
        octo_models.Activity.objects.create(user=ironman, type='run', duration=30, calories=300)
        octo_models.Activity.objects.create(user=batman, type='cycle', duration=45, calories=400)
        octo_models.Activity.objects.create(user=superman, type='swim', duration=60, calories=500)
        octo_models.Activity.objects.create(user=captain, type='walk', duration=20, calories=100)

        # Create workouts
        octo_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes', duration=40)
        octo_models.Workout.objects.create(name='Strength Training', description='Strength for all heroes', duration=60)

        # Create leaderboard
        octo_models.Leaderboard.objects.create(team=marvel, points=400)
        octo_models.Leaderboard.objects.create(team=dc, points=600)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
