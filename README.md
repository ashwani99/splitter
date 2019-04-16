# splitter

Splitter is bill splitting application. You can use this to split your expenses with friends. Currently the application is its initial stage.

# Features

See [feature issues](https://github.com/ashwani99/splitter/labels/enhancement) for current/upcoming features. Feel free to open a new issue if you want to suggest a feature request!

# Run Locally
To get up and running, follow the steps:
- Open up a terminal. Clone the repo
```bash
$ git clone https://github.com/ashwani99/splitter
```
- Change directory into the application directory.
```bash
$ cd splitter
```
- Create a virtual environment. This is optional but recommended. After creating and activating virtual environment, install the dependencies. Make sure you use Python 3 for all this tasks.
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
- Initiate required environment variables.
```bash
$ export FLASK_APP=splitter.py
$ export FLASK_DEBUG=1 # to work in debug mode 
```
Application specific variables `SPLITTER_SECRET`, `DATABASE_URL` have been initialised with default values but its recommened to override them.
- Run the app
```bash
$ flask run
```
That's it. The server address will be shown in the terminal console. By default Flask serves it at localhost at port 5000 i.e [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# Built With
- [Flask](http://flask.pocoo.org/) - The web framework used
- [SQLite](https://www.sqlite.org) - Database used

# License
MIT
