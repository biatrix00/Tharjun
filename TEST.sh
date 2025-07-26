
#!/bin/bash

echo "🧪 Testing MotivAgent..."
echo "=========================="

# Test 1: Direct CLI usage
echo "Test 1: Direct input mode"
python3 main.py "walked 20 minutes and watched 3 episodes of One Piece"

echo -e "\n\n"

# Test 2: Interactive mode with predefined inputs
echo "Test 2: Module imports"
python3 -c "
from src.planner import Planner
from src.executor import Executor
from src.memory import Memory
from src.insight import Insight

# Test planner
planner = Planner()
activities = planner.parse_input('walked 30 min and studied for 2 hours')
print(f'✅ Planner: Parsed {len(activities)} activities')

# Test executor
executor = Executor()
results = executor.process_activities(activities)
print(f'✅ Executor: Processed {len(results)} activities')

# Test memory
memory = Memory()
memory.store_session(results)
print('✅ Memory: Stored session successfully')

# Test insights
insight = Insight(memory)
trends = insight.analyze_weekly_trends()
print('✅ Insights: Generated weekly analysis')

print('\\n🎉 All tests passed! MotivAgent is ready to roast!')
"

echo -e "\n✅ Testing complete!"
