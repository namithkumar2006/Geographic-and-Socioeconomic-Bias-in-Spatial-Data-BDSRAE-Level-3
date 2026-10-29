"""
Spatial Feature Store & Aggregation Pipeline
BDSRAE Project Topic 20: Geographic and Socioeconomic Bias in Spatial Data
Team: Namith Kumar C (PES1UG24AM171), Jayanth K (PES1UG24AM123)
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CENSUS_DIR = os.path.join(BASE_DIR, "data", "census")
OSM_DIR = os.path.join(BASE_DIR, "data", "osm")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def build_spatial_feature_store():
    print("[...] Loading raw data files...")
    trips_df = pd.read_csv(os.path.join(RAW_DIR, "nyc_trips_scaled.csv"))
    zones_df = pd.read_csv(os.path.join(RAW_DIR, "taxi_zone_lookup.csv"))
    census_df = pd.read_csv(os.path.join(CENSUS_DIR, "nyc_census_acs_zones.csv"))
    osm_df = pd.read_csv(os.path.join(OSM_DIR, "nyc_osm_infrastructure.csv"))
    
    print(f"Loaded {len(trips_df):,} trips, {len(zones_df)} zones.")
    
    # Aggregations by Pickup Zone (PULocationID)
    agg_trips = trips_df.groupby("PULocationID").agg(
        total_trip_requests=("trip_id", "count"),
        completed_trips=("trip_status", lambda s: (s == "completed").sum()),
        unfulfilled_trips=("trip_status", lambda s: (s != "completed").sum()),
        mean_wait_time_mins=("wait_time_minutes", "mean"),
        median_wait_time_mins=("wait_time_minutes", "median"),
        p90_wait_time_mins=("wait_time_minutes", lambda x: np.percentile(x, 90)),
        mean_trip_distance=("trip_distance_miles", "mean"),
        mean_fare=("fare_amount", "mean"),
        mean_tip=("tip_amount", "mean"),
        mean_total_amount=("total_amount", "mean")
    ).reset_index().rename(columns={"PULocationID": "LocationID"})
    
    # Calculate fulfillment rate and rejection rate
    agg_trips["fulfillment_rate"] = agg_trips["completed_trips"] / agg_trips["total_trip_requests"]
    agg_trips["rejection_rate"] = agg_trips["unfulfilled_trips"] / agg_trips["total_trip_requests"]
    
    # Join with Zone Lookup metadata
    features_df = zones_df.merge(agg_trips, on="LocationID", how="left")
    
    # Join with Census ACS Demographics
    census_cols = ["LocationID", "median_household_income", "poverty_rate", 
                   "minority_population_pct", "zero_car_household_pct", 
                   "total_population", "transit_dependence_index"]
    features_df = features_df.merge(census_df[census_cols], on="LocationID", how="left")
    
    # Join with OSM spatial features
    osm_cols = ["LocationID", "road_length_km", "subway_station_count", 
                "commercial_poi_count", "intersection_density_per_sqkm", "walkability_score"]
    features_df = features_df.merge(osm_df[osm_cols], on="LocationID", how="left")
    
    # Compute normalized service coverage metrics
    # Trips per 1,000 residents
    features_df["trips_per_1k_residents"] = (
        features_df["total_trip_requests"] / features_df["total_population"]
    ) * 1000.0
    
    # Coverage Index: Ratio of trip requests to transit dependence
    # Higher value means high mobility supply relative to transit need
    features_df["service_adequacy_ratio"] = (
        features_df["trips_per_1k_residents"] / (features_df["transit_dependence_index"] + 1e-5)
    )
    
    # Binary classification of socioeconomically vulnerable zone:
    # Income below NYC median ($65,000) OR poverty rate > 25%
    nyc_median_income = features_df["median_household_income"].median()
    features_df["is_disadvantaged_zone"] = (
        (features_df["median_household_income"] < nyc_median_income) | 
        (features_df["poverty_rate"] > 0.25)
    ).astype(int)
    
    # Save the consolidated spatial feature store
    output_path = os.path.join(PROCESSED_DIR, "zone_equity_features.csv")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    features_df.to_csv(output_path, index=False)
    print(f"[OK] Saved unified spatial equity feature store: {output_path} ({len(features_df)} zones)")
    
    # Print summary statistics by borough
    borough_summary = features_df.groupby("Borough").agg(
        zones=("LocationID", "count"),
        avg_income=("median_household_income", "mean"),
        avg_wait_mins=("mean_wait_time_mins", "mean"),
        trips_per_1k=("trips_per_1k_residents", "mean"),
        fulfillment_pct=("fulfillment_rate", lambda x: np.mean(x) * 100)
    ).reset_index()
    
    print("\n--- Summary by Borough ---")
    print(borough_summary.to_string(index=False))
    return features_df


if __name__ == "__main__":
    build_spatial_feature_store()
