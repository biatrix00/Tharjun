
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
        
        # Custom CSS for enhanced styling
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            animation: fadeInUp 0.8s ease-out;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 3rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header h3 {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0;
            font-weight: 500;
        }
        
        .main-header p {
            color: rgba(255,255,255,0.8);
            margin: 0;
            font-style: italic;
        }
        
        .stats-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .activity-card {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
        }
        
        .activity-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .productivity-high {
            border-left-color: #4caf50 !important;
        }
        
        .productivity-medium {
            border-left-color: #ff9800 !important;
        }
        
        .productivity-low {
            border-left-color: #f44336 !important;
        }
        
        .roast-message {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #ff6b6b;
            font-style: italic;
            margin: 1rem 0;
        }
        
        .metric-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .quick-action-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .quick-action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        .sidebar-content {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        
        .insight-card {
            background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #8e44ad;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px 10px 0 0;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 10px;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Animated Header
        st.markdown("""
        <div class="main-header">
            <h1>🤖 MOTIVAGENT 🤖</h1>
            <h3>Your Sarcastic Life Coach</h3>
            <p>"Motivation with a side of roast"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Sidebar
        with st.sidebar:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.markdown("### 📊 Your Stats Dashboard")
            
            streak_info = st.session_state.memory.get_streak_info()
            
            # Animated metrics
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #667eea; margin: 0;">🔥</h2>
                    <h3 style="margin: 0.5rem 0;">{streak_info['current_streak']}</h3>
                    <p style="margin: 0; color: #666;">Current Streak</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #f093fb; margin: 0;">📝</h2>
                    <h3 style="margin: 0.5rem 0;">{streak_info['total_sessions']}</h3>
                    <p style="margin: 0; color: #666;">Total Sessions</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #4caf50; margin: 0;">🏆</h2>
                    <h3 style="margin: 0.5rem 0;">{streak_info['longest_streak']}</h3>
                    <p style="margin: 0; color: #666;">Longest Streak</p>
                </div>
                """, unsafe_allow_html=True)
                
                if streak_info['is_streak_broken']:
                    st.markdown(f"""
                    <div class="metric-container" style="border: 2px solid #f44336;">
                        <h2 style="color: #f44336; margin: 0;">💔</h2>
                        <h3 style="margin: 0.5rem 0;">{streak_info['days_inactive']}</h3>
                        <p style="margin: 0; color: #f44336;">Days Inactive</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Progress visualization
            if streak_info['current_streak'] > 0:
                progress = min(streak_info['current_streak'] / 30, 1.0)  # 30-day goal
                st.markdown("### 🎯 Progress to 30-Day Goal")
                st.progress(progress)
                st.write(f"{int(progress * 100)}% Complete")
        
        # Main content tabs with enhanced styling
        tab1, tab2, tab3 = st.tabs(["🎯 Log Activities", "📈 Weekly Insights", "🧪 Test Mode"])
        
        with tab1:
            self.activity_logger()
        
        with tab2:
            self.weekly_insights()
            
        with tab3:
            self.test_mode()

    def activity_logger(self):
        st.markdown("### What did you accomplish today?")
        
        # Input methods with better styling
        input_method = st.radio(
            "Choose your preferred input method:",
            ["💬 Text Input", "🎯 Quick Actions"],
            horizontal=True
        )
        
        if input_method == "💬 Text Input":
            st.markdown("#### 💭 Tell me about your day...")
            user_input = st.text_area(
                "",
                placeholder="e.g., 'crushed a 45-minute workout, studied Python for 2 hours, and only watched 1 episode of Netflix (progress!)'",
                height=120,
                help="Be specific! The more details, the better the roast... I mean, motivation! 😏"
            )
            
            if st.button("🚀 Roast My Day!", type="primary", use_container_width=True):
                if user_input.strip():
                    self.process_activities(user_input)
                else:
                    st.warning("🤨 Nothing to report? Even professional procrastination counts as an activity!")
        
        else:
            st.markdown("#### 🎯 Quick Activity Buttons")
            st.markdown("*Click any button to instantly log that activity*")
            
            quick_activities = [
                ("🏃‍♂️ Morning Walk", "walked 30 minutes around the neighborhood", "🌅"),
                ("📚 Study Session", "studied for 1 hour", "🧠"),
                ("📺 Netflix Time", "watched netflix for 2 hours", "🍿"),
                ("💪 Gym Beast Mode", "worked out at gym for 45 minutes", "🔥"),
                ("🧘‍♀️ Zen Moment", "meditated for 20 minutes", "☮️"),
                ("🍳 Master Chef", "cooked dinner for 30 minutes", "👨‍🍳"),
                ("📱 Social Scroll", "scrolled social media for 1 hour", "📱"),
                ("🎮 Gaming Session", "played video games for 3 hours", "🎮"),
                ("📖 Reading Time", "read a book for 45 minutes", "📚")
            ]
            
            cols = st.columns(3)
            for i, (button_text, activity_text, emoji) in enumerate(quick_activities):
                col = cols[i % 3]
                if col.button(f"{emoji} {button_text}", use_container_width=True):
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
        st.markdown("### 📈 Weekly Performance Dashboard")
        
        insights = st.session_state.insight.analyze_weekly_trends()
        weekly_summary = st.session_state.memory.get_weekly_summary()
        
        # Enhanced summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            ("📝", "Activities", weekly_summary.get('total_activities', 0), "#667eea"),
            ("🔥", "Calories", f"{weekly_summary.get('total_calories', 0)} kcal", "#ff6b6b"),
            ("📊", "Avg Score", f"{weekly_summary.get('avg_productivity', 0):.1f}/10", "#4caf50"),
            ("📈", "Trend", insights['trend'].title(), "#764ba2")
        ]
        
        for col, (icon, label, value, color) in zip([col1, col2, col3, col4], metrics):
            col.markdown(f"""
            <div class="metric-container">
                <h2 style="color: {color};">{icon}</h2>
                <h3>{value}</h3>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Weekly roast with enhanced styling
        st.markdown(f"""
        <div class="insight-card">
            <h3>🎭 Weekly Roast Summary</h3>
            <p style="font-size: 1.1em; font-style: italic;">{insights['roast_summary']}</p>
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
        st.markdown("### 🧪 Test Mode - Try Different Scenarios")
        st.markdown("*See how MotivAgent responds to various lifestyle choices!*")
        
        test_scenarios = [
            ("🏃‍♂️ Fitness Enthusiast", "ran 5 miles, did 100 push-ups, and meal prepped for the week"),
            ("📚 Study Grind", "studied calculus for 4 hours straight with only coffee breaks"),
            ("🎮 Gaming Marathon", "played Call of Duty for 8 hours and ordered pizza twice"),
            ("🧘‍♀️ Wellness Warrior", "meditated for 1 hour, did yoga, and journaled my feelings"),
            ("📺 Binge Watcher", "watched entire season of Stranger Things while eating ice cream"),
            ("💼 Workaholic", "worked 12 hours, skipped lunch, and answered emails until midnight"),
            ("🎨 Creative Day", "painted for 3 hours, played guitar, and wrote poetry"),
            ("🍕 Couch Potato", "scrolled TikTok all day and only left bed for snacks")
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
