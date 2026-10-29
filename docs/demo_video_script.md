# 3-Minute Demo Video Script & Storyboard
**Project:** Geographic and Socioeconomic Bias in Spatial Mobility Data (Topic 20)  
**Presenters:** Namith Kumar C (`PES1UG24AM171`) & Jayanth K (`PES1UG24AM123`)  
**Course:** Foundations of Big Data & Responsible AI Engineering  
**Total Target Duration:** Exactly 3 Minutes (180 Seconds)

---

### Video Storyboard & Timing Overview

| Timestamp | Segment Title | Presenter | Key Visual on Screen |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:25** | Project Overview & Real-World Motivation | Namith Kumar C | Title Slide + NYC Borough Map highlighting disparity |
| **0:25 - 0:55** | Big Data Systems Architecture | Jayanth K | Mermaid Architecture Diagram & PySpark DAG Plan |
| **0:55 - 1:35** | Responsible AI Audit & Empirical Bias | Namith Kumar C | Disparity Maps, Boxplots, and Lorenz Curve |
| **1:35 - 2:05** | Real-Time Streaming & Differential Privacy | Jayanth K | Live Streaming Telemetry Terminal & DP Table |
| **2:05 - 2:40** | Policy Simulation & Pareto Tradeoff | Namith Kumar C | Simulation Scorecard & Pareto Frontier Chart |
| **2:40 - 3:00** | Conclusion & Regulatory Governance | Jayanth K | Regulatory Compliance Slide & GitHub Repository |

---

### Section-by-Section Script & Narration

#### [0:00 - 0:25] Segment 1: Motivation & Problem Statement
* **On Screen:** Title slide showing project name, team names (Namith Kumar C - PES1UG24AM171, Jayanth K - PES1UG24AM123), and course title. Transitions to a split map of New York City showing Manhattan versus the South Bronx and East New York.
* **Speaker:** **Namith Kumar C**
* **Narration:**
  > "Hello everyone. Welcome to our presentation on *Geographic and Socioeconomic Bias in Spatial Data*.
  > On-demand ride-hailing and delivery services promise frictionless urban mobility. But under unregulated algorithmic market forces, driver supply overwhelmingly concentrates in wealthy commercial districts like Midtown and the Upper East Side.
  > Meanwhile, residents in lower-income outer boroughs face prolonged wait times, high cancellations, and severe mobility exclusion.
  > Today, we demonstrate a scalable Big Data pipeline and Responsible AI solution that measures this spatial penalty and introduces an equity-weighted policy that successfully fixes it."

---

#### [0:25 - 0:55] Segment 2: Big Data Architecture & Distributed Engine
* **On Screen:** Clean architecture animation showing ingestion of NYC TLC Parquet logs (250,000 trips), US Census ACS tables, and OpenStreetMap infrastructure. Highlights the PySpark DAG and Lakehouse storage layout.
* **Speaker:** **Jayanth K**
* **Narration:**
  > "To analyze urban bias at scale, we engineered a distributed Big Data pipeline.
  > Joining 250,000 spatial trips with 71 census zones across multiple nodes would normally cause massive network shuffle.
  > We solved this by implementing an Apache Spark **Broadcast Hash Join**, broadcasting the spatial metadata directly to all executors. This slashed network shuffle I/O by **94.2%**.
  > The processed feature store is persisted to an ACID-compliant **Lakehouse tier using Parquet** with Snappy compression, partitioned hierarchically by Borough and pickup hour for sub-second analytical querying."

---

#### [0:55 - 1:35] Segment 3: Responsible AI Audit & Disparity Evidence
* **On Screen:** Switching to Jupyter Notebook / Figure display:
  1. `fig1_spatial_coverage_disparity.png` (Trip density vs Income)
  2. `fig2_wait_time_gap_by_borough.png` (Wait times across boroughs)
  3. `fig3_lorenz_curve_spatial_inequality.png` (Lorenz Curve showing Gini = 0.732)
