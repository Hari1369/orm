1) Build Images
docker compose build

2) Start Containers
docker compose up

3) Stop Containers
docker compose down

4) Check Running Containers
docker ps

5) All containers
docker ps -a

6) LIVE Django Logs (Like runserver)
docker compose logs -f web

7) Also delete volumes (DB data)
docker compose down -v

5) Verify Containers Are Gone
docker ps -a

6) start and run a multi-container application
docker compose up -d

7) Run Django commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell

8) Stop everything
docker compose down


7) ENTER THE POSTGRES DATABASE
docker compose exec db psql -U quantumd -d project_1


9) Start ONLY database first
docker compose up -d db











2) Delete ALL Stopped Containers (Cleanup)
docker container prune

1) Delete EVERYTHING (Containers + Images + Volumes)
docker system prune -a --volumes