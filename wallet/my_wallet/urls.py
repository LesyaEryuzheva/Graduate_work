from rest_framework import routers

from .views import (AccountViewSet,
                    ReceiptViewSet,
                    TransactionViewSet,
                    TransferViewSet)

app_name = 'my_wallet'

router = routers.DefaultRouter()

router.register('account', AccountViewSet)
router.register('receipt', ReceiptViewSet)
router.register('transaction', TransactionViewSet)
router.register('transfer', TransferViewSet)

urlpatterns = router.urls
