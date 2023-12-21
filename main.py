import requests
from datetime import datetime
import matplotlib.pyplot as plt

def get_github_contributions(username, token):
    # Get the current year
    current_year = datetime.now().year

    # Set up the GitHub API endpoint
    endpoint = f'https://api.github.com/users/{username}/repos'

    # Set headers for the request
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the request to get user repositories
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        repositories = response.json()

        # Filter repositories based on contributions in the current year
        contributions_repos = [repo for repo in repositories if repo.get('pushed_at') and datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ").year == current_year]

        return contributions_repos
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def generate_pie_chart(languages):
    # Extract language data for the pie chart
    language_names = [language['name'] for language in languages]
    language_sizes = [language['size'] for language in languages]

    # Create a pie chart
    plt.pie(language_sizes, labels=language_names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Primary Language Distribution in GitHub Repositories (Current Year)')
    plt.show()

def main():
    # Replace 'YOUR_GITHUB_USERNAME' and 'YOUR_GITHUB_TOKEN' with your GitHub username and token
    github_username = 'YOUR_GITHUB_USERNAME'
    github_token = 'YOUR_GITHUB_TOKEN'

    # Get contributions for the current year
    contributions = get_github_contributions(github_username, github_token)

    if contributions:
        # Extract primary languages
        languages = [{'name': repo['language'], 'size': repo['size']} for repo in contributions if repo['language']]

        # Generate and display the pie chart
        generate_pie_chart(languages)

if __name__ == "__main__":
    main()
