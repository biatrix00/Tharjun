import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .memory import Memory

class Insight:
    def __init__(self, memory: Memory):
        self.memory = memory

    def analyze_weekly_trends(self) -> Dict[str, Any]:
        """Analyze weekly trends and generate insights"""
        weekly_data = self.memory.get_weekly_data()

        if not weekly_data:
            return {
                'trend': 'no data',
                'trend_strength': 'none',
                'roast_summary': "No data to roast you with... yet. Start logging activities!",
                'insights': ["Start logging your activities to see trends!"],
                'category_analysis': {'breakdown': {}}
            }

        # Calculate trends
        productivity_scores = [session.get('avg_productivity', 0) for session in weekly_data]

        if len(productivity_scores) >= 2:
            if productivity_scores[-1] > productivity_scores[-2]:
                trend = 'improving'
                trend_strength = 'strong' if productivity_scores[-1] - productivity_scores[-2] > 2 else 'moderate'
            elif productivity_scores[-1] < productivity_scores[-2]:
                trend = 'declining'
                trend_strength = 'concerning' if productivity_scores[-2] - productivity_scores[-1] > 2 else 'slight'
            else:
                trend = 'stable'
                trend_strength = 'consistent'
        else:
            trend = 'unknown'
            trend_strength = 'insufficient data'

        # Generate roast summary
        avg_productivity = sum(productivity_scores) / len(productivity_scores) if productivity_scores else 0

        if avg_productivity >= 7:
            roast_summary = "You're actually doing well. Suspicious. Are you cheating?"
        elif avg_productivity >= 5:
            roast_summary = "Mediocre performance. At least you're consistent at being average."
        else:
            roast_summary = "Your productivity is as consistent as your motivation - barely there."

        # Category analysis
        category_breakdown = self._analyze_categories(weekly_data)

        # Generate insights
        insights = self._generate_insights(weekly_data, trend, avg_productivity)

        return {
            'trend': trend,
            'trend_strength': trend_strength,
            'roast_summary': roast_summary,
            'insights': insights,
            'category_analysis': {'breakdown': category_breakdown}
        }

    def _analyze_categories(self, weekly_data: List[Dict]) -> Dict[str, Dict]:
        """Analyze activity categories"""
        category_stats = {}

        for session in weekly_data:
            for activity in session.get('activities', []):
                category = activity.get('category', 'other')
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'total_time': 0}

                category_stats[category]['count'] += 1
                category_stats[category]['total_time'] += activity.get('duration', 0)

        return category_stats

    def _generate_insights(self, weekly_data: List[Dict], trend: str, avg_productivity: float) -> List[str]:
        """Generate actionable insights"""
        insights = []

        if trend == 'declining':
            insights.append("Your productivity is sliding faster than your motivation. Time to step up!")
        elif trend == 'improving':
            insights.append("You're actually improving! Don't let it go to your head.")

        if avg_productivity < 5:
            insights.append("Your productivity score suggests you excel at creative procrastination.")

        # Activity-specific insights
        all_activities = []
        for session in weekly_data:
            all_activities.extend(session.get('activities', []))

        if all_activities:
            categories = [a.get('category') for a in all_activities]
            most_common = max(set(categories), key=categories.count) if categories else None

            if most_common == 'entertainment':
                insights.append("You're a professional binge-watcher. Netflix should sponsor you.")
            elif most_common == 'exercise':
                insights.append("All that exercise and you're still not perfect. Shocking!")

        return insights if insights else ["You exist. That's... something."]

    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on recent activity"""
        recent_data = self.memory.get_recent_activities(days=7)
        suggestions = []

        if not recent_data:
            return ["Start by actually doing something worth logging!"]

        # Analyze recent patterns
        categories = [activity.get('category') for activity in recent_data]
        category_counts = {cat: categories.count(cat) for cat in set(categories)}

        # Suggest based on missing or low categories
        if category_counts.get('exercise', 0) < 3:
            suggestions.append("More exercise wouldn't kill you. Probably.")

        if category_counts.get('study', 0) < 2:
            suggestions.append("Learning something new might prevent brain rot.")

        if category_counts.get('entertainment', 0) > 5:
            suggestions.append("Maybe watch less TV and do something productive? Revolutionary idea!")

        return suggestions if suggestions else ["You're doing fine! Keep being awesome! 🌟"]