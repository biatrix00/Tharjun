
# MotivAgent Architecture Overview

## ASCII Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (CLI)                     │
│                        main.py                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT CORE                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   PLANNER   │  │  EXECUTOR   │  │   MEMORY    │         │
│  │ planner.py  │  │executor.py  │  │ memory.py   │         │
│  │             │  │             │  │             │         │
│  │ Parse input │  │ Generate    │  │ Store logs  │         │
│  │ Structure   │  │ motivation  │  │ Track       │         │
│  │ activities  │  │ Calculate   │  │ streaks     │         │
│  └─────────────┘  │ calories    │  └─────────────┘         │
│                   └─────┬───────┘                          │
│                         │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                INSIGHT ENGINE                       │   │
│  │                 insight.py                          │   │
│  │              Weekly trends analysis                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL APIS & TOOLS                          │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   GEMINI API    │    │  LOCAL STORAGE  │                │
│  │                 │    │                 │                │
│  │ Sarcastic       │    │ JSON files      │                │
│  │ motivation      │    │ activity_logs   │                │
│  │ generation      │    │ user_stats      │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. **User Interface (CLI)**
- **File**: `main.py`
- **Function**: Interactive command-line interface
- **Features**: 
  - Direct input mode: `python main.py "activity description"`
  - Interactive mode with menu system
  - Streak tracking display
  - Weekly insights viewer

### 2. **Agent Core**

#### **Planner** (`src/planner.py`)
- **Purpose**: Parse natural language input into structured activity data
- **Key Functions**:
  - `parse_input()`: Convert user text to activity objects
  - Activity classification (exercise, study, entertainment, etc.)
  - Duration extraction using regex patterns
  - Intensity and mood assessment

#### **Executor** (`src/executor.py`)
- **Purpose**: Process activities and generate responses
- **Key Functions**:
  - `process_activities()`: Main processing pipeline
  - `_calculate_calories()`: Estimate energy expenditure
  - `_generate_motivation()`: Call Gemini API for sarcastic responses
  - Fallback motivation when API unavailable
- **Gemini Integration**: Uses generateContent endpoint with custom roast prompts

#### **Memory** (`src/memory.py`)
- **Purpose**: Persistent storage and streak tracking
- **Key Functions**:
  - `store_session()`: Save daily activities
  - `_calculate_current_streak()`: Track consecutive active days
  - `get_weekly_summary()`: Aggregate statistics
- **Storage**: JSON files in `data/` directory

#### **Insight Engine** (`src/insight.py`)
- **Purpose**: Advanced analytics and trend analysis
- **Key Functions**:
  - `analyze_weekly_trends()`: Productivity pattern detection
  - `_generate_weekly_roast()`: Summary motivation messages
  - `suggest_improvements()`: Actionable recommendations

### 3. **External Tools & APIs**

#### **Google Gemini API**
- **Endpoint**: `generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent`
- **Purpose**: Generate contextual sarcastic motivation
- **Fallback**: Local response generation when API unavailable

#### **Local Storage**
- **Files**: `activity_logs.json`, `user_stats.json`
- **Purpose**: Persistent data storage, streak tracking, analytics

### 4. **Observability**
- **Logging**: Console output for each processing step
- **Error Handling**: Graceful API failure recovery
- **Testing**: `TEST.sh` script for validation
- **Debugging**: Step-by-step activity processing display

## Data Flow

1. **Input** → User provides activity description
2. **Planning** → Parse and structure activities
3. **Execution** → Calculate calories + generate motivation
4. **Storage** → Save to memory with streak updates
5. **Insights** → Analyze trends and provide feedback
6. **Output** → Display roasts, calories, and productivity scores

## Key Design Decisions

- **Modular Architecture**: Separate concerns for maintainability
- **Fallback Systems**: Works without API access
- **JSON Storage**: Simple, human-readable persistence
- **Regex Parsing**: Flexible natural language processing
- **Sarcastic Personality**: Consistent "RoastBot" character throughout
