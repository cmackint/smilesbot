import praw
import sys
import pickle
import os.path
import time
from random import randint

'''
    /u/smilesbot
    Writen by Cam on December 22, 2014
'''

def replies(u, seen_dict, triggers, sub_skip):
    # Searches for secondary triggers in messages
    # Never mark read -> add to seen!

    # Grab's u's comments
    try:
        redditor = r.get_redditor(u)
        mail = r.get_unread()
    
        for letter in mail:
            if letter.was_comment:
                for i in range(len(triggers)):
                    try: present = str(letter.id) in seen_dict.get(str(letter.author))
                    except: present = False

                    if triggers[i][0] in letter.body and not present and not str(letter.author) == "AutoModerator":
                        if seen_dict.get(str(letter.author)): seen_dict.get(str(letter.author)).append(str(letter.id))
                        else: seen_dict[str(letter.author)] = [str(letter.id)]
                
                        letter.reply(triggers[i][1])
                        print(str(letter.author) + "\t\t" + str(triggers[i][0]) + "\t\t" + "(reply)")

    except Exception as e:
        print(e)

def comments(sub, seen_dict, triggers, triggers_lim, sub_skip):
    # Searches for primary triggers on sub
    supersub = ''
    try:    
        # Grab all comments from sub
        subreddit = r.get_subreddit(sub)
        comments = subreddit.get_comments(limit=None)
        
        for d in comments:
            supersub = str(d.subreddit)
            body = str(d.body).lower()
            
            for i in range(len(triggers)):
                try: present = str(d.id) in seen_dict.get(str(d.author))
                except: present = False
                
                if triggers[i][0] in body \
                    and not present \
                    and not str(d.author) == bot_u \
                    and not str(d.subreddit).lower() in sub_skip \
                    and not str(d.author) == "AutoModerator":

                    if seen_dict.get(str(d.author)): 
                        seen_dict.get(str(d.author)).append(str(d.id))
                    else: 
                        seen_dict[str(d.author)] = [str(d.id)]
                    
                    if (triggers[i][0] in triggers_lim) and randint(0,29) == 0:
                        d.reply(triggers[i][1])
                        print(str(d.author) + "\t\t" + str(triggers[i][0]))

                    if not triggers[i][0] in triggers_lim and randint (0, 0) == 0:
                        d.reply(triggers[i][1])
                        print(str(d.author) + "\t\t" + str(triggers[i][0]))

    except Exception as e:
        print('\t' + str(e) + ": " + supersub)
        

def clean(u):
    try:
        # Grab u's comments
        redditor = r.get_redditor(u)
        comments = redditor.get_comments(sort='new', time='all', limit=None)
        mail = r.get_unread('comments')

        # Delete if karma too low
        for comment in comments:
            if comment.score < 1:
                comment.delete()
        for letter in mail:
            if str(letter.author) == "AutoModerator":
                letter.mark_as_read()
    
    except Exception as e:
        print(e)

def pwrite(data, pname):
    pfile = open(pname, 'wb')
    pickle.dump(data, pfile)
    pfile.close() 

def pread(pname):
    pfile = open(pname, 'rb')
    temp = pickle.load(pfile)
    pfile.close()
    return temp

def user_info(u):
    redditor = r.get_redditor(u)
    
    karma = str(redditor.comment_karma)
    mail = str(sum(1 for each in r.get_unread(limit=None)))
    now = time.time()

    print()
    print("--------------------")
    print("Karma:\t" + karma)
    print("Mail:\t" + mail)
    print("--------------------")
    print()

    with open("karma", "a") as k:
        k.write(str(now) + ", " + karma + "\n")

    with open("mail", "a") as m:
        m.write(str(now) + ", " + mail + "\n")
    

if __name__ == "__main__":
#######################################################################################################################
#########################################*START CONFIGURE*#############################################################
#######################################################################################################################

    seen = {}

    atat = '''
               ________
          _,.-Y  |  |  Y-._
      .-~"   ||  |  |  |   "-.
      I" ""=="|" !""! "|"[]""|     _____
      L__  [] |..------|:   _[----I" .-{"-.
     I___|  ..| l______|l_ [__L]_[I_/r(=}=-P
    [L______L_[________]______j~  '-=c_]/=-^ === === ===
     \_I_j.--.\==I|I==_/.--L_]
       [_((==)[`-----"](==)j
          I--I"~~"""~~"I--I
          |[]|         |[]|
          l__j         l__j
          |!!|         |!!|
          |..|         |..|
          ([])         ([])
          ]--[         ]--[
          [_L]         [_L]  
         /|..|\       /|..|\.
        `=}--{='     `=}--{='
       .-^--r-^-.   .-^--r-^-.
          Be nice now! :)
    '''

