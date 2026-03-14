Reproducibility
===============

Clinical trials require that randomization sequences can be reproduced for
auditing and regulatory review. This page explains how the system achieves
deterministic, reproducible assignments.

Random Number Generator
-----------------------

The system uses NumPy's **PCG64** generator, a modern, statistically robust
pseudorandom number generator. The generator is seeded once at study
initialization using the ``starting_seed`` parameter in the configuration
file.

.. code-block:: yaml

   "My Clinical Trial":
       starting_seed: 100
       # ...

Given the same seed, the same sequence of urn draws (and therefore treatment
assignments) will occur, provided participants arrive in the same order with
the same factor levels.

What Determines the Sequence
----------------------------

The assignment for participant *n* depends on:

1. **The seed** — set once in ``config.yaml``.
2. **The order of arrivals** — participant *n* consumes the *n*-th random
   draw from the generator.
3. **The factor levels** — these determine which urn is selected, and
   therefore which ball composition drives the draw.
4. **The urn state** — which reflects all prior assignments (balls added
   via ``alpha`` and ``beta`` after each draw).

If any of these differ between two runs, the sequences will diverge from
that point onward.

Reproducing a Study
-------------------

To reproduce the exact assignment sequence from a completed study:

1. Use the same ``config.yaml`` (same seed, treatments, factors, urn
   parameters).
2. Re-enter participants in the same order with the same factor levels.
3. Ensure no plugin modifies assignments differently.

The system stores every assignment in the database with a timestamp,
participant ID, factor levels, treatment arm, and the user or plugin that
triggered it. This audit trail can be exported via the CLI:

.. code-block:: bash

   urn -s "My Clinical Trial" export --output assignments.csv

Or via the REST API:

.. code-block:: bash

   curl "http://localhost:5000/study_participants?api_key=YOUR_KEY&study=My+Clinical+Trial"

Seed Selection
--------------

Choose a seed that is:

- **Documented** — record it in your study protocol before enrollment begins.
- **Unpredictable** — do not use simple values like ``0`` or ``1``. A large
  arbitrary integer (e.g., ``839217``) is sufficient.
- **Fixed** — never change the seed after enrollment starts. Doing so would
  break the reproducibility of all subsequent assignments.

.. warning::

   Changing the seed, urn parameters (``alpha``, ``beta``, ``w``), or the
   imbalance measure (``D``) mid-study will alter the assignment
   probabilities for all future participants and break reproducibility
   of the sequence.
