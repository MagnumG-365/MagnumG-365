# 🎮 MagnumG-365 - GitHub Profile Repository

This is a special GitHub profile repository featuring an Xbox gaming-themed profile for **EternalNightmar** and utilities for GitHub profile management.

## 📋 Repository Contents

This repository serves two purposes:

1. **GitHub Profile README** - A gaming-themed profile showcase for the gamertag [EternalNightmar](https://www.xbox.com/en-US/play/user/EternalNightmar)
2. **GitHub Profile Tools** - Python utilities for generating GitHub profile reports and managing gaming stats

## 🎯 Profile README

The main profile README (`PROFILE_README.md`) features:
- Xbox gaming theme with EternalNightmar gamertag
- GitHub statistics and activity graphs
- Gaming stats and current games
- Tech stack and skills showcase
- Social links and contact information

To use this as your GitHub profile README:
1. Create a repository with the same name as your GitHub username
2. Copy `PROFILE_README.md` to `README.md` in that repository
3. Customize with your information
4. Add custom assets to the `assets/` directory

## 🛠️ Included Tools

### 1. GitHub Profile Report Generator (`github_profile_report.py`)

A comprehensive Python tool to generate detailed reports for any GitHub user profile. This tool fetches profile information, repository statistics, contribution activity, and generates formatted reports in multiple formats.

### 2. Gaming Stats Tracker (`gaming_stats.py`)

Track and display gaming statistics across platforms, specifically designed for Xbox Live integration and the EternalNightmar gamertag.

---

## 📦 Features

- Fetch complete GitHub user profile information
- Analyze repository statistics (stars, forks, languages, etc.)
- Track recent activity and contributions
- Generate reports in multiple formats:
  - Markdown (default) - Perfect for documentation
  - JSON - Machine-readable format
  - Plain Text - Simple, clean output
- Support for both authenticated and unauthenticated requests
- Language distribution analysis
- Top starred and recently updated repositories
- Activity breakdown by event types

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd MagnumG-365
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install requests python-dotenv
```

## Usage

### Basic Usage

Generate a Markdown report for any GitHub user:

```bash
python github_profile_report.py <username>
```

Example:
```bash
python github_profile_report.py torvalds
```

### Output Formats

Generate reports in different formats:

```bash
# Markdown format (default)
python github_profile_report.py octocat --format markdown

# JSON format
python github_profile_report.py octocat --format json

# Plain text format
python github_profile_report.py octocat --format text
```

### Save to File

Save the report to a file instead of printing to stdout:

```bash
python github_profile_report.py octocat --output report.md
python github_profile_report.py octocat --format json --output report.json
```

### Authenticated Requests

For higher rate limits and access to private data, use a GitHub personal access token:

```bash
python github_profile_report.py octocat --token YOUR_GITHUB_TOKEN
```

You can create a personal access token at: https://github.com/settings/tokens

### Command-Line Options

```
usage: github_profile_report.py [-h] [--format {markdown,json,text}]
                                [--token TOKEN] [--output OUTPUT] username

Generate a comprehensive GitHub profile report for any user.

positional arguments:
  username              GitHub username to generate report for

optional arguments:
  -h, --help            show this help message and exit
  --format {markdown,json,text}, -f {markdown,json,text}
                        Output format (default: markdown)
  --token TOKEN, -t TOKEN
                        GitHub personal access token for authenticated requests
  --output OUTPUT, -o OUTPUT
                        Output file path (prints to stdout if not specified)
```

## Report Contents

The generated report includes:

### Profile Information
- Name, username, and bio
- Company and location
- Website and email
- Public repositories and gists count
- Followers and following count
- Account creation date

### Repository Statistics
- Total repositories (source and forked)
- Total stars received across all repositories
- Total forks and watchers
- Language distribution
- Most starred repositories
- Recently updated repositories

### Activity Statistics
- Recent public events
- Push, pull request, and issue events
- Activity breakdown by event type

## Examples

### Example 1: Generate a Markdown Report

```bash
python github_profile_report.py torvalds > torvalds_report.md
```

### Example 2: Analyze Multiple Users

```bash
for user in torvalds octocat github; do
    python github_profile_report.py $user --output "${user}_report.md"
done
```

### Example 3: JSON Output for Further Processing

```bash
python github_profile_report.py octocat --format json | jq '.profile.followers'
```

### Example 4: Using with Authentication

Create a `.env` file (not committed to git):
```
GITHUB_TOKEN=your_token_here
```

Then use in your script:
```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('GITHUB_TOKEN')
```

## Rate Limiting

GitHub API has rate limits:
- **Unauthenticated requests:** 60 requests per hour
- **Authenticated requests:** 5,000 requests per hour

Using a personal access token is highly recommended for regular use.

## API Permissions

This tool only requires read access to public information. No special permissions are needed for the token unless you want to access private repositories (not currently supported).

## Error Handling

The tool handles common errors gracefully:
- User not found (404)
- Rate limit exceeded (403)
- Network connectivity issues
- Invalid tokens

Error messages are printed to stderr, while the report is printed to stdout.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Issue: Rate limit exceeded

**Solution:** Use a GitHub personal access token with the `--token` flag.

### Issue: User not found

**Solution:** Verify the username is correct and the profile is public.

### Issue: Network errors

**Solution:** Check your internet connection and GitHub's status at https://www.githubstatus.com/

## Future Enhancements

Potential features for future versions:
- HTML report generation with charts
- Contribution calendar visualization
- Repository topic analysis
- Collaboration network analysis
- Historical data tracking
- PDF export
- Comparison between multiple users

## Requirements

- Python 3.6 or higher
- `requests` library
- `python-dotenv` library (for environment variable support)

## Author

Generated for comprehensive GitHub profile analysis.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

## 🎮 Gaming Stats Tracker

The `gaming_stats.py` script helps track and display gaming statistics.

### Usage

```bash
# Display current gaming stats
python gaming_stats.py

# The script will:
# - Show Xbox gamertag information
# - Display currently playing games
# - Generate markdown formatted stats
# - Save stats to JSON file
```

### Features

- Xbox Live profile integration
- Current games tracking
- Gaming profile statistics
- Markdown and JSON output
- Automated stats updates via GitHub Actions

---

## 📁 Repository Structure

```
MagnumG-365/
├── .github/
│   └── workflows/
│       └── update-stats.yml      # Automated stats updates
├── assets/
│   └── README.md                 # Asset guidelines
├── PROFILE_README.md             # Main profile README (gaming theme)
├── README.md                     # This file
├── github_profile_report.py      # GitHub profile report tool
├── gaming_stats.py               # Gaming stats tracker
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── .env.example                  # Environment variables template
```

---

## 🚀 Quick Start

### For GitHub Profile README

1. Fork or clone this repository
2. Customize `PROFILE_README.md` with your information
3. Add your gaming assets to `assets/` directory
4. Rename `PROFILE_README.md` to `README.md`
5. Create a repository matching your GitHub username
6. Push the customized README

### For Profile Report Tool

1. Clone the repository:
```bash
git clone https://github.com/MagnumG-365/MagnumG-365.git
cd MagnumG-365
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the profile report generator:
```bash
python github_profile_report.py <github-username>
```

### For Gaming Stats

1. Update your gaming information in `gaming_stats.py`
2. Run the stats tracker:
```bash
python gaming_stats.py
```

---

## 🎨 Customization

### Profile README Customization

Edit `PROFILE_README.md` to customize:
- Gamertag and Xbox profile links
- Current games and platforms
- Tech stack and skills
- Social media links
- Gaming statistics
- Personal motto and bio

### Assets

Add custom gaming-themed assets to the `assets/` directory:
- `gaming-header.gif` - Profile header
- `gaming-footer.gif` - Profile footer
- Custom badges and icons

See `assets/README.md` for detailed guidelines.

---

## 🔄 Automated Updates

The repository includes a GitHub Actions workflow (`.github/workflows/update-stats.yml`) that:
- Runs daily at midnight UTC
- Updates gaming statistics automatically
- Commits and pushes changes
- Can be triggered manually

---

## 🌟 Inspiration

This profile is inspired by:
- [Awesome GitHub Profile](https://zzetao.github.io/awesome-github-profile/)
- [GitHub Profile Documentation](https://docs.github.com/en/account-and-profile/get-started/profile)
- Xbox gaming community
- EternalNightmar gamertag

---

## 📝 License

This project is open source and available under the MIT License.

---

<div align="center">

**Made with ❤️ for the Gaming and Developer Community**

🎮 **EternalNightmar** | 💻 **Code by day, game by night** 🌙

</div>
