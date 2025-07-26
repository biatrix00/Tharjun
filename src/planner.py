import re
from typing import List, Dict, Any
from datetime import datetime, timedelta

class Planner:
    def __init__(self):
        self.activity_patterns = {
            'exercise': ['walk', 'run', 'jog', 'gym', 'workout', 'exercise', 'bike', 'swim', 'yoga', 'pilates', 'cardio', 'weights', 'fitness', 'crossfit', 'dance', 'martial arts', 'boxing', 'climbing', 'hiking', 'sports'],
            'study': ['study', 'read', 'learn', 'research', 'homework', 'practice', 'code', 'programming', 'course', 'tutorial', 'lecture', 'exam', 'review', 'notes', 'assignment', 'project', 'algorithm', 'math', 'physics', 'chemistry'],
            'work': ['work', 'meeting', 'project', 'office', 'job', 'task', 'email', 'presentation', 'deadline', 'client', 'conference', 'report', 'analysis', 'design', 'development', 'testing', 'documentation'],
            'entertainment': ['netflix', 'tv', 'movie', 'game', 'social media', 'youtube', 'tiktok', 'instagram', 'facebook', 'twitter', 'podcast', 'music', 'show', 'series', 'anime', 'documentary', 'stream', 'video', 'meme'],
            'habits': ['meditate', 'journal', 'clean', 'cook', 'meal prep', 'water', 'sleep', 'brush teeth', 'shower', 'skincare', 'vitamins', 'organize', 'laundry', 'groceries', 'budget', 'plan'],
            'social': ['friend', 'family', 'date', 'party', 'hangout', 'call', 'chat', 'dinner', 'lunch', 'coffee', 'visit', 'event', 'celebration', 'gathering', 'meet', 'text', 'message'],
            'creative': ['draw', 'paint', 'write', 'compose', 'photography', 'design', 'craft', 'pottery', 'music', 'sing', 'instrument', 'art', 'creative', 'sketch', 'blog'],
            'wellness': ['therapy', 'doctor', 'dentist', 'massage', 'spa', 'relaxation', 'mental health', 'mindfulness', 'breathing', 'stretch', 'self-care', 'reflection'],
            'travel': ['flight', 'drive', 'bus', 'train', 'commute', 'trip', 'vacation', 'explore', 'sightseeing', 'travel', 'adventure', 'journey']
        }
        
        # Enhanced time patterns
        self.time_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)\s*(?:and\s*)?(\d+)?\s*(?:minutes?|mins?|m)?',
            r'(\d+(?:\.\d+)?)\s*(?:minutes?|mins?|m)',
            r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)',
            r'for\s+(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)',
            r'for\s+(\d+)\s*(?:minutes?|mins?|m)',
            r'(\d+)\s*to\s*(\d+)\s*(?:hours?|hrs?|h)',
            r'about\s+(\d+)\s*(?:hours?|hrs?|h|minutes?|mins?|m)',
            r'around\s+(\d+)\s*(?:hours?|hrs?|h|minutes?|mins?|m)',
            r'(\d+)-(\d+)\s*(?:hours?|hrs?|h|minutes?|mins?|m)',
            r'all\s+day',
            r'whole\s+day',
            r'entire\s+day'
        ]
        
        # Mood indicators
        self.mood_indicators = {
            'positive': ['enjoyed', 'loved', 'fun', 'great', 'awesome', 'amazing', 'fantastic', 'wonderful', 'excellent', 'productive', 'motivated', 'energetic', 'happy'],
            'negative': ['boring', 'tired', 'exhausted', 'stressed', 'frustrated', 'difficult', 'hard', 'challenging', 'annoying', 'hate', 'dislike', 'unmotivated'],
            'neutral': ['okay', 'fine', 'normal', 'usual', 'regular', 'standard', 'typical']
        }
        
        # Intensity keywords
        self.intensity_keywords = {
            'high': ['intense', 'hard', 'difficult', 'challenging', 'fast', 'heavy', 'vigorous', 'extreme', 'maximum', 'all-out', 'brutal', 'hardcore'],
            'medium': ['moderate', 'normal', 'regular', 'steady', 'medium', 'average', 'standard'],
            'low': ['easy', 'light', 'gentle', 'slow', 'relaxed', 'casual', 'minimal', 'basic', 'simple', 'lazy']
        }
        
        # Context clues for better understanding
        self.context_clues = {
            'location': ['gym', 'home', 'office', 'park', 'library', 'cafe', 'outdoors', 'indoors', 'bedroom', 'kitchen'],
            'tools': ['laptop', 'computer', 'phone', 'book', 'treadmill', 'weights', 'bike', 'car', 'bus'],
            'with_others': ['with friends', 'with family', 'with colleagues', 'alone', 'solo', 'group', 'team', 'partner']
        }

    def parse_input(self, user_input: str) -> List[Dict[str, Any]]:
        """Parse user input into structured activity entries with enhanced NLP"""
        activities = []
        
        # Preprocess input
        processed_input = self._preprocess_input(user_input)
        
        # Split input by common separators with improved logic
        sentences = self._smart_split(processed_input)
        
        # Extract global context (affects all activities)
        global_context = self._extract_global_context(user_input)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 3:
                continue

            # Enhanced activity classification
            activity = self._classify_activity_advanced(sentence.lower())
            duration = self._extract_duration_advanced(sentence)
            intensity = self._estimate_intensity_advanced(sentence.lower(), activity['category'])
            mood = self._detect_mood(sentence.lower())
            context = self._extract_local_context(sentence.lower())
            
            # Merge global and local context
            merged_context = {**global_context, **context}

            activity_entry = {
                'text': sentence,
                'category': activity['category'],
                'subcategory': activity.get('subcategory', 'general'),
                'duration': duration,
                'intensity': intensity,
                'mood': mood,
                'context': merged_context,
                'confidence': activity['confidence'],
                'parsed_elements': {
                    'has_duration': duration > 0,
                    'has_mood_indicator': mood != 'neutral',
                    'has_intensity_modifier': intensity != 'medium',
                    'has_location': 'location' in merged_context,
                    'social_activity': 'with_others' in merged_context
                }
            }

            activities.append(activity_entry)

        # Post-process activities for consistency
        activities = self._post_process_activities(activities)
        
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

    def _preprocess_input(self, text: str) -> str:
        """Preprocess input text for better parsing"""
        # Normalize common abbreviations and variations
        text = re.sub(r'\b(\d+)\s*hrs?\b', r'\1 hours', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(\d+)\s*mins?\b', r'\1 minutes', text, flags=re.IGNORECASE)
        text = re.sub(r'\bNetflix\b', 'netflix', text, flags=re.IGNORECASE)
        text = re.sub(r'\bYouTube\b', 'youtube', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTV\b', 'tv', text, flags=re.IGNORECASE)
        
        # Handle common contractions
        text = re.sub(r"didn't", "did not", text)
        text = re.sub(r"wasn't", "was not", text)
        text = re.sub(r"couldn't", "could not", text)
        
        return text
    
    def _smart_split(self, text: str) -> List[str]:
        """Smart splitting that preserves context"""
        # Enhanced splitting patterns
        split_patterns = [
            r'[,;]\s*(?:and\s+)?(?:then\s+)?',
            r'\.\s+(?:Then\s+|After\s+)?',
            r'\s+and\s+(?:then\s+)?(?:I\s+)?',
            r'\s+then\s+(?:I\s+)?',
            r'\s+after\s+(?:that\s+)?(?:I\s+)?',
            r'\s+before\s+(?:that\s+)?(?:I\s+)?',
            r'\s+while\s+(?:I\s+)?',
            r'\s+during\s+(?:the\s+)?',
        ]
        
        sentences = [text]
        for pattern in split_patterns:
            new_sentences = []
            for sentence in sentences:
                new_sentences.extend(re.split(pattern, sentence))
            sentences = new_sentences
        
        return [s.strip() for s in sentences if s.strip()]
    
    def _classify_activity_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced activity classification with subcategories"""
        best_category = 'other'
        best_subcategory = 'general'
        best_confidence = 0.0
        
        # Enhanced scoring system
        for category, keywords in self.activity_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    # Calculate confidence based on keyword length and context
                    base_confidence = len(keyword) / len(text)
                    
                    # Boost confidence for exact matches
                    if f' {keyword} ' in f' {text} ' or text.startswith(keyword) or text.endswith(keyword):
                        base_confidence *= 1.5
                    
                    # Context-based confidence boost
                    if self._has_supporting_context(text, category):
                        base_confidence *= 1.3
                    
                    if base_confidence > best_confidence:
                        best_confidence = base_confidence
                        best_category = category
                        best_subcategory = self._identify_subcategory(text, category)
        
        return {
            'category': best_category,
            'subcategory': best_subcategory,
            'confidence': min(best_confidence, 1.0)
        }
    
    def _has_supporting_context(self, text: str, category: str) -> bool:
        """Check if text has supporting context for the category"""
        support_words = {
            'exercise': ['calories', 'sweat', 'tired', 'energy', 'fitness', 'health'],
            'study': ['learned', 'knowledge', 'brain', 'focus', 'concentration', 'notes'],
            'work': ['productive', 'deadline', 'boss', 'colleagues', 'project', 'task'],
            'entertainment': ['fun', 'relax', 'enjoy', 'binge', 'episode', 'season'],
        }
        
        return any(word in text for word in support_words.get(category, []))
    
    def _identify_subcategory(self, text: str, category: str) -> str:
        """Identify subcategory within main category"""
        subcategories = {
            'exercise': {
                'cardio': ['run', 'jog', 'bike', 'swim', 'cardio', 'treadmill'],
                'strength': ['weights', 'lifting', 'gym', 'strength', 'muscle'],
                'flexibility': ['yoga', 'stretch', 'pilates', 'flexibility'],
                'sports': ['basketball', 'soccer', 'tennis', 'sport', 'game'],
                'walking': ['walk', 'walking', 'stroll', 'hike']
            },
            'study': {
                'programming': ['code', 'coding', 'programming', 'algorithm', 'debug'],
                'reading': ['read', 'book', 'article', 'paper', 'literature'],
                'math': ['math', 'calculus', 'algebra', 'statistics', 'equation'],
                'language': ['language', 'vocabulary', 'grammar', 'speaking']
            },
            'entertainment': {
                'streaming': ['netflix', 'youtube', 'stream', 'video'],
                'gaming': ['game', 'gaming', 'play', 'xbox', 'playstation'],
                'social_media': ['instagram', 'facebook', 'twitter', 'tiktok', 'social media'],
                'music': ['music', 'song', 'listen', 'podcast', 'audio']
            }
        }
        
        if category in subcategories:
            for subcat, keywords in subcategories[category].items():
                if any(keyword in text for keyword in keywords):
                    return subcat
        
        return 'general'
    
    def _extract_duration_advanced(self, text: str) -> int:
        """Advanced duration extraction with multiple patterns"""
        text_lower = text.lower()
        
        # Check for special cases first
        if any(phrase in text_lower for phrase in ['all day', 'whole day', 'entire day']):
            return 480  # 8 hours
        
        if any(phrase in text_lower for phrase in ['quick', 'briefly', 'short']):
            return 15
        
        if any(phrase in text_lower for phrase in ['long time', 'ages', 'forever']):
            return 120
        
        # Try each pattern
        for pattern in self.time_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                if isinstance(matches[0], tuple):
                    # Handle patterns with multiple groups
                    match = matches[0]
                    if len(match) == 2 and match[1]:  # Hours and minutes
                        hours = float(match[0]) if match[0] else 0
                        minutes = int(match[1]) if match[1] else 0
                        return int(hours * 60 + minutes)
                    elif len(match) == 2:  # Range (e.g., "2-3 hours")
                        start = float(match[0])
                        end = float(match[1])
                        avg = (start + end) / 2
                        return int(avg * 60) if 'hour' in pattern else int(avg)
                else:
                    # Single number
                    duration = float(matches[0])
                    if 'hour' in pattern:
                        return int(duration * 60)
                    else:
                        return int(duration)
        
        # Estimate based on activity type if no duration found
        return self._estimate_default_duration(text_lower)
    
    def _estimate_default_duration(self, text: str) -> int:
        """Estimate duration based on activity type and context"""
        if any(word in text for word in ['episode', 'show', 'movie']):
            episode_count = self._extract_episode_count(text)
            return episode_count * 25  # Average episode length
        
        if any(word in text for word in ['walk', 'walking']):
            return 30
        
        if any(word in text for word in ['workout', 'exercise', 'gym']):
            return 60
        
        if any(word in text for word in ['study', 'read', 'homework']):
            return 90
        
        if any(word in text for word in ['work', 'meeting', 'project']):
            return 120
        
        return 30  # Default
    
    def _extract_episode_count(self, text: str) -> int:
        """Extract number of episodes/shows watched"""
        patterns = [
            r'(\d+)\s*episodes?',
            r'(\d+)\s*eps?',
            r'(\d+)\s*shows?',
            r'(\d+)\s*movies?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return int(matches[0])
        
        # Check for written numbers
        written_numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        for word, number in written_numbers.items():
            if word in text:
                return number
        
        return 1  # Default to 1 episode
    
    def _extract_global_context(self, text: str) -> Dict[str, Any]:
        """Extract context that applies to all activities"""
        context = {}
        text_lower = text.lower()
        
        # Time context
        if any(phrase in text_lower for phrase in ['this morning', 'morning']):
            context['time_of_day'] = 'morning'
        elif any(phrase in text_lower for phrase in ['afternoon', 'this afternoon']):
            context['time_of_day'] = 'afternoon'
        elif any(phrase in text_lower for phrase in ['evening', 'tonight', 'this evening']):
            context['time_of_day'] = 'evening'
        
        # Weather context
        if any(phrase in text_lower for phrase in ['sunny', 'nice weather', 'beautiful day']):
            context['weather'] = 'good'
        elif any(phrase in text_lower for phrase in ['rainy', 'raining', 'cold', 'bad weather']):
            context['weather'] = 'bad'
        
        return context
    
    def _extract_local_context(self, text: str) -> Dict[str, Any]:
        """Extract context specific to this activity"""
        context = {}
        
        # Location context
        for location in self.context_clues['location']:
            if location in text:
                context['location'] = location
                break
        
        # Social context
        for social in self.context_clues['with_others']:
            if social in text:
                context['with_others'] = True
                break
        
        if any(word in text for word in ['alone', 'solo', 'by myself']):
            context['with_others'] = False
        
        # Tool/equipment context
        for tool in self.context_clues['tools']:
            if tool in text:
                context['tools'] = context.get('tools', [])
                context['tools'].append(tool)
        
        return context
    
    def _detect_mood(self, text: str) -> str:
        """Detect mood from text"""
        for mood, indicators in self.mood_indicators.items():
            if any(indicator in text for indicator in indicators):
                return mood
        return 'neutral'
    
    def _estimate_intensity_advanced(self, text: str, category: str) -> str:
        """Advanced intensity estimation"""
        # Check for explicit intensity keywords
        for intensity, keywords in self.intensity_keywords.items():
            if any(keyword in text for keyword in keywords):
                return intensity
        
        # Category-based default with context adjustments
        category_defaults = {
            'exercise': 'medium',
            'study': 'medium',
            'work': 'medium',
            'entertainment': 'low',
            'habits': 'low',
            'social': 'low',
            'creative': 'medium',
            'wellness': 'low',
            'travel': 'medium'
        }
        
        base_intensity = category_defaults.get(category, 'medium')
        
        # Adjust based on duration
        duration = self._extract_duration_advanced(text)
        if duration > 120:  # > 2 hours
            if base_intensity == 'low':
                return 'medium'
        elif duration < 20:  # < 20 minutes
            if base_intensity == 'medium':
                return 'high'  # Short bursts are often intense
        
        return base_intensity
    
    def _post_process_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Post-process activities for consistency and enhancement"""
        # Remove duplicates
        seen = set()
        unique_activities = []
        for activity in activities:
            text_key = activity['text'].lower().strip()
            if text_key not in seen:
                seen.add(text_key)
                unique_activities.append(activity)
        
        # Merge similar activities
        merged_activities = self._merge_similar_activities(unique_activities)
        
        # Add sequence information
        for i, activity in enumerate(merged_activities):
            activity['sequence_order'] = i + 1
            activity['is_first'] = i == 0
            activity['is_last'] = i == len(merged_activities) - 1
        
        return merged_activities
    
    def _merge_similar_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge similar activities (e.g., multiple episodes)"""
        merged = []
        i = 0
        
        while i < len(activities):
            current = activities[i]
            
            # Look for similar activities to merge
            j = i + 1
            total_duration = current['duration']
            merged_count = 1
            
            while j < len(activities):
                next_activity = activities[j]
                if (current['category'] == next_activity['category'] and 
                    current['subcategory'] == next_activity['subcategory'] and
                    abs(current['duration'] - next_activity['duration']) < 10):
                    
                    total_duration += next_activity['duration']
                    merged_count += 1
                    j += 1
                else:
                    break
            
            # Create merged activity
            if merged_count > 1:
                current['duration'] = total_duration
                current['text'] = f"{current['text']} (×{merged_count})"
                current['merged_count'] = merged_count
            
            merged.append(current)
            i = j
        
        return merged
    
    def _create_default_activity(self, original_input: str) -> Dict[str, Any]:
        """Create a default activity when parsing fails"""
        return {
            'text': original_input,
            'category': 'other',
            'subcategory': 'general',
            'duration': 30,
            'intensity': 'medium',
            'mood': 'neutral',
            'context': {},
            'confidence': 0.0,
            'parsed_elements': {
                'has_duration': False,
                'has_mood_indicator': False,
                'has_intensity_modifier': False,
                'has_location': False,
                'social_activity': False
            },
            'sequence_order': 1,
            'is_first': True,
            'is_last': True
        }