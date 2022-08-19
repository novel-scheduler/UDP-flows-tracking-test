import socket
from FlowRecord import FlowRecord
import argparse

# Define constants
MAX_CHUNK_SIZE = 100

# Empty previous flow_sequence in flie
f = open("flow_sequence_server_side.txt", "w")
f.write("")
f.close()

# Empty previous ts in file
f = open("flow_ts_server_side.txt", "w")
f.write("")
f.close()


# Respond to UDP connections
def client_handler(ss):

    while True:
        (data, sender) = ss.recvfrom(MAX_CHUNK_SIZE)
        print("\n\n---------- CLIENT_HANDLER ----------")
        print("* FLOW RECEIVED!")
        print("        * sender => " + str(sender))
        msg = data.decode('utf-8')
        print("        * MSG => " + str(msg))

        # Initialize new flow record
        flow_num = msg
        flow_record = FlowRecord(flow_num=flow_num)

        # Write flow record to file
        f = open("flow_sequence_server_side.txt", "a")
        f.write(str(flow_record.getFlowNum()) + "\n")
        f.close()

        # Write flow record timestamp to file
        f = open("flow_ts_server_side.txt", "a")
        f.write(str(flow_record.getFlowTS()) + "\n")
        f.close()

        reply = f'Server: RESPONSE!'
        ss.sendto(str.encode(reply), sender)


# Start UDP server
def start_UDP_server(host, port):
    # Create UDP socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        ss.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f'UDP SERVER Running on {port}...')

    client_handler(ss)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=False,
                        default='127.0.0.1', help="Host on which to run server")
    parser.add_argument("-p", "--port", type=int, required=False,
                        default=5000, help="Port on which to run server")
    args = parser.parse_args()
    
    # Start server
    host = args.host
    port = args.port
    start_UDP_server(host, port)
