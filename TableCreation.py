import mysql.connector
from mysql.connector import Error

def create_connection():

    '''
        This function has been purely dedicated in creation of MySQL Connection Object.
        Once created, in which ever function is this function called, It will be solely
        to build connection.

        Note : Once built connection. It is in that function that connection and 
        connection cursor needs to be closed after completion of an operation.

    '''

    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",        
            user="root",
            password="root",
            database="swift_recon"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error:", e)
        return None


def querydType(option):

    '''
        This Function basically has the duty to convert the selected option datatype, from the column container, 
        it will be converted into MySQL Datatype Parameters and appended to the list of columns.

        This will be only called during Table Operations stage.

    '''

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

    '''
        This code block is solely dedicated to Table Creation purpose.
        This Table belongs to the data user uploads.
        
        The function accepts a CREATE TABLE query as an argument, that is created during Table Operations.

        Note : This functions calls the create_connection() function. The connection and the cursor connection needs to be closed in here itself.
            If ever overloaded / overriden, please make sure to remember the fact to close the connection, if no further operation is required.

    '''

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
    
def TableOperations(uploadedFile,pd,st):

    '''
        This is the main play arena for all the Table Creation Operation.
        The function takes arguments of streamlit uploaded file object, pandas object, streamlit object itself.

        This function will receive all the data and metadata related to the uploaded File from TableInputs function.
        The streamlit Uploaded file object and pandas object will be passed onto TableInputs.
        
        The data returned is in the format : {'fileName':FileName,'fileType':FileType,'columnsAll':columns}

        In here,
            3 Tables will be created :
                -> Main Table
                -> Invalid Table
                -> Invalid History Table

    '''

    uploadedFileDict = TableInputs(uploadedFile,pd)
    
    '''
        Data Type Options :

            This is to provide the scope of datatypes that the application supports as of now.
            Out of these scopes, can the user select the datatype of the column if they want.
        
        File Type Options :

            This stores the scope of file types our app supports for Reconciliation.

    '''

    dataTypeOptions=('VARCHAR','INT','FLOAT','DATETIME')
    fileTypeOptions=("CSV","EXCEL")

    '''
        Streamlit Session State Variables :

            Streamlit session state variables are used for temporary usage to save the 
            filenames and filetypes which are being used to actually have a default input
            for both File Name Input and File Type Input.

    '''

    if 'fileName' not in st.session_state:
        st.session_state['fileName']=uploadedFileDict['fileName']
    
    if 'fileType' not in st.session_state:
        st.session_state['fileType']=uploadedFileDict['fileType']
    
    fileNameInput=st.text_input(label="File Name : ",value=st.session_state['fileName'],key='fileName')
    fileTypeInput=st.selectbox(label="File Type : ",options=fileTypeOptions,key='fileType')

    '''
        Table Query Elements :
            This is first initialized as an Empty list.
            The Sole purpose of this list is to append all the query datatype details
            of each column seperately.
        
        Streamlit Form :
            It holds all the elements required to create the table.
            And, has the submit button labled as Create Table to 
            trigger and execute the Query.

        Streamlit Container :
            This is to subdivide the form space into containers.
            Each container belongs to each column.

        Streamlit Toast :
            It is a notification system, set for Infinite duration.
            It will display the status of the table creation.

            It holds the message that is returned from the Table Creation
            function.
            This message is passed inside the toast as Creation Status.

    '''

    tableQueryElements=[]
    with st.form(key='Column DataType Selection', clear_on_submit=False, enter_to_submit=False):

        startQuery=f"CREATE TABLE IF NOT EXISTS {fileNameInput} ( ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        
        for key,value in uploadedFileDict['columnsAll'].items():
            dataType=value
            with st.container():
                st.write(f'{key}')
                dTypeOption=st.selectbox(label='Data Type : ',options=dataTypeOptions,key=f'{dataType} {key}')
                
                dType=querydType(dTypeOption)
                query=f"{key} {dType}"

                tableQueryElements.append(query)
        
        midQuery=", ".join(tableQueryElements)
        lastQuery=")"            # Need to add Application Table Columns Status, Recon Iteration Id, Pipeline Execution Id, later on which will also require to link as Foreign Keys
        fullQuery=startQuery+midQuery+lastQuery

        submitted=st.form_submit_button("Create Table")
        if submitted:
            print(fullQuery)
            creationStatus=TableCreation(fullQuery)
            st.toast(creationStatus,duration='infinite')