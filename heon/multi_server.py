import socket
from FlowRecord import FlowRecord
import argparse

# Define constants
MAX_CHUNK_SIZE = 100


def flush_file(file):
    f = open(file, "w")
    f.write("")
    f.close()


# Respond to UDP connections
def client_handler(ss, seq_output_file, ts_output_file):

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
        f = open(seq_output_file, "a")
        f.write(str(flow_record.getFlowNum()) + "\n")
        f.close()

        # Write flow record timestamp to file
        f = open(ts_output_file, "a")
        f.write(str(flow_record.getFlowTS()) + "\n")
        f.close()

        reply = f'Server: RESPONSE!'
        ss.sendto(str.encode(reply), sender)


# Start UDP server
def start_UDP_server(host, port, args):
    # Create UDP socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        ss.bind((host, port))
    except socket.error as e:
        print(str(e))

    # Get output file names
    seq_output_file = args.output_flow_seq_file
    ts_output_file = args.output_flow_ts_file

    print(f'UDP SERVER Running on {port}...')

    client_handler(ss, seq_output_file=seq_output_file, ts_output_file=ts_output_file)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=False,
                        default='127.0.0.1', help="Host on which to run server")
    parser.add_argument("-p", "--port", type=int, required=False,
                        default=5000, help="Port on which to run server")
    parser.add_argument("-s", "--output-flow-seq-file", type=str,
                        required=False, default="flow_sequence_server_side.txt", help="Name of file that contains the output flow sequence")
    parser.add_argument("-t", "--output-flow-ts-file", type=str,
                        required=False, default="flow_ts_server_side.txt", help="Name of file that contains the output flow timestamps")
    args = parser.parse_args()
    
    # Flush output files
    flush_file(args.output_flow_seq_file)
    flush_file(args.output_flow_ts_file)
    
    # Start server
    host = args.host
    port = args.port
    start_UDP_server(host, port, args)
