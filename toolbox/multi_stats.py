import os
import json
from os import environ
from ast import literal_eval
from utils.config import validatorToolbox
from utils.library import loadVarFile, getSignPercent, getWalletBalance, printStars, setVar, loaderIntro
from utils.toolbox import freeSpaceCheck, harmonyServiceStatus, getRewardsBalance, getDBSize, refreshStats
from subprocess import PIPE, run
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu

loadVarFile()

if not environ.get("VALIDATOR_WALLET"):
    # ask for wallet, save to env.
    address = input(f'No Harmony $ONE address found, please input a one1 or 0x address: ')
    address2 = input(f'Please re-enter your address to verify: ')
    if address == address2:
        setVar(validatorToolbox.dot_env, "VALIDATOR_WALLET", address2)

if not environ.get("NETWORK_SWITCH"):
    # ask for mainnet or testnet
    os.system("clear")
    printStars()
    print("* Setup config not found, which blockchain does this node run on?                           *")
    printStars()
    print("* [0] - Mainnet                                                                             *")
    print("* [1] - Testnet                                                                             *")
    printStars()
    menuOptions = [
        "[0] Mainnet",
        "[1] Testnet",
    ]
    terminal_menu = TerminalMenu(menuOptions, title="Mainnet or Testnet")
    results = terminal_menu.show()
    if results == 0:
        setVar(validatorToolbox.dotenv_file, "NETWORK", "mainnet")
        setVar(validatorToolbox.dotenv_file, "NETWORK_SWITCH", "t")
        setVar(validatorToolbox.dotenv_file, "RPC_NET", "https://rpc.s0.t.hmny.io")
    if results == 1:
        setVar(validatorToolbox.dotenv_file, "NETWORK", "testnet")
        setVar(validatorToolbox.dotenv_file, "NETWORK_SWITCH", "b")
        setVar(validatorToolbox.dotenv_file, "RPC_NET", "https://rpc.s0.b.hmny.io")
    os.system("clear")

def statsOutputRegular() -> None:
    # Get server stats & wallet balances
    Load1, Load5, Load15 = os.getloadavg()
    sign_percentage = getSignPercent()
    total_balance, total_balance_test = getWalletBalance(environ.get("VALIDATOR_WALLET"))
    # Get shard stats here
    count = 0
    os.system("clear")
    # Print Menu
    printStars()
    print(f'{Style.RESET_ALL}* {Fore.GREEN}validator-toolbox for Harmony ONE Validators by Easy Node   v{validatorToolbox.easyVersion}{Style.RESET_ALL}   https://easynode.one *')
    printStars()
    print(f'* Your validator wallet address is: {Fore.RED}{str(environ.get("VALIDATOR_WALLET"))}{Style.RESET_ALL}\n* Your $ONE balance is:             {Fore.GREEN}{str(total_balance)}{Style.RESET_ALL}\n* Your pending $ONE rewards are:    {Fore.GREEN}{str(getRewardsBalance(validatorToolbox.rpc_endpoints, environ.get("VALIDATOR_WALLET")))}{Style.RESET_ALL}\n* Server Hostname & IP:             {validatorToolbox.serverHostName}{Style.RESET_ALL} - {Fore.YELLOW}{validatorToolbox.ourExternalIPAddress}{Style.RESET_ALL}')
    harmonyServiceStatus()
    print(f'* Epoch Signing Percentage:         {Style.BRIGHT}{Fore.GREEN}{Back.BLUE}{sign_percentage} %{Style.RESET_ALL}\n* Current disk space free: {Fore.CYAN}{freeSpaceCheck(): >6}{Style.RESET_ALL}\n* Current harmony version: {Fore.YELLOW}{environ.get("HARMONY_VERSION")}{Style.RESET_ALL}, has upgrade available: {environ.get("HARMONY_UPGRADE_AVAILABLE")}\n* Current hmy version: {Fore.YELLOW}{environ.get("HMY_VERSION")}{Style.RESET_ALL}, has upgrade available: {environ.get("HMY_UPGRADE_AVAILABLE")}')
    print(f"* CPU Load Averages: {round(Load1, 2)} over 1 min, {round(Load5, 2)} over 5 min, {round(Load15, 2)} over 15 min")
    printStars()
    while count < 4:
        try:
            remote_data, local_data = multiValidatorStats(count)
            print(f"* Remote Shard {count} Epoch: {remote_data['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(remote_data['result']['shard-chain-header']['number'])}")
            print(f"*  Local Shard {count} Epoch: {local_data['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(local_data['result']['shard-chain-header']['number'])}, Local Shard {environ.get('SHARD')} Size: {getDBSize(environ.get('SHARD'))}")
            printStars()
            count += 1
        except (ValueError, KeyError, TypeError):
            print(f'Shard {count} not found.')
        

def multiValidatorStats(shard):
    loadVarFile()
    remote_shard = [
        f"{validatorToolbox.hmyAppPath}",
        "blockchain",
        "latest-headers",
        f'--node=https://api.s{shard}.{environ.get("NETWORK_SWITCH")}.hmny.io',
    ]
    result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    remote_data = json.loads(result_remote_shard.stdout)

    # local stuff
    local_shard = [f"{validatorToolbox.hmyAppPath}", "blockchain", "latest-headers", f'--node=https://localhost:950{shard}']
    result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    local_data = json.loads(result_local_shard.stdout)
        
    return remote_data, local_data

if __name__ == "__main__":
    loaderIntro()
    refreshStats(1)
    statsOutputRegular()
    