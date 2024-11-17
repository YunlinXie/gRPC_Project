import grpc
import banks_pb2
import banks_pb2_grpc
import time

class Customer:
    def __init__(self, id, events):
        # Initialize customer with ID and list of events to perform
        self.id = id
        self.events = events
        self.recvMsg = list() # Store responses from branch
        self.stub = None # gRPC stub to communicate with branch

    
    def createStub(self):
        # Connect to the branch with the corresponding customer ID on port 50050 + id
        branch_address = f'localhost:{50050 + self.id}'
        channel = grpc.insecure_channel(branch_address)
        self.stub = banks_pb2_grpc.BankStub(channel)

   
    def executeEvents(self):
        # Sequentially process each event for this customer
        for event in self.events:
            if event["interface"] == "deposit":
                # Send a deposit request to the branch server
                response = self.stub.MsgDelivery(
                    banks_pb2.TransactionRequest(
                        customer_id=self.id,
                        operation="deposit",
                        amount=event["money"]
                    )
                )
                self.recvMsg.append({"interface": "deposit", "result": response.status})

            elif event["interface"] == "withdraw":
                # Send a withdraw request to the branch server
                response = self.stub.MsgDelivery(
                    banks_pb2.TransactionRequest(
                        customer_id=self.id,
                        operation="withdraw",
                        amount=event["money"]
                    )
                )
                self.recvMsg.append({"interface": "withdraw", "result": response.status})

            elif event["interface"] == "query":
                # Send a query request to the branch server
                response = self.stub.MsgDelivery(
                    banks_pb2.TransactionRequest(
                        customer_id=self.id,
                        operation="query"
                    )
                )
                self.recvMsg.append({"interface": "query", "balance": response.balance})
            
        print(f"Customer {self.id} received messages: {self.recvMsg}")