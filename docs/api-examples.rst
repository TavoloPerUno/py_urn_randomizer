Python API Examples
===================

This guide shows how to use the REST API from Python with the
`requests <https://docs.python-requests.org>`_ library.

.. contents:: On this page
   :local:
   :depth: 2

Setup
-----

.. code-block:: python

   import os
   import requests
   import pandas as pd
   from dotenv import load_dotenv

   load_dotenv()                       # reads .env in the project root
   API_KEY = os.environ["URN_API_KEY"]
   BASE_URL = "http://localhost:5000"   # change for production / Render

Get Study Configuration
-----------------------

Retrieve the study's treatments, factors, urn parameters, and seed.

.. code-block:: python

   response = requests.get(f"{BASE_URL}/study_config", params={
       "api_key": API_KEY,
       "study": "My Study",
   })
   config = response.json()

   # Inspect treatments and factors
   print(config["results"]["treatments"])   # e.g. ['Treatment A', 'Treatment B']
   print(config["results"]["D"])            # e.g. 'chisquare'

   # Build a quick factor-level table
   pd.DataFrame({
       k: pd.Series(v)
       for k, v in config["results"]["factors"].items()
   }).fillna("")

**Example response:**

.. code-block:: json

   {
     "message": "Success",
     "results": {
       "treatments": ["Treatment A", "Treatment B"],
       "factors": {
         "age_group": ["18-40", "41-65", "65+"],
         "sex": ["Male", "Female"]
       },
       "D": "chisquare",
       "alpha": 0,
       "beta": 1,
       "w": 1,
       "starting_seed": 100,
       "urn_selection": "method1"
     },
     "status": 200
   }

List Participants
-----------------

Fetch all randomized participants and load them into a DataFrame.

.. code-block:: python

   response = requests.get(f"{BASE_URL}/study_participants", params={
       "api_key": API_KEY,
       "study": "My Study",
   })
   data = response.json()

   df = pd.DataFrame(data["results"])
   print(f"{len(df)} participants randomized")
   df.head()

The response includes one row per participant with columns for the
assigned treatment (``trt``), factor levels (``f_``-prefixed), timestamp
(``datetime``), and the user who performed the randomization (``user``).

Randomize a Participant
-----------------------

Send a ``POST`` request with the participant ID and all factor levels.

.. code-block:: python

   # Use the factor levels from the config response
   factors = config["results"]["factors"]

   params = {
       "api_key": API_KEY,
       "study": "My Study",
       "id": "P042",
   }
   # Add one level per factor
   params["age_group"] = "18-40"
   params["sex"] = "Female"

   response = requests.post(f"{BASE_URL}/study_participants", params=params)
   result = response.json()

   assigned_treatment = result["results"][0]["trt"]
   print(f"Participant P042 assigned to: {assigned_treatment}")

**Example response:**

.. code-block:: json

   {
     "message": "Success",
     "results": [{
       "id": "P042",
       "f_age_group": "18-40",
       "f_sex": "Female",
       "trt": "Treatment A",
       "datetime": "2025-09-15 14:30:00",
       "user": "alice"
     }],
     "status": 200
   }

Batch Randomization
-------------------

Randomize several participants in a loop, collecting results into a
DataFrame.

.. code-block:: python

   import random

   records = []
   for i in range(10):
       params = {
           "api_key": API_KEY,
           "study": "My Study",
           "id": f"BATCH-{i:03d}",
       }
       # Pick a random level for each factor
       for factor, levels in factors.items():
           params[factor] = random.choice(levels)

       resp = requests.post(f"{BASE_URL}/study_participants", params=params)
       records.append(resp.json()["results"][0])

   df_batch = pd.DataFrame(records)
   print(df_batch[["id", "trt"]].to_string(index=False))

Error Handling
--------------

All endpoints return a ``status`` field in the JSON body. Check it to
handle errors gracefully.

.. code-block:: python

   response = requests.get(f"{BASE_URL}/study_participants", params={
       "study": "My Study",
       # no api_key — this will fail
   })
   data = response.json()

   if data["status"] != 200:
       print(f"Error {data['status']}: {data['message']}")

Common error codes:

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Status
     - Meaning
     - Fix
   * - ``400``
     - Missing study name or invalid factor values
     - Check required parameters
   * - ``401``
     - Missing or invalid API key
     - Verify ``URN_API_KEY``
   * - ``404``
     - Study not found in configuration
     - Check study name spelling
