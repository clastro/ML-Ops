import pandas as pd
import numpy as np
import glob
from tqdm import tqdm
from xml.etree.ElementTree import parse
import xml.etree.ElementTree as et
import re
import string
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")
import sys

engine = create_engine('sqlite:////smc_work/data/datadisk/smc_data/sql/smc_metadata_2023.db', echo=False)

def parse_xml(xml_file):
    '''
    Args:
        xml_file (file) : xml input file
    Returns:
        Element : xml tag
    '''
    tree = parse(xml_file) #XML 파일을 tree 형태로 파싱
    root = tree.getroot() #연결된 노드의 뿌리를 모두 불러옴
    return root


def only_number(string):
    '''
    Args:
        string (str) : Date or Time Data
    Returns:
        string : number
    '''
    try:
        number = re.sub(r'[^0-9]', '', string)
    except:
        number = '0'
    return number

def df_transform(df,xml_type = 'A',data_type = 'smc'):
    idx_cols = ['PatientID','Sex','Age','SampleRate','Severity','Amplitude','StudyDate','StudyTime','Statement','Comment','BirthDate']
    xml_tag = 'INFINITT_CIS'
    
    if(xml_type == 'B'):
        df['BirthDate'] = None
        xml_tag = 'BTypeECG'
            
    df.columns = idx_cols
    
    xml_info = data_type + '_' + xml_tag
    patient_info = df['PatientID'] + '_' + only_number(df['StudyDate'][0]) + '_' + only_number(df['StudyTime'][0])
    
    df['UniqueID'] =  xml_info + '_' + patient_info
    
    df = df.astype(str)
    
    return df

def append_column(root,cols,tag = 'text'):
    if(tag == 'attrib'):
        return [elem.attrib for elem in root.iter() if elem.tag in cols]
    else:
        return [elem.text for elem in root.iter() if elem.tag in cols]
    
def get_root_child(root,cols,col_order:int):
    """
    Args:
        root (tag) : XML data root
        cols (list) : column list
        col_order (int) : column 순서
    Returns:
        list : XML Info
    """
    return [info.text for info in root.getchildren()[col_order] if info.tag in cols]


def get_double_root_child(root,cols,col_order:int):
    """
    Args:
        root (tag) : XML data root
        cols (list) : column list
        col_order (int) : column 순서
    Returns:
        nested - list : XML Info
    """
    return [[info_detail.text for info_detail in info] for info in root.getchildren()[col_order] if info.tag in cols]

def make_data_A(xml_root,data_type):
    #idx_col = ['PatientID','BirthDate','Gender','Age','Date','Time','Severity','Statement','Comment','SamplingRate','Amplitude']
    
           
    xml_cols = ['ID','BirthDate','Gender','Age','BackupID','Date','Time','Severity','Statement','Comment','SamplingRate','Amplitude']
    
    id_col =  ['ID','BirthDate','Gender','Age','BackupID'] #첫번째 태그
    date_col = ['Date','Time']
    desc_col = ['Severity']
    desc_col2 = ['Diagnosis']
    equip_col = ['SamplingRate','Amplitude']
    
    data = get_root_child(xml_root,id_col,1)

    if(data[0] == None):
        data[0] = data[4]
    
    data.pop()
    del(xml_cols[4])
    
    data.extend(get_root_child(xml_root,date_col,3))
    data.extend(get_double_root_child(xml_root,desc_col,4))
    diagnosis = np.array(get_double_root_child(xml_root,desc_col2,4),dtype='object')
    
    if(len(diagnosis) == 0):
        statement = 'None'
        comment = 'None'
    else:
        statement = diagnosis[:,0]
        comment = diagnosis[:,1]
    
    data.append(statement)
    data.append(comment)
    
    data.extend(get_root_child(xml_root,equip_col,5))

    re_order_cols = ['ID','Gender','Age','SamplingRate','Severity','Amplitude','Date','Time','Statement','Comment','BirthDate']
    
    df = pd.DataFrame([data],columns=xml_cols)
    df = df[re_order_cols]
    df = df_transform(df,'A',data_type)
    
    return df


def make_data_B(xml_root,data_type):

    '''
    Args:
        xml_root (XML) : XML 파일 태그 
    Returns:
        df (DataFrame) : DataFrame 형태로 저장된 환자 정보
    '''
        
    xml_cols = ['PatientID','PatientSEX','PatientAge','SampleRate','Severity','overallgain']
    date_cols = ['StudyDate','StudyTime']
    record_cols = 'Record'
    left_state_cols = ['Leftstatement']
    right_state_cols = ['Rightstatement']

    data = [elem.text for elem in xml_root.iter() if elem.tag in xml_cols]

    date_val = append_column(xml_root,date_cols)
    data.extend(date_val)

    # XML 데이터에 StudyDate는 없고 Record 태그에 있는 경우 추가
    record_val = append_column(xml_root,record_cols,'attrib')

    if(data[6] == None):
        data[6] = record_val[0]['AcqDate']
    if(data[7] == None):
        data[7] = record_val[0]['AcqTime']

    data.append(append_column(xml_root,left_state_cols))
    data.append(append_column(xml_root,right_state_cols))
    
    df = pd.DataFrame([data])
    df = df_transform(df,'B',data_type)
        
    return df


if __name__ == "__main__":
    try:
        folder = sys.argv[1] #폴더명 받기
    except:
        raise 'python XML_to_sql.py (폴더명)'
    
    if(folder == 'changwon'): #83666개 53분 소요
        db_table = 'patient_info_cw_smc'
        data_type = 'cw_smc'
    elif(folder == 'KBSMC'): #10302개 7분 소요
        db_table = 'patient_info_kb_smc'
        data_type = 'kb_smc'
    else:
        db_table = 'patient_info_smc'
        data_type = 'smc'
    
    files = glob.glob(folder+'/**/*.xml', recursive=True)
    for ecg_file in tqdm(files):
        try:
            ecg_root = parse_xml(ecg_file)
        except:
            continue
            
        if(ecg_root.tag != 'BTypeECG'):
            df = make_data_A(ecg_root,data_type)
        else:
            df = make_data_B(ecg_root,data_type)    
        df.to_sql(db_table, con=engine, if_exists='append',index=False)
