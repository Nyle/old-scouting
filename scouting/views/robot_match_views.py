#scouting/views/robot_match_views.py

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.response import Response
from pyramid.view import view_config
#
from sqlalchemy.exc import DBAPIError
#
from ..models import (
    DBSession,
    Robot,
    Match,
    RobotMatch,
    )
#
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )
#
@view_config(route_name='add_robot_match_data', permission='add',
             renderer='../templates/add_robot_match_data.pt')
def add_robot_match_data(request):
    robot_number = request.matchdict['robot_number']
    match_number = request.matchdict['match_number']
    robot_match = DBSession.query(RobotMatch).filter_by(
                   match_number=match_number, robot_number=robot_number).first()
    robot = DBSession.query(Robot).filter_by(number=robot_number).first()
    if 'form.submitted' in request.params:
        robot_match.speed = request.params['speed']
        robot_match.stability = request.params['stability']
        robot_match.occurrences = request.params['occurrences']
#
        if robot.shooter:
            robot_match.auto_1 = request.params['auto_1']
            robot_match.auto_2 = request.params['auto_2']
            robot_match.auto_3 = request.params['auto_3']
            robot_match.auto_miss = request.params['auto_miss']
#
            robot_match.teleop_1 = request.params['teleop_1']
            robot_match.teleop_2 = request.params['teleop_2']
            robot_match.teleop_3 = request.params['teleop_3']
            robot_match.teleop_5 = request.params['teleop_5']
            robot_match.teleop_miss = request.params['teleop_miss']
        if robot.climb:
            robot_match.attempted_climb = 'attempted_climb' in request.params
            if robot_match.attempted_climb:
                robot_match.level_reached = request.params['level_reached']
                robot_match.time_at_start = request.params['time_at_start']
                robot_match.time_at_end = request.params['time_at_end']
                robot_match.frisbees_dumped = request.params['frisbees_dumped']
        if robot.human_loading:
            robot_match.human_loaded = request.params['human_loaded']
            robot_match.human_missed = request.params['human_missed']
        if robot.ground_loading:
            robot_match.auto_loaded = request.params['auto_loaded']
            robot_match.teleop_loaded = request.params['teleop_loaded']
#
        robot_match.scout = request.params['scout']
        robot_match.is_scouted = True
        DBSession.add(robot_match)
        next_match = DBSession.query(Match).filter_by(
                                            number=int(match_number)+1).first()
        if next_match is not None:
            for number, position in (
                [(next_match.r_1, 'r_1'), (next_match.r_2, 'r_2'),
                 (next_match.r_3, 'r_3'), (next_match.b_1, 'b_1'),
                 (next_match.b_2, 'b_2'), (next_match.b_3, 'b_3')]):
                if position == robot_match.position:
                    next_match_robot_number = number
            return HTTPFound(location=request.route_url('add_robot_match_data',
                                        robot_number=next_match_robot_number,
                                        match_number=next_match.number))
        return HTTPFound(location = request.route_url('view_home'))
    return dict(robot_match=robot_match, robot=robot,
                logged_in=authenticated_userid(request))
#
@view_config(route_name='edit_robot_match', permission='edit',
             renderer='../templates/edit_robot_match.pt')
def edit_robot_match(request):
    robot_number = request.matchdict['robot_number']
    match_number = request.matchdict['match_number']
    robot_match = DBSession.query(RobotMatch).filter_by(
                   match_number=match_number, robot_number=robot_number).first()
    robot = DBSession.query(Robot).filter_by(number=robot_number).first()
    if 'form.submitted' in request.params:
        robot_match.speed = request.params['speed']
        robot_match.stability = request.params['stability']
        robot_match.occurrences = request.params['occurrences']
#
        if robot.shooter:
            robot_match.auto_1 = request.params['auto_1']
            robot_match.auto_2 = request.params['auto_2']
            robot_match.auto_3 = request.params['auto_3']
            robot_match.auto_miss = request.params['auto_miss']
#
            robot_match.teleop_1 = request.params['teleop_1']
            robot_match.teleop_2 = request.params['teleop_2']
            robot_match.teleop_3 = request.params['teleop_3']
            robot_match.teleop_5 = request.params['teleop_5']
            robot_match.teleop_miss = request.params['teleop_miss']
        if robot.climb:
            robot_match.attempted_climb = 'attempted_climb' in request.params
            if robot.attempted_climb:
                robot_match.level_reached = request.params['level_reached']
                robot_match.time_at_start = request.params['time_at_start']
                robot_match.time_at_end = request.params['time_at_end']
                robot_match.frisbees_dumped = request.params['frisbees_dumped']
        if robot.human_loading:
            robot_match.human_loaded = request.params['human_loaded']
            robot_match.human_missed = request.params['human_missed']
        if robot.ground_loading:
            robot_match.auto_loaded = request.params['auto_loaded']
            robot_match.teleop_loaded = request.params['teleop_loaded']
#
        robot_match.scout = request.params['scout']
        robot_match.is_scouted = 'is_scouted' in request.params
        DBSession.add(robot_match)
        matches = DBSession.query(Match)
        return HTTPFound(location=request.route_url('view_robot',
                                                    number=robot_number))
    return dict(robot_match=robot_match, robot=robot,
                logged_in=authenticated_userid(request))
