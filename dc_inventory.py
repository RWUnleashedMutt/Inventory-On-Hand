import pandas as pd  # Import the pandas library, commonly used for data manipulation

# 1. Load DataFrames
# Read the main inventory-on-hand data by location from an Excel file.
# This is the starting dataset that will be filtered.
INVENTORY_ON_HAND_LOC_DF = pd.read_excel(
    './Inventory On Hand by Location (xls)_10152025_150528.xlsx')

# Read a list of holiday products (presumably containing SKUs for special items).
HOLIDAY_PRODUCT_DF = pd.read_excel('./holiday_product_export_list.xlsx')

# Read a general list of products relevant to a Distribution Center (DC).
DC_PRODUCT_DF = pd.read_excel(
    './product_export_list_10152025_150926.xlsx')

# 2. Extract SKU Lists
# Convert the 'SKU' column from the holiday product DataFrame into a Python list.
HOLIDAY_SKU_LIST = HOLIDAY_PRODUCT_DF['SKU'].to_list()

# Convert the 'SKU' column from the DC product DataFrame into a Python list.
DC_PRODUCT_SKU_LIST = DC_PRODUCT_DF['SKU'].to_list()

# 3. Initial Filtering (DC Products)
# Filter the main inventory DataFrame (INVENTORY_ON_HAND_LOC_DF)
# to only include rows where the 'SKU' is present in the DC product list (DC_PRODUCT_SKU_LIST).
# This limits the inventory to products relevant to the Distribution Center.
DC_PRODUCT_FILTERED_DF = INVENTORY_ON_HAND_LOC_DF[INVENTORY_ON_HAND_LOC_DF['SKU'].isin(
    DC_PRODUCT_SKU_LIST)]

# 4. Filter Out Holiday Products
# Create a boolean mask to identify rows (SKUs) in the DC-filtered inventory
# that are *also* in the holiday product list. These are the rows to be excluded.
MASK_TO_EXCLUDE = DC_PRODUCT_FILTERED_DF['SKU'].isin(HOLIDAY_SKU_LIST)

# Invert the exclusion mask to create a mask for the rows to be *kept* (i.e., non-holiday items).
MASK_TO_KEEP = ~MASK_TO_EXCLUDE

# Apply the inverted mask to the DC-filtered DataFrame.
# This results in an inventory list that contains DC products *excluding* holiday products.
HOLIDAY_FILTERED_DF = DC_PRODUCT_FILTERED_DF[MASK_TO_KEEP]

# 5. Filter Out Food Products
# Define a list of sub-categories to be excluded (Dog Food, Cat Food).
FOOD_LIST = ['Dog Food', 'Cat Food']

# Create a boolean mask to identify rows (products) in the current filtered inventory
# where the 'Sub-Category' is in the defined food list. These are the rows to be excluded.
MASK_TO_EXCLUDE = HOLIDAY_FILTERED_DF['Sub-Category'].isin(FOOD_LIST)

# Invert the food exclusion mask to create a mask for the rows to be *kept* (i.e., non-food items).
MASK_TO_KEEP = ~MASK_TO_EXCLUDE

# Apply the inverted mask to the holiday-filtered DataFrame.
# This results in the final inventory list, which excludes holiday and food items.
FINAL_FILTERED_DF = HOLIDAY_FILTERED_DF[MASK_TO_KEEP]

# 6. Export Final Data
# Write the resulting final filtered DataFrame to a new Excel file.
# 'index=False' prevents the pandas DataFrame index from being written as a column in the Excel file.
FINAL_FILTERED_DF.to_excel('./dc_inventory_filtered.xlsx', index=False)
