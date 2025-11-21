#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error


def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "GitHub-Activity-CLI"}  # GitHub نیاز دارد
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return json.loads(data)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("❌ Error: User not found!")
        elif e.code == 403:
            print("❌ Error: API rate limit exceeded! Try again later.")
        else:
            print(f"❌ HTTP Error: {e.code}")
        sys.exit(1)

    except urllib.error.URLError:
        print("❌ Network Error: Unable to connect to GitHub API.")
        sys.exit(1)


def parse_event(event):
    event_type = event.get("type")

    if event_type == "PushEvent":
        repo = event["repo"]["name"]
        commits = len(event["payload"]["commits"])
        return f"- Pushed {commits} commits to {repo}"

    elif event_type == "IssuesEvent":
        action = event["payload"]["action"]
        repo = event["repo"]["name"]
        return f"- {action.capitalize()} an issue in {repo}"

    elif event_type == "WatchEvent":
        repo = event["repo"]["name"]
        return f"- Starred {repo}"

    elif event_type == "ForkEvent":
        repo = event["repo"]["name"]
        return f"- Forked {repo}"

    elif event_type == "CreateEvent":
        repo = event["repo"]["name"]
        return f"- Created a new repo or branch in {repo}"

    else:
        # برای انواع خاص نیازی نیست همه رو هندل کنیم
        return f"- {event_type} on {event['repo']['name']}"


def main():
    # Check command arguments
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    print(f"\nFetching recent activity for: {username}\n")

    events = fetch_activity(username)

    if not events:
        print("No recent activity found.")
        return

    for event in events[:10]:  # فقط ۱۰ فعالیت آخر را نشان بده
        print(parse_event(event))


if __name__ == "__main__":
    main()
