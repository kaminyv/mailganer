
# pull official base image
FROM python:2.7.18-alpine

# set work directory
WORKDIR /usr/src/app

# install psycopg2 dependencies
RUN apk update && apk add gcc musl-dev python-dev postgresql-dev


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./mailganer/entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
#COPY . /usr/src/app/

# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]