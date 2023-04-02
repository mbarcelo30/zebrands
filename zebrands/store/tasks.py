from zebrands import celery_app


@celery_app.task(bind=True)
def product_change_notification(self):
    pass


@celery_app.task(bind=True)
def product_update_counter(self):
    pass
