from django.urls import path
from .views import UserProfileView, UserStatsView, CheckoutView,CustomAuthToken,UserOrdersView,link_telegram


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Добавьте этот маршрут
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('orders/', UserOrdersView.as_view(), name='user-orders'),
    path('link-telegram/', link_telegram, name='link-telegram'),
]
