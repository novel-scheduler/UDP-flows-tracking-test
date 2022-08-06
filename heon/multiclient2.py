import socket
import random
import functools
import threading
from Flow import Flow

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

# thraad lock
lock = threading.Lock()


def run_client_connection(cs, thread_num):
    global flow_sequence, flow_sequence_line_count
    
    for num in range(0, COUNT_LIMIT):
        print(f"sending: {thread_num}")
        flow_obj = Flow(Flow.FLOW_NAMES[thread_num])
        
        lock.acquire()
        flow_sequence.append(flow_obj)
        lock.release()
        
        thread_connection_num_map = {
            1: "Connection_One",
            2: "Connection_Two",
            3: "Connection_Three",
        }
        
        cs.sendto(str.encode(thread_connection_num_map[thread_num]), (host, port))
        print("sent: init msg!")

        res = cs.recv(2048)
        print(res.decode('utf-8'))

def start_client_connections():
    global cs_1, cs_2, cs_3
    
    # Creating threads
    thread1 = threading.Thread(target=run_client_connection, args=(cs_1, 1))
    thread2 = threading.Thread(target=run_client_connection, args=(cs_2, 2))
    thread3 = threading.Thread(target=run_client_connection, args=(cs_3, 3))
    
    # Starting the threads
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Waiting for the threads to finish executing
    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == "__main__":
    COUNT_LIMIT = int(input("Define number of iterations: "))
    start_client_connections()

    print("*** Writing flow sequence to file ***")

    all_lines = ''
    for flow in flow_sequence:
        all_lines = all_lines + \
            str(flow_sequence_line_count) + ", " + flow.getFlowInfoStr() + "\n"
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
