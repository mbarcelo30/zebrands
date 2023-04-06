import logging

from django.conf import settings
from django.contrib.auth.models import Group

from rest_framework import status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from store.models import PRODUCT_ADMIN_GROUP, Product, ProductStats

from zebrands import celery_app

log = logging.getLogger()


def send_emails(sg, user, product):
    """
    Sends an email to the given user about the updated product.

    Constructs an email message with the updated product information and sends it to the user's email address.

    @param sg: (SendGridAPIClient) The SendGrid client to use for sending the email.
    @param user: The user to send the email to.
    @param product: The updated product.

    @return:
    - bool: True if the email was sent successfully, False otherwise.
    """
    kwargs = {
        "username": f"{user.first_name} {user.last_name}",
        "name": product.name,
        "brand": product.brand,
        "sku": product.sku,
    }
    message = Mail(
        from_email=(settings.SENDGRID_FROM_EMAIL, "Zebrands"), to_emails=user.email
    )
    message.dynamic_template_data = kwargs
    message.template_id = settings.PRODUCT_UPDATE_EMAIL_ID
    try:
        response = sg.send(message)
    except Exception as error:
        log.exception(error)
        return False

    if response.status_code == status.HTTP_202_ACCEPTED:
        log.info(f"Message successfully sent to {user.email}")
        return True
    else:
        message = (
            f"An error occurred while trying to send the message "
            f"to {user.email} \n "
            f"Response status: {response.status_code} \n"
            f"Response status: {response.status_code} \n"
            f"Response body: {response.body} \n"
            f"Response headers: {response.headers}"
        )
        log.warning(message)
        return False


@celery_app.task
def product_change_notification(sku):
    """
    Sends an email notification to all users in the 'Product Admin' group about a product update.

    Retrieves the product with the given SKU from the database, and sends an email notification to all users
    in the 'Product Admin' group with information about the updated product.

    @param sku: The SKU of the updated product.

    @return None
    """
    product = Product.objects.get(sku=sku)
    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    admins = Group.objects.get(name=PRODUCT_ADMIN_GROUP)
    users = admins.user_set.all()
    for user in users:
        send_emails(sg, user, product)


@celery_app.task
def product_update_counter(sku):
    """
    Updates the view count for a product.

    Retrieves the product with the given SKU from the database, and increments its view count by 1.
    If the product does not yet have a ProductStats object associated with it, one is created.

    @param sku: The SKU of the product to update.

    @return None
    """
    product = Product.objects.get(sku=sku)
    if hasattr(product, "stats"):
        stat = product.stats
    else:
        stat = ProductStats(product=product)
    stat.view_count += 1
    stat.save()
