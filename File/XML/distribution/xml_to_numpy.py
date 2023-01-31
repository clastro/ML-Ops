import pandas as pd
import numpy as np
import glob
from tqdm import tqdm
from xml.etree.ElementTree import parse
import re
import string
import sys

def parse_xml(xml_file):
    '''
    Args:
        xml_file (file) : xml input file
    Returns:
        root(XML) : Returns top node
    '''
    tree = parse(xml_file) #XML 파일을 tree 형태로 파싱
    root = tree.getroot() #연결된 노드의 뿌리를 모두 불러옴
    return root

def only_number(string):
    '''
    Args:
        string (str) : Date or Time Data
    Returns:
        number : Returns only number
    '''
    try:
        number = re.sub(r'[^0-9]', '', string)
    except:
        number = '0'
    return number

def clean_data(input_string):
    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    return input_string.translate(str.maketrans('', '', punctuation))

def make_numpy(xml_root):

    '''
    Args:
        xml_root (file) : xml tag root 
    Returns:
        array : ecg numpy
    '''

    ecg = np.zeros([5000,12]) #ecg Size 초기화
    
    if(xml_root.tag == 'INFINITT_CIS'): #INFINITT_CIS인 경우

        p_id = xml_root.find('PatientInfo').find('ID').text
        if(p_id == None): # ID가 없을 경우
            p_id = xml_root.find('PatientInfo').find('BackupID').text #BackupID로 환자 아이디 추가
        WaveInfo = xml_root.findall("WaveInfo")
        WaveData = [x.findall("WaveData") for x in WaveInfo]
        Data = [x.findtext("Data") for x in WaveData[0]]

        date = xml_root.findall('StudyInfo')[0].find('Date').text
        time = xml_root.findall('StudyInfo')[0].find('Time').text

        time_info = only_number(date) + '_' + only_number(time)
        unique_id = xml_root.tag + '_' + p_id + '_' + time_info
        
        for i in range(len(Data)):
            
            ecg[:,i] = np.array(Data[i].split(','),dtype='float32')

    elif(xml_root.tag == 'BTypeECG'): #IBTypeECG인 경우
        
        p_id = xml_root.find('PatientInfo').find('PatientID').text
        StudyInfo = xml_root.findall("StudyInfo")
        RecordData = [x.findall("RecordData") for x in StudyInfo]
        Waveform = [x.findall("Waveform") for x in RecordData[0]]
        
        #print(StudyInfo[0])
        try:
            RecordInfo = StudyInfo[0].find('Record')
            time_info = only_number(RecordInfo.attrib['AcqDate']) + '_' + only_number(RecordInfo.attrib['AcqTime'])
        except AttributeError as e:
            #print(e)
            time_info = only_number(StudyInfo[0].find('StudyDate').text) + '_' + only_number(StudyInfo[0].find('StudyTime').text)
            #print(time_info)
            
        unique_id = xml_root.tag + '_' + p_id + '_' + time_info

        for i in range(len(Waveform)):
            
            Data = [x.findtext("Data") for x in Waveform[i]]
            cleaned_Data = clean_data(Data[0])
            wave = cleaned_Data.rstrip().split(' ')
            
            if(len(wave)== 4999):
                wave.extend(wave[-1:]) #4999일 경우 가장 마지막 데이터 추가
            elif(len(wave) < 100):
                wave = np.zeros(5000)
            elif(len(wave) < 5000):
                wave.extend(list(np.zeros(5000-len(wave))))
            try:
                ecg[:,i] = np.array(wave,dtype='float32')
            except ValueError:
                wave = np.resize(wave,[5000])
                ecg[:,i] = np.array(wave,dtype='float32')
                print('error!')
                print(unique_id)
        ecg = -1 * ecg # BType은 Inverse 해야 함
                
    else:
        print('error')
        return 0
    return ecg, unique_id


if __name__ == "__main__":
    
    folder = sys.argv[1] #폴더명 받기
    
    files = glob.glob(folder+'/**/*.xml', recursive=True)
    
    for ecg_file in tqdm(files):
        try:
            ecg_root = parse_xml(ecg_file)
        except:
            continue
        ecg,unique_id = make_numpy(ecg_root)
        #print(unique_id)
        np.save('/kb_smc_' + unique_id +'.npy',ecg)
