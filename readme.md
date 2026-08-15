# Nimbus Home — Customer Support Assistant

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg" alt="Project Logo" width="100"/>

### Overview

This project is a **customer support chatbot** built with **Streamlit** and **LangChain**, using **Retrieval Augmented Generation (RAG)** to answer customer questions about company policies, shipping, returns, warranties, and FAQs — grounded entirely in a company knowledge-base PDF rather than the model's general knowledge.

Originally built from an employee-onboarding assistant exercise, this version has been reworked into a **customer-facing** support tool: no internal employee data, no synthetic HR records — just a chatbot that answers real customer questions using retrieved, sourced content.

---

### What It Does

A customer types a question — e.g. *"What's your return policy?"* or *"Do your products work with Alexa?"* — and the assistant:

1. Embeds the question and searches a vector database built from the company's policy/FAQ PDF
2. Retrieves the most relevant chunks of that document
3. Feeds those chunks, along with the conversation history, into an LLM
4. Streams back a grounded, sourced answer in real time
5. Shows which page(s) of the source document the answer came from

---

### Tech Stack

- **Streamlit** — chat interface
- **LangChain** (LCEL) — retrieval + generation pipeline
- **Groq** (`llama-3.1-8b-instant`) — LLM inference
- **Chroma** — local vector database
- **HuggingFace `sentence-transformers`** (`all-MiniLM-L6-v2`) — local embeddings (no external API key or rate limits)
- **PyPDF** — PDF parsing

---

### Project Structure

```
├── app.py              # Entry point: builds vector store, wires up the assistant, launches UI
├── assistant.py         # Assistant class: LangChain RAG pipeline (retrieval + prompt + LLM)
├── gui.py                # AssistantGUI class: Streamlit rendering (chat, sidebar, sources)
├── prompts.py            # SYSTEM_PROMPT and WELCOME_MESSAGE
├── data/
│   └── company_faq.pdf   # Source knowledge base (customer-facing policies/FAQ)
├── requirements.txt
└── runtime.txt            # Pins Python version for deployment
```

---

### Setup

1. **Clone the repository** and create a virtual environment:
```bash
conda create -n nimbus-support python=3.11
conda activate nimbus-support
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add your API key.** Create a `.env` file in the project root:
```dotenv
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

4. **Add your knowledge base.** Place a PDF with your company's policies/FAQ content at `data/company_faq.pdf` (or update the path in `app.py`).

5. **Run the app:**
```bash
streamlit run app.py
```

---

### How It Works

**Ingestion (on first run, cached after):**
- `PyPDFLoader` extracts text from the PDF
- `RecursiveCharacterTextSplitter` breaks it into ~4000-character overlapping chunks
- Each chunk is embedded locally via `sentence-transformers` and stored in Chroma

**Per-question flow:**
- The question is embedded and matched against stored chunks (`similarity_search`)
- Retrieved chunks + conversation history + the question are assembled into a prompt via LangChain's LCEL parallel-runnable pattern
- The prompt is sent to Groq's LLM, and the response is streamed back token by token
- Source chunks are displayed under the answer for transparency

---

### Features

- ✅ Real-time streaming responses
- ✅ Conversation memory across turns
- ✅ Source citation (shows which PDF page each answer came from)
- ✅ "Clear conversation" reset button
- ✅ Fully local embeddings — no external embedding API, no rate limits
- ✅ Honest fallback — the assistant is instructed not to guess when retrieval doesn't return relevant information

---

### Example Questions to Try

- "What's your return policy?"
- "Do you offer free shipping?"
- "Are your products compatible with Alexa or Google Home?"
- "What's covered under warranty?"
- "How do I contact customer support?"
- "Do you sell smart refrigerators?" *(tests the "I don't know" fallback — not in the knowledge base)*

---

### Deployment

This app is deployable to [Streamlit Community Cloud](https://share.streamlit.io) for free. See `runtime.txt` for the pinned Python version (3.11) required for dependency compatibility with `chromadb` and `sentence-transformers`.

Required secret in Streamlit Cloud's "Secrets" panel:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

