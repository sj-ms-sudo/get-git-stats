# GitHub Stats CLI Tool

A command-line tool to fetch and visualize GitHub user profile stats.

## Features
- Get repo count, followers, following, and languages used.
- Optionally visualize data in a bar & pie chart.
- Secure — uses environment variable for GitHub token.

## Usage

```bash
export GITHUB_TOKEN=your_token
python github_stats.py -u <username>
python github_stats.py -u <username> -g  # with graphs
