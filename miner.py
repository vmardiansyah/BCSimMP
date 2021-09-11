import output_file
import output_screen
import HashSearch_PMiner_NumOnly
import blockchain
import usertask
import time
import json
import math
import multiprocessing
import hashlib
from ctypes import c_char_p

target = 2 ** (256 - 2)
type_of_consensus = 1 # preparation other consensus 1=PoW ; 2=PoS ; 3=PoA


class Miner:
    def __init__(self, address):
        self.address = "Miner_worker-" + str(address)
        self.top_block = {}
        self.isAuthorized = False                   # will be used in PoS
        self.next_pos_block_from = self.address     # will be used in PoA
        self.neighbours = set()

    def receive_new_block(self, new_block, type_of_consensus, miner_list, RejectedTRX, diff):
        local_temp_file_chain = output_file.read_file(str("temp/" + self.address + "-chain_link.json"))
        if ((len(local_temp_file_chain) == 0) and (new_block['Generator ID'] == 'The Genesis Block')):
            self.add(new_block, miner_list)
        else:
            list_of_hashes_in_local_chain = []
            for key in local_temp_file_chain:
                list_of_hashes_in_local_chain.append(local_temp_file_chain[key]['Hash Value'])
            if new_block['Hash Value'] not in list_of_hashes_in_local_chain:
                if (proofOFwork_is_valid(new_block, self.top_block['Hash Value'], diff)): # or other condition:
                    self.add(new_block, miner_list)
                    for worker in miner_list:
                        if worker.address in self.neighbours:
                            worker.receive_new_block(new_block, type_of_consensus, miner_list, RejectedTRX, diff)
                else:
                    print('Block is failed to broadcast because of had invalid Proof-of-Work...!!!')


    def add(self, block, list_of_miners):
        ready = False
        while True:
            try:
                local_chain_external_file = open(str("temp/" + self.address + "-chain_link.json"))
                local_temp_file_chain = json.load(local_chain_external_file)
                local_chain_external_file.close()
                break
            except:
                time.sleep(0.2)
        if len(local_temp_file_chain) == 0:
            ready = True
        else:
            if block['Previous Hash'] == self.top_block['Hash Value']:
                blockchain.report_a_successful_block_addition(block['Generator ID'], block['Hash Value'])
                    # output.block_success_addition(self.address, block['generator_id'])
                ready = True
        if ready:
            block['Block Number'] = len(local_temp_file_chain)
            self.top_block = block
            local_temp_file_chain[str(len(local_temp_file_chain))] = block
            output_file.rewrite_file(str("temp/" + self.address + "-chain_link.json"), local_temp_file_chain)


    def build_block(self, miner_list, discarded_txs, data, miner_winner, result_nonce, result_hash_process, result_time_generate, solo_result_time_generate, diff):
        count = 0
        for x in miner_list:
            count += 1
        accumulated_transactions = data
        if accumulated_transactions:
            transactions = accumulated_transactions
#            new_block = proofOFwork(blockchain.generate_new_block(transactions, self.address, self.top_block['Hash Value']))
            new_block = blockchain.generate_new_block(transactions, miner_winner, result_time_generate, solo_result_time_generate, result_nonce, self.top_block['Hash Value'], result_hash_process)
            output_screen.block_information_detail(new_block)
            for elem in miner_list:
                if elem.address in self.neighbours:
                    elem.receive_new_block(new_block, type_of_consensus, miner_list, discarded_txs, diff)


def proofOFwork(block):
    while True:
        block['Hash Value'] = blockchain.compute_hash_function_SHA256(block['Nonce'], block['Transactions'], block['Previous Hash'])
        print('\n\n\n' + block['Hash Value'] + '\n\n\n')
        if int(block['Hash Value'], 16) > target:
            block['Nonce'] += 1
        else:
            break
    return block

def proofOFwork_is_valid(block, expected_previous_hash, diff):
    block_is_valid = False
    state_1 = block['Hash Value'] == blockchain.compute_hash_function_SHA256(block['Nonce'], block['Transactions'], expected_previous_hash)
    state_2 = block['Hash Value'].startswith("0" * diff)
    if state_1 and state_2:
        block_is_valid = True

    return block_is_valid


def accumulate_transactions(num_of_tx_per_block, mempool, miner_address):
    lst_of_transactions = []
    for i in range(num_of_tx_per_block):
        if mempool.qsize() > 0:
            try:
                lst_of_transactions.append(mempool.get(True, 1))
            except:
                print("error in accumulating full new list of TXs")
        else:
            output_screen.mempool_is_empty()
            break
    return lst_of_transactions
