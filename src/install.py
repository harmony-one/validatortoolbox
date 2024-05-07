import subprocess, os
from toolbox.config import config
from toolbox.library import loader_intro, print_stars

if __name__ == "__main__":
    loader_intro()
    subprocess.run("clear")
    print_stars()
    if os.path.isfile(config.user_home_dir + "/harmony.sh"):
        print(
            "* harmony.sh already exists in ~/\n*\n* This will exit, please change to your home directory and run ./harmony.sh to launch the toolbox.\n*\n* Run ./harmony.sh -h for our new help menu!\n*"
        )
    else:
        print("* Downloading harmony.sh to ~/")
        subprocess.run(
            "cd ~/ && wget -O harmony.sh https://raw.githubusercontent.com/easy-node-pro/harmony-toolbox/main/src/bin/harmony.sh && chmod +x harmony.sh && ./harmony.sh",
            shell=True,
        )
    print_stars()
