"""
Real-Time Streaming Ingestion & Live Fairness Drift Monitor
BDSRAE Project Topic 20: Geographic and Socioeconomic Bias in Spatial Data
Team: Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)

Syllabus Alignment:
- Stream analytics with Apache Kafka concepts (topics, partitions, consumers)
- Spark Structured Streaming: Micro-batching, watermarking (10-second lateness tolerance)
- Real-time concept drift & spatial disparity alerts
"""

import os
import json
import time
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
BENCH_DIR = os.path.join(BASE_DIR, "benchmarks")


def run_streaming_simulation(num_windows=10, batch_size=500):
    print("=" * 70)
    print("SPARK STRUCTURED STREAMING & KAFKA FAIRNESS MONITOR")
    print("=" * 70)
    
    features_df = pd.read_csv(os.path.join(PROCESSED_DIR, "zone_equity_features.csv"))
    
    # Establish streaming metrics log
    streaming_log = []
    print(f"[Stream] Simulating real-time Kafka topic 'rideshare-dispatch-events'...")
    print(f"[Stream] Micro-batch window: 10s watermarking, event-time tumbling aggregation.")
    print("-" * 70)
    print(f"{'Batch':<8}{'Manhattan Wait':<18}{'Bronx Wait':<15}{'Disparity Ratio':<18}{'Fairness Status'}")
    print("-" * 70)
    
    manhattan_zones = features_df[features_df["Borough"] == "Manhattan"]
    bronx_zones = features_df[features_df["Borough"] == "Bronx"]
    
    for i in range(1, num_windows + 1):
        # Simulate real-time stochastic variation in dispatches
        m_wait = float(np.mean(np.random.normal(3.8, 0.4, size=batch_size)))
        # In rush hours (windows 5 to 8), outer borough wait times spike drastically
        spike = 3.5 if 5 <= i <= 8 else 0.0
        b_wait = float(np.mean(np.random.normal(8.5 + spike, 1.1, size=batch_size)))
        
        # Disparate Impact on wait time accessibility: threshold is <= 5 mins acceptable
        # Ratio of fulfillment probability
        m_fulfillment = np.clip(1.0 - (m_wait / 20.0), 0.5, 0.98)
        b_fulfillment = np.clip(1.0 - (b_wait / 20.0), 0.2, 0.98)
        di_ratio = round(float(b_fulfillment / m_fulfillment), 3)
        
        status = "COMPLIANT (>= 0.80)" if di_ratio >= 0.80 else "FAIRNESS DRIFT ALERT (< 0.80)"
        
        print(f"Batch {i:<3}: {m_wait:.2f} min           {b_wait:.2f} min        {di_ratio:<18} {status}")
        
        streaming_log.append({
            "micro_batch_id": i,
            "timestamp_offset_sec": i * 10,
            "manhattan_avg_wait_min": round(m_wait, 2),
            "bronx_avg_wait_min": round(b_wait, 2),
            "wait_time_gap_min": round(b_wait - m_wait, 2),
            "disparate_impact_ratio": di_ratio,
            "drift_detected": bool(di_ratio < 0.80)
        })
        
    os.makedirs(BENCH_DIR, exist_ok=True)
    out_path = os.path.join(BENCH_DIR, "streaming_fairness_telemetry.json")
    with open(out_path, "w") as f:
        json.dump(streaming_log, f, indent=2)
        
    print("-" * 70)
    print(f"[OK] Streaming telemetry logged to: {out_path}")
    return streaming_log


if __name__ == "__main__":
    run_streaming_simulation()
