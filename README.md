# django-email-or-username

Example implementation of a django app with a custom auth backend that allows you to login with (case-insensitive!) email or username

Compatible with Django >= 1.8

[![Build Status](https://travis-ci.org/ScottyMJacobson/django-email-or-username.svg?branch=master)](https://travis-ci.org/ScottyMJacobson/django-email-or-username)
[![Coverage Status](https://coveralls.io/repos/ScottyMJacobson/django-email-or-username/badge.svg?branch=master&service=github)](https://coveralls.io/github/ScottyMJacobson/django-email-or-username?branch=master)

## The Code:

The "magic" (if you can call it that) happens in the `_lookup_user` method, called by `authenticate`.

This snippet:

```python
# backends.py, line 15
try:
    validate_email(username_or_email)
except ValidationError:
    # not an email
    using_email = False
else:
    # looks like an email!
    using_email = True
```
Uses Django's built-in `django.core.validators.validate_email()` method to see whether the email passes validation. The old validators were methods that returned `True`/`False`, but now they will raise an exception (`django.forms.ValidationError`) in the `False` case. We listen for this exception and set the `using_email` boolean accordingly.

We then check to see if the username or email inexactly matches (using the case-insensitive `iexact` filter) a username/email in the database:

```python
try:
    if using_email:
        user = User.objects.get(email__iexact=username_or_email)
    else:
        user = User.objects.get(username__iexact=username_or_email)
except User.DoesNotExist:
    return None
else:
	return user
```

We catch the exception if no such user exists, or return the user if we find it.


## Why?

I was confused by Django's insistence on case-sensitive usernames, and figured it'd be a good opportunity to learn more about Django's swappable backends. 
I came across [this snippet](https://djangosnippets.org/snippets/1590/), which had the good idea of using Django's built-in email regex (although it had an outdated import statement), and then the argument over [this ticket](https://code.djangoproject.com/ticket/2273) about case sensitivity in the Django wiki suggested the imatch filter. 
This should combine both suggestions!

## License

This is a hack, and I'm not sure how liability goes with this kind of thing, but usage is subject to the terms of the "LICENSE" file.
