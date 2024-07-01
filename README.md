# AW_website
---
## Инструкция по запуску
### Проект написан на **Django** с использованием **Python 3.11**. 
1. Распакуйте архив с проектом;
2. Откройте терминал и перейдите в рабочую папку проекта;
3. Убедитесь, что все фреймворки установлены и актуальны (___requirements.txt___ должен быть актуальный);
4. В корне проекта (папка, в которой лежит __manage.py__) выполните в терминале ```python manage.py runserver``` для запуска сервера (или что-то в это духе в зависимости от алиасов у вас в системе);
5. В браузере перейдите по ссылке: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
---
## Описание структуры
Все действующие страницы сайта указаны в header'е:
1. Главная (лэндинг);
2. Форма оформления заказа;
3. Страница FAQ и обратной связи;
4. Личный кабинет / авторизация.
Сайт также имеет страницы __logout.html_ и _policy.html_, содержащие 'welcome'-message при логауте и политику конфиденциальности соответственно.
---
## Дополнения
* В релизе есть заполненная база данных - можно посмотреть данные, которые там лежат;
* Роли распределяются через админ-панель Django ([http://127.0.0.1:8000/](http://127.0.0.1:8000/), для доступа нужно авторизоваться через суперюзера;
* Суперюзер имеет также права "сотрудника магазина" - он тоже может смотреть все заказы в системе. Отдельный аккаунт для теста роли потерялся, но можно проверить на этом;
* Логин и пароль суперюзера: <br>
  * login: ~~super~~
  * passwod: ~~test~~
