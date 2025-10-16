import pandas as pd

INVENTORY_ON_HAND_LOC_DF = pd.read_excel(
    './Inventory On Hand by Location (xls)_10152025_150528.xlsx')

HOLIDAY_PRODUCT_DF = pd.read_excel('./holiday_product_export_list.xlsx')

DC_PRODUCT_DF = pd.read_excel(
    './product_export_list_10152025_150926.xlsx')

HOLIDAY_SKU_LIST = HOLIDAY_PRODUCT_DF['SKU'].to_list()

DC_PRODUCT_SKU_LIST = DC_PRODUCT_DF['SKU'].to_list()

DC_PRODUCT_FILTERED_DF = INVENTORY_ON_HAND_LOC_DF[INVENTORY_ON_HAND_LOC_DF['SKU'].isin(
    DC_PRODUCT_SKU_LIST)]

MASK_TO_EXCLUDE = DC_PRODUCT_FILTERED_DF['SKU'].isin(HOLIDAY_SKU_LIST)

MASK_TO_KEEP = ~MASK_TO_EXCLUDE

HOLIDAY_FILTERED_DF = DC_PRODUCT_FILTERED_DF[MASK_TO_KEEP]

FOOD_LIST = ['Dog Food', 'Cat Food']

MASK_TO_EXCLUDE = HOLIDAY_FILTERED_DF['Sub-Category'].isin(FOOD_LIST)

MASK_TO_KEEP = ~MASK_TO_EXCLUDE

FINAL_FILTERED_DF = HOLIDAY_FILTERED_DF[MASK_TO_KEEP]

FINAL_FILTERED_DF.to_excel('./dc_inventory_filtered.xlsx', index=False)
