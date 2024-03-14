from typing import Dict
from dataclasses import dataclass


@dataclass
class UserAccount:

    id: int | None
    first_name: str
    last_name: str
    email: str


class UserAccountNotFoundException(Exception):

    __user_id: int

    def __init__(self, user_id: int):
        self.__user_id = user_id


class UserAccountCollectionInterface:
    """Defines the interface for user account storage methods aka collections"""

    def add_or_update(self, user: UserAccount):
        pass

    def delete(self, user_id: int):
        pass

    def get(self, user_id: int):
        pass

    def update(self, user: UserAccount):
        pass


class InMemoryUserAccountCollection(UserAccountCollectionInterface):

    __users: Dict[int, UserAccount] = {}
    __next_id: int = 1

    def add_or_update(self, user: UserAccount):
        if user.id is None:
            user.id = self.__next_id
            self.__next_id += 1

        self.__users[user.id] = user

    def delete(self, user_id: int):
        if user_id not in self.__users:
            raise UserAccountNotFoundException(user_id)
        else:
            del self.__users[user_id]

    def get(self, user_id: int):
        if user_id not in self.__users:
            raise UserAccountNotFoundException(user_id)
        else:
            return self.__users[user_id]