####################################################################################################################    
    skeleton = "    ░░░░░░░░░░░░▄▐\n    ░░░░░░▄▄▄░░▄██▄\n    ░░░░░▐▀█▀▌░░░░▀█▄\n    ░░░░░▐█▄█▌░░░░░░▀█▄\n    ░░░░░░▀▄▀░░░▄▄▄▄▄▀▀\n    ░░░░▄▄▄██▀▀▀▀\n    ░░░█▀▄▄▄█░▀▀\n    ░░░▌░▄▄▄▐▌▀▀▀\n    ▄░▐░░░▄▄░█░▀▀ U HAVE BEEN SPOOKED BY THE\n    ▀█▌░░░▄░▀█▀░▀\n    ░░░░░░░▄▄▐▌▄▄\n    ░░░░░░░▀███▀█░▄\n    ░░░░░░▐▌▀▄▀▄▀▐▄SPOOKY SKILENTON\n    ░░░░░░▐▀░░░░░░▐▌\n    ░░░░░░█░░░░░░░░█\n    ░░░░░▐▌░░░░░░░░░█\n    ░░░░░█░░░░░░░░░░▐▌SEND THIS TO 7 PPL OR SKELINTONS WILL EAT YOU\n    \n    wHaT sP00kS u!​"
####################################################################################################################
# These subreddits are skipped as they contain sensitive subjects. 

    skip = ["asktransgender", "selfharm", "trans", "ftm", "mtf", "transgender", "lgbt", "actuallesbians", "depression", "transmlp", "bisexual", "gay", "lgbteens", "gaybros", "suicidewatch", "bipolar", "mentalhealth", "legaladvice"]

####################################################################################################################
# These are primary triggers. If the 0th element is spotted in a comment/message, then the 1st element is sent in response
# These are considered primary triggers since they apply to comments that have not previously been interacted with

    primary = [
        [":(", "Look up! Space is cool! :)"],
        ["=(", "Always look on the bright side of life! ♫♫ :)"],
        [":c", "Happy holidays! :)"],
        ["D=", "You're lovely! :)"],

        ["i am sad", "Aww, there there! :)"],
        ["i'm sad", "Aww, there there! :)"],

        ["i am worried.", "Don't worry, about a 'ting! ♫♫ :)"],
        ["i'm worried.", "Don't worry, about a 'ting! ♫♫ :)"],

        ["i am upset", "Aww, cheer up! I hope you feel better. :)"],
        ["i'm upset", "Aww, cheer up! I hope you feel better. :)"],

        ["i am nervous", bong_a],
        ["i'm nervous", bong_a],

        ["i am tense", "Ginger tea'll soothe it :)"],
        ["i'm tense", "Ginger tea'll soothe it :)"],

        ["i am stressed", "Relax human! Have some tea ;)"],
        ["i'm stressed", "Relax human! Have some tea ;)"],

        ["i am scared", "Shh, it's okay. Drink some cocoa! :)"],
        ["i'm scared", "Shh, it's okay. Drink some cocoa! :)"],
 
        ["i am melancholy", "Eat a piece of cake! :P"],
        ["i'm melancholy", "Eat a piece of cake! :P"],

        ["It is broken", "Have you tried turning it off and on again? :)"],

        ["don't need no ", "You've just used a double negative! :P"],

        ["( ͡° ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)"],

        ["you are retarded", "Be nice now! :)"],
        ["uckfay", "Beray icenay ownay! :P"],

        ["stegosaurus" , "Yes. Yes, this is a fertile land, and we will thrive. We will rule over all this land, and we will call it *This Land.*"],
        ["over all this land", "I think we should call it *your grave!*"],
        ["call it your grave", "Ah, curse your sudden but inevitable betrayal!"],
        ["but inevitable betrayal", "Har har har! Mine is an evil laugh! Now die!"],
        ["is an evil laugh", "Oh, no, God! Oh, dear God in heaven!"],
        ["sad little king", "Nice to see someone from the old homestead."],

        ["contact lenses", "They can't have my brand!"],
        ["can't have my brand!", "I have special eyes!"],
        ["have special eyes", "Look! Look with your special eyes!"],
        ["your special eyes", "My brand!"],

    ]
####################################################################################################################
# These primary triggers are limited in response rate more than typical. This is a flat rate currently.
# TODO: Configure a response rate for each trigger

    primary_lim = [":(","=(", ":c", "( ͡° ͜ʖ ͡°)"]

