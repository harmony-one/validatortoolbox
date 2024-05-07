import os
import sys
from os import environ
from toolbox.config import config
from toolbox.library import loader_intro, load_var_file, ask_yes_no, set_var, update_text_file, print_stars, process_command, clear_screen

def install_vstats(vstatsToken) -> None:
    # Check if it exists already
    if os.path.isdir(f"{config.user_home_dir}/harmony_node_stats"):
        question = ask_yes_no("* You already have vstats installed, would you like to update & reinstall vstats? (YES/NO)")
        if question is False:
            raise SystemExit(0)
        else:
            # Start install by stopping and wipe for re-install if yes
            process_command("sudo service harmony_node_stats stop")
            process_command(f"sudo rm -r {config.user_home_dir}/harmony_node_stats")

    # Install it bud, pull git repo
    os.chdir(f"{config.user_home_dir}")
    process_command("git clone https://github.com/FortuneV13/harmony_node_stats")
    os.chdir(f"{config.user_home_dir}/harmony_node_stats")
    # setup python stuff
    process_command("sudo apt install python3-pip -y")
    process_command("pip3 install -r requirements.txt")
    # customize config file
    process_command("cp config.example.py config.py")
    update_text_file(f"{config.user_home_dir}/harmony_node_stats/config.py", 'VSTATS_TOKEN=""', f'VSTATS_TOKEN="{vstatsToken}"')
    if os.path.isdir(f"{config.user_home_dir}/harmony"):
        update_text_file(f"{config.user_home_dir}/harmony_node_stats/config.py", '"harmony_folder":"/home/serviceharmony/harmony"', f'"harmony_folder":"{config.user_home_dir}/harmony"')
    else:
        if os.path.isfile(f"{config.user_home_dir}/harmony"):
            update_text_file(f"{config.user_home_dir}/harmony_node_stats/config.py", '"harmony_folder":"/home/serviceharmony/harmony"', f'"harmony_folder":"{config.user_home_dir}"')
    # Do service stuff here
    if config.active_user == 'root':
        process_command(
        f"sudo cp {config.toolbox_location}/src/bin/harmony_node_stats.service . && sed -i 's/home\/serviceharmony/{config.active_user}/g' 'harmony_node_stats.service' && sed -i 's/serviceharmony/{config.active_user}/g' 'harmony_node_stats.service' && sudo mv harmony_node_stats.service /etc/systemd/system/harmony_node_stats.service && sudo chmod a-x /etc/systemd/system/harmony_node_stats.service && sudo systemctl enable harmony_node_stats.service && sudo service harmony_node_stats start"
    )
    else:
        process_command(
        f"sudo cp {config.toolbox_location}/src/bin/harmony_node_stats.service . && sed -i 's/serviceharmony/{config.active_user}/g' 'harmony_node_stats.service' && sudo mv harmony_node_stats.service /etc/systemd/system/harmony_node_stats.service && sudo chmod a-x /etc/systemd/system/harmony_node_stats.service && sudo systemctl enable harmony_node_stats.service && sudo service harmony_node_stats start"
    )
    return


def get_token():
    if len(sys.argv) > 1:
            vstatsToken = sys.argv[1]
            set_var(config.dotenv_file, "VSTATSBOT_TOKEN", vstatsToken)
            load_var_file(config.dotenv_file)
    if environ.get("VSTATSBOT_TOKEN") is None:
        question = ask_yes_no(
            "* No token found, please run /token on vStats Bot to obtain your token. Would you like to enter one now? (YES/NO)"
        )
        if question:
            vstatsToken = input(
                "* Please input your vStats token here: "
            )
            set_var(config.dotenv_file, "VSTATSBOT_TOKEN", vstatsToken)
        else:
            raise SystemExit(0)
    else:
        vstatsToken = environ.get("VSTATSBOT_TOKEN")
    return vstatsToken


if __name__ == '__main__':
    clear_screen()
    loader_intro()
    # check if it exists, load anyway if it does
    if os.path.exists(config.dotenv_file) is None:
        # ask a bunch of questions to gather data since we don't have env
        vstatsToken = get_token()

    else:
        load_var_file(config.dotenv_file)
        # load env configuration
        vstatsToken = get_token()


    # install once we have the info to customize
    install_vstats(vstatsToken)

    # Goodbye!
    print_stars()
    print("\n*\n* Installer has finished, you should have a ping waiting on vStats if everything was input correctly\n* You can also run `sudo service harmony_node_stats status` to verify your service is online and running!\n*")
    print_stars()
