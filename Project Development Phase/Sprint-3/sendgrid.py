from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 


message = Mail(
    from_email="FROMMAIL",
    to_emails="TOMAIL",
    subject='Plasma Donor',
    html_content='<p>Hello, Your Registration was successfull. <br><br> Thank you for choosing us.</p>')

sg = SendGridAPIClient(
    api_key='SENDGRID_API_KEY')

response = sg.send(message)
print(response.status_code, response.body)
