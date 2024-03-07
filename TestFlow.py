from OpenCAI import CAIFlow
from TestFlowNodes import *


# Test File for Building the Conversational Flow
def conversation_flow():
    testFlow = CAIFlow()
    testFlow.registerNodes(testNodes)
    # testFlow.printRegisteredNodes()

    testFlow.appendNode("TestNode1 - Intro", {"": testNode2.nodeName})
    testFlow.appendNode(testNode2.nodeName, {"": testNode3.nodeName})
    #testFlow.appendNode(testNode2.nodeName, {"Yes": testNode5.nodeName, "No": testNode3.nodeName})
    testFlow.appendNode(testNode3.nodeName, {"": testNode4.nodeName})
    testFlow.appendNode(testNode4.nodeName, {"": testNode2.nodeName})
    return testFlow
# Enable this if you seek to see a visualization of the conversational flow.
# testFlow.visualizeFlow()
