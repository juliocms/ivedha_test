import pandas as pd

file_path = "assignment_data.csv"
df = pd.read_csv(file_path)

df["price_per_sqft"] = df["price"] / df["sq__ft"]
average_price_per_sqft = df["price_per_sqft"].mean()

filtered_df = df[df["price_per_sqft"] < average_price_per_sqft]

output_file = "sales_data_filtered.csv"
filtered_df.to_csv(output_file, index=False)

print(f"Arquivo gerado: {output_file}")
