# notesapp
Simple app allows you to create notes

## Deploy

Move to source directory
`cd django`

Create your .env (from template.env)
`cp template.env .env`

Build Docker containers
`docker-compose build`

Up Docker containers
`docker-compose up -d`

Apply the database migrations
`docker exec -it notesapp-web python manage.py migrate`

To create superuser apply this and follow the instructions
`docker exec -it notesapp-web python manage.py createsuperuser`

To run tests apply this
`docker exec -it notesapp-web python manage.py test`

Your app will deploy on port 8000

## Routing

Admin panel: `/admin`
API: `/api/v1`