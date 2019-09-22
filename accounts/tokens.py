from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
'''https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef'''

'''
PasswordResetTokenGenerator 
Django generate a token without persisting it in the database
et, it still have the capabilities of determining whether a given token is valid or not.
Also the token is only valid for a defined number of days.
The class have two public methods:
    * make_token(user)
    * check_token(user, token)
The make_token method will generate a hash value with user 
related data that will change after the password reset.
* make_token(user)
def _make_hash_value(self, user, timestamp):
    # Ensure results are consistent across DB backends
    login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
    return (
        six.text_type(user.pk) + user.password +
        six.text_type(login_timestamp) + six.text_type(timestamp)
    )
'''


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)
            +
                six.text_type(user.is_active)
                )
account_activation_token = TokenGenerator()