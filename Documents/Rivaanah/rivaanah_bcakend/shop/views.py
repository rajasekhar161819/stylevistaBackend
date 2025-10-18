from rest_framework import viewsets, filters, status
from .models import Product, CartItem, Order
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, StatisticsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import User
from django.db.models import Sum

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'product_type']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=False, methods=['delete'], url_path='clear-cart')
    def by_resume(self, request):
        self.queryset.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'rivaanah-admin3304$':
            return self.queryset
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Stastics(viewsets.ModelViewSet):
    queryset = []
    def get_serializer_class(self):
        return StatisticsSerializer
    @action(detail=False, methods=["get"], url_path="get-statics")
    def get_statics(self, request):
        user_cout = User.objects.count()
        products_cout = Product.objects.count()
        total_orders = Order.objects.count()
        revenue = Order.objects.filter(status='delivered').aggregate(Sum('total_price'))['total_price__sum']
        if revenue is None:
            revenue = 0

        print("Raja.........")
        data = {'user_cout': user_cout,
                          'products_cout': products_cout,
                          'total_orders': total_orders,
                          'revenue': revenue
                          }
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)
         