import argparse
import random


def flush_file(file):
    f = open(file, "w")
    f.write("")
    f.close()


def write_flow_num_to_file(file, value):
    f = open(file, "a")
    f.write(f"{value}\n")
    f.close()


def run_single_iteration(flow_num_list, file_to_write):
    list_to_choose_from = flow_num_list.copy()
    for i in range(len(list_to_choose_from)):
        chosen_num = random.choice(list_to_choose_from)
        write_flow_num_to_file(file_to_write, chosen_num)
        list_to_choose_from.remove(chosen_num)


def generate_random_flow_sequence_grouped(flow_num_list, num_iter, file_to_write):  
    for i in range(0, num_iter):
        run_single_iteration(flow_num_list, file_to_write)
        

def generate_random_flow_sequence_independent(num_conn, flow_num_list, num_iter, file_to_write):
    flow_num_remaining_count_dict = {}
    for i in range(1, num_conn+1):
        flow_num_remaining_count_dict[i] = num_iter
        
    list_to_choose_from = flow_num_list.copy()
    for i in range(0, num_conn * num_iter):
        chosen_num = random.choice(list_to_choose_from)
        write_flow_num_to_file(file_to_write, chosen_num)
        remaining_count = flow_num_remaining_count_dict[chosen_num]
        remaining_count = remaining_count - 1
        flow_num_remaining_count_dict[chosen_num] = remaining_count
        if remaining_count <= 0:
            list_to_choose_from.remove(chosen_num)


def generate_desired_flow_sequence(flow_num_list, num_iter, file_to_write):
    for i in range(0, num_iter):
        for flow_num in flow_num_list:
            write_flow_num_to_file(file_to_write, flow_num)
    

def validate_args(args):
    if args.num_conn <= 0: 
        raise ValueError
    if args.iterations <= 0:
        raise ValueError


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num-conn", type=int, required=False,
                        default=3, help="Number of client connections")
    parser.add_argument("-l", "--iterations", type=int, required=False, default=40,
                        help="Number of iterations. The length of the flow sequence is equal to num_conn * iterations. (ex: 3 * 40 = 120 lines)")
    parser.add_argument("-r", "--random-flow-seq-file", type=str,
                        required=False, default="random_flow_sequence.txt", help="Name of file to store randomly generated flow sequence")
    parser.add_argument("-d", "--desired-flow-seq-file", type=str,
                        required=False, default="desired_flow_sequence.txt", help="Name of file to store desired flow sequence")
    parser.add_argument("-c", "--chosen-seq-type", type=str, choices=["desired", "random"], default="desired", help="Type of flow sequence to store to the file that contains input flow sequence for the client side")
    parser.add_argument("-i", "--input-flow-seq-file", type=str,
                        required=False, default="input_flow_sequence.txt", help="Name of file to store input flow sequence for client")
    parser.add_argument("-m", "--mode", type=str, choices=["grouped", "independent"], default="independent", help="Mode on which the random generation runs. In grouped mode, all flows will paced equally so that no flow number appears twice before the other flow numbers have appeared an equal number of times. In independent mode, the flow order will be comletely random, where a flow number may appear multiple times in a row and break the equal pace shared among other flows")
    args = parser.parse_args()
    
    # Validate arguments
    try:
        validate_args(args)
    except ValueError:
        print("ValueError: Invalid value was passed as argument. Exiting program.")
        exit()
    
    # Empty flow sequence files
    flush_file(args.random_flow_seq_file)
    flush_file(args.desired_flow_seq_file)
    
    # Get a list that stores flow numbers
    flow_num_list = list(range(1, args.num_conn+1))
    
    # Run random flow number generation function depending on mode
    if args.mode == "grouped":
        generate_random_flow_sequence_grouped(flow_num_list, args.iterations, args.random_flow_seq_file)
    elif args.mode == "independent":
        generate_random_flow_sequence_independent(args.num_conn, flow_num_list, args.iterations, args.random_flow_seq_file)
    
    # Generate the desired order of the flow numbers
    generate_desired_flow_sequence(flow_num_list, args.iterations, args.desired_flow_seq_file)
    
    # Copy flow sequence to file that stores input flow sequence for the client
    # Choose from either desired or random flow sequence 
    # Currently, the assumption is that the desired flow sequence is equal to 
    # the input flow sequence (thus the default)
    flush_file(args.input_flow_seq_file)
    file_to_copy = None
    if args.chosen_seq_type == "desired":
        file_to_copy = args.desired_flow_seq_file
    elif args.chosen_seq_type == "random":
        file_to_copy = args.random_flow_seq_file
    with open(file_to_copy,'r') as firstfile, open(args.input_flow_seq_file,'a') as secondfile:
        for line in firstfile:
            secondfile.write(line)
