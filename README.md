# Pasf

## Installation

1. Download [postgresql](https://www.postgresql.org/download/), install pgadmin as well to make things easier.
2. Open pgadmin.
3. Right click on login/group roles and create a new user.
4. Name this user `pasf`, set a password `test` and enable can `Can Login?` under privileges.
5. Right click on databases and create a database called `pasf`.
6. Right click on the newly created database and click on `Query Tool`.
7. Copy paste the [schema](./db/schema.sql) into the query tool and execute it.
8. Make sure your psql database is running on port 5432 (this should be the default).
9.  Follow the [api instructions](./api/) in the README to get the API up and running.
10. [Frontend WIP...](./web/).
