import imapclient
import pandas as pd
import getpass

if __name__=="__main__":
    yourEmail = input()
    yourPassword = getpass.getpass()

    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapObj.login(yourEmail, yourPassword)
    imapObj.select_folder("[Gmail]/All Mail", readonly=True)
    UIDs = imapObj.search('(SINCE "01-jan-2000")')
    mails = []
    for msgid, data in imapObj.fetch(UIDs, ["ENVELOPE"]).items():
        envelope = data[b"ENVELOPE"]
        date = envelope.date
        if envelope.subject is not None:
            subject = envelope.subject.decode()
        else:
            subject = None
        mails.append((subject, date))
    mail_df = pd.DataFrame(mails)
    mail_df.columns = ["Subject", "Date"]
    mail_df["Date"] = pd.to_datetime(mail_df["Date"])
    mail_df = mail_df.set_index("Date")
    mail_df.to_csv("myEmails.csv", encoding='utf-8')
    print("A total of {} e-mails loaded.".format(len(mail_df)))
