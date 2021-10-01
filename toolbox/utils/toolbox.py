import os
import shutil
import requests
import time
import subprocess
import dotenv
from utils.config import validatorToolbox
from os import environ
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple
from colorama import Fore, Back, Style
from pyhmy import blockchain, account
from requests.exceptions import HTTPError
from utils.shared import process_command, printStars, printStarsReset, printWhiteSpace, askYesNo, return_txt, installHarmonyApp, installHmyApp, getSignPercent, loadVarFile
from utils.allsysinfo import allSysInfo

def collectRewards(networkCall):
    os.system(
        f"{networkCall} staking collect-rewards --delegator-addr {environ.get('VALIDATOR_WALLET')} --gas-price 2 {environ.get('PASS_SWITCH')}"
    )
    return


def rewardsCollecter() -> None:
    printStars()
    print("* Harmony ONE Rewards Collection")
    printStars()
    question = askYesNo(
        f"*\n* For your validator wallet {environ.get('VALIDATOR_WALLET')}\n* Would you like to collect your rewards on the Harmony mainnet? (YES/NO) "
    )
    if question:
        collectRewards(validatorToolbox.main_net_call)
        printStars()
        print(
            Fore.GREEN + f"* mainnet rewards for {environ.get('VALIDATOR_WALLET')} have been collected." + Style.RESET_ALL
        )
        printStars()
    question = askYesNo(
        f"*\n* For your validator wallet {environ.get('VALIDATOR_WALLET')}\n* Would you like to collect your rewards on the Harmony testnet? (YES/NO) "
    )
    if question:
        collectRewards(validatorToolbox.test_net_call)
        print()
        printStars()
        print(
            Fore.YELLOW + f"* testnet rewards for {environ.get('VALIDATOR_WALLET')} have been collected." + Style.RESET_ALL
        )
        printStars()
        print()
        input("Press ENTER to return to the main menu.")
    return


def menuTopperRegular() -> None:
    current_epoch = blockchain.get_current_epoch(validatorToolbox.main_net_rpc)
    os.system("clear")
    # Print Menu
    print(Style.RESET_ALL)
    printStars()
    print(
        "* "
        + Fore.GREEN
        + "validator-toolbox for Harmony ONE Validators by Easy Node   v"
        + str(environ.get("EASY_VERSION"))
        + Style.RESET_ALL
        + "   https://easynode.one *"
    )
    printStars()
    print(
        "* Your validator wallet address is: "
        + Fore.RED
        + str(environ.get("VALIDATOR_WALLET"))
        + Style.RESET_ALL
    )
    print(
        "* Server Hostname & IP:             "
        + validatorToolbox.serverHostName
        + Style.RESET_ALL
        + " - "
        + Fore.YELLOW
        + validatorToolbox.ourExternalIPAddress
        + Style.RESET_ALL
    )
    harmonyServiceStatus()
    print(
        "* Epoch Signing Percentage:         "
        + Style.BRIGHT
        + Fore.GREEN
        + Back.BLUE
        + getSignPercent()
        + " %"
        + Style.RESET_ALL
    )
    print(
        "* Current disk space free: "
        + Fore.CYAN
        + f"{freeSpaceCheck(): >6}"
        + Style.RESET_ALL
        + "   Current Epoch: "
        + Fore.GREEN
        + str(current_epoch)
        + Style.RESET_ALL
    )
    printStarsReset()


def menuTopperFull() -> None:
    current_epoch = blockchain.get_current_epoch(validatorToolbox.main_net_rpc)
    os.system("clear")
    # Print Menu
    print(Style.RESET_ALL)
    printStars()
    print(
        "* "
        + Fore.GREEN
        + "validator-toolbox for Harmony ONE Validators by Easy Node   v"
        + str(environ.get("EASY_VERSION"))
        + Style.RESET_ALL
        + "   https://easynode.one *"
    )
    printStars()
    print(
        "* Server Hostname & IP:             "
        + validatorToolbox.serverHostName
        + Style.RESET_ALL
        + " - "
        + Fore.YELLOW
        + validatorToolbox.ourExternalIPAddress
        + Style.RESET_ALL
    )
    harmonyServiceStatus()
    print(
        "* Current disk space free: "
        + Fore.CYAN
        + f"{freeSpaceCheck(): >6}"
        + Style.RESET_ALL
        + "   Current Epoch: "
        + Fore.GREEN
        + str(current_epoch)
        + Style.RESET_ALL
    )
    printStarsReset()


