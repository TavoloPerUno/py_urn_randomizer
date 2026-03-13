Configuration
=============

All study parameters are defined in a YAML configuration file (``config.yaml``
by default). The file path can be overridden with the ``URAND_CONFIG_FILE``
environment variable.

Study Definition
----------------

Each study is defined as a top-level key in the YAML file:

.. code-block:: yaml

   "My Clinical Trial":
       starting_seed: 100
       target_enrollment: 200

       treatments:
           - Treatment A
           - Treatment B
           - Placebo

       factors:
           site:
               ["Site 1", "Site 2", "Site 3"]
           age_group:
               ["18-40", "41-65", "65+"]
           sex:
               ["Male", "Female"]
           disease_severity:
               ["Mild", "Moderate", "Severe"]

Parameter Reference
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Default
     - Description
   * - ``treatments``
     - *(required)*
     - List of treatment arm names.
   * - ``factors``
     - *(required)*
     - Dictionary of prognostic factor names to their possible levels.
   * - ``starting_seed``
     - *(required)*
     - Seed for the NumPy PCG64 random number generator. Ensures
       reproducibility.
   * - ``w``
     - ``1``
     - Initial number of balls per treatment in each urn.
   * - ``alpha``
     - ``0``
     - Number of balls added for the **assigned** treatment after each draw.
   * - ``beta``
     - ``1``
     - Number of balls added for **unassigned** treatments after each draw.
   * - ``D``
     - ``chisquare``
     - Imbalance measure. Options: ``range``, ``variance``, ``chisquare``.
   * - ``urn_selection``
     - ``method1``
     - Method for selecting among strata urns. ``method1`` selects the urn
       with the largest imbalance.
   * - ``target_enrollment``
     - *none*
     - Optional total planned enrollment target. Enables the enrollment
       progress bar in the web dashboard.

Database
--------

The database connection string is set at the top level of the config file:

.. code-block:: yaml

   db: sqlite:///urn-randomization.db

Any SQLAlchemy-compatible connection string is accepted.

Environment Variables
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``URAND_CONFIG_FILE``
     - Path to the YAML config file (overrides default ``config.yaml``).
   * - ``URAND_STUDY_NAME``
     - Name of the study to load (must match a top-level key in the config).
   * - ``FLASK_SECRET_KEY``
     - Secret key for Flask session signing.
   * - ``GOOGLE_OAUTH_CLIENT_ID``
     - Google OAuth 2.0 client ID.
   * - ``GOOGLE_OAUTH_CLIENT_SECRET``
     - Google OAuth 2.0 client secret.
   * - ``DEMO_MODE``
     - Set to ``true`` to bypass OAuth and auto-login as a demo user.

How Urn Randomization Works
---------------------------

The urn randomization scheme (Wei, 1978) maintains a set of urns — one per
factor-level pair (e.g., one urn for ``sex=Male``, another for ``age_group=65+``).
Each urn contains colored balls representing treatment arms.

1. When a new participant arrives, their factor levels identify the relevant
   urns — one urn per factor-level pair.
2. An imbalance score *d* is computed for each matched urn using the configured
   measure (``D``).
3. The urn with the highest imbalance is selected (``urn_selection`` method).
4. A ball is drawn from that urn. Its color determines the treatment assignment.
5. The urn composition is updated: ``alpha`` balls of the assigned treatment
   and ``beta`` balls of each unassigned treatment are added back.

This adaptive mechanism naturally corrects imbalances: the most imbalanced
stratum drives the assignment, shifting probability toward underrepresented
arms across all relevant factor levels.

.. tip::

   For a two-arm trial with ``w=1``, ``alpha=0``, ``beta=1``, the scheme
   starts with equal probability and progressively favours the arm with
   fewer assignments — achieving good balance without being deterministic.
