from unittest import TestCase
from models import db, connect_db, User
from app import app


db.drop_all()
db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)

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
            self.assertEqual(resp.status_code, 302)

    def test_user_display(self):
        with app.test_client() as client:
            client.post('/users/new', data={'first-name-input': 'Nas',
                        'last-name-input': "Jones", 'url-input': ''})
            resp = client.get('/users/2')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Nas Jones', html)

    def test_user_display_404(self):
        with app.test_client() as client:
            resp = client.get('/users/200')
            self.assertEqual(resp.status_code, 404)
