
import os
import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Executor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        
        # Calorie estimates per minute by activity category
        self.calorie_rates = {
            'exercise': 8,  # calories per minute
            'walk': 5,
            'study': 1,
            'work': 1.5,
            'entertainment': 1,
            'habits': 2,
            'social': 1.5,
            'other': 1
        }
        
    def process_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process each activity to generate motivation and calculate calories"""
        results = []
        
        for activity in activities:
            # Calculate calories
            calories = self._calculate_calories(activity)
            
            # Generate motivational response
            motivation = self._generate_motivation(activity)
            
            result = {
                **activity,
                'calories_burned': calories,
                'motivation_message': motivation,
                'productivity_score': self._calculate_productivity_score(activity)
            }
            
            results.append(result)
            
        return results
    
    def _calculate_calories(self, activity: Dict[str, Any]) -> int:
        """Calculate estimated calories burned"""
        category = activity['category']
        duration = activity['duration']
        intensity = activity['intensity']
        
        # Base rate from category
        if any(kw in activity['text'].lower() for kw in ['walk', 'walking']):
            base_rate = self.calorie_rates['walk']
        else:
            base_rate = self.calorie_rates.get(category, 1)
        
        # Intensity multiplier
        intensity_multiplier = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.3
        }.get(intensity, 1.0)
        
        calories = int(base_rate * duration * intensity_multiplier)
        return max(calories, 1)  # Minimum 1 calorie
    
    def _generate_motivation(self, activity: Dict[str, Any]) -> str:
        """Generate motivational or sarcastic response using Gemini API"""
        if not self.api_key:
            return self._get_fallback_motivation(activity)
        
        try:
            prompt = self._create_prompt(activity)
            response = self._call_gemini_api(prompt)
            return response
        except Exception as e:
            print(f"API Error: {e}")
            return self._get_fallback_motivation(activity)
    
    def _create_prompt(self, activity: Dict[str, Any]) -> str:
        """Create enhanced prompt for Gemini API with context awareness"""
        activity_text = activity['text']
        category = activity['category']
        subcategory = activity.get('subcategory', 'general')
        duration = activity['duration']
        intensity = activity['intensity']
        mood = activity.get('mood', 'neutral')
        context = activity.get('context', {})
        productivity_score = activity.get('productivity_score', 5)
        
        # Build context string
        context_parts = []
        if 'location' in context:
            context_parts.append(f"at {context['location']}")
        if context.get('with_others'):
            context_parts.append("with others")
        elif context.get('with_others') == False:
            context_parts.append("alone")
        if 'time_of_day' in context:
            context_parts.append(f"in the {context['time_of_day']}")
        if 'weather' in context:
            context_parts.append(f"weather was {context['weather']}")
        
        context_str = ", ".join(context_parts)
        
        prompt = f"""
You're RoastBot, a witty AI life coach with a sharp tongue and a heart of gold. The user shares what they did today.

Your personality:
- Savage but ultimately motivational
- Funny and memorable
- Tailored responses based on context
- Mix of roasting and genuine encouragement
- Reference specific details when possible

Activity Details:
- What they did: "{activity_text}"
- Category: {category} ({subcategory})
- Duration: {duration} minutes
- Intensity: {intensity}
- Mood during activity: {mood}
- Context: {context_str if context_str else "no specific context"}
- Productivity score: {productivity_score}/10

Response guidelines:
- If productivity score ≥ 7: Praise with playful skepticism
- If productivity score 4-6: Gentle roasting with encouragement  
- If productivity score ≤ 3: Full roast mode but end with motivation
- Reference specific details (duration, location, mood) when relevant
- Keep it 1-2 sentences, punchy and memorable
- Be creative with wordplay and humor

