from typing import Any, List, Type
import os

import pytest

from ergosim.backend.domain.user.account import (UserAccount,
                                                 InMemoryUserAccountCollection,
                                                 UserAccountNotFoundException,
                                                 UserAccountCollectionInterface,
                                                 AlchemyUserAccountCollection)


def is_integration_env() -> bool:
    return os.getenv('ERGOSIM_INTEGRATION_TESTING', '0') == '1'


def collection() -> List[Type[Any]]:
    """Returns the concrete implementation for the testing environment"""
    if is_integration_env():
        return [AlchemyUserAccountCollection]
    else:
        return [InMemoryUserAccountCollection]


class TestUserAccount:

    @pytest.fixture(params=collection())
    def accounts(self, request) -> UserAccountCollectionInterface:
        return request.param()

    @pytest.fixture(autouse=True)
    def setup(self, accounts: Any):
        self.__accounts: UserAccountCollectionInterface = accounts
        if isinstance(self.__accounts, AlchemyUserAccountCollection):
            self.__accounts.setup()
        self.__accounts.add_or_update(
            UserAccount(
                id=None,
                first_name="John",
                last_name="Wayne",
                email="john.wayne@something.com"
            )
        )

    def test_create(self, accounts: UserAccountCollectionInterface):
        sylvester = self.__accounts.add_or_update(
            UserAccount(
                id=None,
                first_name="Sylvester",
                last_name="Stallone",
                email="sylvester.stallone@something.com"
            )
        )

        assert sylvester.id == 2
        assert sylvester.first_name == "Sylvester"

    def test_update(self):
        john = self.__accounts.get(1)
        john.first_name = "Johnny"
        self.__accounts.add_or_update(john)
        john = self.__accounts.get(1)
        assert john.first_name == "Johnny"

    def test_delete(self):
        self.__accounts.delete(1)
        with pytest.raises(UserAccountNotFoundException):
            self.__accounts.get(1)
