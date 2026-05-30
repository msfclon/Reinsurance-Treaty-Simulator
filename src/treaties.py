"""
treaties.py
Módulo 2-4: Implementación de los tres tratados de reaseguro.

Tratados implementados:
- Cuota Parte (Quota Share)
- Exceso de Pérdida (Excess of Loss - XL)
- Stop-Loss Agregado (Aggregate Stop-Loss)
"""

import numpy as np


def apply_quota_share(
    S: np.ndarray,
    alpha: float = 0.40,
) -> dict:
    """
    Aplica un tratado de Cuota Parte sobre la pérdida agregada.

    Parámetros
    
    S     : pérdidas agregadas brutas (una por escenario)
    alpha : porcentaje cedido al reasegurador (default 40%)

    Retorna
    
    dict con:
        - retained  : pérdida retenida por la aseguradora
        - ceded     : pérdida cedida al reasegurador
        - alpha     : parámetro usado
    """

    if not 0 < alpha < 1:
        raise ValueError("alpha debe estar entre 0 y 1")

    retained = (1 - alpha) * S
    ceded = alpha * S

    return {
        "retained": retained,
        "ceded": ceded,
        "alpha": alpha,
    }
def apply_excess_of_loss(
    losses: np.ndarray,
    M: float = 100_000.0,
    L: float = 400_000.0,
) -> dict:
    """
    Aplica un tratado de Exceso de Pérdida (XL) sobre siniestros individuales.

    Parámetros
    
    losses : siniestros individuales (todos los de todos los escenarios)
    M      : retention limit (máximo que paga la aseguradora por siniestro)
    L      : límite de cobertura del reasegurador por siniestro

    Retorna
    
    dict con:
        - retained : pérdida retenida por siniestro
        - ceded    : pérdida cedida por siniestro
        - M        : parámetro usado
        - L        : parámetro usado
    """

    if M <= 0 or L <= 0:
        raise ValueError("M y L deben ser positivos")

    # Pérdida retenida por siniestro: min(Y_j, M)
    retained = np.minimum(losses, M)

    # Pérdida cedida por siniestro: min((Y_j - M)+, L)
    ceded = np.minimum(np.maximum(losses - M, 0), L)

    return {
        "retained": retained,
        "ceded"   : ceded,
        "M"       : M,
        "L"       : L,
    }
def apply_stop_loss(
    S: np.ndarray,
    D: float = 150_000.0,
    C: float = 300_000.0,
) -> dict:
    """
    Aplica un tratado de Stop-Loss Agregado sobre la pérdida agregada.

    Parámetros
    
    S : pérdidas agregadas brutas (una por escenario)
    D : deducible agregado (lo que siempre absorbe la aseguradora)
    C : límite de cobertura del reasegurador

    Retorna
    
    dict con:
        - retained : pérdida retenida por la aseguradora
        - ceded    : pérdida cedida al reasegurador
        - D        : parámetro usado
        - C        : parámetro usado
    """

    if D <= 0 or C <= 0:
        raise ValueError("D y C deben ser positivos")

    # Pérdida cedida: min((S-D)+, C)
    ceded = np.minimum(np.maximum(S - D, 0), C)

    # Pérdida retenida: S - cedido
    retained = S - ceded

    return {
        "retained": retained,
        "ceded"   : ceded,
        "D"       : D,
        "C"       : C,
    }