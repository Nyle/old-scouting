# scouting/security_views.py
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from ..models import (
    User,
    DBSession,
    )

from pyramid.response import Response
from pyramid.view import view_config

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from ..security import authenticate

@view_config(route_name='login', renderer='../templates/login.pt')
@forbidden_view_config(renderer='../templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login'].strip()
        password = request.params['password'].strip()
        if authenticate(login, password):
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message, url = request.application_url + '/login',
        came_from = came_from, login = login, password = password,
        logged_in=authenticated_userid(request)
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('view_home'),
                     headers = headers)

@view_config(route_name='add_user', renderer='../templates/add_user.pt')
def add_user(request):
    message = ''
    if 'form.submitted' in request.params:
        login = request.params['login'].strip()
        password_0 = request.params['password_0'].strip()
        password_1 = request.params['password_1'].strip()
        if login == '':
            message = 'Login must have at least one character'
            return dict(login=login, message=message,
                        password_0=password_0, password_1=password_1,
                        logged_in=authenticated_userid(request))
        if DBSession.query(User).filter_by(name=login).first() is not None:
            message = 'That login has allready been taken'
            return dict(login=login, message=message,
                        password_0=password_0, password_1=password_1,
                        logged_in=authenticated_userid(request))
        if password_0 != password_1:
            message = 'Entered passwords are not identical'
            return dict(login=login, message=message,
                        password_0=password_0, password_1=password_1,
                        logged_in=authenticated_userid(request))
        if len(password_0) < 4:
            message = 'Password must be at least 4 characters long'
            return dict(login=login, message=message,
                        logged_in=authenticated_userid(request))
        user = User(name=login, password=password_0, permission='unapproved')
        DBSession.add(user)
        headers = remember(request, login)
        return HTTPFound(location = '/',
                         headers = headers)
    return dict(login='', message=message,
                logged_in=authenticated_userid(request))

@view_config(route_name='manage_all_users', renderer='../templates/manage_all_users.pt',
             permission='manage')
def manage_all_users(request):
    users = DBSession.query(User)
    return dict(users=users, logged_in=authenticated_userid(request))

@view_config(route_name='manage_user', renderer='../templates/manage_user.pt',
             permission='manage')
def manage_user(request):
    message = ''
    name = request.matchdict['user']
    user = DBSession.query(User).filter_by(name=name).first()
    if 'form.submitted' in request.params:
        user.permission = request.params['permission']

        if 'reset_password' in request.params:
            user.set_password('Password')
            message = 'Password reset to "Password"'

        DBSession.add(user)
        return dict(user=user, message=message,
                    logged_in=authenticated_userid(request))
    return dict(user=user, message=message,
                logged_in=authenticated_userid(request))

@view_config(route_name='reset_password',
             renderer='../templates/reset_password.pt')
def reset_password(request):
    message = ''
    if 'form.submitted' in request.params:
        login = request.params['login'].strip()
        password = request.params['password'].strip()
        password_0 = request.params['password_0'].strip()
        password_1 = request.params['password_1'].strip()
        user = DBSession.query(User).filter_by(name=login).first()
        if user is None:
            message = 'There is no user with that name'
            return dict(login=login, message=message,
                        logged_in=authenticated_userid(request))
        if password_0 != password_1:
            message = 'Entered new passwords are not identical'
            return dict(message=message, login=login,
                        logged_in=authenticated_userid(request))
        if len(password_0) < 4:
            message = 'New password must be at least 4 characters long'
            return dict(message=message, login=login,
                        logged_in=authenticated_userid(request))
        if not user.test(password):
            message = 'Old password is not correct'
            return dict(message=message, login=login,
                        logged_in=authenticated_userid(request))
        user.set_password(password_0)
        DBSession.add(user)
        message = 'Password has been changed'
        return dict(message=message, login=login,
                    logged_in=authenticated_userid(request))
    login=''
    return dict(message=message, login=login,
                logged_in=authenticated_userid(request))
