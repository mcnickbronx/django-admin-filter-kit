"use strict";
// Collapsible filter sidebar: a click on the "Filter" heading hides the filters and gives the table
// the full width. The browser remembers the state for all changelists.
{
    const KEY = "admin-filter-kit:collapsed";

    function isStoredCollapsed() {
        try {
            return localStorage.getItem(KEY) === "1";
        } catch {
            return false; // storage can be blocked: the sidebar just starts expanded
        }
    }

    function storeCollapsed(isCollapsed) {
        try {
            localStorage.setItem(KEY, isCollapsed ? "1" : "0");
        } catch {}
    }

    document.addEventListener("DOMContentLoaded", function () {
        const panel = document.getElementById("changelist-filter");
        const title = panel && panel.querySelector(":scope > h2");
        if (!title) {
            return;
        }
        title.setAttribute("role", "button");
        title.tabIndex = 0;

        function setCollapsed(isCollapsed) {
            panel.classList.toggle("filter-kit-collapsed", isCollapsed);
            title.setAttribute("aria-expanded", String(!isCollapsed));
        }

        function toggle() {
            const isCollapsed = !panel.classList.contains("filter-kit-collapsed");
            setCollapsed(isCollapsed);
            storeCollapsed(isCollapsed);
        }

        setCollapsed(isStoredCollapsed());
        title.addEventListener("click", toggle);
        title.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                toggle();
            }
        });
    });
}
