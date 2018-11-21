# Satori's personal website 2.0

This is the source code of mysite 2.0, which is completely different from [the old one][1]

The code contains two parts. The frontend code and the backend code. But during the development, I will firstly build the backend side.

The main solution to build the website is that we use [nuxt][2] to build the frontend side(through the node server), and [django][3]. 


## Setup

### 1. Install backend dependency

For ubuntu 16.04 or newer, other linux system is similar.

1. install python and pip and virtualenv

```
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

2. make a virtualenv and install other dependency

```
mkdir new_mysite
cd new_mysite
git clone https://github.com/KomeijiSatori/new_mysite
virtualenv --python=python3.6 .
source bin/activate
cd new_mysite
pip install -r requirements.txt
```

3. make your own settings_local.py

Go to backend/src/new_mysite/

Then make a setting_local.py and fill in your own setting. Like DEBUG, SECRET_KEY and ALLOWED_HOSTS and so on.

4. install redis

```
sudo apt-get install redis-server
```

5. migrate, collect static files for admin and run debug server

```
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

And the django server will run on localhost:8000

### 2. Install frontend dependency

1. install node and npm

```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

2. build and run the frontend code

First move to the frontend directory

```
npm install
npm run dev
```

And then the node server will run on localhost:3000

### 3. Make Frontend and Backend part work together

1. install nginx

```
sudo apt install nginx
```

2. make the config file

This step is very important, since two server run on different port, the cannot communicate to each other directly.

So we use nginx's reverse proxy to make them communicate.

Copy the following code to your nginx conf files, for example, /etc/nginx/sites-enabled/new_mysite.conf, root permission is required.

```
server {
    listen      80;
    server_name 127.0.0.1;
    charset     utf-8;

    location /admin {
        proxy_pass                          http://127.0.0.1:8000;
    }

    location /static {
        alias /home/satori/new_mysite/new_mysite/backend/static;  # This should be changed to your own static file folder
    }

    location /api {
        proxy_pass                          http://127.0.0.1:8000;
    }

    location / {
        proxy_pass                          http://127.0.0.1:3000;
    }
}
```

You **should** change the alias of location static to your own static file folder(the folder where collectstatic command put files in).

This config file tells nginx that I will listen to port 80(other port will also be ok), when a url comes with prefix admin(the default django admin pages),

we pass the request to the django server. We point the `/static` to django's static file directory, so the django admin pages can find static files.

Since our api call will have a prefix `/api`, so when a url comes with prefix api, pass it to django server to deal with the api call.

And last, we pass the other request to the node server to render the pages.

3. restart nginx

```
sudo service nginx restart
```

### 4. Play with it

1. make a superuser

Go to backend/

```
python manage.py createsuperuser
```

2. add other users

Go to localhost/admin to make more users as you like.

3. play

Just visit localhost to play with it. Have fun!


## The reason to use nuxt and django

The reason to use nuxt is that it is a server side render framework to vue.js. The server side render is better for SEO. Vue is a powerful frontend framework that is responsive, which can replace the django template render.

Django is a real powerful web framework that can help build application rather quick, while the template render seems not capable for large scale web application, so I decide to use vue to replace this part.


[1]: https://github.com/KomeijiSatori/mysite
[2]: https://nuxtjs.org/
[3]: https://www.djangoproject.com/
