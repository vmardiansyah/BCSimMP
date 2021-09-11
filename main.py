import output_screen
import output_file
import blockchain
import usertask
import miner
import user_node
import HashSearch_PMiner_NumOnly
import HashSearch_SMiner_NumOnly

import multiprocessing
import math
import random
import time
import os

blockchaindifficultylevel = 0
blockchainmaxminer = 0
blockchainmaxusernode = 0
blockchain_difficulty_level = ['1', '2', '3', '4', '5', '6', '7']
blockchain_max_miner = ['3', '4', '5', '6', '7', '8', '9', '10']
blockchain_max_user_node = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
blockchain_max_num_trx_per_block = ['1', '2', '3', '4', '5']
number_of_miner_neighbours = 2
num_of_end_users_per_node = 2
num_of_task_per_user = 1
numOfTXperBlock = 3
list_of_user_nodes = []
list_of_end_users = []
miners_initial_wallet_value_set = 10 # set the value/reward of all miners
type_of_consensus = 1 # preparation other consensus 1=PoW ; 2=PoS ; 3=PoA


def user_screen_input_maksimum_transaction_per_block():
    while True:
        output_screen.choose_maximum_number_trx_per_block()
        global numOfTXperBlock
        numOfTXperBlock = input('-> ')
        if numOfTXperBlock in blockchain_max_num_trx_per_block:
            numOfTXperBlock = int(numOfTXperBlock)
            break
        else:
            print("Your input is incorrect, please check and try again..!!!\n")

def user_screen_input_difficultty_level():
    while True:
        output_screen.choose_difficulty_level()
        global blockchaindifficultylevel
        blockchaindifficultylevel = input('-> ')
        if blockchaindifficultylevel in blockchain_difficulty_level:
            blockchaindifficultylevel = int(blockchaindifficultylevel)
            break
        else:
            print("Your input is incorrect, please check and try again..!!!\n")

def user_screen_input_maximum_miner():
    while True:
        output_screen.choose_maximum_miner()
        global blockchainmaxminer
        blockchainmaxminer = input('-> ')
        if blockchainmaxminer in blockchain_max_miner:
            blockchainmaxminer = int(blockchainmaxminer)
            break
        else:
            print("Your input is incorrect, please check and try again..!!!\n")

def user_screen_input_maximum_user_node():
    while True:
        output_screen.choose_maximum_user_node()
        global blockchainmaxusernode
        blockchainmaxusernode = input('-> ')
        if blockchainmaxusernode in blockchain_max_user_node:
            blockchainmaxusernode = int(blockchainmaxusernode)
            break
        else:
            print("Your input is incorrect, please check and try again..!!!\n")

def initiate_user():
    for eachUserNode in range(blockchainmaxusernode):
        list_of_user_nodes.append(usertask.UserTask(eachUserNode + 1))
        for eachEndUser in range(num_of_end_users_per_node):
            list_of_end_users.append(user_node.UserNode(eachEndUser + 1, eachUserNode + 1))
    for UserNode in list_of_end_users:
        UserNode.create_tasks(num_of_task_per_user, list_of_end_users)
        UserNode.send_tasks(list_of_user_nodes)

def send_tasks_to_Blockchain():
    for node in list_of_user_nodes:
        node.send_tasks_to_Blockchain()

def create_bridging(bridges, miners_list):
    while len(bridges) != 1:
        bridge = random.choice(tuple(bridges))
        other_bridge = random.choice(tuple(bridges))
        same_bridge = True
        while same_bridge:
            other_bridge = random.choice(tuple(bridges))
            if other_bridge != bridge:
                same_bridge = False
        for eachminer in miners_list:
            if eachminer.address == bridge:
                eachminer.neighbours.add(other_bridge)
            if eachminer.address == other_bridge:
                eachminer.neighbours.add(bridge)
        bridges.remove(bridge)

def create_components(miners_list):
    all_components = set()
    for eachminer in miners_list:
        component = set()
        while len(eachminer.neighbours) < number_of_miner_neighbours:
            neighbour = random.choice(miners_list).address
            if neighbour != eachminer.address:
                eachminer.neighbours.add(neighbour)
                component.add(neighbour)
                for eachminerX in miners_list:
                    if eachminerX.address == neighbour:
                        eachminerX.neighbours.add(eachminer.address)
                        component.add(eachminer.address)
                        break
        if component:
            all_components.add(tuple(component))
    return all_components

def connect_miners(miners_list):
    bridges = set()
    all_components = create_components(miners_list)
    for comp in all_components:
        bridge = random.choice(tuple(comp))
        bridges.add(bridge)
    create_bridging(bridges, miners_list)

