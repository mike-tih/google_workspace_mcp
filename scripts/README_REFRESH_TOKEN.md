# Получение Refresh Token с нужными скоупами

Этот скрипт помогает получить Google OAuth refresh token с необходимыми правами доступа для Gmail и Calendar.

## 🚀 Быстрый старт

### 1. Настройте Google Cloud Console

1. Откройте https://console.cloud.google.com/apis/credentials
2. Выберите ваш OAuth 2.0 Client ID (или создайте новый)
3. В разделе **"Authorized redirect URIs"** добавьте:
   ```
   http://localhost:8080/
   ```
4. Сохраните изменения
5. Скопируйте **Client ID** и **Client Secret**

### 2. Установка и настройка

```bash
cd scripts

# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env своими credentials
nano .env  # или используйте любой редактор

# Запустите установку
chmod +x setup.sh run.sh
./setup.sh
```

### 3. Запуск

```bash
./run.sh
```

Скрипт:
1. Откроет браузер с OAuth consent screen
2. Попросит авторизоваться в Google
3. Покажет список разрешений (должно быть 11 пунктов)
4. **ВАЖНО**: Выберите ВСЕ разрешения
5. После успешной авторизации выведет refresh_token

### 4. Результат

После успешной авторизации вы увидите:

```
======================================================================
SUCCESS!
======================================================================

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

======================================================================
Next steps:
======================================================================
1. Copy the refresh token above
2. Set it as TMP_REFRESH_TOKEN environment variable
3. Update your code to use it
```

### 5. Использование refresh token

Скопируйте refresh token и используйте в вашем приложении:

```bash
export TMP_REFRESH_TOKEN="1//0gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX..."
```

Или добавьте в `.env` файл вашего приложения.

## 📁 Структура файлов

```
scripts/
├── get_refresh_token.py   # Основной скрипт
├── setup.sh                # Установка venv и зависимостей
├── run.sh                  # Запуск скрипта с загрузкой .env
├── requirements.txt        # Python зависимости
├── .env.example            # Шаблон для credentials
└── .env                    # Ваши credentials (создается вручную)
```

## 🔧 Troubleshooting

### Ошибка: "redirect_uri_mismatch"

**Причина**: redirect URI не настроен в Google Cloud Console

**Решение**:
1. Откройте https://console.cloud.google.com/apis/credentials
2. Выберите ваш OAuth Client ID
3. Добавьте `http://localhost:8080/` в "Authorized redirect URIs"
4. Сохраните и подождите 1-2 минуты
5. Попробуйте снова

### Ошибка: "Address already in use" (порт 8080 занят)

**Решение 1** - Остановите процесс на порту 8080:
```bash
# Найдите процесс
lsof -ti:8080

# Остановите его
kill $(lsof -ti:8080)
```

**Решение 2** - Измените порт в скрипте:

Отредактируйте `get_refresh_token.py`, замените `port=8080` на другой порт (например, 8081):

```python
credentials = flow.run_local_server(
    port=8081,  # <-- измените здесь
    ...
)
```

И добавьте новый redirect URI в Google Cloud Console: `http://localhost:8081/`

### Ошибка: "invalid_grant" в OAuth Playground

**Причина**: OAuth Playground не всегда правильно передает scopes при обмене code на token

**Решение**: Используйте этот скрипт вместо OAuth Playground - он правильно обрабатывает весь OAuth flow

### Virtual environment не создается

**Проверьте наличие python3-venv**:

```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# macOS (через Homebrew)
# venv уже включен в Python

# Windows
# venv уже включен в Python
```

### Браузер не открывается автоматически

Скрипт выведет URL в консоль. Скопируйте его и откройте вручную в браузере.

## 📝 Какие скоупы запрашиваются

### Базовые (обязательные):
- `openid` - OpenID Connect
- `https://www.googleapis.com/auth/userinfo.email` - Email пользователя
- `https://www.googleapis.com/auth/userinfo.profile` - Профиль пользователя

### Gmail:
- `https://www.googleapis.com/auth/gmail.readonly` - Чтение писем
- `https://www.googleapis.com/auth/gmail.send` - Отправка писем
- `https://www.googleapis.com/auth/gmail.compose` - Создание черновиков
- `https://www.googleapis.com/auth/gmail.modify` - Изменение писем
- `https://www.googleapis.com/auth/gmail.labels` - Управление метками

### Calendar:
- `https://www.googleapis.com/auth/calendar` - Полный доступ к календарю
- `https://www.googleapis.com/auth/calendar.readonly` - Чтение календаря
- `https://www.googleapis.com/auth/calendar.events` - Управление событиями

## 🔐 Безопасность

- ⚠️ **Никогда не коммитьте файл `.env` в git**
- ⚠️ **Храните refresh token в секрете** - он дает постоянный доступ к аккаунту
- ✅ `.env` уже добавлен в `.gitignore`
- ✅ Используйте переменные окружения или secret management системы в production

## 🆘 Дополнительная помощь

Если у вас остались вопросы:
1. Проверьте [Google OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2)
2. Убедитесь что все API включены в Google Cloud Console
3. Проверьте что OAuth consent screen настроен корректно
