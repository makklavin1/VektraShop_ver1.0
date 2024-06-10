from django.urls import path
from .views import UserProfileView, UserStatsView, CheckoutView,CustomAuthToken,ProductListView


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Добавьте этот маршрут
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product-list'),
]
