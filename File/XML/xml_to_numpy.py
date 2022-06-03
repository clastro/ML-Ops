import pandas as pd
import numpy as np
#!pip install pandas_read_xml
import pandas_read_xml as pdx
from tqdm import tqdm
import glob

xml_file = glob.glob('/smc_work/home/weladmin/Desktop/data/XML/foldername/*.xml') # 경로의 모든 xml 파일

valueErrorsum = 0
attriErrorSum = 0

for xml in tqdm(xml_file):
    #print(xml)
    machine_type = 'INFINITT_CIS'
    
    try:
        wave_data = pdx.read_xml(xml,['INFINITT_CIS','WaveInfo','WaveData'],encoding='utf-16')
    except UnicodeError as e:
        #print(e)
        wave_data = pdx.read_xml(xml,['INFINITT_CIS','WaveInfo','WaveData'],encoding='utf-8-sig')
    except KeyError as e:
        #print(e)
        wave_data = pdx.read_xml(xml,['BTypeECG','StudyInfo','RecordData'],encoding='utf-16')
        machine_type = 'BTypeECG'
    except:
        wave_data = pdx.read_xml(xml,['BTypeECG','StudyInfo','RecordData'])
        machine_type = 'BTypeECG'
        
    file_name = xml.split('/')[-1].split('.')[0]
     
    for i in range(12):
        if(machine_type == 'INFINITT_CIS'):
            try:
                lead = np.array(wave_data[i][0]['Data']['#text'].split(','),dtype=np.float32)
            except:
                lead = np.zeros(lead_sum.shape[1]) #lead Number가 아예 존재하지 않으면 0으로 다 채워 넣음
        else:
            try:
                lead = np.array(wave_data[i][0]['Waveform']['Data'].split(' '),dtype=np.float32) * -1
            except AttributeError as e:
                print(e)
                print(xml)
                lead = np.zeros(lead_sum.shape[1]) #lead Number가 아예 존재하지 않으면 0으로 다 채워 넣음
                
        if(i == 0):
            lead_sum = lead
        else:
            try:
                lead_sum = np.vstack([lead_sum,lead])
            except ValueError as e: #Lead가 부족하거나 일부 존재
                print(e)
                print(xml)
                print('lead 부족하거나 일부 존재')
                print(valueErrorsum)
                valueErrorsum +=1
                new_lead = np.pad(lead,(0,lead_sum.shape[1]-lead.shape[0]),'constant', constant_values=0) 
                #lead가 부족하면 오른쪽은 0으로 모두 채움                
                lead_sum = np.vstack([lead_sum,new_lead])
        
    np.save('./original/smc_cw_data_' + machine_type +'_' + file_name +'.npy',lead_sum.T)
