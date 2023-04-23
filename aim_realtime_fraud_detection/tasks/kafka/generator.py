import datetime
from abc import ABC, abstractmethod

from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import time
class KafkaGenerator(ABC):
    """
    Base class to read a dataset, transform it, and save it to a table.
    """
    def __init__(self):
        print("init")
        self.consumer = KafkaConsumer('quickstart-events', 
                                    bootstrap_servers=['localhost:9092'],
                                    auto_offset_reset='earliest',
                                    enable_auto_commit=True,
                                    group_id='my-group',
                                    value_deserializer=lambda x: loads(x.decode('utf-8')))


    def producer(self) -> None:
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        print("Hello")
        for e in range(10):
            data = {'number' : e}
            print(data)
            self.producer.send('quickstart-events', value=json.dumps(data).encode('utf-8'))            
            time.sleep(1)
   

    def consume(self) -> None:
        print("TODO implement cosumer")
    

    
def main() -> None:
    p = KafkaGenerator()    
    p.producer()


if __name__ == "__main__":
    main()

    