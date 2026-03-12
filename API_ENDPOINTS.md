# API Endpoints Documentation

## Swagger Documentation

Интерактивная документация API доступна через Swagger UI:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **JSON Schema**: `http://localhost:8000/swagger.json`
- **YAML Schema**: `http://localhost:8000/swagger.yaml`

## Base URL
`/api/`

## Main Endpoints

### Главная страница
- `GET /api/main-page/` - Получить главную страницу
- `GET /api/main-page/{id}/` - Детали главной страницы

### Новости и события
- `GET /api/news/` - Список новостей
- `GET /api/news/{id}/` - Детали новости
- `GET /api/news/events/` - Все события
- `GET /api/news/pinned/` - Закрепленные новости
- `GET /api/news-photos/` - Фото новостей
- `GET /api/announcements/` - Объявления
- `GET /api/announcements/pinned/` - Закрепленные объявления

### Образование
- `GET /api/education-programs/` - Образовательные программы
- `GET /api/education-directions/` - Направления образования

### Библиотека
- `GET /api/library-categories/` - Категории библиотеки
- `GET /api/library-resources/` - Ресурсы библиотеки

### Контакты
- `GET /api/contacts/` - Контакты
- `GET /api/contact-departments/` - Отделы контактов
- `GET /api/social-links/` - Социальные сети

### Об академии
- `GET /api/about-academy/` - Об академии
- `GET /api/partners/` - Партнеры
- `GET /api/academy-charter/` - Устав академии
- `GET /api/academy-history/` - История академии
- `GET /api/academy-logo/` - Логотип академии
- `GET /api/organizational-structure/` - Организационная структура
- `GET /api/departments/` - Департаменты
- `GET /api/academic-council/` - Ученый совет
- `GET /api/academic-council-files/` - Файлы ученого совета
- `GET /api/trade-union/` - Профсоюзный комитет
- `GET /api/quality-management/` - Система менеджмента качества
- `GET /api/quality-management-files/` - Файлы системы качества
- `GET /api/bulletin/` - Вестник АГУПКР
- `GET /api/bulletin-files/` - Файлы вестника
- `GET /api/budget-programs/` - Проект бюджетных программ
- `GET /api/honorary-professors/` - Почетные профессора
- `GET /api/international-cooperation/` - Международное сотрудничество
- `GET /api/international-cooperation-links/` - Ссылки сотрудничества
- `GET /api/academic-honesty/` - Академическая честность
- `GET /api/legal-documents/` - Нормативно-правовые акты

### Расписание
- `GET /api/schedules/` - Расписания
- `GET /api/surveys/` - Анкетирование

## Фильтрация и поиск

### Новости
- `?is_pinned=true` - Закрепленные новости
- `?is_event=true` - События
- `?search=текст` - Поиск по заголовку и описанию
- `?ordering=-date` - Сортировка по дате

### Образовательные программы
- `?program_type=bachelor` - Фильтр по типу программы
- `?search=текст` - Поиск

### Библиотека
- `?category={id}` - Фильтр по категории

### Нормативно-правовые акты
- `?document_type=external` - Внешние документы
- `?document_type=internal` - Внутренние документы

## Пагинация
Все списки используют пагинацию (20 элементов на страницу):
- `?page=1` - Номер страницы

## Админ-панель
Доступна по адресу: `/admin/`
Использует Jazzmin для красивого интерфейса.

## Документация API
- Swagger UI: `/swagger/` - Интерактивная документация с возможностью тестирования API
- ReDoc: `/redoc/` - Альтернативный стиль документации
- JSON Schema: `/swagger.json` - Схема API в формате JSON
- YAML Schema: `/swagger.yaml` - Схема API в формате YAML

