# AI Project

A Python project demonstrating **LangChain** agents with web search (Tavily), structured outputs, and optional local LLM usage via Ollama.

## Features

- **LangChain agent** – Uses OpenAI (GPT) with Tavily search to answer questions and return structured responses with an answer and source URLs.
- **Structured output** – Pydantic models (`AgentResponse`, `Source`) for typed answers and citations.
- **Model testing** – Optional chain using Ollama (e.g. `gemma3:270m`) with a prompt template for summarization.
- **LangSmith** (optional) – Trace and debug runs in [LangSmith](https://smith.langchain.com).

## Prerequisites

- **Python 3.10+**
- **OpenAI API key** – for the main agent
- **Tavily API key** – for web search ([Tavily](https://tavily.com))
- **Ollama** (optional) – only if you want to run `model_testing()` with a local model

## Installation

Using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Environment

Create a `.env` file in the project root (do not commit it):

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### LangSmith (optional)

To trace agent and chain runs in [LangSmith](https://smith.langchain.com) for debugging and monitoring, add:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
```

Get an API key at [smith.langchain.com](https://smith.langchain.com). With these set, runs from `main.py` will appear in your LangSmith project.

## Usage

Run the main entry point (runs the agent with a sample query):

```bash
python main.py
```

By default this runs **agent testing**: the agent uses Tavily to answer a question (e.g. weather in Hyderabad) and prints a structured response with `answer` and `sources`.

To try the **model testing** flow (Ollama summarization), uncomment `model_testing()` in `main()` and comment out `agentTesting()`, then ensure Ollama is running with the `gemma3:270m` model.

## Project structure

- `main.py` – Entry point, agent setup, tools, and model-testing chain
- `pyproject.toml` – Project metadata and dependencies
- `.env` – API keys (create from the template above; keep out of version control)

## Dependencies

Key dependencies (see `pyproject.toml` for versions):

- **langchain** – Agent and chain orchestration
- **langchain-openai** – OpenAI chat model
- **langchain-ollama** – Ollama chat model (optional)
- **langchain-tavily** – Tavily search tool
- **python-dotenv** – Load `.env` variables
- **black**, **isort** – Formatting and import sorting
