import json

import pandas

from fetch_data import fetch_data, PAST_PURCHASES_QUERY, PAST_CART_ADDS_QUERY

def convert_to_json():
    """PostgreSQL’den gelen verileri JSON formatına dönüştür ve kaydet"""
    purchases = fetch_data(PAST_PURCHASES_QUERY)
    carts = fetch_data(PAST_CART_ADDS_QUERY)

    dataset = []

    for _, row in purchases.iterrows():
        dataset.append({
            "CustomerId": row["CustomerId"],
            "PastPurchases": [
                {
                    "ProductName": row["ProductName"],
                    "ProductBrand": row["ProductBrand"],
                    "ProductCategory": row["ProductCategory"],
                    "ProductQuantity": row["ProductQuantity"],
                    "ProductPrice": row["ProductPrice"],
                    "OrderDate": row["OrderDate"].isoformat() if pandas.notna(row["OrderDate"]) else None
                }
            ]
        })

    for _, row in carts.iterrows():
        dataset.append({
            "CustomerId": row["CustomerId"],
            "PastCartAdds": [
                {
                    "ProductName": row["ProductName"],
                    "ProductBrand": row["ProductBrand"],
                    "ProductCategory": row["ProductCategory"],
                    "ProductQuantity": row["ProductQuantity"],
                    "ProductPrice": row["ProductPrice"],
                    "AddToCartDate": row["AddToCartDate"].isoformat() if pandas.notna(row["AddToCartDate"]) else None
                }
            ]
        })

    with open("data/train_data.json", "w", encoding="utf-8") as json_file:
        json.dump(dataset, json_file, indent=4, ensure_ascii=False)

    print("✅ JSON formatında veri başarıyla kaydedildi!")

if __name__ == "__main__":
    convert_to_json()
