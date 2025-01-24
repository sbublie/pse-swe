from tasks import order_from_china, order_from_korea

if __name__ == '__main__':
    # Task asynchron starten
    response_korea = order_from_korea.delay("chair", 20)
    response_china = order_from_china.delay("table", 20)
    print(f"Order send to Korea. Task-ID: {response_korea.id}")
    print(f"Order send to China. Task-ID: {response_china.id}")

    # Ergebnis abfragen
    
    print(f"Response from Korea: {response_korea.get(timeout=15)}")
    print(f"Response from China: {response_china.get(timeout=15)}")
