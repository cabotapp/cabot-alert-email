Cabot Hipchat Plugin
=====

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by their user handle in a hipchat room.

## Installation
Enter the cabot virtual environment.
    $ pip install cabot-alert-hipchat
    $ foreman stop
Add cabot_alert_hipchat to the installed apps in settings.py
    $ foreman run python manage.py syncdb
    $ foreman start
