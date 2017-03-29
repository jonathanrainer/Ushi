import unittest
import random
import string
import os

from pathlib import Path

from ushi import Ushi


class UshiUnitTests(unittest.TestCase):

    pdf_directory = os.path.join("..", "pdfs")

    def setUp(self):
        random.seed(a=3000)
        self.user_ids = [
            "{0}{1}".format(
                ''.join(random.choice(string.ascii_lowercase)
                        for _ in range(random.randint(2, 4))),
                random.randint(100, 9999)
            ) for _ in range(0, 10)
        ]
        for user_id in self.user_ids:
            self.create_pdf_file(user_id)
        self.ushi = Ushi()

    def tearDown(self):
        for pdf in os.listdir(self.pdf_directory):
            if pdf[0] != '.':
                os.remove(os.path.join(self.pdf_directory, pdf))

    def create_pdf_file(self, name):
        name += ".pdf"
        Path(os.path.join(self.pdf_directory, name)).touch()

    def test_get_pdf_file_list_returns_correct_list(self):
        self.create_pdf_file("my_holiday_photos")
        self.create_pdf_file("some_other_file")
        self.create_pdf_file("jonathan_rainer")
        pdf_list = self.ushi.get_pdf_file_list(self.pdf_directory)
        self.assertEqual(10, len(pdf_list))

    def test_get_message_text(self):
        message = "Hi\nThis is certainly a message.\nFrom\nJonathan"
        with open("test.txt", "w") as text_file:
            text_file.write(message)
        message_text = self.ushi.get_message_text("test.txt")
        self.assertEqual(message_text, message)
        os.remove("test.txt")

    def test_get_credentials(self):
        credentials = self.ushi.get_credentials("..")
        self.assertIsNotNone(credentials)

if __name__ == '__main__':
    unittest.main()
