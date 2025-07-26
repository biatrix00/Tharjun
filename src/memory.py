import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class Memory:
    def __init__(self):
        self.data_dir = "data"
        self.activity_log_file = os.path.join(self.data_dir, "activity_log.json")
        self.user_stats_file = os.path.join(self.data_dir, "user_stats.json")

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize files if they don't exist
        self._init_files()

    def _init_files(self):
        """Initialize data files if they don't exist"""
        if not os.path.exists(self.activity_log_file):
            with open(self.activity_log_file, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.user_stats_file):
            default_stats = {
                'total_sessions': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'last_active_date': None,
                'total_activities': 0,
                'total_calories': 0
            }
            with open(self.user_stats_file, 'w') as f:
                json.dump(default_stats, f)

    def store_session(self, activities: List[Dict[str, Any]]):
        """Store a session of activities"""
        if not activities:
            return

        # Load existing logs
        with open(self.activity_log_file, 'r') as f:
            logs = json.load(f)

        # Create session entry
        session = {
            'date': datetime.now().isoformat(),
            'activities': activities,
            'total_calories': sum(a.get('calories_burned', 0) for a in activities),
            'avg_productivity': sum(a.get('productivity_score', 0) for a in activities) / len(activities)
        }

        # Add to logs
        logs.append(session)

        # Save logs
        with open(self.activity_log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        # Update user stats
        self._update_user_stats(activities)

    def _update_user_stats(self, activities: List[Dict[str, Any]]):
        """Update user statistics"""
        with open(self.user_stats_file, 'r') as f:
            stats = json.load(f)

        today = datetime.now().date().isoformat()
        last_active = stats.get('last_active_date')

        # Update basic stats
        stats['total_sessions'] += 1
        stats['total_activities'] += len(activities)
        stats['total_calories'] += sum(a.get('calories_burned', 0) for a in activities)

        # Update streak
        if last_active:
            last_date = datetime.fromisoformat(last_active).date()
            today_date = datetime.now().date()
            days_diff = (today_date - last_date).days

            if days_diff == 1:
                # Consecutive day
                stats['current_streak'] += 1
            elif days_diff > 1:
                # Streak broken
                stats['current_streak'] = 1
            # Same day, don't change streak
        else:
            # First session
            stats['current_streak'] = 1

        # Update longest streak
        if stats['current_streak'] > stats['longest_streak']:
            stats['longest_streak'] = stats['current_streak']

        stats['last_active_date'] = today

        # Save stats
        with open(self.user_stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

    def get_streak_info(self) -> Dict[str, Any]:
        """Get current streak information"""
        with open(self.user_stats_file, 'r') as f:
            stats = json.load(f)

        today = datetime.now().date()
        last_active = stats.get('last_active_date')

        if last_active:
            last_date = datetime.fromisoformat(last_active).date()
            days_inactive = (today - last_date).days
            is_streak_broken = days_inactive > 1

            if is_streak_broken:
                stats['current_streak'] = 0
        else:
            days_inactive = 0
            is_streak_broken = False

        return {
            'current_streak': stats['current_streak'],
            'longest_streak': stats['longest_streak'],
            'total_sessions': stats['total_sessions'],
            'days_inactive': days_inactive,
            'is_streak_broken': is_streak_broken
        }

    def get_weekly_data(self) -> List[Dict[str, Any]]:
        """Get data from the last 7 days"""
        with open(self.activity_log_file, 'r') as f:
            logs = json.load(f)

        week_ago = datetime.now() - timedelta(days=7)
        weekly_logs = []

        for log in logs:
            log_date = datetime.fromisoformat(log['date'])
            if log_date >= week_ago:
                weekly_logs.append(log)

        return weekly_logs

    def get_recent_activities(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent activities"""
        weekly_data = self.get_weekly_data()
        activities = []

        for session in weekly_data:
            activities.extend(session.get('activities', []))

        return activities

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get weekly summary statistics"""
        weekly_data = self.get_weekly_data()

        if not weekly_data:
            return {
                'total_activities': 0,
                'total_calories': 0,
                'avg_productivity': 0
            }

        total_activities = sum(len(session.get('activities', [])) for session in weekly_data)
        total_calories = sum(session.get('total_calories', 0) for session in weekly_data)

        productivities = [session.get('avg_productivity', 0) for session in weekly_data]
        avg_productivity = sum(productivities) / len(productivities) if productivities else 0

        return {
            'total_activities': total_activities,
            'total_calories': total_calories,
            'avg_productivity': round(avg_productivity, 1)
        }