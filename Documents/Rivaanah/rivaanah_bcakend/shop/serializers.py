from rest_framework import serializers
from .models import Product, CartItem, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user']


class StatisticsSerializer(serializers.Serializer):
    user_cout = serializers.IntegerField()
    products_cout = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)