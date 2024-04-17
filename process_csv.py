import pandas as pd

def process_csv(file_path):
    # Load the CSV file using the correct delimiter
    data = pd.read_csv(file_path, delimiter=';')
    
    # Filter records
    filtered_data = data[(data['is_buybox'] == False) & (data['status'] == 'Online')]
    
    # Create a new dataframe with the specified logic
    new_data = pd.DataFrame({
        'product_id': filtered_data['product_uuid'],
        'listing_id': filtered_data['listing_id'],
        'market': 'fr-fr',
        'price': filtered_data['buybox_price'],
        'sku': filtered_data['sku'].where(pd.notnull(filtered_data['sku']), None),
        'grade_code': filtered_data['grade_code']
    })
    
    # Save the new dataframe to a new CSV file
    new_file_path = file_path.replace('.csv', '_processed.csv')
    new_data.to_csv(new_file_path, index=False)
    print(f"Processed file saved as {new_file_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        process_csv(file_path)
    else:
        print("Please provide a file path.")