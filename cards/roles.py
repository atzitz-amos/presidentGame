import enum


class Roles(enum.Enum):
    PRESIDENT = 0
    VICE_PRESIDENT = 1
    MERCHANT = 2
    SERVITOR = 3
    LABOURER = 4


class RolesHolder:

    def __init__(self, num_players):
        self.roles = []

        self.num_players = num_players
        self.used_roles = self._used_roles()

    def clear(self):
        self.roles = []

    def queue(self, player):
        self.roles.append(player)

        return self.used_roles[len(self.roles) - 1]

    def _used_roles(self):
        used = [Roles.PRESIDENT]
        if self.num_players == 3:
            used.append(Roles.MERCHANT)
        elif self.num_players == 4:
            used.append(Roles.VICE_PRESIDENT)
            used.append(Roles.SERVITOR)
        if self.num_players > 4:
            used.append(Roles.VICE_PRESIDENT)
            used.extend([Roles.MERCHANT] * (self.num_players - 4))
            used.append(Roles.SERVITOR)

        return used + [Roles.LABOURER]

    @property
    def PRESIDENT(self):
        return self.roles[0] if len(self.roles) > 0 else None

    @property
    def VICE_PRESIDENT(self):
        return self.roles[1] if len(self.roles) > 3 and Roles.VICE_PRESIDENT in self.used_roles else None

    @property
    def MERCHANT(self):
        if Roles.MERCHANT in self.used_roles and len(self.roles) > 2:
            boundaries = [1, -1]
            if Roles.VICE_PRESIDENT in self.used_roles:
                boundaries[0] = 2
            if Roles.SERVITOR in self.used_roles:
                boundaries[1] = -2
            return self.roles[boundaries[0]:boundaries[1]]

        return []

    @property
    def SERVITOR(self):
        return self.roles[-2] if len(self.roles) > 3 and Roles.SERVITOR in self.used_roles else None

    @property
    def LABOURER(self):
        return self.roles[-1] if len(self.roles) > 3 and Roles.VICE_PRESIDENT in self.used_roles else None
