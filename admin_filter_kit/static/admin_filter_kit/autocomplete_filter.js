"use strict";
// Autocomplete filter: picking an object reloads the list filtered by it, clearing removes the filter.
{
    const $ = django.jQuery;

    $(document).on("change", ".filter-kit-autocomplete select", function () {
        const box = this.closest(".filter-kit-autocomplete");
        const params = new URLSearchParams(box.dataset.queryString);
        if (this.value) {
            params.set(box.dataset.lookup, this.value);
        }
        window.location.search = params.toString();
    });

    // Select2 4.0.13 with jQuery 3.6+ doesn't focus the search box on open: the first typed letter is lost
    $(document).on("select2:open", function () {
        const search = document.querySelector(".select2-container--open .select2-search__field");
        if (search) {
            search.focus();
        }
    });
}
