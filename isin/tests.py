from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
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

    def test_not_logged_in_cant_update_status(self):
        resp = self.client.post('/u', {'status': 'out'})
        resp = self.client.get('/')
        self.assertIn('without status', resp.context['s'].status)

    def test_log_in_no_user(self):
        l = self.client.login(username='plam', password='secret')
        self.assertFalse(l)
        resp = self.client.get('/u')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login', resp.content)
        self.assertNotIn('submit', resp.content)

    def test_log_in_bad_password(self):
        user = User.objects.create_user('plam', 'p.lam@ece.uwaterloo.ca', 'sekrit')
        l = self.client.login(username='plam', password='secret')
        self.assertFalse(l)
        resp = self.client.get('/u')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login', resp.content)
        self.assertNotIn('submit', resp.content)

    def test_logged_in_not_admin(self):
        user = User.objects.create_user('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        resp = self.client.get('/u')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Logout', resp.content)
        self.assertNotIn('submit', resp.content)

    def test_logged_in_admin(self):
        user = User.objects.create_superuser('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        resp = self.client.get('/u')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Logout', resp.content)
        self.assertIn('submit', resp.content)
        self.assertIn('without status', resp.context['s'].status)

    def test_update(self):
        user = User.objects.create_superuser('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        self.client.post('/u', {'status': u'outUniqToken'})
        resp = self.client.get('/u')
        self.assertEquals(u'outUniqToken', resp.context['s'].status)

    def test_replace_older_update(self):
        user = User.objects.create_superuser('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        self.client.post('/u', {'status': u'outUniqToken'})
        self.client.post('/u', {'status': u'followpainshortdirect'})
        resp = self.client.get('/u')
        self.assertEquals(u'followpainshortdirect', resp.context['s'].status)

    def test_do_not_replace_older_update(self):
        user = User.objects.create_superuser('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        create_status('newest', 1)
        self.client.post('/u', {'status': u'followpainshortdirect'})
        resp = self.client.get('/u')
        self.assertEquals(u'newest', resp.context['s'].status)

class QuickUpdateTests(TestCase):
    """ Tests quick-update (i.e. update-by-ip-address) functionality.

    Uses the hardcoded IP address as a test. Since we don't have a mock reverse-DNS library, we won't test the DNS functionality.
    """
    def test_not_logged_in(self):
        resp = self.client.get('/q')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login', resp.content)
        self.assertNotIn('submit', resp.content)

    def test_not_logged_in(self):
        user = User.objects.create_superuser('plam', 'p.lam@ece.uwaterloo.ca', 'secret')
        l = self.client.login(username='plam', password='secret')
        self.assertTrue(l)
        resp = self.client.get('/q', REMOTE_ADDR='129.97.90.101')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('cambridge', resp.content)
        self.assertIn('DC2597D', resp.context['s'].status)

# random python debugging hint:
#import pdb; pdb.set_trace()
