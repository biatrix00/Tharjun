
# MotivAgent Technical Explanation

## 1. Agent Workflow

MotivAgent processes user input through a structured pipeline:

1. **Receive User Input**: CLI accepts natural language activity descriptions
2. **Parse & Plan** (`planner.py`): 
   - Extract activities using regex patterns
   - Classify into categories (exercise, study, entertainment, etc.)
   - Estimate duration, intensity, and mood
3. **Execute & Generate** (`executor.py`):
   - Calculate calories burned using activity-specific rates
   - Call Gemini API with specialized "RoastBot" prompts
   - Generate sarcastic/motivational responses based on productivity
4. **Store & Track** (`memory.py`):
   - Save session data in JSON format
   - Update streak counters and statistics
   - Maintain historical activity logs
5. **Analyze & Insight** (`insight.py`):
   - Detect weekly productivity trends
   - Generate actionable suggestions
   - Create comprehensive roast summaries

## 2. Key Modules

### **Planner** (`src/planner.py`)
- **Core Function**: `parse_input(user_input) → List[Dict[activity_data]]`
- **Features**:
  - Activity classification using keyword matching
  - Duration extraction via regex: `(\d+)\s*(min|minutes|hour|hours)`
  - Intensity assessment (low/medium/high)
  - Mood detection from positive/negative keywords
  - Subtask identification for complex activities

### **Executor** (`src/executor.py`)
- **Core Function**: `process_activities(activities) → List[Dict[processed_data]]`
- **Gemini Integration**:
  - Custom "RoastBot" personality prompts
  - Context-aware sarcasm based on activity category
  - Fallback responses when API unavailable
- **Calorie Calculation**: Category-based rates with intensity multipliers
- **Productivity Scoring**: 1-10 scale based on activity value

### **Memory Store** (`src/memory.py`)
- **Storage Format**: JSON files in `data/` directory
  - `activity_logs.json`: Daily session history
  - `user_stats.json`: Aggregate statistics and streaks
- **Streak Logic**: Consecutive day tracking with break detection
- **Analytics**: Weekly summaries and category breakdowns

### **Insight Engine** (`src/insight.py`)
- **Trend Analysis**: Productivity trajectory over 7 days
- **Pattern Detection**: Dominant activity categories
- **Recommendation System**: Personalized improvement suggestions
- **Roast Generation**: Weekly summary with sarcastic commentary

## 3. Tool Integration

### **Google Gemini API**
- **Function**: `_call_gemini_api(prompt) → motivation_message`
- **Endpoint**: `generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent`
- **Prompt Template**:
```python
prompt = f"""
You're a savage AI life coach named *RoastBot*. The user shares what they did today. Your job:
- Praise them if they were productive (study, exercise, habit)
- Sarcastically insult them if they slacked (e.g. watched Netflix, did nothing)
- Respond in a short, funny, roast-style message (max 2 sentences)
- Never be boring

Activity: "{activity_text}"
Category: {category}
Duration: {duration} minutes
"""
```

### **Local JSON Storage**
- **Function**: `store_session(activities) → None`
- **Persistence**: Automatic file creation and management
- **Recovery**: Graceful handling of corrupted data

### **Calorie Calculator**
- **Function**: `_calculate_calories(activity) → int`
- **Rates**: Category-specific calories/minute (exercise: 8, study: 1, etc.)
- **Modifiers**: Intensity multipliers (low: 0.8x, high: 1.3x)

## 4. Observability & Testing

### **Logging Strategy**
- **Console Output**: Step-by-step processing visualization
- **Error Handling**: API failures with fallback activation
- **Debug Info**: Activity parsing details and calorie calculations

### **Testing Suite** (`TEST.sh`)
- **Module Imports**: Verify all components load correctly
- **Direct Input**: Test CLI with sample activity
- **Integration**: End-to-end workflow validation
- **Edge Cases**: Empty input and API failure scenarios

### **Traceability**
Judges can trace decisions through:
1. **Input Parsing**: View classified activities and extracted metadata
2. **API Calls**: See generated prompts and responses
3. **Calculations**: Calorie and productivity score breakdowns
4. **Storage**: Inspect JSON files for data persistence
5. **Insights**: Understand trend analysis logic

## 5. Known Limitations

### **Performance Bottlenecks**
- **API Latency**: Gemini calls can take 1-3 seconds per activity
- **File I/O**: JSON parsing for large history files
- **Memory Usage**: Loads entire activity history for analysis

### **Edge Cases**
- **Ambiguous Input**: "did stuff" → defaults to low-productivity "other"
- **Time Parsing**: Complex time expressions may not parse correctly
- **API Failures**: Network issues gracefully degrade to fallback responses
- **Empty Sessions**: Handles days with no activities

### **Accuracy Limitations**
- **Calorie Estimation**: Simplified calculations, not medical-grade
- **Activity Classification**: Keyword-based, may misclassify novel activities
- **Sarcasm Consistency**: API responses vary, fallbacks are static

### **Scale Limitations**
- **Local Storage**: JSON files become unwieldy with years of data
- **Concurrent Access**: No file locking for multi-user scenarios
- **API Quotas**: Gemini rate limits may affect heavy usage

### **User Experience**
- **CLI Only**: No web interface for broader accessibility
- **Setup Complexity**: Requires API key configuration
- **Error Messages**: Technical errors may confuse non-developers

## 6. Future Improvements

- **Web Interface**: Streamlit dashboard for better UX
- **Database Migration**: SQLite for better performance
- **Advanced NLP**: More sophisticated activity parsing
- **Goal Setting**: User-defined targets and achievement tracking
- **Social Features**: Share roasts and compete with friends
