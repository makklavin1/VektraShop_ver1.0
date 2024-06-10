from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, PurchaseHistory
from products.models import Product
from .serializers import UserProfileSerializer, UserStatsSerializer, PurchaseHistorySerializer, ProductSerializer
import logging
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserStatsView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatsSerializer
    permission_classes = [IsAuthenticated]

class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = request.data.get('cart_items', [])

        logger.info("Received cart items: %s", cart_items)  # Логирование данных корзины

        total_cost = 0
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['id'])
                total_cost += product.price * item['quantity']
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {item["id"]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if user.balance < total_cost:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the amount from user's balance
        user.balance -= total_cost
        user.save()

        # Create purchase history
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            try:
                PurchaseHistory.objects.create(user=user, product=product)
                logger.info("Created PurchaseHistory for user %s and product %s", user.username, product.name)
            except Exception as e:
                logger.error("Error creating PurchaseHistory: %s", e)
                return Response({'error': 'Error creating purchase history'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Purchase successful'}, status=status.HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.info("Login attempt for user: %s", request.data.get('username'))
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        if 'token' in response.data:
            token = Token.objects.get(key=response.data['token'])
            logger.info("Login successful for user: %s", token.user.username)
            return Response({'token': token.key, 'user_id': token.user_id, 'email': token.user.email})
        else:
            logger.error("Login failed for user: %s", request.data.get('username'))
            return Response(response.data, status=response.status_code)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
