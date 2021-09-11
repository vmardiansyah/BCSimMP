import multiprocessing
import sys
import os
import time
import hashlib
from ctypes import c_char_p

# increase python default recursion depth limit
sys.setrecursionlimit(1000000000)

def solo_compute_hash(data):
    # MD5, SHA1, SHA224, SHA256, SHA384, and SHA512
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def solo_tampil(data, prev_hash, diff):
    startCount = 0
    trx = str(data) + str(prev_hash) + str(startCount)
    cari_nol = solo_compute_hash(trx)
    if not cari_nol.startswith("0" * diff):
        while not cari_nol.startswith("0" * diff):
            startCount += 1
            cari_nol = solo_compute_hash(str(data) + str(prev_hash) + str(startCount))
            if ((startCount % 1000000) == 0):
                print("Solo Miner update searching at : " + str(startCount) + " - " + str(startCount+1000000))
    return str(startCount) + ' ' + str(cari_nol)

def solo_processHashNumericOnly(data, prev_hash, diff):
    start = time.perf_counter()
    print("Solo Miner start searching at : 0 - 1000000")
    hasil = solo_tampil(data, prev_hash, diff)
    print('-------------------------------------RESULT--------------------------------------')
    print(str(diff) + ' Prefix Leading-Zeroes has Found...!')
    stop = time.perf_counter()
    hasil += ' ' + str(stop - start)
    hasil = list(hasil.split())

    print("Using Solo Miner    ")
#    print("Data Trx      : " + str(data))
#    print("Nonce         : " + str(hasil[0]))
#    print("Hash Value    : " + str(hasil[1]))
    print("Generate Time : " + str(hasil[2]) + ' seconds')
    print('-----------------------------------END RESULT------------------------------------')
#    print('Took: %.2f seconds.' % (stop - start))

    return hasil
