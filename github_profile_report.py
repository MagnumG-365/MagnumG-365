#!/usr/bin/env python3
"""
GitHub Profile Report Generator

This script generates a comprehensive report for any GitHub user profile,
including statistics, repositories, contributions, and activity analysis.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional
import requests
from collections import Counter


class GitHubProfileReporter:
    """Generate comprehensive reports for GitHub user profiles."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub Profile Reporter.

        Args:
            token: Optional GitHub personal access token for authenticated requests
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the GitHub API.

        Args:
            endpoint: API endpoint (without base URL)
            params: Optional query parameters

        Returns:
            JSON response as dictionary or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Error: Resource not found - {endpoint}", file=sys.stderr)
                return None
            elif response.status_code == 403:
                print(f"Error: Rate limit exceeded or forbidden. Consider using a GitHub token.", file=sys.stderr)
                return None
            else:
                print(f"Error: API request failed with status {response.status_code}", file=sys.stderr)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Request failed - {e}", file=sys.stderr)
            return None

    def _get_all_pages(self, endpoint: str, params: Optional[Dict] = None, max_pages: int = 10) -> List[Dict]:
        """
        Fetch all pages of paginated results.

        Args:
            endpoint: API endpoint
            params: Optional query parameters
            max_pages: Maximum number of pages to fetch

        Returns:
            List of all items from all pages
        """
        all_items = []
        params = params or {}
        params['per_page'] = 100
        params['page'] = 1

        for _ in range(max_pages):
            data = self._make_request(endpoint, params)
            if not data or not isinstance(data, list):
                break

            all_items.extend(data)

            if len(data) < 100:  # Last page
                break

            params['page'] += 1

        return all_items

    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Fetch user profile information.

        Args:
            username: GitHub username

        Returns:
            User profile data or None if error
        """
        return self._make_request(f"/users/{username}")

    def get_user_repos(self, username: str) -> List[Dict]:
        """
        Fetch all repositories for a user.

        Args:
            username: GitHub username

        Returns:
            List of repository data
        """
        return self._get_all_pages(f"/users/{username}/repos", {'sort': 'updated'})

    def get_user_events(self, username: str) -> List[Dict]:
        """
        Fetch recent public events for a user.

        Args:
            username: GitHub username

        Returns:
            List of event data
        """
        return self._get_all_pages(f"/users/{username}/events", max_pages=3)

    def analyze_repositories(self, repos: List[Dict]) -> Dict:
        """
        Analyze repository statistics.

        Args:
            repos: List of repository data

        Returns:
            Dictionary of repository statistics
        """
        if not repos:
            return {}

        total_repos = len(repos)
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        total_watchers = sum(repo.get('watchers_count', 0) for repo in repos)
        total_size = sum(repo.get('size', 0) for repo in repos)

        # Language distribution
        languages = [repo.get('language') for repo in repos if repo.get('language')]
        language_counts = Counter(languages)

        # Most starred repos
        most_starred = sorted(
            repos,
            key=lambda x: x.get('stargazers_count', 0),
            reverse=True
        )[:5]

        # Most forked repos
        most_forked = sorted(
            repos,
            key=lambda x: x.get('forks_count', 0),
            reverse=True
        )[:5]

        # Recently updated repos
        recently_updated = sorted(
            repos,
            key=lambda x: x.get('updated_at', ''),
            reverse=True
        )[:5]

        # Count by type
        sources = sum(1 for repo in repos if not repo.get('fork', False))
        forks = sum(1 for repo in repos if repo.get('fork', False))

        return {
            'total_repos': total_repos,
            'source_repos': sources,
            'forked_repos': forks,
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_watchers': total_watchers,
            'total_size_kb': total_size,
            'languages': dict(language_counts.most_common()),
            'most_starred': most_starred,
            'most_forked': most_forked,
            'recently_updated': recently_updated,
        }

    def analyze_activity(self, events: List[Dict]) -> Dict:
        """
        Analyze user activity from events.

        Args:
            events: List of event data

        Returns:
            Dictionary of activity statistics
        """
        if not events:
            return {}

        event_types = Counter(event.get('type') for event in events)

        # Count contributions
        push_events = sum(1 for event in events if event.get('type') == 'PushEvent')
        pr_events = sum(1 for event in events if event.get('type') == 'PullRequestEvent')
        issue_events = sum(1 for event in events if event.get('type') == 'IssuesEvent')

        return {
            'total_events': len(events),
            'event_types': dict(event_types.most_common()),
            'push_events': push_events,
            'pull_request_events': pr_events,
            'issue_events': issue_events,
        }

    def generate_report(self, username: str, output_format: str = 'markdown') -> Optional[str]:
        """
        Generate a comprehensive profile report.

        Args:
            username: GitHub username
            output_format: Output format ('markdown', 'json', or 'text')

        Returns:
            Formatted report string or None if error
        """
        print(f"Fetching profile for {username}...", file=sys.stderr)

        # Fetch all data
        profile = self.get_user_profile(username)
        if not profile:
            return None

        print(f"Fetching repositories...", file=sys.stderr)
        repos = self.get_user_repos(username)

        print(f"Fetching recent activity...", file=sys.stderr)
        events = self.get_user_events(username)

        # Analyze data
        repo_stats = self.analyze_repositories(repos)
        activity_stats = self.analyze_activity(events)

        # Generate report based on format
        if output_format == 'json':
            return self._generate_json_report(profile, repo_stats, activity_stats)
        elif output_format == 'text':
            return self._generate_text_report(profile, repo_stats, activity_stats)
        else:  # markdown
            return self._generate_markdown_report(profile, repo_stats, activity_stats)

    def _generate_markdown_report(self, profile: Dict, repo_stats: Dict, activity_stats: Dict) -> str:
        """Generate a Markdown formatted report."""
        lines = []
        lines.append(f"# GitHub Profile Report: {profile.get('login', 'Unknown')}")
        lines.append("")
        lines.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("")

        # Profile Information
        lines.append("## Profile Information")
        lines.append("")
        if profile.get('name'):
            lines.append(f"**Name:** {profile['name']}")
        lines.append(f"**Username:** {profile.get('login', 'N/A')}")
        if profile.get('bio'):
            lines.append(f"**Bio:** {profile['bio']}")
        if profile.get('company'):
            lines.append(f"**Company:** {profile['company']}")
        if profile.get('location'):
            lines.append(f"**Location:** {profile['location']}")
        if profile.get('blog'):
            lines.append(f"**Website:** {profile['blog']}")
        if profile.get('email'):
            lines.append(f"**Email:** {profile['email']}")
        lines.append(f"**Public Repos:** {profile.get('public_repos', 0)}")
        lines.append(f"**Public Gists:** {profile.get('public_gists', 0)}")
        lines.append(f"**Followers:** {profile.get('followers', 0)}")
        lines.append(f"**Following:** {profile.get('following', 0)}")
        lines.append(f"**Account Created:** {profile.get('created_at', 'N/A')}")
        lines.append(f"**Profile URL:** {profile.get('html_url', 'N/A')}")
        lines.append("")

        # Repository Statistics
        if repo_stats:
            lines.append("## Repository Statistics")
            lines.append("")
            lines.append(f"**Total Repositories:** {repo_stats.get('total_repos', 0)}")
            lines.append(f"**Source Repositories:** {repo_stats.get('source_repos', 0)}")
            lines.append(f"**Forked Repositories:** {repo_stats.get('forked_repos', 0)}")
            lines.append(f"**Total Stars Received:** {repo_stats.get('total_stars', 0)}")
            lines.append(f"**Total Forks:** {repo_stats.get('total_forks', 0)}")
            lines.append(f"**Total Watchers:** {repo_stats.get('total_watchers', 0)}")
            lines.append("")

            # Language Distribution
            if repo_stats.get('languages'):
                lines.append("### Language Distribution")
                lines.append("")
                for lang, count in repo_stats['languages'].items():
                    lines.append(f"- **{lang}:** {count} repositories")
                lines.append("")

            # Most Starred Repositories
            if repo_stats.get('most_starred'):
                lines.append("### Most Starred Repositories")
                lines.append("")
                for repo in repo_stats['most_starred'][:5]:
                    stars = repo.get('stargazers_count', 0)
                    name = repo.get('name', 'Unknown')
                    desc = repo.get('description', 'No description')
                    url = repo.get('html_url', '')
                    if stars > 0:
                        lines.append(f"- **[{name}]({url})** - {stars} stars")
                        if desc:
                            lines.append(f"  - {desc}")
                lines.append("")

            # Recently Updated Repositories
            if repo_stats.get('recently_updated'):
                lines.append("### Recently Updated Repositories")
                lines.append("")
                for repo in repo_stats['recently_updated'][:5]:
                    name = repo.get('name', 'Unknown')
                    updated = repo.get('updated_at', 'N/A')
                    url = repo.get('html_url', '')
                    lines.append(f"- **[{name}]({url})** - Updated: {updated}")
                lines.append("")

        # Activity Statistics
        if activity_stats:
            lines.append("## Recent Activity Statistics")
            lines.append("")
            lines.append(f"**Total Recent Events:** {activity_stats.get('total_events', 0)}")
            lines.append(f"**Push Events:** {activity_stats.get('push_events', 0)}")
            lines.append(f"**Pull Request Events:** {activity_stats.get('pull_request_events', 0)}")
            lines.append(f"**Issue Events:** {activity_stats.get('issue_events', 0)}")
            lines.append("")

            if activity_stats.get('event_types'):
                lines.append("### Event Type Breakdown")
                lines.append("")
                for event_type, count in activity_stats['event_types'].items():
                    lines.append(f"- **{event_type}:** {count}")
                lines.append("")

        lines.append("---")
        lines.append("*Report generated by GitHub Profile Report Generator*")

        return "\n".join(lines)

    def _generate_text_report(self, profile: Dict, repo_stats: Dict, activity_stats: Dict) -> str:
        """Generate a plain text formatted report."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"GitHub Profile Report: {profile.get('login', 'Unknown')}")
        lines.append("=" * 70)
        lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("")

        # Profile Information
        lines.append("PROFILE INFORMATION")
        lines.append("-" * 70)
        if profile.get('name'):
            lines.append(f"Name:            {profile['name']}")
        lines.append(f"Username:        {profile.get('login', 'N/A')}")
        if profile.get('bio'):
            lines.append(f"Bio:             {profile['bio']}")
        if profile.get('company'):
            lines.append(f"Company:         {profile['company']}")
        if profile.get('location'):
            lines.append(f"Location:        {profile['location']}")
        lines.append(f"Public Repos:    {profile.get('public_repos', 0)}")
        lines.append(f"Followers:       {profile.get('followers', 0)}")
        lines.append(f"Following:       {profile.get('following', 0)}")
        lines.append(f"Account Created: {profile.get('created_at', 'N/A')}")
        lines.append("")

        # Repository Statistics
        if repo_stats:
            lines.append("REPOSITORY STATISTICS")
            lines.append("-" * 70)
            lines.append(f"Total Repositories:  {repo_stats.get('total_repos', 0)}")
            lines.append(f"Source Repositories: {repo_stats.get('source_repos', 0)}")
            lines.append(f"Forked Repositories: {repo_stats.get('forked_repos', 0)}")
            lines.append(f"Total Stars:         {repo_stats.get('total_stars', 0)}")
            lines.append(f"Total Forks:         {repo_stats.get('total_forks', 0)}")
            lines.append("")

            if repo_stats.get('languages'):
                lines.append("Language Distribution:")
                for lang, count in repo_stats['languages'].items():
                    lines.append(f"  - {lang}: {count} repositories")
                lines.append("")

        # Activity Statistics
        if activity_stats:
            lines.append("RECENT ACTIVITY")
            lines.append("-" * 70)
            lines.append(f"Total Events:         {activity_stats.get('total_events', 0)}")
            lines.append(f"Push Events:          {activity_stats.get('push_events', 0)}")
            lines.append(f"Pull Request Events:  {activity_stats.get('pull_request_events', 0)}")
            lines.append(f"Issue Events:         {activity_stats.get('issue_events', 0)}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def _generate_json_report(self, profile: Dict, repo_stats: Dict, activity_stats: Dict) -> str:
        """Generate a JSON formatted report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'profile': profile,
            'repository_statistics': repo_stats,
            'activity_statistics': activity_stats,
        }
        return json.dumps(report, indent=2)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Generate a comprehensive GitHub profile report for any user.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python github_profile_report.py torvalds
  python github_profile_report.py octocat --format json
  python github_profile_report.py github --token YOUR_TOKEN --output report.md
        '''
    )

    parser.add_argument(
        'username',
        help='GitHub username to generate report for'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'json', 'text'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    parser.add_argument(
        '--token', '-t',
        help='GitHub personal access token for authenticated requests (optional but recommended)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (prints to stdout if not specified)'
    )

    args = parser.parse_args()

    # Create reporter
    reporter = GitHubProfileReporter(token=args.token)

    # Generate report
    report = reporter.generate_report(args.username, output_format=args.format)

    if report is None:
        print(f"Failed to generate report for {args.username}", file=sys.stderr)
        sys.exit(1)

    # Output report
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)


if __name__ == '__main__':
    main()
