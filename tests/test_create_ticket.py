# 📂 tests/test_create_ticket.py - Pruebas para la creación de tickets en Jira
import unittest
from src.create_ticket import create_jira_ticket

class TestCreateTicket(unittest.TestCase):
    def test_create_jira_ticket(self):
        response = create_jira_ticket("Test Summary", "Test Description", "user1", "TEST", "https://jira.example.com", ("user", "pass"))
        self.assertIn("id", response)

if __name__ == "__main__":
    unittest.main()
