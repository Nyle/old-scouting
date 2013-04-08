# scouting/views/__init__.py

from .robot_views import (
    view_robot,
    edit_robot,
    add_robot,
    )

from .match_views import (
    view_match,
    add_match,
    edit_match,
    )

from .view_home import (
    view_home,
    )

from .security_views import (
    login,
    logout,
    add_user,
    reset_password,
    manage_user,
    manage_all_users,
    )
