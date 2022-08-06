f = open("flow_sequence_client_side.txt", "r")
flow_sequence_lines_client = f.readlines()
f.close()

f = open("flow_sequence_server_side.txt", "r")
flow_sequence_lines_server = f.readlines()
f.close()

client_server_flow_match_arr = []
is_flow_order_perfectly_matching = True

i = 0
iterations = int(input("Number of iterations from client: "))
while i < iterations:
    curr_flow_client =  flow_sequence_lines_client[i].split(", ")[1].strip()
    curr_flow_server = flow_sequence_lines_server[i].split(",")[1].strip()
    
    client_server_flow_match_arr.append(curr_flow_client == curr_flow_server)
    
    if curr_flow_client != curr_flow_server: 
        is_flow_order_perfectly_matching = False
    
    i = i + 1

# print(client_server_flow_match_arr)
print(is_flow_order_perfectly_matching)