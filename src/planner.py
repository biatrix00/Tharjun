
import re
from typing import List, Dict, Any
from datetime import datetime

class Planner:
    def __init__(self):
        self.activity_patterns = {
            'exercise': ['walk', 'run', 'jog', 'gym', 'workout', 'exercise', 'bike', 'swim', 'yoga', 'pilates'],
            'study': ['study', 'read', 'learn', 'research', 'homework', 'practice', 'code', 'programming'],
            'work': ['work', 'meeting', 'project', 'office', 'job', 'task', 'email'],
            'entertainment': ['netflix', 'tv', 'movie', 'game', 'social media', 'youtube', 'tiktok', 'instagram'],
            'habits': ['meditate', 'journal', 'clean', 'cook', 'meal prep', 'water', 'sleep'],
            'social': ['friend', 'family', 'date', 'party', 'hangout', 'call', 'chat']
        }
        
    def parse_input(self, user_input: str) -> List[Dict[str, Any]]:
        """Parse user input into structured activity entries"""
        activities = []
        text = user_input.lower()
        
        # Extract time durations
        time_pattern = r'(\d+)\s*(min|minutes|hour|hours|hr|h)'
        time_matches = re.findall(time_pattern, text)
        
        # Split input by common separators
        sentences = re.split(r'[,;.]\s*|and\s+', user_input)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            activity = self._classify_activity(sentence.lower())
            duration = self._extract_duration(sentence)
            intensity = self._estimate_intensity(sentence.lower(), activity['category'])
            
            activity_entry = {
                'text': sentence,
                'category': activity['category'],
                'keywords': activity['keywords'],
                'duration': duration,
                'intensity': intensity,
                'mood': self._assess_mood(sentence.lower()),
                'subtasks': self._identify_subtasks(sentence),
                'timestamp': datetime.now().isoformat()
            }
            
            activities.append(activity_entry)
            
        return activities if activities else [self._create_default_activity(user_input)]
    
    def _classify_activity(self, text: str) -> Dict[str, Any]:
        """Classify activity based on keywords"""
        for category, keywords in self.activity_patterns.items():
            found_keywords = [kw for kw in keywords if kw in text]
            if found_keywords:
                return {'category': category, 'keywords': found_keywords}
        
        return {'category': 'other', 'keywords': []}
    
    def _extract_duration(self, text: str) -> int:
        """Extract duration in minutes from text"""
        time_pattern = r'(\d+)\s*(min|minutes|hour|hours|hr|h)'
        matches = re.findall(time_pattern, text.lower())
        
        total_minutes = 0
        for amount, unit in matches:
            amount = int(amount)
            if unit in ['hour', 'hours', 'hr', 'h']:
                total_minutes += amount * 60
            else:
                total_minutes += amount
                
        return total_minutes if total_minutes > 0 else 30  # Default 30 minutes
    
    def _estimate_intensity(self, text: str, category: str) -> str:
        """Estimate intensity based on keywords and category"""
        high_intensity = ['intense', 'hard', 'difficult', 'challenging', 'heavy']
        low_intensity = ['easy', 'light', 'gentle', 'relaxed', 'casual']
        
        if any(word in text for word in high_intensity):
            return 'high'
        elif any(word in text for word in low_intensity):
            return 'low'
        elif category == 'exercise':
            return 'medium'
        elif category in ['entertainment', 'social']:
            return 'low'
        else:
            return 'medium'
    
    def _assess_mood(self, text: str) -> str:
        """Assess mood from text"""
        positive_words = ['good', 'great', 'awesome', 'amazing', 'fun', 'enjoyed', 'love']
        negative_words = ['bad', 'terrible', 'boring', 'hate', 'awful', 'struggled']
        
        if any(word in text for word in positive_words):
            return 'positive'
        elif any(word in text for word in negative_words):
            return 'negative'
        else:
            return 'neutral'
    
    def _identify_subtasks(self, text: str) -> List[str]:
        """Identify potential subtasks"""
        # Simple subtask identification
        if 'and' in text:
            return [part.strip() for part in text.split('and')]
        return [text.strip()]
    
    def _create_default_activity(self, text: str) -> Dict[str, Any]:
        """Create default activity for unclassified input"""
        return {
            'text': text,
            'category': 'other',
            'keywords': [],
            'duration': 30,
            'intensity': 'low',
            'mood': 'neutral',
            'subtasks': [text],
            'timestamp': datetime.now().isoformat()
        }
