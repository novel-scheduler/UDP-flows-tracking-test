import argparse
import sys


def compare_lists(list1, list2):
    if len(list1) != len(list2):
        print("*** List lengths are different, terminating program! ***")
        sys.exit()
       
    return list1 == list2


def compare_flow_sequence(args):
    # Get client-side flow sequence input
    # By default, input flow sequence for the client is equal to the desired flow sequence
    f = open(args.client_seq_input, "r")
    flow_input_lines_client = f.readlines()
    flow_input_client = [line.strip() for line in flow_input_lines_client]
    f.close()
    
    # Get client-side flow sequence output
    f = open(args.client_seq_output, "r")
    flow_sequence_lines_client = f.readlines()
    flow_sequence_client = [line.strip() for line in flow_sequence_lines_client]
    f.close()

    # Get server-side flow sequence output
    f = open(args.server_seq_output, "r")
    flow_sequence_lines_server = f.readlines()
    flow_sequence_server = [line.strip() for line in flow_sequence_lines_server]
    f.close()
    
    # Get desired flow sequence output
    f = open(args.desired_seq_file, "r")
    flow_sequence_lines_desired = f.readlines()
    flow_sequence_desired = [line.strip() for line in flow_sequence_lines_desired]
    f.close()

    # Get comparison results
    client_input_desired_match = compare_lists(flow_input_client, flow_sequence_desired)
    client_server_match = compare_lists(flow_sequence_client, flow_sequence_server)
    server_desired_match = compare_lists(flow_sequence_server, flow_sequence_desired)
    
    f = open(args.compare_result_file, "w")
    f.write(f"Client Input & Desired (Expected) Match => {client_input_desired_match}\n")
    f.write(f"Client & Server Match => {client_server_match}\n")
    f.write(f"Server & Desired (Expected) Match => {server_desired_match}\n")
    f.close()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--client-seq-input", type=str,
                        required=False, default="input_flow_sequence.txt", help="Name of file that contains the input flow sequence on the client side.")
    parser.add_argument("-c", "--client-seq-output", type=str,
                        required=False, default="flow_sequence_client_side.txt", help="Name of file that contains the output flow sequence on the client side.")
    parser.add_argument("-s", "--server-seq-output", type=str,
                        required=False, default="flow_sequence_server_side.txt", help="Name of file that contains the output flow sequence on the server side.")
    parser.add_argument("-d", "--desired-seq-file", type=str,
                        required=False, default="desired_flow_sequence.txt", help="Name of file that contains the desired flow sequence")
    parser.add_argument("-r", "--compare-result-file", type=str,
                        required=False, default="compare_result.txt", help="Name of file that contains the result of the flow sequence comparison.")
    args = parser.parse_args()

    # Run comparison
    compare_flow_sequence(args)
