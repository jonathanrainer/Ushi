import os
import httplib2
import re
import mimetypes
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from googleapiclient.errors import HttpError

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = '../credentials.json'
APPLICATION_NAME = 'Ushi'


class Ushi():

    def main(self, pdf_directory,
             message_text_file, from_email, message_subject, no_send_mode, working_directory):
        # Check and count the number of PDFs in the folder given
        print("Checking number of PDF files to send...")
        pdf_file_list = self.get_pdf_file_list(pdf_directory)
        try:
            assert pdf_file_list
        except AssertionError:
            print("ERROR: NO PDF FILES FOUND. EXITING...")
            return
        print("Number of PDF files to send: {0}".format(len(pdf_file_list)))
        # Check the existence of the message text and load it into the program
        print("Checking for existence of message text...")
        message_text = self.get_message_text(message_text_file)
        # Check that all the credentials exist for the Gmail API
        print("Connecting to GMail API...")
        service = self.initialise_api(working_directory)
        try:
            assert service
        except AssertionError:
            print("ERROR: NO API CONNECTION FOUND. EXITING...")
            return
        # Print list of people to send emails to
        print("Emails should be sent to: ")
        for pdf in pdf_file_list:
            print("\t{0}".format(pdf))
        # Send emails
        if not no_send_mode:
            print("Sending Emails")
            self.send_emails(pdf_directory, pdf_file_list, service, message_text, message_subject,
                             from_email)
        return

    @staticmethod
    def get_pdf_file_list(pdf_directory):
        return [file for file in os.listdir(pdf_directory)
                if file.endswith(".pdf") and (re.match("^[a-zA-Z]+[0-9]+", file)
                                              is not None)]

    @staticmethod
    def get_message_text(message_text_file):
        try:
            assert os.path.exists(message_text_file)
        except AssertionError:
            print("ERROR: NO MESSAGE TEXT FOUND. EXITING...")
        with open(message_text_file, 'r') as text_file:
            return text_file.read()

    def initialise_api(self, working_directory):
        credentials = self.get_credentials(working_directory)
        http = credentials.authorize(httplib2.Http())
        return discovery.build("gmail", 'v1', http=http)

    @staticmethod
    def get_credentials(working_directory):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = os.path.join(working_directory, "gmail_credentials.json")
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def send_emails(self, pdf_directory, pdf_file_list, service, message_text, message_subject,
                    from_email):
        email_address = {pdf: "{0}@york.ac.uk".format(os.path.splitext(pdf)[0]) for pdf in pdf_file_list}
        messages = []
        for user_id, email in email_address.items():
            messages.append((email, self.create_message(email, from_email, message_subject, message_text,
                                                os.path.join(pdf_directory, user_id))))
        for message in messages:
            try:
                result = (service.users().messages().send(userId="me", body=message[1]).execute())
                print('Message Id: {0} Sent To: {1}'.format(result['id'], message[0]))
            except HttpError as error:
                print('An error occurred: {0}'.format(error))

    @staticmethod
    def create_message(to, sender, subject, message_text, file):
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'application':
            fp = open(file, 'rb')
            msg = MIMEApplication(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}


if __name__ == "__main__":
    # TODO Argument parsing for pdf directory, message text file, no send mode
    ushi = Ushi()
    ushi.main("pdfs", "message.txt", "jr776@york.ac.uk",
              "MFCS Formative Test Results", False, ".")
