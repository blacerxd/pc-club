# Техническое задание: сайт ПК-клуба

Стек: Django + DRF (backend/API), React (frontend), PostgreSQL (БД).

---

## 1. Django apps

| App | Зона ответственности |
|---|---|
| `users` | Пользователи, роли, профиль, аутентификация (JWT) |
| `clubs` | Клубы, зоны, места (workstations), железо |
| `catalog` | Каталог игр и привязка игр к местам |
| `bookings` | Бронирования, статусы, история изменений, live-загруженность зала, лист ожидания |
| `menu` | Меню кафе клуба (категории, позиции) |
| `orders` | Заказы еды |
| `loyalty` | Бонусная система, транзакции, правила начисления |
| `tournaments` | Турниры, команды, участники, матчи/сетка |
| `promotions` | Акции и промокоды |
| `analytics` | Статистика активности (агрегации + трекинг сессий по играм) |
| `notifications` | Email/push/telegram/push-уведомления (напоминание о брони, статус заказа, освобождение места из очереди) |
| `core` | Общие абстракции (TimeStampedModel), права доступа, утилиты |

Рекомендация по разделению между тремя участниками:
- **Backend/бронирования и клубы**: `clubs`, `bookings`, `catalog`, `core`
- **Backend/коммерция и вовлечение**: `menu`, `orders`, `loyalty`, `promotions`, `tournaments`
- **Frontend + DevOps + `users`/`analytics`/`notifications`**: auth, ЛК, админка, карта, деплой

Постройте OpenAPI/Swagger-схему API в первые 2 недели — тогда фронт и бэк смогут работать параллельно.

---

## 2. Сущности и атрибуты (схема БД)

### users
**User** (кастомная модель, наследует `AbstractUser`)
- id, username / phone (уникальный, вход по номеру)
- email, password
- first_name, last_name
- phone_number
- avatar
- role: `client` / `staff` / `admin`
- home_club (FK → Club, nullable)
- is_active, is_verified
- date_joined, last_login

**StaffProfile**
- user (OneToOne)
- club (FK)
- position (администратор зала / менеджер / и т.д.)
- hired_at

### clubs
**Club**
- id, name, slug
- address, city
- latitude, longitude
- phone, email, description
- logo, photos (галерея)
- is_active, created_at

**WorkingHours** (расписание по дням недели, если клубы работают не 24/7)
- club (FK), weekday, open_time, close_time, is_day_off

**Zone**
- id, club (FK)
- name
- zone_type: `standard` / `vip` / `ps5` / `bootcamp`
- description
- price_per_hour
- capacity
- icon/color (для отображения на схеме зала)

**HardwareProfile** (конфигурация железа, переиспользуется на нескольких местах)
- id, name (например, "Топовая станция")
- cpu, gpu, ram, storage
- monitor, monitor_refresh_rate
- peripherals (мышь/клавиатура/гарнитура — можно текстом или отдельной M2M-моделью Peripheral)

**Workstation** (место/ПК/консоль)
- id, zone (FK)
- number/label (например, "PC-12")
- device_type: `pc` / `ps5` / `xbox`
- hardware_profile (FK → HardwareProfile)
- status: `free` / `occupied` / `reserved` / `maintenance`
- position_x, position_y (координаты на схеме зала, опционально)

### catalog
**Game**
- id, title, slug
- genre (тег/M2M)
- cover_image, description
- platform: `pc` / `ps5` / `xbox` / `multi`
- min_requirements (опционально)

**WorkstationGame** (M2M через промежуточную таблицу)
- workstation (FK), game (FK), installed_at

### bookings
**Booking**
- id, user (FK)
- workstation (FK)
- club (денормализовано для быстрых выборок)
- start_time, end_time
- actual_start, actual_end (факт заезда/выезда — нужно для статистики в ЛК)
- status: `pending` / `confirmed` / `active` / `completed` / `cancelled` / `no_show`
- participants_count (для групповых броней bootcamp-зоны)
- price
- comment
- created_by (сам пользователь или сотрудник — для админского добавления/изменения брони)
- created_at, updated_at

**BookingStatusLog** (история изменений — нужна для админ-панели)
- booking (FK)
- old_status, new_status
- changed_by (FK User)
- comment, changed_at

**Waitlist** (лист ожидания — если зал забит, встать в очередь на зону/тип места)
- id, user (FK)
- club (FK)
- zone (FK, nullable — если ждёт конкретную зону) / device_type (nullable — если ждёт любую консоль/ПК определённого типа)
- desired_start, desired_duration (желаемое время и длительность сессии)
- status: `waiting` / `notified` / `booked` / `expired` / `cancelled`
- notified_at (когда ушло уведомление об освобождении)
- expires_at (сколько времени даётся на подтверждение после уведомления, иначе место уходит следующему)
- created_at

> **Live-карта загруженности** отдельной таблицы не требует: это read-only API-эндпоинт, агрегирующий текущий `status` всех `Workstation` по зонам (`свободно/занято/на обслуживании` в разрезе `Zone`). Данные те же, что для карты бронирования — просто отдаются в облегчённом виде без деталей конкретной брони.

