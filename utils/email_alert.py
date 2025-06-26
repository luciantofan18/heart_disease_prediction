from django.core.mail import send_mail

def send_alert_email(to_emails, subject, message):
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    send_mail(
        subject,
        message,
        None,  # DEFAULT_FROM_EMAIL
        to_emails,
        fail_silently=False
    )
