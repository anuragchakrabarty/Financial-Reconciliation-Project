import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",        # e.g., "127.0.0.1"
            user="root",
            password="root",
            database="swift_recon"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error:", e)
        return None
    
# def check_connection():
#     connection=create_connection()
#     if connection:
#         connection.close()
#         return "Connected"
#     return "Not Connected"

# a=check_connection()
# print(a)

def querydType(option):
    if option.lower()=='varchar':
        return 'VARCHAR(200) DEFAULT NULL'
    elif option.lower()=='int':
        return 'INT DEFAULT NULL'
    elif option.lower()=='float':
        return 'FLOAT DEFAULT NULL'
    elif option.lower()=='datetime':
        return 'DATETIME DEFAULT NULL'

def TableInputs(uploadedFile,pd):
    from collections import defaultdict

    FileName=uploadedFile.name
    FileType=uploadedFile.type
    tableDF=pd.read_csv(uploadedFile)

    '''
        Table Headers :
            tableHeaders is to store all the column headers present in the file in the form of a list

        Default UI Data Type :
            datatype is to have the default data types that will be used to showcase in UI, that what datatype there columns should be.
                -> This will automatically be detected according to the values of each columns. By default it should be varchar if only num encountered then INT, or if a float then FLOAT

        Column Type :
            It is a dictionary that stores the data types as a key and has values as the list of column headers.
            This is to help seggregate the column datatypes by default unless the user thinks otherwise, will have option to select.

    '''
    tableHeaders=tableDF.columns.to_list()
    
    columns=defaultdict()

    ''' 
        The below loop actually helps us append by default the column headers into the respective datatype keys.

        ALL DATATYPES : 'VARCHAR','INT','STRING','FLOAT'
    '''
    for value in tableHeaders:
        count=0
        creationViewDF=tableDF[value].head(10).values.tolist()
        for values in creationViewDF:
            if str(values).isnumeric():
                count+=1
        if count==len(creationViewDF):
            columns[value]='INT'
        else:
            columns[value]='VARCHAR'
    
    
    return {'fileName':FileName,'fileType':FileType,'columnsAll':columns}

def TableCreation(query):
    connection=create_connection()
    creationStatus=None
    if connection:
        cursor=connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params=None)
            connection.commit()

            creationStatus='Table Created Successfully'
        
        except Error as e:
            creationStatus=f"Error Executing Query : {e}"

        finally:
            cursor.close()
            connection.close()

        return creationStatus
    
def TableOperations(uploadedFile,pd,st,tc):
    uploadedFileDict = tc.TableInputs(uploadedFile,pd)
    
    dataTypeOptions=('VARCHAR','INT','FLOAT','DATETIME')
    fileTypeOptions=("CSV","EXCEL")

    if 'fileName' not in st.session_state:
        st.session_state['fileName']=uploadedFileDict['fileName']
    
    if 'fileType' not in st.session_state:
        st.session_state['fileType']=uploadedFileDict['fileType']
    
    fileNameInput=st.text_input(label="File Name : ",value=st.session_state['fileName'],key='fileName')
    fileTypeInput=st.selectbox(label="File Type : ",options=fileTypeOptions,key='fileType')

    tableQueryElements=[]
    with st.form(key='Column DataType Selection', clear_on_submit=False, enter_to_submit=False):

        startQuery=f"CREATE TABLE IF NOT EXISTS {fileNameInput} ( ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        
        for key,value in uploadedFileDict['columnsAll'].items():
            dataType=value
            with st.container():
                st.write(f'{key}')
                dTypeOption=st.selectbox(label='Data Type : ',options=dataTypeOptions,key=f'{dataType} {key}')
                
                dType=tc.querydType(dTypeOption)
                query=f"{key} {dType}"

                tableQueryElements.append(query)
        
        midQuery=", ".join(tableQueryElements)
        lastQuery=")"            # Need to add Application Table Columns Status, Recon Iteration Id, Pipeline Execution Id, later on which will also require to link as Foreign Keys
        fullQuery=startQuery+midQuery+lastQuery

        submitted=st.form_submit_button("Create Table")
        if submitted:
            st.write(fullQuery)
            print(fullQuery)
            creationStatus=tc.TableCreation(fullQuery)
            st.toast(creationStatus,duration='infinite')