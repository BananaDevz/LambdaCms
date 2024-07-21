import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

# Configurações do teste
url = 'http://127.0.0.1:8000/api/posts/'
headers = {'Content-Type': 'application/json'}
total_requests = 30000  # Número total de requisições
concurrent_requests = 10  # Número de requisições concorrentes

# Função para criar um payload único
def create_payload(index):
    return {
        'title': f'My Title {index}',
        'content': f'Some content {index}',
        'tags': f'tag{index % 5},tag{(index + 1) % 5}'
    }

def send_request(session, payload):
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Levanta um erro para status de resposta 4xx/5xx
        return (True, response.status_code)
    except requests.RequestException as e:
        return (False, str(e))

def stress_test():
    start_time = time.time()
    failed_requests = 0
    failed_details = []
    
    # Cria uma lista de payloads únicos
    payloads = [create_payload(i) for i in range(total_requests)]

    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        with requests.Session() as session:
            futures = [executor.submit(send_request, session, payloads[i]) for i in range(total_requests)]

            for future in as_completed(futures):
                success, status = future.result()
                if not success:
                    failed_requests += 1
                    failed_details.append(status)

    elapsed_time = time.time() - start_time
    print(f"Total requests made: {total_requests}")
    print(f"Total failed requests: {failed_requests}")
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    if failed_requests > 0:
        print("Failure details:")
        for detail in failed_details:
            print(detail)

if __name__ == "__main__":
    stress_test()
