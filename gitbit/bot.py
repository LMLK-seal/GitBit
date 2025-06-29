# gitbit/bot.py

import yaml
from . import tagger, assignee, linker

class GitBitBot:
    """
    The main bot class that orchestrates the analysis of a GitHub issue.
    """
    def __init__(self, repo, issue):
        self.repo = repo
        self.issue = issue
        self.config = self._load_config()

    def _load_config(self):
        """Loads the .gitbit.yml configuration file from the repository root."""
        try:
            config_content = self.repo.get_contents(".gitbit.yml").decoded_content
            return yaml.safe_load(config_content)
        except Exception as e:
            print(f"Error loading .gitbit.yml: {e}")
            raise FileNotFoundError(".gitbit.yml not found or is invalid.")

    def run(self):
        """
        Runs the full analysis pipeline and posts a summary comment on the issue.
        """
        issue_text = f"{self.issue.title} {self.issue.body}"

        # 1. Suggest tags
        suggested_tags = tagger.suggest_tags(issue_text, self.config.get('tag_keywords', {}))
        
        # 2. Recommend assignees
        max_scan = self.config.get('assignee_rec', {}).get('max_issues_to_scan', 100)
        recommended_assignees = assignee.recommend_assignees(self.repo, suggested_tags, max_scan)

        # 3. Find related issues
        threshold = self.config.get('issue_linking', {}).get('similarity_threshold', 0.7)
        related_issues = linker.find_related_issues(self.repo, self.issue, threshold)

        # 4. Format and post the comment
        comment = self._format_comment(suggested_tags, recommended_assignees, related_issues)
        
        if comment:
            self.issue.create_comment(comment)
            print("Successfully posted suggestions to the issue.")
        else:
            print("No suggestions to post.")

    def _format_comment(self, tags, assignees, issues):
        """Formats the bot's findings into a clean Markdown comment."""
        if not tags and not assignees and not issues:
            return None

        comment_parts = ["### 🤖 GitBit Bot Analysis\n\nI've analyzed this issue and have the following suggestions:\n"]

        if tags:
            tag_list = ", ".join([f"`{tag}`" for tag in tags])
            comment_parts.append(f"**🏷️ Suggested Labels:**\n{tag_list}\n")

        if assignees:
            assignee_list = ", ".join([f"@{user}" for user in assignees])
            comment_parts.append(f"**👤 Recommended Assignees:**\n{assignee_list} (based on their work on related issues)\n")
        
        if issues:
            issue_list = "\n".join([f"- Issue #{i.number}: {i.title}" for i in issues])
            comment_parts.append(f"**🔗 Potentially Related Issues:**\n{issue_list}\n")

        comment_parts.append("---\n*I am a bot. My suggestions are based on patterns in this repository. Please review them before applying.*")
        
        return "\n".join(comment_parts)