# 📂 tests/test_telegram_bot.py - Pruebas para el bot de Telegram
import unittest
from telegram.ext import Updater

class TestTelegramBot(unittest.TestCase):
    def test_bot_initialization(self):
        bot = Updater("TEST_TOKEN", use_context=True)
        self.assertIsNotNone(bot)

if __name__ == "__main__":
    unittest.main()
