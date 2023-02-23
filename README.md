This repository is a simple blueprint for running a Django project on 2 Docker containers (`djangoproject`, `postgres`) using *docker-compose*.

It has has step-by-step instructions for both *Development* and *Production*. All commands below have been tested on Linux Debian 11.

First of all clone the current repository on your disk and remove the git repository link:
```
git clone <REPOSITORY_SSH_URL> /path/to/repo
cd /path/to/repo
rm -rf .git*
```



# Development

**Overview**

*(see compose-dev.yaml, djangoproject/Dockerfile-dev)*

The `djangoproject` container simply links to the `djangoproject` codebase directory on the host machine. So you can keep coding on the host machine while Django web server runs in the container, auto-restarts after code changes, serves static files.

**Caveat**

All commands below are preceeded by `env UID=$(id -u) GID=$(id -g)`. This makes the container set ownership of any new file it creates (e.g. when your run Django `startapp`) to the same user of your host machine.

**Setup steps**

* On your disk, cd into the root of the repository:
    ```
    cd /path/to/repo
    ```

* Create the environment file for the `djangoproject` container in the root of the repo:
    ```
    touch djangoproject.env
    ```

* Open `djangoproject.env` and insert environment variables (below is an example):
    ```
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1
    CSRF_COOKIE_SECURE=False
    CSRF_TRUSTED_ORIGINS=http://127.0.0.1:50500
    SECRET_KEY=somesecr3tkeY
    SESSION_COOKIE_SECURE=False
    WEBSITE_BASE_URL=http://127.0.0.1:50500

    # These work out of the box with the Postgres container (see compose-dev.xml)
    DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
    DATABASE_HOST=postgres
    DATABASE_PORT=5432
    DATABASE_NAME=thedbname
    DATABASE_USER=thedbuser
    DATABASE_PASSWORD=thedbpwd
    DATABASE_SSLMODE=disable
    ```

* Start all containers:
    ```
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml up -d
    ```

* Perform the Django db migration (re-run these every time you make model.py changes in the codebase):
    ```
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec djangoproject python manage.py makemigrations
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec djangoproject python manage.py migrate
    ```

* Here's how to create your first Django superuser and do Django static file collection, if needed:
    ```
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec djangoproject python manage.py createsuperuser
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec djangoproject python manage.py collectstatic
    ```

* Using a web browser, go to the `/admin/` endpoint of the `WEBSITE_BASE_URL` you configured in `djangoproject.env`. For example:
    ```
    http://127.0.0.1:50500/admin/
    ```

* Useful commands:
    ```
    # Kill all containers but preserve the Postgres volume:
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml down

    # View Django logs
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml logs djangoproject

    # Create new Django app "ciaooo"
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec djangoproject python manage.py startapp ciaooo

    # Access the Postgres CLI:
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec postgres psql -U thedbuser thedbname

    # Import Postgres records from a SQL file:
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec -T postgres psql -U thedbuser thedbname < import.sql

    # Export Postgres records to a SQL file:
    env UID=$(id -u) GID=$(id -g) docker-compose --file compose-dev.yaml exec postgres pg_dump -U thedbuser thedbname > exported.sql
    ```



# Production

**Overview**

*(see compose-prod.yaml, djangoproject/Dockerfile-prod)*

The `djangoproject` container stores a copy of the `djangoproject` codebase, runs Gunicorn on port 6970, runs Nginx on port 80, Nginx proxies to Gunicorn and serves Django static files.

**Setup steps**

* On your disk, cd into the root of the repository:
    ```
    cd /path/to/repo
    ```

* Create the environment variables file for the `djangoproject` container in the root of the repo, so outside the `djangoproject` directory:
    ```
    touch djangoproject.env
    ```

* Open `djangoproject.env` and add environment variables, here's an example:
    ```
    DEBUG=False
    ALLOWED_HOSTS=yourdomain.com
    CSRF_COOKIE_SECURE=True
    CSRF_TRUSTED_ORIGINS=https://yourdomain.com
    SECRET_KEY=somesecr3tkeY
    SESSION_COOKIE_SECURE=True
    WEBSITE_BASE_URL=https://yourdomain.com

    # These work out of the box with the Postgres container (see compose-prod.xml)
    DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
    DATABASE_HOST=postgres
    DATABASE_PORT=5432
    DATABASE_NAME=thedbname
    DATABASE_USER=thedbuser
    DATABASE_PASSWORD=thedbpwd
    DATABASE_SSLMODE=disable
    ```

* Start the containers. Please note that Django db migration + static file collection get executed automatically (see `diangoproject/Dockerfile-prod`):
    ```
    docker-compose --file compose-prod.yaml up -d
    ```

* Here's how to create your first Django superuser, if needed:
    ```
    docker-compose --file compose-prod.yaml exec djangoproject python manage.py createsuperuser
    ```

* Setup an Nginx website on the host machine to proxy pass your domain to `http://127.0.0.1:50500`, here's a sample nginx site configuration:
    ```
    server {
        server_name yourdomain.com;
        location / {
            proxy_pass          http://127.0.0.1:50500;
            proxy_redirect      off;
            proxy_set_header    Host $host;
            proxy_set_header    X-Real-IP $remote_addr;
            proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header    X-Forwarded-Host $server_name;
            proxy_set_header    X-Forwarded-Proto https;
            include             /etc/nginx/mime.types;
        }
    }
    ```

* Secure your domain with TLS (https), perhaps using Certbot.

* Using a web browser, go to the `/admin/` endpoint of the `WEBSITE_BASE_URL` you configured in `djangoproject.env`. For example:
    ```
    https://yourdomain.com/admin/
    ```

* Useful commands:
    ```
    # Kill all containers but preserve the Postgres volume:
    docker-compose --file compose-prod.yaml down

    # View Django logs
    docker-compose --file compose-prod.yaml logs djangoproject

    # Access the Postgres CLI:
    docker-compose --file compose-prod.yaml exec postgres psql -U thedbuser thedbname

    # Import Postgres records from a SQL file:
    docker-compose --file compose-prod.yaml exec -T postgres psql -U thedbuser thedbname < import.sql

    # Export Postgres records to a SQL file:
    docker-compose --file compose-prod.yaml exec postgres pg_dump -U thedbuser thedbname > exported.sql
    ```


