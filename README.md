# Resume AI Screener

An AI-powered resume screening tool that helps recruiters evaluate candidate resumes against job descriptions with semantic understanding. Built with LangChain, OpenAI GPT, Retrieval-Augmented Generation (RAG), PostgreSQL, PGVector, and Streamlit.

## **🌟 Key Features**
- Upload Resume: Users can upload resumes (PDF format) tied to specific job postings.

- Job ID Selection: Dropdown for selecting available job IDs with auto-fill job title.

- Candidate Summary View: Dashboard displays a quick overview of submitted resumes.

- Semantic Insights: Extracts and summarizes experience, current title, and skills using AI.

- Candidate Actions: Buttons for initiating a chat or viewing the original resume.

- RAG-based Screening: Integrates LLMs with vector search for intelligent candidate evaluation.

## **🖥️ User Interface Preview**

### **Upload Page**

<img width="1678" alt="Screenshot 2025-05-05 at 10 56 16 PM" src="https://github.com/user-attachments/assets/c9270b4a-6d84-4855-bdb6-56ce7a9d038a" />

- Dropdown to select Job ID

- PDF upload interface (Drag & Drop or Browse)

- "View Candidate Profile" button to see extracted insights

### **Screening Dashboard**


<img width="1672" alt="Screenshot 2025-05-05 at 10 56 40 PM" src="https://github.com/user-attachments/assets/38c11a9d-85cf-4011-9fe2-6fa0783167b5" />

Displays:

- Job ID & Title

- Resume counts

- Post start and end dates

- Candidate list with name, experience summary, skills, and degree status

- Interactive options: Chat and Resume View

## **🛠️ Tech Stack**

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | Streamlit              |
| Backend Logic    | Python + LangChain     |
| LLM Integration  | OpenAI GPT (via API)   |
| Embedding Search | PGVector + PostgreSQL  |
| PDF Parsing      | PyMuPDF / pdfminer.six |