### menu
**MenuCategory**
- id, club (FK, nullable если меню общее для всех клубов)
- name, order, image

**MenuItem**
- id, category (FK)
- name, description, price, image
- is_available
- calories/weight (опционально)

### orders
**Order**
- id, user (FK)
- booking (FK, nullable — привязка заказа к текущей игровой сессии)
- club (FK)
- status: `new` / `accepted` / `cooking` / `delivered` / `cancelled`
- total_price
- payment_method: `bonus` / `cash` / `card`
- comment
- created_at, delivered_at

**OrderItem**
- order (FK), menu_item (FK)
- quantity
- price_at_order (фиксация цены на момент заказа)

### loyalty
**LoyaltyAccount**
- user (OneToOne)
- balance
- tier: `bronze` / `silver` / `gold` (опционально)
- total_earned, total_spent
- updated_at

**LoyaltyTransaction**
- account (FK)
- amount (может быть отрицательным)
- type: `earn_booking` / `earn_order` / `spend` / `manual_admin` / `referral`
- related_booking (FK, nullable), related_order (FK, nullable)
- created_by (FK User — для ручных начислений сотрудником)
- comment, created_at

**LoyaltyRule** (чтобы админ мог настраивать начисление без деплоя кода)
- action_type: `booking` / `order`
- points_per_unit (например, 1 балл за каждые 10 ₽)
- is_active

### tournaments
**Tournament**
- id, club (FK, nullable — общий/онлайн турнир)
- title, slug, game (FK)
- description, banner
- format: `single_elimination` / `double_elimination` / `round_robin` / `swiss`
- team_size (1 = соло)
- max_participants
- registration_start, registration_end
- start_date, end_date
- prize_pool
- status: `draft` / `registration_open` / `ongoing` / `finished` / `cancelled`
- created_by (FK User)

**Team**
- name, logo, captain (FK User)

**TeamMember**
- team (FK), user (FK), role: `captain` / `member`, joined_at

**TournamentParticipant**
- tournament (FK)
- user (FK, nullable если участвует команда)
- team (FK, nullable если участвует соло)
- registered_at
- status: `registered` / `checked_in` / `eliminated` / `winner` / `disqualified`
- seed (позиция в сетке)

**Match**
- tournament (FK), round_number
- participant1, participant2 (FK → TournamentParticipant, participant2 nullable для bye)
- winner (FK, nullable)
- score, scheduled_at
- status: `scheduled` / `ongoing` / `finished`

### promotions
**Promotion**
- club (FK, nullable = все клубы)
- title, description, banner
- discount_type: `percent` / `fixed_amount` / `bonus_multiplier` / `free_hour`
- value
- applicable_zone (FK → Zone, nullable)
- promo_code (опционально)
- start_date, end_date, is_active
- created_by (FK User)

### analytics
**SessionGameActivity** (для "в какие игры играет пользователь" — требует агента на ПК, репортящего активный процесс; см. раздел "Открытые вопросы")
- booking (FK)
- game (FK, nullable если процесс не распознан)
- started_at, ended_at

Остальная статистика ЛК (средняя длительность сессии, частота бронирований, дата последнего визита, любимая зона) — это **агрегирующие запросы** к `Booking` (Django `annotate`/`aggregate`), отдельные таблицы для них не нужны.

### core
- `TimeStampedModel` (abstract): created_at, updated_at — наследуют большинство моделей
- `City` (id, name) — если клубов несколько городов, для фильтра на карте

---

## 3. Задачи по модулям

### Этап 0 — Проектирование (недели 1–2)
- [ ] ER-диаграмма БД целиком, ревью всей командой
- [ ] Разбивка API по ресурсам, черновик OpenAPI/Swagger-схемы
- [ ] Wireframes ключевых экранов (главная, карта, бронирование, ЛК, админка)
- [ ] Настройка репозитория: монорепо или два репо, git-flow, CI (lint + тесты на пуш)
- [ ] Скелет Django-проекта (apps выше), скелет React-приложения (роутинг, стейт-менеджер, API-клиент)
- [ ] Docker-compose для локальной разработки (Django + Postgres + Redis)

### Модуль users / auth (недели 2–3)
- [ ] Кастомная модель User, регистрация/вход (JWT, refresh-токены)
- [ ] Вход по телефону + SMS-код (или email, если проще для MVP)
- [ ] Профиль пользователя (редактирование, аватар)
- [ ] Роли и права доступа (client / staff / admin), permission-классы DRF
- [ ] Восстановление пароля

### Модуль clubs (недели 2–4)
- [ ] CRUD клубов, зон, мест, hardware-профилей (через админку/API для сотрудников)
- [ ] API получения списка мест с фильтром по зоне/статусу/клубу
- [ ] Отображение установленных игр и характеристик железа на карточке места
- [ ] Схема зала (визуальная раскладка мест по зонам) — фронт

