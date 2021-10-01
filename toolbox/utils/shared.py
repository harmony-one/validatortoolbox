import os
import dotenv
import subprocess
import os
import subprocess
import requests
from utils.config import validatorToolbox
from os import environ
from dotenv import load_dotenv
from simple_term_menu import TerminalMenu
from colorama import Style


def loaderIntro():
    printStars()
    print(" ____ ____ ____ ____ _________ ____ ____ ____ ____           ")
    print("||E |||a |||s |||y |||       |||N |||o |||d |||e ||          ")
    print("||__|||__|||__|||__|||_______|||__|||__|||__|||__||          ")
    print("|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|          ")
    print(" ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ")
    print("||H |||a |||r |||m |||o |||n |||y |||       |||O |||N |||E ||")
    print("||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__||")
    print("|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|")
    print(" ____ ____ ____ ____ ____ ____ ____ ____ ____                ")
    print("||v |||a |||l |||i |||d |||a |||t |||o |||r ||               ")
    print("||__|||__|||__|||__|||__|||__|||__|||__|||__||               ")
    print("|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|               ")
    print(" ____ ____ ____ ____ ____ ____ ____                          ")
    print("||T |||o |||o |||l |||b |||o |||x ||                         ")
    print("||__|||__|||__|||__|||__|||__|||__||                         ")
    print("|/__\|/__\|/__\|/__\|/__\|/__\|/__\|                         ")
    printStars()


def installHmyApp(harmonyDirPath):
    os.chdir(f"{harmonyDirPath}")
    os.system("curl -LO https://harmony.one/hmycli && mv hmycli hmy && chmod +x hmy")
    printStars()
    print("* hmy application installed.")


