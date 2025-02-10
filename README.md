
# SportFlow  
**Умная система учета спортивного инвентаря для школ.**  

ССЫЛКА НА ДЕМОНСТРАЦИЮ:
https://rutube.ru/video/private/d6a903ea2342177ecaad9b304afb7d8d/?p=nduTOuLeONN1vr9aZqxBXg

---

## 📖 Оглавление  
- [О проекте](##-о-проекте)  
- [Функционал](##-функционал)  
- [Установка](##-установка)  
- [Использование](##-использование)  
- [Технологии](##-технологии)    

---

## 🚀 О проекте  
**SportFlow** — веб-приложение для эффективного управления спортивным инвентарем в школах.  
Позволяет:  
✅ Отслеживать наличие и состояние инвентаря.  
✅ Распределять снаряжение между пользователями.  
✅ Планировать закупки и формировать отчеты.  
✅ Упростить взаимодействие администраторов и учителей физкультуры.  

---

## 🔧 Функционал  

### 👨💻 Для администраторов  
| Функция                   | Описание                                                                                                          |     |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- | --- |
| **Авторизация**           | Доступ к панели управления через защищенный вход.                                                                 |     |
| **Управление инвентарем** | Добавление, редактирование и удаление позиций (название, количество, состояние: в запасе/используемый/сломанный). |     |
| **Планирование закупок**  | Создание планов закупок с указанием цены и поставщика.                                                            |     |
| **Закрепление инвентаря** | Распределение снаряжения между пользователями.                                                                    |     |

### 👤 Для пользователей (учителей/сотрудников)  
| Функция | Описание |  
|---------|----------|  
| **Регистрация/авторизация** | Создание аккаунта и вход в систему. |  
| **Просмотр инвентаря** | Доступ к списку доступного снаряжения. |  
| **Заявки** | Создание запросов на получение инвентаря и отслеживание их статуса. |  


---

## ⚙️ Установка  
### Через Docker:
1. Клонируйте репозиторий: 
```bash  
git clone https://github.com/yourusername/sportflow.git  
cd sportflow 
```

1. Запустите контейнер 
```bash
# с docker-compose
docker compose up -d

# без docker-compose
docker build -t sportinventory .
docker run -p 8000:8000 -d --name sportinventory sportinventory
```

### Ручной запуск:
1. Клонируйте репозиторий:  
```bash  
git clone https://github.com/yourusername/sportflow.git  
cd sportflow  
```  

2. Установите зависимости:  
```bash  
pip install -r requirements.txt  
```  

3. Настройте базу данных:  
```bash  
python manage.py migrate  
```  

4. Запустите сервер:  
```bash  
python manage.py runserver  
```  

---

## 🖥️ Использование  

### Создание аккаутна администратора
- Используйте команду

```bash
python manage.py createsuperuser  
```

### Для администратора  
- Перейдите по адресу сайта
- Войдите с логином и паролем.  
- Управляйте инвентарем, закупками и отчетами через интуитивную панель.  

### Для пользователя  
- Зарегистрируйтесь на странице `/register`.  
- Подавайте заявки через раздел **"Инвентарь"**.  
- Отслеживайте статус заявок.

---

## 🛠️ Технологии  
- **Backend**: Django (Python)  
- **Frontend**: HTML/CSS, TailwindCSS, JavaScript
- **База данных**: SQLite  

---

**Разработано с ❤️ для школ!**  
**Спасибо, что выбрали SportFlow!** 🏆  
