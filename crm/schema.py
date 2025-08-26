import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Order

# Define Object Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone", "created_at")

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "product", "quantity", "created_at")

# Define Queries
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(CustomerType, id=graphene.Int(required=True))
    recent_orders = graphene.List(OrderType, days=graphene.Int(default_value=30))

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_customer_by_id(self, info, id):
        return Customer.objects.get(id=id)

    def resolve_recent_orders(self, info, days):
        from django.utils import timezone
        from datetime import timedelta
        return Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=days))

# Create Schema
schema = graphene.Schema(query=Query)