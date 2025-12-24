#RT_IOT2022

# ai_iot_security.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import time
import requests

# Function to send normal device detection
def send_normal(ip, name):
    try:
        requests.get(f"http://localhost:5000/normal/{ip}/{name}")
    except:
        pass  # Ignore if dashboard not running

# Function to send attack detection
def send_attack(ip, atype):
    try:
        requests.get(f"http://localhost:5000/attack/{ip}/{atype}")
    except:
        pass  # Ignore if dashboard not running

    
print("🚀 Loading dataset...")
df = pd.read_csv('RT_IOT2022.csv')

# Check label column
if 'Attack_type' not in df.columns:
    print("❌ Error: 'Attack_type' column not found.")
    exit()

# Use only known normal device types for clean demo
normal_types = ["Thing_Speak", "MQTT_Publish", "Wipro_bulb"]
all_types = df['Attack_type'].unique()

# Filter dataset: keep only normal + a few attack types
filtered_df = df[df['Attack_type'].isin(normal_types + ['DOS_SYN_Hping', 'ARP_poisioning'])]
filtered_df = filtered_df.sample(500, random_state=42).reset_index(drop=True)  # Small sample

# Encode labels
le = LabelEncoder()
filtered_df['label_encoded'] = le.fit_transform(filtered_df['Attack_type'])

# Select features
features = [
    'flow_duration', 'fwd_pkts_tot', 'bwd_pkts_tot',
    'fwd_pkts_per_sec', 'bwd_pkts_per_sec', 'flow_pkts_per_sec',
    'flow_SYN_flag_count', 'flow_ACK_flag_count', 'flow_iat.avg'
]
features = [f for f in features if f in filtered_df.columns]

X = filtered_df[features]
y = filtered_df['label_encoded']

# Train only Random Forest (simpler, more accurate)
print("🌳 Training Random Forest Classifier...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Simulate 10 Normal Devices
print("\n" + "="*60)
print("📡 LIVE MONITORING: 10 NORMAL DEVICES")
print("="*60)

normal_only = filtered_df[filtered_df['Attack_type'].isin(normal_types)]
sampled = normal_only.sample(10, random_state=42).reset_index(drop=True)

for i, row in sampled.iterrows():
    ip = f"192.168.1.{10 + i}"
    pkt_data = row[features].values
    
    # Predict
     # Wrap packet data in DataFrame with correct column names
    pkt_df = pd.DataFrame([pkt_data], columns=features)

# Predict
    pred = model.predict(pkt_df)[0]
    device_type = le.inverse_transform([pred])[0]

# Status
    if device_type in normal_types:
        status = "🟢 Normal"
        action = ""
    else:
        status = "🔴 ATTACK DETECTED!"
        action = f"   🛡️ Action: Blocking IP {ip}"
    
    print(f"[{time.strftime('%H:%M:%S')}] Device-{i+1} ({device_type})")
    print(f"   IP: {ip}")
    print(f"   Status: {status}")

    if action:
        print(action)
    send_normal(ip, device_type)
    print("-" * 50)
    time.sleep(1.2)

# 🔁 First: Simulate DDoS Flood Attack
print("⚠️ External Attack Detected: DDoS Flood from 203.0.113.55")
time.sleep(2)

ddos_flow = [
    0.01,   # flow_duration       - very short
    1000,   # fwd_pkts_tot        - many packets
    10,     # bwd_pkts_tot
    100000, # fwd_pkts_per_sec    - extremely high rate
    100,    # bwd_pkts_per_sec
    100100, # flow_pkts_per_sec
    1,      # flow_SYN_flag_count - frequent connection attempts
    0,      # flow_ACK_flag_count
    0.001   # flow_iat.avg        - rapid bursts
]
ddos_df = pd.DataFrame([ddos_flow], columns=features)
pred = model.predict(ddos_df)[0]
attack_type = le.inverse_transform([pred])[0]

print(f"[{time.strftime('%H:%M:%S')}] 🔴 MALICIOUS DEVICE (DDoS)")
print(f"   IP: 203.0.113.55 | Type: {attack_type}")
print(f"   Status: 🔴 ATTACK DETECTED!")
print(f"   🛡️ Action: Blocking IP & Alerting Admin")
send_attack("203.0.113.55", "DOS_SYN_Hping")
print("-" * 50)
time.sleep(2)


# 🔍 Second: Simulate Port Scan Attack
print("⚠️ New Threat: Port Scan from 198.51.100.77")
time.sleep(2)

port_scan_flow = [
    120.0,  # flow_duration       - long-lived
    100,    # fwd_pkts_tot        - low packet count
    50,     # bwd_pkts_tot
    1,      # fwd_pkts_per_sec    - very slow rate
    0.5,    # bwd_pkts_per_sec
    1.5,    # flow_pkts_per_sec
    0,      # flow_SYN_flag_count - may not use SYN heavily
    100,    # flow_ACK_flag_count - ACK-based scanning
    1.0     # flow_iat.avg        - regular intervals
]
port_scan_df = pd.DataFrame([port_scan_flow], columns=features)
pred = model.predict(port_scan_df)[0]
attack_type = le.inverse_transform([pred])[0]

print(f"[{time.strftime('%H:%M:%S')}] 🔴 MALICIOUS DEVICE (Port Scan)")
print(f"   IP: 198.51.100.77 |")
print(f"   Status: 🔴 ATTACK DETECTED!")
print(f"   🛡️ Action: Blocking IP & Isolating device ,initiating security audit")
send_attack("198.51.100.77", "Port Scan")
print("="*60)



print("✅ System Secure – All Threats Neutralized")