Generate your roast/motivation response:
"""
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API with improved error handling"""
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
                else:
                    raise Exception("No candidates in API response")
            elif response.status_code == 429:
                raise Exception("API rate limit exceeded - try again later")
            elif response.status_code == 400:
                raise Exception("Invalid API request - check your prompt")
            else:
                raise Exception(f"API call failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("API request timed out")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to Gemini API")
        except Exception as e:
            print(f"⚠️ Gemini API Error: {e}")
            raise e
    
    def _get_fallback_motivation(self, activity: Dict[str, Any]) -> str:
        """Fallback motivational messages when API is unavailable"""
        category = activity['category']
        text = activity['text'].lower()
        
        if category == 'exercise' or 'walk' in text:
            return "Look at you moving your body! Revolutionary concept. Keep it up, champ! 💪"
        elif category == 'study':
            return "Wow, learning something? Your brain cells are probably confused by the sudden activity. Impressive!"
        elif category == 'entertainment':
            if 'netflix' in text or 'tv' in text or 'movie' in text:
                return "Watched more shows? Inspirational. Truly. Your couch misses you when you're gone."
            return "Another day, another masterclass in professional time-wasting. Chef's kiss! 👌"
        elif category == 'work':
            return "Actually being productive? Who are you and what did you do with the real slacker?"
        elif 'sleep' in text:
            return "Sleep? The ultimate life hack. At least you're good at something!"
        else:
            return "Did... something today? Well, that's technically better than nothing. Barely."
    
    def _calculate_productivity_score(self, activity: Dict[str, Any]) -> int:
        """Calculate enhanced productivity score (1-10) with multiple factors"""
        category = activity['category']
        subcategory = activity.get('subcategory', 'general')
        duration = activity['duration']
        intensity = activity['intensity']
        mood = activity.get('mood', 'neutral')
        context = activity.get('context', {})
        
        # Enhanced base scores with subcategories
        base_scores = {
            'exercise': 8,
            'study': 9,
            'work': 7,
            'habits': 6,
            'social': 4,
            'entertainment': 2,
            'creative': 7,
            'wellness': 6,
            'travel': 5,
            'other': 3
        }
        
        # Subcategory modifiers
        subcategory_modifiers = {
            'programming': 1,  # Extra point for coding
            'reading': 1,      # Extra point for reading
            'cardio': 1,       # Extra point for cardio
            'strength': 1,     # Extra point for strength training
            'streaming': -1,   # Penalty for passive entertainment
            'social_media': -2 # Extra penalty for social media
        }
        
        base_score = base_scores.get(category, 3)
        base_score += subcategory_modifiers.get(subcategory, 0)
        
        # Duration adjustments (more nuanced)
        if duration > 180:  # > 3 hours
            if category in ['entertainment']:
                base_score -= 2  # Penalty for too much entertainment
            elif category in ['study', 'work']:
                base_score += 1  # Bonus for sustained productive work
        elif duration > 60:  # 1-3 hours
            base_score += 1
        elif duration < 15:  # < 15 minutes
            if category in ['exercise', 'habits']:
                base_score -= 1  # Too short for meaningful impact
            else:
                base_score += 1  # Quick tasks can be efficient
        
        # Intensity modifiers
        intensity_modifiers = {
            'high': 1,
            'medium': 0,
            'low': -1
        }
        base_score += intensity_modifiers.get(intensity, 0)
        
        # Mood modifiers
        mood_modifiers = {
            'positive': 1,
            'neutral': 0,
            'negative': -1
        }
        base_score += mood_modifiers.get(mood, 0)
        
        # Context modifiers
        if context.get('with_others') and category in ['exercise', 'study']:
            base_score += 1  # Bonus for social productive activities
        
        if context.get('location') == 'gym' and category == 'exercise':
            base_score += 1  # Bonus for going to gym
        
        if context.get('time_of_day') == 'morning' and category in ['exercise', 'study']:
            base_score += 1  # Morning productivity bonus
        
        # Sequence bonuses (if multiple productive activities)
        if activity.get('sequence_order', 1) > 1 and base_score >= 6:
            base_score += 1  # Consistency bonus
            
        return max(1, min(10, base_score))
