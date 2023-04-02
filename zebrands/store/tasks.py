from store.models import Product, ProductStats

from zebrands import celery_app


@celery_app.task
def product_change_notification(sku):
    pass


@celery_app.task
def product_update_counter(sku):
    product = Product.objects.get(sku=sku)
    if hasattr(product, "stats"):
        stat = product.stats
    else:
        stat = ProductStats(product=product)
    stat.view_count += 1
    stat.save()
