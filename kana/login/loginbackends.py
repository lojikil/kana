import anydbm
from sqlalchemy import select
from model import users
from hashlib import sha256
from kana.util.timestamp import generate_datetimestamp


class Backend(object):

    def check_credentials(self, user, password):
        raise NotImplementedError


class SQLBackend(Backend):

    def set_engine(self, engine):
        self.engine = engine

    def update_credentials(self, user, password, username):
        """Update a user's information, including password, &c..

        Args:
            user (str): the user's username.
            password (str): the user's
            username (str): the user's display name (e.g. Stefan Edwards).

        Return:
            bool. True means success, False unsucess.

        """

        try:
            timestamp = generate_datetimestamp()
            salt = timestamp + user
            m = sha256()
            m.update(salt + password)

            for i in range(0, 4096):
                hres = m.hexdigest()
                m.update(hres)

            hpass = m.hexdigest()

            update([users]).where(users.c.user == user).values(
                  salt=timestamp,
                  password=hpass,
                  username=username)
            return True
        except:
            return False

    def check_credentials(self, user, password):
        """A simple function to check a user's credentials against the database.

        Args:
            user (str): the user's username.
            password (str): the user's (unencrypted, unhashed) password.

        Returns:
            int. The return code::

                >= 0 -- Success, integer is the user's UID
                -1 -- user not found or password does not match

        Checks the user's credentials against those stored in the database;
        since this uses iterated & salted SHA256 to store the user's pass,
        we have to retrieve the user's salt (generally a time-stamp string),
        append the user's username, and then iterate through the hashing
        process."""

        conn = self.engine.connect()
        query = select([users]).where(users.c.user == user)
        res = conn.execute(query)
        data = res.fetchone()
        conn.close()
        salt = data['salt'] + user
        m = sha256()

        m.update(salt + password)

        for i in range(0, 4096):
            hres = m.hexdigest()
            m.update(hres)

        if data:
            if m.hexdigest().upper() == data['password']:
                return data['id']
            else:
                return -1
        else:
            return -1


class DummyBackend(Backend):

    def check_credentials(self, user, password):
        return True


class FileBackend(Backend):

    def __init__(self, database="./data/users.db"):
        self.database = anydbm.open(database)

    def check_credentials(self, user, password):
        print ("FileBackend")
        if self.database[user] == password:
            return True
        return False

    def __del__(self):
        self.database.close()

    def __exit__(self):
        self.databse.close()
