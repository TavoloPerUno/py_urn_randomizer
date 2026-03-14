Plugin System
=============

The plugin system lets you override or modify the default urn randomization
logic for specific scenarios. Plugins are standard Python modules placed in
the ``plugins/`` directory at the project root.

How Plugins Work
----------------

After the urn randomization algorithm assigns a treatment, the system checks
for plugins. If a plugin is registered, it receives the study object and the
participant (with the preliminary assignment) and can modify the assignment
before it is saved.

The plugin is called **after** the urn draw but **before** the result is
persisted, so you can override the treatment arm, change the recording user,
or apply conditional business rules.

Writing a Plugin
----------------

A plugin is a Python file in the ``plugins/`` directory with two required
components:

1. A module-level ``service`` string that names the plugin.
2. A ``randomize(study, participant)`` function that receives the study and
   participant objects and returns the (possibly modified) participant.

Minimal Example
^^^^^^^^^^^^^^^

.. code-block:: python

   # plugins/my_rule.py

   service = "my_rule"

   def randomize(study, participant):
       """Override assignment under specific conditions."""
       # Example: cap Treatment A at 50 participants
       history = study.export_history()
       count_a = (history["trt"] == "Treatment A").sum()
       if participant.trt == "Treatment A" and count_a >= 50:
           participant.trt = "Treatment B"
           participant.user = service
       return participant

Real-World Example
^^^^^^^^^^^^^^^^^^

The included ``tues_asgmt.py`` plugin demonstrates a date-based override.
On Tuesdays, if more than three participants have already been assigned to
the MART arm that day, subsequent MART assignments are redirected to RMC-Q:

.. code-block:: python

   from datetime import datetime
   import pandas as pd
   import pytz

   service = "tues_asgmt"
   tzone = pytz.timezone("America/Chicago")

   def randomize(study, participant):
       if study.study_name == "CHS JCOIN HUB":
           if datetime.now(tzone).weekday() == 1:  # Tuesday
               if participant.trt == "MART":
                   history = study.export_history()
                   # ... filter to today's MART assignments ...
                   if today_mart_count >= 3:
                       participant.trt = "RMC-Q"
                       participant.user = service
       return participant

Plugin API Reference
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Object
     - Description
   * - ``study.study_name``
     - The name of the current study (string).
   * - ``study.export_history()``
     - Returns a DataFrame of all past assignments with columns:
       ``id``, ``trt``, ``datetime``, ``user``, and one column per factor.
   * - ``participant.trt``
     - The treatment arm assigned by the urn draw. Writable.
   * - ``participant.user``
     - The user who triggered the randomization. Writable (set to your
       ``service`` name when overriding).

Guidelines
----------

- Keep plugin logic simple and testable. Complex rules increase the risk
  of unintended assignment patterns.
- Always set ``participant.user = service`` when you override an assignment
  so the audit trail shows which plugin made the change.
- Plugins cannot prevent a randomization from being recorded. If you need
  to reject a participant, raise an exception.
- Only one plugin can be active at a time. If multiple files exist in
  ``plugins/``, behavior is undefined.
