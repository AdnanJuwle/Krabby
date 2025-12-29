# 🏛️ Council of LLM Models - Parliamentary System

A democratic AI system where multiple LLM models work together like a parliament to reach consensus on questions and topics through discussion and voting.

---

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Setup](#step-by-step-setup)
- [Configuration](#-configuration)
  - [API Keys Setup](#api-keys-setup)
  - [Ollama Setup (Optional)](#ollama-setup-optional)
  - [Environment Variables](#environment-variables)
- [Usage](#-usage)
  - [GUI Application (Recommended)](#gui-application-recommended)
  - [Command Line Interface](#command-line-interface)
- [How It Works](#-how-it-works)
- [Model Providers](#-model-providers)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-frequently-asked-questions)
- [Contributing](#-contributing)

---

## ✨ Features

- 🤖 **Multiple Models**: Supports Ollama (local), Groq, Hugging Face, Together AI, and Cohere
- 🔒 **Anonymized Voting**: Models vote on anonymous opinions to prevent bias
- 🗳️ **Democratic Process**: Each model votes independently, majority wins
- 💬 **Discussion Rounds**: Models discuss and refine opinions before voting (2 rounds by default)
- 🆓 **Free APIs**: Uses free tiers of various AI services
- 🎨 **Modern GUI**: Beautiful desktop application with real-time progress tracking
- 📊 **Detailed Results**: View all opinions, discussions, and voting breakdowns
- 💾 **Export Results**: Save deliberation results to JSON for analysis

---

## 🚀 Quick Start

**For users who want to get started immediately:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (at least one):
   - Copy `env.example` to `.env`
   - Add at least one API key (see [API Keys Setup](#api-keys-setup))

3. **Run the GUI:**
   ```bash
   python main_gui.py
   ```
   Or double-click `run_council.bat` on Windows.

**That's it!** The system will automatically detect available models and start working.

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** (Python 3.9 or higher recommended)
- **pip** (Python package manager)
- **Internet connection** (for API-based models)
- **API keys** (for at least one provider - see below)

### Step-by-Step Setup

#### 1. Clone or Download the Project

If you have the project files, navigate to the project directory:
```bash
cd Krabby
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** On some systems, you may need to use `pip3` instead of `pip`.

#### 3. Verify Installation

Check that all packages installed correctly:
```bash
python -c "import ollama, groq, cohere; print('✓ All dependencies installed')"
```

---

## ⚙️ Configuration

### API Keys Setup

The system supports multiple AI providers. You need at least **one API key** to get started.

#### Step 1: Create `.env` File

Copy the example environment file:
```bash
# On Windows (PowerShell)
Copy-Item env.example .env

# On Linux/Mac
cp env.example .env
```

#### Step 2: Get API Keys

Choose one or more providers and get free API keys:

| Provider | Free Tier | Get API Key |
|----------|-----------|-------------|
| **Groq** | ✅ Yes (Very Fast) | [Get Key](https://console.groq.com/keys) |
| **Hugging Face** | ✅ Yes | [Get Key](https://huggingface.co/settings/tokens) |
| **Together AI** | ✅ Yes | [Get Key](https://api.together.xyz/settings/api-keys) |
| **Cohere** | ✅ Yes | [Get Key](https://dashboard.cohere.com/api-keys) |
| **Google Gemini** | ✅ Yes | [Get Key](https://makersuite.google.com/app/apikey) |

#### Step 3: Add Keys to `.env`

Open `.env` in a text editor and add your keys:

```env
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
TOGETHER_API_KEY=your_together_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

**Important:** 
- Replace `your_*_api_key_here` with your actual API keys
- Don't share your `.env` file or commit it to version control
- You only need **one** API key to get started, but more models = better results

### Ollama Setup (Optional)

Ollama allows you to run models **locally** without API keys. This is completely optional but recommended for privacy and offline use.

#### Install Ollama

1. **Download Ollama:**
   - Visit: https://ollama.ai
   - Download for your operating system
   - Install the application

2. **Verify Installation:**
   ```bash
   ollama --version
   ```

3. **Start Ollama Service:**
   ```bash
   # On Windows: Usually starts automatically
   # On Linux/Mac: Run in terminal
   ollama serve
   ```

4. **Download Models:**
```bash
ollama pull llama3.2
ollama pull mistral
ollama pull phi3
```

5. **Verify Models:**
   ```bash
   ollama list
   ```

**Note:** Ollama models work offline and don't require API keys, but they need sufficient RAM (4GB+ recommended per model).

### Environment Variables

You can customize the council behavior using environment variables in your `.env` file:

```env
# Discussion rounds (default: 2)
COUNCIL_DISCUSSION_ROUNDS=2

# Voting mode (default: majority)
COUNCIL_VOTING_MODE=majority

# Ollama base URL (default: http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434

# Model timeout in seconds (default: 60)
MODEL_TIMEOUT=60

# Maximum retry attempts (default: 3)
MAX_RETRIES=3
```

---

## 💻 Usage

### GUI Application (Recommended)

The GUI provides a modern, user-friendly interface with real-time progress tracking.

#### Windows:
```bash
python main_gui.py
```
Or simply double-click `run_council.bat`

#### Linux/Mac:
```bash
python main_gui.py
```
Or use the shell script:
```bash
bash run_council.sh
```

#### GUI Features:
- 📝 **Input Panel**: Enter your question or topic
- 📊 **Status Panel**: See which models are available
- 🏆 **Results Tabs**: 
  - **Final Output**: The winning opinion
  - **All Opinions**: See what each model initially thought
  - **Voting Results**: Detailed vote breakdown
- 💾 **Export**: Save results to JSON
- 🗑️ **Clear**: Reset and start over

### Command Line Interface

For users who prefer the terminal or want to automate the process:

```bash
python main.py
```

The CLI will:
1. Check Ollama connection
2. Check API keys
3. Show available models
4. Prompt for your question
5. Display results
6. Optionally save results to JSON

**Example Session:**
```
Enter your question or topic for the council: 
What is the best approach to learn machine learning?

Step 1: Gathering initial opinions from all models...
Step 2.1: Discussion round 1...
Step 2.2: Discussion round 2...
Step 3: Models are voting...
Step 4: Counting votes...

FINAL OUTPUT (WINNING OPINION):
[The winning opinion will be displayed here]
```

---

## 🔄 How It Works

The Council system uses a democratic process to reach consensus:

1. **📥 Input Phase**: All models receive the same question/topic
2. **💭 Initial Opinions**: Each model independently generates its own opinion
3. **🔒 Anonymization**: Opinions are assigned random IDs and shuffled to prevent bias
4. **💬 Discussion Rounds**: Models review all anonymous opinions and discuss (default: 2 rounds)
5. **🗳️ Voting Phase**: Each model votes for the best opinion (without knowing who wrote it)
6. **🏆 Output**: The opinion with the most votes wins and becomes the final output

**Why Anonymization?** 
By hiding which model wrote which opinion, we prevent models from voting based on reputation or bias. They must evaluate opinions purely on merit.

---

## 🤖 Model Providers

| Provider | Type | API Key Required | Speed | Best For |
|----------|------|------------------|-------|----------|
| **Ollama** | Local | ❌ No | Medium | Privacy, offline use |
| **Groq** | Cloud | ✅ Yes | ⚡ Very Fast | Quick responses |
| **Hugging Face** | Cloud | ✅ Yes | Medium | Variety of models |
| **Together AI** | Cloud | ✅ Yes | Fast | High-quality models |
| **Cohere** | Cloud | ✅ Yes | Fast | Business applications |
| **Google Gemini** | Cloud | ✅ Yes | Fast | Google ecosystem |

**Recommendation:** Start with **Groq** (fastest) or **Ollama** (no API key needed).

---

## 📁 Project Structure

```
Krabby/
├── council/                    # Main council package
│   ├── __init__.py
│   ├── council.py             # Main council orchestration logic
│   ├── models.py              # Model wrappers for different providers
│   ├── anonymizer.py          # Opinion anonymization system
│   ├── voting.py              # Voting system implementation
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── logging.py         # Logging configuration
│       └── validation.py      # Input validation
├── config.py                  # Configuration and model list
├── main.py                    # CLI entry point
├── main_gui.py                # GUI entry point
├── requirements.txt           # Python dependencies
├── env.example                # Environment variables template
├── .env                       # Your API keys (create from env.example)
├── run_council.bat            # Windows launcher
├── run_council.sh             # Linux/Mac launcher
├── README.md                  # This file
└── WHY_ONLY_3_MODELS.md       # Troubleshooting guide
```

---

## 📝 Examples

### Example 1: Learning Question

**Question:** "What is the best approach to learn machine learning?"

**Process:**
- 5 models generate initial opinions
- Models discuss and refine opinions (2 rounds)
- Models vote on the best approach
- Winning opinion is returned

### Example 2: Decision Making

**Question:** "Should I use Python or JavaScript for a new web project?"

**Process:**
- Each model provides pros/cons
- Models debate the trade-offs
- Final consensus recommendation

### Example 3: Creative Problem Solving

**Question:** "How can I improve my productivity while working from home?"

**Process:**
- Diverse perspectives from different models
- Discussion leads to comprehensive solution
- Voted best practices emerge

---

## 🔧 Troubleshooting

### Problem: "No models are available"

**Solutions:**
1. **Check API Keys:**
   - Verify your `.env` file exists
   - Ensure at least one API key is set
   - Check that keys are not expired

2. **Check Ollama (if using local models):**
   ```bash
   ollama list
   ```
   If empty, pull models:
   ```bash
   ollama pull llama3.2
   ```

3. **Verify Ollama is Running:**
   ```bash
   # Test connection
   python -c "import ollama; print(ollama.Client().list())"
   ```

### Problem: "Ollama models not detected"

**Solutions:**
1. **Start Ollama Service:**
   ```bash
   ollama serve
   ```

2. **Check Windows Task Manager** for "ollama" process

3. **Verify Models are Installed:**
   ```bash
   ollama list
   ```

4. **Restart the Application** after starting Ollama

See `WHY_ONLY_3_MODELS.md` for more details.

### Problem: API Errors

**Solutions:**
1. **Check Internet Connection**
2. **Verify API Key is Valid:**
   - Test key on provider's website
   - Check for typos in `.env` file
3. **Check API Rate Limits:**
   - Free tiers have usage limits
   - Wait a few minutes and try again
4. **Verify API Key Format:**
   - No extra spaces
   - No quotes around the key
   - Correct variable name

### Problem: "Module not found" errors

**Solutions:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use pip3
pip3 install -r requirements.txt
```

### Problem: GUI won't open

**Solutions:**
1. **Check Python Version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Install Tkinter** (usually included, but some Linux distros need it):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   ```

---

## ❓ Frequently Asked Questions

### Q: Do I need all API keys?

**A:** No! You only need **one** API key to get started. More models = better results, but one is enough.

### Q: Which provider should I use?

**A:** 
- **Beginners:** Start with **Groq** (fastest, easy setup)
- **Privacy-conscious:** Use **Ollama** (runs locally, no API key)
- **Best results:** Use multiple providers for diverse perspectives

### Q: How many models do I need?

**A:** Minimum 2 models for voting to work. Recommended 3-5 models for good consensus.

### Q: Is it free?

**A:** Yes! All providers offer free tiers. Ollama is completely free and runs locally.

### Q: Can I use this offline?

**A:** Yes, if you use **Ollama** models. Cloud-based models (Groq, etc.) require internet.

### Q: How long does it take?

**A:** Depends on:
- Number of models (more = longer)
- Discussion rounds (default: 2)
- Model speed (Groq is fastest)
- Typically 30 seconds to 2 minutes

### Q: Can I customize the voting system?

**A:** Yes! Edit `config.py` or set `COUNCIL_VOTING_MODE` in `.env`.

### Q: How do I add more models?

**A:** Edit `config.py` and add model configurations to the `MODELS` list.

### Q: Can I save results?

**A:** Yes! 
- **GUI:** Click "Export Results" button
- **CLI:** Answer 'y' when prompted

### Q: What if a model fails?

**A:** The system automatically skips failed models and continues with available ones.

---

## 🤝 Contributing

Contributions are welcome! Here are some ways to help:

1. **Report Bugs:** Open an issue with details
2. **Suggest Features:** Share your ideas
3. **Improve Documentation:** Fix typos, add examples
4. **Add Model Providers:** Extend support for new AI services
5. **Optimize Performance:** Improve speed and efficiency

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

## 🎯 Quick Reference

**Start GUI:**
```bash
python main_gui.py
```

**Start CLI:**
```bash
python main.py
```

**Check Models:**
```bash
python main.py  # Shows available models
```

**Test Ollama:**
```bash
ollama list
```

**Get API Keys:**
- Groq: https://console.groq.com/keys
- Hugging Face: https://huggingface.co/settings/tokens
- Together AI: https://api.together.xyz/settings/api-keys
- Cohere: https://dashboard.cohere.com/api-keys

---

**Need Help?** Check the [Troubleshooting](#-troubleshooting) section or open an issue!

