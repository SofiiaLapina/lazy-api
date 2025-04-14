# 🦥 Lazy Excuse Generator — Cloud Project

Жартівливий вебсервіс, який видає випадкові відмазки, коли користувач заходить на сторінку. Ми реалізували повноцінний приклад хмарної архітектури з усіма чотирма моделями: **IaaS, PaaS, SaaS, FaaS**, а також **BaaS** як доповнення.

---

## ☁️ Моделі хмарних сервісів у проєкті

### 📦 IaaS — Інфраструктура як сервіс (AWS EC2)
- Ми створили власний сервер (EC2) на AWS.
- Туди надсилаються логи кожного запиту до API `/random-excuse`.
- Сервер піднятий вручну, встановлено Python та Flask, і приймає POST-запити з логами.
- Вихідний файл: `receive_logs.py`, лог-файл: `received-logs.txt`.

### 🛠️ PaaS — Платформа як сервіс (Railway)
- Основний проєкт задеплоєно на Railway з GitHub.
- Railway автоматично деплоїть Flask API, налаштовує середовище.
- Отримали домен: https://lazy-api-production.up.railway.app

### 💻 SaaS — Програмне забезпечення як сервіс
- Користувачу нічого встановлювати не треба.
- Відмазка видається прямо в браузері (HTML + JS + API).
- Дизайн зроблено у `templates/index.html`, відповідає стилю жартівливого SaaS.

### ⚡️ FaaS — Функція як сервіс (GitHub Actions)
- Окремий GitHub Action виконується автоматично за розкладом.
- Запускає `function.py`, який звертається до Firestore і виводить випадкову відмазку в GitHub Logs.
- 🔄 Немає окремого сервера, лише функція → це і є FaaS.
- ✅`.github/workflows/faas-action.yml`, файл `function.py`, запуск по `cron`.

### 🗄️ BaaS — База як сервіс (Firestore)
- Всі відмазки зберігаються у Firestore (Firebase).
- Ми не піднімали свою базу, лише підключилися через API.
- Файл `phrases.json` — джерело, `import_excuses.py` — імпортує в колекцію `excuses`.

---

## 🗂️ Структура проєкту

```
lazy-api/
├── firebase-key.json            # 🔐 
├── main.py                      # 🌐 Flask API (PaaS)
├── import_excuses.py            # 🛠️ імпорт відмазок
├── phrases.json                 # 📃 відмазки
├── excuse-log.txt               # 🧱 локи (локальні)
├── requirements.txt             # 📦 залежності
├── templates/
│   └── index.html               # 🖼️ інтерфейс (SaaS)
└── .github/
    └── workflows/
        └── faas-action.yml      # ⚙️ GitHub FaaS
```

---

## 🚀 Запуск локально

```bash
pip install -r requirements.txt
python main.py
```

---

## 🔥 Firestore імпорт (одноразово)

```bash
python import_excuses.py
```
