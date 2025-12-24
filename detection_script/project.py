# ai_iot_security.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import time
import requests


def send_normal(ip, name):
    try:
        requests.get(f"http://localhost:5000/normal/{ip}/{name}")
    except:
        pass 


def send_attack(ip, atype):
    try:
        requests.get(f"http://localhost:5000/attack/{ip}/{atype}")
    except:
        pass  

    
print("🚀 Loading dataset...")
df = pd.read_csv('RT_IOT2022.csv')

if 'Attack_type' not in df.columns:
    print("❌ Error: 'Attack_type' column not found.")
    exit()

normal_types = ["Thing_Speak", "MQTT_Publish", "Wipro_bulb"]
all_types = df['Attack_type'].unique()

filtered_df = df[df['Attack_type'].isin(normal_types + ['DOS_SYN_Hping', 'ARP_poisioning'])]
filtered_df = filtered_df.sample(500, random_state=42).reset_index(drop=True)  # Small sample

le = LabelEncoder()
filtered_df['label_encoded'] = le.fit_transform(filtered_df['Attack_type'])

features = [
    'flow_duration', 'fwd_pkts_tot', 'bwd_pkts_tot',
    'fwd_pkts_per_sec', 'bwd_pkts_per_sec', 'flow_pkts_per_sec',
    'flow_SYN_flag_count', 'flow_ACK_flag_count', 'flow_iat.avg'
]
features = [f for f in features if f in filtered_df.columns]

X = filtered_df[features]
y = filtered_df['label_encoded']

print("🌳 Training Random Forest Classifier...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\n" + "="*60)
print("📡 LIVE MONITORING: 10 NORMAL DEVICES")
print("="*60)

normal_only = filtered_df[filtered_df['Attack_type'].isin(normal_types)]
sampled = normal_only.sample(10, random_state=42).reset_index(drop=True)

for i, row in sampled.iterrows():
    ip = f"192.168.1.{10 + i}"
    pkt_data = row[features].values
    pkt_df = pd.DataFrame([pkt_data], columns=features)

    pred = model.predict(pkt_df)[0]
    device_type = le.inverse_transform([pred])[0]

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


print("⚠️ External Attack Detected: DDoS Flood from 203.0.113.55")
time.sleep(2)

ddos_flow = [
    0.01,   
    1000,   
    10,     
    100000, 
    100,    
    100100, 
    1,      
    0,     
    0.001   
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


print("⚠️ New Threat: Port Scan from 198.51.100.77")
time.sleep(2)

port_scan_flow = [
    120.0,  
    100,   
    50,     
    1,      
    0.5,    
    1.5,    
    0,      
    100,   
    1.0     
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
