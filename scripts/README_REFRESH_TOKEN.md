# Получение Refresh Token с нужными скоупами

## Подготовка

1. Установите зависимости:
```bash
pip install google-auth-oauthlib google-auth-httplib2
```

2. Убедитесь что у вас есть:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`

## Запуск

```bash
export GOOGLE_CLIENT_ID="your_client_id"
export GOOGLE_CLIENT_SECRET="your_client_secret"

python scripts/get_refresh_token.py
```

## Что происходит

1. Скрипт запустит локальный сервер на порту 8080
2. Откроется браузер с OAuth consent screen
3. Авторизуйтесь и **выберите ВСЕ разрешения**
4. После успешной авторизации скрипт выведет refresh_token

## Результат

Скрипт выведет:
```
Refresh Token:
1//0gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Access Token:
ya29.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Scopes granted:
  - openid
  - https://www.googleapis.com/auth/userinfo.email
  - https://www.googleapis.com/auth/userinfo.profile
  - https://www.googleapis.com/auth/gmail.readonly
  - https://www.googleapis.com/auth/gmail.send
  - https://www.googleapis.com/auth/gmail.compose
  - https://www.googleapis.com/auth/gmail.modify
  - https://www.googleapis.com/auth/gmail.labels
  - https://www.googleapis.com/auth/calendar
  - https://www.googleapis.com/auth/calendar.readonly
  - https://www.googleapis.com/auth/calendar.events
```

## Использование

Скопируйте Refresh Token и установите его как переменную окружения:

```bash
export TMP_REFRESH_TOKEN="1//0gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Или добавьте в `.env` файл вашего приложения.

## Troubleshooting

### Ошибка "redirect_uri_mismatch"

Добавьте `http://localhost:8080/` в список Authorized redirect URIs в Google Cloud Console:
1. Откройте https://console.cloud.google.com/apis/credentials
2. Выберите ваш OAuth Client ID
3. В разделе "Authorized redirect URIs" добавьте: `http://localhost:8080/`
4. Сохраните и попробуйте снова

### Порт 8080 занят

Измените порт в скрипте (например, на 8081):
```python
credentials = flow.run_local_server(
    port=8081,  # <-- измените здесь
    ...
)
```

И добавьте новый redirect URI в Google Cloud Console: `http://localhost:8081/`
