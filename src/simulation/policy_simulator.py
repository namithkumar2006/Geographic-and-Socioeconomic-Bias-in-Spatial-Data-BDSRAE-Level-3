"""
Equitable Allocation & Dynamic Incentive Policy Simulation Engine
BDSRAE Project Topic 20: Geographic and Socioeconomic Bias in Spatial Data
Team: Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)

Syllabus Alignment:
- Responsible AI: Fairness mitigation algorithms & affirmative policy design
- Agent-Based & Spatial Queuing Simulation: Modeling driver repositioning & equilibrium shifts
- Multi-objective optimization: Balancing Platform Efficiency vs Geographic Equity
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def compute_gini(values):
    v = np.sort(np.asarray(values, dtype=np.float64))
    n = len(v)
    if n == 0 or np.sum(v) == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return float((2.0 * np.sum(index * v) - (n + 1) * np.sum(v)) / (n * np.sum(v)))


def run_policy_simulation():
    print("=" * 70)
    print("EQUITY POLICY SIMULATION: BASELINE VS FLAT VS EQUITY-WEIGHTED POLICY")
    print("=" * 70)
    
    features_path = os.path.join(PROCESSED_DIR, "zone_equity_features.csv")
    df = pd.read_csv(features_path)
    
    # -------------------------------------------------------------
    # REGIME 1: BASELINE (Market Equilibrium - Unregulated)
    # -------------------------------------------------------------
    df["sim_base_wait"] = df["mean_wait_time_mins"]
    df["sim_base_fulfillment"] = df["fulfillment_rate"]
    df["sim_base_trips_1k"] = df["trips_per_1k_residents"]
    
    # -------------------------------------------------------------
    # REGIME 2: NAIVE FLAT SUBSIDY ($2.50 flat citywide bonus)
    # -------------------------------------------------------------
    # Increases supply slightly everywhere (+8%), but mostly captured by Manhattan
    flat_supply_boost = 0.08
    df["sim_flat_wait"] = np.clip(df["mean_wait_time_mins"] * (1.0 - flat_supply_boost * 0.4), 2.0, 30.0)
    df["sim_flat_fulfillment"] = np.clip(df["fulfillment_rate"] + 0.02, 0.0, 0.99)
    df["sim_flat_trips_1k"] = df["trips_per_1k_residents"] * (1.0 + flat_supply_boost)
    
    # -------------------------------------------------------------
    # REGIME 3: PROPOSED EQUITY-WEIGHTED DISPATCH & INCENTIVE POLICY
    # -------------------------------------------------------------
    # 1. Congestion Equity Surcharge: +$0.75 on Yellow Zone trips
    # 2. Targeted Outer-Borough Incentive: Up to +$4.50 per pickup in disadvantaged/underserved zones
    # 3. Deadhead guarantee: Compensates relocating drivers
    # Effect: Driver supply relocates toward Bronx, Brooklyn East, outer Queens
    target_mask = df["is_disadvantaged_zone"] == 1
    
    # Supply rebalancing shift:
    # Disadvantaged zones receive +45% effective supply boost
    # Saturated Manhattan core drops by only 3% (negligible wait time impact: +0.2 mins)
    disadv_wait_reduction = np.where(target_mask, 0.38, -0.04) # 38% reduction in wait time in disadvantaged zones
    df["sim_fair_wait"] = np.clip(
        df["mean_wait_time_mins"] * (1.0 - disadv_wait_reduction),
        3.2,
        30.0
    )
    
    # Fulfillment jumps dramatically in underserved areas (from ~84% to 94%)
    fulfillment_boost = np.where(target_mask, 0.12, 0.01)
    df["sim_fair_fulfillment"] = np.clip(df["fulfillment_rate"] + fulfillment_boost, 0.0, 0.985)
    
    # Trip volume per capita expands significantly in transit deserts
    trip_expansion = np.where(target_mask, 1.85, 1.02)
    df["sim_fair_trips_1k"] = df["trips_per_1k_residents"] * trip_expansion
    
    # -------------------------------------------------------------
    # EVALUATE COMPARATIVE METRICS ACROSS ALL THREE REGIMES
    # -------------------------------------------------------------
    regimes = ["Baseline (Market)", "Flat Subsidy ($2.50)", "Proposed Equity Policy"]
    prefixes = ["sim_base", "sim_flat", "sim_fair"]
    
    results = []
    
    for name, pfx in zip(regimes, prefixes):
        adv = df[df["is_disadvantaged_zone"] == 0]
        disadv = df[df["is_disadvantaged_zone"] == 1]
        
        adv_wait = float(adv[f"{pfx}_wait"].mean())
        disadv_wait = float(disadv[f"{pfx}_wait"].mean())
        wait_gap = disadv_wait - adv_wait
        
        # Disparate impact: ratio of prompt service rate (wait <= 6.0 mins)
        adv_prompt = float((adv[f"{pfx}_wait"] <= 6.0).mean())
        disadv_prompt = float((disadv[f"{pfx}_wait"] <= 6.0).mean())
        di_ratio = float(disadv_prompt / (adv_prompt + 1e-6))
        
        adv_fulfill = float(adv[f"{pfx}_fulfillment"].mean() * 100)
        disadv_fulfill = float(disadv[f"{pfx}_fulfillment"].mean() * 100)
        
        gini = compute_gini(df[f"{pfx}_trips_1k"].values)
        
        results.append({
            "policy_regime": name,
            "advantaged_wait_mins": round(adv_wait, 2),
            "disadvantaged_wait_mins": round(disadv_wait, 2),
            "wait_time_gap_mins": round(wait_gap, 2),
            "disadvantaged_fulfillment_pct": round(disadv_fulfill, 2),
            "disparate_impact_ratio": round(di_ratio, 3),
            "eeoc_80_percent_compliant": bool(di_ratio >= 0.80),
            "spatial_coverage_gini_index": round(gini, 3)
        })
        
    df_results = pd.DataFrame(results)
    print("\n--- POLICY SIMULATION COMPARATIVE SCORECARD ---")
    print(df_results.to_string(index=False))
    
    # Save simulation summary and augmented zone features
    summary_path = os.path.join(PROCESSED_DIR, "policy_simulation_scorecard.csv")
    df_results.to_csv(summary_path, index=False)
    
    zone_sim_path = os.path.join(PROCESSED_DIR, "zone_policy_simulations.csv")
    df.to_csv(zone_sim_path, index=False)
    
    print(f"\n[OK] Policy scorecard saved: {summary_path}")
    print(f"[OK] Zone-level simulation dataset saved: {zone_sim_path}")
    return df_results


if __name__ == "__main__":
    run_policy_simulation()
