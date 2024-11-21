CREATE TABLE SalesData (
    SalesName VARCHAR(255),
    SerialNumber float,
    Year int,
    DateRecorded datetime,
    Town VARCHAR(100),
    Address VARCHAR(255),
    SaleAmount float,
    PropertyType VARCHAR(100),
    ResidentialType VARCHAR(100),
    Company VARCHAR(100),
    SalesRatio float,
    SalesCommission float
);

select count(*) from Real_State_Sales_Datav5$;
select * from  SalesData;

BULK INSERT SalesData
FROM 'G:\Real_State_Sales_Datav5.csv'
WITH (
    FIELDTERMINATOR = ',',  
    ROWTERMINATOR = '\n',   
    FIRSTROW = 2  -- Skip header row
);

--View 
-- how many sales per each Salesperson ?
select * from SalesPerPersonPErYear
Create view SalesPerPersonPErYear as
select Salesname,Company,Year,count(*) Sales_Count,sum(SaleAmount) Total_Sales ,sum(SalesCommission) Total_Commission
 from  SalesData where Salesname != 'unkown sales'
group by salesname,Company,year;

--who is the top performer in each year ??
select * from Top_performers_salesinYear
Create view Top_performers_salesinYear as
WITH RankedSales AS (
    SELECT 
        SalesName,
		Company,
        Year,
        Total_Sales,
        Total_commission,
        RANK() OVER (PARTITION BY Year ORDER BY Total_Sales DESC) AS SalesRank
    FROM 
        SalesPerPersonPErYear
)

SELECT 
    SalesName,
	Company
    Year,
    Total_Sales,
    Total_commission
FROM 
    RankedSales
WHERE 
    SalesRank = 1;


--Sales of each company each year ?
select * from SalesPerCompanyPErYear
Create view SalesPerCompanyPErYear as
select Company,Year,count(*) Sales_Count,sum(SaleAmount) Total_Sales ,sum(SalesCommission) Total_Commission
 from  SalesData 
group by Company,year;

--what is the most sold property type ??
select * from SoldPropertypeperyear
create view SoldPropertypeperyear as
select s.PropertyType,Year,count(*) Apartment_sold
 from  SalesData s where s.PropertyType !='unknown Property'
group by s.PropertyType,Year;


--Who is the top performer in each company in each year ?
select * from Topperformerineachcompanyperyear
Create view Topperformerineachcompanyperyear as 
WITH RankedSales AS (
    SELECT 
        SalesName,
        Company,
		Year,
        Total_Sales,
        Total_commission,
        RANK() OVER (PARTITION BY Year,Company ORDER BY Total_Sales DESC) AS SalesRank
    FROM 
        SalesPerPersonPErYear
)

SELECT 
    SalesName,
	Company,
    Year,
    Total_Sales,
    Total_commission
FROM 
    RankedSales
WHERE 
    SalesRank = 1;

--how many sold units in each town per town ??
select * from salescountpertownperyear
	create view  salescountpertownperyear as
	select s.Town ,Year, count(*) TotalSales from SalesData s group by s.Town,year;
	select * from salescountpertownperyear



--Most Potential 3 Towns each year 
select * from Potentialtownsineachyear
Create view  Potentialtownsineachyear as
WITH RankedSales AS (
    SELECT 
        Town,
        Year,
        TotalSales,
        RANK() OVER (PARTITION BY Year ORDER BY TotalSales DESC) AS SalesRank
    FROM 
        salescountpertownperyear
)
SELECT 
    Town,
    Year,
    TotalSales,
	SalesRank
FROM 
    RankedSales
WHERE 
    SalesRank in (1,2,3);



	

