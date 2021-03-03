This is a larger flask project with modules, blueprints, a config file, extended layouts in jinja, smart caching for static assets, imported jinja macros, a bootstrap responsive nav bar, a useful site-map, error pages, and some firebase/firestore hookups in it.

Plans for some localization with Flask BabelEx and more firestore auth setup.  Maybe a better Flask Admin or NoSql ORM to use with Firebase.  Maybe some WebSockets for interaction with the firebase streams.

Ignoring the firebase part, this is pretty close to what I like to start with for an SqlAlchemy Flask project.  Maybe drop the auth module and and the admin module and use Flask-Admin and Flask-Login and Flask-RBAC.

Hopefully it will be useful for your project.

Look at the README.md under `app/mod_todo_list/README.md` to get started with a `key.json` from Firebase.

Based on a few different examples:

# Larger Flask Project Organization

https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#larger-applications

https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints

# Firebase Examples

https://github.com/Rev0kz/Flask-Google

https://medium.com/google-cloud/building-a-flask-python-crud-api-with-cloud-firestore-firebase-and-deploying-on-cloud-run-29a10c502877

https://github.com/Timtech4u/flask-firestore

## To be included soonish

https://medium.com/@bobthomas295/client-side-authentication-with-python-firestore-and-firebase-352e484a2634

https://flask-rbac.readthedocs.io/en/latest/index.html

https://github.com/klokantech/flask-firebase

https://gist.github.com/Bob-Thomas/49fcd13bbd890ba9031cc76be46ce446

https://github.com/Selich/Pyrebase

https://raturi.in/blog/webpush-notification-using-python-and-flask/

https://bitbucket.org/joetilsed/firebase/src/master/

https://ai-facets.org/using-flask-jwt-with-flask-login/


# Firebase APIs for Python

https://googleapis.dev/python/firestore/latest/client.html

https://github.com/firebase/firebase-admin-python

https://github.com/firebase/quickstart-python/tree/master/messaging

# Firebase APIs for Web-UI

https://github.com/firebase/firebaseui-web#using-firebaseui-for-authentication