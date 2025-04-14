# Lazy Excuse Generator

Генератор смішних відмазок і бабусиних порад, створений з використанням Flask, Firebase Firestore і Railway. Проєкт охоплює всі 4 моделі хмарних сервісів: SaaS, PaaS, FaaS, IaaS.

---

## Демонстрація

- Вебсайт: [lazy-api-production.up.railway.app](https://lazy-api-production.up.railway.app)
- API: `GET /random-excuse`
- Логи: `GET /logs`

---

## Стек технологій

| Модель | Що реалізовано |
|--------|-----------------|
| **SaaS** | Інтерфейс з кнопкою, емодзі, бабусею, звуками |
| **PaaS** | Хостинг через Railway (Flask-сервер) |
| **FaaS** | Firebase Firestore — serverless база даних |
| **IaaS** | Лог-файл `excuse-log.txt` на віртуальному диску Railway |

---

## 🔧 Як запустити локально

### 1. Клонувати репозиторій

```bash
git clone https://github.com/SofiiaLapina/lazy-api.git
cd lazy-api
```

### 2. Додати файл `firebase-key.json`

> Цей файл не зберігається в GitHub. Попросіть його в автора проєкту.

### 3. Встановити залежності

```bash
python3 -m pip install -r requirements.txt
```

### 4. Запустити сервер

```bash
python3 main.py
```

### 5. Відкрити у браузері

- `http://localhost:5000` — головна сторінка
- `http://localhost:5000/random-excuse` — API
- `http://localhost:5000/logs` — лог-файл (IaaS доказ)

---

## Структура проєкту

```
lazy-api/
├── firebase-key.json        #  секретний ключ Firebase (локально)
├── main.py                  #  Flask API
├── phrases.json             #  фрази для імпорту
├── import_excuses.py        #  імпорт фраз у Firestore
├── excuse-log.txt           #  лог-файл запитів (IaaS)
├── requirements.txt         #  залежності
└── templates/
    └── index.html           #  інтерфейс
```

---


