import re
from typing import List, Dict, Any

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
                'duration': duration,
                'intensity': intensity,
                'confidence': activity['confidence']
            }

            activities.append(activity_entry)

        return activities if activities else [self._create_default_activity(user_input)]

    def _classify_activity(self, text: str) -> Dict[str, Any]:
        """Classify activity based on keywords"""
        text_lower = text.lower()
        best_category = 'other'
        best_confidence = 0.0

        for category, keywords in self.activity_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    confidence = len(keyword) / len(text_lower)  # Simple confidence score
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_category = category

        return {
            'category': best_category,
            'confidence': best_confidence
        }

    def _extract_duration(self, text: str) -> int:
        """Extract duration from text"""
        # Look for patterns like "30 min", "2 hours", etc.
        time_pattern = r'(\d+)\s*(min|minutes|hour|hours|hr|h)'
        matches = re.findall(time_pattern, text.lower())

        if matches:
            number, unit = matches[0]
            duration = int(number)

            # Convert to minutes
            if unit in ['hour', 'hours', 'hr', 'h']:
                duration *= 60

            return duration

        # Default duration if not specified
        return 30

    def _estimate_intensity(self, text: str, category: str) -> str:
        """Estimate intensity based on keywords and category"""
        high_intensity_words = ['intense', 'hard', 'difficult', 'challenging', 'fast', 'heavy']
        low_intensity_words = ['easy', 'light', 'gentle', 'slow', 'relaxed', 'casual']

        text_lower = text.lower()

        if any(word in text_lower for word in high_intensity_words):
            return 'high'
        elif any(word in text_lower for word in low_intensity_words):
            return 'low'
        else:
            # Default based on category
            if category == 'exercise':
                return 'medium'
            elif category == 'entertainment':
                return 'low'
            else:
                return 'medium'

    def _create_default_activity(self, original_input: str) -> Dict[str, Any]:
        """Create a default activity when parsing fails"""
        return {
            'text': original_input,
            'category': 'other',
            'duration': 30,
            'intensity': 'medium',
            'confidence': 0.0
        }