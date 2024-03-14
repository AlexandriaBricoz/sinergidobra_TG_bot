import time
import traceback
import uuid

from yookassa import Configuration, Payment


def create_payment(full_name, amount, description):
    Configuration.account_id = "334322"
    Configuration.secret_key = "live__yJu0OWX0jep-Fqn02RKSIQR98BTZTBHpsLOwiyVNZw"
    # Создание платежа
    idempotence_key = str(uuid.uuid4())
    data = {
        "type": 'payment',
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Luba_helper_bot"
        },
        "capture": True,
        "receipt": {
            "customer": {
                "full_name": full_name,
                "email": "email@email.ru",
                "phone": "79211234567",
            },
            "items": [
                {
                    "description": description,
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": "2",

                },
            ]
        },
        "description": description
    }
    payment = Payment.create(data, idempotence_key)
    return payment


def check_payment_status(payment_id):
    Configuration.account_id = "334322"
    Configuration.secret_key = "live__yJu0OWX0jep-Fqn02RKSIQR98BTZTBHpsLOwiyVNZw"
    payment = Payment.find_one(payment_id)
    status = payment.status

    if status == "succeeded":
        return True
    else:
        return False


# Пример использования
def main():
    full_name = "Ivanov Ivan Ivanovich"
    amount = 2.00
    description = "Заказ №1"
    try:
        payment = create_payment(full_name, amount, description)
        print("Payment created with ID:", payment.id)
        print(payment.confirmation.confirmation_url)
        check_payment_status(payment.id)
    except Exception as e:
        traceback.print_exception(e)


if __name__ == "__main__":
    main()
