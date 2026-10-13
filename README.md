# django-admin-filter-kit

Русский · [English](https://github.com/mcnickbronx/django-admin-filter-kit/blob/main/README.en.md)

Небольшие дополнения к фильтрам списков в админке Django:

- **`AutocompleteFilter`** — фильтр по связанной записи с подсказками по мере набора. Для
  справочников, которые не помещаются в панель фильтров списком ссылок.
- **Сворачиваемая панель фильтров** — щелчок по заголовку «Фильтр» прячет фильтры, и таблица
  занимает всю ширину. Браузер запоминает выбор для всех списков. Включено по умолчанию.
- **Курсор сразу в поле поиска**, когда открываются подсказки. Select2 4.0.13, который идёт
  с Django, с jQuery 3.6+ фокус сам не ставит, и первая набранная буква теряется.

Зависимостей, кроме Django, нет. Поддерживаются Django 5.2, 6.0 и 6.1 на Python 3.10+.

## Установка

```
pip install django-admin-filter-kit
```

```python
INSTALLED_APPS = [
    "admin_filter_kit",  # выше django.contrib.admin
    "django.contrib.admin",
    # ...
]
```

Приложение должно стоять выше `django.contrib.admin`. Скрипты пакета подключает его собственный
шаблон `admin/change_list.html` — он расширяет шаблон Django, а Django берёт первый найденный.
Если порядок неверный, об этом предупредит проверка `admin_filter_kit.W001`.

## Фильтр с подсказками

```python
from django.contrib import admin

from admin_filter_kit.filters import AutocompleteFilter


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = [
        ("author", AutocompleteFilter),           # ForeignKey
        ("tags", AutocompleteFilter),             # ManyToManyField
        ("author__country", AutocompleteFilter),  # через связь
    ]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]  # обязательно: подсказки ищут по этим полям
```

Подсказки приходят из встроенного автокомплита админки — того же, что работает у
`autocomplete_fields`. Поэтому своих адресов у пакета нет, а правила те же:

- у админки связанной модели должны быть `search_fields`;
- подсказки видит тот, у кого есть право просмотра связанной модели; поиск и сортировка — как
  в её админке, учитывается `limit_choices_to` поля;
- подсказки подгружаются по 20 при наборе и прокрутке, подпись записи — `str(obj)`.

Страница списка не загружает справочник целиком — только выбранную запись, чтобы показать её
название. Выбор записи перезагружает список с фильтром, × снимает фильтр. Остальные фильтры,
поиск и сортировка сохраняются.

Пока не умеет: выбрать несколько записей сразу и отобрать записи без связи.

## Сворачиваемая панель

Работает во всех списках админки, где есть фильтры, — код писать не нужно. Выключить:

```python
ADMIN_FILTER_KIT_COLLAPSIBLE = False
```

## Свои шаблоны списка

Если в проекте переопределён `admin/change_list.html` или у `ModelAdmin` задан
`change_list_template`, этот шаблон должен расширять `"admin/change_list.html"` — как обычно
и делают. Иначе скрипты пакета на страницу не попадут, и фильтр с подсказками не заработает.

## Разработка

```
pip install -e .
python -m django test --settings=tests.settings
```

## Лицензия

MIT
