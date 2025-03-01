import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/network_logs.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

X = df[['packet_loss', 'latency', 'jitter', 'bandwidth_usage', 'temperature']]
y = df['network_failure']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("models/network_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model training complete! Saved as 'models/network_model.pkl'")
