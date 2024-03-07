import networkx as nx
import matplotlib.pyplot as plt
import time
from OpenAIChatBot import OpenAIChatBot

with open("APIKey.txt", "r") as textFile:
    openAIAPIKey = textFile.read().strip()  # Personal OpenAI product key
openAIModelVersion = "gpt-3.5-turbo"  # GPT Version to use

textGenerationChatBotInfo = {"role": "assistant", "content": "You are a message writer working for a client. The client"
                                                             " will give you instructions on what should be written "
                                                             "and your job is to generate a message that naturally "
                                                             "incorporates the client's instructions. Furthermore, the"
                                                             " message should be written in such a way that would make"
                                                             " the messages seem like they are part of a one on one "
                                                             "conversation."}

codeGenerationChatBotInfo = {"role": "assistant", "content": "You are a webdesign coder working for a client. The code"
                                                             " you produce is in HTML, embedded CSS, and embedded "
                                                             "JavaScript. The client will inform you of what the "
                                                             "webpage should look like and your code should reflect "
                                                             "these requests. Do not provide anything other than the "
                                                             "code."}

userIntentClassifierChatBotInfo = {"role": "assistant", "content": "You are a message intention classifier for a "
                                                                   "client. The client will give you an array of "
                                                                   "words along with a message (they will be "
                                                                   "separated by a comma). Analyze the message to "
                                                                   "understand its contextual intention. Afterwards, "
                                                                   "choose a word from the provided array that best "
                                                                   "represents the contextual intention of the "
                                                                   "provided message, and return that one word as "
                                                                   "your response. Nothing other but the word should "
                                                                   "be your response, and your response must be one "
                                                                   "of the case sensitive words belonging to the "
                                                                   "provided array. Ensure there are no quotation "
                                                                   "marks in your response. For example, if the "
                                                                   "client gives you the input '[morning, afternoon, "
                                                                   "evening, night], it is dark but I can still see "
                                                                   "some natural light. the '[morning, afternoon, "
                                                                   "evening, night]' portion of the client input "
                                                                   "represents the array and the 'it is dark but I "
                                                                   "can still see some natural light' portion of the "
                                                                   "client input represents the message. The word in "
                                                                   "the array that best describes the message intent "
                                                                   "is 'evening' so your response should simply be "
                                                                   "'evening'. The response 'Evening' is an invalid "
                                                                   "response because it does not match the case "
                                                                   "sensitivity of the word in the array."}

adaptiveCodeGenerationChatBotInfo = {"role": "assistant", "content": "You are a prompt engineer for a client. The "
                                                                     "client will give you a generative prompt along "
                                                                     "with a user message. The two will be put in "
                                                                     "separate curly braces separated by a comma, where"
                                                                     " the first text encapsulated by the curly braces "
                                                                     "is the generative prompt and the second text "
                                                                     "encapsulated by the curly braces is the message. "
                                                                     "Analyze the generative prompt to understand what "
                                                                     "its general generative objectives are, and then "
                                                                     "analyze the message to extract the details that "
                                                                     "may be relevant to the context of the generative "
                                                                     "prompt. Return a new generative prompt such that"
                                                                     " it maintains the general expected output of the "
                                                                     "original generative prompt but includes the "
                                                                     "relevant details provided from the message by "
                                                                     "substituting those details in for the general "
                                                                     "details in the original generative prompt. For "
                                                                     "example, if the client inputs '{Generate an image"
                                                                     "of a city park}, {the sky should be sunset}', "
                                                                     "an appropriate response to return would be "
                                                                     "'Generate an image of a city park with a sunset "
                                                                     "sky.' Another example is if the client inputs '{"
                                                                     "Generate a Python loop that prints the current "
                                                                     "iteration and loops as much as the user requests}"
                                                                     ", {i want it 100 times}', then an appropriate "
                                                                     "response to return would be 'Generate a Python "
                                                                     "loop that loops 100 times and prints the current "
                                                                     "iteration each time.'"}

textGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                            openAIModelVersion=openAIModelVersion,
                                            systemRole=textGenerationChatBotInfo["role"],
                                            systemContent=textGenerationChatBotInfo["content"])

codeGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                            openAIModelVersion=openAIModelVersion,
                                            systemRole=codeGenerationChatBotInfo["role"],
                                            systemContent=codeGenerationChatBotInfo["content"])

userIntentClassifierChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                                  openAIModelVersion=openAIModelVersion,
                                                  systemRole=userIntentClassifierChatBotInfo["role"],
                                                  systemContent=userIntentClassifierChatBotInfo["content"])

adaptiveCodeGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                                    openAIModelVersion=openAIModelVersion,
                                                    systemRole=adaptiveCodeGenerationChatBotInfo["role"],
                                                    systemContent=adaptiveCodeGenerationChatBotInfo["content"])

textGenerationChatBotObject.setUpChatBot()
codeGenerationChatBotObject.setUpChatBot()
userIntentClassifierChatBotObject.setUpChatBot()
adaptiveCodeGenerationChatBotObject.setUpChatBot()

nodeConfigurationDataExample = {"NodeName": "", "AITextGenerationPrompt": "", "AICodeGenerationPrompt": "",
                                "DefaultSystemPrompt": "", "TextResponse": False, "ButtonResponse": False,
                                "AdaptiveCodeGeneration": "", "TransitionTime": 0}


class Node:

    def __init__(self, nodeConfigurationData: dict) -> None:  # Class attributes

        # Initialization Data
        self.nodeName = nodeConfigurationData["NodeName"]
        self.aiTextGenerationPrompt = nodeConfigurationData["AITextGenerationPrompt"]
        self.aiCodeGenerationPrompt = nodeConfigurationData["AICodeGenerationPrompt"]
        self.defaultSystemPrompt = nodeConfigurationData["DefaultSystemPrompt"]
        self.textResponse = nodeConfigurationData["TextResponse"]
        self.buttonResponse = nodeConfigurationData["ButtonResponse"]
        self.adaptiveCodeGeneration = nodeConfigurationData["AdaptiveCodeGeneration"]
        self.transitionTime = nodeConfigurationData["TransitionTime"]
        self.dynamicPrompt = nodeConfigurationData.get("DynamicPrompt", None)

        # Configuration Data
        self.responsePaths = None

        # Default Data
        self.userResponse = ""
        self.parentNodes = {}
        self.nextNode = None
        self.previousNode = None

    def get_dynamic_prompt(self):
        # Assuming 'self.dynamicPrompt' can be a callable or a static value
        if callable(self.dynamicPrompt):
            return self.dynamicPrompt()  # Call if it's callable
        return self.dynamicPrompt  # Return as is if not callable