def menuRegular() -> None:
    menuTopperRegular()
    print(Style.RESET_ALL)
    for x in return_txt(
        validatorToolbox.mainMenuRegular
    ):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)

def menuFull() -> None:
    menuTopperFull()
    print(Style.RESET_ALL)
    for x in return_txt(
        validatorToolbox.mainMenuFull
    ):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)


def getWalletJSON(wallet: str) -> str:
    testOrMain = environ.get("NETWORK")
    try:
            response = requests.get(f"https://api.stake.hmny.io/networks/{testOrMain}/validators/{wallet}")
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()
    #        print("Entire JSON response")
    #        print(jsonResponse)
    except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'* You have not created your validator yet, try again after you add one!\n* cd ~/harmony\n* ./hmy keys recover-from-mnemonic {validatorToolbox.activeUserName} {environ.get("PASS_SWITCH")}')
            input("Press ENTER to return to the main menu.")
            return
    except Exception as err:
            print(f'Other error occurred: {err}')
            input("Press ENTER to return to the main menu.")
            return
    return(jsonResponse)


def tmiServerInfo() -> None:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    jsonResponse = getWalletJSON(validatorWallet)
    for key, value in jsonResponse.items():
        print(key, ":", value)
    printStarsReset()
    input("Press ENTER to return to the main menu.")


def runFullNode() -> None:
    loadVarFile()
    menu_options = {
        # 0: finish_node,
        1: runStats,
        2: menuCheckBalance,
        3: comingSoon,
        4: comingSoon,
        5: comingSoon,
        6: comingSoon,
        7: comingSoon,
        8: menuServiceStopStart,
        9: menuServiceRestart,
        10: menuBinaryUpdates,
        11: hmyCLIUpgrade,
        12: menuUbuntuUpdates,
        13: serverDriveCheck,
        14: comingSoon,
        15: allSysInfo,
        999: menuRebootServer,
    }
    while True:
        menuFull()
        try:
            option = int(input("Enter your option: "))
        except ValueError:
                os.system("clear")
                printWhiteSpace()
                printStarsReset()
                print(
                    "* "
                    + Fore.RED
                    + "WARNING"
                    + Style.RESET_ALL
                    + ": Only numbers are possible, please try your selection on the main menu once again."
                )
                printStarsReset()
                printWhiteSpace()
                input("* Press ENTER to return to the main menu")
                runFullNode(environ.get("NODE_TYPE"))
        if option == 0:
            return finish_node()
        os.system("clear")
        menu_options[option]()


def comingSoon():
    os.system("clear")
    printWhiteSpace()
    printStars()
    print("* This option isn't available on your system, yet!")
    printStars()
    print("* Press enter to return to the main menu.")
    printStars()
    input()
    return


def runRegularNode() -> None:
    loadVarFile()
    menu_options = {
        # 0: finish_node, 
        1: runStats,
        2: menuActiveBLS,
        3: menuCheckBalance,
        4: rewardsCollecter,
        5: comingSoon,
        6: comingSoon,
        7: comingSoon,
        8: menuServiceStopStart,
        9: menuServiceRestart,
        10: menuBinaryUpdates,
        11: hmyCLIUpgrade,
        12: menuUbuntuUpdates,
        13: serverDriveCheck,
        14: tmiServerInfo,
        15: allSysInfo,
        999: menuRebootServer,
    }
    while True:
        menuRegular()
        try:
            option = int(input("Enter your option: "))
        except ValueError:
                os.system("clear")
                printWhiteSpace()
                printStarsReset()
                print(
                    "* "
                    + Fore.RED
                    + "WARNING"
                    + Style.RESET_ALL
                    + ": Only numbers are possible, please try your selection on the main menu once again."
                )
                printStarsReset()
                printWhiteSpace()
                input("* Press ENTER to return to the main menu")
                runRegularNode()
        if option == 0:
            return finish_node()
        os.system("clear")
        menu_options[option]()


