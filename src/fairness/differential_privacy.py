"""
Spatial Differential Privacy (Laplace Mechanism) Module
BDSRAE Project Topic 20: Geographic and Socioeconomic Bias in Spatial Data
Team: Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)

Syllabus Alignment:
- Responsible AI & Privacy: Differential Privacy (DP), Epsilon budgeting
- Protecting citizen pickup location trajectories from re-identification in small census zones
- Query release mechanisms: Laplace Mechanism with Global Sensitivity L1 = 1
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
BENCH_DIR = os.path.join(BASE_DIR, "benchmarks")


def laplace_dp_query(counts, epsilon=0.5, sensitivity=1.0):
    """
    Applies the classical Laplace Mechanism to release count queries with epsilon-DP.
    Noise ~ Laplace(scale = sensitivity / epsilon)
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(loc=0.0, scale=scale, size=len(counts))
    sanitized_counts = np.maximum(0, np.round(counts + noise)).astype(int)
    return sanitized_counts, noise


def evaluate_privacy_utility_tradeoff():
    print("=" * 70)
    print("SPATIAL DIFFERENTIAL PRIVACY AUDIT (LAPLACE MECHANISM)")
    print("=" * 70)
    
    features_path = os.path.join(PROCESSED_DIR, "zone_equity_features.csv")
    df = pd.read_csv(features_path)
    
    true_counts = df["total_trip_requests"].values
    
    epsilon_values = [0.1, 0.25, 0.5, 1.0, 2.0]
    dp_results = []
    
    print(f"{'Epsilon (eps)':<14}{'Privacy Guarantee':<20}{'Mean Abs Error (MAE)':<24}{'Relative Error (%)'}")
    print("-" * 70)
    
    for eps in epsilon_values:
        noisy_counts, noise = laplace_dp_query(true_counts, epsilon=eps, sensitivity=1.0)
        mae = float(np.mean(np.abs(noisy_counts - true_counts)))
        rel_error = float(np.mean(np.abs(noisy_counts - true_counts) / (true_counts + 1e-5)) * 100)
        
        guarantee = "Very High (Strict)" if eps <= 0.25 else ("Balanced" if eps <= 1.0 else "Relaxed")
        print(f"eps = {eps:<8} {guarantee:<20} {mae:<24.2f} {rel_error:.2f}%")
        
        dp_results.append({
            "epsilon": eps,
            "privacy_tier": guarantee,
            "mean_absolute_error_trips": round(mae, 2),
            "mean_relative_error_pct": round(rel_error, 2),
            "laplace_scale": round(1.0 / eps, 2)
        })
        
    os.makedirs(BENCH_DIR, exist_ok=True)
    out_file = os.path.join(BENCH_DIR, "differential_privacy_benchmarks.json")
    with open(out_file, "w") as f:
        json.dump(dp_results, f, indent=2)
        
    print("-" * 70)
    print(f"[OK] DP benchmarks saved to: {out_file}")
    return dp_results


if __name__ == "__main__":
    evaluate_privacy_utility_tradeoff()
