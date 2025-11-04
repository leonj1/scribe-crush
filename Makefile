.PHONY: start stop restart logs status

start:
	docker compose up -d

stop:
	docker compose down

restart: stop start

logs:
	docker compose logs -f

status:
	docker compose ps
