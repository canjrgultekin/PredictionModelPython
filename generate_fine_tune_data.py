import json
import pandas as pd
from fetch_data import fetch_data, PAST_PURCHASES_QUERY, PAST_CART_ADDS_QUERY


def generate_fine_tune_data():
    """Gerçek müşteri verilerini GPT fine-tune formatına çevirir ve .jsonl olarak kaydeder"""

    purchases = fetch_data(PAST_PURCHASES_QUERY)
    carts = fetch_data(PAST_CART_ADDS_QUERY)

    fine_tune_data = []

    for _, row in purchases.iterrows():
        user_message = f"Müşteri ID: {row['CustomerId']}, Ürün: {row['ProductName']}, Marka: {row['ProductBrand']}, " \
                       f"Kategori: {row['ProductCategory']}, Adet: {row['ProductQuantity']}, Fiyat: {row['ProductPrice']} TL"

        # Satın alma oranını belirleme (Geçmiş satın alımlara göre)
        possibility = 90 if row["ProductQuantity"] > 1 else 75

        assistant_message = f"Bu müşteri {row['ProductName']} ürününü %{possibility} ihtimalle satın alacak."

        fine_tune_data.append({
            "messages": [
                {"role": "system",
                 "content": "Bu model, müşteri alışveriş verilerini kullanarak sepetindeki her ürün için satın alma tahminleri yapar."},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message}
            ]
        })

    for _, row in carts.iterrows():
        user_message = f"Müşteri ID: {row['CustomerId']}, Ürün: {row['ProductName']}, Marka: {row['ProductBrand']}, " \
                       f"Kategori: {row['ProductCategory']}, Adet: {row['ProductQuantity']}, Fiyat: {row['ProductPrice']} TL"

        # Sepete ekleyip satın almadıysa düşük ihtimal
        assistant_message = f"Bu müşteri {row['ProductName']} ürününü %30 ihtimalle satın alacak."

        fine_tune_data.append({
            "messages": [
                {"role": "system",
                 "content": "Bu model, müşteri alışveriş verilerini kullanarak sepetindeki her ürün için satın alma tahminleri yapar."},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message}
            ]
        })

    # JSONL formatında kaydet
    with open("data/fine_tune_data.jsonl", "w", encoding="utf-8") as jsonl_file:
        for entry in fine_tune_data:
            jsonl_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print("✅ Fine-tune dataset GERÇEK verilerle oluşturuldu: data/fine_tune_data.jsonl")


if __name__ == "__main__":
    generate_fine_tune_data()
