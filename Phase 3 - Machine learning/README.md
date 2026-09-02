# Profit Prediction Model

This project uses machine learning to predict the **Profit** of a sold product. The data comes from a sales database with several related tables (products, customers, geography, shipping, and dates). The notebook combines these tables, prepares the data, trains three different models, and selects the best one.

## Goal

The main goal is to build a model that can estimate profit based on order information. This kind of model can help a company understand which factors affect profit and plan better business decisions.

## Data Files

The notebook uses the following files:

| File | Description |
|------|-------------|
| `FactSales.csv` | Main sales table. Contains sales amount, quantity, discount, shipping cost, and profit for each order line. |
| `DimProduct.csv` | Product details, including category and sub-category. |
| `DimCustomer.csv` | Customer details, including customer segment. |
| `DimGeography.csv` | Location details, including region and market. |
| `DimShipMode.csv` | Shipping method used for each order. |
| `DimOrderPriority.csv` | Priority level of each order. |
| `DimDate.csv` | Calendar table used to extract month, weekday, and season. |

All files are joined together with `pandas` into one table before training.

## Steps in the Notebook

1. **Load the data**
   All CSV files are read with `pandas`.

2. **Join the tables**
   The main sales table is merged with the other tables using their key columns (for example, `ProductKey`, `CustomerKey`). Only useful columns are kept from each table.

3. **Select features**
   Columns with too many unique values (like product name or customer name) are removed, because they do not help the model generalize well. Instead, category-level columns are kept, such as:
   - Category, Sub-Category
   - Segment
   - Region, Market
   - Ship Mode
   - Order Priority
   - Season, Month, Day of Week

   Numeric columns are also kept, such as Sales, Quantity, Discount, Shipping Cost, and Delivery Days.

4. **Split the data**
   The data is split into a training set (80%) and a test set (20%). The model learns from the training set and is evaluated on the test set, which it has never seen before.

5. **Preprocess the data**
   - Categorical columns are converted into numbers using **One-Hot Encoding**.
   - Numeric columns are standardized using **StandardScaler**.

6. **Train three models**
   Three different regression models are trained and tuned using **GridSearchCV**, which tests several parameter combinations and picks the best one for each model:
   - **Ridge Regression** – a simple linear model
   - **Random Forest** – an ensemble of decision trees
   - **Gradient Boosting** – another ensemble method that builds trees step by step

7. **Compare the models**
   Each model is evaluated on both the training set and the test set. The notebook shows:
   - **Train R²** – how well the model fits the training data
   - **Test R²** – how well the model performs on new, unseen data
   - **Overfitting gap** – the difference between Train R² and Test R²

   A large gap between Train R² and Test R² usually means the model is **overfitting**: it memorized the training data instead of learning general patterns.

8. **Select the best model**
   The model with the highest **Test R²** is chosen as the final model, because test performance shows how well the model will work on new data.

9. **Visualize the results**
   A scatter plot compares the predicted profit values with the actual profit values from the test set. Points close to the diagonal line mean better predictions.

## Result

In the last run, **Gradient Boosting** performed best, with a Test R² of about **0.73**. This means the model can explain roughly 73% of the variation in profit using the available features. The gap between train and test performance was small, which shows the model generalizes reasonably well and is not strongly overfitting.

## How to Use This Notebook

1. Make sure all the data files are in the same folder as the notebook (or update the `DATA_DIR` path in the code).
2. Install the required libraries if needed:
   ```
   pip install pandas numpy scikit-learn matplotlib
   ```
3. Run the notebook cells in order, from top to bottom.
4. Check the comparison table and the final plot to see the model's performance.

## Notes

- The random seed is fixed (`random_state=42`), so the results should be the same every time you run the notebook.
- You can change the parameter grids in the `model_grid` dictionary to try more combinations, but this will make the training take longer.
