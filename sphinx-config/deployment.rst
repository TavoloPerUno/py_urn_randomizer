Deployment
==========

The application can be deployed to any platform that supports Python WSGI
applications. This guide covers deployment to **Render** and general
production considerations.

Render
------

The repository includes a ``render.yaml`` blueprint for one-click deployment.

1. Fork or clone the repository to your GitHub account.
2. Create a new **Web Service** on `Render <https://render.com>`_ and connect
   it to your repository.
3. Set the following environment variables in the Render dashboard:

   .. list-table::
      :header-rows: 1
      :widths: 35 65

      * - Variable
        - Value
      * - ``FLASK_SECRET_KEY``
        - A random string (e.g., output of ``python -c "import secrets; print(secrets.token_hex(32))"``)
      * - ``URAND_CONFIG_FILE``
        - ``config-demo.yaml`` (or your own config file)
      * - ``URAND_STUDY_NAME``
        - Must match a top-level key in your config YAML
      * - ``DEMO_MODE``
        - ``true`` to bypass OAuth (demo only)
      * - ``GOOGLE_OAUTH_CLIENT_ID``
        - Your OAuth client ID (production)
      * - ``GOOGLE_OAUTH_CLIENT_SECRET``
        - Your OAuth client secret (production)

4. Render will automatically build and deploy. The start command is:

   .. code-block:: bash

      gunicorn urand_gui.app:app

Demo Mode
---------

Setting ``DEMO_MODE=true`` bypasses Google OAuth and automatically logs in
all visitors as a pre-seeded demo user. This is intended for public
demonstrations only — **do not use demo mode in production**.

To seed the demo database with sample participants:

.. code-block:: bash

   flask init-demo

This creates 25 participants with randomized factor levels and treatment
assignments, spread across several months for a realistic enrollment
timeline.

Production Considerations
-------------------------

- **Use a persistent database.** The default SQLite file is suitable for
  single-server deployments. For multi-server setups, use PostgreSQL.
- **Set a strong** ``FLASK_SECRET_KEY``.
- **Restrict OAuth users.** Only registered users (added via ``flask add_user``)
  can access the web interface.
- **Use HTTPS.** Platforms like Render provide this automatically.
- **Back up your database** regularly — it contains all randomization history.
