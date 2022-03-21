from classic.http_auth import Group, Permission, strategies
import os

class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL, ))


dummy_strategy = strategies.Dummy(
    user_id=1,
    login='dummy',
    name='Admin dummy',
    groups=(Groups.ADMINS.name, ),
)

jwt_strategy = strategies.JWT(
    secret_key=str(os.getenv('SECRET_KEY'))
)

ALL_GROUPS = (Groups.ADMINS, )


