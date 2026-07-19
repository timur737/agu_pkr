# API Endpoints Documentation

## Swagger Documentation

Интерактивная документация API доступна через Swagger UI:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **JSON Schema**: `http://localhost:8000/swagger.json`
- **YAML Schema**: `http://localhost:8000/swagger.yaml`

## Base URL
`/api/`

## Основные endpoints новой CMS-структуры

### Страницы сайта
- `GET /api/pages/` — список активных страниц в порядке админ-панели.
- `GET /api/pages/{slug}/` — детальная страница с вложенными подстраницами и блоками.
- `POST /api/pages/` — создать страницу.
- `PUT/PATCH /api/pages/{slug}/` — обновить страницу.
- `DELETE /api/pages/{slug}/` — удалить страницу.

Фильтры и сортировка:
- `?group=home|about|abdrakhmanov|ideology|professional_development|education|science|international|contacts`
- `?parent={id}` — получить подстраницы конкретной главной страницы.
- `?is_development=true` — показать страницы в разработке.
- `?search=текст` — поиск по названию, описанию и slug.
- `?ordering=order` или `?ordering=-created_at`.

### Блоки страниц
- `GET /api/page-blocks/` — список активных блоков.
- `GET /api/page-blocks/{id}/` — детальный блок.
- `POST /api/page-blocks/` — создать блок.
- `PUT/PATCH /api/page-blocks/{id}/` — обновить блок.
- `DELETE /api/page-blocks/{id}/` — удалить блок.

Типы блоков:
- `text` — текст / description.
- `photo_text` — фото + description.
- `link` — ссылка под текстом или редирект.
  Для AVN/ЭОП заполняйте поле `url`; ссылки внутри `description` сохраняются как HTML из CKEditor и должны рендериться фронтендом.
- `pdf` — PDF файл, который фронтенд может скрывать под текстом.
- `number` — текстовое поле с цифрой.
- `social` — ссылка на социальную сеть.
- `slider` — слайд карусели с фото, датой и текстом.

Фильтры и сортировка:
- `?page_id={id}` — блоки конкретной страницы (`page` зарезервирован под пагинацию).
- `?block_type=text|photo_text|link|pdf|number|social|slider`.
- `?search=текст` — поиск по названию, описанию, ссылке и значению.
- `?ordering=order` или `?ordering=-created_at`.

## Админ-панель
Доступна по адресу: `/admin/`.
Авторизация, Django admin и Jazzmin-дизайн сохранены. Старые модели контента удалены из админ-панели и заменены двумя разделами:
- **01. Страницы сайта** — главные страницы, подстраницы и общие поля страницы.
- **02. Блоки страниц** — повторяемые блоки, файлы, ссылки, соцсети, цифры и слайды.

При применении миграций автоматически создается структура страниц в порядке из ТЗ, а подстраницы привязываются к соответствующим главным страницам.
