# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Seeding primary data for the dashboard application.
"""

from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import internet, person, date_time
from dashboard.models import ContactList, Contact, Template, Mailing

fake = Faker()
fake.add_provider((internet, person, date_time))


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed()
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    Mailing.objects.all().delete()
    Template.objects.all().delete()
    ContactList.objects.all().delete()
    Contact.objects.all().delete()


def create_contact(quantity, contact_list):
    # type: (int, ContactList) -> None
    """Creates a contact object."""
    for _ in range(quantity):
        contact = Contact(
            email=fake.ascii_free_email(),
            last_name=fake.last_name(),
            first_name=fake.first_name(),
            date_of_birth=fake.date(),
        )
        contact.save()
        contact.lists = [contact_list]
        contact.save()


def create_contact_list():
    # type: () -> ContactList
    """Creates a contact list object"""
    contact_list = ContactList(
        name='Test contact list',
    )
    contact_list.save()

    return contact_list


def create_template():
    # type: () -> Template
    """Creates a template object"""
    template = Template(
        name='Test template',
        subject='Test email subject line.',
        body='I am a test letter for {{last_name}} {{first_name}} who was born on {{date_of_birth}}',
    )

    template.save()

    return template


def create_mailing(contact_list, template):
    # type: (ContactList, Template) -> None
    """Creates a mailing object"""
    Mailing(
        contact_list=contact_list,
        template=template,
    ).save()


def run_seed():
    """Seed database based on mode"""
    clear_data()
    contact_list = create_contact_list()
    template = create_template()

    create_contact(100, contact_list)

    create_mailing(contact_list, template)
