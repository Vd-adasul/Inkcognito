# Content Generation & Humanization Pipeline

A fast Python project that generates high-quality, human-like content using Google Gemini API and then applies NLP-based humanization techniques.

## Features

- **Fast Content Generation**: Single API call to Gemini generates 2000-3000 word passages in seconds
- **Text Humanization**: Applies NLP techniques (synonym replacement, contraction expansion, academic transitions) to make AI-generated text appear more human-like
- **Modular Architecture**: Clean separation of concerns with configurable settings
- **No Model Downloads**: Fast startup - no heavy model loading required

## Project Structure

```
.
├── run.py                 # Main execution file
├── requirements.txt       # All dependencies
├── README.md             # Setup and usage instructions
├── config/               # Configuration files
│   └── config.py         # API keys and settings
├── models/               # (Empty - no local models needed)
└── src/                  # Source code modules
    ├── generator.py      # Fast content generation logic
    └── humanizer.py     # Text humanization logic
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd inkcognito
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables:**
   
   Create a `.env` file in the project root with your API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   Alternatively, you can set it as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Execution Command

```bash
python run.py "Your input prompt here"
```

### Example

```bash
python run.py "Write a detailed 2000-3000 word essay on climate change and renewable energy."
```

### How It Works

1. **Phase 1 - Fast Content Generation:**
   - Single API call to Google Gemini (gemini-2.5-flash)
   - Generates 2000-3000 word article based on your prompt
   - Uses optimized system prompt for quality output
   - Typically completes in 10-30 seconds

2. **Phase 2 - Text Humanization:**
   - Applies NLP transformations to the generated text:
     - Expands contractions (can't → can not, I'm → I am)
     - Replaces words with synonyms using WordNet
     - Adds academic transition phrases
     - Normalizes punctuation spacing
   - Processes text sentence-by-sentence for natural variation

## Configuration

You can modify settings in `config/config.py`:

- `GEMINI_MODEL`: Gemini model to use (default: "gemini-2.5-flash")
- `DEFAULT_P_SYN`: Synonym replacement probability (default: 1.0)
- `DEFAULT_P_TRANS`: Academic transition frequency (default: 1.0)

## Performance

- **Generation Time**: ~10-30 seconds (depends on Gemini API response time)
- **Humanization Time**: ~5-15 seconds (for 2000-3000 words)
- **Total Runtime**: ~15-45 seconds
- **No Model Loading**: Instant startup - no waiting for model downloads

## Notes

- The system uses Google Gemini API for generation - ensure you have API credits/quota
- NLTK and spaCy resources are downloaded automatically on first run
- The humanization process is CPU-bound and runs locally
- All processing happens in-memory - no disk I/O for models

## Troubleshooting

1. **"GEMINI_API_KEY is not set" error:**
   - Make sure you've created a `.env` file in the project root
   - Or set the environment variable: `export GEMINI_API_KEY=your_key`
   - Verify the key is valid and has API access

2. **NLTK resource errors:**
   - Resources download automatically on first run
   - If you see "punkt_tab not found", the code will auto-download it
   - Ensure you have internet connection for first-time setup

3. **spaCy model not found:**
   - Run: `python -m spacy download en_core_web_sm`
   - Or let the code auto-download it (may take a moment)

4. **API rate limit errors:**
   - Check your Gemini API quota/limits
   - Wait a few moments and try again
   - Consider upgrading your API plan if needed

5. **Import errors:**
   - Make sure you've activated your virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Ensure Python 3.8+ is being used

## License

This project is provided as-is for educational and research purposes.
