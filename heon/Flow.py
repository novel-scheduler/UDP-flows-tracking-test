import datetime


class Flow:
    FLOW_NAMES = {
        1: "FLOW_ONE",
        2: "FLOW_TWO",
        3: "FLOW_THREE",
    }

    CONN_MSG_FLOW_NUM_MATCH = {
        "Connection_One": 1,
        "Connection_Two": 2,
        "Connection_Three": 3,
    }

    def __init__(self, flow_name):
        self.name = flow_name
        self.timestamp = datetime.datetime.now().timestamp()

    def getFlowInfoArray(self):
        '''return [name, timestamp] array of the flow'''
        return [self.name, self.timestamp]

    def getFlowInfoStr(self):
        '''return "name, timestamp" in string'''
        return f"{self.name}, {self.timestamp}"

    @staticmethod
    def getMatchingFlowNameFromConnectionMsg(connection_msg):
        matched_flow_num = Flow.CONN_MSG_FLOW_NUM_MATCH[connection_msg]
        matched_flow_name = Flow.FLOW_NAMES[matched_flow_num]
        return matched_flow_name
