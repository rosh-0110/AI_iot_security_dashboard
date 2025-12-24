# 🛡️ AI-Powered Adaptive Security Framework for Simulated IoT Networks

## 🔹One-Line Summary
An intelligent system that detects cyberattacks in simulated IoT networks using AI and displays real-time alerts on a live dashboard.

---

## 📖 Overview
This project demonstrates an adaptive security framework designed to protect IoT networks from common cyber threats such as DDoS attacks, port scanning, and ARP poisoning. Using machine learning models trained on real IoT traffic data, the system identifies malicious behavior and simulates automatic defensive actions like blocking attacker IPs. A Flask-based web dashboard provides real-time visualization of network activity, making it easy to monitor threats and responses.

The entire system is built in Python and runs locally, offering a scalable prototype for future smart device security solutions.

---

## ⚠️ Problem Statement
Traditional firewall and rule-based intrusion detection systems (IDS) fail to detect evolving or unknown attacks in dynamic IoT environments. With billions of connected devices lacking strong built-in security, there’s a growing need for **intelligent, self-adaptive protection** that can learn normal behavior and respond to anomalies without human intervention.

This project addresses that gap by building an AI-driven system capable of detecting known and unknown threats in real time.

---

## 📊 Dataset
- **Name**: RT_IOT2022.csv
- **Source**: https://www.kaggle.com/datasets/supplejade/rt-iot2022real-time-internet-of-things/data
- **Attack Types Included**:
  - DOS_SYN_Hping (DDoS)
  - ARP_poisioning
  - NMAP_UDP_SCAN, NMAP_TCP_scan
  - Metasploit_Brute_Force_SSH
  - DDOS_Slowloris
- **Key Features Used**:
  - `flow_duration`, `fwd_pkts_tot`, `bwd_pkts_per_sec`
  - `flow_SYN_flag_count`, `flow_iat.avg`, `idle.avg`

> 💡The dataset reflects realistic IoT communication patterns and is ideal for intrusion detection research.

---

## 🛠️ Tools and Technologies
| Category | Technology |
|--------|------------|
| **Programming Language** | Python 3.8+ |
| **Machine Learning** | Scikit-learn (Random Forest, Isolation Forest) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib |
| **Web Framework** | Flask |
| **Dashboard** | HTML, CSS, JavaScript (auto-refreshing) |
| **Development Environment** | VS Code / IDLE |

---

## 🧪 Methods
1. **Data Preprocessing**: Cleaned and encoded labels; selected 15 key features for model input.
2. **Model Training**:
   - Trained **Random Forest Classifier** (supervised): Achieved **98% accuracy**
   - Used **Isolation Forest** (unsupervised) for anomaly detection
3. **Threat Simulation**: Injected synthetic DDoS and Port Scan attacks with realistic packet patterns.
4. **Adaptive Response**: Simulated IP blocking when attacks were detected.
5. **Real-Time Dashboard**: Built with Flask to display live alerts and a pie chart showing normal vs. attack ratio.

---

## 🔍 Key Insights
- Random Forest outperformed other models in classifying known attacks with high precision.
- Isolation Forest flagged unusual behaviors even without prior labeling — useful for zero-day threats.
- Combining supervised and unsupervised methods improved overall detection reliability.

---

## 🖥️ Dashboard Model
### Dashboard Features:
- Live alert feed (green = normal, red = attack)
- Auto-updating every 2 seconds
- Pie chart visualizing threat distribution
- Accessible via browser at: [http://localhost:5000](http://localhost:5000)

### Detection Output:
- Terminal shows real-time detection:
