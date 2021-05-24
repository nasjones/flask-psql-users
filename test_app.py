from unittest import TestCase
from models import db, connect_db, User, Posts
from app import app


db.drop_all()
db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        Posts.query.delete()
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('<h1>Users</h1>', html)

    def test_new_user_get(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('<h1>Add User</h1>', html)

    def test_new_user_post(self):
        with app.test_client() as client:
            resp = client.post(
                '/users/new', data={'first-name-input': 'Nas', 'last-name-input': "Jones", 'url-input': ''})
            self.assertEqual(resp.status_code, 200)

    def test_user_display(self):
        with app.test_client() as client:
            client.post('/users/new', data={'first-name-input': 'Nas',
                        'last-name-input': "Jones", 'url-input': ''})
            resp = client.get('/users/4')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Nas Jones', html)

    def test_user_display_404(self):
        with app.test_client() as client:
            resp = client.get('/users/200')
            self.assertEqual(resp.status_code, 404)

    def test_add_post(self):
        with app.test_client() as client:
            client.post('/users/new', data={'first-name-input': 'Nas',
                        'last-name-input': "Jones", 'url-input': ''})
            resp = client.post('/users/1/posts/new', data={
                'title-input': 'First post', 'content-input': "Test content", 'url-input': ''})
            self.assertEqual(resp.status_code, 200)

    def test_post_display(self):
        with app.test_client() as client:
            client.post('/users/new', data={'first-name-input': 'Nas',
                        'last-name-input': "Jones", 'url-input': ''})
            client.post('/users/3/posts/new', data={
                'title-input': 'First post', 'content-input': "Test content", 'url-input': ''})
            resp = client.get('/posts/2')
            self.assertEqual(resp.status_code, 200)
