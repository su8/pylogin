Login module for your python app. The usernames, passwords, username dict keys are stored as sha512 hash values. Only the person that has been added,logged in or has the right permission can operate the given user.
Automated lockdown is activated for 1 minute if you failed to login after 4 attempts. After that minute of lockdown you are allowed to try again, made that to restrict brute forcing programs.
Avoid using weak passwords and or usernames that can be compromised in brute-force attack. For example, John the Ripper cracked the hash value of 'hello' for less than a second, while it couldn't crack 'whatabia7*&ch'
The hash values aren't bulletproof but at least provide some basic protection from prying eyes.

## Requirements:
* python 2 or 3

## Installation:

    sudo python2 setup.py install

or

    sudo python3 setup.py install

## Usage:

```python
>>> import pylogin   # the module itself
>>> auth = pylogin.Auth()
>>> auth.add_user('myusername', 'password')
>>> auth.add_permission('test')
>>> auth.login('myusername', 'eqwewq')
Traceback (most recent call last):
    raise InvalidPassword(username, password)
InvalidPassword: ('myusername', 'eqwewq')
>>> auth.login('myusername', 'password')
True
>>> auth.is_logged_in('myusername')
True
>>> auth.check_permission('test', 'myusername')
Traceback (most recent call last):
    raise NotPermittedError(username)
NotPermittedError: ('myusername')
>>> auth.permit_user('test321', 'myusername')
Traceback (most recent call last):
    raise PermissionError("Permission does not exists")
PermissionError: Permission does not exists
>>> auth.permit_user('test', 'myusername')
>>> auth.check_permission('test', 'myusername')
True
>>> auth.add_user('user2', 'pass')
Traceback (most recent call last):
    raise PasswordTooShort(username)
login.PasswordTooShort: ('user2')
>>> auth.add_user('user2', 'password2')
>>> auth.add_user('myusername', 'password')
Traceback (most recent call last):
    UsernameAlreadyExists: ('myusername')
>>> auth.logout('myusername', 'password')
True
>>> # login 'myusername' and then delete 'myusername'
>>> auth.delete_user('myusername', 'password')
Traceback (most recent call last):
    raise InvalidUsername(username)

```
## Integration in your program

```python
>>> import pylogin
>>> auth = pylogin.Auth()
>>> auth.add_user('user1', 'userpassword')
>>> auth.add_permission('test program')
>>> auth.add_permission('change program')
>>> auth.permit_user('test program', 'user1')
>>> auth.permit_user('change program', 'user1')
>>> class MyApp(object):
    def __init__(self):
        self.username = None
        self.menu_map = {
            "login": self.login,
            'test': self.test,
            'change': self.change,
            'quit': self.quit
            }
    def login(self):
        logged_in = False
        while not logged_in:
            username = input('username: ')
            password = input('password: ')
            try:
                logged_in = auth.login(
                    username, password)
            except InvalidUsername:
                print('Sorry, that username does not exists')
            except InvalidPassword:
                print('Sorry, incorrect Password')
            else:
                self.username = username
    def is_permitted(self, permission):
        try:
            auth.check_permission(
                permission, self.username)
        except NotLoggedInError as e:
            print('{} is not logged in'.format(e.username))
        except NotPermittedError as e:
            print('{} cannot {}'.format(
                e.username, permission))
            return False
        else:
            return True
    def test(self):
        if self.is_permitted('test program'):
            print('Testing program now')
    def change(self):
        if self.is_permitted('change program'):
            print('Changing program now...')
    def quit(self):
        raise SystemExit()
    def menu(self):
        try:
            answer = str()
            while True:
                print("""
Please Enter a command:
\tLoging\tLogin
\ttest\tTest the program
\tchange\tChange the program
\tquit\tQuit
""")
                answer = input('enter a command: ').lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print('{} is not a valid option'.format(
                        answer))
                else:
                    func()
        finally:
            print('Thank you for testing the login module')

            
>>> MyApp().menu()

```