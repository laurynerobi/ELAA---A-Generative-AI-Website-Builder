from OpenCAI import Node
from flask import session, request

testNodeData1 = {"NodeName": "TestNode1 - Intro",
                 "AITextGenerationPrompt": "Generate a brief greeting message that introduces you as an automated "
                                           "web designer named 'Elaa'. The message should not be longer than 3 "
                                           "sentences and the message should not be open-ended.",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": "",
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5,

                 }
testNode1 = Node(testNodeData1)


def node_two_prompt():
    template_type = session.get('website_type', 'default')
    print(f"template-type:{template_type}")
    return f"I see that you want to build a {template_type} website. Let's get started."


testNodeData2 = {"NodeName": "TestNode2 - Confirm Website Type",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt":node_two_prompt,
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5
                 }
testNode2 = Node(testNodeData2)

def node_three_prompt():
    return "What would you like to name your website?"


testNodeData3 = {"NodeName": "TestNode3 - Website Name",
                 "AITextGenerationPrompt": "Generate a brief message asking the user what they would like to name their "
                                           "website. Given the type of website. Furthermore, make sure the message gets "
                                           "to the point- no small talk. ",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": node_three_prompt,
                 "TextResponse": True,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5
                 }
testNode3 = Node(testNodeData3)

def node_four_prompt():
    website_name = session.get('website_name')
    print(f"Business_name:{website_name}")
    return f"I see that you want to name your website {website_name} . Let's continue."


testNodeData4 = {"NodeName": "TestNode4 - Confirm Website Name",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt":node_four_prompt,
                 "TextResponse":True,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5
                 }
testNode4 = Node(testNodeData4)

testNodeData5 = {"NodeName": "TestNode5 - Pick Background Color",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "Generate an HTML 'Hello World!' page with the user requested background.s",
                 "DefaultSystemPrompt": "What color would you like the background to be?",
                 "DynamicPrompt": "",
                 "TextResponse": True,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "TestNode3 - Pick Background Color",
                 "TransitionTime": 0
                 }
testNode5 = Node(testNodeData5)

testNodeData6 = {"NodeName": "TestNode6 - Update code new background color",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "Generate an HTML 'Hello World!' page with the user requested background.",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": "",
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": testNode3.nodeName,
                 "TransitionTime": 0
                 }
testNode6 = Node(testNodeData6)

testNodeData7 = {"NodeName": "TestNode7 - Website name",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "What do you want your website to be called?",
                 "DynamicPrompt": "",
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 0
                 }
testNode7 = Node(testNodeData7)

testNodes = [testNode1, testNode2, testNode3, testNode4, testNode5, testNode6, testNode7]
