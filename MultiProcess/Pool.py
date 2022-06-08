from multiprocessing import Pool, TimeoutError
from tqdm import tqdm
import time
import os

with Pool(processes=15) as pool:
    results = [pool.apply_async(f, args=(i, )) for i in df_pqrst_afib['unique_id']]
    results = [r.get() for r in tqdm(results)]
