# Kelly - AI Skeptical Poet Chatbot 🧪

A Streamlit chatbot where Kelly, a skeptical AI scientist-poet, responds to questions about AI in the form of analytical, cautious poems.

## Features

- 🎭 **Poetic Responses**: Every answer is a poem
- 🔬 **Skeptical Analysis**: Questions AI hype and highlights limitations
- 📊 **Practical Guidance**: Ends with concrete, actionable steps
- ⚡ **Powered by Groq**: Uses Llama 3.3 70B for fast inference

## Project Structure

```
kelly/
├── app.py                      # Main application entry point
├── src/
│   ├── api_manager.py         # API key management
│   ├── config.py              # Configuration and prompts
│   ├── poem_generator.py      # Poem generation logic
│   ├── ui_components.py       # Streamlit UI components
│   └── utils.py               # Utility functions
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml           # API keys (not in git)
├── .env                        # Environment variables (not in git)
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version
└── README.md                   # This file
```

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AkshayAshok/kelly.git
   cd kelly
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**
   
   Create a `.env` file:
   ```bash
   Groq_API_KEY=your_groq_api_key_here
   ```
   
   Or create `.streamlit/secrets.toml`:
   ```toml
   Groq_API_KEY = "your_groq_api_key_here"
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Deployment

### Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Add environment variable: `Groq_API_KEY`
5. Deploy!

### Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Add secret in dashboard: `Groq_API_KEY = "your_key"`
4. Deploy!

## Usage

1. Open the app
2. Type a question about AI (e.g., "What do you think about GPT-4?")
3. Kelly responds with a skeptical, analytical poem
4. Export your conversation as a text file

## Configuration

Modify Kelly's behavior in `src/config.py`:
- System prompt
- Default guiding principles
- Temperature and model settings (in `poem_generator.py`)

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Groq API (Llama 3.3 70B)
- **Language**: Python 3.12
- **Deployment**: Render / Streamlit Cloud

## License

MIT License

## Author

AkshayAshok

---

**Kelly**: *"Question assumptions, test your claims, and always show your work."* 🧪
