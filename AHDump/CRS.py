import os

class Config:

    def __init__(self):
        self.token_client_id = os.environ['client_id']
        self.token_secret = os.environ['secret']
        
class CRS:
    def __init__(self):
        self.cfg = Config()
