from django.contrib import admin

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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = [("book__author", AutocompleteFilter)]
