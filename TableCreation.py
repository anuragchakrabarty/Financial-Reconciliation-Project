import mysql.connector
from mysql.connector import Error

def create_connection(self):
    try:
        self.connection = mysql.connector.connect(
            host="127.0.0.1",        # e.g., "127.0.0.1"
            user="root",
            password="root",
            database="swift_recon"
        )
        if self.connection.is_connected():
            print("Connected to Swift Recon DataBase")
            return self.connection
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

def TableCreation():
    return