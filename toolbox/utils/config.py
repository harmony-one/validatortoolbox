import os
import socket
import urllib.request

class validatorToolbox:
    easyVersion = "1.1.6"
    serverHostName = socket.gethostname()
    userHomeDir = os.path.expanduser("~")
    dotenv_file = f"{userHomeDir}/.easynode.env"
    activeUserName = os.path.split(userHomeDir)[-1]
    harmonyDirPath = os.path.join(userHomeDir, "harmony")
    harmonyAppPath = os.path.join(harmonyDirPath, "harmony")
    hmyAppPath = os.path.join(harmonyDirPath, "hmy")
    harmonyConfPath = os.path.join(harmonyDirPath, "harmony.conf")
    blskeyDirPath = os.path.join(hmyAppPath, ".hmy", "blskeys")
    hmyWalletStorePath = os.path.join(userHomeDir, ".hmy_cli", "account-keys", activeUserName)
    toolboxLocation = os.path.join(userHomeDir, "validatortoolbox")
    validatorData = os.path.join(toolboxLocation, "toolbox", "metadata", "validator.json")
    passwordPath = os.path.join(harmonyDirPath, "passphrase.txt")
    toolboxLocation = os.path.join(userHomeDir, "validatortoolbox")
    main_net_rpc = 'https://rpc.s0.t.hmny.io'
    main_net_call = '/home/serviceharmony/harmony/hmy --node="https://api.s0.t.hmny.io"'
    test_net_rpc = 'https://rpc.s0.b.hmny.io'
    test_net_call = '/home/serviceharmony/harmony/hmy --node="https://api.s0.b.hmny.io"'
    ourExternalIPAddress = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    mainMenuRegular = os.path.join(toolboxLocation, "toolbox", "messages", "regularmenu.txt")
    mainMenuFull = os.path.join(toolboxLocation, "toolbox", "messages", "fullmenu.txt")