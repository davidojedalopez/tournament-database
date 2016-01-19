[![Codacy Badge](https://api.codacy.com/project/badge/grade/004a38500bf04451bd81398662c9e3ea)](https://www.codacy.com/app/david-ojeda-lopez/tournament-database)

# Tournament Database :trophy:

## About

Python module that uses a PostgreSQL database to keep track of players and matches in a game tournament.

## File List

| File | Description |
|------|-------------|
| tournament.py | Python implementation of the methods to access and query the database |
| tournament_test.py | Python test cases for the tournament.py methods |
| tournament.sql | Sets up the database shcema |
| README.md | This file |

## Installation

To run this application you must have installed a version of PostgreSQL (9.4.4 is preferable) and Python (2.7). You can download them from here: [PostgreSQL][1] and here: [Python][2] respectively. Also, a package for the integration between Python and the PostgreSQL database is needed. You can install it running: `pip install psycopg2`.

## Usage

To test that the database is working properly, you should follow this steps:

1. Open the command prompt.
2. Move to the project root folder.
3. Run the following commands:
	- `psql -U postgres -f tournament.sql`
	- `python tournament_test.py`

This will run a series of unit and integration tests to confirm that the database is working properly. After that you can connect to the database running: `psql tournament`. Then, you can create, read, update and delete at your will.

## Comments

Database supports the feature of giving a skipped round when there is an even number of players. This method is not tested on the tournament_test.py though.

[1]: http://www.postgresql.org/download/
[2]: https://www.python.org/downloads/
