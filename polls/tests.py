import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        self.assertIs(Question(pub_date=time).was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        self.assertIs(Question(pub_date=time).was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        self.assertIs(Question(pub_date=time).was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question("Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        question = create_question("Past question.", days=-30)
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        q1 = create_question("Past question 1.", days=-30)
        q2 = create_question("Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q2, q1])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future = create_question("Future question.", days=5)
        response = self.client.get(reverse("polls:detail", args=(future.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past = create_question("Past Question.", days=-5)
        response = self.client.get(reverse("polls:detail", args=(past.id,)))
        self.assertContains(response, past.question_text)


class QuestionResultsViewTests(TestCase):
    def test_results_with_past_question(self):
        past = create_question("Past Question.", days=-5)
        Choice.objects.create(question=past, choice_text="Choice 1", votes=3)
        response = self.client.get(reverse("polls:results", args=(past.id,)))
        self.assertContains(response, past.question_text)
        self.assertContains(response, "3 votes")

    def test_results_with_future_question(self):
        future = create_question("Future question.", days=5)
        response = self.client.get(reverse("polls:results", args=(future.id,)))
        self.assertEqual(response.status_code, 404)


class ModelStringTests(TestCase):
    def test_question_str(self):
        q = create_question("What's up?", days=-1)
        self.assertEqual(str(q), "What's up?")

    def test_choice_str(self):
        q = create_question("Q?", days=-1)
        c = Choice.objects.create(question=q, choice_text="Not much")
        self.assertEqual(str(c), "Not much")


class NavigationTests(TestCase):
    def test_index_has_heading(self):
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "<h1>Available Polls</h1>")

    def test_detail_links_back_to_index(self):
        q = create_question("Q?", days=-1)
        response = self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertContains(response, "Back to polls")
        self.assertContains(response, 'href="%s"' % reverse("polls:index"))

    def test_results_links_back_to_index(self):
        q = create_question("Q?", days=-1)
        response = self.client.get(reverse("polls:results", args=(q.id,)))
        self.assertContains(response, "Back to polls")
        self.assertContains(response, 'href="%s"' % reverse("polls:index"))


class VoteTests(TestCase):
    def test_vote_increments_and_redirects(self):
        q = create_question("Q?", days=-1)
        c = Choice.objects.create(question=q, choice_text="A")
        response = self.client.post(
            reverse("polls:vote", args=(q.id,)), {"choice": c.id}
        )
        self.assertRedirects(response, reverse("polls:results", args=(q.id,)))
        c.refresh_from_db()
        self.assertEqual(c.votes, 1)

    def test_vote_without_choice_shows_error(self):
        q = create_question("Q?", days=-1)
        response = self.client.post(reverse("polls:vote", args=(q.id,)))
        self.assertContains(response, "You didn")
