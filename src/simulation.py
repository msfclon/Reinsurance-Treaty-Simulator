"""
Simulación de siniestros bajo el modelo colectivo de riesgo.
S = sum_{j=1}^{N} Y_j
donde N ~ Poisson(lambda) y Y_j ~ Pareto o Lognormal
"""

import numpy as np


def simulate_aggregate_losses(
    n_simulations: int = 100_000,
    lam: float = 50.0,
    severity: str = "pareto",
    pareto_alpha: float = 1.5,
    pareto_xm: float = 1_000.0,
    lognormal_mu: float = 8.0,
    lognormal_sigma: float = 1.5,
    random_seed: int = 42,
) -> np.ndarray:
    """
    Simula n_simulations realizaciones de la pérdida agregada S.

    Parámetros
    
    n_simulations : número de escenarios simulados
    lam           : media de la Poisson (frecuencia esperada de siniestros)
    severity      : 'pareto' o 'lognormal'
    pareto_alpha  : parámetro de forma de Pareto 
    pareto_xm     : parámetro de escala de Pareto 
    lognormal_mu  : media del logaritmo
    lognormal_sigma: desviación estándar del logaritmo
    random_seed   : semilla para reproducibilidad
    """

    rng = np.random.default_rng(random_seed)

    # Paso 1: simular frecuencia N ~ Poisson
    N = rng.poisson(lam=lam, size=n_simulations)

    # Paso 2: simular severidad y acumular por escenario
    S = np.zeros(n_simulations)

    for i, n in enumerate(N):
        if n == 0:
            S[i] = 0.0
            continue

        if severity == "pareto":
            # Pareto: Y = xm / U^(1/alpha), U ~ Uniform(0,1)
            U = rng.uniform(size=n)
            Y = pareto_xm / (U ** (1.0 / pareto_alpha))

        elif severity == "lognormal":
            Y = rng.lognormal(mean=lognormal_mu, sigma=lognormal_sigma, size=n)

        else:
            raise ValueError("severity debe ser 'pareto' o 'lognormal'")

        S[i] = Y.sum()

    return S