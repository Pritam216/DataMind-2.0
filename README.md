# 🚀 **DataMind-2.0** — Advanced Backend for Smart Data Analysis AI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688?logo=fastapi)
![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20GPT-orange)
![Redis](https://img.shields.io/badge/Redis-State%20Management-red?logo=redis)
![Railway](https://img.shields.io/badge/Deployed%20On-Railway-purple?logo=railway)
![API](https://img.shields.io/badge/API-RESTful-success)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---
![AI Powered](https://img.shields.io/badge/AI-Powered-blueviolet)
![Backend](https://img.shields.io/badge/Backend-FastAPI-black)
![Scalable](https://img.shields.io/badge/Scalable-Yes-success)
---
> 🔗 **Demo Link:** [https://datamind-20-production.up.railway.app/docs](https://datamind-20-production.up.railway.app/docs)

## 🎥 Demo Video
[![DataMind-2.0 Demo](https://github.com/user-attachments/assets/1373eede-50db-4382-a509-8ea019e73939)](https://youtu.be/OxyeqtRZHqU)

---

## 📌 **Introduction**

DataMind-2.0 is the backend service powering a next-generation **AI-driven data analysis and insight platform**. This system is designed to parse, understand, and intelligently process structured and unstructured data via **Large Language Models (LLMs)** and ML-orchestrated workflows — enabling users to query and analyze datasets, generate charts, drive insight queries, and apply analytics in natural language.

Unlike simple demo bots, this backend is **scalable, production-ready**, and structured to support **persistent storage, multi-user sessions, and agent coordination** behind the scene.

---

## 🧠 **Purpose & Vision**

DataMind-2.0 is built to address real-world data analysis needs:

* Turn raw data into AI-understandable representations
* Enable **Auto-analysis** of tabular data, SQL content, CSVs, spreadsheets
* Facilitate natural language queries against datasets
* Power intelligent dashboards, explanations, recommendations
* Serve as the backend for multi-agent AI workflows

By coupling a backend API with LLM workflows and vector memory, this project makes **data analysis accessible, interactive, and automatic**.

---

## 📁 **Project Structure**

```
DATAMIND-2.0
├── __pycache__
├── Backend
│   ├── __pycache__
│   ├── data
│   ├── chat_nodes.py
│   ├── graph.py
│   ├── main_nodes.py
│   ├── main.py
│   ├── models.py
│   ├── mongo.py
│   ├── prompt.py
│   ├── session_store.py
│   ├── state.py
│   ├── storage_graphs.py
│   ├── testing_ground.ipynb
│   └── tools_functions.py
├── venv
├── .env
├── .gitignore
├── app.py
├── LICENSE
├── Procfile
├── README.md
└── requirements.txt
```

---

## 🤖 **LLM & AI Engines Used**

> You can elaborate this table once specific models are in your code.

| Component       | Model / Service                             |
| --------------- | ------------------------------------------- |
| Chat & Analysis | Google Gemini / Cohere / Groq API           |
| Memory Storage  | Vector DB / Cloudinary                      |
| Agent Logic     | Custom workflow orchestrator                |
| Graph           | LangGraph, LangChain                        |

---
## 🔐 **Environment Variables**

Create a `.env` file with the following:

```
GEMINI_API_KEY = ""
COHERE_API_KEY = ""
GROQ_API_KEY = ""

CLOUDINARY_CLOUD_NAME = ""
CLOUDINARY_API_KEY = ""
CLOUDINARY_API_SECRET = ""

MONGO_URI = ""
DB_NAME = ""
COLLECTION_NAME = ""
```

> DB and vector storage depends on your exact implementation.

---
<img width="181" height="933" alt="image" src="https://github.com/user-attachments/assets/fab2c541-689e-46b0-b6ac-56a573e70022" />

## 🛠️ **Setup & Installation**

1. **Clone the repo**

   ```bash
   git clone https://github.com/Pritam216/DataMind-2.0.git
   cd DataMind-2.0
   ```

2. **Create Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env` with keys**
   *(Refer to Environment Variables above)*

---

## ▶️ **How to Run Locally**

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

📌 Visit: `http://localhost:8000/docs` — Auto API docs

---

## ⭐ **Features**

### 🔐 Privacy-First Data Handling

* **No data storage** — datasets are processed in memory only
* **Automatic deletion** once EDA completes
* Zero long-term retention, eliminating data leakage risks

---

### ⚙️ Pure Python Analytics

* Entire analysis runs on:

  * **NumPy** for computation
  * **Pandas** for data processing
  * **Plotly** for interactive visualizations
* No external analytics engines or data persistence

---

### 🤖 Safe & Responsible AI Usage

* AI models (Gemini / ChatGPT / others) are used **only to generate insights**
* Raw data is **never stored, reused, or trained on**
* Safer than uploading datasets directly to AI chat tools

---

### 📊 Ephemeral EDA Execution

* EDA runs fully within a single session
* Charts and summaries are generated on the fly
* Memory is cleared immediately after execution

**Your data is analyzed, visualized, and forgotten.**

---

## 📘 **How to Use**

1. **Deploy backend**
2. Connect frontend or client UI
3. Send natural language data analysis requests
4. Receive structured insights and insights outputs
5. Combine with dashboards & reports

---

## 💡 **Why Use DataMind-2.0?**

You might ask:

> *“Why not just upload to Gemini / ChatGPT and ask?”*

Great question. Here’s why DataMind-2.0 is valuable:

### 🚀 **1. Production Grade**

* Designed for APIs, backend scaling, persistent memory
* Not a one-off prompt session

### 🧱 **2. Structured Intelligence**

* Custom workflows, logic, error handling
* Knowledge memory & context that persists beyond single chats

### 📈 **3. Integrations**

* Connects to DBs, Redis, vector DBs, queues
* Boosts reliability and enterprise use-cases

### 🔧 **4. Customization**

* Easily adapt to domain logic, improve models
* Add your workflows, constraints, agents

---

## 🧭 **Advancements Over Consumer Chat**

| ChatGPT / Gemini   | DataMind-2.0 Backend        |
| ------------------ | --------------------------- |
| Single session NLP | Persistent memory + context |
| No endpoint API    | REST APIs for apps          |
| Generic model      | Tunable for data analysis   |
| Prompt only        | Complex logic & workflows   |

---

## 🔭 **Future Enhancements**

✨ *Planned improvements:*

* **Vector DB integration** (Pinecone / Milvus / Weaviate)
* **Larger model support** (LLaMA 3 / GPT-5 / Gemini Ultra)
* **Document upload & auto parsing**
* **Web dashboard integration**
* **User auth & RBAC**
* **Interactive analytics UI**
* **Streaming responses & WebSockets support**

---

## 📌 **Conclusion**

DataMind-2.0 is a powerful backend scaffold for AI-powered data analysis and insight generation. It turns raw data into actionable intelligence through smart LLM-driven workflows while being robust enough for real deployment environments like Railway, Render, or AWS.

This repository isn’t just a demo — it’s a **foundation for real applications**, scalable enrichments, and production AI projects. Whether building analytics dashboards, AI-assistant UIs, or internal tools, DataMind-2.0 provides a solid backend foundation.

---

## ❤️ **Support & Contribution**

If you find this project useful:

⭐ Star the repository
📥 Open issues for ideas
📄 Submit PRs for enhancements

---
