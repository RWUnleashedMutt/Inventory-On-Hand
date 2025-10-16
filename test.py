# Import the pandas library, which is essential for data manipulation and is conventionally aliased as 'pd'.
import pandas as pd

# --- 1. Load DataFrames and Create Initial SKU Lists ---

# Load the main product list into a DataFrame called DF.
# This likely contains all products relevant to the current operation.
DF = pd.read_excel(
    './product_export_list_10152025_150926.xlsx')

# Load the special list of holiday products into a DataFrame called HOL_DF.
HOL_DF = pd.read_excel('./holiday_product_export_list.xlsx')

# Extract the 'SKU' (Stock Keeping Unit) column from the holiday products DataFrame
# and convert it into a Python list. This list will be used for exclusion later.
HOL_SKU_LIST = HOL_DF['SKU'].to_list()

# Extract the 'SKU' column from the main products DataFrame (DF)
# and convert it into a Python list. This list will be used for initial filtering.
SKU_LIST = DF['SKU'].to_list()


# Load the inventory on-hand data into a DataFrame called OH_DF.
# This DataFrame contains the raw inventory data, including SKUs, locations, and quantities.
OH_DF = pd.read_excel(
    './Inventory On Hand by Location (xls)_10152025_150528.xlsx')

# --- 2. Initial Filtering (Products MUST be in the Main List) ---

# Filter the raw inventory DataFrame (OH_DF) to only include rows
# where the 'SKU' is present in the main product list (SKU_LIST).
# This creates a subset of inventory that is relevant to the product list DF.
filtered_df = OH_DF[OH_DF['SKU'].isin(SKU_LIST)]

# --- 3. First Exclusion: Removing Holiday Products ---

# Create a boolean mask to identify rows that should be EXCLUDED (holiday products).
# This returns True for any row where the 'SKU' is found in the HOL_SKU_LIST.
mask_to_exclude = filtered_df['SKU'].isin(HOL_SKU_LIST)

# Invert the mask using the logical NOT operator (~).
# This flips the True/False values, so True now identifies rows to KEEP
# (i.e., non-holiday products).
mask_to_keep = ~mask_to_exclude

# Apply the inverted mask to 'filtered_df' to remove all holiday products.
# The result is stored in 'final_filter_df'.
final_filter_df = filtered_df[mask_to_keep]

# The following line is commented out, but it would save the result of the first filter to an Excel file.
# final_filter_df.to_excel('./t.xlsx', index=False)

# --- 4. Second Exclusion: Removing Specific Sub-Categories (e.g., Food) ---

# Define a list of 'Sub-Category' names that should also be removed.
food_list = ['Dog Food', 'Cat Food']

# Create a new mask to identify rows that should be EXCLUDED (food items).
# This returns True for any row where the 'Sub-Category' is in the 'food_list'.
mask_to_exclude = final_filter_df['Sub-Category'].isin(food_list)

# Invert the mask again. True now identifies rows to KEEP (i.e., non-food items).
mask_to_keep = ~mask_to_exclude

# Apply the inverted mask to remove the specified food items from 'final_filter_df'.
# The final, fully filtered DataFrame is stored in 'f_df'.
f_df = final_filter_df[mask_to_keep]

# --- 5. Final Output ---

# Export the final filtered DataFrame (f_df) to a new Excel file named 't.xlsx'.
# index=False prevents pandas from writing the DataFrame's internal row numbers (index) to the file.
f_df.to_excel('./t.xlsx', index=False)
