import pandas as pd
import numpy as np
import glob
from tqdm import tqdm
from xml.etree.ElementTree import parse

files = glob.glob('/path/*.xml')

for file in tqdm(files):
    
    filename = file.split('KBSMC/')[1].split('.xml')[0] #파일 이름 xml이랑 똑같이 설정
    
    info_dict = {} #한 명 환자의 정보를 담을 dictionary
    
    tree = parse(file) #XML 파일을 tree 형태로 파싱
    root = tree.getroot() #연결된 노드의 뿌리를 모두 불러옴
    
    ecg = np.zeros([5000,12]) #ecg Size 초기화
    
    if(root.tag == 'INFINITT_CIS'): #INFINITT_CIS인 경우
        
        WaveInfo = root.findall("WaveInfo")
        WaveData = [x.findall("WaveData") for x in WaveInfo]
        Data = [x.findtext("Data") for x in WaveData[0]]
        
        for i in range(len(Data)):
            
            ecg[:,i] = np.array(Data[i].split(','),dtype='float32')
        
    elif(root.tag == 'BTypeECG'): #IBTypeECG인 경우
        
        StudyInfo = root.findall("StudyInfo")
        RecordData = [x.findall("RecordData") for x in StudyInfo]
        Waveform = [x.findall("Waveform") for x in RecordData[0]]
        
        for i in range(len(Waveform)):
            
            Data = [x.findtext("Data") for x in Waveform[i]]
            ecg[:,i] = np.array(Data[0].split(' '),dtype='float32')
            
    else:
        print('error')
    np.save('./original/smc_kb_data_' + root.tag +'_' + filename +'.npy',ecg)
