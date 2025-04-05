import os   # Library to use system commands
import sys  # Library to handle command-line arguments

# SUBSTITUTE YOUR TOKENS, REPOSITORIES AND USERNAMES IN THE LIST BELOW, MAKE SURE TO MATCH THE INFORMATION
# FOR THE SAME REPO IN THE SAME POSITION OF THE LIST

# Tokens and the name of their corresponding repositories
tokens = (
    "your-token-here",
    "other-token-here"
    )
tokenNames = (
    "your-repo-name-here",
    "other-repo-name-here"
    )
users = (
    "your-username-here",
    "other-username-here"
    )

# Function to check that the selected repo is correct
def repoCheck():
    repo = int(input(f"Select a repository (1 - {len(tokens)})\n>> "))
    while(repo < 1 or repo > len(tokens)):
        repo = int(input("Please select a valid repo\n>> "))
    return repo

# Function to copy the token to the clipboard
def copyToken(repo):
    token = tokens[repo - 1]  # Get the token for the selected repo
    try:
        # Use xclip to copy the token to the clipboard
        os.system(f"echo {token} | xclip -sel clip -r")
        print("\033[92mToken copied to clipboard!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: Unable to copy token to clipboard: {e}\033[0m")
        
# Function to copy the user to the clipboard
def copyUser(repo):
    user = users[repo - 1]  # Get the user for the selected repo
    try:
        # Use xclip to copy the user to the clipboard
        os.system(f"echo {user} | xclip -sel clip -r")
        print("\033[92mUser copied to clipboard!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: Unable to copy user to clipboard: {e}\033[0m")

# Function to copy user \n token
def copyUserToken(repo):
    content = users[repo - 1]
    content += "\n"
    content += tokens[repo - 1]
    try:
        # Use xclip to copy the token to the clipboard
        os.system(f"echo {content} | xclip -sel clip -r")
        print("\033[92mCopied to clipboard!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: Unable to copy to clipboard: {e}\033[0m")

# Function to execute the corresponding git pull
def makePull(repo):
    token = tokens[repo - 1]  # Get the token for the selected repo
    username = users[repo - 1]  # Get the username for the selected repo
    repo_name = tokenNames[repo - 1]  # Get the repository name

    # Construct the remote URL with the token
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

    try:
        # Run git pull command
        os.system(f"git pull {remote_url}")  # Pull using the token-authenticated URL
        print("\033[92mPull complete!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: An error occurred during the git pull: {e}\033[0m")

# Function to execute the corresponding git push
def makePush(repo, com):
    token = tokens[repo - 1]  # Get the token for the selected repo
    username = users[repo - 1]  # Get the username for the selected repo
    repo_name = tokenNames[repo - 1]  # Get the repository name

    # Construct the remote URL with the token
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

    try:
        # Run git commands
        os.system("git add .")
        os.system(f'git commit -m "{com}"')  # Commit with the user-provided message
        os.system(f"git push {remote_url}")  # Push using the token-authenticated URL
        print("\033[92mPush complete!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: An error occurred during the git push: {e}\033[0m")
        
# Function to execute the corresponding git push
def makePushNoAdd(repo, com):
    token = tokens[repo - 1]  # Get the token for the selected repo
    username = users[repo - 1]  # Get the username for the selected repo
    repo_name = tokenNames[repo - 1]  # Get the repository name

    # Construct the remote URL with the token
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

    try:
        # Run git commands
        os.system(f'git commit -m "{com}"')  # Commit with the user-provided message
        os.system(f"git push {remote_url}")  # Push using the token-authenticated URL
        print("\033[92mPush complete!\033[0m")
    except Exception as e:
        print(f"\033[91mERROR: An error occurred during the git push: {e}\033[0m")

# Check if the program can be used
if(len(tokens) < 1 or len(tokenNames) != len(tokens) or len(users) != len(tokens)):
    print("\033[91mERROR: Check that the tokens, repos and users are correctly declared!\033[0m")
    exit(1) # Error code that indicates that tokens are not well-defined

# Ensure the correct usage of the script
if len(sys.argv) < 2 or sys.argv[1].lower() not in ["push", "pull", "token", "pushnoadd", "user", "usertoken"]:
    print("\033[91mERROR: Usage: python3 gitmanager.py <push/pull/token/pushnoadd/user/usertoken>\033[0m")
    exit(1)

operation = sys.argv[1].lower()

# Program interface
print("=============== [GITMANAGER.PY] ===============")
print("Available repositories:")
for i in range(len(tokens)):
    print(f"{i + 1}. {tokenNames[i]}")
    if(i + 1 >= len(tokens)):
        print("")

# Variable declaration
repo = repoCheck()

if operation == "pull":
    makePull(repo)
elif operation == "push":
    com = input("Enter a commit message\n>> ")
    makePush(repo, com)
elif operation == "pushnoadd":
    com = input("Enter a commit message\n>> ")
    makePushNoAdd(repo, com)
elif operation == "token":
    copyToken(repo)
elif operation == "user":
    copyUser(repo)
elif operation == "usertoken":
    copyUserToken(repo)
