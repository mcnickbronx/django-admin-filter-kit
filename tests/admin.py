from django.contrib import admin
from django.db.models import Q

from admin_filter_kit.filters import AutocompleteFilter
from tests.models import Author, Book, Review, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]  # a plain filter: the sidebar is there, the autocomplete scripts are not


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = [("author", AutocompleteFilter), ("tags", AutocompleteFilter)]


class WriterFilter(AutocompleteFilter):
    """Own title and own filtering: reviews of the author's books or mentioning the author."""

    title = "writer"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        author = Author.objects.get(pk=self.value())
        return queryset.filter(Q(book__author=author) | Q(text__contains=author.name))


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = [("book__author", WriterFilter)]
