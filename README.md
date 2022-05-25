# Point of Sale Dashboard

## Introduction

This project is as part of the requirements for Programming Essentials Masters coursework at NTU.

## Analysis Goals

1) Compare Financial Metrics By Year
Provide users with an overview over the entire business performance over time.
Why: Business performance metrics are important for management to obtain a helicopter view over the business that they
are managing. Using these performance metrics, management can decide on business strategies going forward.

2) Compare Product Performance
Provide users the ability to explore specific SKU/ProductID and their payment terms.
Why: As the business in question is a trading business, choosing the right products and upselling products is important.
Management must understand which products are most popular over time and which have faded in popularity. This allows
them to make decisions on inventory and product substitution.

3) Compare Customer Buying Behavior
Provide users the ability to explore customer buying behaviour, which customers are recurring vs once off and which have
an increasing requirement for more stock.
Why: Management must have an idea which customers to invest into. A growing customer can be provided with (but not
limited to) priority access to new stock, delivery timeframes, favourable credit terms. This the business to work with
growing partners and thus increase organic sales.

## Deployment

Python 3.7 or later is required for deployment

```bash
conda create -n pos-dashboard python=3.7
conda activate pos-dashboard
```

Install packages by

```bash
pip install -r requirements.txt
```

To directly deploy the interface

```bash
python -m flask run
```

## Insights from Data

1) Among the financial metrics available, the yearly profit is highly correlated to the yearly amount of quantity sold.
While it might be easy for management to surmise that to increase profit they must increase volume of trading, I would
like to offer an alternative insight. Taking the year 2018 as an example, 2018 was a record profitable year for the
company. However, the company also had to move 20% more products to achieve only a 6% increase in profit vs the previous
year. The company would be better off focusing on products that have higher margin rather than to increase sales volume.

2) Cash on delivery customers only form a small fraction (<4%) of the overall sales for the business. Depending on the
terms of credit provided and bad debt accrued, A high number of customers on credit may pose a risk to the business.
As business would be quite affected if a slowdown occurs and customers are unable to make payments on time.
Management should review the list of customers who are on overly generous payment terms and tighten credit control.

3) Assuming customer prefix was grouped together by business relationships (i.e. subsidiaries of business provided with
the same starting prefix). The top 20 customers make up 80% of overall profit over the past 11 years.
Similarly, the top 2% of products sold accounted for ~50% of the overall profit of the business over the past 11 years.
As we have no idea of network effects of holding so many inventory items, perhaps management can do a study on which
items are more sought after by their customer and rationalize number of inventory item types.
