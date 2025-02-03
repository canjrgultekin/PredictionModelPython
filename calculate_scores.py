import pandas as pd
import json
from fetch_data import fetch_data, PAST_PURCHASES_QUERY, PAST_CART_ADDS_QUERY

def calculate_customer_scores():
    """Müşteri skorlarını hesaplar ve JSON olarak kaydeder"""
    purchases = fetch_data(PAST_PURCHASES_QUERY)
    carts = fetch_data(PAST_CART_ADDS_QUERY)

    # Tüm müşteri ID'lerini al ve int türüne çevir
    customer_ids = set(purchases["CustomerId"].astype(int).unique()).union(
        set(carts["CustomerId"].astype(int).unique())
    )

    customer_scores = {}

    for customer_id in customer_ids:
        # Müşterinin geçmiş satın almaları
        past_purchases = purchases[purchases["CustomerId"] == customer_id]
        past_carts = carts[carts["CustomerId"] == customer_id]

        # Müşterinin toplam harcaması
        total_spent = past_purchases["ProductPrice"].sum()

        # Müşterinin kaç farklı ürün kategorisinden alışveriş yaptığı
        unique_categories = past_purchases["ProductCategory"].nunique()

        # En çok tercih edilen marka
        if not past_purchases.empty:
            top_brand = past_purchases["ProductBrand"].mode()[0]  # En çok tekrar eden marka
        else:
            top_brand = None

        # Sepete ekleyip satın almadığı ürün sayısı
        abandoned_cart_items = past_carts.shape[0]

        # Ortalama ürün fiyatı
        avg_product_price = past_purchases["ProductPrice"].mean()

        # Müşteri skoru hesaplama (Özel bir formül)
        score = (
            (total_spent * 0.4) +            # Toplam harcamanın %40 ağırlığı
            (unique_categories * 10) +       # Kaç farklı kategoriden alışveriş yaptığı (10x çarpan)
            (abandoned_cart_items * -5) +    # Sepete ekleyip almadıkları -5 puan etkisi
            (avg_product_price * 0.2)        # Ortalama ürün fiyatının %20 etkisi
        )

        customer_scores[str(customer_id)] = {  # Anahtarları string formatına çeviriyoruz
            "CustomerId": int(customer_id),  # int64'ü normal int'e çevir
            "TotalSpent": round(total_spent, 2),
            "UniqueCategories": unique_categories,
            "TopBrand": top_brand,
            "AbandonedCartItems": abandoned_cart_items,
            "AvgProductPrice": round(avg_product_price, 2) if not pd.isna(avg_product_price) else 0,
            "CustomerScore": round(score, 2)
        }

    # JSON olarak kaydet
    with open("data/customer_scores.json", "w", encoding="utf-8") as json_file:
        json.dump(customer_scores, json_file, indent=4, ensure_ascii=False)

    print("✅ CustomerScores başarıyla hesaplandı ve kaydedildi!")

if __name__ == "__main__":
    calculate_customer_scores()
