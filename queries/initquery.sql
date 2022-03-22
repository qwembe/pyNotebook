--sql queries

CREATE TABLE IF NOT EXISTS auth 
( Username VARCHAR(100) NOT NULL ,
  Pass VARCHAR(100) NOT NULL,
  dateob DATE,
  PRIMARY KEY (Username)) 
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS notebook 
( uname VARCHAR(100) NOT NULL ,
  tel VARCHAR(100) NOT NULL,
  dateob DATE NOT NULL,
  PRIMARY KEY (uname, tel , dateob))
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- SELECT * from notebook

-- INSERT INTO  notebook
-- (uname,tel,dateob) VALUES
-- ("Андрей", "telephone","2000-01-11");