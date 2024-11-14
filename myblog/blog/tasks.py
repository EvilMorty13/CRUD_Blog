# blog/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_post_creation_email(post_title, author_email):
    send_mail(
        'New Post Created',
        f'A new post titled "{post_title}" has been created.',
        'admin@myblog.com',
        [author_email],
        fail_silently=False,
    )
    

@shared_task
def send_comment_notification_email(post_title, comment_author, comment_content, post_author_email):
    send_mail(
        'New Comment on Your Post',  # Subject of the email
        f'A new comment has been posted on your post "{post_title}".\n\n'
        f'Comment by {comment_author}:\n'
        f'"{comment_content}"',  # Body of the email, includes comment details
        'admin@myblog.com',  # Sender's email address
        [post_author_email],  # Recipient's email address (the post author)
        fail_silently=False,  # Raise an exception if the email cannot be sent
    )
