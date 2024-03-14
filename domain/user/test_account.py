import unittest

import pytest

from domain.user.account import UserAccount, InMemoryUserAccountCollection, UserAccountNotFoundException


@pytest.fixture(params=[InMemoryUserAccountCollection])
def accounts(request):
    return request.param()


class UserAccountTests(unittest.TestCase):

    def setUp(self):
        self.accounts = InMemoryUserAccountCollection()
        self.lookup = {
            "John Wayne": self.accounts.add_or_update(
                UserAccount(
                    id=None,
                    first_name="John",
                    last_name="Wayne",
                    email="john.wayne@something.com"
                )
            )
        }

    def test_create(self):
        john = self.accounts.get(self.lookup["John Wayne"])
        self.assertEqual(john.first_name, "John")

    def test_update(self):
        user_id = self.lookup["John Wayne"]
        john = self.accounts.get(user_id)
        john.first_name = "Johnny"
        self.accounts.add_or_update(john)
        john = self.accounts.get(user_id)
        self.assertEqual(john.first_name, "Johnny")

    def test_delete(self):
        self.accounts.delete(self.lookup["John Wayne"])
        with self.assertRaises(UserAccountNotFoundException):
            self.lookup["John Wayne"] = self.accounts.get(self.lookup["John Wayne"])


if __name__ == '__main__':
    unittest.main()
