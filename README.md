# Diwali-Sales-Data-Analysis-and-Predictive-Modeling
Project Title: Diwali Sales Data Analysis and Predictive Modeling
1. Project Overview
This project analyzes sales data from the Diwali festival period to uncover key purchasing trends, customer demographics, and spending patterns. The goal is to derive actionable business insights and build a predictive model to forecast sales amount based on customer and product attributes.
2. Tools & Technologies Used
•	Programming Language: Python
•	Libraries:
o	pandas, numpy: For data manipulation and analysis.
o	matplotlib, seaborn: For creating informative and detailed visualizations.
o	scikit-learn (sklearn): For machine learning (data preprocessing and linear regression modeling).
•	Algorithm: Linear Regression.
3. The Dataset (Diwali Sales Data.csv)
•	The dataset contains 11,251 records of individual sales orders.
•	It includes 15 initial features covering:
o	Customer Demographics: User_ID, Gender, Age Group, Age, Marital_Status, State, Zone.
o	Product Details: Product_ID, Product_Category.
o	Transaction Details: Orders, Amount (Spending), Occupation.
o	Irrelevant Columns: Status and unnamed1 (which were empty and subsequently dropped).
4. Project Steps & Methodology
Phase 1: Data Cleaning and Preprocessing
•	Handling Missing Values: Identified and dropped completely null columns (Status, unnamed1). Filled the 12 missing values in the critical Amount column with the median value.
•	Data Inspection: Used .info() and .isnull().sum() to understand the data structure and ensure cleanliness before analysis.
Phase 2: Exploratory Data Analysis (EDA) and Business Intelligence
The core of the project involves answering key business questions through visualizations:
•	Key Metrics: Calculated and displayed total sales amount, total orders, average order value (AOV), and total unique customers.
•	Sales by Gender: A pie chart revealed that women (F) accounted for ~70% of all sales, a crucial insight for targeted marketing.
•	Sales by Age Group: A bar chart showed that adults aged 26-35 were the highest spending demographic, followed by 36-45 and 18-25. This defines the primary customer base.
•	Sales by Marital Status: Analysis showed that married individuals spent significantly more than single individuals.
•	Sales by Zone: The Central zone was the top-performing sales region.
•	Sales by Occupation: Individuals in IT, Healthcare, and Aviation were the top-spending professions.
•	Product Analysis:
o	Food was the top-selling product category by revenue, followed closely by Clothing & Apparel and Electronics & Gadgets.
o	A separate chart showed the most ordered categories, providing insight into volume vs. value.
Phase 3: Predictive Modeling with Machine Learning
•	Goal: Predict the Amount a customer is likely to spend based on their attributes.
•	Data Preparation:
o	Features (X): Selected Gender, Age Group, Marital_Status, Zone, Occupation, Product_Category, and Orders.
o	Target (y): Amount.
o	Encoding: Used pd.get_dummies() to convert all categorical variables (like Gender, Zone, Occupation) into a numerical format that the Linear Regression model can process.
o	Train-Test Split: Split the data into 90% for training and 10% for testing.
•	Model Building and Training: A Linear Regression model was created and trained on the prepared data.
•	Model Evaluation:
o	Root Mean Squared Error (RMSE): 3,058.99.
o	R-squared (R²) Score: 0.67.
•	Interpretation of Results: The R² score of 0.67 means that 67% of the variance in the sales amount can be explained by the input features (like age, occupation, product category). This is a reasonably good fit for a real-world sales dataset, indicating the model has identified meaningful patterns.
5. Key Findings and Business Implications
1.	Target Audience: The primary customer is a married woman, aged 26-35, living in the Central zone, working in IT, Healthcare, or Aviation.
2.	Product Strategy: The highest revenue comes from Food, Clothing, and Electronics. Marketing and inventory should be prioritized accordingly.
3.	Marketing Strategy: Campaigns should be heavily targeted towards women and the 26-45 age bracket. Partnerships with companies in the top-spending occupational sectors could be highly effective.
4.	Predictive Power: The company can now build a system to predict a customer's potential spending based on their profile, which can be used for personalized discounts, product recommendations, and customer segmentation.
6. Conclusion
This project successfully transformed raw sales data into a strategic asset. The comprehensive EDA provided a clear picture of who is buying what and where, enabling data-driven decision-making for marketing, sales, and inventory management. The predictive model, while not perfect, provides a strong, explainable foundation for forecasting customer value, demonstrating the powerful synergy between data analysis and machine learning in a business context.

