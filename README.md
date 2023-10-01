----------------------------
# cryptomines-blockchain
----------------------------
## How to install from source
### For Linux and Mac OS:

1. Open terminal and go to instalation catalog. (for example /opt).

        cd /opt

2. Download repository with submodules.

        git https://github.com/Cryptomines-Network/cryptomines-blockchain.git --recurse-submodules

3. Go to "./cryptomines-blockchain".

        cd cryptomines-blockchain

4. Give executable permision to "./install.sh" and if you want to install GUI for this blockchain "./install-gui.sh".

        chmod +x ./install.sh
        chmod +x ./install-gui.sh

5. Run "./install.sh".

        sh ./install.sh

6. Active virtual enviroment.

        . ./activate

7. (Optional) Install GUI.

        sh ./install-gui.sh
