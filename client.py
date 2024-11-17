import grpc
import json
import sys
import multiprocessing
import customer
import time

def start_customer_process(customer_id, events):
    # Initialize Customer, create stub, and execute events
    cust = customer.Customer(customer_id, events)
    cust.createStub()
    cust.executeEvents()
    return {"id": customer_id, "recv": cust.recvMsg}  # Return the response messages for this customer

def main():
    # Load the customer configurations from the input JSON file
    with open(sys.argv[1]) as f:
        config = json.load(f)

    # Filter customer elements from the configuration
    customers = [item for item in config if item['type'] == 'customer']
    # List to store all customer responses
    output_data = []

    # Start each customer process sequentially with a delay to allow propagation
    for cust in customers:
        result = start_customer_process(cust['id'], cust['events'])
        output_data.append(result)
        time.sleep(3)  # Delay for propagation

    # Write the output data to output.json file in the current directory
    with open("output.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4)

if __name__ == '__main__':
    main()




