# nParseExtended for Project1999

Extended version of nParse with more functional custom triggers. Provides player location and spell tracking support for Project 1999 by reading the player log.

----

Running from source
========

Setup:

1. Create the directory where you would like nParse to be cloned to and then `cd` into the directory.
2. Clone the repository: `git clone https://github.com/WigF1/nparseextended.git .`  
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment: 
    - Windows: `.\venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
5. Install pip requirements: `pip install -r requirements.txt`
6. Install nParse: `pip install .`

Usage:

1. Activate the virtual environment: 
    - Windows: `.\venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
2. Run nParse: `python nparse.py`

----

Development
========

Setup:

1. Create the directory where you would like nParse to be cloned to and then `cd` into the directory.
2. Clone the repository: `git clone https://github.com/WigF1/nparseextended.git .`
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment: 
    - Windows: `.\venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
5. Install pip requirements: `pip install -r requirements-dev.txt`
6. Install nParse: `pip install -e .` (Note the -e, this puts the package into editable mode)
7. Run nParse: `python nparse.py`

Usage:

- Run Tests: `pytest.exe src/ tests/`
- Generate command line coverage report: `pytest --cov=src/ tests/`
- Generate HTML coverage report: `coverage html`

----

Building
========

Setup:

1. Create the directory where you would like nParse to be cloned to and then `cd` into the directory.
2. Clone the repository: `git clone https://github.com/WigF1/nparseextended.git .`
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment: 
    - Windows: `.\venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
5. Install pip requirements: `pip install -r requirements-build.txt`
6. Install nParse: `pip install .`

Usage:

1. Build nParse: `pyinstaller nparse_py.spec`
2. The compiled nParse executable will be in:
    - Windows: `builds\dist\nparse.exe`
    - Linux: `builds/dist/nparse`

----
