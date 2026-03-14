Why Urn Randomization?
======================

Complete randomization — flipping a fair coin for each participant —
is the simplest allocation method, but it provides no guarantee of
treatment balance, especially in small-to-moderate trials. Urn
randomization (Wei, 1978) adaptively adjusts allocation probabilities
to maintain balance while preserving the unpredictability needed to
prevent selection bias.

This page summarizes a Monte Carlo simulation comparing four
randomization strategies across 1,000 independent trials of 2,500
participants each with three treatment arms.

.. contents:: On this page
   :local:
   :depth: 2

Strategies Compared
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Strategy
     - Description
   * - **Complete Randomization**
     - Each participant is assigned to a treatment arm with equal probability
       (1/k), independent of prior assignments.
   * - **Urn (β=1, D=χ²)**
     - Wei's urn model with β=1 ball added for the non-assigned treatment
       after each draw. The imbalance metric D is the χ² statistic across
       arms.
   * - **Urn (β=1, D=range)**
     - Same as above, but the imbalance metric D is the range (max − min)
       of arm counts.
   * - **Urn (β=2, D=χ²)**
     - Stronger adaptive correction: β=2 balls added for the non-assigned
       treatment, making the urn pull more aggressively toward balance.

In all urn strategies, α=0 (no extra balls for the assigned treatment)
and w=1 (one initial ball per treatment).

How the Simulation Works
------------------------

For each of the 1,000 trials:

1. Initialize an urn with ``w`` balls per treatment arm.
2. For each of the 2,500 participants, draw from the urn to assign a
   treatment.
3. After each assignment, update the urn: add ``α`` balls for the assigned
   arm and ``β`` balls for all other arms.
4. After every assignment, record the maximum proportional imbalance
   across strata:

   .. math::

      d = \frac{\max_k n_k - \min_k n_k}{\sum_k n_k}

   where :math:`n_k` is the count assigned to arm *k*.

The simulation tracks this imbalance metric ``d`` at every enrollment
step across all 1,000 trials to compute means, confidence intervals, and
tail probabilities.

Results
-------

Treatment Imbalance Over Enrollment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mean maximum proportional imbalance ``d`` decreases as enrollment
grows. Urn strategies drive imbalance down faster than complete
randomization.

At small sample sizes (n < 50), complete randomization frequently
produces imbalances above 20%, while urn methods keep imbalance below
10% on average. The gap is largest in the critical early phase of a
trial when interim analyses are most sensitive to allocation imbalance.

Increasing β from 1 to 2 produces even tighter balance, at the cost of
slightly more predictable allocation sequences.

Tail Probabilities
^^^^^^^^^^^^^^^^^^

The fraction of trials where the maximum proportional difference exceeds
a given threshold provides a practical measure of risk:

.. list-table:: Fraction of trials with d ≥ 20% (at n = 100 participants)
   :header-rows: 1
   :widths: 40 30

   * - Strategy
     - Trials with d ≥ 20%
   * - Complete Randomization
     - ~35%
   * - Urn (β=1, D=χ²)
     - < 1%
   * - Urn (β=1, D=range)
     - < 1%
   * - Urn (β=2, D=χ²)
     - < 0.1%

At 100 participants, roughly one in three completely randomized trials
has a ≥ 20% imbalance, while urn randomization virtually eliminates
this risk.

Choice of Imbalance Metric (D)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two D metrics — χ² and range — produce similar results for two-arm
trials. With three or more arms, χ² is more sensitive to multiway
imbalance because it considers all arms simultaneously, while range only
looks at the gap between the largest and smallest arms.

Key Takeaways
-------------

1. **Urn randomization reduces imbalance** compared to complete
   randomization at every sample size, with the largest benefit at small n.

2. **The benefit is automatic** — no blocking or stratification scheme
   needs to be pre-specified. The urn adjusts continuously.

3. **Higher β values** produce tighter balance but increase the
   predictability of the next assignment. β=1 is a common practical
   choice that balances these concerns.

4. **Stratification multiplies the benefit** — applying urn randomization
   within each stratum (factor-level combination) maintains balance both
   overall and within subgroups defined by prognostic factors.

References
----------

- Wei, L.J. (1978). The Adaptive Biased Coin Design for Sequential
  Experiments. *Annals of Statistics*, 6(1), 92–100.
  `doi:10.1214/aos/1176344068 <https://doi.org/10.1214/aos/1176344068>`_

- Wei, L.J. (1978). An Application of an Urn Model to the Design of
  Sequential Experiments. *Journal of the American Statistical
  Association*, 73(363), 559–563.
  `doi:10.2307/2286597 <https://doi.org/10.2307/2286597>`_
