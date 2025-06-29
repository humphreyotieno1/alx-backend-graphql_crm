import graphene
from graphene.relay import Node
from .queries import Query as CRMQuery
from .mutations import Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    """Root query for the CRM application."""
    node = Node.Field()
    
    class Meta:
        description = "The root query type for the CRM application"


class Mutation(CRMMutation, graphene.ObjectType):
    """Root mutation for the CRM application."""
    class Meta:
        description = "The root mutation type for the CRM application"


# Create the schema with the Node interface
schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        # Add any custom types that need to be included in the schema
    ]
)
