def index():
    return dict(message=T('Hello!'))

def form():

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
    return dict(form=form, vars=form.vars)



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


