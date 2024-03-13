data = {
    "type": 'payment',
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    'test': True,
"receipt": {
            "customer": {
                "full_name": "Ivanov Ivan Ivanovich",
                "email": "email@email.ru",
                "phone": "79211234567",
                "inn": "6321341814"
            },
            "items": [
                {
                    "description": "Переносное зарядное устройство Хувей",
                    "quantity": "1.00",
                    "amount": {
                        "value": 1000,
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "country_of_origin_code": "CN",
                    "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                    "customs_declaration_number": "10714040/140917/0090376",
                    "excise": "20.00",
                    "supplier": {
                        "name": "string",
                        "phone": "string",
                        "inn": "string"
                    }
                },
            ]
        },
    "description": "Order No. 1"
}
headers = {
    'Idempotence-Key': '123112123231'
}
r = requests.post('https://api.yookassa.ru/v3/payments', json=data, headers=headers, auth=('334322', 'live__yJu0OWX0jep-Fqn02RKSIQR98BTZTBHpsLOwiyVNZw'))
print(r.json())