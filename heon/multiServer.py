from nis import match
import socket
from _thread import *
from Flow import Flow

# Define constants
host = '127.0.0.1'
port = 12345
ThreadCount = 0
MAX_CHUNK_SIZE = 100 

# empty previous flow_sequence in flie
f = open("flow_sequence_server_side.txt", "w")
f.write("")
f.close()


"""
Respond to any UDP connection.
"""
def client_handler(ss):
    while True:
        (data, sender) = ss.recvfrom(MAX_CHUNK_SIZE)
        print("\n\n---------- CLIENT_HANDLER ----------")
        print("* FLOW RECEIVED!")
        print("        * sender => " + str(sender))
        msg = data.decode('utf-8')
        print("        * MSG => " + str(msg))
        
        # Initialize new flow object
        flow_name = Flow.getMatchingFlowNameFromConnectionMsg(msg)
        flow_obj = Flow(flow_name)
        
        # Write flow information to file
        f = open("flow_sequence_server_side.txt", "a")
        f.write(flow_obj.getFlowInfoStr() + "\n")
        f.close()
        
        if msg == "4":
            ss.close()
            break
        
        reply = f'Server: YO WHAT UP'
        ss.sendto(str.encode(reply), sender)
    ss.close()


"""
Originally used for accepting and starting a new thread with a 
client socket from new TCP connections, which isn't used for UDP.
Will not be needed.
"""
# def receive_init_conn(ss):
#     (data, sender) = ss.recvfrom(MAX_CHUNK_SIZE)
#     msg = data.decode('utf-8')
#     print('Received first connection from: ' + str(sender[0]) + ":" + str(sender[1]))
#     print('      * MSG =>' + str(msg))
#     start_new_thread(client_handler, (ss, sender))


"""
Start UDP server.
"""
def start_server(host, port):
    # Create UDP socket 
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        ss.bind((host, port))
    except socket.error as e:
        print(str(e))
        
    print(f'UDP SERVER Running on {port}...')

    while True:
        client_handler(ss)


if __name__ == "__main__":
    start_server(host, port)
