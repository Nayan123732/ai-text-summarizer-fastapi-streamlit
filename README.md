# AI Text Summarizer

Summarizes long text or chats. Built for a low-RAM Windows laptop: it uses the small
`sshleifer/distilbart-cnn-12-6` model on the CPU instead of the large Pegasus model.

## One-time setup

Open a terminal in this folder and make sure the prompt starts with `(summary)`:

    conda activate summary
    pip install -r requirements.txt
    pip install -e .

## Run the app (two terminals, both in this folder, both showing `(summary)`)

Terminal 1, the backend (the first start downloads the model, about 1.2 GB, and loads it):

    uvicorn app:app --host 127.0.0.1 --port 8000

Wait for: `Application startup complete.`

Terminal 2, the web page:

    streamlit run streamlit_app.py

Streamlit opens http://localhost:8501 in the browser.

## Optional: data pipeline

    python main.py

Downloads the SAMSum dataset, checks it, and tokenizes it. The app does not need this.

## Settings

- `config/config.yaml` -> `prediction.model_name`: the model to use
- `config/params.yaml` -> `Generation`: summary length, beams, maximum input length

If it is slow or runs out of memory: set `num_beams: 2` and `max_input_tokens: 512`,
close other programs, or try `sshleifer/distilbart-cnn-6-6` as the model.
