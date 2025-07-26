
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .memory import Memory

class Insight:
    def __init__(self, memory: Memory):
        self.memory = memory
        
    def analyze_weekly_trends(self) -> Dict[str, Any]:
        """Analyze weekly productivity and activity trends"""
        recent_activities = self.memory.get_recent_activities(7)
        
        if not recent_activities:
            return {
                'trend': 'inactive',
                'message': "Ghost mode activated! Your activity log is emptier than my motivational energy.",
                'suggestions': ["Try moving for 5 minutes", "Do literally anything", "Prove you exist"]
            }
        
        # Calculate daily productivity scores
        daily_scores = self._get_daily_productivity_scores()
        
        # Determine trend
        trend = self._calculate_trend(daily_scores)
        
        # Category analysis
        category_analysis = self._analyze_categories(recent_activities)
        
        # Generate insights
        insights = self._generate_insights(trend, category_analysis, daily_scores)
        
        return {
            'trend': trend['direction'],
            'trend_strength': trend['strength'],
            'daily_scores': daily_scores,
            'category_analysis': category_analysis,
            'insights': insights,
            'roast_summary': self._generate_weekly_roast(trend, category_analysis)
        }
    
    def _get_daily_productivity_scores(self) -> Dict[str, float]:
        """Get productivity scores for each day of the week"""
        daily_scores = {}
        
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            activities = self.memory.get_recent_activities(1)  # Get that specific day
            
            if activities:
                day_activities = [a for a in activities if a.get('timestamp', '').startswith(date)]
                if day_activities:
                    avg_score = sum(a.get('productivity_score', 0) for a in day_activities) / len(day_activities)
                    daily_scores[date] = round(avg_score, 1)
                else:
                    daily_scores[date] = 0
            else:
                daily_scores[date] = 0
                
        return daily_scores
    
    def _calculate_trend(self, daily_scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate productivity trend"""
        scores = list(daily_scores.values())
        
        if len(scores) < 2:
            return {'direction': 'stable', 'strength': 'weak'}
        
        # Simple trend calculation
        recent_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else scores[0]
        older_avg = sum(scores[-3:]) / 3 if len(scores) >= 3 else scores[-1]
        
        difference = recent_avg - older_avg
        
        if abs(difference) < 0.5:
            direction = 'stable'
        elif difference > 0:
            direction = 'improving'
        else:
            direction = 'declining'
            
        strength = 'strong' if abs(difference) > 1.5 else 'moderate' if abs(difference) > 0.5 else 'weak'
        
        return {
            'direction': direction,
            'strength': strength,
            'difference': round(difference, 1)
        }
    
    def _analyze_categories(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze activity categories"""
        category_stats = {}
        
        for activity in activities:
            category = activity['category']
            if category not in category_stats:
                category_stats[category] = {
                    'count': 0,
                    'total_time': 0,
                    'total_calories': 0,
                    'avg_productivity': 0
                }
            
            stats = category_stats[category]
            stats['count'] += 1
            stats['total_time'] += activity.get('duration', 0)
            stats['total_calories'] += activity.get('calories_burned', 0)
            stats['avg_productivity'] += activity.get('productivity_score', 0)
        
        # Calculate averages
        for category, stats in category_stats.items():
            if stats['count'] > 0:
                stats['avg_productivity'] = round(stats['avg_productivity'] / stats['count'], 1)
                stats['avg_duration'] = round(stats['total_time'] / stats['count'], 1)
        
        # Find dominant category
        if category_stats:
            dominant_category = max(category_stats.items(), key=lambda x: x[1]['count'])
            return {
                'breakdown': category_stats,
                'dominant_category': dominant_category[0],
                'dominant_percentage': round(dominant_category[1]['count'] / len(activities) * 100, 1)
            }
        
        return {'breakdown': {}, 'dominant_category': None, 'dominant_percentage': 0}
    
    def _generate_insights(self, trend: Dict[str, Any], category_analysis: Dict[str, Any], daily_scores: Dict[str, float]) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Trend insights
        if trend['direction'] == 'improving':
            insights.append("📈 You're on an upward trajectory! Whatever you're doing, keep it up.")
        elif trend['direction'] == 'declining':
            insights.append("📉 Productivity is sliding faster than your motivation. Time to course correct!")
        else:
            insights.append("📊 You're consistent... consistently mediocre. But hey, consistency counts for something!")
        
        # Category insights
        dominant = category_analysis.get('dominant_category')
        if dominant == 'entertainment':
            insights.append("🍿 Entertainment is your specialty! Maybe balance it with some actual productivity?")
        elif dominant == 'exercise':
            insights.append("💪 Look at you being all healthy and stuff! Your future self thanks you.")
        elif dominant == 'study':
            insights.append("🧠 Big brain energy detected! Keep feeding those neurons.")
        
        # Activity frequency insights
        total_activities = sum(1 for score in daily_scores.values() if score > 0)
        if total_activities < 3:
            insights.append("⚠️ You're more inactive than a Windows 95 computer. Time to wake up!")
        elif total_activities >= 6:
            insights.append("🔥 Daily activity streak! You're like a productivity machine (that occasionally breaks down).")
        
        return insights
    
    def _generate_weekly_roast(self, trend: Dict[str, Any], category_analysis: Dict[str, Any]) -> str:
        """Generate a weekly roast summary"""
        direction = trend['direction']
        dominant = category_analysis.get('dominant_category', 'nothing')
        percentage = category_analysis.get('dominant_percentage', 0)
        
        if direction == 'improving':
            return f"Well, well, well... look who's actually trying! You spent {percentage}% of your time on {dominant}. Progress is progress, I guess. 🎉"
        elif direction == 'declining':
            return f"Yikes! Your productivity is declining faster than my faith in humanity. {percentage}% {dominant}? Really? Time for an intervention! 😬"
        else:
            if dominant == 'entertainment':
                return f"Stable mediocrity achieved! {percentage}% entertainment. You've mastered the art of doing just enough to survive. Bravo! 👏"
            else:
                return f"Consistently inconsistent! {percentage}% {dominant}. You're like a metronome... if metronomes were powered by chaos. 🎭"
    
    def get_motivation_history(self) -> List[str]:
        """Get recent motivational messages for pattern analysis"""
        recent_activities = self.memory.get_recent_activities(7)
        return [activity.get('motivation_message', '') for activity in recent_activities if activity.get('motivation_message')]
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on analysis"""
        weekly_summary = self.memory.get_weekly_summary()
        streak_info = self.memory.get_streak_info()
        
        suggestions = []
        
        # Based on productivity
        if weekly_summary.get('avg_productivity', 0) < 5:
            suggestions.append("Try adding one productive activity daily - even 15 minutes counts!")
        
        # Based on streak
        if streak_info['current_streak'] == 0:
            suggestions.append("Start a new streak! Log one activity today.")
        elif streak_info['current_streak'] < 3:
            suggestions.append("You're building momentum! Keep the streak alive.")
        
        # Based on dominant activity
        most_common = weekly_summary.get('most_common_activity')
        if most_common == 'entertainment':
            suggestions.append("Balance entertainment with some exercise or learning.")
        elif most_common == 'exercise':
            suggestions.append("Great exercise habit! Maybe add some learning activities?")
        
        return suggestions if suggestions else ["You're doing fine! Keep being awesome! 🌟"]
