
import streamlit as st
import sys
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.planner import Planner
from src.executor import Executor
from src.memory import Memory
from src.insight import Insight

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MotivAgentWeb:
    def __init__(self):
        if 'planner' not in st.session_state:
            st.session_state.planner = Planner()
            st.session_state.executor = Executor()
            st.session_state.memory = Memory()
            st.session_state.insight = Insight(st.session_state.memory)

    def run(self):
        st.set_page_config(
            page_title="🤖 MotivAgent",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Enhanced minimalist CSS with better contrast and harmony
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .main-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2.5rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            text-align: center;
            border: none;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }
        
        .main-header h1 {
            color: #1a202c;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
            letter-spacing: -1px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header h3 {
            color: #4a5568;
            margin: 0.5rem 0;
            font-weight: 400;
            font-size: 1.1rem;
        }
        
        .main-header p {
            color: #718096;
            margin: 0;
            font-weight: 300;
            font-style: italic;
        }
        
        .metric-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border: none;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        .metric-container h2 {
            font-size: 1.8rem;
            margin: 0 0 0.5rem 0;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        }
        
        .metric-container h3 {
            color: #2d3748;
            margin: 0.5rem 0;
            font-weight: 600;
            font-size: 1.4rem;
        }
        
        .metric-container p {
            color: #4a5568;
            margin: 0;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .activity-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .activity-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        .activity-card h4 {
            color: #1a202c;
            margin: 0 0 1rem 0;
            font-weight: 600;
        }
        
        .productivity-high {
            border-left-color: #48bb78 !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(72, 187, 120, 0.05) 100%);
        }
        
        .productivity-medium {
            border-left-color: #ed8936 !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(237, 137, 54, 0.05) 100%);
        }
        
        .productivity-low {
            border-left-color: #f56565 !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(245, 101, 101, 0.05) 100%);
        }
        
        .roast-message {
            background: linear-gradient(135deg, #fef5e7 0%, #fed7d7 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid #f56565;
            margin: 1rem 0;
            color: #2d3748;
            box-shadow: 0 2px 10px rgba(245, 101, 101, 0.1);
        }
        
        .sidebar-content {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border: none;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        }
        
        .insight-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: none;
            border-left: 4px solid #805ad5;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(128, 90, 213, 0.05) 100%);
        }
        
        .insight-card h3 {
            color: #1a202c;
            margin: 0 0 1rem 0;
            font-weight: 600;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: none;
            border-bottom: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.7);
            color: #4a5568;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        /* Enhanced Streamlit component overrides */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        }
        
        .stTextArea > div > div > textarea {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div > div > div {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
        }
        
        .stRadio > div {
            background: rgba(255, 255, 255, 0.8);
            padding: 1rem;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
        
        /* Enhanced progress bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Clean Header
        st.markdown("""
        <div class="main-header">
            <h1>MotivAgent</h1>
            <h3>Your Personal Activity Coach</h3>
            <p>Track, analyze, and improve your daily habits</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean Sidebar
        with st.sidebar:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.markdown("### Statistics")
            
            streak_info = st.session_state.memory.get_streak_info()
            
            # Clean metrics
            st.markdown(f"""
            <div class="metric-container">
                <h2 style="color: #e74c3c;">🔥</h2>
                <h3>{streak_info['current_streak']}</h3>
                <p>Current Streak</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-container">
                <h2 style="color: #3498db;">📊</h2>
                <h3>{streak_info['total_sessions']}</h3>
                <p>Total Sessions</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-container">
                <h2 style="color: #27ae60;">🏆</h2>
                <h3>{streak_info['longest_streak']}</h3>
                <p>Best Streak</p>
            </div>
            """, unsafe_allow_html=True)
            
            if streak_info['is_streak_broken']:
                st.markdown(f"""
                <div class="metric-container" style="border-left: 3px solid #e74c3c;">
                    <h2 style="color: #e74c3c;">⏰</h2>
                    <h3>{streak_info['days_inactive']}</h3>
                    <p>Days Inactive</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Progress visualization
            if streak_info['current_streak'] > 0:
                progress = min(streak_info['current_streak'] / 30, 1.0)  # 30-day goal
                st.markdown("### 🎯 Progress to 30-Day Goal")
                st.progress(progress)
                st.write(f"{int(progress * 100)}% Complete")
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["Log Activities", "Weekly Insights", "Test Mode"])
        
        with tab1:
            self.activity_logger()
        
        with tab2:
            self.weekly_insights()
            
        with tab3:
            self.test_mode()

    def activity_logger(self):
        st.markdown("### Daily Activity Log")
        
        # Input methods
        input_method = st.radio(
            "Input Method",
            ["Text Input", "Quick Actions"],
            horizontal=True
        )
        
        if input_method == "Text Input":
            st.markdown("#### Describe your activities")
            user_input = st.text_area(
                "Activities",
                placeholder="e.g., 'walked 45 minutes, studied for 2 hours, watched 1 episode of a show'",
                height=100,
                help="Be specific about duration and activities for better tracking"
            )
            
            if st.button("Analyze Activities", type="primary", use_container_width=True):
                if user_input.strip():
                    self.process_activities(user_input)
                else:
                    st.warning("Please enter some activities to analyze")
        
        else:
            st.markdown("#### Quick Activity Buttons")
            st.markdown("*One-click activity logging*")
            
            quick_activities = [
                ("Morning Walk", "walked 30 minutes", "🚶"),
                ("Study Session", "studied for 1 hour", "📚"),
                ("Exercise", "worked out for 45 minutes", "💪"),
                ("Reading", "read for 30 minutes", "📖"),
                ("Meditation", "meditated for 20 minutes", "🧘"),
                ("Cooking", "cooked for 30 minutes", "🍳"),
                ("Screen Time", "watched shows for 2 hours", "📺"),
                ("Gaming", "played games for 1 hour", "🎮"),
                ("Social Media", "browsed social media for 1 hour", "📱")
            ]
            
            cols = st.columns(3)
            for i, (button_text, activity_text, icon) in enumerate(quick_activities):
                col = cols[i % 3]
                if col.button(f"{icon} {button_text}", use_container_width=True):
                    self.process_activities(activity_text)

    def process_activities(self, user_input):
        with st.spinner("🧠 Analyzing your life choices... This might sting a little..."):
            # Parse activities
            activities = st.session_state.planner.parse_input(user_input)
            
            # Process with executor
            processed = st.session_state.executor.process_activities(activities)
            
            # Store in memory
            st.session_state.memory.store_session(processed)
            
            # Display results with enhanced styling
            st.success("✅ Analysis Complete! Brace yourself...")
            
            total_calories = sum(a['calories_burned'] for a in processed)
            avg_productivity = sum(a['productivity_score'] for a in processed) / len(processed)
            
            # Enhanced summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #ff6b6b;">🔥</h2>
                    <h3>{total_calories}</h3>
                    <p>Calories Burned</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                color = "#4caf50" if avg_productivity >= 7 else "#ff9800" if avg_productivity >= 4 else "#f44336"
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: {color};">📊</h2>
                    <h3>{avg_productivity:.1f}/10</h3>
                    <p>Avg Productivity</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #667eea;">📝</h2>
                    <h3>{len(processed)}</h3>
                    <p>Activities</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                total_time = sum(a['duration'] for a in processed)
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #764ba2;">⏰</h2>
                    <h3>{total_time}</h3>
                    <p>Total Minutes</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Individual activity results with enhanced cards
            st.markdown("### 🎭 RoastBot's Individual Verdicts")
            
            for i, activity in enumerate(processed, 1):
                productivity_class = "productivity-high" if activity['productivity_score'] >= 7 else \
                                   "productivity-medium" if activity['productivity_score'] >= 4 else "productivity-low"
                
                st.markdown(f"""
                <div class="activity-card {productivity_class}">
                    <h4>📌 Activity {i}: {activity['text']}</h4>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <div>
                            <strong>Category:</strong> {activity['category'].title()}<br>
                            <strong>Duration:</strong> {activity['duration']} minutes<br>
                            <strong>Intensity:</strong> {activity['intensity'].title()}
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #ff6b6b;"><strong>{activity['calories_burned']} kcal</strong></div>
                            <div style="color: #667eea;"><strong>{activity['productivity_score']}/10</strong></div>
                        </div>
                    </div>
                    <div class="roast-message">
                        <strong>🎭 RoastBot Says:</strong><br>
                        {activity['motivation_message']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def weekly_insights(self):
        st.markdown("### Weekly Overview")
        
        insights = st.session_state.insight.analyze_weekly_trends()
        weekly_summary = st.session_state.memory.get_weekly_summary()
        
        # Clean summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            ("📊", "Activities", weekly_summary.get('total_activities', 0), "#3498db"),
            ("🔥", "Calories", f"{weekly_summary.get('total_calories', 0)}", "#e74c3c"),
            ("⭐", "Avg Score", f"{weekly_summary.get('avg_productivity', 0):.1f}/10", "#27ae60"),
            ("📈", "Trend", insights['trend'].title(), "#9b59b6")
        ]
        
        for col, (icon, label, value, color) in zip([col1, col2, col3, col4], metrics):
            col.markdown(f"""
            <div class="metric-container">
                <h2 style="color: {color};">{icon}</h2>
                <h3>{value}</h3>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Weekly summary
        st.markdown(f"""
        <div class="insight-card">
            <h3>Weekly Summary</h3>
            <p>{insights['roast_summary']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for insights and breakdown
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 💡 Key Insights")
            for insight in insights['insights']:
                st.markdown(f"• {insight}")
        
        with col2:
            st.markdown("### 📋 Activity Breakdown")
            if insights['category_analysis']['breakdown']:
                breakdown_data = []
                for category, stats in insights['category_analysis']['breakdown'].items():
                    breakdown_data.append({
                        'Category': category.title(),
                        'Count': stats['count'],
                        'Time (min)': stats['total_time']
                    })
                
                df = pd.DataFrame(breakdown_data)
                
                # Create a pie chart
                fig = px.pie(df, values='Count', names='Category', 
                           title="Activity Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Suggestions with enhanced styling
        suggestions = st.session_state.insight.suggest_improvements()
        st.markdown("### 🎯 Improvement Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        border-left: 4px solid #2196f3;">
                <strong>{i}.</strong> {suggestion}
            </div>
            """, unsafe_allow_html=True)

    def test_mode(self):
        st.markdown("### Test Scenarios")
        st.markdown("*Try different activity patterns to see how the system responds*")
        
        test_scenarios = [
            ("Active Day", "ran 5 miles, did 100 push-ups, and meal prepped for the week"),
            ("Study Focus", "studied calculus for 4 hours straight with breaks"),
            ("Gaming Session", "played video games for 8 hours"),
            ("Wellness Day", "meditated for 1 hour, did yoga, and journaled"),
            ("Entertainment", "watched entire season of a show"),
            ("Work Day", "worked 12 hours and answered emails"),
            ("Creative Time", "painted for 3 hours, played guitar, and wrote"),
            ("Relaxation", "took it easy and rested all day")
        ]
        
        cols = st.columns(2)
        for i, (title, scenario) in enumerate(test_scenarios):
            col = cols[i % 2]
            with col:
                if st.button(f"{title}", key=f"test_{i}", use_container_width=True):
                    st.markdown(f"**Testing scenario:** *{scenario}*")
                    self.process_activities(scenario)

if __name__ == "__main__":
    app = MotivAgentWeb()
    app.run()
