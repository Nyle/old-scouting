# scouting/scripts/initializedb.py
import os
import sys
import transaction

from random import (
    randint,
    sample,
    )

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Robot,
    Match,
    RobotMatch,
    Base,
    User,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        robot_numbers = set([randint(1, 3999) for i in range(30)])
        sample_robots = [Robot(number=i) for i in robot_numbers]
        for robot in sample_robots:
            DBSession.add(robot)
        sample_matches = []
        for i in range(1, 40):
            robots = sample(robot_numbers, 6)
            sample_matches += [Match(number=i,
                                   r_1=robots[0], r_2=robots[1], r_3=robots[2],
                                   b_1=robots[3], b_2=robots[4], b_3=robots[5])]
        for match in sample_matches:
            DBSession.add(match)
        nyle = User(name='nyle', permission='lead_scout', password='Password')
        DBSession.add(nyle)