def osUpgrades() -> None:
    printStars()
    upgrades = (
        "sudo apt update",
        "sudo apt upgrade -y",
        "sudo apt dist-upgrade -y",
        "sudo apt autoremove -y",
    )
    for x in upgrades:
        process_command(x)
    printStars()


def harmonyServiceStatus() -> None:
    # Why use os.system here?
    status = subprocess.call(["systemctl", "is-active", "--quiet", "harmony"])
    if status == 0:
        print(
            "* Harmony Service is:               "
            + Fore.BLACK
            + Back.GREEN
            + "   Online  "
            + Style.RESET_ALL
        )
        return
    else:
        print(
            "* Harmony Service is:               "
            + Fore.WHITE
            + Back.RED
            + "  *** Offline *** "
            + Style.RESET_ALL
        )
        return


def diskFreeSpace(mountPoint: str) -> str:
    total, used, free = shutil.disk_usage(mountPoint)
    free = str(convertedUnit(free))
    return free


def freeSpaceCheck() -> str:
    ourDiskMount = get_mount_point(validatorToolbox.harmonyDirPath)
    total, used, free = shutil.disk_usage(ourDiskMount)
    free = diskFreeSpace(ourDiskMount)
    return free


def serverDriveCheck() -> None:
    if environ.get("MOUNT_POINT") is not None:
        ourDiskMount = environ.get("MOUNT_POINT")
    else:
        dotenv.set_key(validatorToolbox.dotenv_file, "MOUNT_POINT", validatorToolbox.harmonyDirPath)
        load_dotenv(validatorToolbox.dotenv_file)
        ourDiskMount = environ.get("MOUNT_POINT")
    printStarsReset()
    print("Here are all of your mount points: ")
    for part in disk_partitions():
        print(part)
    printStars()
    total, used, free = shutil.disk_usage(ourDiskMount)
    total = str(convertedUnit(total))
    used = str(convertedUnit(used))
    print(
        "Disk: "
        + str(ourDiskMount)
        + "\n"
        + freeSpaceCheck()
        + " Free\n"
        + used
        + " Used\n"
        + total
        + " Total"
    )
    printStars()
    input("Disk check complete, press ENTER to return to the main menu. ")


def disk_partitions(all=False):
    disk_ntuple = namedtuple("partition", "device mountpoint fstype")
    # Return all mountd partitions as a nameduple.
    # If all == False return phyisical partitions only.
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())
    retlist = []
    f = open("/etc/mtab", "r")
    for line in f:
        if not all and line.startswith("none"):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == "none":
            device = ""
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist


def get_mount_point(pathname):
    """
    Get the mount point of the filesystem containing pathname
    """
    pathname = os.path.normcase(os.path.realpath(pathname))
    parent_device = path_device = os.stat(pathname).st_dev
    while parent_device == path_device:
        mount_point = pathname
        pathname = os.path.dirname(pathname)
        if pathname == mount_point:
            break
        parent_device = os.stat(pathname).st_dev
    return mount_point


def convertedUnit(n):
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def serviceMenuOption() -> None:
    status = os.system("systemctl is-active --quiet harmony")
    if status == 0:
        print(
            "*  [8] "
            + Fore.RED
            + "Stop Harmony Serivce      "
            + Fore.WHITE
            + "- "
            + Fore.YELLOW
            + Back.RED
            + "WARNING: You will miss blocks while stopped!   "
            + Style.RESET_ALL
        )
        print(
            "*  [9] Restart Harmony Service   - "
            + Back.RED
            + Fore.YELLOW
            + "WARNING: You will miss blocks during a restart!"
            + Style.RESET_ALL
        )
    else:
        print("*  [8] " + Fore.GREEN + "Start Harmony Service" + Style.RESET_ALL)


def makeBackupDir() -> str:
    if not os.path.isdir(f"{validatorToolbox.harmonyDirPath}/harmony_backup"):
        printStarsReset()
        print("Backup directory not found, creating folder")
        os.system(f"mkdir -p {validatorToolbox.harmonyDirPath}/harmony_backup")
        return
    return


