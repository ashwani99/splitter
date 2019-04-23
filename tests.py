from app import create_app, db
from app.models import User
from config import TestConfig
import unittest


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='ashwani', email='ashwani@example.com')
        u.set_password('password')
        self.assertFalse(u.verify_password('ashwani'))
        self.assertTrue(u.verify_password('password'))


if __name__ == '__main__':
    unittest.main()