Author: David Ojeda
Email: david.ojeda.lopez@gmail.com


I. File list
------------
tournament.py 			Python implementation of the methods to access and query the database
tournament.sql			SQL initialization code to import from PostgreSQL
tournament_test.py 		Python test cases for the tournament.py methods
README.txt			This file
------------


II. Installation
------------
To run this application you must have installed a version of PostgreSQL (9.4.4 is preferable) and Python (2.7). You can download them from here: http://www.postgresql.org/download/ and here: https://www.python.org/downloads/ respectively. Also, a package for the integration between Python and the PostgreSQL database is needed. You can install it running: pip install psycopg2.

Unzip the contents into a known location. 
------------


III. Usage
------------
To test that the database is working properly, you should follow this steps:
	1. Open the command prompt.
	2. Move to the unzipped known location.
	3. Run the following commands:
		3.1. psql -U postgres -f tournament.sql
		3.2. python tournament_test.py

This will run a series of unit and integration tests to confirm that the database is working properly. After that you can connect to the database running: psql tournament. Then, you can create, read, update and delete at your will.
------------


IV. Comments
------------
Database supports the feature of giving a skipped round when there is an even number of players. This method is not tested on the tournament_test.py though
