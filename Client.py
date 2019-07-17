# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:13:24 2018

@author: vemm97
"""

import socket, sys

i = 0

def special(input):
    return input == "<" or input == ">" or input == "(" or input == ")" or input == "[" or input == "]" or input == '"\"' or input == "." or input == "," or input == ";" or input == ":" or input == "@" or input == '"'

def digit(input):
    return input.isdigit()

def letter(input):
    #return input == "A" or input == "a" or input == "B" or input == "b" or input == "C" or input == "c" or input == "D" or input == "d" or input == "E" or input == "e" or input == "F" or input == "f" or input == "G" or input == "g" or input == "H" or input == "h" or input == "I" or input == "i" or input == "J" or input == "j" or input == "K" or input == "k" or input == "L" or input == "l" or input == "M" or input == "m" or input == "N" or input == "n" or input == "O" or input == "o" or input == "P" or input == "p" or input == "Q" or input == "q" or input == "R" or input == "r" or input == "S" or input == "s" or input == "T" or input == "t" or input == "U" or input == "u" or input == "V" or input == "v" or input == "W" or input == "w" or input == "X" or input == "x" or input == "Y" or input == "y" or input == "Z" or input == "z"
    return input.isalpha()

def space(input):
    return input == " " or input == "    "

def char(input):
    return ord(input) < 128 and not special(input) and not space(input)

def let_dig(input):
    return letter(input) or digit(input)

def string(input):
    global i
    if(i >= len(input) or i+1 >= len(input)):
        print("ERROR -- string")
        return False
    if(not char(input[i])):
        print("ERROR -- string")
        return False
    elif(not char(input[i+1])):
        i = i + 1
        return True
    else:
        i = i + 1
        return string(input)

def let_dig_str(input):
    global i
    if(i >= len(input) - 1):
        return False
    if(not let_dig(input[i])):
        return False
    elif(not let_dig(input[i+1])):
        i = i + 1
        return True
    else:
        i = i + 1
        return let_dig_str(input)

def name(input):
    global i
    if(i >= len(input)):
        print("ERROR -- name")
        return False
    if(not letter(input[i])):
        print("ERROR -- name")
        return False
    i = i + 1
    if(not let_dig_str(input)):
        return False
    return True

def element(input):
    if(i >= len(input)):
        print("ERROR -- element")
        return False
    if(letter(input[i])):
        if(name(input)):
            return True
        else:
            return False
        return True
    else:
        print("ERROR -- element")
        return False

def whitespace(input):
    global i
    if(not space(input[i])):
        #print("ERROR -- whitespace")
        return False
    elif(not space(input[i+1])):
        i = i + 1
        return True
    else:
        i = i + 1
        return whitespace(input);

def crlf(input):
    if(input.endswith('\n')):
        return True
    else:
        print("ERROR -- CRLF")
        return False

def null(input):
    return not char(input) and not special(input) and space(input) and input != "\n"
    
def nullspace(input):
    if(i >= len(input)):
        print("ERROR -- nullspace")
        return False
    return not null(input[i]) or whitespace(input)

def domain(input):
    global i
    if(not element(input)):
        return False
    elif(input[i] != "."):
        return True
    else:
        i = i + 1
        return domain(input)

def local_part(input):
    return string(input)
    
def mailbox(input):
    global i
    if(not local_part(input)):
        return False
    if(i >= len(input)):
        print("ERROR -- mailbox")
        return False
    if(input[i] != "@"):
        print("ERROR -- mailbox")
        return False
    i = i + 1
    if(not domain(input)):
        return False
    return True
    
def path(input):
    global i
    if(i >= len(input)):
        print("ERROR -- path")
        return False
    if(not mailbox(input)):
        return False
    return True

def reverse_path(input):
    return path(input)

def forward_path(input):
    return path(input)

def serverHelo(input):
    global i
    if(input[0:3] != "250"):
        return False
    i = i + 3
    if(not whitespace(input)):
        return False
    if(input[i : i+4] != "HELO"):
        return False
    i = i + 4
    if(not whitespace(input)):
        return False
    if(not domain(input)):
        return False
    if(not whitespace(input)):
        return False
    if(input[i : i+19] != "pleased to meet you"):
        return False
    i = i + 19
    if(not nullspace(input)):
        return False
    if(not crlf(input)):
        return False
    return True

def main():
    global i
    serverHost = sys.argv[1]
    serverPort = int(sys.argv[2])

    from_input = raw_input("From: ")
    while(not reverse_path(from_input + "\n")):
        i = 0
        from_input = raw_input("From: ")
        
    to_inputs = raw_input("To: ")
    to_inputs_strip = to_inputs.strip()
    rcpts = to_inputs_strip.split(",")
    j = 0
    while(j < len(rcpts)):
        i = 0
        if(not nullspace(rcpts[j])):
            to_inputs = raw_input("To: ")
            to_inputs_strip = to_inputs.strip()
            rcpts = to_inputs_strip.split(",")
            j = 0
            continue
        if(not forward_path(rcpts[j] + "\n")):
            to_inputs = raw_input("To: ")
            to_inputs_strip = to_inputs.strip()
            rcpts = to_inputs_strip.split(",")
            j = 0
            continue
        j = j + 1
        
    subject_input = raw_input("Subject: ") + "\n"
    message_input = raw_input("Message: ") + "\n"
    
    std_input = sys.stdin
    m_input = std_input.readline()
    
    while(m_input != ".\n"):
        message_input = message_input + m_input
        m_input = std_input.readline()
    
    message_input = message_input + m_input
    
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverHost, serverPort))
    clientDomain = "cs.unc.edu"
    
    greeting1 = clientSocket.recv(1024)
    greeting1_decode = greeting1.decode()
    if(greeting1_decode[0:3] != "220"):
        print("Error -- unsuccessful connection to server")
        clientSocket.close()
        return
        
    greeting2 = "HELO " + clientDomain + "\n"
    clientSocket.send(greeting2.encode())
    
    greeting3 = clientSocket.recv(1024)
    greeting3_decode = greeting3.decode()
    i = 0
    if(not serverHelo(greeting3_decode)):
        print("Error -- server did not respond to HELO")
        clientSocket.close()
        return
    
    mail_from = "MAIL FROM: <" + from_input.strip() + ">\n"
    clientSocket.send(mail_from.encode())
    response = clientSocket.recv(1024)
    response_decode = response.decode()
    if(response_decode[0:3] != "250"):
        print("Error -- server did not successfully receive MAIL FROM command")
        clientSocket.close()
        return
    
    rcpt_to = ""
    for rcpt in rcpts:
        i = 0
        nullspace(rcpt)
        rcpt_to = "RCPT TO: <" + rcpt[i:len(rcpt)] + ">\n"
        clientSocket.send(rcpt_to.encode())
        response = clientSocket.recv(1024)
        response_decode = response.decode()
        if(response_decode[0:3] != "250"):
            print("Error -- server did not successfully receive RCPT TO command")
            clientSocket.close()
            return
    
    data = "DATA\n"
    clientSocket.send(data.encode())
    response = clientSocket.recv(1024)
    response_decode = response.decode()
    if(response_decode[0:3] != "354"):
        print("Error -- server did not successfully receive DATA command")
        clientSocket.close()
        return
        
    user_message = "From: <" + from_input.strip() + ">\nTo: "
    j = 0
    while(j < len(rcpts)):
        i = 0
        rcpt = rcpts[j]
        nullspace(rcpt)
        if(j == len(rcpts) - 1):
            user_message = user_message + "<" + rcpt[i:len(rcpt)] + ">\n"
        else:
            user_message = user_message + "<" + rcpt[i:len(rcpt)] + ">, "
        j = j + 1
        
    user_message = user_message + "Subject: " + subject_input + "\n"
    user_message = user_message + message_input
    
    clientSocket.send(user_message.encode())
    
    response = clientSocket.recv(1024)
    response_decode = response.decode()
    if(response_decode[0:3] != "250"):
        print("Error -- server did not successfully receive message")
        clientSocket.close()
        return
        
    quit_cmd = "QUIT"
    clientSocket.send(quit_cmd.encode())
    
    response = clientSocket.recv(1024)
    response_decode = response.decode()
    if(response[0:3] != "221"):
        print("Error -- server did not successfully close")
        clientSocket.close()
        return
        
    clientSocket.close()
    
    

main()