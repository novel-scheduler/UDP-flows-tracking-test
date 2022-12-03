import datetime


class FlowRecord:

    def __init__(self, flow_num):
        self.num = flow_num
        self.timestamp = datetime.datetime.now().timestamp()

    def getFlowNum(self):
        '''return the number that identifies the flow'''
        return self.num

    def getFlowTS(self):
        '''return timestamp at which flow record was created'''
        return self.timestamp
