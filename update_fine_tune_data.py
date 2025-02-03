import json

CUSTOMER_SCORES_FILE = "data/customer_scores.json"
FINE_TUNE_DATA_FILE = "data/fine_tune_data.jsonl"

def update_fine_tune_data():
    """Müşteri skorları güncellendikçe fine-tune datasetini de günceller."""
    customer_scores = {}

    # Güncellenmiş müşteri skorlarını yükle
    with open(CUSTOMER_SCORES_FILE, "r", encoding="utf-8") as file:
        customer_scores = json.load(file)

    updated_data = []

    # Eski fine-tune verisini yükle
    with open(FINE_TUNE_DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            user_message = data["messages"][1]["content"]

            # Müşteri ID’sini ayıkla
            customer_id = user_message.split(",")[0].split(":")[1].strip()

            if customer_id in customer_scores:
                new_score = customer_scores[customer_id]["CustomerScore"]
                new_assistant_message = f"Bu müşteri {user_message.split(',')[1].strip()} ürününü %{new_score} ihtimalle satın alacak."

                data["messages"][2]["content"] = new_assistant_message
                updated_data.append(data)

    # Güncellenmiş fine-tune datasını kaydet
    with open(FINE_TUNE_DATA_FILE, "w", encoding="utf-8") as file:
        for entry in updated_data:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

    print("✅ Fine-tune dataset müşteri geri bildirimleriyle güncellendi!")

if __name__ == "__main__":
    update_fine_tune_data()
