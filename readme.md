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
5. migrate and run debug server
```
python manage.py migrate
python manage.py runserver
```


### 2. Install node and nuxt
This part has not been used yet, and will be added in later version.

## Run the code
### start the django server

## The reason to use nuxt and django

The reason to use nuxt is that it is a server side render framework to vue.js. The server side render is better for SEO. Vue is a powerful frontend framework that is responsive, which can replace the django template render.
Django is a real powerful web framework that can help build application rather quick, while the template render seems not capable for large scale web application, so I decide to use vue to replace this part. And with django-rest-framework, I can build restful api in a nice way.


[1]: https://github.com/KomeijiSatori/mysite
[2]: https://nuxtjs.org/
[3]: https://www.djangoproject.com/

