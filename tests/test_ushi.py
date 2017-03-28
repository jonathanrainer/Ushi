import unittest
import random
import string
import os

from pathlib import Path

from ushi import Ushi


class UshiUnitTests(unittest.TestCase):

    pdf_directory = "../pdfs"

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

    def tearDown(self):
        for file in os.listdir(self.pdf_directory):
            if file[0] != '.':
                os.remove(os.path.join(self.pdf_directory, file))

    def create_pdf_file(self, name):
        name += ".pdf"
        Path(os.path.join(self.pdf_directory, name)).touch()

    def test_get_pdf_file_list_returns_correct_list(self):
        self.create_pdf_file("my_holiday_photos")
        self.create_pdf_file("some_other_file")
        self.create_pdf_file("jonathan_rainer")
        ushi = Ushi()
        pdf_list = ushi.get_pdf_file_list(self.pdf_directory)
        self.assertEqual(10, len(pdf_list))


if __name__ == '__main__':
    unittest.main()
