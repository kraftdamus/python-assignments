# Amidst Ourselves: A Game of Deception
# 
# ©2020 Karl Damus, All Rights Reserved
#

PLAYERS = ['blue', 'brown', 'green', 'orange', 'pink', 'red', 'yellow']
# testDict = {'upper engine': ['cafeteria', 'reactor', 'security', 'lower engine', 'medbay'], 'reactor': ['security', 'upper engine', 'lower engine'], 'security': ['upper engine', 'lower engine', 'reactor'], 'lower engine': ['electrical', 'storage', 'upper engine', 'reactor', 'security'], 'medbay': ['upper engine', 'cafeteria'], 'cafeteria': ['storage', 'admin', 'weapons', 'upper engine', 'medbay'], 'weapons': ['o2', 'navigation', 'cafeteria', 'shields'], 'o2': ['weapons', 'navigation', 'shields'], 'navigation': ['weapons', 'o2', 'shields'], 'shields': ['communications', 'storage', 'weapons', 'o2', 'navigation'], 'communications': ['storage', 'shields'], 'storage': ['admin', 'cafeteria', 'lower engine', 'electrical', 'shields', 'communications'], 'electrical': ['storage', 'lower engine'], 'admin': ['cafeteria', 'storage'],}

def main():
    load_map("data/skeld.txt")
    load_chat_log("data/chatlog.txt", load_map("data/skeld.txt"))
    tally_votes(load_chat_log("data/chatlog.txt", load_map("data/skeld.txt")))
    get_paths(load_chat_log("data/chatlog.txt", load_map("data/skeld.txt")))

def load_map(file_path):
    with open(file_path, "r") as f:
        map_dictionary = {}
        for line in f:
            line = line.strip().split(":")
            line[1] = line[1].strip(" ").split(", ")
            # add to dictionary
            map_dictionary[line[0]] = line[1]
    # print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in map_dictionary.items()) + "}")
    return map_dictionary


def simplify_testimony(chat, rooms):
    # if the 'chat' is a vote simply use the line. if not, follow else statement
    checkForVote = chat.find("voted")

    if checkForVote >= 0:
        simplifiedChat = chat.strip()
    else:
        chat = chat.split(":")
        speaker = chat[0]
        message = chat[1]

        # check for player in message
        for val in PLAYERS:
            checkSubject = message.find(val)
            if checkSubject >= 0:
                subject = val
                break
            else:
                subject = ""
        # check for location in message
        for key in rooms:
            checkLocation = message.find(key)
            if checkLocation >= 0:
                location = key
                break
            else:
                location = ""

        # accusatory condition
        if location != "" and subject != "":
            simplifiedChat = (speaker + ": " + subject + " in " + location)
        # self condition
        if location != "" and subject == "":
            simplifiedChat = (speaker + ": " + speaker + " in " + location)
        # useless condition
        if location == "":
            pass
    
    try:
        return simplifiedChat
    except NameError:
        pass

def load_chat_log(filename, rooms):
    simplifiedChatLog = []
    with open(filename, "r") as f:
        for line in f:
            chatMessageSimplified = simplify_testimony(line, load_map("data/skeld.txt"))
            # if something was returned then push to array
            if chatMessageSimplified != None:
                simplifiedChatLog.append(chatMessageSimplified)
    return(simplifiedChatLog)

def tally_votes(chat_log):
    tally = {}
    # create a key for each player
    for player in PLAYERS:
        tally[player] = 0
    # add a key for 'skip'
    tally["skip"] = 0
    for val in chat_log:
        isVote = val.find("voted")
        if isVote >= 0:
            val = val.split(" ")
            tally[val[2]] = (int(tally[val[2]]) + 1)
    return tally


def get_paths(chat_log):
    pathDict = {}
    # create keys in dictionary for each player
    for player in PLAYERS:
        pathDict[player] = [] 
    # print(chat_log)
    # run through chat_log -- skip if a vote or if accusatory
    for chatVal in chat_log:
        if chatVal.find("voted") >= 0:
            pass
        else:
            chatVal = chatVal.split(":")
            # check if accusatory
            if chatVal[1].find(chatVal[0]) >= 0:
                print(chatVal)
            
        


    # for val in chat_log:
    #     isVote = val.find("voted")
    #     val = val.split(":")
    #     for testAccusatory in PLAYERS:
    #         isAccusatory = val[1].find(testAccusatory)
    #         if isAccusatory >= 0:
    #             break
    #     if isVote >= 0 or isAccusatory >= 0:
    #         pass
    #     else:
    #         print("Correct")

if __name__ == '__main__':
    main()

"""
chat = chat.split(":")
    speaker = chat[0]
    message = chat[1]
"""