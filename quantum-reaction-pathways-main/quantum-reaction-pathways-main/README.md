Q-ENZYME : QUANTUM REACTION PATHWAY SCANNER

ABOUT

This project is an attempt to translate real world quantum physical laws into software so that chemical reaction pathways emerge from first principle quantum dynamics rather than from prior data heuristics or trained models.

The core idea is to represent an enzyme active site as an effective quantum system governed by a Hamiltonian. Time evolution of this Hamiltonian produces population flow between reactant transition and product states which can be interpreted as quantum reaction pathways.

Instead of predicting reactions from known examples this approach lets catalytic behavior arise directly from the underlying physics.


PHYSICS BASIS

Reaction dynamics are modeled using a discrete quantum basis corresponding to reactant transition region and product states. The Hamiltonian includes physically interpretable terms such as tunneling strength transition state stabilization product bias and environmental perturbation.

Quantum time evolution is performed to obtain state populations as a function of time. These populations represent how probability amplitude moves through the reaction coordinate which directly maps to reaction pathway efficiency.

This allows quantum effects such as tunneling coherent transfer and barrier reshaping to be captured in a simple but physically meaningful way.


Q-ENZYME 

A Q Enzyme is an abstract representation of an enzyme encoded as Hamiltonian parameters. Different parameter choices correspond to different catalytic behaviors.

Efficient enzymes inhibited enzymes and weak catalysts all emerge from the same physical model without changing the simulation method. This makes it possible to compare catalytic mechanisms using physics alone.


REAL WORLD MOTIVATION AND IMPACT

In drug discovery and enzyme design many candidate molecules must be tested to identify those that efficiently drive a desired reaction. Classical simulations are expensive and data driven models depend heavily on prior examples.

This software demonstrates how physics driven quantum simulation could be used to screen and compare catalytic candidates early in the pipeline. Even a simplified quantum model can reduce the search space by identifying promising mechanisms before costly experiments.

As quantum computing hardware matures the same approach can be extended toward larger and more realistic biochemical systems.


STATUS

This repository contains a working prototype focused on conceptual correctness and physical interpretability. It is not a full quantum chemistry engine but a demonstration of how reaction pathways can emerge from quantum dynamics encoded directly in software.

CLIMATE AWARE ENZYME STABILITY PREDICTOR (CAESP)

A CAESP module is included in the Streamlit UI as a second simulation option inside the Generate section. It evaluates how candidate enzyme Hamiltonians retain catalytic efficiency under climate-linked stressors:

- Heat (temperature)
- Drought intensity
- Salinity
- pH deviation

Each stressor contributes to an effective environment perturbation term in the Hamiltonian. The interface reports retained catalytic efficiency relative to baseline and plots reaction probability versus stress intensity for rapid simulation-first screening.

This provides an MVP workflow for testing whether enzyme variants remain functional before costly field trials.
