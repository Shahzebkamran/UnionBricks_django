

from django.urls import path, include
from .views import ArchitectViewSet, DesignPaymentViewSet, DesignViewSet, ItemViewSet, MeetingPaymentViewSet, MeetingViewSet, OrderPaymentViewSet, OrderViewSet, ProjectViewSet, UserCartApi, UserViewSet
from rest_framework.routers import DefaultRouter
from api.auth import CustomObtainAuthToken
# article_list, article_details, ArticleList, ArticleDetails

router = DefaultRouter()
# router.register('articles', ArticleViewSet, basename='articles')
router.register('users', UserViewSet, basename='users')
router.register('architects', ArchitectViewSet, basename='architects')
router.register('items', ItemViewSet, basename='items')
router.register('meetings', MeetingViewSet, basename='meetings')
router.register('meetingspayment', MeetingPaymentViewSet,
                basename='meetingspayment')
router.register('projects', ProjectViewSet, basename='projects')
router.register('designs', DesignViewSet, basename='designs')
router.register('designspayment', DesignPaymentViewSet,
                basename='designspayment')
router.register('orderpayments', OrderPaymentViewSet, basename='orderpayments')
router.register('orders', OrderViewSet, basename='orders')
router.register('mycart', UserCartApi, basename='mycart')


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', CustomObtainAuthToken.as_view()),
    

    # path('api/mycart/<int:id>/', UserCartApi),
    # path('api/test/<int:id>/', UserRetrive),
    # path('articles/<int:id>/', ArticleDetails.as_view())
    # path('articles/', article_list),
    # path('articles/<int:pk>/', article_details),

]
