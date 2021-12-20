# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("TEST-6122793014650444-073119-089578ba621636d1686acded8b84cff8-233007992")

def create_mercadopago_items(item_array):
    formated_data = {
        "items": item_array
    }

    try:
        preference_response = sdk.preference().create(formated_data)
        preference = preference_response["response"]
        return preference

    except AssertionError as error:
        print(error)