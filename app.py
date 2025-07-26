
import streamlit as st
import sys
import os
from datetime import datetime
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
            layout="wide"
        )
        
        # Header
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #ff6b6b, #4ecdc4); border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>🤖 MOTIVAGENT 🤖</h1>
            <h3 style='color: white; margin: 0;'>Your Sarcastic Life Coach</h3>
            <p style='color: white; margin: 0;'>"Motivation with a side of roast"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar - Stats
        with st.sidebar:
            st.header("📊 Your Stats")
            streak_info = st.session_state.memory.get_streak_info()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔥 Current Streak", f"{streak_info['current_streak']} days")
                st.metric("📝 Total Sessions", streak_info['total_sessions'])
            with col2:
                st.metric("🏆 Longest Streak", f"{streak_info['longest_streak']} days")
                if streak_info['is_streak_broken']:
                    st.error(f"💔 Days inactive: {streak_info['days_inactive']}")
        
        # Main tabs
        tab1, tab2, tab3 = st.tabs(["🎯 Log Activities", "📈 Weekly Insights", "🧪 Test Mode"])
        
        with tab1:
            self.activity_logger()
        
        with tab2:
            self.weekly_insights()
            
        with tab3:
            self.test_mode()

    def activity_logger(self):
        st.header("What did you do today?")
        
        # Input methods
        input_method = st.radio("Choose input method:", ["💬 Text Input", "🎯 Quick Actions"])
        
        if input_method == "💬 Text Input":
            user_input = st.text_area(
                "Describe your activities:",
                placeholder="e.g., 'walked 30 min and watched 2 episodes of Netflix'",
                height=100
            )
            
            if st.button("🚀 Roast Me!", type="primary", use_container_width=True):
                if user_input.strip():
                    self.process_activities(user_input)
                else:
                    st.warning("🤨 Nothing to report? Even doing nothing is doing something... I guess.")
        
        else:
            st.subheader("Quick Activity Buttons")
            col1, col2, col3 = st.columns(3)
            
            quick_activities = [
                ("🏃‍♂️ Walked 30 min", "walked 30 minutes"),
                ("📚 Studied 1 hour", "studied for 1 hour"),
                ("📺 Watched Netflix", "watched netflix for 2 hours"),
                ("💪 Worked out", "worked out at gym for 45 minutes"),
                ("🧘‍♀️ Meditated", "meditated for 20 minutes"),
                ("🍳 Cooked meal", "cooked dinner for 30 minutes")
            ]
            
            for i, (button_text, activity_text) in enumerate(quick_activities):
                if i % 3 == 0:
                    col = col1
                elif i % 3 == 1:
                    col = col2
                else:
                    col = col3
                    
                if col.button(button_text, use_container_width=True):
                    self.process_activities(activity_text)

    def process_activities(self, user_input):
        with st.spinner("🧠 Analyzing your life choices..."):
            # Parse activities
            activities = st.session_state.planner.parse_input(user_input)
            
            # Process with executor
            processed = st.session_state.executor.process_activities(activities)
            
            # Store in memory
            st.session_state.memory.store_session(processed)
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            total_calories = sum(a['calories_burned'] for a in processed)
            avg_productivity = sum(a['productivity_score'] for a in processed) / len(processed)
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("🔥 Calories Burned", f"{total_calories} kcal")
            col2.metric("📊 Avg Productivity", f"{avg_productivity:.1f}/10")
            col3.metric("📝 Activities", len(processed))
            
            # Individual activity results
            for i, activity in enumerate(processed, 1):
                with st.expander(f"📌 Activity {i}: {activity['text']}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Category:** {activity['category'].title()}")
                        st.write(f"**Duration:** {activity['duration']} minutes")
                        
                        # Roast message with styling
                        if activity['productivity_score'] >= 7:
                            st.success(f"🎭 **RoastBot:** {activity['motivation_message']}")
                        elif activity['productivity_score'] >= 4:
                            st.info(f"🎭 **RoastBot:** {activity['motivation_message']}")
                        else:
                            st.warning(f"🎭 **RoastBot:** {activity['motivation_message']}")
                    
                    with col2:
                        st.metric("Calories", f"{activity['calories_burned']} kcal")
                        st.metric("Productivity", f"{activity['productivity_score']}/10")

    def weekly_insights(self):
        st.header("📈 Weekly Insights")
        
        insights = st.session_state.insight.analyze_weekly_trends()
        weekly_summary = st.session_state.memory.get_weekly_summary()
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📝 Activities", weekly_summary.get('total_activities', 0))
        col2.metric("🔥 Total Calories", f"{weekly_summary.get('total_calories', 0)} kcal")
        col3.metric("📊 Avg Productivity", f"{weekly_summary.get('avg_productivity', 0)}/10")
        
        trend_color = "🟢" if insights['trend'] == 'improving' else "🔴" if insights['trend'] == 'declining' else "🟡"
        col4.metric("📈 Trend", f"{trend_color} {insights['trend'].title()}")
        
        # Weekly roast
        st.subheader("🎭 Weekly Roast")
        st.info(insights['roast_summary'])
        
        # Insights
        st.subheader("💡 Insights")
        for insight in insights['insights']:
            st.write(f"• {insight}")
        
        # Category breakdown
        if insights['category_analysis']['breakdown']:
            st.subheader("📋 Activity Breakdown")
            
            breakdown_data = []
            for category, stats in insights['category_analysis']['breakdown'].items():
                breakdown_data.append({
                    'Category': category.title(),
                    'Count': stats['count'],
                    'Total Time (min)': stats['total_time']
                })
            
            st.dataframe(breakdown_data, use_container_width=True)
        
        # Suggestions
        suggestions = st.session_state.insight.suggest_improvements()
        st.subheader("🎯 Suggestions")
        for suggestion in suggestions:
            st.write(f"• {suggestion}")

    def test_mode(self):
        st.header("🧪 Test Mode")
        st.write("Try different inputs to see how MotivAgent responds!")
        
        test_inputs = [
            "walked 20 minutes and watched 3 episodes of One Piece",
            "studied calculus for 2 hours",
            "binged Netflix for 5 hours straight",
            "went to gym and worked out hard for 1 hour",
            "meditated for 30 minutes and journaled",
            "scrolled social media all day"
        ]
        
        for test_input in test_inputs:
            if st.button(f"Test: '{test_input}'", use_container_width=True):
                self.process_activities(test_input)

if __name__ == "__main__":
    app = MotivAgentWeb()
    app.run()
