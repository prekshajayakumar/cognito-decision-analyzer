import statistics


QUESTIONS = [
    {
        "text": "You have an unexpected free evening. What do you do?",
        "options": ["Go out immediately", "Think of a few options first", "Plan the evening carefully"],
    },
    {
        "text": "You need to buy a phone. How do you choose?",
        "options": ["Pick the one that looks best", "Compare a few and decide", "Research everything in detail"],
    },
    {
        "text": "In a quiz, when unsure, you usually...",
        "options": ["Answer quickly", "Pause and think briefly", "Take time before choosing"],
    },
    {
        "text": "When selecting food at a restaurant, you...",
        "options": ["Order fast", "Look at a few options", "Read the whole menu carefully"],
    },
    {
        "text": "Before making a decision, you usually...",
        "options": ["Trust instinct", "Use instinct plus some thought", "Analyze all possibilities"],
    },
    {
        "text": "When a plan suddenly changes, you...",
        "options": ["React immediately", "Adjust after thinking briefly", "Reconsider the whole plan"],
    },
    {
        "text": "When solving a problem, you usually...",
        "options": ["Try the first idea", "Compare two possible solutions", "Analyze multiple solutions deeply"],
    },
    {
        "text": "When choosing between similar options, you...",
        "options": ["Pick quickly", "Think for a short while", "Take time to compare details"],
    },
]


def extract_features(responses):
    times = [r.response_time for r in responses]

    hesitation_count = sum(1 for t in times if t > 5)
    fast_answer_count = sum(1 for t in times if t < 3)
    slow_answer_count = sum(1 for t in times if t > 6)

    return {
        "avg_response_time": round(sum(times) / len(times), 2),
        "median_response_time": round(statistics.median(times), 2),
        "max_response_time": round(max(times), 2),
        "min_response_time": round(min(times), 2),
        "std_response_time": round(statistics.pstdev(times), 2),
        "total_time": round(sum(times), 2),
        "hesitation_count": hesitation_count,
        "hesitation_ratio": round(hesitation_count / len(times), 2),
        "fast_answer_count": fast_answer_count,
        "slow_answer_count": slow_answer_count,
    }