def updateTextFile(fileName):
    f = open(fileName,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace("MaxKeys = 10","MaxKeys = 30")

    f = open(fileName,'w')
    f.write(newdata)
    f.close()
    return


def installHarmonyApp(harmonyDirPath):
    testOrMain = environ.get("NETWORK")
    os.chdir(f"{harmonyDirPath}")
    if testOrMain == "testnet":
        os.system("curl -LO https://harmony.one/binary_testnet && mv binary_testnet harmony && chmod +x harmony")
        os.system("./harmony config dump --network testnet harmony.conf")
        updateTextFile(validatorToolbox.harmonyConfPath)
    if testOrMain == "mainnet":
        os.system("curl -LO https://harmony.one/binary && mv binary harmony && chmod +x harmony")
        os.system("./harmony config dump harmony.conf")
        updateTextFile(validatorToolbox.harmonyConfPath)
    # when we setup rasppi as an option, this is the install command for harmony
    if environ.get("ARC") == "arm64":
        if environ.get("NETWORK") == "testnet":
            # no current testnet know for arm64, break for now
            print("No known testnet for R Pi at this time, try mainnet")
            raise SystemExit(0)
        else:
            os.system("curl -LO https://harmony.one/binary-arm64 && mv binary-arm64 harmony && chmod +x harmony")
            os.system("./harmony config dump harmony.conf")
    printStars()
    print(f"* Harmony {testOrMain} application installed & ~/harmony/harmony.conf created.")


def setWalletEnv(dotenv_file):
    if environ.get("VALIDATOR_WALLET") is None:
        output = subprocess.getoutput(f"{validatorToolbox.hmyAppPath} keys list | grep {validatorToolbox.activeUserName}")
        outputStripped = output.lstrip(validatorToolbox.activeUserName)
        outputStripped = outputStripped.strip()
        dotenv.set_key(dotenv_file, "VALIDATOR_WALLET", outputStripped)
        return outputStripped
    else:
        loadVarFile()
        validatorWallet = environ.get("VALIDATOR_WALLET")
        return validatorWallet
    

def process_command(command: str) -> None:
    process = subprocess.Popen(command, shell=True)
    output, error = process.communicate()


def printStars() -> str:
    print(
        "*********************************************************************************************"
    )
    return


def printStarsReset() -> str:
    print(
        "*********************************************************************************************"
        + Style.RESET_ALL
    )
    return


def printWhiteSpace() -> str:
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()


def askYesNo(question: str) -> bool:
    YesNoAnswer = ""
    while not YesNoAnswer.startswith(("Y", "N")):
        YesNoAnswer = input(f"{question}: ").upper()
    if YesNoAnswer.startswith("Y"):
        return True
    return False


def save_text(fn: str, to_write: str) -> bool:
    try:
        with open(fn, "w") as f:
            f.write(to_write)
            return True
    except Exception as e:
        print(f"Error writing file  ::  {e}")
        return False


def return_txt(fn: str) -> list:
    """
    Opens a file and returns the whole file as a list
    Args:
        fn (str): File name to open
    Returns:
        list: return whole file as a list
    """
    try:
        with open(fn, "r") as f:
            return f.readlines()
    except FileNotFoundError as e:
        print(f"File not Found  ::  {e}")
        return []


def loadVarFile():
    if os.path.exists(validatorToolbox.dotenv_file) == True:
        load_dotenv(validatorToolbox.dotenv_file)
        return


def firstRunMenu():
    os.system("clear")
    print("*********************************************************************************************")
    print("* First run detected!                                                                       *")
    print("*********************************************************************************************")
    print("* [0] = Start Harmony Installer App - For brand new servers needed validator software       *")
    print("* [1] = Load Validator Toolbox Menu App - Our simple management server for installed Nodes  *")
    print("*********************************************************************************************")
    menuOptions = ["[0] - Start Installer Application", "[1] - Load Validator Toolbox Menu", ]
    terminal_menu = TerminalMenu(menuOptions, title="* Is this a new server or an already existing harmony node?")
    setupStatus = str(terminal_menu.show())
    dotenv.unset_key(validatorToolbox.dotenv_file, "SETUP_STATUS", setupStatus)
    dotenv.set_key(validatorToolbox.dotenv_file, "SETUP_STATUS", setupStatus)
    return



def getShardMenu(dotenv_file) -> None:
    if environ.get("SHARD") is None:
        os.system("clear")
        print("*********************************************************************************************")
        print("* First Boot - Gathering more information about your server                                 *")
        print("*********************************************************************************************")
        print("* Which shard do you want this node run on?                                                 *")
        print("*********************************************************************************************")
        menuOptions = ["[0] - Shard 0", "[1] - Shard 1", "[2] - Shard 2", "[3] - Shard 3", ]
        terminal_menu = TerminalMenu(menuOptions, title="* Which Shard will this node operate on? ")
        ourShard = str(terminal_menu.show())
        dotenv.set_key(dotenv_file, "SHARD", ourShard)
        return ourShard


def getNodeType(dotenv_file) -> None:
    if not os.path.exists(validatorToolbox.hmyWalletStorePath):
        if environ.get("NODE_TYPE") == None:
            os.system("clear")
            print("*********************************************************************************************")
            print("* Which type of node would you like to run on this server?                                  *")
            print("*********************************************************************************************")
            print("* [0] - Standard w/ Wallet - Harmony Validator Signing Node with Wallet                     *")
            print("* [1] - Standard No Wallet - Harmony Validator Signing Node no Wallet                       *")
            print("* [2] - Full Node Dev/RPC - Non Validating Harmony Node                                     *")
            print("*********************************************************************************************")
            menuOptions = ["[0] Signing Node w/ Wallet", "[1] Signing Node No Wallet", "[2] Full Node Non Validating Dev/RPC", ]
            terminal_menu = TerminalMenu(menuOptions, title="Regular or Full Node Server")
            results = terminal_menu.show()
            if results == 0:
                dotenv.set_key(dotenv_file, "NODE_TYPE", "regular")
                dotenv.set_key(dotenv_file, "NODE_WALLET", "true")
            if results == 1:
                dotenv.set_key(dotenv_file, "NODE_TYPE", "regular")
                dotenv.set_key(dotenv_file, "NODE_WALLET", "false")
            if results == 2:
                dotenv.set_key(dotenv_file, "NODE_TYPE", "full")
            os.system("clear")
            return
        else:
            if environ.get("VALIDATOR_WALLET"):
                return
            getWalletAddress()
    if not environ.get("NODE_TYPE"):
        dotenv.set_key(dotenv_file, "NODE_TYPE", "regular")
    return


def setMainOrTest(dotenv_file) -> None:
    if environ.get("NETWORK") is None:
        os.system("clear")
        print("*********************************************************************************************")
        print("* Setup config not found, which blockchain does this node run on?                           *")
        print("*********************************************************************************************")
        print("* [0] - Mainnet                                                                             *")
        print("* [1] - Testnet                                                                             *")
        print("*********************************************************************************************")
        menuOptions = ["[0] Mainnet", "[1] Testnet", ]
        terminal_menu = TerminalMenu(menuOptions, title="Mainnet or Testnet")
        results = terminal_menu.show()
        if results == 0:
            dotenv.set_key(dotenv_file, "NETWORK", "mainnet")
            dotenv.set_key(dotenv_file, "NETWORK_SWITCH", "t")
            dotenv.set_key(dotenv_file, "RPC_NET", "https://rpc.s0.t.hmny.io")
        if results == 1:
            dotenv.set_key(dotenv_file, "NETWORK", "testnet")
            dotenv.set_key(dotenv_file, "NETWORK_SWITCH", "b")
            dotenv.set_key(dotenv_file, "RPC_NET", "https://rpc.s0.b.hmny.io")
        os.system("clear")
        loadVarFile()
        return 


def getExpressStatus(dotenv_file) -> None:
    if environ.get("EXPRESS") is None:
        os.system("clear")
        print("*********************************************************************************************")
        print("* Express or Manual Setup?                                                                  *")
        print("*********************************************************************************************")
        print("* Would you like the turbo express setup or Manual approval of each step?                   *")
        print("*********************************************************************************************")
        menuOptions = ["[0] - Express Install", "[1] - Manual Approval", ]
        terminal_menu = TerminalMenu(menuOptions, title="* Express Or Manual Setup")
        dotenv.set_key(dotenv_file, "EXPRESS", str(terminal_menu.show()))
    return


def getWalletAddress():
    os.system("clear")
    print("*********************************************************************************************")
    print("* Signing Node, No Wallet!                                                                  *")
    print("* You are attempting to launch the menu but no wallet has been loaded, as you chose         *")
    print("* If you would like to use the menu on the server, complete the following:                  *")
    print("*********************************************************************************************")
    print("* Edit ~/.easynode.env and add your wallet address on a new line like this example:         *")
    print("* VALIDATOR_WALLET='one1thisisjustanexamplewalletreplaceme'                                 *")
    print("*********************************************************************************************")
    raise SystemExit(0)


def setAPIPaths(dotenv_file):
    if environ.get("NETWORK_0_CALL") is None:
        dotenv.set_key(dotenv_file, "NETWORK_0_CALL", f"{validatorToolbox.hmyAppPath} --node='https://api.s0.{environ.get('NETWORK_SWITCH')}.hmny.io' ")
        dotenv.set_key(dotenv_file, "NETWORK_S_CALL", f"{validatorToolbox.hmyAppPath} --node='https://api.s{environ.get('SHARD')}.{environ.get('NETWORK_SWITCH')}.hmny.io' ")
    return 


def getValidatorInfo(
    one_address: str, main_net_rpc: str, validatorData: str, save_data: bool = False, display: bool = False
) -> dict:

    d = {
        "jsonrpc": "2.0",
        "method": "hmyv2_getValidatorInformation",
        "params": [one_address],
        "id": 1,
    }
    try:
        response = post(main_net_rpc, json=d)
    except Exception as e:
        print("ERROR: <getValidatorInfo> Something went wrong with the RPC API.")
        return False, {"Error": response.text}

    if response.status_code == 200:
        data = response.json()

        if save_data:
            save_json(validatorData, data)

        if display:
            print(dumps(data, indent=4))

    else:
        data = False, {f"Error [{response.status_code}]": response.text}

    return True, data


def currentPrice():
    try:
        response = requests.get(validatorToolbox.onePriceURL, timeout=5)
    except (ValueError, KeyError, TypeError):
        response = "0.0000"
        return response
    data_dict = response.json()
    type(data_dict)
    data_dict.keys()
    return (data_dict['lastPrice'][:-4])


def getWalletBalance(
    wallet: str, save_data: bool = False, display: bool = False
) -> dict:

    d = {
        "jsonrpc": "2.0",
        "method": "hmyv2_getBalance",
        "params": [wallet],
        "id": 1,
    }
    try:
        response = post(validatorToolbox.rpc_url, json=d)
    except (ValueError, KeyError, TypeError):
        return render_template("regular_wallet.html")

    if response.status_code == 200:
        data = response.json()

        if save_data:
            save_json(validatorToolbox.validatorData, data)

        if display:
            print(dumps(data, indent=4))

    else:
        data = False, {f"Error [{response.status_code}]": response.text}

    return True, data


def getRewardsBalance(
    wallet: str, save_data: bool = False, display: bool = False
) -> dict:

    d = {
        "jsonrpc": "2.0",
        "method": "hmy_getDelegationsByDelegator",
        "params": [wallet],
        "id": 1,
    }
    try:
        response = post(validatorToolbox.rpc_url, json=d)
    except (ValueError, KeyError, TypeError):
        return render_template("regular_wallet.html")

    if response.status_code == 200:
        data = response.json()

        if save_data:
            save_json(validatorToolbox.validatorData, data)

        if display:
            print(dumps(data, indent=4))

    else:
        data = False, {f"Error [{response.status_code}]": response.text}

    return True, data


def save_json(fn: str, data: dict) -> dict:
    with open(fn, "w") as j:
        dump(data, j, indent=4)


def return_json(fn: str, single_key: str = None) -> dict:
    try:
        with open(fn, "r", encoding="utf-8") as j:
            data = load(j)
            if single_key:
                return data.get(single_key)
            return data
    except FileNotFoundError as e:
        # print(f"File not Found  ::  {e}")
        return {}


def walletPendingRewards(wallet):
    res, walletBalance = getRewardsBalance(wallet, save_data=True, display=False)
    totalRewards = 0
    for i in walletBalance["result"]:
        totalRewards = totalRewards + i["reward"]
    totalRewards = "{:,}".format(round(totalRewards * 0.000000000000000001, 2))
    return totalRewards


def getSignPercent() -> str:
    output = subprocess.getoutput(
        f"{environ.get('NETWORK_0_CALL')} blockchain validator information {environ.get('VALIDATOR_WALLET')} | grep signing-percentage"
    )
    outputStripped = output.lstrip(
        '        "current-epoch-signing-percentage": "'
    ).rstrip('",')
    try:
        math = float(outputStripped)
        signPerc = math * 100
        roundSignPerc = round(signPerc, 6)
        return str(roundSignPerc)
    except (OSError, ValueError):
        outputStripped = "0"
        return str(outputStripped)