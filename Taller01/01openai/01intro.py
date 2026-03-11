from openai import OpenAI
import getpass

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = getpass.getpass("Ingresa tu API Key de OpenAI : ")
)

model = "gpt-4.1-mini" #gpt-4"

# Define el mensaje de entrada para el chat
prompt = "quién es Leonel Messi"
message_input = {
    'messages': [
        {'role': 'system', 'content': 'Eres un asistente virtual'},
        {'role': 'user', 'content': prompt}
    ]
}

# Realiza una solicitud a la API de OpenAI
response = client.chat.completions.create(
    model = model,
    messages = message_input['messages'],
    temperature = 0, #Si está más cercano a 1, es posible que tenga alucinaciones.
    n = 1, #Número de respuestas
    max_tokens = 100
)

# Imprime la respuesta del modelo
result = response.choices[0].message.content
print(result)