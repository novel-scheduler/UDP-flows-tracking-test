import socket
from FlowRecord import FlowRecord
import argparse

# Define constants
MAX_CHUNK_SIZE = 100

# Initialize client UDP sockets
cs_list = []

# Empty previous flow_sequence in flie
f = open("flow_sequence_client_side.txt", "w")
f.write("")
f.close()

# Empty previous ts in file
f = open("flow_ts_client_side.txt", "w")
f.write("")
f.close()


# Create a new client socket
def init_client_socket():
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return cs


# Run a single client connection. Send a msg to the UDP server and
# listen for a response.
def run_single_client_connection(cs, flow_num, server_addr):
    print(f"sending: {flow_num}")
    flow_record = FlowRecord(flow_num=flow_num)

    cs.sendto(str.encode(str(flow_record.getFlowNum())), server_addr)
    print("sent!")

    f = open("flow_sequence_client_side.txt", "a")
    f.write(str(flow_record.getFlowNum()) + "\n")
    f.close()

    f = open("flow_ts_client_side.txt", "a")
    f.write(str(flow_record.getFlowTS()) + "\n")
    f.close()

    res = cs.recv(MAX_CHUNK_SIZE)
    print(res.decode('utf-8'))


# Run a set of client connections 
def run_client_connections(args):
    # Get the input flow sequence
    f = open(args.input_flow_seq_file, "r")
    lines = f.readlines()
    input_flow_seq = [int(line.strip()) for line in lines]

    # Initialize client sockets
    # ex) If num_conn is 3 -> 3 client sockets are created and added to the list.
    # Each
    for i in range(0, args.num_conn):
        cs_list.append(init_client_socket())

    # Iterate through input flow sequence and send client msg accordingly
    for flow_num in input_flow_seq:
        run_single_client_connection(cs=cs_list[flow_num-1], flow_num=flow_num, server_addr=(args.host, args.port))


def validate_args(args):
    if args.num_conn <= 0: 
        raise ValueError


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=False,
                        default='127.0.0.1', help="Host to connect to")
    parser.add_argument("-p", "--port", type=int, required=False,
                        default=12345, help="Port to connect to")
    parser.add_argument("-n", "--num-conn", type=int, required=False,
                        default=3, help="Number of client connections to initiate")
    parser.add_argument("-f", "--input-flow-seq-file", type=str,
                        required=False, default="input_flow_sequence.txt", help="Name of file that contains the input flow sequence")
    args = parser.parse_args()
    
    # Validate arguments
    try:
        validate_args(args)
    except ValueError:
        print("ValueError: Invalid value was passed as argument. Exiting program.")
        exit()

    # Run client connections
    run_client_connections(args)

    print("\n*** Exiting the application ***\n\n")

    # Close client sockets
    for cs in cs_list:
        cs.close()

    exit()
