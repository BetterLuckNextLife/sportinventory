<div align="center">

# sportinventory
</div>

# Docker
```bash
# с docker-compose
docker compose up -d

# без docker-compose
docker build -t sportinventory .
docker run -p 8000:8000 -d --name sportinventory sportinventory
```

# TODO
- [x] ~Создать frontend~
- [x] ~Добавить urls~
- [x] ~Зарендерить странички из view~
- [x] ~Создать модели пользователя и продуктов~
- [x] ~Настроить Docker~
- [ ] Реализовать регистрацию и авторизацию
- [ ] Сделать страницу инвентаря допустимым только для авторизованных пользователей
- [ ] Реализовать взаимодействие страницы инвентаря с базой данных
- [ ] Добавить почту, как способ авторизации/регистрации
- [ ] Защитить приложение от sql-инъкуций и DDos атак
- [ ] Осуществить работу с хостингом

