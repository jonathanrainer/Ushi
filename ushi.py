import os
import httplib2
import re

from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Test Client'

class Ushi():

    def main(self, pdf_directory,
             message_text_file, no_send_mode, working_directory):
        # Check and count the number of PDFs in the folder given
        print("Checking number of PDF files to output...")
        pdf_file_list = self.get_pdf_file_list(pdf_directory)
        # Check the existence of the message text and load it into the program
        # Check that all the credentials exist for the Gmail API
        service = self.initialise_api(working_directory)
        # Print list of people to send emails to
        # Send emails

    @staticmethod
    def get_pdf_file_list(pdf_directory):
        return [file for file in os.listdir(pdf_directory)
                if file.endswith(".pdf") and (re.match("[a-zA-Z]+[0-9]+", file)
                                              is not None)]

    def check_gmail_api_connection(self):
        return

    def initialise_api(self, working_directory):
        credentials = self.get_credentials(working_directory)
        http = credentials.authorize(httplib2.Http())
        return discovery.build("gmail", 'v1', http=http)

    def get_credentials(self, working_directory):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = os.path.join(self, working_directory,
                                       "credentials.json")
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

if __name__ == "__main__":
    # TODO Argument parsing for pdf directory, message text file, no send mode
    ushi = Ushi()
    ushi.main("~/Documents/Development/Python/Ushi/pdfs",
         "~/Documents/Development/Python/Ushi/message.txt",
         True, "~/Documents/Development/Python/Ushi/")