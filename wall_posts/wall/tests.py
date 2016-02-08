from django.test import TestCase
from django.test import Client
from wall.models import Message
from django.contrib.auth.models import User
from django.utils import timezone


class WallTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test')
        self.user_2 = User.objects.create_user('homer', 'homer@simpson.net', 'simpson')

    def test_wall_profile(self):
        c = Client()
        response = c.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_wall_start(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 200)

    def test_wall_not_found(self):
        c = Client()
        response = c.get('/accounts/')
        self.assertEquals(response.status_code, 404)

    def test_wall_login(self):
        login = self.client.login(username='homer', password='simpson')
        self.assertTrue(login)

    def test_wall_login_redirect(self):
        self.client.login(username='homer', password='simpson')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

    def test_wall_context_empty(self):
        c = Client()
        response = c.get('/accounts/profile/')
        self.assertEquals(response.context['all_messages'], 0)

    def test_wall_context_empty_nodes(self):
        c = Client()
        response = c.get('/accounts/profile/')
        self.assertEquals(len(response.context['nodes']), 0)

    def test_wall_create_model(self):
        Message.objects.create(
            user=self.user,
            message='Test message',
            date_save=timezone.now(),
            likes=0,
            parent=None
        ).save()
        self.assertEquals(Message.objects.all().count(), 1)

    def tearDown(self):
        self.user.delete()
        self.user_2.delete()
