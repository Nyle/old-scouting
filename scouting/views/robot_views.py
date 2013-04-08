# scouting/views/robot_views.py

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Robot,
    Match,
    RobotMatch,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

@view_config(route_name='view_robot', renderer='../templates/view_robot.pt',
             permission='view')
def view_robot(request):
    number = request.matchdict['number']
    robot = DBSession.query(Robot).filter_by(number=number).first()
    if robot is None:
        return HTTPFound(location = request.route_url('add_robot',
                                                     number=number))
    robot_matches = DBSession.query(RobotMatch).filter_by(robot_number=number)
    return dict(robot=robot, robot_matches=robot_matches,
                logged_in=authenticated_userid(request))

@view_config(route_name='add_robot', renderer='../templates/add_robot.pt',
             permission='edit')
def add_robot(request):
    message = ''
    if 'form.submitted' in request.params:
        number = request.params['number']
        wheels = request.params['wheels']
        gearbox = request.params['gearbox']
        drive_motors = request.params['drive_motors']
        description = request.params['description']
        shooter = 'shooter' in request.params
        climb = 'climb' in request.params
        human_loading = 'human_loading' in request.params
        ground_loading = 'ground_loading' in request.params
        scout = request.params['scout']
        robot = Robot(number=number, wheels=wheels, gearbox=gearbox,
                      description=description, shooter=shooter, climb=climb,
                      human_loading=human_loading, scout=scout,
                      ground_loading=ground_loading, is_scouted=True)
        message = 'A robot with that number allready exists'
        if DBSession.query(Robot).filter_by(number=number).first() is not None:
            return dict(robot=robot, message=message)
        DBSession.add(robot)
        robot=Robot()
        message = 'Robot number {0} has been added'.format(number)
        return dict(robot=robot, message=message,
                    logged_in=authenticated_userid(request))
    robot = Robot()
    return dict(robot=robot, message=message,
                logged_in=authenticated_userid(request))

@view_config(route_name='edit_robot', renderer='../templates/edit_robot.pt',
             permission='edit')
def edit_robot(request):
    message = ''
    original_number = request.params['original_number']
    robot = DBSession.query(Robot).filter_by(number=original_number).first()
    if 'form.submitted' in request.params:
        robot.wheels = request.params['wheels']
        robot.gearbox = request.params['gearbox']
        robot.drive_motors = request.params['drive_motors']
        robot.description = request.params['description']
        robot.shooter = 'shooter' in request.params
        robot.climb_10 = 'climb_10' in request.params
        robot.climb = 'climb' in request.params
        robot.human_loading = 'human_loading' in request.params
        robot.ground_loading = 'ground_loading' in request.params
        robot.is_scouted = 'is_scouted' in request.params
        robot.scout = request.params['scout']
        if (request.params['number'] != original_number and
                DBSession.query(Robot).filter_by(
                    number=request.params['number']).first()
                is not None):
            message = 'Robot number {0} allready exists'.format(
                                                       request.params['number'])
            return dict(robot=robot, original_number=original_number,
                        logged_in=authenticated_userid(request),
                        message=message)
        else:robot.number = request.params['number']

        DBSession.add(robot)

        return HTTPFound(location = request.route_url('view_robot',
                                                     number=robot.number))
    robot.is_scouted = True
    return dict(robot=robot, original_number=original_number,
                logged_in=authenticated_userid(request), message=message)
