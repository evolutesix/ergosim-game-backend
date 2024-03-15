from abc import abstractmethod
from typing import Dict
from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy import String



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

    @abstractmethod
    def add_or_update(self, user: UserAccount) -> UserAccount:
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass

    @abstractmethod
    def get(self, user_id: int) -> UserAccount:
        pass


class InMemoryUserAccountCollection(UserAccountCollectionInterface):

    __users: Dict[int, UserAccount] = {}
    __next_id: int = 1

    def add_or_update(self, user: UserAccount) -> UserAccount:
        if user.id is None:
            user.id = self.__next_id
            self.__next_id += 1

        self.__users[user.id] = user
        return user

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


class Base(DeclarativeBase):
    pass


class UserAccountRecord(Base):

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"<UserAccountRecord(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})>"


class AlchemyUserAccountCollection(UserAccountCollectionInterface):

    @staticmethod
    def create(user_account: UserAccount) -> UserAccountRecord:
        record: UserAccountRecord = UserAccountRecord(
            first_name=user_account.first_name,
            last_name=user_account.last_name,
            email=user_account.email
        )
        if user_account.id is not None:
            record.id = user_account.id

        return record

    @staticmethod
    def hydrate(user_account_record: UserAccountRecord) -> UserAccount:
        return UserAccount(
            id=user_account_record.id,
            first_name=user_account_record.first_name,
            last_name=user_account_record.last_name,
            email=user_account_record.email
        )

    def setup(self):
        with Session(self.__engine) as session:
            UserAccountRecord.metadata.drop_all()
            UserAccountRecord.metadata.create_all(self.__engine)

    def __init__(self):
        self.__engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    def add_or_update(self, user: UserAccount) -> UserAccount:
        with Session(self.__engine) as session:
            record: UserAccountRecord = self.create(user)
            session.add(record)
            session.commit()
            return self.hydrate(record)

    def delete(self, user_id: int):
        with Session(self.__engine) as session:
            session.delete(UserAccountRecord(id=user_id))
            session.commit()

    def get(self, user_id: int) -> UserAccount:
        with Session(self.__engine) as session:
            record = session.get(UserAccountRecord, user_id)
            if record is None:
                raise UserAccountNotFoundException(user_id)
            else:
                return self.hydrate(record)