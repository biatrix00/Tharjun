
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
import re
from typing import List, Dict, Any

class Planner:
    def __init__(self):
        # Activity keywords for classification
        self.activity_keywords = {
            'exercise': ['workout', 'gym', 'run', 'jog', 'bike', 'swim', 'yoga', 'pilates', 'cardio', 'weights', 'lift'],
            'walk': ['walk', 'walking', 'stroll', 'hike', 'hiking'],
            'study': ['study', 'read', 'learn', 'practice', 'homework', 'course', 'tutorial', 'book'],
            'work': ['work', 'project', 'meeting', 'code', 'coding', 'program', 'develop'],
            'entertainment': ['watch', 'movie', 'tv', 'netflix', 'show', 'episode', 'game', 'gaming', 'video'],
            'habits': ['meditate', 'journal', 'clean', 'organize', 'cook', 'meal prep'],
            'social': ['friend', 'family', 'date', 'party', 'hangout', 'call', 'text'],
        }
        
        # Time extraction patterns
        self.time_patterns = [
            (r'(\d+)\s*hours?', lambda x: int(x) * 60),
            (r'(\d+)\s*hrs?', lambda x: int(x) * 60),
            (r'(\d+)\s*h', lambda x: int(x) * 60),
            (r'(\d+)\s*minutes?', lambda x: int(x)),
            (r'(\d+)\s*mins?', lambda x: int(x)),
            (r'(\d+)\s*m(?!\w)', lambda x: int(x)),
            (r'(\d+)\s*episodes?', lambda x: int(x) * 25),  # Assume 25 min per episode
            (r'(\d+)\s*shows?', lambda x: int(x) * 45),     # Assume 45 min per show
        ]
    
    def parse_input(self, user_input: str) -> List[Dict[str, Any]]:
        """Parse user input and extract activities"""
        if not user_input.strip():
            return []
        
        # Split by common delimiters
        activity_chunks = self._split_activities(user_input.lower())
        
        activities = []
        for chunk in activity_chunks:
            activity = self._parse_single_activity(chunk)
            if activity:
                activities.append(activity)
        
        return activities
    
    def _split_activities(self, text: str) -> List[str]:
        """Split text into individual activity chunks"""
        # Split on common delimiters
        delimiters = [' and ', ', ', '; ', ' then ', ' also ']
        
        chunks = [text]
        for delimiter in delimiters:
            new_chunks = []
            for chunk in chunks:
                new_chunks.extend(chunk.split(delimiter))
            chunks = new_chunks
        
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def _parse_single_activity(self, text: str) -> Dict[str, Any]:
        """Parse a single activity chunk"""
        # Extract duration
        duration = self._extract_duration(text)
        
        # Classify activity
        category = self._classify_activity(text)
        
        # Determine intensity
        intensity = self._determine_intensity(text, category)
        
        return {
            'text': text,
            'category': category,
            'duration': duration,
            'intensity': intensity,
            'raw_input': text
        }
    
    def _extract_duration(self, text: str) -> int:
        """Extract duration in minutes from text"""
        for pattern, converter in self.time_patterns:
            match = re.search(pattern, text)
            if match:
                return converter(match.group(1))
        
        # Default durations based on activity type
        if any(word in text for word in ['episode', 'show', 'movie']):
            return 25  # Default episode length
        elif any(word in text for word in ['workout', 'gym', 'exercise']):
            return 45  # Default workout
        elif any(word in text for word in ['walk', 'run', 'jog']):
            return 30  # Default walk/run
        else:
            return 30  # Default activity length
    
    def _classify_activity(self, text: str) -> str:
        """Classify activity into categories"""
        for category, keywords in self.activity_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'other'
    
    def _determine_intensity(self, text: str, category: str) -> str:
        """Determine activity intensity"""
        high_intensity_words = ['intense', 'hard', 'difficult', 'sprint', 'hiit']
        low_intensity_words = ['easy', 'light', 'gentle', 'slow', 'casual']
        
        if any(word in text for word in high_intensity_words):
            return 'high'
        elif any(word in text for word in low_intensity_words):
            return 'low'
        elif category in ['exercise', 'work']:
            return 'medium'
        else:
            return 'low'
