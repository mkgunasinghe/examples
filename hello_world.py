print "Hello World!"
x = raw_input()
if x == "Hello":
    print "How are you today?"
    y = raw_input()
    if y == "Good!":
        print "That is marvelous news :-) You finished this program on the first go and have shown enthusiam and proper punctuation."
    elif y != "Good!":
        print "Show some enthusiam next time (Hint: Good!)?"
        y2 = raw_input()
        if y2 == "Good!":
            print "This is the end of the program. You have learnt enthusiam and proper punctuation."
elif x != "Hello":
    print "Why don't you use capitalization and try again (Hint: Hello)?"
    x2 = raw_input()
    if x2 == "Hello":
        print "How are you today?"
    z = raw_input()
    if z == "Good!":
        print "That is marvelous news :-) You finished this program on the first go and have shown enthusiam and proper punctuation."
    elif z != "Good!":
        print "Show some enthusiam next time (Hint: Good!)?"
    z2 = raw_input()
    if z2 == "Good!":
        print "This is the end of the program. You have learnt enthusiam and proper punctuation."