[![Codacy Badge](https://app.codacy.com/project/badge/Grade/215c4479f0304b40a535f7e84ce75f55)](https://www.codacy.com/gh/easy-node-one/validatortoolbox/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=easy-node-one/validatortoolbox&amp;utm_campaign=Badge_Grade)
[![Telegram Badge](https://img.shields.io/badge/chat-telegram-blue?logo=telegram)](https://t.me/easynodesupport)
[![Discord Badge](https://img.shields.io/badge/chat-discord-purple?logo=discord)](https://discord.gg/babnYCEZ7Q)
[![Stake Now Badge](https://img.shields.io/badge/stake-harmony-brightgreen)](https://bit.ly/easynode)


# Easy Node - Validator Toolbox
by [EasyNode.ONE](http://EasyNode.ONE "EasyNode.ONE")

This repository provides two functions in one application:
-   Harmony Validator Menu Driven Installer
-   Harmony Validator Management Interface Menu

[![Easy Node - Harmony Validator Operations Toolbox](http://img.youtube.com/vi/mtlgZQc7BjM/0.jpg)](https://www.youtube.com/watch?v=mtlgZQc7BjM "Easy Node - Harmony Validator Operations Toolbox")

## Quickstart Guide
### Pre-Installation Requirements:
Digital Ocean users can use [this pre-installation quick guide](https://validator-toolbox-guide.easynode.one/full-manual/pre-installation-information/pre-installation/digital-ocean-validator-node-setup "this pre-installation quick guide").

**Operating System**
-   Ubuntu 20.04LTS - The suggested operating system from harmony
**Account**
-   Be logged into any user account, we strongly suggest not using root.
	-   Account must have sudoless root access (if not using the root account)
	-   If you skip this step, you will be prompted for your password during rclone setup but it will be hidden in the menu. If it pauses there type your user account password.
**Storage Volume**
	-   Mount your volume to any folder inside of /mnt and we'll detect a single mount point inside of that folder, install harmony in /mnt/yourfolder/harmony and symlink that folder to ~/harmony

### Installation
**After** completing the Pre-Instlalation Requirements pull the repository into your home directory.
```bash
cd ~/
git clone https://github.com/easy-node-one/validatortoolbox.git
```
Install requirements.
```bash
cd validatortoolbox
sudo apt-get install dnsutils python3-pip python3-dotenv -y
pip3 install -r requirements.txt
```
Run the installer from anywhere. You'll be presented with our menu to grab configuration details.
```bash
python3 ~/validatortoolbox/toolbox/start.py
```

## Full Installation Guide & Documentation
See the gitbook for validatortoolbox to [install our software here](https://validator-toolbox-guide.easynode.one/ "validatortoolbox gitbook guide").
