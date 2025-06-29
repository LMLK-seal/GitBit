# gitbit/assignee.py

from collections import defaultdict

def recommend_assignees(repo, suggested_tags: list[str], max_issues_to_scan: int) -> list[str]:
    """
    Recommends assignees based on their history of closing issues with similar tags.

    Args:
        repo: The PyGithub repository object.
        suggested_tags: A list of tags suggested for the new issue.
        max_issues_to_scan: The number of closed issues to analyze.

    Returns:
        A list of recommended assignee usernames, sorted by relevance.
    """
    if not suggested_tags:
        return []

    # Build an expertise map: {label: {user: count}}
    expertise_map = defaultdict(lambda: defaultdict(int))
    
    # Scan recent closed issues to build expertise profile
    closed_issues = repo.get_issues(state='closed', sort='updated', direction='desc')
    
    count = 0
    for issue in closed_issues:
        if count >= max_issues_to_scan:
            break
        
        # Only consider issues that were actually assigned and have labels
        if issue.assignee and issue.labels:
            for label in issue.labels:
                expertise_map[label.name][issue.assignee.login] += 1
        count += 1
    
    if not expertise_map:
        return []

    # Find best assignees for the suggested tags
    recommendation_scores = defaultdict(int)
    for tag in suggested_tags:
        if tag in expertise_map:
            # Find the top expert for this tag
            top_expert = max(expertise_map[tag], key=expertise_map[tag].get)
            recommendation_scores[top_expert] += 1 # Give a point to this expert
    
    # Sort recommended assignees by their score (how many tags they are an expert in)
    sorted_recommendations = sorted(recommendation_scores.keys(), key=lambda user: recommendation_scores[user], reverse=True)
    
    return sorted_recommendations