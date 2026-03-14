Glossary
========

.. glossary::
   :sorted:

   Adaptive biased coin design
      A randomization method where the probability of assigning a participant
      to a treatment arm changes based on existing imbalances. The urn model
      by Wei (1978) is one implementation.

   Imbalance measure
      A statistic that quantifies how uneven the treatment allocations are
      within a stratum. Supported measures are ``range``, ``variance``, and
      ``chisquare``. See :doc:`configuration` for details.

   Prognostic factor
      A baseline characteristic (e.g., age group, site, disease severity)
      used to stratify randomization so that treatment groups are balanced
      within each factor level.

   Stratum
      A subgroup defined by a specific combination of prognostic factor
      levels. For example, ``site=Site 1, sex=Male`` is one stratum. Each
      stratum maintains its own urn.

   Treatment arm
      One of the experimental conditions to which participants can be
      assigned (e.g., Treatment A, Placebo).

   Urn
      A conceptual container holding colored balls, one color per treatment
      arm. Drawing a ball determines the treatment assignment. After each
      draw, balls are added back according to the ``alpha`` and ``beta``
      parameters, shifting future probabilities toward balance.

   Urn randomization
      The randomization scheme described by Wei (1978) in which an urn
      model adaptively adjusts assignment probabilities to reduce treatment
      imbalance across prognostic factors.

   PCG64
      The pseudorandom number generator used by NumPy and this system.
      Given the same ``starting_seed``, the sequence of assignments is
      fully reproducible.

   API key
      A secret token assigned to each user that authenticates REST API
      requests. Generated automatically by the ``flask add_user`` command.

   Plugin
      A Python module in the ``plugins/`` directory that can override or
      modify treatment assignments after the urn draw. See :doc:`plugins`.
