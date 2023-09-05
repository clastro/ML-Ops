import pandas as pd
import numpy as np
#!pip install pandas_read_xml
import pandas_read_xml as pdx
from tqdm import tqdm
import glob
import os
from xml.etree.ElementTree import parse
import pathlib

def clean_data(input_string):
    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    return input_string.translate(str.maketrans('', '', punctuation))

class XMLparser:
    
    def __init__(self, file):
        
        self.file = file
        tree = parse(self.file) #XML 파일을 tree 형태로 파싱
        self.root = tree.getroot() #연결된 노드의 뿌리를 모두 불러옴
        
    def xml2npy(self):        
        
        ecg = np.zeros([5000,12]) #ecg Size 초기화
        
        if(self.root.tag == 'INFINITT_CIS'): #INFINITT_CIS인 경우

                WaveInfo = self.root.findall("WaveInfo")
                WaveData = [x.findall("WaveData") for x in WaveInfo]
                Data = [x.findtext("Data") for x in WaveData[0]]

                for i in range(len(Data)):

                    ecg[:,i] = np.array(Data[i].split(','),dtype='float32')

        elif(self.root.tag == 'BTypeECG'): #IBTypeECG인 경우

            StudyInfo = self.root.findall("StudyInfo")
            RecordData = [x.findall("RecordData") for x in StudyInfo]
            Waveform = [x.findall("Waveform") for x in RecordData[0]]
            
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

        else:
            print('Type ERROR')
            
        return ecg
    
    def xml2info(self):
        
        path = pathlib.Path(self.file)
        unique_id = path.name.split('.')[0]
        
        info_dict = {}
    
        if(self.root.tag == 'INFINITT_CIS'): #INFINITT_CIS인 경우

            PatientInfo = self.root.findall("PatientInfo") #환자 정보 불러옴
            PatientID = [x.findtext("ID") for x in PatientInfo] #환자 ID 불러옴
            Age = [x.findtext("Age") for x in PatientInfo] #환자 ID 불러옴
            Gender = [x.findtext("Gender") for x in PatientInfo] #환자 ID 불러옴

            StudyInfo = self.root.findall("StudyInfo") # Examination 태그 데이터 정보 불러옴
            Status = [x.findtext("Status") for x in StudyInfo]
            StudyDate = [x.findtext("Date") for x in StudyInfo]
            StudyTime = [x.findtext("Time") for x in StudyInfo]

            Examination = self.root.findall("Examination") # Examination 태그 데이터 정보 불러옴
            Diagnosis = [x.findall("Diagnosis") for x in Examination] #진단 정보 불러옴 
            Statements = [x.findtext("Statement") for x in Diagnosis[0]] #진단 정보의 Statements 태그 (SMC 라벨링)

            Status.extend(Statements)

            #info_dict['Severity'] = Severity[0] 
            info_dict['Statements'] = Status    
            info_dict['Age'] = Age[0]    
            info_dict['gender'] = Gender[0]    
            info_dict['StudyDate'] = StudyDate[0]
            info_dict['StudyTime'] = StudyTime[0]
            info_dict['Type'] = 'INFINITT_CIS'
            info_dict['Patient_id'] = PatientID[0]
            info_dict['unique_id'] = unique_id

        elif(self.root.tag == 'BTypeECG'): #IBTypeECG인 경우

            PatientInfo = self.root.findall("PatientInfo") #환자 정보 불러옴
            PatientID = [x.findtext("PatientID") for x in PatientInfo] #환자 ID 불러옴
            Age = [x.findtext("PatientAge") for x in PatientInfo] #환자 ID 불러옴
            Gender = [x.findtext("PatientSex") for x in PatientInfo] #환자 ID 불러옴

            StudyInfo = self.root.findall("StudyInfo") # Examination 태그 데이터 정보 불러옴
            StudyDate = [x.findtext("StudyDate") for x in StudyInfo]
            StudyTime = [x.findtext("StudyTime") for x in StudyInfo]

            Interpretation = [x.findall("Interpretation") for x in StudyInfo]
            Statements = [x.findall("Statement") for x in Interpretation[0]]

            Mdsignatureline = [x.findtext("Mdsignatureline") for x in Interpretation[0]]
            Leftstatement = [x.findtext("Leftstatement") for x in Statements[0]]
            Mdsignatureline.extend(Leftstatement)

            #info_dict['Severity'] = Severity[0] 
            info_dict['Statements'] = Mdsignatureline    
            info_dict['Age'] = Age[0]    
            info_dict['gender'] = Gender[0]    
            info_dict['StudyDate'] = StudyDate[0]
            info_dict['StudyTime'] = StudyTime[0]
            info_dict['Type'] = 'BTypeECG'
            info_dict['Patient_id'] = PatientID[0]
            info_dict['unique_id'] = unique_id

        else:
            print(file)
        return info_dict
    
    