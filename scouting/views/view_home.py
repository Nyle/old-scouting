# scouting/views/view_home.py

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

@view_config(route_name='view_home', renderer='../templates/view_home.pt',
             permission='view')
def view_home(request):
    matches = DBSession.query(Match.number, Match.r_1, Match.r_2, Match.r_3,
                Match.b_1, Match.b_2, Match.b_3, Match.r_total, Match.b_total,
                Match.are_scores_entered)
    robots = DBSession.query(Robot.number, Robot.is_scouted)
    robot_matches = DBSession.query(RobotMatch.robot_number,
                RobotMatch.match_number, RobotMatch.is_scouted)
    add_match_url = request.route_url('view_home')
    add_robot_url = request.route_url('view_home')
    return dict(matches=matches, robots=robots, robot_matches=robot_matches,
                logged_in=authenticated_userid(request))
