import os
import requests
import yaml
import subprocess

REMOTE_YAML_URL = "https://raw.githubusercontent.com/juspay/hyperswitch-helm/main/charts/incubator/hyperswitch-web/values.yaml"
VERSION_FILE = "hyperswitch-web/gitVersion"

def get_remote_git_version():
    print("Fetching remote values.yaml...")
    resp = requests.get(REMOTE_YAML_URL)
    resp.raise_for_status()
    data = yaml.safe_load(resp.text)
    return data["autoBuild"]["gitCloneParam"]["gitVersion"].strip()

def get_local_git_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def update_git_version(version):
    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        f.write(version + "\n")

def run_git(*args):
    try:
        return subprocess.run(["git"] + list(args), check=True, text=True,stderr=subprocess.STDOUT, stderr=subprocess.STDERR)
    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)
        exit(1)

def main():
    remote_version = get_remote_git_version()
    print(f"Remote gitVersion: {remote_version}")

    local_version = get_local_git_version()
    print(f"Local gitVersion: {local_version}")

    if local_version != remote_version:
        print("Updating gitVersion...")
        update_git_version(remote_version)
        run_git("config", "user.name", "github-actions[bot]")
        run_git("config", "user.email", "github-actions[bot]@users.noreply.github.com")
        run_git("add", VERSION_FILE)
        run_git("commit", "-m", f"Update gitVersion to {remote_version}")
        run_git("push")
    else:
        print("gitVersion is up to date. No changes made.")

if __name__ == "__main__":
    main()