### Модуль карты клубов (недели 3–4)
- [ ] Интеграция с картами (Яндекс.Карты API или 2GIS API — учитывая российский контекст)
- [ ] Геолокация пользователя, сортировка клубов по расстоянию
- [ ] Фильтры на карте (город, наличие VIP/PS5/bootcamp, сейчас открыт)

### Модуль bookings (недели 4–7) — ядро проекта
- [ ] Модель доступности (проверка пересечения броней на уровне БД — уникальный индекс/constraint или блокировка при записи)
- [ ] API создания/отмены/переноса брони
- [ ] Календарь/таймлайн бронирования на фронте (выбор даты, времени, места)
- [ ] Групповая бронь для bootcamp-зоны (несколько мест разом)
- [ ] Уведомления о статусе брони (см. `notifications`)
- [ ] Логика авто-отмены неподтверждённых броней (Celery beat)
- [ ] Real-time статус занятости мест (WebSocket/Channels или поллинг) — чтобы карта зала обновлялась без перезагрузки
- [ ] **Live-карта загруженности зала**: публичный API-эндпоинт с агрегированным количеством свободных/занятых мест по зонам (без деталей брони), виджет на главной/странице клуба, обновление через тот же WebSocket-канал, что и карта зала
- [ ] **Лист ожидания (Waitlist)**: API постановки в очередь, когда все места нужной зоны заняты; фоновая задача (Celery/сигнал при смене статуса Workstation на `free`), которая находит первого в очереди и шлёт уведомление; таймер на подтверждение (`expires_at`), при истечении — уведомление следующему в очереди; экран "моя очередь" в ЛК с позицией и примерным временем ожидания

### Модуль меню и заказов (недели 6–8)
- [ ] CRUD меню (категории, позиции) в админке
- [ ] Оформление заказа из ЛК/во время активной сессии
- [ ] Статусы заказа и их смена сотрудником (кухня/бар)
- [ ] Уведомление пользователя о готовности заказа

### Модуль бонусной системы (недели 7–8)
- [ ] Начисление баллов при завершении брони/заказа (сигналы Django или Celery-таск)
- [ ] Списание баллов при оплате
- [ ] Настраиваемые правила начисления (LoyaltyRule) в админке
- [ ] История транзакций в ЛК

### Модуль турниров (недели 8–10)
- [ ] CRUD турниров и регистрация участников/команд
- [ ] Генерация сетки (single elimination — самое простое для старта)
- [ ] Обновление результатов матчей сотрудником, автопродвижение победителя по сетке
- [ ] Публичная страница турнира с live-сеткой

### Модуль акций (неделя 9)
- [ ] CRUD акций/промокодов в админке
- [ ] Применение промокода к брони/заказу, отображение активных акций на главной

### Модуль статистики в ЛК (недели 9–10)
- [ ] Агрегация: любимые игры, средняя длительность сессии, частота визитов, последний визит
- [ ] Графики на фронте (recharts/d3): активность по неделям/месяцам
- [ ] (опционально, если останется время) сбор SessionGameActivity — см. открытые вопросы ниже

### Админ-панель (сквозной модуль, недели 4–11)
Отдельный React-роут с доступом только для staff/admin, либо кастомизация Django Admin (быстрее для MVP, но менее гибко для нетехнического персонала).
- [ ] Управление местами/железом/зонами (добавление, редактирование, статус "на обслуживании")
- [ ] Управление бронированиями: список, ручное создание/отмена/перенос, история изменений
- [ ] Управление пользователями: поиск, блокировка, ручная корректировка баланса бонусов
- [ ] Управление акциями и турнирами
- [ ] Дашборд с ключевыми метриками (загрузка залов, выручка, топ игр)

### DevOps и качество (сквозные, весь проект)
- [ ] Тесты: pytest-django для API, React Testing Library для ключевых компонентов
- [ ] Деплой: Docker + docker-compose, nginx, CI/CD (GitHub Actions)
- [ ] Логирование и мониторинг ошибок (Sentry — есть бесплатный тариф)
- [ ] Резервное копирование БД

### Финал (недели 11–12)
- [ ] Нагрузочная проверка сценария бронирования (race condition при параллельной записи на одно место — обязательно протестировать)
- [ ] Полировка UI/UX, адаптивная вёрстка
- [ ] Документация (README, схема архитектуры, инструкция для админов)
- [ ] Подготовка демо-сценария для защиты

---

## Открытые вопросы, которые стоит решить в начале

1. **Как получать данные о железе/играх на ПК** — вручную через админку (проще, реалистичнее для 3 месяцев) или через агент на клиентском ПК, который сам репортит конфигурацию и активный процесс (сложнее, даёт "живую" статистику игр, но это отдельный небольшой сервис вне Django/React стека).
2. **Оплата** — реальная интеграция с платёжным шлюзом или тестовый режим/только бонусами для MVP.
3. **SMS-провайдер** для входа по телефону — нужен аккаунт у сервиса (SMS.ru, SMSC и т.п.), стоит заложить время на интеграцию.
