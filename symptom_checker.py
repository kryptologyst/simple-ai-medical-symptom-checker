import requests
import json
import gradio as gr

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_symptoms(symptoms):
    """
    Streams analysis using Ollama and renders structured sections.
    """
    if not symptoms or not symptoms.strip():
        return "Please enter your symptoms (e.g., fever, cough, sore throat)."

    prompt = (
        "You are a helpful medical information assistant. You are NOT a doctor and do not provide diagnoses or treatment.\n"
        f"Analyze the following patient-reported symptoms and respond concisely in the structure below.\n\n"
        f"Symptoms: {symptoms}\n\n"
        "Format your response exactly with these sections and short bullet points where relevant:\n"
        "## Possible Conditions\n"
        "- ...\n"
        "\n## Red Flags (seek medical care if present)\n"
        "- ...\n"
        "\n## General Advice\n"
        "- ...\n"
        "\n## Triage\n"
        "Severity: Low | Medium | High — one sentence reason.\n\n"
        "End with: 'Disclaimer: This is general information, not medical advice.'"
    )

    payload = {
        "model": "mistral:latest",
        "prompt": prompt,
        "stream": True,
    }

    accumulated = ""
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    # If a line isn't valid JSON, skip it safely
                    continue
                chunk = data.get("response")
                if chunk:
                    accumulated += chunk
                    # Stream progressive content to Gradio
                    yield accumulated
                if data.get("done"):
                    break
    except requests.exceptions.RequestException as e:
        yield f"Error contacting model: {e}"

# Create Gradio interface
interface = gr.Interface(
    fn=analyze_symptoms,
    inputs=gr.Textbox(lines=3, placeholder="e.g., Fever, cough, sore throat, fatigue"),
    outputs=gr.Markdown(label="Analysis"),
    title="AI Medical Symptom Checker",
    description=(
        "Enter your symptoms to receive possible conditions, red flags, general advice, and a rough triage.\n"
        "This is general information and not medical advice."
    ),
)

# Launch the web app
if __name__ == "__main__":
    interface.launch()
# # Test Medical Symptom Checker
# if __name__ == "__main__":
#     test_symptoms = "Fever, cough, body aches"
#     print("### AI Medical Analysis ###")
#     print(analyze_symptoms(test_symptoms))
