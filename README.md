# DistributedBankingSystemSimulation
This project simulates a distributed banking system.
We assume all customers share one banking account.
Customers send requests to servers with the same ids (customer_id == branch_id),
then propagate any balance changes to other server branches.

1. make sure python and pip are installed correctly
2. run the following command to install required packages:
   python -m pip install grpcio==1.64.1 grpcio-tools==1.64.1 protobuf==5.27.2
4. run the following command:
   "python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. ./protos/banks.proto"
5. open one terminal and run "python server.pu input.json"
6. open a different terminal and run "python client.py input.json"
7. you will see a output.json being generated (remember to delete the existing output.json)
