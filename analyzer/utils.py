QUESTIONS = [
    {
        "text": "You have an unexpected free evening. What do you do?",
        "options": [
            "Go out immediately",
            "Think of a few options first",
            "Plan the evening carefully",
        ],
    },
    {
        "text": "You need to buy a phone. How do you choose?",
        "options": [
            "Pick the one that looks best",
            "Compare a few and decide",
            "Research everything in detail",
        ],
    },
    {
        "text": "In a quiz, when unsure, you usually...",
        "options": [
            "Answer quickly",
            "Pause and think briefly",
            "Take time before choosing",
        ],
    },
    {
        "text": "When selecting food at a restaurant, you...",
        "options": [
            "Order fast",
            "Look at a few options",
            "Read the whole menu carefully",
        ],
    },
    {
        "text": "Before making a decision, you usually...",
        "options": [
            "Trust instinct",
            "Use instinct plus some thought",
            "Analyze all possibilities",
        ],
    },
]


def classify_decision_style(avg_response_time, total_hesitations):
    if avg_response_time < 3 and total_hesitations <= 1:
        return "Impulsive"
    elif avg_response_time >= 5 or total_hesitations >= 3:
        return "Analytical"
    return "Balanced"
