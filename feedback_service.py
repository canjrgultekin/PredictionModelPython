from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

CUSTOMER_SCORES_FILE = "data/customer_scores.json"


# Müşteri skorlarını JSON'dan yükleme fonksiyonu
def load_customer_scores():
    """Müşteri skorlarını yükler"""
    if not os.path.exists(CUSTOMER_SCORES_FILE):
        return {}
    with open(CUSTOMER_SCORES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Yeni müşteri ekleme veya güncelleme fonksiyonu
def update_customer_scores(customer_id, feedback):
    """Geri besleme verisine göre müşteri skorlarını günceller veya yeni müşteri ekler"""
    customer_scores = load_customer_scores()

    customer_id = str(customer_id)  # JSON anahtarları string olmalı

    # Eğer müşteri kayıtlı değilse, yeni müşteri ekle
    if customer_id not in customer_scores:
        customer_scores[customer_id] = {
            "CustomerId": int(customer_id),
            "TotalSpent": 0,
            "UniqueCategories": 0,
            "TopBrand": None,
            "AbandonedCartItems": 0,
            "AvgProductPrice": 0,
            "CustomerScore": 50  # Varsayılan başlangıç skoru
        }

    # Satın alma gerçekleştiyse pozitif geri bildirim
    if feedback == "purchased":
        customer_scores[customer_id]["CustomerScore"] += 5
    elif feedback == "not_purchased":
        customer_scores[customer_id]["CustomerScore"] -= 5  # Yanlış tahmin olursa skoru düşür

    # Güncellenmiş skorları kaydet
    with open(CUSTOMER_SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(customer_scores, file, indent=4, ensure_ascii=False)

    return True


@app.route("/feedback", methods=["POST"])
def receive_feedback():
    """Müşteri tahmin doğruluğunu test eden ve modeli iyileştiren geri besleme endpoint’i"""
    data = request.json
    customer_id = data.get("CustomerId")
    feedback = data.get("Feedback")  # "purchased" veya "not_purchased"

    if not customer_id or feedback not in ["purchased", "not_purchased"]:
        return jsonify({"error": "Eksik veya hatalı veri!"}), 400

    update_customer_scores(customer_id, feedback)

    return jsonify({"message": "Geri bildirim işlendi!", "CustomerId": customer_id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
