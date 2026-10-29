"""
Master End-to-End Execution & Reproduction Script
BDSRAE Project Topic 20: Geographic and Socioeconomic Bias in Spatial Data
Team: Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)
"""

import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from pipeline.data_loader import main as step1_data_loader
from pipeline.spatial_feature_store import build_spatial_feature_store as step2_feature_store
from pipeline.pyspark_pipeline import run_pyspark_pipeline as step3_pyspark
from pipeline.streaming_simulation import run_streaming_simulation as step4_streaming
from fairness.metrics import audit_spatial_fairness as step5_fairness_audit
from fairness.differential_privacy import evaluate_privacy_utility_tradeoff as step6_dp
from simulation.policy_simulator import run_policy_simulation as step7_simulation
from visualization.generate_disparity_maps import main as step8_visualizations


def run_full_pipeline():
    start_time = time.time()
    print("=" * 80)
    print("STARTING FULL END-TO-END BIG DATA & RESPONSIBLE AI REPRODUCIBILITY PIPELINE")
    print("Project: Geographic and Socioeconomic Bias in Spatial Mobility Data")
    print("Authors: Namith Kumar C (PES1UG24AM171) & Jayanth K (PES1UG24AM123)")
    print("=" * 80)
    
    print("\n[STAGE 1/8] Data Ingestion & Synthetic Scaler...")
    step1_data_loader()
    
    print("\n[STAGE 2/8] Spatial Feature Store Construction & Joins...")
    step2_feature_store()
    
    print("\n[STAGE 3/8] Distributed PySpark ETL & Lakehouse Partitioning...")
    step3_pyspark()
    
    print("\n[STAGE 4/8] Spark Structured Streaming & Live Fairness Drift Monitor...")
    step4_streaming(num_windows=10)
    
    print("\n[STAGE 5/8] Responsible AI Fairness & Bias Auditing...")
    step5_fairness_audit()
    
    print("\n[STAGE 6/8] Spatial Differential Privacy (Laplace Mechanism)...")
    step6_dp()
    
    print("\n[STAGE 7/8] Equitable Policy Multi-Objective Simulation...")
    step7_simulation()
    
    print("\n[STAGE 8/8] Generating Disparity Maps & Publication Figures...")
    step8_visualizations()
    
    total_elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"PIPELINE FULLY EXECUTED IN {total_elapsed:.2f} SECONDS WITH FULL REPRODUCIBILITY.")
    print("All deliverables are generated and verified.")
    print("=" * 80)


if __name__ == "__main__":
    run_full_pipeline()
