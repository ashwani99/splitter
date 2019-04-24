from app import create_app, db
from app.models import User, Bill, BillDetails
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


class BillsModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_bill_creation(self):
        # create users
        u1 = User(username='user1', email='user1@example.com')
        u2 = User(username='user2', email='user2@example.com')
        u3 = User(username='user3', email='user3@example.com')
        u4 = User(username='user4', email='user4@example.com')
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

        # create a bill to split
        b = Bill(title='New Bill', desc='some description',
            amount=250, payer=u3)
        db.session.add(b)
        db.session.commit()

        self.assertTrue(len(b.bill_details) == 1)
        self.assertTrue(b.bill_details[0].user == u3)

        participants = [u1, u2, u3, u4]
        shares = [50, 100, 75, 25]
        for participant, share in zip(participants, shares):
            b.add_participant(participant, share)

        db.session.commit()
        self.assertTrue(len(b.bill_details) == 4)
        

if __name__ == '__main__':
    unittest.main()