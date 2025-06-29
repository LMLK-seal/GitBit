# GitBit: Intelligent Issue Management Bot for GitHub

 <!-- You can create a simple logo -->

GitBit is a Python-based GitHub bot that streamlines issue management for repository maintainers. It uses natural language processing (NLP) and machine learning to automate repetitive tasks, making it an invaluable tool for managing large open-source projects.

## Key Features

-   **🤖 Automatic Issue Linking:** Analyzes new issue descriptions to detect and link semantically related or duplicate issues, reducing clutter and improving organization.
-   **🏷️ Smart Tagging:** Suggests relevant labels (e.g., `bug`, `documentation`, `feature-request`) based on the issue's content, ensuring consistent and meaningful categorization.
-   **👤 Assignee Recommendations:** Recommends contributors to assign issues to, based on their past contributions and expertise demonstrated in previously closed issues.

## Why It’s Unique

While there are many tools for GitHub automation, GitBit combines NLP and machine learning to provide **intelligent, context-aware suggestions** tailored to each repository. Its focus on issue management—a critical yet time-consuming task—sets it apart from generic bots or static analysis tools.

## How It Works

GitBit is deployed as a GitHub Action that triggers whenever a new issue is opened in your repository. Here's the process:

1.  **Trigger:** A new issue is created.
2.  **Analysis:** The bot reads the issue's title and body.
3.  **Processing:**
    *   It compares the new issue's text to a keyword map in your config file to suggest labels.
    *   It scans recently closed issues to find which users are experts on topics related to the suggested labels.
    *   It uses TF-IDF vectorization and cosine similarity to find other open issues with similar content.
4.  **Comment:** The bot posts a single, helpful comment on the new issue with all its suggestions, allowing maintainers to review and apply them with a single click.

---

## 🚀 Setup Instructions

Setting up GitBit takes less than 5 minutes.

### Step 1: Create the Configuration File

In the root of your repository, create a file named `.gitbit.yml`. This file controls the bot's behavior.

**Copy and paste this template into `.gitbit.yml` and customize it for your project:**

```yaml
# .gitbit.yml

# --- Smart Tagging Configuration ---
# Map labels to keywords. The bot will suggest a label if an issue's
# title or body contains any of the associated keywords.
tag_keywords:
  bug:
    - error
    - exception
    - traceback
    - panic
    - crash
    - fail
  documentation:
    - docs
    - readme
    - help
    - example
    - tutorial
  feature-request:
    - feature
    - enhance
    - improvement
    - idea
  question:
    - how to
    - what is
    - why

# --- Assignee Recommendation Configuration ---
# The number of recently closed issues to scan to build an expertise profile.
# A higher number is more accurate but slower.
assignee_rec:
  max_issues_to_scan: 100

# --- Issue Linking Configuration ---
# The similarity score required to consider an issue "related".
# Value should be between 0.0 and 1.0. Higher is more strict.
# A good starting point is 0.7.
issue_linking:
  similarity_threshold: 0.7