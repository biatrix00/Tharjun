
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class Memory:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.logs_file = os.path.join(data_dir, "activity_logs.json")
        self.stats_file = os.path.join(data_dir, "user_stats.json")
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def store_session(self, activities: List[Dict[str, Any]]) -> None:
        """Store a session of activities"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Load existing logs
        logs = self._load_logs()
        
        # Add today's activities
        if today not in logs:
            logs[today] = []
            
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'activities': activities,
            'total_calories': sum(a.get('calories_burned', 0) for a in activities),
            'avg_productivity': sum(a.get('productivity_score', 0) for a in activities) / len(activities) if activities else 0
        }
        
        logs[today].append(session_data)
        
        # Save logs
        self._save_logs(logs)
        
        # Update stats
        self._update_stats(activities)
        
    def _load_logs(self) -> Dict[str, Any]:
        """Load activity logs from file"""
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_logs(self, logs: Dict[str, Any]) -> None:
        """Save activity logs to file"""
        with open(self.logs_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
            
    def _update_stats(self, activities: List[Dict[str, Any]]) -> None:
        """Update user statistics"""
        stats = self._load_stats()
        
        # Update totals
        stats['total_sessions'] = stats.get('total_sessions', 0) + 1
        stats['total_activities'] = stats.get('total_activities', 0) + len(activities)
        stats['total_calories'] = stats.get('total_calories', 0) + sum(a.get('calories_burned', 0) for a in activities)
        
        # Update category counts
        if 'category_counts' not in stats:
            stats['category_counts'] = {}
            
        for activity in activities:
            category = activity['category']
            stats['category_counts'][category] = stats['category_counts'].get(category, 0) + 1
        
        # Calculate streaks
        stats['current_streak'] = self._calculate_current_streak()
        stats['longest_streak'] = max(stats.get('longest_streak', 0), stats['current_streak'])
        
        # Update last activity date
        stats['last_activity_date'] = datetime.now().strftime("%Y-%m-%d")
        
        self._save_stats(stats)
        
    def _load_stats(self) -> Dict[str, Any]:
        """Load user statistics"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_stats(self, stats: Dict[str, Any]) -> None:
        """Save user statistics"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
            
    def _calculate_current_streak(self) -> int:
        """Calculate current activity streak in days"""
        logs = self._load_logs()
        
        if not logs:
            return 0
            
        # Get sorted dates
        dates = sorted(logs.keys(), reverse=True)
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if user was active today
        streak = 0
        current_date = datetime.now()
        
        for i in range(30):  # Check last 30 days
            date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            if date_str in logs and logs[date_str]:
                streak += 1
            else:
                break
                
        return streak
    
    def get_streak_info(self) -> Dict[str, Any]:
        """Get streak information"""
        stats = self._load_stats()
        logs = self._load_logs()
        
        current_streak = self._calculate_current_streak()
        longest_streak = stats.get('longest_streak', 0)
        
        # Days since last activity
        last_date = stats.get('last_activity_date')
        days_inactive = 0
        
        if last_date:
            last_activity = datetime.strptime(last_date, "%Y-%m-%d")
            days_inactive = (datetime.now() - last_activity).days
            
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'days_inactive': days_inactive,
            'total_sessions': stats.get('total_sessions', 0),
            'is_streak_broken': days_inactive > 1
        }
    
    def get_recent_activities(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get activities from the last N days"""
        logs = self._load_logs()
        recent_activities = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in logs:
                for session in logs[date]:
                    recent_activities.extend(session['activities'])
                    
        return recent_activities
    
    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get weekly activity summary"""
        recent_activities = self.get_recent_activities(7)
        
        if not recent_activities:
            return {'message': 'No activities recorded this week. Time to start moving!'}
        
        # Calculate weekly stats
        total_calories = sum(a.get('calories_burned', 0) for a in recent_activities)
        avg_productivity = sum(a.get('productivity_score', 0) for a in recent_activities) / len(recent_activities)
        
        # Category breakdown
        category_counts = {}
        for activity in recent_activities:
            cat = activity['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
        return {
            'total_activities': len(recent_activities),
            'total_calories': total_calories,
            'avg_productivity': round(avg_productivity, 1),
            'category_breakdown': category_counts,
            'most_common_activity': max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else 'none'
        }
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
        
        logs.append(session)
        
        # Save updated logs
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
        
        # Update counters
        stats['total_sessions'] += 1
        stats['total_activities'] += len(activities)
        stats['total_calories'] += sum(a.get('calories_burned', 0) for a in activities)
        
        # Update streak
        if last_active:
            last_date = datetime.fromisoformat(last_active).date()
            today_date = datetime.now().date()
            
            if last_date == today_date:
                # Same day, don't update streak
                pass
            elif last_date == today_date - timedelta(days=1):
                # Consecutive day
                stats['current_streak'] += 1
            else:
                # Streak broken
                stats['current_streak'] = 1
        else:
            # First session
            stats['current_streak'] = 1
        
        # Update longest streak
        if stats['current_streak'] > stats['longest_streak']:
            stats['longest_streak'] = stats['current_streak']
        
        stats['last_active_date'] = today
        
        # Save updated stats
        with open(self.user_stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def get_streak_info(self) -> Dict[str, Any]:
        """Get current streak information"""
        with open(self.user_stats_file, 'r') as f:
            stats = json.load(f)
        
        # Check if streak is broken
        is_streak_broken = False
        days_inactive = 0
        
        if stats.get('last_active_date'):
            last_date = datetime.fromisoformat(stats['last_active_date']).date()
            today = datetime.now().date()
            days_since_last = (today - last_date).days
            
            if days_since_last > 1:
                is_streak_broken = True
                days_inactive = days_since_last
                stats['current_streak'] = 0
        
        return {
            'current_streak': stats.get('current_streak', 0),
            'longest_streak': stats.get('longest_streak', 0),
            'total_sessions': stats.get('total_sessions', 0),
            'is_streak_broken': is_streak_broken,
            'days_inactive': days_inactive
        }
    
    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get weekly activity summary"""
        with open(self.activity_log_file, 'r') as f:
            logs = json.load(f)
        
        # Filter last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        recent_logs = [
            log for log in logs 
            if datetime.fromisoformat(log['date']) > week_ago
        ]
        
        if not recent_logs:
            return {
                'total_activities': 0,
                'total_calories': 0,
                'avg_productivity': 0,
                'sessions': 0
            }
        
        total_activities = sum(len(log['activities']) for log in recent_logs)
        total_calories = sum(log.get('total_calories', 0) for log in recent_logs)
        avg_productivity = sum(log.get('avg_productivity', 0) for log in recent_logs) / len(recent_logs)
        
        return {
            'total_activities': total_activities,
            'total_calories': total_calories,
            'avg_productivity': round(avg_productivity, 1),
            'sessions': len(recent_logs)
        }
    
    def get_activity_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get activity history for specified days"""
        with open(self.activity_log_file, 'r') as f:
            logs = json.load(f)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            log for log in logs 
            if datetime.fromisoformat(log['date']) > cutoff_date
        ]
