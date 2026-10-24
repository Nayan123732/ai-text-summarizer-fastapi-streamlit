# AI Text Summarizer

An end-to-end text summarization app. Paste a long text or a chat conversation and get a short summary, with word counts and an option to hear the summary read aloud.

It is built like a small production project: a modular data pipeline, a REST API, and a web interface. It runs on the CPU with a small model, so it works on laptops with limited RAM (tested on a 4 GB machine setup).

## Features
- Modular ML pipeline: data ingestion, validation, and tokenization (SAMSum dialogue dataset)
- FastAPI backend with a `/predict` endpoint and a `/health` check; the model is loaded once at startup
- Streamlit web page with original and summary word counts and how much shorter the summary is
- Read-aloud button using the browser's built-in text-to-speech
- Settings in YAML files (`config/config.yaml`, `config/params.yaml`) for model, beams, and length limits

## Tech stack
Python, PyTorch, Hugging Face Transformers, Datasets, FastAPI, Uvicorn, Streamlit

## Model
`sshleifer/distilbart-cnn-12-6`, a distilled BART model. It was trained on news articles, so summaries of chats are reasonable but not as strong as a model fine-tuned on dialogue. Fine-tuning is not part of this repo. You can change the model in `config/config.yaml`.

## Project structure
```
app.py                  FastAPI backend
streamlit_app.py        Web page
main.py                 Runs the data pipeline
config/                 config.yaml, params.yaml
src/text_summarizer/
    components/         ingestion, validation, transformation
    pipeline/           stages and prediction
    config/ entity/ constants/ utils/ logging/
```

## Setup
```
conda create -n summary python=3.11
conda activate summary
pip install -r requirements.txt
pip install -e .
```

## Run
Terminal 1 (the first start downloads the model, about 1.2 GB):
```
uvicorn app:app --host 127.0.0.1 --port 8000
```
Terminal 2:
```
streamlit run streamlit_app.py
```
Open http://localhost:8501.

Optional data pipeline: `python main.py`

## Speed tips
In `config/params.yaml`, set `num_beams: 1` and a lower `max_input_tokens` for faster summaries.

## Dataset license
The SAMSum dataset is licensed for non-commercial research use (CC BY-NC-ND 4.0). The dataset is downloaded when you run the pipeline and is not included in this repo.
