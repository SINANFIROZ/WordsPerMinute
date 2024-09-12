import curses
from curses import wrapper
import time

def startscreen(stdscr):
    stdscr.clear()           #Clears the entire screen
    stdscr.addstr("Welcome to the Typing test\n")     #Prints the string required
    stdscr.addstr("\nPress any key to begin")     #Prints the string required
    stdscr.refresh()
    stdscr.getkey()         #Wait for the user to type something or else the text will be displayed only for a millisecond

def display_text(stdscr,target,current,wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM:{wpm}")

    for i,char in enumerate(current):
        correct_char=target[i]
        color=curses.color_pair(1)
        if char!=correct_char:
            color=curses.color_pair(2)
        
        stdscr.addstr(0,i,char,color)

def wpmtest(stdscr):
    target_text="Hello! This is a text test for testing your speed while typing on a keyboard"
    current_text=[]
    wpm=0
    start_time=time.time()
    stdscr.nodelay(True)  #This is given so that it does not wait for the user to hit a key


    while True:
        time_elapsed=max(time.time()-start_time,1)
        wpm=round((len(current_text)/(time_elapsed/60)/5))

        stdscr.clear()
        display_text(stdscr,target_text,current_text,wpm)
        stdscr.refresh

        if "".join(current_text)==target_text:  #"".join(current_text) is used to combine the elements in the list to a string, for eg:["h","e","l","l","o"] to "hello"
            stdscr.nodelay(False)
            break

        try:
            key=stdscr.getkey()
        except:
            continue

        if ord(key)==27: #Represents the ASCII value for esc key on keyboard
            break
        if key in("KEY_BACKSPACE",'\b',"\x7f"): #If key is a backspace
            if len(current_text)>0:
                current_text.pop()
        elif len(current_text)<len(target_text):
            current_text.append(key)

        for char in target_text:
            stdscr.addstr(char,curses.color_pair(1))
        stdscr.refresh()
    
def main(stdscr):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)

    
    startscreen(stdscr)
    wpmtest(stdscr)

    stdscr.addstr(2,0,"You completed the text! Press any key to continue....")
    stdscr.getkey()

wrapper(main)