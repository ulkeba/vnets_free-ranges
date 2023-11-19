# Prepare Python
- Create a new virtual environment
  ```
  python3 -m venv env
  ```

- Install required packages
  ```
  pip install -r requirements.txt
  ```

# Prepare Azure CLI
- Install [Azure Command-Line Interface (CLI)](https://learn.microsoft.com/en-us/cli/azure/).
- [Sing in](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli-interactively) by running
  ```
  az login
  ```
- [Select the right subscription](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-set) by running
  ```
  az account set --subscription [YOUR SUBSCRIPTION GUID HERE]
  ```

# Get VNet data
- Get all subscription's VNets' metadata and save to `vnets.json` by running
  ```
  ./vnets_get.sh
  ```

# Identify free ranges
- Run the Python script based on [netaddr](https://netaddr.readthedocs.io/en/latest/index.html) to identfy free ranges and save them to `vnets_free-ranges.json` by running
  ```
  python3 ./vnets_identify-free-ranges.py
  ```