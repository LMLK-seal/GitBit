# gitbit/main.py

import os
import json
from github import Github
from bot import GitBitBot

def main():
    """
    Main function to run the GitBit bot.
    It initializes the bot and processes the new issue.
    """
    # --- GitHub API Authentication ---
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return
    g = Github(github_token)

    # --- Get Repository and Issue Information from GitHub Actions context ---
    repo_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_name:
        print("Error: GITHUB_REPOSITORY environment variable not set.")
        return
    repo = g.get_repo(repo_name)

    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("Error: GITHUB_EVENT_PATH environment variable not set.")
        return

    with open(event_path, 'r') as f:
        event_data = json.load(f)
    
    # We are only interested in newly opened issues
    if event_data.get("action") != "opened":
        print("This action is not a new issue. Exiting.")
        return

    issue_number = event_data["issue"]["number"]
    issue = repo.get_issue(number=issue_number)

    print(f"Processing new issue #{issue.number}: '{issue.title}' in repository {repo.full_name}")

    # --- Initialize and Run the Bot ---
    try:
        bot = GitBitBot(repo, issue)
        bot.run()
    except FileNotFoundError:
        print(f"Configuration file .gitbit.yml not found in the root of {repo.full_name}.")
        print("Please create the .gitbit.yml configuration file.")
        # Optionally, you could post a comment to the issue about the missing config
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Consider logging this error to an issue for debugging
        
if __name__ == "__main__":
    main()