def initiate_number_of_miners():
    the_list_of_miners = []

    for i in range(blockchainmaxminer):
        the_list_of_miners.append(miner.Miner(i + 1))

    for eachminer in the_list_of_miners:
        output_file.write_file("temp/" + eachminer.address + "-chain_link.json", {})
        miner_wallets_log = output_file.read_file("temp/Miner_wallets_log.json")
        miner_wallets_log[str(eachminer.address)] = miners_initial_wallet_value_set
        output_file.rewrite_file("temp/Miner_wallets_log.json", miner_wallets_log)
    connect_miners(the_list_of_miners)
    output_screen.miners_are_ready()
    return the_list_of_miners

def generate_genesis_block():
    genesis_block_transactions = ["Genesis Block transaction contain the list of miners"]
    for i in range(len(miner_list)):
        genesis_block_transactions.append(miner_list[i].address)

    genesis_block = blockchain.generate_new_block(genesis_block_transactions, 'The Genesis Block', 0, 0, 0, 0, 0)
    output_screen.genesis_block_information_detail(genesis_block)
    for eachminer in miner_list:
        eachminer.receive_new_block(genesis_block, type_of_consensus, miner_list, usertask.RejectedTRX, blockchaindifficultylevel)
    output_screen.genesis_block_generation_information()

def miners_activation_process(miner_list):
    output_screen.display_mempool_information(usertask.MemPoolTRX)
    while (usertask.MemPoolTRX.qsize() > 0):
        obj = random.choice(miner_list)
        data = miner.accumulate_transactions(numOfTXperBlock, usertask.MemPoolTRX, obj.address)
        # setting interval for different difficulty level
        if (blockchaindifficultylevel <= 3):
            interval = 100
        elif (blockchaindifficultylevel == 4):
            interval = 1000
        elif (blockchaindifficultylevel == 5):
            interval = 10000
        elif (blockchaindifficultylevel == 6):
            interval = 100000
        else:
            interval = 1000000

        # Pool Miner Searching
        print('Pool Mining Searching Begin...')
        print('---------------------------------------------------------------------------------')
        HashResult = HashSearch_PMiner_NumOnly.processHashNumericOnly(data, obj.top_block['Hash Value'], blockchaindifficultylevel, blockchainmaxminer, interval)

        # Solo Miner Searching
        print('Solo Mining Searching Begin...')
        print('---------------------------------------------------------------------------------')
        print('Please be patient, the higher difficulty level makes need more time to generate.')
        Solo_HashResult = HashSearch_SMiner_NumOnly.solo_processHashNumericOnly(data, obj.top_block['Hash Value'], blockchaindifficultylevel)

        while (str(obj.address) != str('Miner_worker-' + str(HashResult[0]))):
             obj = random.choice(miner_list)
        solo_obj = obj
        miner_winner = str('Miner_worker-' + str(HashResult[0]))
        result_nonce = HashResult[1]
        result_hash_process = HashResult[2]
        result_time_generate = HashResult[3]

        solo_miner_winner = str('Solo Miner')
        solo_result_nonce = Solo_HashResult[0]
        solo_result_hash_process = Solo_HashResult[1]
        solo_result_time_generate = Solo_HashResult[2]

        obj.build_block(miner_list, usertask.RejectedTRX,
                data, miner_winner, result_nonce, result_hash_process, result_time_generate, solo_result_time_generate, blockchaindifficultylevel)



if __name__ == '__main__':
    # clear screen
    output_screen.clear()

    # initialitation active folder for output
    output_file.initiate_files()

    # Welcoming Screen of BCSimMP
    output_screen.opening_screen()

    # input the number of maximum user node
    user_screen_input_maximum_user_node()

    # input the maximum number of task/transaction per block
    user_screen_input_maksimum_transaction_per_block()

    # input the number of maximum miner node
    user_screen_input_maximum_miner()

    # input difficulty level of simulator application
    user_screen_input_difficultty_level()

    # initiate user node and their tasks
    initiate_user()

    # initiate number of miner based on user Input
    miner_list = initiate_number_of_miners()

    # Generate the first block or called Genesis BLOCK
    generate_genesis_block()

    # Sending Task
    send_tasks_to_Blockchain()

    # capturing time start the miner
    time_start = time.time()

    # miner process begin from other_bridge
    miners_activation_process(miner_list)

    blockchain.award_to_miner_winner(len(miner_list))

    elapsed_time = time.time() - time_start
    print("Elapsed time = " + str(elapsed_time) + " seconds")
    print('Finish...!')
    print('Thank you for using BCSimMP - Created on 2021.')


















# the_miners_list ==> the_list_of_miners
