# gitbit/linker.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_related_issues(repo, new_issue, similarity_threshold: float) -> list:
    """
    Finds issues that are semantically similar to a new issue.

    Args:
        repo: The PyGithub repository object.
        new_issue: The new issue object to compare against.
        similarity_threshold: The minimum cosine similarity score to be considered related.

    Returns:
        A list of PyGithub Issue objects that are potentially related.
    """
    open_issues = repo.get_issues(state='open')
    
    # Create a corpus of documents (issue title + body)
    issue_map = {}
    corpus = []
    
    for issue in open_issues:
        # Exclude the new issue itself from the comparison list
        if issue.number == new_issue.number:
            continue
        
        issue_text = f"{issue.title} {issue.body}"
        issue_map[len(corpus)] = issue # Map corpus index to issue object
        corpus.append(issue_text)

    if not corpus:
        return [] # No other open issues to compare against

    # Add the new issue's text to the end of the corpus for vectorization
    new_issue_text = f"{new_issue.title} {new_issue.body}"
    corpus.append(new_issue_text)
    
    # Vectorize the text using TF-IDF
    try:
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        # This can happen if the corpus is empty or contains only stop words.
        return []

    # Calculate cosine similarity between the new issue and all others
    # The new issue is the last one in the matrix
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Find issues that exceed the similarity threshold
    related_issues = []
    similar_indices = cosine_sim[0].argsort()[:-5:-1] # Get top 4 most similar indices

    for i in similar_indices:
        if cosine_sim[0][i] > similarity_threshold:
            related_issues.append(issue_map[i])
            
    return related_issues