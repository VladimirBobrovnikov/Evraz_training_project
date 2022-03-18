from classic.http_auth import Group, Permission, strategies


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

ALL_GROUPS = (Groups.ADMINS, )
