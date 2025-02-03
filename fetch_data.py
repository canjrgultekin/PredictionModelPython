import pandas as pd
from db_config import get_db_connection

def fetch_data(query):
    """PostgreSQL veritabanından verilen SQL sorgusuna göre veri çeker"""
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None

# Müşteri geçmiş satın alma sorgusu
PAST_PURCHASES_QUERY = """
SELECT 
    x1."Id" AS "CustomerId",
    x2."Name" AS "ProductName",
    x2."Brand" AS "ProductBrand",
    x2."Category" AS "ProductCategory",
    x2."Quantity" AS "ProductQuantity",
    x2."Price" AS "ProductPrice",
    x3."CartTotal" as "OrderAmount",
    x3."CompletedDate" as "OrderDate"
FROM public."AppCustomers" x1 
LEFT JOIN public."AppSessionProducts" x2 ON x1."Id" = x2."CustomerId"
LEFT JOIN public."AppSessions" x3 ON x2."SessionId" = x3."Id"
WHERE x3."ExternalOrderId" IS NOT NULL 
  AND x3."ExternalOrderId" != ''
  AND x2."Category" IS NOT NULL 
  AND x2."Category" != '';
"""

# Sepete eklenen ancak satın alınmayan ürünler
PAST_CART_ADDS_QUERY = """
SELECT 
    x1."Id" AS "CustomerId",
    x2."Name" AS "ProductName",
    x2."Brand" AS "ProductBrand",
    x2."Category" AS "ProductCategory",
    x2."Quantity" AS "ProductQuantity",
    x2."Price" AS "ProductPrice",
    x3."SendAt" AS "AddToCartDate"
FROM public."AppCustomers" x1 
LEFT JOIN public."AppEventProducts" x2 ON x1."Id" = x2."CustomerId"
LEFT JOIN public."AppEvents" x3 ON x2."SessionId" = x3."SessionId"
LEFT JOIN public."AppSessions" x4 ON x2."SessionId" = x4."Id"
WHERE x3."Type" IN ('checkout','add_to_cart')
  AND x2."Category" IS NOT NULL 
  AND x2."Category" != ''
  AND x4."IsCompleted" = false;
"""

if __name__ == "__main__":
    purchases = fetch_data(PAST_PURCHASES_QUERY)
    carts = fetch_data(PAST_CART_ADDS_QUERY)

    print("📌 Müşteri Geçmiş Satın Alma Verileri:")
    print(purchases.head())

    print("\n📌 Sepete Eklenen Ancak Satın Alınmayan Ürünler:")
    print(carts.head())
