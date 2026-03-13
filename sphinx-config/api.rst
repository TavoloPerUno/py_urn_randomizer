REST API
========

The randomization service can be accessed programmatically via its HTTP API.
Authentication is handled via a user-specific **API key** provided by the
system administrator.

.. warning::

   Store your API key securely. It grants full access to randomize
   participants and read study data.

Endpoints
---------

.. autoflask:: urand_gui.app:app
   :endpoints: api_get_config, api_get_participants, api_randomize_participant

Examples
--------

Get Study Configuration
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   curl -s "http://localhost:5000/study_config?\
   api_key=YOUR_KEY&study=My+Study" | python -m json.tool

**Response:**

.. code-block:: json

   {
     "message": "Success",
     "results": {
       "factors": {
         "age_group": ["18-40", "41-65", "65+"],
         "sex": ["Male", "Female"]
       },
       "treatments": ["Treatment A", "Treatment B"],
       "D": "chisquare",
       "alpha": 0,
       "beta": 1,
       "w": 1
     },
     "status": 200
   }

List Participants
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   curl -s "http://localhost:5000/study_participants?\
   api_key=YOUR_KEY&study=My+Study" | python -m json.tool

Look up a specific participant:

.. code-block:: bash

   curl -s "http://localhost:5000/study_participants?\
   api_key=YOUR_KEY&study=My+Study&id=P001" | python -m json.tool

Randomize a Participant
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   curl -X POST "http://localhost:5000/study_participants?\
   api_key=YOUR_KEY&study=My+Study&id=P026&age_group=18-40&sex=Female&\
   disease_severity=Mild&prior_treatment=No"

**Response:**

.. code-block:: json

   {
     "message": "Success",
     "results": [{
       "id": "P026",
       "trt": "Treatment A",
       "age_group": "18-40",
       "sex": "Female",
       "disease_severity": "Mild"
     }],
     "status": 200
   }

Error Handling
--------------

All endpoints return a JSON object with ``message``, ``results``, and
``status`` fields. Common error codes:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Meaning
   * - ``400``
     - Missing required parameters or invalid factor values.
   * - ``401``
     - Invalid or missing API key.
   * - ``404``
     - Study name not found in configuration.
