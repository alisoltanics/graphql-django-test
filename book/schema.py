import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from .models import Book

class CreateBook(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()

    class Arguments:
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()

        return CreateBook(
            id=book.id,
            title=book.title,
            description=book.description,
        )


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class Query(object):
    all_books = graphene.List(BookType)
    book = graphene.Field(
        BookType,
        id=graphene.Int(),
    )
    delete_book = graphene.Field(
        BookType,
        id=graphene.Int(),
    )

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, **kwargs):
        id = kwargs.get('id')
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You must login first!')
        
        if id:
            return Book.objects.get(pk=id)
    
    def resolve_delete_book(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            Book.objects.get(pk=id).delete()
            return None


