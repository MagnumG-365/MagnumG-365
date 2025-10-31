#!/usr/bin/env python3
"""
Gaming Stats Tracker for GitHub Profile
Integrates with various gaming platforms to display stats
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class GamingStatsTracker:
    """Track and display gaming statistics across platforms."""

    def __init__(self):
        """Initialize the gaming stats tracker."""
        self.stats = {
            "xbox": {
                "gamertag": "EternalNightmar",
                "platform": "Xbox Live",
                "profile_url": "https://www.xbox.com/en-US/play/user/EternalNightmar",
            },
            "gaming_profile": {
                "motto": "Code by day, game by night 🌙",
                "favorite_genres": ["Action/Adventure", "RPG", "Racing", "FPS"],
                "platforms": ["Xbox", "PC", "PlayStation"],
            },
            "current_games": [
                {
                    "name": "Halo Infinite",
                    "platform": "Xbox",
                    "status": "Active",
                    "progress": "Campaign Complete, Multiplayer Active",
                },
                {
                    "name": "Forza Horizon 5",
                    "platform": "Xbox",
                    "status": "Active",
                    "progress": "Exploring Mexico",
                },
                {
                    "name": "Starfield",
                    "platform": "Xbox/PC",
                    "status": "Active",
                    "progress": "Main Quest in Progress",
                },
            ],
            "achievements": {
                "total_games_played": "100+",
                "completion_rate": "High",
                "achievement_hunter": True,
                "competitive_player": True,
            },
        }

    def get_xbox_stats(self) -> Dict:
        """
        Get Xbox Live statistics.

        Returns:
            Dictionary of Xbox stats
        """
        return self.stats["xbox"]

    def get_current_games(self) -> List[Dict]:
        """
        Get currently playing games.

        Returns:
            List of current games
        """
        return self.stats["current_games"]

    def get_gaming_profile(self) -> Dict:
        """
        Get overall gaming profile.

        Returns:
            Dictionary of gaming profile info
        """
        return self.stats["gaming_profile"]

    def generate_stats_markdown(self) -> str:
        """
        Generate markdown formatted gaming stats.

        Returns:
            Markdown formatted string
        """
        lines = []
        lines.append("# Gaming Statistics")
        lines.append("")
        lines.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("")

        # Xbox Profile
        xbox = self.stats["xbox"]
        lines.append("## Xbox Live Profile")
        lines.append("")
        lines.append(f"- **Gamertag:** {xbox['gamertag']}")
        lines.append(f"- **Platform:** {xbox['platform']}")
        lines.append(f"- **Profile:** [View on Xbox]({xbox['profile_url']})")
        lines.append("")

        # Current Games
        lines.append("## Currently Playing")
        lines.append("")
        for game in self.stats["current_games"]:
            lines.append(f"### {game['name']}")
            lines.append(f"- **Platform:** {game['platform']}")
            lines.append(f"- **Status:** {game['status']}")
            lines.append(f"- **Progress:** {game['progress']}")
            lines.append("")

        # Gaming Profile
        profile = self.stats["gaming_profile"]
        lines.append("## Gaming Profile")
        lines.append("")
        lines.append(f"**Motto:** {profile['motto']}")
        lines.append("")
        lines.append("**Platforms:**")
        for platform in profile["platforms"]:
            lines.append(f"- {platform}")
        lines.append("")
        lines.append("**Favorite Genres:**")
        for genre in profile["favorite_genres"]:
            lines.append(f"- {genre}")
        lines.append("")

        return "\n".join(lines)

    def save_stats_json(self, filepath: str = "gaming_stats.json"):
        """
        Save stats to JSON file.

        Args:
            filepath: Path to save JSON file
        """
        stats_with_timestamp = {
            "last_updated": datetime.now().isoformat(),
            "stats": self.stats,
        }

        with open(filepath, "w") as f:
            json.dump(stats_with_timestamp, f, indent=2)

        print(f"Stats saved to {filepath}")

    def update_profile_readme(self, readme_path: str = "PROFILE_README.md"):
        """
        Update specific sections of the profile README with latest stats.

        Args:
            readme_path: Path to the profile README file
        """
        # This would update dynamic sections of the README
        # For now, we'll just print a message
        print(f"Profile README at {readme_path} can be updated with latest stats")
        print("Stats are embedded in the profile README template")


def main():
    """Main function for CLI usage."""
    tracker = GamingStatsTracker()

    print("Gaming Stats Tracker")
    print("=" * 50)
    print()

    # Display Xbox stats
    xbox = tracker.get_xbox_stats()
    print(f"Xbox Gamertag: {xbox['gamertag']}")
    print(f"Profile: {xbox['profile_url']}")
    print()

    # Display current games
    print("Currently Playing:")
    for game in tracker.get_current_games():
        print(f"  - {game['name']} ({game['platform']})")
    print()

    # Generate markdown
    print("Generating markdown stats...")
    markdown = tracker.generate_stats_markdown()
    print(markdown)
    print()

    # Save JSON
    tracker.save_stats_json()
    print()

    # Update README
    tracker.update_profile_readme()


if __name__ == "__main__":
    main()
