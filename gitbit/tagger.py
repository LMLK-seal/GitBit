# gitbit/tagger.py

import re

def suggest_tags(issue_text: str, tag_keyword_map: dict) -> list[str]:
    """
    Suggests tags for an issue based on keywords found in its text.

    Args:
        issue_text: The combined title and body of the issue.
        tag_keyword_map: A dictionary mapping tags to a list of keywords.

    Returns:
        A list of suggested tag names.
    """
    suggested_tags = []
    # Normalize text to lower case for case-insensitive matching
    normalized_text = issue_text.lower()

    for tag, keywords in tag_keyword_map.items():
        for keyword in keywords:
            # Use regex to find whole words to avoid partial matches (e.g., 'bug' in 'debug')
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', normalized_text):
                if tag not in suggested_tags:
                    suggested_tags.append(tag)
    
    return sorted(suggested_tags)