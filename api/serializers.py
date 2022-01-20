from rest_framework import serializers
from .models import Cart, Design, Meeting, Order, OrderPayment, DesignPayment, Project, User, Item, Architect
from rest_framework.authtoken.views import Token


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'price', 'stock']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name','display_picture']

        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     Token.objects.create(user=user)
    #     return user


class ArchitectSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Architect
        fields = UserSerializer.Meta.fields + ['experience', 'education']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_id', 'id', 'date_placed', 'ship_date', 'address',
                  'status', 'items']


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'time', 'title', 'client_id',
                  'client_name', 'status', 'fee']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'date', 'items']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'description', 'title', 'client_id',
                  'client_name', 'percentage', 'cost', 'start_date', 'comp_date']


class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = ['id', 'client_id',
                  'client_name', 'arch_id', 'cost', 'img', 'status', 'description']


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order_id', 'method', 'amount',
                  'status', 'date']


class DesignPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignPayment
        fields = ['id', 'design_id', 'amount',
                  'status', 'date']


class MeetingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignPayment
        fields = ['id', 'meeting_id', 'amount',
                  'status', 'date']
