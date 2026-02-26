import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from hamiltonians.qenzyme import QEnzyme


def _stress_to_env_scale(temperature_c, drought_index, salinity_psu, ph):
    """Map climate stressors to an effective Hamiltonian perturbation."""
    temp_component = max(0.0, (temperature_c - 25.0) / 25.0) * 0.35
    drought_component = drought_index * 0.25
    salinity_component = min(salinity_psu / 60.0, 1.0) * 0.25
    ph_component = min(abs(ph - 7.0) / 3.0, 1.0) * 0.15
    return min(temp_component + drought_component + salinity_component + ph_component, 1.0)


def _simulate_stress_profile(base_params, stress_levels, ph):
    product_prob = []
    times = np.linspace(0, 12, 300)

    for stress in stress_levels:
        temperature = 25 + 20 * stress
        drought = stress
        salinity = 50 * stress
        env_scale = _stress_to_env_scale(temperature, drought, salinity, ph)

        enzyme = QEnzyme(
            tunneling=base_params["tunneling"],
            bias=base_params["bias"],
            ts_stabilization=base_params["ts"],
            environment=base_params["env"] + env_scale * 0.5,
        )
        populations = enzyme.simulate(times)
        product_prob.append(populations[-1, 3])

    return np.array(product_prob)


def climate_page(key_prefix="caesp", show_header=True):
    if show_header:
        st.subheader("🌦️ Climate-Aware Enzyme Stability Predictor (CAESP)")

    st.caption(
        "Stress-test catalytic Hamiltonians against heat, drought, salinity, and pH "
        "shift to estimate retained reaction efficiency before field trials."
    )

    st.markdown("---")
    st.markdown("#### Enzyme Hamiltonian parameters")

    col_a, col_b = st.columns(2)
    with col_a:
        tunneling = st.slider("Tunneling strength", 0.1, 2.0, 1.0, key=f"{key_prefix}_tunneling")
        ts = st.slider(
            "Transition-state stabilization", 0.0, 1.0, 0.3, key=f"{key_prefix}_ts"
        )
    with col_b:
        bias = st.slider("Product stabilization", 0.0, 2.0, 1.0, key=f"{key_prefix}_bias")
        env = st.slider(
            "Baseline environmental perturbation", 0.0, 0.5, 0.1, key=f"{key_prefix}_env"
        )

    st.markdown("#### Climate stress scenario")

    col1, col2 = st.columns(2)
    with col1:
        temperature_c = st.slider("Temperature (°C)", 10, 55, 30, key=f"{key_prefix}_temp")
        drought_index = st.slider("Drought stress", 0.0, 1.0, 0.2, key=f"{key_prefix}_drought")
    with col2:
        salinity_psu = st.slider("Salinity (PSU)", 0, 60, 10, key=f"{key_prefix}_salinity")
        ph = st.slider("pH", 4.0, 10.0, 7.0, key=f"{key_prefix}_ph")

    env_scale = _stress_to_env_scale(temperature_c, drought_index, salinity_psu, ph)

    st.info(
        f"Derived stress perturbation scale: **{env_scale:.2f}** "
        "(added to the Hamiltonian environment term)."
    )

    if st.button("Run Climate Stability Simulation", type="primary", key=f"{key_prefix}_run"):
        times = np.linspace(0, 12, 300)

        stressed = QEnzyme(
            tunneling=tunneling,
            bias=bias,
            ts_stabilization=ts,
            environment=env + env_scale * 0.5,
        )

        baseline = QEnzyme(
            tunneling=tunneling,
            bias=bias,
            ts_stabilization=ts,
            environment=env,
        )

        stressed_pop = stressed.simulate(times)
        baseline_pop = baseline.simulate(times)

        retained_efficiency = 100 * (stressed_pop[-1, 3] / (baseline_pop[-1, 3] + 1e-9))

        st.metric(
            "Retained catalytic efficiency under climate stress",
            f"{retained_efficiency:.1f}%",
            delta=f"{(stressed_pop[-1, 3] - baseline_pop[-1, 3]):.3f} Δ product probability",
        )

        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.plot(times, baseline_pop[:, 3], label="Baseline product probability", linewidth=2)
        ax.plot(times, stressed_pop[:, 3], label="Stressed product probability", linewidth=2)
        ax.set_xlabel("Time")
        ax.set_ylabel("Product population |3⟩")
        ax.set_title("Catalytic pathway resilience under selected climate stress")
        ax.grid(alpha=0.25)
        ax.legend()
        st.pyplot(fig, use_container_width=True)

        stress_levels = np.linspace(0.0, 1.0, 25)
        profile = _simulate_stress_profile(
            {"tunneling": tunneling, "bias": bias, "ts": ts, "env": env},
            stress_levels,
            ph,
        )

        fig2, ax2 = plt.subplots(figsize=(8, 4.6))
        ax2.plot(stress_levels, profile, color="#47d7ac", linewidth=2.3)
        ax2.set_xlabel("Combined climate stress intensity")
        ax2.set_ylabel("Final product probability")
        ax2.set_title("Reaction probability vs climate stress (MVP CAESP curve)")
        ax2.grid(alpha=0.25)
        st.pyplot(fig2, use_container_width=True)
