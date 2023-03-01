# Mailganer

The project is done as part of a test assignment.

Demonstrates how the bulk mail service works.

## Test task

Write a small email service in Python 2.7*.

**Tasks:**

1. Sending newsletters using html layout and subscriber list. 
2. To create a mailing list, use an ajax request.
   The form to create a newsletter is filled out in the modal window. 
   Use libraries: jquery, bootstrap. 
3. Sending pending newsletters.
4. Using variables in the mailing list layout.
   (Example: first name, last name, birthday from the list of subscribers)
5. Tracking open emails.

Implement delayed shipments with Celery.

The method of storing email layouts and lists of subscribers 
is at the discretion of the performer.

## Test environment

Docker must be installed for deployment.

**Interfaces (default)**:
- Application web interface: `http://127.0.0.1:8000`
- Web interface of the email client: `http://127.0.0.1:8025`
- Web interface rabbitmq: `http://127.0.0.1:15672`

### Deploying
- Clone the repository: `git clone https://github.com/kaminyv/mailganer.git`
- Go to the project directory: `cd mailganer/`
- Copy the file with the environment variables: 
  `cp mailganer/.env.example mailganer/.env`
- Edit the file with the environment variables: `nano mailganer/.env` 
  (You can leave the default)
- Run the environment build: `docker compose up`
- Start seeding the initial data: 
  `docker compose exec -it web python manage.py seed`

If built successfully, the application interface for the application and 
services will be are available at the addresses specified in **interfaces**.
