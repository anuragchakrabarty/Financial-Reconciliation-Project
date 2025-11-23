import streamlit as st
import TableCreation as tc
import pandas as pd
import numpy as np

st.title('Table Creation Page')
uploadedFile=st.file_uploader("Upload File")

if uploadedFile:
    uploadedFileDict = tc.TableInputs(uploadedFile,pd)
    # {'fileName': 'test.csv', 'fileType': 'text/csv', 'columnsAll': defaultdict(None, {'STID': 'INT', 'FIRSTCOLUMN': 'VARCHAR', 'SECONDCOLUMN': 'VARCHAR', 'LASTCOLUMN': 'INT'})}
    
    datatype=('VARCHAR','INT','STRING','FLOAT')

    if 'fileName' not in st.session_state:
        st.session_state['fileName']=uploadedFileDict['fileName']
    
    fileNameInput=st.text_input("File Name : ",value=st.session_state['fileName'],key='fileName')