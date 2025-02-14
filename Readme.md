# LawGlance: AI-Powered Legal Assistant

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/license/apache-2-0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Open%20Source-5e9cff?logo=langchain&logoColor=white)](https://python.langchain.com/docs/introduction/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Backend-1c1c1c?logo=langgraph&logoColor=white)](https://langchain-ai.github.io/langgraph/)

**Website:** [lawglance.com](https://lawglance.com/)

LawGlance is a free, open-source legal AI assistant built on Retrieval-Augmented Generation (RAG). It delivers accurate, cited answers to legal questions for both laypeople and professionals, currently covering Indian law with plans to expand internationally.

---

## Legal Coverage

LawGlance currently indexes the following statutes:

- The Indian Constitution
- The Bharatiya Nyaya Sanhita, 2023
- The Bharatiya Nagarik Suraksha Sanhita, 2023
- The Bharatiya Sakshya Adhiniyam, 2023
- The Consumer Protection Act, 2019
- The Motor Vehicles Act, 1988
- The Information Technology Act, 2000
- The Protection of Children from Sexual Offences Act (POCSO), 2012
- The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013

---

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- An OpenAI API key
- Redis (optional, recommended for production)

### Setup

**1. Clone the repository**

```bash
git clone https://github.com/lawglance/lawglance.git
cd lawglance
```

**2. Install uv**

macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal to ensure the `uv` command is on your PATH.

**3. Install dependencies**

```bash
uv sync
```

**4. Configure environment**

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

**5. Run the application**

```bash
uv run streamlit run app.py
```

**6. Open in browser**

```
http://127.0.0.1:8501
```

---

## Architecture

LawGlance is powered by an agentic retrieval pipeline built with **LangGraph**, located in the [`backend/`](backend/) directory. Rather than a fixed RAG chain, the agent autonomously decides when to invoke the `retrieve_docs` tool, iterates until sufficient context is gathered, and then produces a cited final answer.

| Module | Responsibility |
|---|---|
| `backend/graph.py` / `backend/nodes.py` | LangGraph agent loop: `llm_call → tool_node → final_answer` |
| `backend/tools.py` | Vector-store retrieval tool |
| `backend/retrieval.py` | `agent_invoke()` — entry point called by `app.py` |
| `backend/main.py` | Optional FastAPI HTTP API wrapping the same agent |

The original single-chain implementation (`lawglance_main.py`, `chains.py`) remains in the repository for reference but is no longer the active path.

### FastAPI backend

Run the HTTP API standalone (useful for integrating LawGlance into other applications):

```bash
uv run uvicorn backend.main:app --reload
```

Query directly:
```bash
curl "http://127.0.0.1:8000/query?query=What+is+Article+21%3F"
```

---

## Redis Caching

Redis caches chat history and LLM responses, improving throughput for concurrent users. It is optional for local development but recommended for production deployments.

### Installation

**Ubuntu / Linux**
```bash
sudo apt-get update && sudo apt-get install redis-server
```

**macOS (Homebrew)**
```bash
brew install redis
```

**Windows** — use WSL (Ubuntu), then:
```bash
sudo apt-get update && sudo apt-get install redis-server
redis-server
```

### Verify

```bash
redis-cli ping
# Expected: PONG
```

The backend connects to `redis://localhost:6379/0` by default. Override via the `redis_url` parameter in the configuration if needed.

---

## Technology Stack

| Technology | Role |
|---|---|
| **LangGraph** | Agentic retrieval loop (`backend/`) |
| **LangChain** | Conversational AI pipelines, RAG orchestration |
| **ChromaDB** | Vector database for legal document embeddings |
| **FastAPI** | HTTP API layer (`backend/main.py`) |
| **Streamlit** | Chat UI (`app.py`) |
| **Redis** | Chat history and response caching |
| **OpenAI API** | Language model inference |

---

## Roadmap

- **Agentic framework** — delivered. The LangGraph single-agent pipeline now powers the live application. A full multi-agent specialist team remains on the roadmap.
- **Global legal coverage** — extending the knowledge base to additional jurisdictions (Canada and others).
- **Voice interaction** — speech input for hands-free legal queries.
- **Multi-lingual support** — answers in languages beyond English.
- **Advanced search** — precision ranking and personalised suggestions.
- **Legal document generation** — contract and agreement templates via guided input.
- **Case management** — deadline tracking and matter organisation.

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes with a descriptive message.
4. Push to your fork and open a pull request against `main`.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE.md](LICENSE.md) for the full text.
