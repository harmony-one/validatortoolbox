import subprocess
from pathlib import Path
from toolbox.config import config
from toolbox.library import loader_intro, print_stars

if __name__ == "__main__":
    loader_intro()
    subprocess.run(["clear"])
    print_stars()
    harmony_script_path = Path(config.user_home_dir) / "harmony.sh"
    if harmony_script_path.is_file():
        print("* harmony.sh already exists in ~/\n*\n* Launching the toolbox with help menu.")
        subprocess.run(["bash", "-x", str(harmony_script_path), "-h"])
    else:
        print("* Downloading harmony.sh to ~/")
        subprocess.run(["wget", "-O", str(harmony_script_path), "https://raw.githubusercontent.com/easy-node-pro/harmony-toolbox/main/src/bin/harmony.sh"])
        harmony_script_path.chmod(0o755)
        subprocess.run([str(harmony_script_path)])
    print_stars()
