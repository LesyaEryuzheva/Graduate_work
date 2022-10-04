from rest_framework import routers

from .views import (StatisticsReceiptViewSet, StatisticsTransactionViewSet, StatisticsViewSet,
                    ExportTransactionsToExcelViewSet,
                    ExportReceiptToExcelViewSet)

app_name = 'reportings'

router = routers.DefaultRouter()


router.register('Statistics',
                StatisticsViewSet,
                basename='Statistics')
router.register('StatisticsReceipt',
                StatisticsReceiptViewSet,
                basename='StatisticsReceipt')
router.register('StatisticsTransaction',
                StatisticsTransactionViewSet,
                basename='StatisticsTransaction')

router.register('export_receipts_to_excel',
                ExportReceiptToExcelViewSet,
                basename='export_receipts_to_excel')
router.register('export_transactions_to_excel',
                ExportTransactionsToExcelViewSet,
                basename='export_transactions_to_excel')

urlpatterns = router.urls
