import requests

# Replace these values with the values for the app you want to check
repo_owner = "samchen023"
repo_name = "control-center"

# Make a request to the GitHub API to get the latest release
response = requests.get(
    f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest")

# Check the status code of the response to see if the request was successful
if response.status_code == 200:
    # Get the name of the latest release
    release_data = response.json()
    if "name" in release_data:
        latest_release_name = release_data["name"]
    else:
        latest_release_name = release_data["tag_name"]

    # Get the tag name of the latest release
    latest_release_tag_name = release_data["tag_name"]

    # Print the name and tag name of the latest release
    print(
        f"Latest release of {repo_name} is {latest_release_name} ({latest_release_tag_name})")
else:
    print("Failed to get latest release")
