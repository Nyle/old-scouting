# scouting/views/match_views.py

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


@view_config(route_name='view_match', renderer='../templates/view_match.pt',
             permission='view')
def view_match(request):
    number = request.matchdict['number']
    match = DBSession.query(Match).filter_by(number=number).first()
    if match is None:
        return HTTPFound(location = request.route_url('add_match',
                                                     number=number))
    return dict(match=match, logged_in=authenticated_userid(request))

@view_config(route_name='add_match', renderer='../templates/add_match.pt',
             permission='add')
def add_match(request):
    message=''
    if 'form.submitted' in request.params:
        number = int(request.params['number'])
        r_1 = request.params['r_1']
        r_2 = request.params['r_2']
        r_3 = request.params['r_3']
        b_1 = request.params['b_1']
        b_2 = request.params['b_2']
        b_3 = request.params['b_3']

        match = Match(number=number,
                      r_1=r_1, r_2=r_2, r_3=r_3,
                      b_1=b_1, b_2=b_2, b_3=b_3)

        if (DBSession.query(Match).filter_by(number=number).first()
                is not None):
            message = 'Match number {0} has all ready been entered'.format(
                                                                        number)
            return dict(match=match, message=message,
                        logged_in=authenticated_userid(request))

        robot_numbers = [robot.number for robot in DBSession.query(Robot)]
        for robot_number in [match.r_1, match.r_2, match.r_3,
                             match.b_1, match.b_2, match.b_3]:
            if int(robot_number) not in robot_numbers:
                message = 'Robot number {0} is not in the database'.format(
                                                                   robot_number)
                return dict(match=match, message=message,
                            logged_in=authenticated_userid(request))
        if (len(set([match.r_1, match.r_2, match.r_3,
                     match.b_1, match.b_2, match.b_3])) !=
                len([match.r_1, match.r_2, match.r_3,
                     match.b_1, match.b_2, match.b_3])):
             message = 'All Robots must have different numbers'
             return dict(match=match, message=message,
                         logged_in=authenticated_userid(request))

        DBSession.add(match)
        message = 'Match {0} has been added'.format(number)
        number += 1
        match = Match(number=number)
        return dict(match=match, message=message,
                    logged_in=authenticated_userid(request))
    match = Match()
    return dict(match=match, message=message,
                logged_in=authenticated_userid(request))

@view_config(route_name='edit_match', renderer='../templates/edit_match.pt',
             permission='edit')
