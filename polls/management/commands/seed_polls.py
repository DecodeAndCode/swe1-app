from django.core.management.base import BaseCommand
from django.utils import timezone

from polls.models import Choice, Question


class Command(BaseCommand):
    help = "Create a sample poll if the database has no questions."

    def handle(self, *args, **options):
        if Question.objects.exists():
            self.stdout.write("Polls already exist; nothing to seed.")
            return
        question = Question.objects.create(
            question_text="What's your favorite color?",
            pub_date=timezone.now(),
        )
        for text in ("Yellow", "Green", "Blue"):
            Choice.objects.create(question=question, choice_text=text)
        self.stdout.write("Created sample poll.")
