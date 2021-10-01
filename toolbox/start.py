import os
import time
import dotenv
from os import environ
from utils.config import validatorToolbox
from utils.installer import firstSetup, printStars, recheckVars, passphraseStatus
from utils.shared import loaderIntro, setWalletEnv
from utils.toolbox import runRegularNode, runFullNode


if __name__ == "__main__":
    os.system("clear")
    loaderIntro()
    if os.path.exists(validatorToolbox.dotenv_file) == False:
        firstSetup()
    print("* Configuration file detected, loading the validatortoolbox menu application.")
    printStars()
    if validatorToolbox.easyVersion != environ.get("EASY_VERSION"):
        dotenv.unset_key(validatorToolbox.dotenv_file, "EASY_VERSION")
        dotenv.set_key(validatorToolbox.dotenv_file, "EASY_VERSION", validatorToolbox.easyVersion)
    time.sleep(1)
    if environ.get("SETUP_STATUS") != "2":
        recheckVars()
        passphraseStatus()
    if environ.get("NODE_TYPE") == "regular":
        if environ.get("VALIDATOR_WALLET") is None:
            setWalletEnv(validatorToolbox.dotenv_file)
        runRegularNode()
    if environ.get("NODE_TYPE") == "full":
        runFullNode()
    print("Uh oh, you broke me! Contact Easy Node")
    raise SystemExit(0)