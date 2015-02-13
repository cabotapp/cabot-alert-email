Cabot Email alert Plugin
=====

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by email.

## Installation
Enter the cabot virtual environment.
    $ pip install cabot-alert-hipchat
    $ foreman stop
Add cabot_alert_email to the installed apps in settings.py
    $ foreman run python manage.py syncdb
    $ foreman start
