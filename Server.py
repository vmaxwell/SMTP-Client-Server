# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:13:52 2018

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
    if(i >= len(input) or i+1 >= len(input)):
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
        return False
    if(input[i] != "<"):
        return False
    i = i + 1
    if(not mailbox(input)):
        return False
    if(input[i] != ">"):
        return False
    i = i + 1
    return True

def reverse_path(input):
    return path(input)

def forward_path(input):
    return path(input)

def mail_from_cmd(input):
    global i
    i = 0
    
    #if(len(input) < 16):
        #return False
    if(input[i] != "M"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+1] != "A"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+2] != "I"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+3] != "L"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 4
    if(not whitespace(input)):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i] != "F"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+1] != "R"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+2] != "O"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+3] != "M"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    if(input[i+4] != ":"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 5
    nullspace(input)
    if(not reverse_path(input)):
        #return False
        return 501
    if(not nullspace(input)):
        #print("501 Syntax error in parameters or arguments")
        #return False
        return 501
    if(not crlf(input)):
        #print("501 Syntax error in parameters or arguments")
        #return False
        return 501
    else:
        #print("250 OK")
        #return True
        return 250
    
def rcpt_to_cmd(input):
    global i
    i = 0
    if(input[i] != "R"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "C"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "P"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "T"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(not whitespace(input)):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    #i = i + 1
    if(input[i] != "T"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "O"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != ":"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    nullspace(input)
        #print("501 Syntax error in parameters or arguments")
        #return False
        #return 501
    if(not forward_path(input)):
        #print("501 Syntax error in parameters or arguments")
        #return False
        return 501
    if(not nullspace(input)):
        #print("501 Syntax error in parameters or arguments")
        #return False
        return 501
    if(not crlf(input)):
        #print("501 Syntax error in parameters or arguments")
        #return False
        return 501
    else:
        #print("250 OK")
        #return True
        return 250
        
def data_cmd(input):
    global i
    i = 0
    if(input[i] != "D"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "A"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "T"):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    i = i + 1
    if(input[i] != "A"):
        #print("ERROR")
        #return False
        return 500
    i = i + 1
    if(not nullspace(input)):
    #if(not nullspace(input)):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 500
    
    if(not crlf(input[i])):
        #print("500 Syntax error: command unrecognized")
        #return False
        return 501
    else:
        #print("354 Start mail input; end with <CRLF>.<CRLF>")
        #return True
        return 354
    
def contains(inputArr, input):
    for element in inputArr:
        if(input == element):
            return True
        
    return False

def main():
    serverPort = int(sys.argv[1])
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(1)
    
    while True:
        forwardPaths = []
        message = ""
        (connectionSocket, addr) = serverSocket.accept()
        
        greeting1 = "220 snapper.cs.unc.edu\n"
        connectionSocket.send(greeting1.encode())
        
        greeting2 = connectionSocket.recv(1024)
        greeting2_decode = greeting2.decode()
        
        if(greeting2_decode[0:4] != "HELO"):
            print("Error -- unable to connect with client")
            connectionSocket.close()
            continue
            
        greeting3 = "250 HELO " + greeting2_decode[4:len(greeting2_decode)] + " pleased to meet you\n"
        connectionSocket.send(greeting3.encode())
        
        mail_from = connectionSocket.recv(1024)
        mail_from_decode = mail_from.decode()
        
        result = mail_from_cmd(mail_from_decode)
        if(result != 250):
            print("Error -- could not process MAIL FROM command")
            connectionSocket.close()
            continue
        
        response = "250 OK\n"
        connectionSocket.send(response.encode())
        
        client_resp = connectionSocket.recv(1024)
        client_resp_decode = client_resp.decode()
        
        result = rcpt_to_cmd(client_resp_decode)
        
        while(result == 250):
            fPath = client_resp_decode[(client_resp_decode.index("@") + 1) : client_resp_decode.index(">")]
            if(not contains(forwardPaths, fPath)):
                forwardPaths.append(fPath)
            
            response = "250 OK\n"
            connectionSocket.send(response.encode())
            client_resp = connectionSocket.recv(1024)
            client_resp_decode = client_resp.decode()
            result = rcpt_to_cmd(client_resp_decode)
            
        if(result == 501):
            print("Error -- could not process RCPT TO command")
            connectionSocket.close()
            continue
        
        result = data_cmd(client_resp_decode)
        if(result != 354):
            print("Error -- could not process DATA command")
            connectionSocket.close()
            continue
        
        response = "354 Start mail input; end with <CRLF>.<CRLF>\n"
        connectionSocket.send(response.encode())
        
        client_resp = connectionSocket.recv(1024)
        client_resp_decode = client_resp.decode()
        
        if(client_resp_decode.endswith("\n.\n")):
            message = message + client_resp_decode[0 : client_resp_decode.rfind("\n.\n")] + "\n"
            response = "250 OK\n"
            connectionSocket.send(response.encode())
        else:
            print("Error -- mail message did not end with . on blank line")
            connectionSocket.close()
            continue
        
        for file in forwardPaths:
            f = open("forward/" + file, "a")
            f.write(message)
            f.close()
        
        client_resp = connectionSocket.recv(1024)
        client_resp_decode = client_resp.decode()
        
        if(client_resp_decode != "QUIT"):
            print("Error -- client did not respond with QUIT")
            connectionSocket.close()
            continue
        
        response = "221 snapper closing connection\n"
        connectionSocket.send(response.encode())
        
        connectionSocket.close()
        
        
        
    
main()