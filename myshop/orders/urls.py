from django.urls import path
from .views import ActiveOrdersView

urlpatterns = [
    path('active-orders/', ActiveOrdersView.as_view(), name='active-orders'),
]
