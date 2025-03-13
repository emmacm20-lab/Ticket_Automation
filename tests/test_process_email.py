# 📂 tests/test_process_email.py - Pruebas para el procesamiento de correos
import unittest
from src.process_email import fetch_emails

class TestEmailProcessing(unittest.TestCase):
    def test_fetch_emails(self):
        emails = fetch_emails("test_user", "test_pass", "imap.test.com")
        self.assertIsInstance(emails, list)

if __name__ == "__main__":
    unittest.main()
