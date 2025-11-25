import streamlit as st
import TableCreation as tc
import pandas as pd
import numpy as np

st.title('Table Creation Page')
uploadedFile=st.file_uploader("Upload File")

if uploadedFile:
    tc.TableOperations(uploadedFile,pd,st)      