# Django Cars API

Simple Django Rest Framework app providing a REST API for a basic makes and models database interacting with external Product Information Catalog Vehicle Listing (vPIC) [API](https://vpic.nhtsa.dot.gov/api/).

# Getting started

Django cars API is hosted on heroku: https://kszczyrbak-django-cars.herokuapp.com

# Running the app

There are two ways to run this app - locally or using docker-compose.
First, clone this repo to a directory of your choice. The directory containing this README will be the work directory for all of the CLI commands afterwards.

## Docker

### Requirements

Install Docker for the OS of your choice.

In this directory, create a `docker.env` file, copying the environment variables from the `.env.template` file and filling them according to the instructions in the comments.

**Make sure to put every variable and its value in a separate line!**

Make sure Docker backend is running, then:
```
docker-compose build
docker-compose up -d
```

If those commands successfully complete, try out your composed instance at http://localhost:8000/api/cars/.

If you can see the BrowsableAPI interface, congrats! You have a running instance of Django Cars API.

## Locally

### Requirements

First, install the requirements to the virutal or global Python environment:

`pip install -r requirements.txt`

### Configuration
Before running the Django app, you have to set the configuration variables. The necessary variables are listed in the `.env.template` file. You can either:
* Set the environment variables specified in the template file manually, or
* Use the installed `dotenv` package, to set those variables locally, using the .template file. Make sure that the path to the created .env file in `settings.py load_dotenv` function is correct.

**When using .env, make sure to put every variable and its value in a separate line!**


Then, go back to the project directory, and perform migrations on the database:

```python manage.py migrate```

### Running the server

If this command runs without errors, great! Now, try to run the server. You can either use the built-in webserver:

`python manage.py runserver 8000`

or, but only if you are not on Windows, use the installed Gunicorn WSGI:

`gunicorn django_cars.wsgi`

# Running tests

To run the tests, use:

`python manage.py test`

To run tests in Docker environment, connect to the shell of running instance and run that same command.

# API Specification

The created API consists of four endpoints:


| URL          | Verb | Description                     | Filtering   | Ordering            |
| ------------ | ---- | ------------------------------- | ----------- | ------------------- |
| /api/cars    | GET  | Get a list of cars              | make, model | make, model, rating |
| /api/cars    | POST | Add a new car                   | -           | -                   |
| /api/rate    | POST | Rate a car                      | -           | -                   |
| /api/popular | GET  | Get a list of most popular cars | make        | -                   |

## Pagination

This API uses limit/offset pagination. The default limit is set to 10, you can modify that value in `settings.py` `REST_FRAMEWORK` dictionary.

You can use the limit and offset query params to modify the size of result set.

The result sets contain hyperlinks to next and previous pages of your query, supposing the same limit size. If the `next` or `previous` fields are `null`, that means there aren't any other cars in the API to return in another query. 
### Examples:

`GET https://kszczyrbak-django-cars.herokuapp.com/api/cars/?limit=5`

* Returns 5 first cars of a set of all cars in the API.

`https://kszczyrbak-django-cars.herokuapp.com/api/cars/?limit=2&offset=1`

* Returns first 2 cars after the first car in the API.
## Filtering and ordering

Options specified in filtering and ordering fields of the table can be used in query params to accordingly filter and/or order the returned response set.

### Examples:

`GET https://kszczyrbak-django-cars.herokuapp.com/api/cars/?make=Honda&ordering=-rating`

* Returns a set of cars made by Honda, sorted by their rating in descending order.

`GET https://kszczyrbak-django-cars.herokuapp.com/api/cars/?make=audi&ordering=model`

* Returns a set of cars made by Audi, sorted by their model name in ascending order.

 **Filtering param values are case insensitive, but match only the exact value - be wary of spelling mistakes!**
 
 # Chosen technologies
 
 ## Database
 PostgreSQL - Pairs well with Django, also it's the db I'm most familiar with
 
 ## Additional packages
 Requests - Standard choice to perform HTTP requests for external API's
 Django-filter - Easy to use class-based filtering and ordering for viewsets
 Gunicorn - Popular choice for production WSGI servers
 WhiteNoise - Pairs well with Django, allows to serve static files easier in WSGI apps
 
