# Zebrands


## How to run

- Search for the file *zebrands/dotenv.template* and rename it as ".env".
Complete the environment on your ".env" file.
- Create your data directory on database folder:
    `mkdir ./database/data`
- On root folder run the command
  `docker-compose -f docker-compose.dev.yml up`
- Once the server is up and running, it is necessary to load the fixtures.

    `$ docker exec -it zebrands-api /bin/bash`
    
    `$ python manage.py loaddata users`


## Important URLS

- [0.0.0.0:8000/api/doc/](https://) The doc of the project
- [0.0.0.0:8000/admin/](https://) Django admin
- [0.0.0.0:5555](https://) Flower