* **Speaker:** **Namith Kumar C**
* **Narration:**
  > "Now let's examine the empirical bias uncovered by our Responsible AI audit.
  > Under the **EEOC 80% Rule**, a Disparate Impact Ratio below 0.80 indicates statutory discrimination.
  > In baseline market conditions, the Disparate Impact Ratio between disadvantaged and advantaged zones is **0.629**—a direct violation of federal fairness guidelines!
  > Disadvantaged outer-borough zones experience a 29.5% Demographic Parity Gap. In the Bronx, average wait times exceed 8.5 minutes, compared to just 3.9 minutes in Manhattan.
  > Furthermore, our Lorenz curve reveals a spatial Gini index of **0.732**, while correlation analysis confirms a statistically significant penalty: income inversely predicts wait time with r = -0.585 and p < 10⁻⁷."

---

#### [1:35 - 2:05] Segment 4: Real-Time Streaming & Differential Privacy
* **On Screen:** Live terminal showing Spark Structured Streaming micro-batch log with automated alerts, followed by the Laplace Differential Privacy utility chart.
* **Speaker:** **Jayanth K**
* **Narration:**
  > "Mobility disparities worsen during peak hours. Using **Spark Structured Streaming** over simulated Kafka streams with 10-second watermarking, our platform detects real-time concept drift when the Disparate Impact drops during rush hours, triggering live operational alerts.
  > Furthermore, publishing fine-grained spatial pickup locations poses severe re-identification risks to citizens in low-density census tracts.
  > We implemented the **Laplace Mechanism for Differential Privacy**. At epsilon = 0.5, our system provides rigorous mathematical privacy protection with a mean absolute error of just 2.1 trips, guaranteeing privacy without sacrificing utility."

---

#### [2:05 - 2:40] Segment 5: Equitable Policy Simulation & Pareto Frontier
* **On Screen:** Showing `fig5_policy_simulation_comparison.png` (Baseline vs Flat Subsidy vs Equity Policy) and `fig6_pareto_equity_efficiency_tradeoff.png` (Pareto frontier).
* **Speaker:** **Namith Kumar C**
* **Narration:**
  > "To solve this systemic issue, we tested three operational policies in our spatial queuing simulator.
  > A naive flat subsidy of $2.50 fails because over 70% of funds flow straight into already-saturated Manhattan rides.
  > Instead, we designed an **Equity-Weighted Dynamic Incentive Policy**. It leverages a modest 75-cent Manhattan congestion surcharge to fund up to a $4.50 pickup incentive in underserved neighborhoods, combined with a deadheading guarantee floor for repositioning drivers.
  > The result? Outer-borough wait times plunge by **38.4%**, ride fulfillment rises to **97.8%**, and the Disparate Impact Ratio surges to **1.444**, fully restoring regulatory compliance while preserving **93.8% of platform revenue efficiency**."

---

#### [2:40 - 3:00] Segment 6: Conclusion & Regulatory Governance
* **On Screen:** Summary slide showing regulatory compliance checklist (NYC Local Law 144, Title VI Civil Rights Act, Gebru Datasheet & Model Card), repository QR code / GitHub URL.
* **Speaker:** **Jayanth K**
* **Narration:**
  > "In conclusion, our project demonstrates that algorithmic fairness and big data scalability go hand in hand.
  > With our reproducible Docker pipeline, distributed PySpark architecture, and verified Responsible AI framework, cities and platforms can ensure every neighborhood receives fair, reliable transportation.
  > Full code, notebooks, and datasets are available in our GitHub repository.
  > Thank you!"

---

### Production Recording Notes
- **Resolution:** 1080p (1920x1080), 30 fps or 60 fps.
- **Audio:** Clear microphone voiceover with crisp delivery.
- **Visuals:** Seamless screen recordings of the executed notebook `notebooks/results_analysis.ipynb`, terminal execution of `python run_all.py`, interactive HTML dashboard `docs/disparity_map_summary.html`, and generated high-resolution PNG figures.
