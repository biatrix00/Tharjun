
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
        """Create prompt for Gemini API"""
        activity_text = activity['text']
        category = activity['category']
        duration = activity['duration']
        
        prompt = f"""
You're a savage AI life coach named *RoastBot*. The user shares what they did today. Your job:
- Praise them if they were productive (study, exercise, habit)
- Sarcastically insult them if they slacked (e.g. watched Netflix, did nothing)
- Respond in a short, funny, roast-style message (max 2 sentences)
- Never be boring
- Be witty and memorable

Activity: "{activity_text}"
Category: {category}
Duration: {duration} minutes

Generate a single roast/motivation message:
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
        """Calculate productivity score (1-10)"""
        category = activity['category']
        duration = activity['duration']
        
        base_scores = {
            'exercise': 8,
            'study': 9,
            'work': 7,
            'habits': 6,
            'social': 4,
            'entertainment': 2,
            'other': 3
        }
        
        base_score = base_scores.get(category, 3)
        
        # Duration bonus/penalty
        if duration > 60:
            base_score += 1
        elif duration < 15:
            base_score -= 1
            
        return max(1, min(10, base_score))
