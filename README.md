# Опросник на Django 2 + DRF 3

## Инструкция как развернуть проект
### Разворачиваем окружение
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```

### Быстрый способ

* Выполнить

```bash
source venv/bin/activate
python manage.py runserver
```

+ логин и пароль в django admin 1:1 venv

### Если нужно создать бд заново

* Удалить db.sqlite3
* Выполнить

```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# Описание API

```json
{
  "surveys": {
    "/": {
      "GET": {
        "desc": "Получаем все активные опросники"
      },
      "/passed_surveys": {
        "GET": {
          "desc": "Получаем опросники которые прошёл пользователь",
          "params": {
            "user_id": "идентивикатор пользователя"
          }
        }
      }
    }
  },
  "my-answers": {
    "/": {
      "GET": {
        "desc": "Получаем ответы человека на определённый опрос",
        "params": {
          "user_id": "идентификатор пользователя",
          "survey_id": "идентификатор опроса"
        }
      },
      "POST": {
        "id": {
          "type": "integer",
          "required": false,
          "read_only": true,
          "label": "ID"
        },
        "user_id": {
          "type": "string",
          "required": true,
          "read_only": false,
          "label": "User id",
          "max_length": 32
        },
        "question": {
          "type": "field",
          "required": true,
          "read_only": false,
          "label": "Question"
        },
        "survey": {
          "type": "field",
          "required": true,
          "read_only": false,
          "label": "Survey"
        },
        "answ_txt": {
          "type": "string",
          "required": false,
          "read_only": false,
          "label": "Answ txt"
        },
        "answ_choices": {
          "type": "field",
          "required": false,
          "read_only": false,
          "label": "Answ choices"
        }
      }
    }
  },
  "questions": {
    "/": {
      "GET": {
        "desc": "Получаем вопросы для опроса",
        "params": {
          "survey_id": "идентификатор опроса"
        }
      }
    }
  }
```