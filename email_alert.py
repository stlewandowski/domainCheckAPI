from configparser import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import base64


class EmailAction:
    """Class to send an email alert of new results."""

    def __init__(self, domain, domain_response):
        """Initialize class and set variables."""
        config = ConfigParser()
        config.read("conf.ini")
        self.e_from = config["email"]["from"]
        self.e_to = config["email"]["to"]
        self.e_domain = config["email"]["domain"]
        self.e_port = config["email"]["port"]
        self.e_pw = config["email"]["pw"]
        self.domain = domain
        self.domain_response = domain_response

    def send_alert(self):
        """Construct email message and send."""
        message = MIMEMultipart()
        e_from = self.e_from
        e_to = self.e_to
        self.e_pw = self.e_pw[2:-1]
        password = base64.b64decode(self.e_pw)
        password = str(password, "utf-8")
        message["From"] = e_from
        message["To"] = e_to
        message["Subject"] = f"Domain {self.domain} has been registered!"
        body = f"Domain {self.domain} has been registered!\n\n{self.domain_response}"
        message.attach(MIMEText(body, "plain"))
        # payload = MIMEBase("application", "octet-stream")
        # encoders.encode_base64(payload)
        # message.attach(payload)
        send = smtplib.SMTP(self.e_domain, self.e_port)
        send.starttls()
        send.login(e_from, password)
        text = message.as_string()
        send.sendmail(e_from, e_to, text)
        send.quit()


if __name__ == "__main__":
    a = EmailAction("example.com", "example registration response")
    a.send_alert()
