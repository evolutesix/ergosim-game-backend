import unittest

from domain.accounts.user_account import UserAccount


class UserAccountTests(unittest.TestCase):
    def test_create(self):
        a: UserAccount = UserAccount(
            first_name="James",
            last_name="Cauwelier",
            email="james.cauwelier@something.com"
        )
        a.first_name = "ok"
        self.assertEqual(a.first_name, "James")


if __name__ == '__main__':
    unittest.main()
