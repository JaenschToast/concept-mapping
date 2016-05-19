import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import networkx as nx
import sys

def index():
    return dict(message=T('Hello!'))

def form():
    db = DAL('sqlite://storage.sqlite')
    db.define_table('person',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('married', 'boolean'),
    Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
    Field('profile', 'text'),
    Field('image', 'upload'))
    SQLFORM(db.person)
    form = SQLFORM(db.person)
    if form.process().accepted:
	response.flash = 'form accepted'
    elif form.errors:
	response.flash = 'form has errors'
    else:
	response.flash = 'please fill out the form'
    return dict(form=form)
"""
    form = FORM(TABLE(
        TR('Your first name:', INPUT(_type='text', _name='firstname',
           requires=IS_NOT_EMPTY())),
        TR('Your last name:', INPUT(_type='text', _name='lastname',
           requires=IS_NOT_EMPTY())),
	TR('', INPUT(_type='submit', _value='SUBMIT')),
    ))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form is invalid'
    else:
        response.flash = 'please fill the form'
    return dict(form=form, vars=form.vars)"""


def user():
    return dict(form=auth())


@cache.action()

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    return service()


