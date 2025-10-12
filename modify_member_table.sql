-- SQL指令來修改MEMBER表格結構
-- 將 NAME 列改為 FNAME 和 LNAME 兩列

-- 1. 創建備份表
CREATE TABLE MEMBER_backup AS SELECT * FROM MEMBER;

-- 2. 刪除舊的MEMBER表格
DROP TABLE MEMBER;

-- 3. 創建新的MEMBER表格結構
CREATE TABLE "MEMBER" (
	"MID"	INTEGER NOT NULL UNIQUE,
	"FNAME"	TEXT NOT NULL,
	"LNAME"	TEXT NOT NULL,
	"ACCOUNT"	TEXT NOT NULL,
	"PASSWORD"	TEXT NOT NULL,
	"IDENTITY"	TEXT NOT NULL,
	PRIMARY KEY("MID" AUTOINCREMENT)
);

-- 4. 從備份表格遷移數據（需要手動分割NAME欄位）
-- 假設NAME格式是 "FirstName LastName"
INSERT INTO MEMBER (MID, FNAME, LNAME, ACCOUNT, PASSWORD, IDENTITY)
SELECT 
    MID,
    CASE 
        WHEN instr(NAME, ' ') > 0 THEN substr(NAME, 1, instr(NAME, ' ') - 1)
        ELSE NAME
    END as FNAME,
    CASE 
        WHEN instr(NAME, ' ') > 0 THEN substr(NAME, instr(NAME, ' ') + 1)
        ELSE ''
    END as LNAME,
    ACCOUNT,
    PASSWORD,
    IDENTITY
FROM MEMBER_backup;

-- 5. 刪除備份表格（可選）
-- DROP TABLE MEMBER_backup;