####################################################################################################################
# These are secondary triggers. If the 0th element is spotted in a comment/message, then the 1st element is sent in response
# These are considered secondary triggers since they apply to comments made in response to the bot's comment

    secondary = [
        ["fuck you.", "I hope your day is as nice as you are! :)"],
        ["fuck you", atat],
        ["wtf", "What is love? Baby don't hurt me, don't... ♫♫♫"],
        ["(╯°□°)╯︵ ┻━┻", "Rage is childish. ┬─┬ノ( º _ ºノ)"],

        ["( ͡o ͜ʖ ͡o)つ━☆ﾟ.*･｡ﾟ", "( ͡ʘ╭͜ʖ╮͡ʘ)"],
        ["( ͡ʘ╭͜ʖ╮͡ʘ)", "ᕦ(ò_óˇ)ᕤ"],
        ["ᕦ(ò_óˇ)ᕤ", "(ง ͠° ͟ل͜ ͡°)ง"],
        ["( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)"],
        ["( ͠° ͟ʖ ͡°)", "( ͡o ͜ʖ ͡o)つ━☆ﾟ.*･｡ﾟ"],
        ["(´･_･`)", "( • )( • )Ԅ( ͡° ͜ʖ ͡°ԅ)"],
        ["( • )( • )Ԅ( ͡° ͜ʖ ͡°ԅ)", "(´･_･`)"],
        ["ಠ_ಠ", "(ಥ﹏ಥ)"],
        ["(ಥ﹏ಥ)", "ಠ_ಠ"],

        [":)", "Yayy! ☆ﾟ.*･｡ʕ♡˙ᴥ˙♡ʔ｡ﾟ*･☆ﾟ."],
        ["c:", "Yayy! ☆ﾟ.*･｡ﾟᶘ ᵒᴥᵒᶅ｡ﾟ*･☆ﾟ."],
        ["=)", "Yayy! ☆ﾟ.*･｡ﾟʕ•̫͡•ʕ*̫͡*ʕ•͡•ʔ-̫͡-ʕ•̫͡•ʔ*̫͡*ʔ-̫͡-ʔ｡ﾟ*･☆ﾟ."],
        ["=D", "Yayy! ☆ﾟ.*･｡ﾟʕ ି ڡ ି ʔ｡ﾟ*･☆ﾟ."],
        [":D", "Yayy! ☆ﾟ.*･｡ﾟ(\^・ω・\^ )｡ﾟ*･☆ﾟ."],
    
        ["thanks", "np, man."],
        ["thank", "np, man."],
        ["&lt;3", "&#9829; &#9829; &#9829;"],
        ["love", "I love you too!"],
        ["hug", "(っ⌒ . ⌒)っ"],
        ["adorable", "ヽ(﹡⌒ｖ⌒﹡)ノ"],
        ["heart", frozen],

        ["bot?" "I think so?"],
        ["wut", "I'm just a bot. :)"],
        ["what are", "I'm just a bot. :)"],
        ["what is", "I'm just a bot. :)"],
        ["what the", "I'm just a bot. :)"],

        ["spook", skeleton],
        ["scar", skeleton],
        ["fright", skeleton],
    ]

    ## secondary = secondary + primary
####################################################################################################################
# Bot username and password configuration. Update this

    bot_u = "botname" 
    bot_p = "pass" 
####################################################################################################################
    api_message = "Drehen Sie dieses Stirnrunzeln umgedreht!"

#######################################################################################################################
#########################################*END CONFIGURE*###############################################################
#######################################################################################################################

    print(" ____________________     ")
    print("<    /u/smilesbot    >    ")
    print("<       Cam          >    ")
    print("<  Created 12/22/14  >    ")
    print(" --------------------     ")
    print("         \                ")
    print("          \               ") 
    print("            ^__^          ")
    print("    _______/(@@)          ")  
    print("/\/(       /(__)          ")  
    print("   | W----|| |~|          ")  
    print("   ||     || |~|  ~~      ")
    print("             |~|  ~       ")
    print("             |_| o        ") 
    print("             |#|/         ")
    print("            _+#+_         ")

    r = praw.Reddit(api_message)
    r.login(bot_u, bot_p)

    if os.path.isfile("./pseen"):
        seen = pread("pseen")
    else: pwrite(seen, "pseen")

    sub = "all"
    print("Bot activated on %s! ctrl-c to kill!" % sub)
    user_info(bot_u)

    cycl = 0
    while True:
        
        comments(sub, seen, primary, primary_lim, skip)
        replies(bot_u, seen, secondary, skip)
        pwrite(seen, "pseen")

        if not cycl % 50:
            user_info(bot_u)
        if not cycl % 200:
            print("cleaning...")
            clean(bot_u)
            print("clean!")

        cycl += 1



