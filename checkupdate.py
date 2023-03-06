import requests

repo_owner = "samchen023"
repo_name = "control-center"


response = requests.get(
    f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest")


if response.status_code == 200:
    release_data = response.json()
    if "name" in release_data:
        latest_release_name = release_data["name"]
    else:
        latest_release_name = release_data["tag_name"]

    latest_release_tag_name = release_data["tag_name"]

    print(
        f"Latest release of {repo_name} is {latest_release_name} ({latest_release_tag_name})")
else:
    print("Failed to get latest release")
