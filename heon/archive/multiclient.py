import socket
import random
import functools
from FlowRecord import FlowRecord

# Define constants
host = '127.0.0.1'
port = 12345
COUNT_LIMIT = 10

# Initialize array for storing Flow objects
# whose data is later to be written to file
flow_sequence = []
flow_sequence_line_count = 1

# Initialize 3 client UDP sockets
cs_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cs_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cs_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def start_client_connections():
    # Randomly select client socket and send UDP packet
    for num in range(0, COUNT_LIMIT):
        element = random.randint(1, 3)
        print("\nrandomly chosen: ", str(element))
        if element == 1:
            print("sending: 1")
            flow_obj = Flow(Flow.FLOW_NAMES[1])
            flow_sequence.append(flow_obj)
            cs_1.sendto(str.encode("Connection_One"), (host, port))
            print("sent: init msg!")

            res_1 = cs_1.recv(2048)
            print(res_1.decode('utf-8'))

        elif element == 2:
            print("sending: 2")
            flow_obj = Flow(Flow.FLOW_NAMES[2])
            flow_sequence.append(flow_obj)
            cs_2.sendto(str.encode("Connection_Two"), (host, port))
            print("sent: init msg!")

            res_2 = cs_2.recv(2048)
            print(res_2.decode('utf-8'))

        elif element == 3:
            print("sending: 3")
            flow_obj = Flow(Flow.FLOW_NAMES[3])
            flow_sequence.append(flow_obj)
            cs_3.sendto(str.encode("Connection_Three"), (host, port))

            print("sent: init msg!")
            res_3 = cs_3.recv(2048)
            print(res_3.decode('utf-8'))

        elif element == 4:
            print("exiting the application")
            cs_1.close()
            cs_2.close()
            cs_3.close()
            exit()

        else:
            print("invalid choice try again")


if __name__ == "__main__":
    COUNT_LIMIT = int(input("Define number of iterations: "))
    start_client_connections()

    print("*** Writing flow sequence to file ***")
    
    all_lines = ''
    for flow in flow_sequence:
        all_lines = all_lines + str(flow_sequence_line_count) + ", " + flow.getFlowInfoStr() + "\n"
        flow_sequence_line_count = flow_sequence_line_count + 1

    f = open("flow_sequence_client_side.txt", "w")
    f.writelines(all_lines)
    f.close()

    print("\n*** Exiting the application ***\n\n")

    # Close client sockets & exit
    cs_1.close()
    cs_2.close()
    cs_3.close()
    exit()