class CAIFlow:

    def __init__(self) -> None:  # Class attributes
        self.flowStart = None
        self.registeredNodes = {}
        self.currentNode = None
        self.processNodeCounter = 2
        self.processNodeCounterRange = self.processNodeCounter + 1

    def registerNodes(self, nodesToRegister: []):

        for node in nodesToRegister:
            nodeID = {node.nodeName: node}
            self.registeredNodes.update(nodeID)

    def appendNode(self, nodeName: str, userResponsePaths: dict) -> None:

        node = self.registeredNodes[nodeName]

        # If no nodes are in the conversational flow yet
        if self.flowStart is None:
            self.flowStart = node

        # Register response paths to node
        node.responsePaths = userResponsePaths

        for response in node.responsePaths:
            childNodeName = node.responsePaths[response]
            childNode = self.registeredNodes[childNodeName]

            childNode.parentNodes.update({childNodeName: response})

    def traverseFlow(self):

        if self.currentNode is None:
            self.currentNode = self.flowStart
            print(self.currentNode)
        else:
            self.currentNode = self.currentNode.nextNode
            print(self.currentNode)

    def generateText(self) -> str:

        # Generate the chatbot text given the node's text generation prompt and print it out
        if self.currentNode.aiTextGenerationPrompt != "":

            textPrompt = textGenerationChatBotObject.generatePromptResponse(self.currentNode.aiTextGenerationPrompt)

        # Print out the given the node's default system prompt if no AI generation was specified
        else:
            textPrompt = self.currentNode.defaultSystemPrompt

        return textPrompt

    def getUserInputOptions(self):
        inputOptions = {"TextInput": self.currentNode.textResponse, "ButtonsInput": []}

        if self.currentNode.buttonResponse:
            buttonOptions = [responseKey for responseKey, _ in self.currentNode.responsePaths.items()]
            inputOptions["ButtonsInput"] = buttonOptions


        return inputOptions

    def registerUserResponse(self, userResponse) -> str:

        self.currentNode.userResponse = userResponse
        return ""

    def generateCode(self) -> str:

        if self.currentNode.aiCodeGenerationPrompt != "":

            if self.currentNode.adaptiveCodeGeneration == "":

                codeGenerationResult = codeGenerationChatBotObject.generatePromptResponse(
                    self.currentNode.aiCodeGenerationPrompt)

            else:

                userInput = self.registeredNodes[self.currentNode.adaptiveCodeGeneration].userResponse
                adaptiveCodeGenerationPrompt = ("{" + self.currentNode.aiCodeGenerationPrompt + "}, {" + userInput
                                                + "}")

                adaptedCodeGeneratedPrompt = adaptiveCodeGenerationChatBotObject.generatePromptResponse(
                    adaptiveCodeGenerationPrompt)

                codeGenerationResult = codeGenerationChatBotObject.generatePromptResponse(
                    adaptedCodeGeneratedPrompt)

            return codeGenerationResult
        else:
            return ""


    def set_current_node_by_name(self, node_name):
        if node_name in self.registeredNodes:
            self.currentNode = self.registeredNodes[node_name]
            print(self.currentNode)
        else:
            print("Node name not found in registered nodes.")

    def setNextNode(self):

        responsePaths = self.currentNode.responsePaths

        if responsePaths is not None:

            numberOfPaths = len(responsePaths)

            if numberOfPaths == 1:
                self.currentNode.nextNode = self.registeredNodes[next(iter(responsePaths.values()), None)]

            elif numberOfPaths > 1:

                userResponsePrompt = "["

                for key, value in responsePaths.items():
                    userResponsePrompt = userResponsePrompt + key + ", "

                userResponsePrompt = (userResponsePrompt[:len(userResponsePrompt) - 2] + "], "
                                      + self.currentNode.userResponse)

                userIntent = userIntentClassifierChatBotObject.generatePromptResponse(userResponsePrompt)
                self.currentNode.nextNode = self.registeredNodes[responsePaths[userIntent]]

    def processNode(self, userResponse=""):
        if not self.currentNode:
            self.currentNode = self.flowStart

        print(f"userResponse: {userResponse}")
        print(f"{self.currentNode.responsePaths}")

        # Process user input to determine next node directly
        if userResponse in self.currentNode.responsePaths:
            nextNodeName = self.currentNode.responsePaths[userResponse]
            self.currentNode = self.registeredNodes[nextNodeName]
        elif '' in self.currentNode.responsePaths:
            # Default transition for any input
            nextNodeName = self.currentNode.responsePaths['']
            self.currentNode = self.registeredNodes[nextNodeName]

        dynamicPrompt = self.currentNode.get_dynamic_prompt()

        # Generate response based on current node
        generatedText = dynamicPrompt if dynamicPrompt else self.generateText()
        userInputOptions = self.getUserInputOptions()

        # Optionally advance the flow automatically if no user input is expected
        if not self.currentNode.textResponse and not self.currentNode.buttonResponse:
            self.setNextNode()
            # Regenerate response for new current node
            dynamicPrompt = self.currentNode.get_dynamic_prompt()
            generatedText = dynamicPrompt if dynamicPrompt else self.generateText()
            userInputOptions = self.getUserInputOptions()

        # Update returnInfo with the new current node's response
        returnInfo = {
            "GeneratedText": generatedText,
            "UserInputOptions": userInputOptions
        }

        return returnInfo


nodeConfigurationDataExample2 = {"NodeName": "", "AITextGenerationPrompt": "", "AICodeGenerationPrompt": "",
                                 "DefaultSystemPrompt": "", "TextResponse": False, "ButtonResponse": False,
                                 "AdaptiveCodeGeneration": "", "TransitionTime": 0}
