# Data Card & Datasheet for NYC Spatial Mobility & Socioeconomic Equity Datasets
**Project:** Geographic and Socioeconomic Bias in Spatial Mobility Data  
**Course:** Foundations of Big Data & Responsible AI Engineering (Topic 20)  
**Authors:** Namith Kumar C (`PES1UG24AM171`), Jayanth K (`PES1UG24AM123`)  
**Standard Compliance:** Gebru et al. (*Datasheets for Datasets*) & Mitchell et al. (*Model Cards for Model Reporting*)

---

## 1. Dataset Motivation
* **For what purpose was the dataset created?**  
  To empirically measure, benchmark, and mitigate geographic and socioeconomic bias in urban on-demand mobility and delivery services across New York City's 5 boroughs and 71 TLC Taxi Zones.
* **Who created the dataset?**  
  Compiled and synthesized by the research team using publicly available open government and spatial repositories:
  - New York City Taxi and Limousine Commission (NYC TLC Open Data)
  - United States Census Bureau (American Community Survey - ACS 5-Year Estimates)
  - OpenStreetMap (OSM) via Geofabrik spatial extracts
* **Who funded the creation of the dataset?**  
  Academic project conducted at PES University under the Foundations of Big Data & Responsible AI Engineering curriculum.

---

## 2. Composition & Data Schema
* **What do the instances that comprise the dataset represent?**  
  1. **Trip Records (`nyc_trips_scaled.csv` - 250,000 rows):** Individual on-demand dispatch logs including `trip_id`, `PULocationID`, `DOLocationID`, `pickup_hour`, `trip_distance_miles`, `wait_time_minutes`, `trip_duration_minutes`, `fare_amount`, `tip_amount`, `total_amount`, and `trip_status`.
  2. **Spatial Zone Lookup (`taxi_zone_lookup.csv` - 71 zones):** TLC Zone ID, Borough, Zone Name, Service Zone, Centroid Latitude, and Centroid Longitude.
  3. **Census Demographics (`nyc_census_acs_zones.csv` - 71 zones):** Median household income, poverty rate, minority population percentage, zero-car household percentage, total population, and transit dependence index.
  4. **OpenStreetMap Infrastructure (`nyc_osm_infrastructure.csv` - 71 zones):** Road network length (km), subway station counts, commercial POI counts, intersection density per sq km, and walkability scores.

* **Does the dataset contain all possible instances or is it a sample?**  
  Represents a scaled, statistically balanced 250,000-trip cohort across peak and off-peak travel periods reflecting empirically validated NYC TLC trip distribution and spatial queuing behaviors.

* **Are there sensitive attributes or personal data included?**  
  **No.** In strict adherence to Responsible AI and project guidelines:
  - **Zero Personally Identifiable Information (PII):** No passenger names, driver IDs, credit card details, IP addresses, or exact GPS trajectories.
  - Aggregated strictly at the spatial TLC Taxi Zone level (centroid coordinates).
  - Further protected via **$\epsilon$-Differential Privacy (Laplace Mechanism)** for public query release.

---

## 3. Collection & Synthesis Methodology
* **How was the data acquired or generated?**  
  - Real TLC Taxi Zone lookup tables and spatial centroid definitions were mapped to 2020 US Census PUMA and ACS economic tables.
  - OpenStreetMap Overpass API features were extracted for transportation network metrics (transit stops, road density).
  - Spatial queuing and market equilibrium algorithms synthesized trip dispatch logs calibrated against empirical NYC TLC trip frequency, driver concentration in commercial hubs, and outer-borough dispatch friction.

* **What preprocessing was performed?**  
  - Data cleaning to eliminate impossible spatial coordinates and invalid durations.
  - Feature normalization for per-capita metrics ($\text{Trips} / 1,000\text{ residents}$).
  - Construction of the unified spatial equity feature store (`zone_equity_features.csv`).

---

## 4. Uses & Intended Applications
* **What are the intended uses?**  
  - Academic research on algorithmic fairness in spatial queuing systems.
  - Benchmarking Big Data distributed pipelines (PySpark, Lakehouse, Spark Structured Streaming).
  - Policy simulation for transportation regulators (e.g., NYC TLC, transit authorities) seeking to audit algorithmic dispatch systems for compliance with civil rights statutes (EEOC 80% Rule, Title VI, NYC Local Law 144).

* **What are the out-of-scope or prohibited uses?**  
  - **Do NOT** use to target individual driver earnings, blacklist low-income neighborhoods, or justify discriminatory redlining.
  - **Do NOT** use without differential privacy noise addition when operating on small demographic slices.

---

## 5. Distribution & Licensing
* **How is the dataset distributed?**  
  Hosted directly inside the reproducibility repository under the `data/` directory.
* **What is the license?**  
  - NYC Open Data Terms of Use (Public Domain).
  - OpenStreetMap Open Database License (ODbL).
  - Code & Derivatives: MIT License.

---

## 6. Maintenance & Governance
* **Who maintains the dataset?**  
  Namith Kumar C (`PES1UG24AM171`) & Jayanth K (`PES1UG24AM123`).
* **Governance & Errata:**  
  Any corrections or schema evolutions are tracked in git commits with OpenLineage and Lakehouse versioning principles.
