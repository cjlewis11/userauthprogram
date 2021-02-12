# userauthprogram
A small Python based program that will allow a user to register an account, login to said account, and then logout. For webroot.

To maintain simplicty, Python3 was used to implement this program.

Requirements set forth that credentials should be stored locally. In order to meet this requirement, I assumed that no databases were allowed. I also avoided using a file system as my hashes where in byte format and wanted to spend time on the hashing and security rather than the file io of non-utf-8 bytes. This means that users only persistent for the session and then are removed.

Bcrypt's PBKDF2 Hashing is used to create cryptographically secure password hashes, and all passwords are salted with Bcrypts salt generator.
Each salt should be unique to the user preventing timing attacks.

Testing was done utilzing Pytest and MagicMock


To run:
  Ensure Python3 is installed. Python 3.6.9 was used to develop this.

  Create a virtual enviroment outside of the projet directory using:
    python -m venv env_name

  Activate said virtual enviroment with (on unix based system):
    source env_name/bin/activate

  Navigate to project root folder
    cd userauthprogram

  Install requirements from requirements.txt using pip
    pip install -r requirements.txt

  To run main program:
    python3 main.py

  To run testing enter command in root directory:
    pytest


If you have any question feel free to email me at lewis.cj11@gmail.com
