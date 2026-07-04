"Useful when you want simple probabilistic distribution"

import random

class RandomBalancer:
       def __init__(self, servers):
               self.servers = servers

       def select_servers(self):
               return random.choice(self.servers)

lb = RandomBalancer(["A", "B", "C"])

for i in range(10):
       print("Request {i  1} -> Server {lb.select_server()}")
