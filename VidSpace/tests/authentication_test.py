import os
import unittest
import tempfile

from VidSpace import app

class FlaskrTestCase(unittest.TestCase):
  # set up a new temp database for per test
  def setUp(self):
    self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    self.app = app.app.test_client()
    app.init_db()

  # destroy the temp database for per test
  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(app.app.config['DATABASE'])

  def signup(self, username, password):
        return self.app.post('/signup', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

  # test messages
  def test_signup_messages(self):
    """Test signup messages using helper functions."""
    rv = self.signup(
            "ashutosh@123.com",
            ""
    )
    assert b'Password is required' in rv.data

    rv = self.signup(
            "",
            "123"
    )
    assert b'Username is required' in rv.data