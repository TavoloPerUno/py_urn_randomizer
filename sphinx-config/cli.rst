CLI Reference
=============

The application provides two sets of CLI commands:

- **Flask commands** (``flask <command>``) — manage the web application's
  database and users.
- **Urn commands** (``urn <command>``) — interact directly with the
  randomization engine for scripting and batch operations.

Flask Commands
--------------

These commands manage the web application. Run them from the project root
with ``flask <command>``.

.. click:: urand_gui.cli:create_db
   :prog: flask createdb

.. click:: urand_gui.cli:add_user
   :prog: flask add_user

.. click:: urand_gui.cli:list_users
   :prog: flask list_users

.. click:: urand_gui.cli:delete_user
   :prog: flask delete_user

Urn Commands
------------

These commands interact directly with the randomization engine. They are
useful for scripting, batch operations, and data management.

.. click:: urand.cli:cli
   :prog: urn
   :show-nested:

Examples
--------

Set up a new study from scratch:

.. code-block:: bash

   # Initialize the database
   flask createdb

   # Add users
   flask add_user alice alice@hospital.org
   flask add_user bob bob@hospital.org

   # Randomize from the command line
   urn -s "My Study" randomize --id P001 --user alice

   # Export all participant data
   urn -s "My Study" export participants.csv

   # Seed a study with dummy data for testing
   urn -s "My Study" dummy_study --n_participants 50 --seed 42
