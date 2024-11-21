#---------------------#
import pandas as pd 
import seaborn as sns 






df = pd.read_csv('G:\Real_Estate_Sales_2001-2022_GL.csv')

df.info()

df.dtypes
# View the first few rows
print(df.head())

# Get a summary of the dfset
print(df.info())

# Convert Serial Number and Year to object type
df['Serial Number'] = df['Serial Number'].astype(str)
df['Year'] = df['Year'].astype(str)
# Rename column 
df.rename(columns={'Alice': 'Sales name'}, inplace=True)
df.rename(columns={'List Year': 'Year'}, inplace=True)


#Filling Null Data to avoid data loss 
df.loc[df['Residential Type'] == 'Commercial', 'Property Type'] = 'Commercial'
df.loc[df['Residential Type'] == 'Vacant Land', 'Property Type'] = 'Vacant Land'
df.loc[df['Residential Type'] == 'Industrial', 'Property Type'] = 'Industrial'



# Check for null values
print(df.isnull().sum())

import numpy as np
df['List Year'] = np.random.choice(range(2020, 2025), size=len(df))

#Filling null cells with unkown as it may affect the data integrity
df['Property Type'] = df['Property Type'].fillna('unknown Property')
df['Residential Type'] = df['Residential Type'].fillna('unknown Property')
df['Address'] = df['Address'].fillna('N/A')
df['Sales name'] = df['Sales name'].fillna('unkown sales')
df['Residential Type'] = df['Residential Type'].replace('unknown Property', 'unknown type')


# Check for null values
print(df.isnull().sum())

#Get unique sales names 
df['Sales name'].unique()

#Get unique Years 
df['List Year'].unique()

#Get Date Range
# Get the highest and lowest dates in the 'random_date' column
highest_date = df['Date Recorded'].max() #01-10-2024
lowest_date = df['Date Recorded'].min() #01-01-2020


######################################################################


df.to_csv('G:\Real_State_Sales_Datav4.csv', index=False)


#deleteing Rows with null sale amount 
df = df[df['Sales ratio'] != 'null']
# Ensure 'Sale Amount' is a float (just in case)
df['Sale Amount'] = df['Sale Amount'].astype(float)
df['Sales ratio'] = df['Sales ratio'].astype(float)
df['Sales_Commision'] = df['Sales_Commision'].astype(float)


df['Sales_Commision']= df['Sales ratio'] * df['Sale Amount']


df.groupby("Sales name")['Year'].min();

# Group by Sales name, Company, and Year
sales_summary_Per_Sales_Person = df.groupby(['Sales name','company', 'Year'], as_index=False)['Sale Amount'].sum()
# Format sales for better readability
sales_summary_Per_Sales_Person['Sales Amount'] = sales_summary_Per_Sales_Person['Sale Amount'].apply(lambda x: f"{x:,.2f}")
print(sales_summary_Per_Sales_Person)


# Group by Company and Year to calculate total sales
annual_sales_PerCompany = df.groupby(['company', 'Year'])['Sale Amount'].sum().reset_index()
annual_sales_PerCompany['Sale Amount'] = annual_sales_PerCompany['Sale Amount'].apply(lambda x: f"{x:,.2f}")
print(annual_sales_PerCompany)

# Convert 'Sale Amount' to numeric
df['Sale Amount'] = pd.to_numeric(df['Sale Amount'])
print(df.dtypes)

# Group by Sales name, company, and Year to calculate total sales
annual_sales = df.groupby(['Sales name', 'company', 'Year'], as_index=False)['Sale Amount'].sum()
print(annual_sales.dtypes)
# Calculate targets for each salesperson and year
annual_sales['Target'] = annual_sales.groupby(['Sales name', 'company'])['Sale Amount'].shift(1) * 1.05  # Assuming a 5% growth rate
annual_sales['Target'] = annual_sales['Target'].fillna(annual_sales['Sale Amount'])  # First year target equals actual sales
# Rename 'Sale Amount' column to 'Total Sales'
annual_sales.rename(columns={'Sale Amount': 'Total Sales'}, inplace=True)
annual_sales['Total Sales'] = annual_sales['Total Sales'].apply(lambda x: f"{x:,.2f}")
annual_sales['Target'] = annual_sales['Target'].apply(lambda x: f"{x:,.2f}")

print(annual_sales.dtypes)

print(annual_sales)
# Strip any whitespace from column names
annual_sales.columns = annual_sales.columns.str.strip()
# Add a column to indicate if the sales exceeded the target
annual_sales['Performance'] = annual_sales.apply(lambda x: 'Exceeds' if x['Total Sales'] > x['Target'] else 'Not Exceed', axis=1)

print(annual_sales)
annual_sales.to_csv('G:\Performance_Per_Year.csv', index=False)

####################################################
# Count sales per company in each year
sales_count = df.groupby(['Year', 'company']).size().reset_index(name='Sales Count')
print(sales_count)
sales_count.to_csv('G:\Sales_Per Years PEr Company.csv', index=False)


import matplotlib.pyplot as plt
import seaborn as sns

# Sample sales count DataFrame
sales_count = df.groupby(['Year', 'company']).size().reset_index(name='Sales Count')

# Bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=sales_count, x='Year', y='Sales Count', hue='company')
plt.title('Sales Count per Company by Year')
plt.xlabel('Year')
plt.ylabel('Sales Count')
plt.legend(title='Company')
plt.show()




#######################################
#Sales Count Per Sales Person 
sales_count_per_Salesperson = df.groupby(['Year', 'Sales name']).size().reset_index(name='Sales Count')
print(sales_count_per_Salesperson)
sales_count_per_Salesperson.to_csv('G:\Sales_Per Years PEr SalesPerson.csv', index=False)


import matplotlib.pyplot as plt
import seaborn as sns

# Sample sales count DataFrame
sales_count_per_Salesperson = df.groupby(['Year', 'Sales name']).size().reset_index(name='Sales Count')

# Bar plot
plt.figure(figsize=(14, 7))
sns.barplot(data=sales_count_per_Salesperson, x='Year', y='Sales Count', hue='Sales name')
plt.title('Sales Count per Salesperson by Year')
plt.xlabel('Year')
plt.ylabel('Sales Count')
plt.legend(title='Salesperson', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



##################################################33
# Grouping by Town to get count of sales and sum of sale amount
sales_summary = df.groupby('Town').agg(
    Sales_Count=('Sales name', 'count'),  # Count of sales
    Total_Sale_Amount=('Sale Amount', 'sum')  # Sum of sale amounts
).reset_index()

sales_summary['Total_Sale_Amount'] = sales_summary['Total_Sale_Amount'].apply(lambda x: f"{x:,.2f}")

# Display the result
print(sales_summary)

sales_summary.to_csv('G:\Sales Sum and Count Per Town .csv', index=False)


############################################33
# Convert 'Total Sales' and 'Target' to numeric, removing commas if necessary
annual_sales['Total Sales'] = annual_sales['Total Sales'].replace(',', '', regex=True).astype(float)
annual_sales['Target'] = annual_sales['Target'].replace(',', '', regex=True).astype(float)

# Group by Company and Year to find the best performer
best_performers = annual_sales.loc[
    annual_sales.groupby(['company', 'Year'])['Total Sales'].idxmax()
].reset_index(drop=True)
best_performers['Total Sales'] = best_performers['Total Sales'].apply(lambda x: f"{x:,.2f}")

# Display the best performers
print(best_performers)


best_performers.to_csv('G:\Top PErformers.csv', index=False)
