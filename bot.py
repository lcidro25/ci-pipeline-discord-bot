import discord
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
import json

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

intents = discord.Intents.default()
intents.message_content = True  # Important for reading message content!

client = discord.Client(intents=intents)

# Store bot start time for uptime
BOT_START_TIME = datetime.now()

def get_github_headers():
    return {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

def format_duration(seconds):
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if content.startswith("!hello"):
        await message.channel.send(f"Hello, {message.author.display_name} 👋")

    elif content.startswith("!help"):
        help_text = """**🤖 DevOps Bot Commands:**

**Pipeline Monitoring:**
- `!status` - Latest CI run status
- `!last-commit` - Most recent commit details
- `!failures` - Recent failed builds
- `!trigger-deploy` - Manually trigger deployment
- `!pipeline-history` - Last 5 pipeline runs
- `!branch-status <branch>` - Check specific branch status

**Repository Info:**
- `!repo-info` - Repository statistics
- `!open-prs` - List open pull requests
- `!recent-commits` - Recent commits
- `!branch-list` - List all branches

**Utility:**
- `!uptime` - Bot uptime
- `!ping` - Response time
- `!version` - Bot version

**Help:**
- `!help` - Show this message"""
        await message.channel.send(help_text)

    elif content.startswith("!status"):
        await handle_status_command(message)

    elif content.startswith("!last-commit"):
        await handle_last_commit_command(message)

    elif content.startswith("!failures"):
        await handle_failures_command(message)

    elif content.startswith("!trigger-deploy"):
        await handle_trigger_deploy_command(message)

    elif content.startswith("!pipeline-history"):
        await handle_pipeline_history_command(message)

    elif content.startswith("!branch-status"):
        await handle_branch_status_command(message)

    elif content.startswith("!repo-info"):
        await handle_repo_info_command(message)

    elif content.startswith("!open-prs"):
        await handle_open_prs_command(message)

    elif content.startswith("!recent-commits"):
        await handle_recent_commits_command(message)

    elif content.startswith("!branch-list"):
        await handle_branch_list_command(message)

    elif content.startswith("!uptime"):
        uptime = datetime.now() - BOT_START_TIME
        await message.channel.send(f"⏱️ Bot uptime: **{format_duration(int(uptime.total_seconds()))}**")

    elif content.startswith("!ping"):
        await message.channel.send("🏓 Pong!")

    elif content.startswith("!version"):
        await message.channel.send("🤖 **DevOps Bot v1.0.0**\nMonitoring GitHub pipelines and deployments")

async def handle_status_command(message):
    """Handle !status command"""
    headers = get_github_headers()
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?per_page=1"
    
    try:
        response = requests.get(repo_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["workflow_runs"]:
                run = data["workflow_runs"][0]
                status = run["conclusion"] or run["status"]
                html_url = run["html_url"]
                branch = run["head_branch"]
                commit_msg = run["head_commit"]["message"][:50] + "..." if len(run["head_commit"]["message"]) > 50 else run["head_commit"]["message"]
                
                status_emoji = "✅" if status == "success" else "❌" if status == "failure" else "🔄"
                await message.channel.send(f"{status_emoji} **Latest CI Run:** {status.upper()}\n🌿 **Branch:** {branch}\n📝 **Commit:** {commit_msg}\n🔗 {html_url}")
            else:
                await message.channel.send("📭 No workflow runs found.")
        else:
            await message.channel.send(f"❌ Failed to fetch CI status. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_last_commit_command(message):
    """Handle !last-commit command"""
    headers = get_github_headers()
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?per_page=1"
    
    try:
        response = requests.get(commits_url, headers=headers)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                commit = commits[0]
                sha = commit["sha"][:7]
                author = commit["commit"]["author"]["name"]
                message = commit["commit"]["message"]
                date = commit["commit"]["author"]["date"]
                
                await message.channel.send(f"📝 **Last Commit:**\n🔗 **SHA:** {sha}\n👤 **Author:** {author}\n📅 **Date:** {date}\n💬 **Message:** {message}")
            else:
                await message.channel.send("📭 No commits found.")
        else:
            await message.channel.send(f"❌ Failed to fetch commit. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_failures_command(message):
    """Handle !failures command"""
    headers = get_github_headers()
    runs_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?per_page=5&status=completed&conclusion=failure"
    
    try:
        response = requests.get(runs_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["workflow_runs"]:
                failures_text = "❌ **Recent Failures:**\n"
                for i, run in enumerate(data["workflow_runs"][:3], 1):
                    branch = run["head_branch"]
                    commit_msg = run["head_commit"]["message"][:40] + "..." if len(run["head_commit"]["message"]) > 40 else run["head_commit"]["message"]
                    created_at = run["created_at"]
                    html_url = run["html_url"]
                    failures_text += f"{i}. **{branch}** - {commit_msg}\n   📅 {created_at}\n   🔗 {html_url}\n\n"
                await message.channel.send(failures_text)
            else:
                await message.channel.send("✅ No recent failures found!")
        else:
            await message.channel.send(f"❌ Failed to fetch failures. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_trigger_deploy_command(message):
    """Handle !trigger-deploy command"""
    headers = get_github_headers()
    workflows_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows"
    
    try:
        # First, get available workflows
        response = requests.get(workflows_url, headers=headers)
        if response.status_code == 200:
            workflows = response.json()["workflows"]
            deploy_workflows = [w for w in workflows if "deploy" in w["name"].lower()]
            
            if deploy_workflows:
                workflow = deploy_workflows[0]  # Use first deploy workflow
                trigger_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{workflow['id']}/dispatches"
                
                # Trigger the workflow
                trigger_data = {"ref": "main"}  # Default to main branch
                trigger_response = requests.post(trigger_url, headers=headers, json=trigger_data)
                
                if trigger_response.status_code == 204:
                    await message.channel.send(f"🚀 **Deployment triggered!**\n📋 Workflow: {workflow['name']}\n🌿 Branch: main")
                else:
                    await message.channel.send(f"❌ Failed to trigger deployment. Error: {trigger_response.status_code}")
            else:
                await message.channel.send("❌ No deployment workflows found.")
        else:
            await message.channel.send(f"❌ Failed to fetch workflows. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_pipeline_history_command(message):
    """Handle !pipeline-history command"""
    headers = get_github_headers()
    runs_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?per_page=5"
    
    try:
        response = requests.get(runs_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["workflow_runs"]:
                history_text = "📊 **Pipeline History (Last 5):**\n"
                for run in data["workflow_runs"]:
                    status = run["conclusion"] or run["status"]
                    branch = run["head_branch"]
                    commit_msg = run["head_commit"]["message"][:30] + "..." if len(run["head_commit"]["message"]) > 30 else run["head_commit"]["message"]
                    
                    status_emoji = "✅" if status == "success" else "❌" if status == "failure" else "🔄"
                    history_text += f"{status_emoji} **{status.upper()}** - {branch} - {commit_msg}\n"
                
                await message.channel.send(history_text)
            else:
                await message.channel.send("📭 No pipeline history found.")
        else:
            await message.channel.send(f"❌ Failed to fetch pipeline history. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_branch_status_command(message):
    """Handle !branch-status command"""
    parts = message.content.split()
    if len(parts) < 2:
        await message.channel.send("❌ Please specify a branch: `!branch-status <branch-name>`")
        return
    
    branch = parts[1]
    headers = get_github_headers()
    runs_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?branch={branch}&per_page=1"
    
    try:
        response = requests.get(runs_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["workflow_runs"]:
                run = data["workflow_runs"][0]
                status = run["conclusion"] or run["status"]
                html_url = run["html_url"]
                
                status_emoji = "✅" if status == "success" else "❌" if status == "failure" else "🔄"
                await message.channel.send(f"{status_emoji} **Branch {branch}:** {status.upper()}\n🔗 {html_url}")
            else:
                await message.channel.send(f"📭 No runs found for branch: {branch}")
        else:
            await message.channel.send(f"❌ Failed to fetch branch status. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_repo_info_command(message):
    """Handle !repo-info command"""
    headers = get_github_headers()
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    
    try:
        response = requests.get(repo_url, headers=headers)
        if response.status_code == 200:
            repo = response.json()
            await message.channel.send(f"📊 **Repository Info:**\n⭐ **Stars:** {repo['stargazers_count']}\n🍴 **Forks:** {repo['forks_count']}\n👀 **Watchers:** {repo['watchers_count']}\n🌿 **Default Branch:** {repo['default_branch']}\n📅 **Created:** {repo['created_at']}")
        else:
            await message.channel.send(f"❌ Failed to fetch repo info. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_open_prs_command(message):
    """Handle !open-prs command"""
    headers = get_github_headers()
    prs_url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls?state=open&per_page=5"
    
    try:
        response = requests.get(prs_url, headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                prs_text = "🔀 **Open Pull Requests:**\n"
                for pr in prs:
                    prs_text += f"#{pr['number']} **{pr['title']}** by {pr['user']['login']}\n🔗 {pr['html_url']}\n\n"
                await message.channel.send(prs_text)
            else:
                await message.channel.send("✅ No open pull requests!")
        else:
            await message.channel.send(f"❌ Failed to fetch PRs. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_recent_commits_command(message):
    """Handle !recent-commits command"""
    headers = get_github_headers()
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?per_page=5"
    
    try:
        response = requests.get(commits_url, headers=headers)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                commits_text = "📝 **Recent Commits:**\n"
                for commit in commits:
                    sha = commit["sha"][:7]
                    author = commit["commit"]["author"]["name"]
                    message = commit["commit"]["message"][:50] + "..." if len(commit["commit"]["message"]) > 50 else commit["commit"]["message"]
                    commits_text += f"🔗 **{sha}** by {author}\n💬 {message}\n\n"
                await message.channel.send(commits_text)
            else:
                await message.channel.send("📭 No commits found.")
        else:
            await message.channel.send(f"❌ Failed to fetch commits. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_branch_list_command(message):
    """Handle !branch-list command"""
    headers = get_github_headers()
    branches_url = f"https://api.github.com/repos/{GITHUB_REPO}/branches?per_page=10"
    
    try:
        response = requests.get(branches_url, headers=headers)
        if response.status_code == 200:
            branches = response.json()
            if branches:
                branches_text = "🌿 **Branches:**\n"
                for branch in branches:
                    branches_text += f"• {branch['name']}\n"
                await message.channel.send(branches_text)
            else:
                await message.channel.send("📭 No branches found.")
        else:
            await message.channel.send(f"❌ Failed to fetch branches. Error: {response.status_code}")
    except Exception as e:
        await message.channel.send(f"❌ Error: {str(e)}")

client.run(DISCORD_BOT_TOKEN)
