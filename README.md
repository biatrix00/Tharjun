
# 🤖 MotivAgent - Your Sarcastic Life Coach

**ODSC Agentic AI Hackathon 2025 Entry**

> "Motivation with a side of roast" - Making habit tracking actually entertaining through AI-powered sarcasm

## 🎯 Problem Statement

Traditional fitness and productivity apps are **boring, generic, and forgettable**. Users lose motivation because feedback lacks personality and engagement. MotivAgent solves this by providing **AI-powered sarcastic motivation** that makes daily activity logging fun and memorable.

## 🚀 Live Demo

- **Web Interface**: Still under process...
- **CLI Version**: Run `python main.py` for command-line interface
- **Demo Video**: [GO through Demo](DEMO.md)

## ✨ Key Features

### 🎭 Sarcastic AI Personality
- Powered by Google Gemini API with custom "RoastBot" prompts
- Context-aware responses based on activity type and productivity
- Consistent personality that's savage but ultimately motivational

### 🧠 Intelligent Activity Parsing
- Natural language processing: "walked 30 min and watched 3 Netflix episodes"
- Automatic categorization (exercise, study, entertainment, etc.)
- Duration extraction, intensity assessment, and mood detection

### 📊 Smart Analytics & Insights
- Real-time calorie calculations with intensity modifiers
- Productivity scoring (1-10 scale) based on activity value
- Weekly trend analysis and personalized improvement suggestions

### 🔥 Gamified Streak Tracking
- Consecutive day tracking with break detection
- Personal records and achievement milestones
- Visual progress indicators and goal setting

### 🌐 Dual Interface
- **Web App**: Modern Streamlit dashboard with glassmorphism UI
- **CLI**: Interactive command-line interface for power users

## 🔧 Agentic AI Architecture

```
User Input → Planner → Executor → Memory → Insights
     ↓         ↓         ↓        ↓        ↓
  Parse    Calculate  Generate   Store   Analyze
Activities Calories   Roasts    Data    Trends
```

### Planning Agent (`src/planner.py`)
- **Natural Language Understanding**: Converts free-form text into structured activities
- **Smart Classification**: Categorizes activities using keyword matching and context
- **Temporal Parsing**: Extracts duration, time patterns, and intensity levels

### Execution Agent (`src/executor.py`)
- **Gemini Integration**: Custom prompts for context-aware sarcastic responses
- **Fallback Intelligence**: Local response generation when API unavailable
- **Multi-modal Processing**: Handles calories, productivity, and motivation simultaneously

### Memory Agent (`src/memory.py`)
- **Persistent Storage**: JSON-based activity logs and user statistics
- **Streak Logic**: Complex consecutive day tracking with break detection
- **Historical Analysis**: Maintains weekly trends and performance patterns

### Insight Agent (`src/insight.py`)
- **Trend Detection**: Identifies productivity patterns over time
- **Behavioral Analysis**: Suggests improvements based on activity history
- **Roast Synthesis**: Generates weekly performance commentary

## 🛠️ Technical Excellence

- **Modular Architecture**: Clean separation of concerns for maintainability
- **Error Resilience**: Graceful handling of API failures and edge cases
- **Extensible Design**: Easy to add new activity types and response patterns
- **Real-time Processing**: Immediate feedback with sub-second response times

## 🏃‍♂️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/MotivAgent.git
   cd MotivAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API (optional)**
   ```bash
   # Add to .env file
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   # Web interface
   streamlit run app.py --server.port=5000

   # CLI interface
   python main.py
   ```

## 📈 Innovation Highlights

### Creative Gemini Integration
- **Custom Personality Engineering**: Specialized "RoastBot" character with consistent voice
- **Context-Aware Responses**: Different roast styles for exercise vs. entertainment
- **Adaptive Feedback**: Responses scale with productivity levels (praise vs. roast)

### Advanced NLP Capabilities
- **Multi-Activity Parsing**: Handles complex inputs like "walked 20 min, studied 2 hours, watched Netflix"
- **Confidence Scoring**: Self-assessment of parsing accuracy for quality control
- **Context Extraction**: Detects location, social context, and emotional state

### Intelligent Fallbacks
- **Offline Functionality**: Works without internet connection
- **API Failure Recovery**: Seamless degradation to local responses
- **Data Persistence**: Never loses user progress or streaks

## 🎖️ Hackathon Criteria Alignment

### Technical Excellence ⭐⭐⭐⭐⭐
- Robust error handling and edge case management
- Clean, maintainable code architecture
- Comprehensive testing suite (`TEST.sh`)

### Solution Architecture & Documentation ⭐⭐⭐⭐⭐
- Clear modular design with ASCII diagrams
- Comprehensive documentation (README, ARCHITECTURE, EXPLANATION)
- Well-commented code with inline documentation

### Innovative Gemini Integration ⭐⭐⭐⭐⭐
- Novel "sarcastic life coach" personality implementation
- Creative prompt engineering for consistent character voice
- Efficient API usage with intelligent caching and fallbacks

### Societal Impact & Novelty ⭐⭐⭐⭐⭐
- Addresses real problem: boring, ineffective habit tracking
- Novel approach: entertainment-driven motivation
- Potential for widespread adoption and positive behavioral change

## 📁 Project Structure

```
MotivAgent/
├── src/                    # Core agent modules
│   ├── planner.py         # Activity parsing and classification
│   ├── executor.py        # Gemini integration and processing
│   ├── memory.py          # Data persistence and streak tracking
│   └── insight.py         # Analytics and trend analysis
├── data/                  # User data storage
├── main.py               # CLI interface
├── app.py                # Streamlit web interface
├── ARCHITECTURE.md       # Technical architecture overview
├── EXPLANATION.md        # Detailed technical explanation
├── DEMO.md              # Demo video and highlights
└── TEST.sh              # Testing suite
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
chmod +x TEST.sh
./TEST.sh
```

## 🔮 Future Roadmap

- **Social Features**: Share roasts and compete with friends
- **Goal Setting**: User-defined targets and achievement tracking
- **Advanced Analytics**: Machine learning for personalized insights
- **Mobile App**: Native iOS/Android applications
- **Integration APIs**: Connect with fitness trackers and productivity tools

## 🏆 Awards & Recognition

- **ODSC Agentic AI Hackathon 2025** - Submission Entry
- **Innovation in AI Personality** - Candidate
- **Best Use of Gemini API** - Candidate

---

**Built with ❤️ and 🤖 for the ODSC Agentic AI Hackathon 2025**

*Making personal development fun, one roast at a time.*
