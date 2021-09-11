import multiprocessing
import sys
import os
import time
import hashlib
from ctypes import c_char_p

# increase python default recursion depth limit
sys.setrecursionlimit(1000000000)

def compute_hash(data):
    # MD5, SHA1, SHA224, SHA256, SHA384, and SHA512
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def tampil(data, prev_hash, diff, pID, startCount, maxCount, output, maxMiner,interval):
    trx = str(data) + str(prev_hash) + str(startCount)
    cari_nol = compute_hash(trx)
    if not cari_nol.startswith("0" * diff):
        while not cari_nol.startswith("0" * diff) and startCount < maxCount:
            startCount += 1
            cari_nol = compute_hash(str(data) + str(prev_hash) + str(startCount))
            if cari_nol.startswith("0" * diff):
                if not output.value:
                    output.value = str(pID) + ' ' + str(startCount) + ' ' + str(cari_nol)
            elif ((startCount == maxCount) and (cari_nol.startswith("0" * diff) == False)):
                startCount = int(startCount) + (int(maxMiner) * int(interval)) - (int(interval) - 1)
                maxCount = int(maxCount) + (int(maxMiner) * int(interval))

                print("Miner #" + str(pID) + " update searching at : " + str(startCount) + " - " + str(maxCount))
                tampil(data, prev_hash, diff, pID, startCount, maxCount, output, maxMiner,interval)
    else:
        if not output.value:
            output.value = str(pID) + ' ' + str(startCount) + ' ' + str(cari_nol)

def processHashNumericOnly(data, prev_hash, diff, maxMiner, interval):
    jobs = []
    # Create parent event/manager
    parent = multiprocessing.Manager()
    # Create child variable
    output = parent.Value(c_char_p, False)
    x = 1

    start = time.perf_counter()

    #Create Miner
    for i in range(1, int(maxMiner)+1):
        print("Miner #" + str(i) + " start searching at : " + str((i-1) * int(interval)) + " - " + str((i-1) * (int(interval)) + int(interval)))
        p = multiprocessing.Process(target=tampil, args=(data, prev_hash, int(diff), i, ((i-1) * int(interval)), ((i-1) * (int(interval)) + int(interval)), output, maxMiner,interval))
        x += 1
        p.start()
        jobs.append(p)

    #Check whether parent is set or not. When set close all child processes
    q = True
    while q:
        if output.value:
            for j in jobs:
                #Terminate each process
                j.terminate()
            #Terminating main process
            print('-------------------------------------RESULT--------------------------------------')
            print(str(diff) + ' Prefix Leading-Zeroes has Found...!')
            stop = time.perf_counter()
            output.value += ' ' + str(stop - start)
            hasil = output.value
            hasil = list(hasil.split())
            del output # release output from mem to avoid cached result
            q = False
    print("By Miner      : " + str(hasil[0]))
    print("Nonce         : " + str(hasil[1]))
    print("Hash Value    : " + str(hasil[2]))
    print("Generate Time : " + str(hasil[3]) + ' seconds')
    print('-----------------------------------END RESULT------------------------------------')
#    print('Took: %.2f seconds.' % (stop - start))

    return hasil
