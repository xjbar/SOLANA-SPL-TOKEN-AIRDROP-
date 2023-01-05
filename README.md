# SOLANA-SPL-TOKEN-AIRDROP
*Python script for airdropping Solana SPL tokens to a list of addresses.*

## **PREREQUISITES:**

- Python 3
- Solana (install at https://docs.solana.com/cli/install-solana-cli-tools)
- a .txt file that includes all of the wallet addresses you want to airdrop to

Your txt file needs to be formatted like this:

`[WALLET ADDRESS] [AMOUNT TO AIRDROP]`

**Example**

![Alt Image text](https://i.imgur.com/o2VAjRB.jpg "")

## **HOW TO RUN:**

1. Download the `airdrop.py`
2. Open CLI and CD to the directory you saved it to.
3. run `python airdrop.py --token_address [YOUR TOKEN ADDRESS HERE] --whitelist_file [PATH TO YOUR TXT FILE]`
4. Follow prompts and airdrop! Done
