# scouting/__init__.py
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from scouting.security import (
    groupfinder,
    get_user,
    )


from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='scouting.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('add_user', '/create_account')

    config.add_route('manage_all_users', '/manage')
    config.add_route('manage_user', '/manage/{user}')

    config.add_route('reset_password', '/reset')

    config.add_route('view_robot', '/robot/{number:\d+}')
    config.add_route('add_robot', '/robot/add')
    config.add_route('edit_robot', '/robot/edit')

    config.add_route('view_match', '/match/{number:\d+}')
    config.add_route('add_match_scores', '/match/{number:\d+}/add_scores')
    config.add_route('add_match', '/match/add')
    config.add_route('edit_match', '/match/edit')

    config.add_route('add_robot_match_data',
                     '/robot/{robot_number:\d+}/{match_number:\d+}/add_data')
    config.add_route('edit_robot_match',
                     '/robot/{robot_number:\d+}/{match_number:\d+}/edit')

    config.add_request_method(get_user, 'user', reify=True)

    config.scan()
    return config.make_wsgi_app()
