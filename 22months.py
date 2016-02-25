import matplotlib.pyplot as plt
import numpy as np
import sys
import os

Greetings=['Hello', 'HI!', 'hi!', 'hello', 'Hi', 'Hi!', 'HELLO', 'Hello!', 'hi', 'HI']
Affirmative=['YES', 'Yes', 'YES!', 'yes', 'yeah', 'YEAH', 'YEA', 'YEAH!', 'yea']  

print "Hello Papazon! (Don't forget your punctuation)"
while True:
            x = (raw_input())
            if x not in Greetings: 
	       print "Try again!"
	       continue
            else:
                if x in Greetings:
                    break
print "Is it your 22 month anniversary with a silly goldfish?"
while True:
           y = (raw_input())
           if y not in Affirmative: 
	      print "Try again!"
	      continue
           else:
	         if y in Affirmative:
	               break
print "HAPPY ANNIVERSARY!!! This is quite the silly practice exercise since I have not learnt much since the last time but ..."

t = np.arange(0, 2 * np.pi, 0.1)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
plt.plot(x, y)
plt.savefig('/Users/samantha/Desktop/22.png')
os.system("open '/Users/samantha/Desktop/22.png'")
sys.exit()