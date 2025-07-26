
#!/usr/bin/env python3
"""
MotivAgent - Sarcastic Motivational AI Agent
ODSC Agentic AI Hackathon Entry
"""

import os
import sys
from datetime import datetime
from src.planner import Planner
from src.executor import Executor
from src.memory import Memory
from src.insight import Insight

class MotivAgent:
    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.memory = Memory()
        self.insight = Insight(self.memory)
        
    def display_banner(self):
        """Display the MotivAgent banner"""
        banner = """
╔═══════════════════════════════════════════════════════╗
║                    🤖 MOTIVAGENT 🤖                   ║
║              Your Sarcastic Life Coach                ║
║            "Motivation with a side of roast"          ║
╚═══════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def display_streak_info(self):
        """Display current streak information"""
        streak_info = self.memory.get_streak_info()
        
        print(f"\n📊 YOUR STATS:")
        print(f"🔥 Current streak: {streak_info['current_streak']} days")
        print(f"🏆 Longest streak: {streak_info['longest_streak']} days")
        print(f"📝 Total sessions: {streak_info['total_sessions']}")
        
        if streak_info['is_streak_broken']:
            print(f"💔 Days inactive: {streak_info['days_inactive']} (streak broken!)")
        
    def process_daily_reflection(self, user_input: str):
        """Process user's daily reflection"""
        print(f"\n🔍 ANALYZING: '{user_input}'")
        print("=" * 50)
        
        # Step 1: Parse input
        print("📋 Planning activities...")
        activities = self.planner.parse_input(user_input)
        
        # Step 2: Execute with Gemini
        print("🧠 Generating roasts/motivation...")
        processed_activities = self.executor.process_activities(activities)
        
        # Step 3: Store in memory
        print("💾 Storing in memory...")
        self.memory.store_session(processed_activities)
        
        # Step 4: Display results
        self.display_results(processed_activities)
        
        return processed_activities
    
    def display_results(self, activities):
        """Display the motivation results"""
        print(f"\n🎭 ROASTBOT'S VERDICT:")
        print("=" * 50)
        
        total_calories = 0
        total_productivity = 0
        
        for i, activity in enumerate(activities, 1):
            print(f"\n📌 Activity {i}: {activity['text']}")
            print(f"   Category: {activity['category'].title()}")
            print(f"   Duration: {activity['duration']} minutes")
            print(f"   Calories: {activity['calories_burned']} kcal")
            print(f"   Productivity: {activity['productivity_score']}/10")
            print(f"   🗣️  RoastBot: {activity['motivation_message']}")
            
            total_calories += activity['calories_burned']
            total_productivity += activity['productivity_score']
        
        # Summary
        avg_productivity = total_productivity / len(activities) if activities else 0
        print(f"\n📊 SESSION SUMMARY:")
        print(f"   Total calories burned: {total_calories} kcal")
        print(f"   Average productivity: {avg_productivity:.1f}/10")
        
        # Productivity verdict
        if avg_productivity >= 7:
            print(f"   🏆 Verdict: PRODUCTIVITY CHAMPION!")
        elif avg_productivity >= 5:
            print(f"   👍 Verdict: Not terrible!")
        else:
            print(f"   😴 Verdict: Professional time-waster!")
    
    def show_weekly_insights(self):
        """Show weekly insights and trends"""
        print(f"\n📈 WEEKLY INSIGHTS")
        print("=" * 50)
        
        insights = self.insight.analyze_weekly_trends()
        
        print(f"📊 Trend: {insights['trend'].title()} ({insights.get('trend_strength', 'unknown')})")
        print(f"🎭 Weekly Roast: {insights['roast_summary']}")
        
        print(f"\n💡 INSIGHTS:")
        for insight in insights['insights']:
            print(f"   • {insight}")
        
        # Category breakdown
        if insights['category_analysis']['breakdown']:
            print(f"\n📋 ACTIVITY BREAKDOWN:")
            for category, stats in insights['category_analysis']['breakdown'].items():
                print(f"   • {category.title()}: {stats['count']} activities, {stats['total_time']} minutes")
        
        # Suggestions
        suggestions = self.insight.suggest_improvements()
        print(f"\n🎯 SUGGESTIONS:")
        for suggestion in suggestions:
            print(f"   • {suggestion}")
    
    def interactive_mode(self):
        """Run the interactive CLI"""
        self.display_banner()
        self.display_streak_info()
        
        while True:
            print(f"\n" + "=" * 50)
            print("What would you like to do?")
            print("1. Log today's activities")
            print("2. View weekly insights")
            print("3. Check streak status")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                user_input = input("\n💬 What did you do today? (e.g., 'walked 30 min and watched 2 episodes of Netflix'): ").strip()
                if user_input:
                    self.process_daily_reflection(user_input)
                else:
                    print("🤨 Nothing to report? Even doing nothing is doing something... I guess.")
                    
            elif choice == '2':
                self.show_weekly_insights()
                
            elif choice == '3':
                self.display_streak_info()
                weekly_summary = self.memory.get_weekly_summary()
                print(f"\n📈 WEEKLY SUMMARY:")
                print(f"   Activities: {weekly_summary.get('total_activities', 0)}")
                print(f"   Calories: {weekly_summary.get('total_calories', 0)} kcal")
                print(f"   Avg Productivity: {weekly_summary.get('avg_productivity', 0)}/10")
                
            elif choice == '4':
                print("\n👋 Thanks for using MotivAgent!")
                print("🎭 Remember: Tomorrow is another chance to disappoint RoastBot!")
                break
                
            else:
                print("🤔 Invalid choice. Even basic number selection is challenging for you, huh?")

def main():
    """Main entry point"""
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Warning: GEMINI_API_KEY not found in environment variables.")
        print("   MotivAgent will use fallback responses instead of Gemini API.")
        print("   Add your API key to .env file or environment variables for full functionality.\n")
    
    agent = MotivAgent()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Direct input mode
        user_input = " ".join(sys.argv[1:])
        agent.display_banner()
        agent.process_daily_reflection(user_input)
    else:
        # Interactive mode
        agent.interactive_mode()

if __name__ == "__main__":
    main()
