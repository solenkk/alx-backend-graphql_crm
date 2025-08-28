import graphene
from . import schema  # Import your schema file

class Query(schema.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from graphene_django import DjangoObjectType
from django.db.models import F
from .models import Product  # Assuming you have a Product model

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock", "price")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        increment = graphene.Int(default_value=10)

    products = graphene.List(ProductType)
    message = graphene.String()
    updated_count = graphene.Int()

    @classmethod
    def mutate(cls, root, info, increment=10):
        try:
            # Get products with stock less than 10
            low_stock_products = Product.objects.filter(stock__lt=10)
            
            # Update their stock by incrementing
            updated_count = low_stock_products.update(stock=F('stock') + increment)
            
            # Get the updated products
            updated_products = Product.objects.filter(
                id__in=low_stock_products.values_list('id', flat=True)
            )
            
            return UpdateLowStockProducts(
                products=updated_products,
                message=f"Successfully updated {updated_count} low-stock products",
                updated_count=updated_count
            )
            
        except Exception as e:
            return UpdateLowStockProducts(
                products=[],
                message=f"Error updating low-stock products: {str(e)}",
                updated_count=0
            )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Add this to your existing schema if you have other mutations
# schema = graphene.Schema(mutation=Mutation, query=Query)
["UpdateLowStockProducts", "10", "from crm.models import Product"]