def hmyCLIUpgrade():
    printStarsReset()
    question = askYesNo(
        "Are you sure you would like to proceed with updating the Harmony CLI file?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.chdir(f"{validatorToolbox.harmonyDirPath}")
        makeBackupDir()
        os.system(f"cp {validatorToolbox.hmyAppPath} {validatorToolbox.harmonyDirPath}/harmony_backup")
        printStars()
        installHmyApp(validatorToolbox.harmonyDirPath)
        printStars()
        print("Harmony cli has been updated to: ")
        os.system(f"{validatorToolbox.hmyAppPath} version")
        printStars()
        input("Update completed, press ENTER to return to the main menu. ")
        return


def upgradeHarmonyApp(testOrMain):
    os.chdir(f"{validatorToolbox.harmonyDirPath}")
    printStarsReset()
    print("Currently installed version: ")
    os.system("./harmony -V")
    makeBackupDir()
    os.system(f"cp {validatorToolbox.harmonyDirPath}/harmony {validatorToolbox.harmonyDirPath}/harmony_backup")
    printStars()
    print("Downloading current harmony binary file from harmony.one: ")
    printStars()
    installHarmonyApp(validatorToolbox.harmonyDirPath)
    printStars()
    print("Updated version: ")
    os.system("./harmony -V")
    os.system("sudo service harmony restart")
    printStars()
    print(
        "Harmony Service is restarting, wait 10 seconds and we'll check your stats..."
    )
    time.sleep(10)
    return


def runStats() -> str:
    timeNow = datetime.now()
    ourShard = environ.get("SHARD")
    networkNumCall = environ.get("NETWORK_S_CALL")
    printStars()
    print(
        f"* Current Date & Time: {timeNow}\n* Current Status of our server {validatorToolbox.serverHostName} currently on Shard {environ.get('SHARD')}:\n"
    )
    os.system(
        f"{validatorToolbox.hmyAppPath} blockchain latest-headers | grep epoch && {validatorToolbox.hmyAppPath} blockchain latest-headers | grep viewID && {validatorToolbox.hmyAppPath} blockchain latest-headers | grep shardID"
    )
    print(
        f"\n* Current Status of the Harmony Blockchain Shard {environ.get('SHARD')}:\n"
    )
    os.system(
        f"{networkNumCall} blockchain latest-headers | grep epoch && {networkNumCall} blockchain latest-headers | grep viewID && {networkNumCall} blockchain latest-headers | grep shardID"
    )
    shardStats(ourShard)
    input("Validator stats completed, press ENTER to return to the main menu. ")


def getDBSize(ourShard) -> str:
    harmonyDBSize = subprocess.getoutput(f"du -h {validatorToolbox.harmonyDirPath}/harmony_db_{ourShard}")
    harmonyDBSize = harmonyDBSize.rstrip('\t')
    return harmonyDBSize[:-41]


def shardStats(ourShard) -> str:
    ourUptime = subprocess.getoutput("uptime")
    dbZeroSize = getDBSize('0')
    if ourShard == "0":
        os.system(
            f"echo '\n* Uptime :: {ourUptime}\n\n Harmony DB 0 Size  ::  {dbZeroSize}\n'"
        )
        os.system(
            f"{validatorToolbox.harmonyAppPath} -V"
        )
    else:
        os.system(
            f"echo '\n* Uptime :: {ourUptime}\n\n Harmony DB 0 Size  ::  {dbZeroSize}\n Harmony DB {ourShard} Size  ::   {getDBSize(str(ourShard))}\n'"
        )
        os.system(
            f"{validatorToolbox.harmonyAppPath} -V"
        )
    printStars()
    return


def menuBinaryUpdates():
    testOrMain = environ.get("NETWORK")
    printStarsReset()
    question = askYesNo(
        Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS WHILE YOU UPGRADE THE HARMONY SERVICE.\n\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        upgradeHarmonyApp(testOrMain)
        runStats()


def menuUbuntuUpdates() -> str:
    printStarsReset()
    question = askYesNo(
        Fore.WHITE
        + "Are you sure you would like to proceed with Linux apt Upgrades?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        osUpgrades()
        print()
        input("OS Updates completed, press ENTER to return to the main menu. ")


def menuRebootServer() -> str:
    printStarsReset()
    question = askYesNo(
        Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS WHILE YOU REBOOT YOUR ENTIRE SERVER.\n\n"
        + "Reconnect after a few moments & Run the Validator Toolbox Menu again with: python3 ~/validator-toolbox/toolbox/start.py\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed with rebooting your server?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.system("sudo reboot")
    else:
        print("Invalid option.")


def menuServiceStopStart() -> str:
    status = os.system("systemctl is-active --quiet harmony")
    if status != 0:
        os.system("sudo service harmony start")
        print()
        print("Harmony Service Has Been Started.")
        print()
        input("Press ENTER to return to the main menu.")
    else:
        question = askYesNo(
            "*********\n"
            + Fore.RED
            + "WARNING: YOU WILL MISS BLOCKS IF YOU STOP THE HARMONY SERVICE.\n\n"
            + Fore.WHITE
            + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
        )
        if question:
            os.system("sudo service harmony stop")
            print()
            print(
                "Harmony Service Has Been Stopped. "
                + Fore.RED
                + "YOU ARE MISSING BLOCKS ON THIS NODE."
                + Style.RESET_ALL
            )
            print()
            input("Press ENTER to return to the main menu.")


def menuServiceRestart() -> str:
    question = askYesNo(
        "*********\n"
        + Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS UNTIL RESTART IS COMPLETED & SYNC CATCHES UP!\n\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.system("sudo service harmony restart")
        print()
        print("* The Harmony Service Has Been Restarted")
        input("* Press ENTER to return to the main menu.")


def menuActiveBLS() -> str:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    jsonResponse = getWalletJSON(validatorWallet)
    printStarsReset()
    print("* This is a list of your BLS Keys that are active for the next election.")
    for i, x in enumerate(jsonResponse["bls-public-keys"]):
        print(f"BLS Key {i+1} {x}")
    printStars()
    input("Press ENTER to return to the main menu.")


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def menuCheckBalance() -> None:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    if environ.get("NODE_TYPE") == "regular":
        printStarsReset()
        print("* Calling mainnet and testnet for balances...")
        printStars()
        total_balance = account.get_total_balance(validatorWallet, endpoint=validatorToolbox.main_net_rpc)
        total_balance_test = account.get_total_balance(validatorWallet, endpoint=validatorToolbox.test_net_rpc)
        print(f"* Your Validator Wallet Balance on Mainnet is: {total_balance*0.000000000000000001} Harmony ONE Coins")
        print(f"* Your Validator Wallet Balance on Testnet is: {total_balance_test*0.000000000000000001} Harmony ONE Test Coins")
        printStars()
        i = 0
        while i < 1:
            question = askYesNo(
                "* Would you like to check another Harmony ONE Address? (YES/NO) "
            )
            if question:
                balanceCheckAny()
            else:
                i = 1
        return
    else:
        i = 0
        while i < 1:
            question = askYesNo(
                "* Would you like to check a Harmony ONE Address? (YES/NO) "
            )
            if question:
                balanceCheckAny()
            else:
                i = 1
    return


def balanceCheckAny():
    printStarsReset()
    checkWallet = input(
        "* Type the address of the Harmony ONE Wallet you would like to check.\n"
        + "* Only one wallets will work, no 0x addresses : "
    )
    print("* Calling mainnet and testnet for balances...")
    printStarsReset()
    total_balance = account.get_total_balance(checkWallet, endpoint=validatorToolbox.main_net_rpc)
    total_balance_test = account.get_total_balance(checkWallet, endpoint=validatorToolbox.test_net_rpc)
    print(f"* The Wallet Balance is: {total_balance*0.000000000000000001} Harmony ONE Coins")
    print(f"* Your Validator Wallet Balance on Testnet is: {total_balance_test*0.000000000000000001} Harmony ONE Test Coins")
    printStars()
    input("Press ENTER to continue.")


def finish_node():
    printStars()
    print("Don't forget to check for some BINGOs with:")
    print()
    print(
        f"tail -f /home/{validatorToolbox.activeUserName}/harmony/latest/zerolog-harmony.log | grep BINGO"
    )
    print()
    print("Thanks for using Easy Node - EZ Mode! Goodbye.")
    printStars()
    raise SystemExit(0)