web-up:
	docker compose up

web_build:
	docker compose build

web-test:
	docker compose exec -it website pytest

web-tailwind:
