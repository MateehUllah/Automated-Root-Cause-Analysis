# 🌐 Automated Root Cause Analysis

This project integrates **AI-powered network monitoring** with **a voice-enabled chatbot**.  
It uses **machine learning models** to predict network failures and an **AI chatbot** to assist with **network-related troubleshooting**.

---

## **🚀 Features**
✅ **AI Network Failure Prediction** (Packet Loss, Latency, Bandwidth Usage)  
✅ **Weather-Based Network Monitoring**  
✅ **AI Chatbot for Network Issues (Mistral-7B)**  
✅ **Voice-to-Text Chatbot (Microphone Only - Whisper)**  
✅ **Text-to-Speech (AI Reads Responses Aloud)**  
✅ **Email Alerts for Network Failures**  

---

## **📌 Installation Guide**
### **1️⃣ Install Python 3.10.16 (If Not Installed)**
Ensure you are using **Python 3.10.16**:

```bash
python --version
```
If you don't have Python 3.10.16 installed, install it using:

```bash
# macOS
brew install python@3.10
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Ubuntu/Linux
sudo apt update
sudo apt install python3.10

# Windows (Use Python Installer)
```

---

### **2️⃣ Clone This Repository**
```bash
git clone https://github.com/MateehUllah/Automated-Root-Cause-Analysis.git
cd automated-root-cuase-analysis
```

---

### **3️⃣ Create a Virtual Environment**
```bash
python3.10 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

### **4️⃣ Install Required Dependencies**
```bash
pip install -r requirements.txt
```

---

### **5️⃣ Set Up Environment Variables**
Create a `.env` file in the project root and add:

```ini
OPEN_WEATHER_API=
SMTP_SERVER=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_RECEIVER=
HUGGINGFACEHUB_API_TOKEN=
```

---

### **6️⃣ Run the Application**
```bash
streamlit run app.py
```

---

## **📚 How to Use**
### **1️⃣ AI Network Monitor**
- **Select a location** on the map to fetch real-time weather.
- **Adjust packet loss, latency, jitter, and bandwidth usage** using sliders.
- **AI predicts** if network failure is likely.
- **If failure is detected**, AI provides **mitigation recommendations**.
- **Send email alerts** if necessary.

### **2️⃣ AI Chatbot (NetBot)**
- **Type your query** (e.g., "How do I fix packet loss?").
- **OR Use your microphone** to **speak your query**.
- **AI transcribes your voice and responds with solutions**.
- **Response can be read or played as speech**.

---

## **📚 Technologies Used**
| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Network Prediction** | Scikit-learn (RandomForest) |
| **Chatbot AI** | Mistral-7B (Hugging Face) |
| **Speech-to-Text** | Whisper (Local Processing) |
| **Text-to-Speech** | Hugging Face TTS |
| **Weather API** | OpenWeatherMap |
| **Email Alerts** | SMTP via Python |

---

## **📚 Directory Structure**
```
📂 automated-root-cuase-analysis
│── 📂 components
│   ├── init.py               # Init file for components module
│   ├── chatbot.py                # AI Chatbot Code (Microphone Only)
│   ├── network_weather.py        # Network Monitoring Code
│
│── 📂 models
│   ├── network_model.pkl         # Trained ML Model for Failure Prediction
│
│── 📂 utils
│   ├── init.py               # Init file for utils module
│   ├── alert_system.py           # Email Alerts
│   ├── recommendations.py        # AI Recommendations
│
│── 📂 data                        # Folder for storing dataset files
│   ├── network_logs.csv
|
│── .env                           # API Keys (Ignored in Git)
│── app.py                         # Main Streamlit Application
│── requirements.txt                # Dependencies
│── README.md                      # Documentation
```

---

## **📚 Dependencies**
| Package | Version |
|---------|---------|
| **Python** | 3.10.16 |
| **Streamlit** | Latest |
| **scikit-learn** | 1.6.1 |
| **numpy** | Latest |
| **requests** | 2.32.3 |
| **folium** | Latest |
| **streamlit-folium** | Latest |
| **transformers** | 4.48.1 |
| **huggingface-hub** | 0.27.1 |
| **whisper** | Local |
| **soundfile** | Latest |
| **librosa** | Latest |

---

## **📚 Future Improvements**
- ✅ **Deploy on Hugging Face Spaces**
- ✅ **Web App UI Enhancement**
- ✅ **Multi-Language Support**
- ✅ **Live Network Monitoring API Integration**

---

## **📚 Contributing**
1️⃣ **Fork the repository**  
2️⃣ **Create a feature branch** (`feature-branch`)  
3️⃣ **Commit changes** (`git commit -m "Added new feature"`)  
4️⃣ **Push to GitHub** (`git push origin feature-branch`)  
5️⃣ **Create a Pull Request**  


