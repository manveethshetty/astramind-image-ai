# 🎨 AstraMind Image AI — AI Image Generation Chatbot

An AI-powered image generation tool built with Python and Streamlit. Type a prompt, choose a style, and generate AI art — powered by Hugging Face's Inference Providers and the FLUX.1-dev model.

## 🔗 Live Demo
[https://astramind-image-ai-qwzxymkj79k9smmk2lsgn7.streamlit.app/]

## 📸 What It Does

Users type a text prompt, select a visual style from radio buttons, and the app generates a custom AI image combining both. Example:

```
Input:  A futuristic Indian city at night
Style:  Cyberpunk
Output: An AI-generated image with neon lights and a cyberpunk aesthetic
```

## ✨ Features

- **Text-to-image generation** powered by FLUX.1-dev via Hugging Face Inference Providers
- **6 style options** — Anime, Cyberpunk, Photorealistic, Watercolor Painting, Pencil Sketch, Fantasy Art
- **Style-conditioned prompts** — automatically appends style-specific descriptors to the user's prompt before sending to the API
- **Prompt history / gallery view** — every generated image stays visible with timestamp and download option
- **Download button** — save any generated image as PNG
- **Sidebar dashboard** — live generation count, last-generated timestamp, and recent thumbnails
- **Graceful error handling** — friendly messages for API failures, model loading delays, and quota limits

## 🛠️ Tech Stack
- **Frontend + Backend** — Python, Streamlit
- **Image Model** — `black-forest-labs/FLUX.1-dev` via Hugging Face Inference Providers
- **Client Library** — `huggingface_hub.InferenceClient`
- **Image Processing** — Pillow (PIL)
- **Environment Management** — python-dotenv

## 🏗️ Project Architecture

```
astramind-image-ai/
│
├── app.py             # Streamlit UI — input, style selection, gallery display
├── image_api.py        # Hugging Face InferenceClient integration
├── styles.py            # Style names mapped to prompt descriptors
├── requirements.txt
└── .gitignore
```

### Data Flow
```
User Prompt + Style Selection
        ↓
    app.py
        ↓
fetches style descriptor from styles.py
        ↓
concatenates: "{user_prompt}, {style_descriptor}"
        ↓
passes to image_api.py → Hugging Face InferenceClient
        ↓
PIL Image returned
        ↓
displayed in app.py + added to session_state history
```

## 🧠 Key Technical Decisions

**Style conditioning via prompt concatenation** — Unlike chat LLMs that accept separate system/user messages, image models take a single prompt string. Style is implemented by appending descriptive tags (e.g. "anime style, detailed, vibrant colors") to the user's input before the API call.

**Dictionary-based style management** — All styles live in one dictionary in `styles.py`, following the same Separation of Concerns pattern as prompt modes in AstraMind AI (the text-based sibling project). Adding a new style requires changing only one file.

**Dedicated client library over raw HTTP** — Initially built with raw `requests.post()` calls, later migrated to `huggingface_hub.InferenceClient` after discovering Hugging Face restructured their API into a multi-provider routing system. The client library abstracts away authentication headers, JSON formatting, and response decoding.

**Graceful degradation on API errors** — Specific handling for HTTP 503 (model loading) with a friendly wait message, plus a broad exception catch for unexpected failures, so the app never crashes mid-demo.

## 🚀 Running Locally

1. Clone the repo
```bash
git clone https://github.com/manveetshetty/astramind-image-ai.git
cd astramind-image-ai
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file
```
HF_API_KEY=your_huggingface_token_here
```

Get a token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — create a fine-grained token with **"Make calls to Inference Providers"** permission enabled.

4. Run the app
```bash
streamlit run app.py
```

## 🔐 Adding Your API Key (Deployment)

When deploying on **Streamlit Community Cloud**, do not upload your `.env` file. Instead:

1. Go to your app's **Settings → Secrets** in Streamlit Cloud
2. Add:
```toml
HF_API_KEY = "your_huggingface_token_here"
```
3. The app reads this automatically — no code change needed since `os.getenv("HF_API_KEY")` works identically with Streamlit Secrets

## ⚠️ Known Limitation

**Hugging Face free-tier accounts receive only $0.10 in monthly Inference Provider credits** — enough for roughly 2-5 image generations depending on the model and provider used. Once exhausted, the API returns a `402 Payment Required` error until the next billing cycle or until pre-paid credits are purchased. For consistent production use, a Hugging Face PRO subscription (20x more included usage) or a paid provider account is recommended.

## 🔮 Future Improvements
- Negative prompt input to exclude unwanted elements
- Image size / aspect ratio selector
- Multiple image generation per request
- Random prompt generator for inspiration
- Dark/light theme toggle
- Export gallery as a downloadable ZIP

## 👤 Author
Manveeth J Shetty — Third year CSE student at Manipal Institute of Technology
