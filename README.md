# Docker
```bash
# с docker-compose
docker compose up -d

# без docker-compose
docker build -t sportinventory .
docker run -p 8000:8000 -d --name sportinventory sportinventory
```
