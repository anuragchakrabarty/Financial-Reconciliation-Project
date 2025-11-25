-- SQL Scripts to load before the applications is ready to load. Creating Application Table to store.
	
    -- Application Table 1 ( App Users )
		CREATE TABLE IF NOT EXISTS APPLICATION_USERS (
			ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            FIRST_NAME VARCHAR(150) NOT NULL,
            LAST_NAME VARCHAR(150) NOT NULL,
            EMAIL_ID VARCHAR(250) NOT NULL,
            PASSCODE BLOB NOT NULL
        );
        
    -- Applcation Table 2 ( Data Table )
		CREATE TABLE IF NOT EXISTS TABLE_CREATED (
			ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            TABLE_NAME VARCHAR(254) NOT NULL,
            TABLE_TYPE VARCHAR(50) NOT NULL,
            DATA_FORMAT VARCHAR(50) NOT NULL,
            USER_ID INT DEFAULT NULL, -- WILL CHANGE DEFAULT LATER ON TO NOT NULL.
            
            FOREIGN KEY (USER_ID)
            REFERENCES APPLICATION_USERS(ID)
        );
        
	-- Application Table 3 ( Table Usage ) / can merge this in table_created column itself.
		-- This table will store the last used date, If the table has been unused for 60 days. The User will provided a prompt on email. 
        -- If he / she requires to revisit the project. If not, on confirmation will automatically delete. After 90 unused, auto delete.