.PHONY: clean run

# Tag da imagem
TAG := $(shell python -c "import random; print(f'{random.randint(0, 999999):06}')")

all: clean run

clean:
	@echo Deleting all containers...
	-docker ps -aq | for /f %%i in ('more') do docker stop %%i && docker rm -f %%i
	@echo Deleting all images...
	-docker images -aq | for /f %%i in ('more') do docker rmi -f %%i
	@echo Deleting all volumes...
	-docker volume ls -q | for /f %%i in ('more') do docker volume rm %%i
	@echo Pruning build cache...
	docker builder prune -a -f

run:
	docker build -t sim-api:$(TAG) ./model
	docker build -t licitabot:$(TAG) ./app
	powershell -Command "(Get-Content 'docker-compose.yml') -replace '\d{6}', '$(TAG)' | Set-Content 'docker-compose.yml'"
	docker compose up -d
	docker compose logs -f