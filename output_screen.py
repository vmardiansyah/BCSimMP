from os import system, name

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
     # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# display the task/transaction at mempool
def display_mempool_information(MemPoolTRX):
    print('The mempool contains the following tasks / transactions:')
    print('---------------------------------------------------------------------------------')
    txs = []
    for i in range(MemPoolTRX.qsize()):
        txs.append(MemPoolTRX.get())
    for tx in txs:
        print(tx)
        MemPoolTRX.put(tx)
    print('\n')

# define the maximum number of task/transaction per block of blockchain
def choose_maximum_number_trx_per_block():
    print("\nThe maximum task/transaction can be collected per block.\n"
          "Please choose the maximum number of task/transaction :\n"
          "From 1 until 5 task/transaction")

# define the screen output for user to choose difficulty level
def choose_difficulty_level():
    print("\nThe difficulty level of hash process is based on leading-zero or prefix-zero.\n"
          "Please choose the difficulty level of the Blockchain network:\n"
          "From level 1 (1 leading/prefix zero) until level 7 (7 leading/prefix zero)")

# define the screen output for user to choose the number of miners
def choose_maximum_miner():
    print("\nThe number of miners involved will impact to the process mining block.\n"
          "Please choose the number of miner that will participate:\n"
          "From minimum 3 until 10 miners")

# define the screen output for user to choose the number of user node
def choose_maximum_user_node():
    print("\nThe number of user node involved to give task/transaction.\n"
          "Please choose the number of user node that will participate:\n"
          "From minimum 1 until 10 user node")

def miners_are_ready():
    print("\n=================================================================================\n"
          "==          All Miners nodes are set and connected to their neighbors,         ==\n"
          "==            and now ready for the first block (GENESIS BLOCK)...!            ==\n"
          "=================================================================================\n")

# define the screen output for application BCSimMP openins sscreen
def opening_screen():
    print("=================================================================================\n"
          "==          Welcome to BCSimMP (Blockchain Simulator with Mining Pool          ==\n"
          "==  a blockchain simulator to introduce the power of pool miner vs solo miner  ==\n"
          "=================================================================================\n")

def genesis_block_generation_information():
    print("\n---------------------------------------------------------------------------------\n"
          "--  Genesis Block successfully generated. The Blockchain system now is up...!  --\n"
          "---------------------------------------------------------------------------------\n")

def genesis_block_information_detail(block):
    print("\n---------------------------------------------------------------------------------\n"
          " " + str(block['Generator ID']) + " has been generated and is chained into the Blockchain network \n"
          "---------------------------------------------------------------------------------")
    print("Transactions\t\t: " + str(block['Transactions']))
    print("Hash Value\t\t: " + str(block['Hash Value']))
    print("Timestamp\t\t: " + str(block['Timestamp']))
    print("Nonce\t\t\t: " + str(block['Nonce']))
    print("Previous Hash Value\t: " + str(block['Previous Hash']))
    print("---------------------------------------------------------------------------------\n")

def block_information_detail(block):
    print("\n---------------------------------------------------------------------------------\n"
          " Block has been generated and is chained into the Blockchain Network by. " + block['Generator ID'] + "\n"
          "---------------------------------------------------------------------------------")
    print("Transactions\t\t: " + str(block['Transactions']))
    print("Hash Value\t\t: " + str(block['Hash Value']))
    print("Timestamp\t\t: " + str(block['Timestamp']))
    print("Nonce\t\t\t: " + str(block['Nonce']))
    print("Previous Hash Value\t: " + str(block['Previous Hash']))
    print("---------------------------------------------------------------------------------\n")

def mempool_is_empty():
    print("MemPool do not have any task/transaction...")