def edit_match(request):
    message = ''
    original_number = request.params['original_number']
    match = DBSession.query(Match).filter_by(number=original_number).first()
    if 'form.submitted' in request.params:
        match.scout = request.params['scout']

        r_1 = int(request.params['r_1'])
        r_2 = int(request.params['r_2'])
        r_3 = int(request.params['r_3'])
        b_1 = int(request.params['b_1'])
        b_2 = int(request.params['b_2'])
        b_3 = int(request.params['b_3'])

        match.r_disc = request.params['r_disc']
        match.r_climb = request.params['r_climb']
        match.r_foul = request.params['r_foul']
        match.r_total = request.params['r_total']

        match.b_disc = request.params['b_disc']
        match.b_climb = request.params['b_climb']
        match.b_foul = request.params['b_foul']
        match.b_total = request.params['b_total']

        match.are_scores_entered = 'are_scores_entered' in request.params

        robot_numbers = [robot.number for robot in DBSession.query(Robot)]
        for robot_number in [r_1, r_2, r_3, b_1, b_2, b_3]:
            if int(robot_number) not in robot_numbers:
                message = 'Robot number {0} is not in the database'.format(
                                                                   robot_number)
                match.r_1 = int(request.params['r_1'])
                match.r_2 = int(request.params['r_2'])
                match.r_3 = int(request.params['r_3'])
                match.b_1 = int(request.params['b_1'])
                match.b_2 = int(request.params['b_2'])
                match.b_3 = int(request.params['b_3'])
                return dict(match=match, message=message,
                            original_number=original_number,
                            logged_in=authenticated_userid(request))
        if (len(set([r_1, r_2, r_3, b_1, b_2, b_3])) !=
                len([r_1, r_2, r_3, b_1, b_2, b_3])):
            message = 'All Robots must have different numbers'
            match.r_1 = int(request.params['r_1'])
            match.r_2 = int(request.params['r_2'])
            match.r_3 = int(request.params['r_3'])
            match.b_1 = int(request.params['b_1'])
            match.b_2 = int(request.params['b_2'])
            match.b_3 = int(request.params['b_3'])
            return dict(match=match, message=message,
                        original_number=original_number,
                        logged_in=authenticated_userid(request))

        if (request.params['number'] != original_number and
                DBSession.query(Match).filter_by(
                    number=request.params['number']).first()
                is not None):
            message = 'Match number {0} all ready exists'.format(
                                                       request.params['number'])
            match.number = request.params['number']
            return dict(match=match, original_number=original_number,
                        logged_in=authenticated_userid(request),
                        message=message)

        match.set(number=request.params['number'],
                  r_1=r_1, r_2=r_2, r_3=r_3,
                  b_1=b_1, b_2=b_2, b_3=b_3)
        if match.are_scores_entered:
            try:
                match.r_disc = int(match.r_disc)
                match.r_climb = int(match.r_climb)
                match.r_foul = int(match.r_foul)
                match.r_total = int(match.r_total)

                match.b_disc = int(match.b_disc)
                match.b_climb = int(match.b_climb)
                match.b_foul = int(match.b_foul)
                match.b_total = int(match.b_total)
            except ValueError:
                message = 'Scores Entered has been checked, but not all score data are valad integers'
                return dict(match=match, original_number=original_number,
                            logged_in=authenticated_userid(request),
                            message=message)
            if (match.r_disc + match.r_climb + match.r_foul != match.r_total):
                message = 'The red total is not equal to the sum of all the red points'
                return dict(match=match, original_number=original_number,
                            logged_in=authenticated_userid(request),
                            message=message)

            if match.b_disc + match.b_climb + match.b_foul != match.b_total:
                message = 'The blue total is not equal to the sum of all the blue points'
                return dict(match=match, original_number=original_number,
                            logged_in=authenticated_userid(request),
                            message=message)

        DBSession.add(match)

        return HTTPFound(location = request.route_url('view_match',
                                                     number=match.number))
    return dict(match=match, original_number=original_number,
                logged_in=authenticated_userid(request), message=message)

@view_config(route_name='add_match_scores',
             renderer='../templates/add_match_scores.pt', permission='edit')
def add_match_scores(request):
    message = ''
    number = request.matchdict['number']
    match = DBSession.query(Match).filter_by(number=number).first()
    if 'form.submitted' in request.params:
        match.scout = request.params['scout']
        match.r_disc = int(request.params['r_disc'])
        match.r_climb = int(request.params['r_climb'])
        match.r_foul = int(request.params['r_foul'])
        match.r_total = int(request.params['r_total'])

        match.b_disc = int(request.params['b_disc'])
        match.b_climb = int(request.params['b_climb'])
        match.b_foul = int(request.params['b_foul'])
        match.b_total = int(request.params['b_total'])
        if match.are_scores_entered:
            message = 'Scores have allready been entered for this match'
            return dict(match=match, original_number=original_number,
                        logged_in=authenticated_userid(request))
        if (match.r_disc + match.r_climb + match.r_foul != match.r_total):
            message = 'The red total is not equal to the sum of all the red points'
            return dict(match=match, original_number=original_number,
                        logged_in=authenticated_userid(request))

        if match.b_disc + match.b_climb + match.b_foul != match.b_total:
            message = 'The blue total is not equal to the sum of all the blue points'
            return dict(match=match, message=message,
                        logged_in=authenticated_userid(request))
        match.are_scores_entered = True
        DBSession.add(match)

        return HTTPFound(location = request.route_url('view_home'))
    if match.are_scores_entered:
        return HTTPFound(location = request.route_url('view_match',
                                                      number=number))
    return dict(match=match, message=message,
                logged_in=authenticated_userid(request))
