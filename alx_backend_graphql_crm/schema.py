import graphene
from graphene.relay import Node
from crm.schema.schema import schema as crm_schema


class Query(crm_schema.Query, graphene.ObjectType):
    """Root query that includes all other app queries."""
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    # Include the Node interface
    node = Node.Field()
    
    class Meta:
        description = "The root query type that includes all other app queries"


class Mutation(crm_schema.Mutation, graphene.ObjectType):
    """Root mutation that includes all other app mutations."""
    class Meta:
        description = "The root mutation type that includes all other app mutations"


# Create the schema with the Node interface
schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        # Add any additional types that need to be included in the schema
    ]
)
