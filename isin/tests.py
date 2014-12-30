from django.test import TestCase
from django.utils import timezone
import datetime
from models import Status

def create_status(s, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Status.objects.create(status=s,
                                 pub_date=time)

class EmptyDBTests(TestCase):
    def test_empty_index_view(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('s' in resp.context)
        self.assertIn('without status', resp.context['s'].status)

    def test_index_view_two_statuses_one_in_past(self):
        create_status("future status", 1)
        create_status("past status", -1)
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        #import pdb; pdb.set_trace()
        self.assertTrue('s' in resp.context)
        self.assertIn('future status', resp.context['s'].status)

class PopulatedDBStatusTests(TestCase):
    fixtures = ['isin_testdata']

    def test_index_view_one_status(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('s' in resp.context)
        self.assertIn('away in Montreal', resp.context['s'].status)

    def test_index_view_two_statuses_one_in_future(self):
        # assumes that isin_testdata has a test in the past
        create_status("future status", 1)
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('s' in resp.context)
        self.assertIn('future status', resp.context['s'].status)

class UpdateTests(TestCase):
    def test_not_logged_in(self):
        resp = self.client.get('/u')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login', resp.content)
        self.assertNotIn('submit', resp.content)

        #self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])

# random python debugging hint:
#import pdb; pdb.set_trace()
