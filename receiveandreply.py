import time
import email
import imaplib
import smtplib
from email.mime.text import MIMEText

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()

def start_email_service():
    imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
    imap_ssl_port = 993
    username = 'aaaa@gmail.com'
    password = 'abcd'
    uid_max = 0
    
    
    
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')

    result, data = server.uid('search', None, "unseen")

    uids = [int(s) for s in data[0].split()]
    if uids:
        uid_max = max(uids)
        # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

    server.logout()


    # Keep checking messages ...
    print("Email service started...")
    while 1:
        # Have to login/logout each time because that's the only way to get fresh results.
        server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
        server.login(username, password)
        server.select('INBOX')

        result, data = server.uid('search', None, "unseen")

        uids = [int(s) for s in data[0].split()]

        for uid in uids:
            # Have to check again because Gmail sometimes does not obey UID criterion.
            if uid > uid_max:
                result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
                msg = email.message_from_string(data[0][1].decode("utf-8"))
                
                uid_max = uid
            
                text = get_first_text_block(msg)

                smtp_ssl_host = 'smtp.gmail.com'
                smtp_ssl_port = 465
                username = 'aaaa@gmail.com'
                password = 'abcd'
                sender = 'aaaa@gmail.com'
                targets = [msg['From']]

                msg1 = MIMEText('Hi, Weijie is busy now, he will contact you X mins later.')
                msg1['Subject'] = 'Hello'
                msg1['From'] = sender
                msg1['To'] = ', '.join(targets)

                server1 = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
                server1.login(username, password)
                server1.sendmail(sender, targets, msg1.as_string())
                server1.quit()


                print('A new message')
                print("From :"+ (email.utils.parseaddr(msg['From']))[1])
                print("Subject:"+ str(msg['Subject']))
                print("Content:"+ str(text))




#        print('Start: %s' % time.ctime())
        server.logout()
        time.sleep(10)
#        print('End: %s' % time.ctime())
