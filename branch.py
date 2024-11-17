import grpc
import banks_pb2
import banks_pb2_grpc

class Branch(banks_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        # Initialize branch ID, balance, and list of branch IDs for communication
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()

        # Create gRPC stubs to communicate with other branches
        for branch_id in self.branches:
            if branch_id != self.id:
                branch_channel = grpc.insecure_channel(f'localhost:{50050 + branch_id}')
                self.stubList.append(banks_pb2_grpc.BankStub(branch_channel))

    def MsgDelivery(self, request, context):
        if request.operation == "deposit":
            return self.Deposit(request, context)
        elif request.operation == "withdraw":
            return self.Withdraw(request, context)
        elif request.operation == "query":
            return self.Query(request, context)
        elif request.operation == "propagate_deposit":
            return self.Propagate_Deposit(request, context)
        elif request.operation == "propagate_withdraw":
            return self.Propagate_Withdraw(request, context)

    def Deposit(self, request, context):
        self.balance += request.amount
        # print(f"Customer {request.customer_id} deposited {request.amount} to Branch {self.id}. New balance: {self.balance}")
        
        # Propagate the deposit to other branches
        for stub in self.stubList:
            stub.MsgDelivery(banks_pb2.TransactionRequest(
                customer_id=request.customer_id,
                operation="propagate_deposit",
                amount=request.amount
            ))
        return banks_pb2.TransactionResponse(status="success")

    def Withdraw(self, request, context):
        if request.amount <= self.balance:
            self.balance -= request.amount
            # print(f"Customer {request.customer_id} withdrew {request.amount} from Branch {self.id}. New balance: {self.balance}")

            # Propagate the withdrawal to other branches
            for stub in self.stubList:
                stub.MsgDelivery(banks_pb2.TransactionRequest(
                    customer_id=request.customer_id,
                    operation="propagate_withdraw",
                    amount=request.amount
                ))
            return banks_pb2.TransactionResponse(status="success")
        else:
            # Insufficient funds
            return banks_pb2.TransactionResponse(status="fail")

    def Query(self, request, context):
        # print(f"Customer {request.customer_id} queried balance from Branch {self.id}. Balance: {self.balance}")
        return banks_pb2.TransactionResponse(status="success", balance=self.balance)

    def Propagate_Deposit(self, request, context):
        self.balance += request.amount
        # print(f"Branch {self.id} received a propagated deposit of {request.amount}. New balance: {self.balance}")
        return banks_pb2.TransactionResponse(status="success")

    # Inter-branch propagation of withdrawal
    def Propagate_Withdraw(self, request, context):
        if request.amount <= self.balance:
            self.balance -= request.amount
            # print(f"Branch {self.id} received a propagated withdrawal of {request.amount}. New balance: {self.balance}")
            return banks_pb2.TransactionResponse(status="success")
        else:
            print(f"Branch {self.id} failed to apply a propagated withdrawal of {request.amount}. Insufficient funds.")
            return banks_pb2.TransactionResponse(status="fail")
