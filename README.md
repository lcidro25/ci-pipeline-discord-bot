# 🤖 CI Pipeline Discord Bot

A powerful Discord bot designed to monitor GitHub repositories and provide real-time updates on CI/CD pipelines, commits, pull requests, and repository activity. Perfect for DevOps teams who want to stay informed about their projects directly in Discord.

## ✨ Features

### 🔄 Pipeline Monitoring
- **Real-time CI Status**: Get instant updates on the latest CI/CD pipeline runs
- **Build History**: View the last 5 pipeline runs with detailed status information
- **Failure Tracking**: Monitor recent failed builds and their causes
- **Branch-specific Status**: Check pipeline status for specific branches
- **Manual Deployment**: Trigger deployments directly from Discord

### 📊 Repository Intelligence
- **Commit Tracking**: Monitor recent commits with author and message details
- **Pull Request Management**: View open PRs and their status
- **Branch Overview**: List all repository branches
- **Repository Statistics**: Stars, forks, watchers, and creation date

### 🛠️ Utility Commands
- **Bot Uptime**: Monitor bot performance and availability
- **Response Time**: Check bot latency with ping command
- **Version Information**: Get bot version and capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- GitHub Personal Access Token
- A GitHub repository to monitor

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ci-pipeline-discord-bot.git
   cd ci-pipeline-discord-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   GITHUB_TOKEN=your_github_personal_access_token_here
   GITHUB_REPO=owner/repository-name
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## 🔧 Configuration

### Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Invite the bot to your server with appropriate permissions

### GitHub Token Setup
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Generate a new token with the following permissions:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
3. Copy the token and add it to your `.env` file

### Repository Configuration
Set the `GITHUB_REPO` environment variable to the repository you want to monitor:
```env
GITHUB_REPO=username/repository-name
```

## 📋 Available Commands

### Pipeline Monitoring
| Command | Description |
|---------|-------------|
| `!status` | Get the latest CI run status |
| `!last-commit` | Show details of the most recent commit |
| `!failures` | Display recent failed builds |
| `!trigger-deploy` | Manually trigger a deployment |
| `!pipeline-history` | Show the last 5 pipeline runs |
| `!branch-status <branch>` | Check status for a specific branch |

### Repository Information
| Command | Description |
|---------|-------------|
| `!repo-info` | Display repository statistics |
| `!open-prs` | List open pull requests |
| `!recent-commits` | Show recent commits |
| `!branch-list` | List all repository branches |

### Utility Commands
| Command | Description |
|---------|-------------|
| `!uptime` | Show bot uptime |
| `!ping` | Test bot response time |
| `!version` | Display bot version |
| `!help` | Show all available commands |

## 🏗️ Project Structure

```
ci-pipeline-discord-bot/
├── bot.py              # Main bot application
├── github_api.py       # GitHub API utilities
├── test_api.py         # API testing utilities
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── LICENSE            # Project license
```

## 🐛 Troubleshooting

### Common Issues

**Bot not responding to commands:**
- Check if the bot has the correct permissions in Discord
- Verify the bot token is correct
- Ensure the bot is online and connected

**GitHub API errors:**
- Verify your GitHub token has the correct permissions
- Check if the repository name is correct (format: `owner/repo`)
- Ensure the repository is accessible with your token

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8 or higher

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request


## 🙏 Acknowledgments

- Built with [discord.py](https://discordpy.readthedocs.io/)
- GitHub API integration using [requests](https://requests.readthedocs.io/)
- Environment management with [python-dotenv](https://github.com/theskumar/python-dotenv)

---

**Made with ❤️ for the DevOps community**
