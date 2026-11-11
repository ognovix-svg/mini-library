git clone https://github.com/ognovix-svg/mini-library.git
cd mini-library
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_data
