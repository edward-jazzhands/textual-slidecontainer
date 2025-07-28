# tag_release.py
import subprocess
import tomllib # Or `tomli` for Python < 3.11

# 1. Read the version from the single source of truth
with open("pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)
    version = pyproject_data["project"]["version"]

# 2. Construct the tag and the git command
tag = f"v{version}"
print(f"Found version {version}. Creating tag: {tag}")

# 3. Run the git command
try:
    subprocess.run(["git", "tag", tag], check=True)
    print(f"Successfully created tag '{tag}'.")
except subprocess.CalledProcessError:
    print(f"Error: Could not create tag. Does the tag '{tag}' already exist?")
except FileNotFoundError:
    print("Error: 'git' command not found. Is Git installed and in your PATH?")