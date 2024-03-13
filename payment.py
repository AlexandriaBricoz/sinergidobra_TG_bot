import time
import uuid
import traceback

from yookassa import Configuration, Payment

# Установка настроек
Configuration.account_id = "334322"
Configuration.secret_key = "live__yJu0OWX0jep-Fqn02RKSIQR98BTZTBHpsLOwiyVNZw"


def create_payment(amount, description, return_url):
    # Создание платежа
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "sbp",
        },
        "confirmation": {
            "type": "redirectembedded",
            "locale": "ru_RU"
        },
        "description": "Заказ №72"
    }, idempotence_key)
    return payment


def check_payment_status(payment_id):
    while True:
        payment = Payment.find_one(payment_id)
        status = payment.status
        print("Current status:", status)
        if status in ["succeeded", "canceled"]:
            break
        time.sleep(5)  # Пауза между запросами, можно увеличить или уменьшить

    if status == "succeeded":
        print("Payment successful!")
    else:
        print("Payment canceled or failed.")


# Пример использования
def main():
    amount = "2.00"
    description = "Заказ №1"
    return_url = "https://vk.com/al_im.php?sel=381001074"
    try:
        payment = create_payment(amount, description, return_url)
        print("Payment created with ID:", payment.id)
        print(payment)
        check_payment_status(payment.id)
    except Exception as e:
        traceback.print_exception(e)


if __name__ == "__main__":
    main()
