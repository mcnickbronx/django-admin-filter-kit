import re

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from admin_filter_kit.apps import check_app_order
from tests.models import Author, Book, Review, Tag


class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser("admin", "admin@example.com", "password")
        cls.tolstoy = Author.objects.create(name="Leo Tolstoy")
        cls.chekhov = Author.objects.create(name="Anton Chekhov")
        cls.war = Book.objects.create(title="War and Peace", author=cls.tolstoy)
        cls.steppe = Book.objects.create(title="The Steppe", author=cls.chekhov)
        cls.novel = Tag.objects.create(name="novel")
        cls.war.tags.add(cls.novel)

    def setUp(self):
        self.client.force_login(self.user)

    def get_books(self, **params):
        return self.client.get(reverse("admin:tests_book_changelist"), params)


class AutocompleteFilterTests(AdminTestCase):
    def test_related_objects_are_not_loaded_into_the_page(self):
        response = self.get_books()
        self.assertContains(response, 'data-field-name="author"')
        self.assertContains(response, 'data-field-name="tags"')
        self.assertNotContains(response, "Leo Tolstoy")
        self.assertNotContains(response, "novel")

    def test_list_is_filtered_and_only_the_selected_object_is_shown(self):
        response = self.get_books(author__id__exact=self.tolstoy.pk)
        self.assertEqual(list(response.context["cl"].result_list), [self.war])
        self.assertContains(response, f'<option value="{self.tolstoy.pk}" selected>Leo Tolstoy</option>', html=True)
        self.assertNotContains(response, "Anton Chekhov")

    def test_many_to_many(self):
        response = self.get_books(tags__id__exact=self.novel.pk)
        self.assertEqual(list(response.context["cl"].result_list), [self.war])

    def test_filter_across_a_relation(self):
        review = Review.objects.create(book=self.war, text="Long")
        Review.objects.create(book=self.steppe, text="Short")
        response = self.client.get(reverse("admin:tests_review_changelist"), {"book__author__id__exact": self.tolstoy.pk})
        self.assertEqual(list(response.context["cl"].result_list), [review])
        self.assertContains(response, 'data-model-name="book" data-field-name="author"')

    def test_list_address_without_the_filter_keeps_the_others(self):
        response = self.get_books(author__id__exact=self.tolstoy.pk, tags__id__exact=self.novel.pk)
        query_string = re.search(r'data-query-string="([^"]*)" data-lookup="author__id__exact"', response.content.decode())[1]
        self.assertEqual(query_string, f"?tags__id__exact={self.novel.pk}")

    def test_scripts_load_in_order(self):
        # Select2 registers itself on the global jQuery, which jquery.init.js removes;
        # the filter script needs django.jQuery from jquery.init.js
        content = self.get_books().content.decode()
        for script_list in [
            ["vendor/jquery/jquery", "select2/select2.full", "admin/js/jquery.init.js", "admin/js/autocomplete.js"],
            ["admin/js/jquery.init.js", "admin_filter_kit/autocomplete_filter.js"],
        ]:
            position_list = [content.index(script) for script in script_list]
            self.assertEqual(position_list, sorted(position_list), script_list)
        self.assertEqual(content.count("select2/select2.full"), 1)

    def test_autocomplete_view_accepts_the_widget_parameters(self):
        params = {"app_label": "tests", "model_name": "book", "field_name": "author", "term": "tol"}
        response = self.client.get(reverse("admin:autocomplete"), params)
        self.assertEqual([result["text"] for result in response.json()["results"]], ["Leo Tolstoy"])


class CollapseTests(AdminTestCase):
    def test_sidebar_is_collapsible_by_default(self):
        response = self.client.get(reverse("admin:tests_author_changelist"))
        self.assertContains(response, "admin_filter_kit/collapse.js")
        self.assertNotContains(response, "select2")

    @override_settings(ADMIN_FILTER_KIT_COLLAPSIBLE=False)
    def test_collapse_can_be_turned_off(self):
        response = self.get_books()
        self.assertNotContains(response, "admin_filter_kit/collapse.js")
        self.assertContains(response, "admin_filter_kit/autocomplete_filter.js")


class AppOrderCheckTests(SimpleTestCase):
    def test_no_warning_when_listed_before_admin(self):
        self.assertEqual(check_app_order(None), [])

    @override_settings(INSTALLED_APPS=["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "admin_filter_kit"])
    def test_warning_when_listed_after_admin(self):
        self.assertEqual([warning.id for warning in check_app_order(None)], ["admin_filter_kit.W001"])
