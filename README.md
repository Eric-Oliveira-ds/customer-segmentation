customer-segmentation
==============================

Develop a customer segmentation to define the best marketing strategy

- [**Streamlit web app**]()


- **Business problem:**

    One of the crux of the marketing industry is getting to know customers and understanding their needs. By understanding consumers we can send specific campaigns for specific needs. If we have data about customers we can apply data science to segment the market. And that's why I was hired by a bank in New York to analyze the data and divide customers into groups to boost the marketing team's decision-making when defining campaigns at the bank.

- **Following is the Data Dictionary for Credit Card dataset :**

    CUST_ID : Identification of Credit Card holder (Categorical)

    BALANCE : Balance amount left in their account to make purchases 

    BALANCE_FREQUENCY : How frequently the Balance is updated, score between 0 and 1 (1 = frequently updated, 0 = not frequently updated)

    PURCHASES : Amount of purchases made from account

    ONEOFF_PURCHASES : Maximum purchase amount done in one-go

    INSTALLMENTS_PURCHASES : Amount of purchase done in installment

    CASH_ADVANCE : Cash in advance given by the user

    PURCHASES_FREQUENCY : How frequently the Purchases are being made, score between 0 and 1 (1 = frequently purchased, 0 = not frequently purchased)

    ONEOFFPURCHASESFREQUENCY : How frequently Purchases are happening in one-go (1 = frequently purchased, 0 = not frequently purchased)

    PURCHASESINSTALLMENTSFREQUENCY : How frequently purchases in installments are being done (1 = frequently done, 0 = not frequently done)

    CASHADVANCEFREQUENCY : How frequently the cash in advance being paid

    CASHADVANCETRX : Number of Transactions made with "Cash in Advanced"

    PURCHASES_TRX : Numbe of purchase transactions made

    CREDIT_LIMIT : Limit of Credit Card for user

    PAYMENTS : Amount of Payment done by user

    MINIMUM_PAYMENTS : Minimum amount of payments made by user

    PRCFULLPAYMENT : Percent of full payment paid by user

    TENURE : Tenure of credit card service for user

- **Data prep:**

    Repair missing data with zero.

- **Modeling:**

    Using KMeans with standardized data and PCA in pipeline for make training and predict clusters data.

- **Evaluate:**

    Using mlflow for tracking experiments and evaluate model with sillhute score. The score is bad now but the algorthem predict four cluster. I make a segmenatiom with this four cluster predicted and add into Streamlit a dashboard with analytical vizualizations and table for user best decision make.

- **Solution:**

    A web app was created that enhances the decision making of the marketing team through interactive analysis of data and grouping of vip, plus, mid and low customers, thus creating strategies and personalized products for customers.


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
