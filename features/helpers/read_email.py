import imaplib
import email
from email.header import decode_header


class ReadEmail:

    def __init__(self, host, emailaddress, password, emailstofetch):
        self.host = host
        self.emailid = emailaddress
        self.password = password
        self.noofemailstofetch = emailstofetch

    def reademailbody(self, containsemailsubject, containsbodytext):

        imap = imaplib.IMAP4_SSL(self.host)
        # authenticate
        imap.login(self.emailid, self.password)
        status, messages = imap.select("INBOX")

        # total number of emails
        messages = int(messages[0])
        actualmesasgestofetch = self.noofemailstofetch

        if messages >= 1:
            if messages <= actualmesasgestofetch:
                actualmesasgestofetch = messages
            for i in range(messages, messages - actualmesasgestofetch, -1):

                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):

                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode()
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)

                        if containsemailsubject not in subject:
                            continue
                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()

                        if content_type == "text/html":
                            if containsbodytext in body:
                                return body
        # close the connection and logout
        imap.close()
        imap.logout()
        return ""
