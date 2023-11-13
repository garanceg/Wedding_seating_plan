import pytest
from peewee import *
import sys
sys.path.append("src")
from profil import db, Orga, Guest, Player, Tables

db.connect() #connecting to the database
db.create_tables([Guest, Player, Orga, Tables]) #creating the tables 

data_orga_test = {'name':'John',
        'surname':'Doe',
        'email':'johndoe@example.com',
        'password':'password',
        'mariage':'test_wed',
        'groom_name':'John',
        'groom_surname':'Doe',
        'bride_name':'Jane',
        'bride_surname':'Doe'}


def test_orga_full_name():
    # Test if the full name is returned as expected
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    expected_full_name = orga_test.name + ' ' + orga_test.surname
    print(expected_full_name)
    assert orga_test.orga_full_name() == expected_full_name
    orga_test.delete_instance()

def test_groom_full_name():
    # Test if the groom full name is returned as expected
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    expected_full_name = orga_test.groom_name + ' ' + orga_test.groom_surname
    assert orga_test.groom_full_name() == expected_full_name
    orga_test.delete_instance()

def test_bride_full_name():
    # Test if the bride full name is returned as expected
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    expected_full_name = orga_test.bride_name + ' ' + orga_test.bride_surname
    assert orga_test.bride_full_name() == expected_full_name
    orga_test.delete_instance()

def test_get_orga_mariage():
    # Test if the expected orga is returned based on the given mariage name
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    orga = Orga.get_orga_mariage('test_wed')
    assert orga.mariage == orga_test.mariage
    assert orga.email == orga_test.email
    assert orga.password == orga_test.password
    orga_test.delete_instance()

def test_get_orga_mail_returns_None_when_no_record():
    # Test if None is returned when there is no orga with the given mariage name and email
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    orga = Orga.get_orga_mail('non_existing_mariage', 'non_existing_email')
    assert orga is None
    orga_test.delete_instance()

def test_get_orga_mail():
    # Test if the expected orga is returned based on the given mariage name and email
    orga_test =  Orga.create(**data_orga_test)
    orga_test.save()
    orga = Orga.get_orga_mail('test_wed', 'johndoe@example.com')
    assert orga.mariage == orga_test.mariage
    assert orga.email == orga_test.email
    orga_test.delete_instance()


db.close()