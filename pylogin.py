# Created by Aaron Caffrey
# License: GPLv3
from hashlib import sha512
from random import getrandbits
try:
    from time import process_time as current_time
except ImportError:
    from time import clock as current_time

class AuthException(Exception):
    def __init__(self, arg):
        super(AuthException, self).__init__(arg)
        self.arg = arg

class AlreadyLoggedIn(AuthException):
    pass

class UsernameAlreadyExists(AuthException):
    pass

class PasswordTooShort(AuthException):
    pass

class InvalidUsername(AuthException):
    pass

class PermissionError(Exception):
    pass

class InvalidPassword(AuthException):
    pass

class NotPermittedError(AuthException):
    pass

class NotLoggedInError(AuthException):
    pass

class LockDownError(AuthException):
    pass

class User(object):
    def __init__(self, username, password):
        '''Create a new user object. The password will be encrypted before storing'''
        _encryt_usr = (username + random_number).encode('utf-8')
        self.username = sha512(_encryt_usr).hexdigest()
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False
    def _encrypt_pw(self, password):
        '''Encrypt the password with the username and return the sha digest.'''
        hash_string = (self.username + password).encode('utf-8')
        return sha512(hash_string).hexdigest()
    def check_password(self, password):
        '''Return True if the password is valid for this user, false otherwise'''
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password
    def __dict__(self):
        pass

random_number = str(getrandbits(100000))

class Authenticator(object):
    def __init__(self):
        '''Construct an authenticator to manage user logging in and out'''
        self._users = dict()
        self._attempts = 1
        self._cur_time = str()
    def add_user(self, username, passwordd):
        '''Hash the username to be used as dict key'''
        current_usr = User(username, random_number).password
        if current_usr in self._users:
            raise UsernameAlreadyExists(username)
        if len(passwordd) < 6:
            raise PasswordTooShort(passwordd)
        self._users[current_usr] = User(username, passwordd)
    def delete_user(self, username, passwordd):
        current_usr = User(username, random_number).password
        if not self.is_logged_in(username):
            raise NotLoggedInError(username)
        if not self._users[current_usr].check_password(passwordd):
            raise InvalidPassword(passwordd)
        del self._users[current_usr]
    def is_logged_in(self, username):
        current_usr = User(username, random_number).password
        if current_usr in self._users:
            return self._users[current_usr].is_logged_in
        return False
    def login(self, username, passwordd):
        if self._attempts < 5:
            if self.is_logged_in(username):
                self._attempts += 1
                raise AlreadyLoggedIn(username)

            current_usr = User(username, random_number).password
            user = self._users.get(current_usr)
            if not user:
                self._attempts += 1
                raise InvalidUsername(username)
            if not user.check_password(passwordd):
                self._attempts += 1
                raise InvalidPassword(passwordd)
            user.is_logged_in = True
        else:
            if not self._cur_time:
                # strftime hardly depends on the system time
                # and thus makes it vulnerable, deprecated
                self._cur_time = str(current_time()).split('.')[0]
            if str(current_time()).split('.')[0] != self._cur_time:
                self._cur_time = str()
                self._attempts = 1
                self.login(username, passwordd)
            else:
                raise LockDownError("You've been locked down for a minute")

    def logout(self, username, passwordd):
        current_usr = User(username, random_number).password
        if not self.is_logged_in(username):
            raise NotLoggedInError(username)
        if not self._users[current_usr].check_password(passwordd):
            raise InvalidPassword(passwordd)
        self._users[current_usr].is_logged_in = False
    def __dict__(self):
        pass

class Auth(Authenticator):
    def __init__(self):
        super(Auth, self).__init__()
        self._permissions = dict()
    def add_permission(self, perm_name):
        '''Create a new permission that users can be added to'''
        if not perm_name in self._permissions:
            self._permissions[perm_name] = set()
        else:
            raise PermissionError("Permission '{}' Exists".format(perm_name))
    def permit_user(self, perm_name, username):
        '''Grant the given permission to the user'''
        current_usr = User(username, random_number).password
        perm_set = self._permissions.get(perm_name)
        if not perm_name in self._permissions:
            raise PermissionError("Permission '{}' does not exists"
                .format(perm_name))
        else:
            if not current_usr in self._users:
                raise InvalidUsername(username)
            perm_set.add(current_usr)
    def check_permission(self, perm_name, username):
        current_usr = User(username, random_number).password
        if not self.is_logged_in(username):
            raise NotLoggedInError(username)
        perm_set = self._permissions.get(perm_name)
        if not perm_name in self._permissions:
            raise PermissionError("Permission '{}' does not exists"
                .format(perm_name))
        else:
            if not current_usr in perm_set:
                raise NotPermittedError(username)
            else:
                return True
    def __dict__(self):
        pass