from dataclasses import dataclass


@dataclass
class UserAccount:
    """Represents a user account"""

    id: int
    first_name: str
    last_name: str
    email: str


class UserNotFoundException(Exception):

    __user_id: int

    def __init__(self, user_id: int):
        self.__user_id = user_id


class UserAccountCollectionInterface:
    """Defines the interface for user account storage methods aka collections"""

    def add(self, user: UserAccount):
        pass

    def delete(self, user_id: int):
        pass

    def get(self, user_id: int):
        pass

    def update(self, user: UserAccount):
        pass