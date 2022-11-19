from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 


message = Mail(
    from_email="plasmadonorbank@gmail.com",
    to_emails="arun1751121@gmail.com",
    subject='Plasma Donor',
    html_content='<p>Hello, Your Registration was successfull. <br><br> Thank you for choosing us.</p>')

sg = SendGridAPIClient(
    api_key='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')

response = sg.send(message)
print(response.status_code, response.body)