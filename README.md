# ILinkProj
SITP Project

##Documentation
[Requirements Document](https://github.com/HermanZzz/ILinkProj/blob/Dev/doc/Documentation.md)

##Getting Started

###Install Python

Python version 2.X is preffered, download from [python.org](https://www.python.org/downloads/).

Then, you can verify that Python is installed by typing `python` from your shell; you should see something like:

```bash
	Python 2.7.10 (v2.7.10:15c95b7d81dc, May 23 2015, 09:33:12) 
	[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
	Type "help", "copyright", "credits" or "license" for more 	information.
	>>> 
```

P.S. You may have another version of Python installed.

###Install Django 


1. Install [pip](https://pip.pypa.io/en/stable/).The easiest way is to use the [standalone pip installer](https://pip.pypa.io/en/latest/installing/#install-pip). 
2. *(not required) Take a look at [virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). These tools provide isolated Python environments, which are more practical than installing packages systemwide. They also allow installing packages without administrator privileges. 
3. After you’ve created and *activated a virtual environment, enter the command `pip install Django` at the shell prompt.

To verify that Django can be seen by Python, type `python` from your shell. Then at the Python prompt, try to import Django:

```bash
	>>> import django
	>>> print(django.get_version())
	1.9
```

P.S. You may have another version of Django installed.

###Run the Server

Open your shell and :

```bash
git clone git://github.com/HermanZzz/ILinkProj
cd ILinkProj/ILink
python manage.py runserver
```

If succeed, you should see something like:

```bash
Django version 1.9.3, using settings 'ILink.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

You can now open it by entering `//127.0.0.1:8000/` in your browser.