1) Delete EVERYTHING (Containers + Images + Volumes)
docker system prune -a --volumes

2) Delete ALL Stopped Containers (Cleanup)
docker container prune

3) Also delete volumes (DB data)
docker compose down -v

4) See RUNNING Containers
cl
ear
5) Verify Containers Are Gone
docker ps -a

6) start and run a multi-container application
docker compose up -d

7) ENTER THE POSTGRES DATABASE
docker compose exec db psql -U quantumd -d project_1

8) docker Django Shell
docker compose exec web python manage.py shell

9) Start ONLY database first
docker compose up -d db