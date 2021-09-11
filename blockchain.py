import hashlib
import time
import output_file

winning_award = 5
miner_award = 2




def generate_new_block(transactions, generator_id, generate_time, solo_generate_time, nonce, prev_hash, hash_value):
    new_block = {'Transactions': transactions,
                 'Block Number': 0,
                 'Nonce': nonce,
                 'Generator ID': generator_id,
                 'Previous Hash': prev_hash,
                 'Timestamp': time.ctime(),
                 'Block Time Generation': {
                                            'Using Pool Miner (seconds)' : float(generate_time) ,
                                            'Using Solo Miner (seconds)' : float(solo_generate_time) } ,
                 'Hash Value': hash_value}
#    new_block['Hash Value'] = compute_hash_function_SHA256(new_block['Nonce'], new_block['Transactions'], new_block['Generator ID'], new_block['Previous Hash'])
    if (hash_value == 0):
        new_block['Hash Value'] = compute_hash_function_SHA256(new_block['Nonce'], new_block['Transactions'], new_block['Previous Hash'])
    return new_block

#def compute_hash_function_SHA256(nonce, transactions, generator_id, prev_hash):
def compute_hash_function_SHA256(nonce, transactions, prev_hash):
    # Can be expanded to other hash function such as MD5, SHA1, SHA224, SHA256, SHA384, and SHA512
    dataTRX = (str(transactions) + str(prev_hash) + str(nonce))
    return hashlib.sha256(dataTRX.encode('utf-8')).hexdigest()

def report_a_successful_block_addition(winning_miner, hash_of_added_block):
    record_exist = False
    temporary_confirmation_log = output_file.read_file("temp/Confirm_log.json")
    for key in temporary_confirmation_log:
        if key == hash_of_added_block and winning_miner == temporary_confirmation_log[key]['Miner Winner']:
            temporary_confirmation_log[key]['Confirmation'] += 1
            record_exist = True
            break
    if not record_exist:
        temporary_confirmation_log[str(hash_of_added_block)] = {'Miner Winner': winning_miner, 'Confirmation': 1}
    output_file.rewrite_file("temp/Confirm_log.json", temporary_confirmation_log)

def award_to_miner_winner(num_of_miners):
    read_conf_log_file = output_file.read_file("temp/Confirm_log.json")
    write_award_wallets_log = output_file.read_file("temp/Miner_wallets_log.json")
    for key in read_conf_log_file:
        if read_conf_log_file[key]['Confirmation'] > int(num_of_miners/2):
            for key1 in write_award_wallets_log:
                if key1 == read_conf_log_file[key]['Miner Winner']:
                    write_award_wallets_log[key1] += winning_award  # winner got more award
                else:
                    write_award_wallets_log[key1] += miner_award # all miner got award for their contribution
    output_file.rewrite_file("temp/Miner_wallets_log.json", write_award_wallets_log)
