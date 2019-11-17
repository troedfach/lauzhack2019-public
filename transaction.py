class Transaction:
    def __init__(self, sender, destination, contents, signature, contents_hash, timestamp):
        self.sender = sender
        self.destination = destination
        self.contents = contents
        self.signature = signature
        self.contents_hash = contents_hash
        self.timestamp = timestamp