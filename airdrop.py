"""
Python script for airdropping tokens to a list of addresses.

Usage: python airdrop.py --token_address [YOUR TOKEN ADDRESS HERE] --whitelist_file [PATH TO YOUR TXT FILE]

example: 

python airdrop.py --token_address GGEmzbXiMmsSnkWBTWR5SfNeb5tjPAAHmdSnUdVft4GR --whitelist_file ./whitelist.txt

note: default [whitelist_file] is 'whitelist.txt' but it can be any .txt name as long as the file itself is formatted as [wallet address] [amount of token to airdrop]

example:

JBArjpYUpXJB1b3wsY3szmrynPXDPz6qgEp5NZjNRF7J 50
HHa1uCFew8jGSJSJRTqsfCvSaSpJ1zGCirkme3umH2aP 275
B7fQhEEmAdwbL87VYEmfW9RYBptKdG7A57J9cZmRT8jT 3

If no token address is provided as an argument, the user will be prompted to enter one. If no whitelist file is provided, the user will be prompted to enter the path to the file.

Dependencies:
- Python 3
- solana (install at https://docs.solana.com/cli/install-solana-cli-tools)

"""

import argparse
import logging
import sys
import subprocess
import os

def main(token_address, whitelist_file):
    # Print the current wallet and RPC cluster
    subprocess.run(["solana", "config", "get"], check=False)
    logging.info("Verify that the wallet and RPC cluster above are correct before continuing. Press enter to continue or Ctrl-C to exit.")
    input()

    # Prompt the user to enter the token address if it was not provided as an argument
    if token_address is None:
        while True:
            token_address = input("Enter the token address: ")

            # Check that the token address is 44 characters
            if len(token_address) == 44:
                break
            else:
                logging.error("Error: Invalid token address. Please try again.")

    # Check for the whitelist file in the current directory or the specified path
    if whitelist_file is None:
        file_path = "./whitelist.txt"
        if not os.path.exists(file_path):
            # If the file is not in the current directory, ask the user for the path
            while True:
                file_path = input("Enter the path to the whitelist file: ")

                # Try to open the file at the specified path
                try:
                    f = open(file_path)
                    break
                except FileNotFoundError:
                    logging.error("Error: Invalid file path. Please try again.")
        else:
            # If the file is in the current directory, open it
            f = open(file_path)
    else:
        # Open the specified file
        f = open(whitelist_file)

    # Read from the file and transfer tokens
    logging.info("Starting airdrop...")
    total_transfers = sum(1 for line in f)  # Get the total number of transfers to be done
    f.seek(0)  # Reset the file pointer to the beginning of the file
    for i, line in enumerate(f):
        address, number_to_airdrop = line.strip().split(" ")
        if not address or not number_to_airdrop:
            logging.error(f"Error: Invalid line in {whitelist_file}: {line}")
            sys.exit(f"Error: Invalid whitelist file {whitelist_file}. Please fix the error and try again.")
        # Check that the address is 44 characters long
        elif len(address) != 44:
            logging.error(f"Error: Invalid address in {whitelist_file}: {address}")
            sys.exit(f"Error: Invalid whitelist file {whitelist_file}. Please fix the error and try again.")
        # Check that the number_to_airdrop is a whole number
        elif not number_to_airdrop.isdigit():
            logging.error(f"Error: Invalid number_to_airdrop in {whitelist_file}: {number_to_airdrop}")
            sys.exit(f"Error: Invalid whitelist file {whitelist_file}. Please fix the error and try again.")
        else:
            subprocess.run(["spl-token", "transfer", token_address, number_to_airdrop, address, "--allow-unfunded-recipient", "--fund-recipient"], check=False)
            logging.info(f"{i + 1}/{total_transfers} transfers complete")  # Print progress

    # Print "Finished airdropping tokens." after all transfers are complete
    logging.info("\nFinished airdropping tokens.")
    
    # Prompt the user to close the script
    input("Press enter to close the script.")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Script for airdropping tokens to a list of addresses.')
    parser.add_argument('--token_address', help='Address of the token to be airdropped')
    parser.add_argument('--whitelist_file', help='Path to the whitelist file')

    # Parse arguments
    args = parser.parse_args()
    token_address = args.token_address
    whitelist_file = args.whitelist_file

    # Call main function
    main(token_address, whitelist_file)
