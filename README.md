# AI Medical Symptom Checker

A lightweight Gradio app that sends your symptoms to a local Ollama LLM and streams back a structured analysis.

Not medical advice. For emergencies, call your local emergency number.

## Features

- Streaming responses from Ollama for fast feedback
- Structured output sections:
  - Possible Conditions
  - Red Flags
  - General Advice
  - Triage (Low/Medium/High with reason)
- Simple Gradio UI
- Optional FastAPI endpoint

## Requirements

- Python 3.10+
- Ollama (running locally): https://ollama.com/
- Model: `mistral:latest`

## Setup

1) Install Python packages

```bash
pip install -r requirements.txt
```

2) Pull the model (one time)

```bash
ollama pull mistral:latest
```

3) Run the Gradio app

```bash
python3 symptom_checker.py
```

Open the URL printed in the terminal (default: http://127.0.0.1:7861).

## FastAPI (optional)

You can also expose a simple HTTP API:

```bash
uvicorn app:app --reload
```

POST to `/medical/` with a JSON body string containing symptoms.

## Configuration

- Ollama endpoint: `OLLAMA_URL` in `symptom_checker.py` (default: http://localhost:11434/api/generate)
- Model: set in the payload (currently `mistral:latest`)

## Project Structure

- `symptom_checker.py` — Gradio UI and streaming logic
- `app.py` — FastAPI endpoint (non-streaming)

## Disclaimers

- This tool is for informational purposes only and does not provide medical advice.
- Always consult a qualified healthcare provider for diagnosis and treatment.
