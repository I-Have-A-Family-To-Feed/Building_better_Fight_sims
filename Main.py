# NEXT THING TO WORK ON: BOSS IMMUNITIES

#TO DO: CREATE  A BOSS NAME/EID DICT




#FIGHTS THAT WORK FULLY: Shriekwing, hungering, innerva, sludgefist, xymox, 
#FIGHTS THAT WORK, BUT HAVE ISSUES: huntsman. ---> no barghast adds (don't show up in the adds table for some reason), does not account for moving barghast away.

#FIGHTS THAT DO NOT WORK CURRENTLY: Sun king, Council, SLG, Denathrius. 

import raw_queries as Q
import query_variables
import header
import requests
#import http.client
import tkinter as tk 
from tkinter import *
import re
import math

url = "https://www.warcraftlogs.com/api/v2"
V=query_variables.variables
token = header.headers


# hard coding this stuff for now
EIDtable=[2398,2418,2383,2402,2405,2406,2412,2399,2417,2407] 
names=['Shriekwing','Huntsman Altimor','Hungering Destroyer','Lady Inerva Darkvein',"Sun King's Salvation","Artificer Xy'mox",'Council of Blood','Sludgefist','Stone Legion Generals','Sire Denathrius']
# the " suffix on each of the names is because of how the API data gets parsed/stored. 
#currently names is duplicated/used in get_boss_ID. it is actually used in data_parsing_handler
#EIDtable is used in data_parsing_handler



########################################################################################################################################################################
########################################################################################################################################################################

def parse_position():#fucking unreal that I can do it in this few of lines.  6 lines compared to 21. and I don't even need to pass variables. 
    #print('parse_position called')
    TXY=[]
    response = requests.request("POST", url, json={"query": Q.boss_Damage_taken_query, "variables":V}, headers=token).json()
    #print('WHATS IN HERE:', response)
    for i in response['data']['reportData']['report']['events']['data']:
            if 'x' in i: TXY.append([i['timestamp'],i['x'],i['y']])
    NPT=response['data']['reportData']['report']['events']['nextPageTimestamp']
    #print(NPT)
    return ([NPT,TXY])



#grabs the start time, end time, and encounter ID for the slection
def get_start_end_EID(selection):
    #print('get_start_end_EID called')
    #print('selection=',selection)
    response = requests.request("POST", url, json={"query": Q.get_start_end_EID_query, "variables":V}, headers=token).json()
    for i in response['data']['reportData']['report']['fights']:
        #print(i['name'])
        if selection == i.get('name'):
            out=[i['startTime'],i['endTime'],i['encounterID']]
            print(out)
            V['start']=out[0]
            V['end']=out[1]
            V['EID']=out[2]
            return out #format is [start,end,encounterID]


def TXY_to_TM(TXY,interval=.2500): #formats the Timestamps and the coordinates into a usable format of [time,total distance moved during that interval]
    #print(' TXY to TM called',len(TXY))
    #for i in TXY: print(i)
    Current_interval=[]    
    initial = float(TXY[0][0])
    #initial cleanup and formatting of TXY:
    for i in range (0,len(TXY)):
        #convert time into seconds, and start the counting at 0, rather than at UTC
        TXY[i][0]=round((float(TXY[i][0])-initial)/1000,4)
        TXY[i][1]=round(int(TXY[i][1])/100,2)
        TXY[i][2]=round(int(TXY[i][2])/100,2)
    TM=[] #holds the time that's elapsed, and how much movement has occurred in the formaat [T,M]. 
    for i in TXY:
        #print(i)
        if len(Current_interval) ==0:
            Current_interval.append(i)
        else:
            if i[0] - Current_interval[0][0] <= interval:
                Current_interval.append(i)
            else:
                Xs=[]
                Ys=[]
                for k in Current_interval:
                    #print(k[1],k[2],Current_interval[0][1],Current_interval[0][2])
                    Xs.append(round(abs(abs(k[1])-abs(Current_interval[0][1])),2))
                    Ys.append(round(abs(abs(k[2])-abs(Current_interval[0][2])),2))
                dxy= round(math.sqrt(max(Xs)**2 + max(Ys)**2),2) #good ole pythagorean theorem. thanks 7th grade math class.
                TM.append([Current_interval[0][0],dxy])
                Current_interval=[]
    #for i in TM: print(i)
    return TM



    #move_threshold:    the minimum distance the move must cover to be inclduded in the results (unit it yards)
    #Twindow:           time between moves before the movement is confirmed as having ended (unit is seconds)
def movement_intervals(TM,move_threshold=3,Twindow=2 ):
    #print('movement_intervals called')
    #print('in Move_intervals',len(TM))
    moves=[]
    mStart=0
    mRunTot=0
    mEndFinder=0
    for i in range (0,len(TM)):
        if i==0: #is this the very first iteration of the loop?
            mStart=TM[i][0] 
            mRunTot=TM[i][1]
        else: #if  it's NOT the very first itteration
            if TM[i][1]>0: # was there any movement in this interval?
            #if YES:
                if mRunTot==0:#is it new movement?
                        mStart=TM[i][0]
                        mEndFinder = TM[i][0]
                        mRunTot=TM[i][1]
                else:#or is it a continuation
                        mEndFinder = TM[i][0]
                        mRunTot+=TM[i][1]
            #if no movement this interval:
            else: 
                if TM[i][0]-mEndFinder >= Twindow: #has there been no movement for 3 seconds?
                #IF NO MOVEMENT:
                    if len(moves)==0:#if it's the first move, just slap that shit into moves
                        moves.append([round(mStart,2),mEndFinder,round(mEndFinder-mStart,2),round(mRunTot,2)])
                        mRunTot=0
                    #if it's NOT the first move  
                    elif moves[-1][0] != mStart: #making sure that the line hasn't been added yet (for some reason it likes to add multiples of the same movement if I dont add this check)
                        if mRunTot>=move_threshold: #has the total movement been greater than the threshold? (done to minimize tiny moves that are meaningless)
                            #if yes, then slap it into moves
                            moves.append([round(mStart,2),mEndFinder,round(mEndFinder-mStart,2),round(mRunTot,2)])
                        mRunTot=0   #clear mRunTot because this move is over. regardless of whether or not we saved the move.                
    return moves

def get_boss_IDs():#NEED TO FIX THE BOSSES THAT AREN'T THE SAME NAME AS THE ENCOUNTER: IE COUNCIL OF BLOOD DOEESNT HAVE BOSS ENTITIES NAMED COUNCIL OF BLOOD
    #print('get_boss_IDs() called')
    
    #print('yes i actually fucking use this for some reason')
    response = requests.request("POST", url, json={"query": Q.get_boss_IDs_query, "variables":V}, headers=token).json()
    #print('WHATS IN HERE:', response)
    #there's probably a nicer way of doing this, but it seems kinda low prio. 
    names=['Shriekwing','Huntsman Altimor','Hungering Destroyer','Lady Inerva Darkvein',"Sun King's Salvation","Artificer Xy'mox",'Council of Blood','Sludgefist','Stone Legion Generals','Sire Denathrius']
    boss_npcIDs =    [[],[],[],[],[],[],[],[],[],[]]
    boss_local_IDs = [[],[],[],[],[],[],[],[],[],[]]
    fights =         [[],[],[],[],[],[],[],[],[],[]]
    for i in response['data']['reportData']['report']['masterData']['actors']:
        
        if i.get('name')in names:
            boss_npcIDs[names.index(i.get('name'))]=i.get('gameID')
            boss_local_IDs[names.index(i.get('name'))]=i.get('id')
            fights[names.index(i.get('name'))]=i.get('name')
    return [boss_npcIDs,boss_local_IDs,fights]


#THE FUNCTION THAT ORCHASTRATES GETTING THE POSITIONING DATA
#the flow:
#   1) find what boss the user picked, then find the local encounter ID that the report is using for that kill using get_boss_IDs
#   2) find the start and end of that encounter using get_start_end_EID
#   3) generate the TXY list using parse_position. this frequently takes multiple queries so it's done in a while loop 
#
def data_parsing_handler(report):
    #print('data parsing handler called')
    global start, end #CAN PROBABLY DELETE #making all these variables global feels like it's not what I'm 'supposed to do', but I was lazy and it works.#CAN PROBABLY DELETE
    global local_boss_id #i might have to keep this, so ive sectioned it off.
    #determine the start/end time for that kill
    pick=str(boss_selected.get())
    #print(pick)
    get_start_end_EID(pick) #MAKING SURE THAT THE DICT HAS BEEN UPDATED
    #grab all the position data for that boss
    PP=parse_position()
    NPT,TXY=PP[0],PP[1]
    #print(NPT)
    original_start=V['start']
    #print(original_start)
    while NPT != None:
        ph=parse_position()
        V['start']=ph[0]
        for i in ph[1]:
            TXY.append(i)
    V['start'] = original_start #this way I dont have to requery the starttime of the fight.
    return TXY

    

def drop_down_maker(creatureIDs):
    #print('drop down maker called')
    #print(creatureIDs)
    global boss_selected
    dd=[]
    for i in creatureIDs:
            if len(i) > 0:
                dd.append(i)
    #print(dd)
    boss_selected=StringVar(root)
    dropdown=OptionMenu(root,boss_selected,*dd)
    dropdown.pack()
    dropdown.place(x=10, y=50)
    
    encounterLabel = Label(root, text = "Select Encounter to parse")
    encounterLabel.pack()
    encounterLabel.place(x=0, y=30)
    
    bGO = Button(root,text ='Generate SimCraft Script',command = GO)
    bGO.pack()
    bGO.place(x=300, y = 50)
    
    #return boss_selected


def grab_report_code():
    global report, local_IDs
    url=URL_entry.get()
    kek=url.split('https://www.warcraftlogs.com/reports/')
    report=kek[1].split('#')
    V['code']=report[0]
    #print(report)
    local_IDs=get_boss_IDs()
    drop_down_maker(local_IDs[2])
    
#ONCE YOU CLICK GENERATE SCRIPT:   
def GO(): 
    boss_selected.get()
    print(boss_selected.get())
    TXY=data_parsing_handler(report) #GENERATE TXY
    #print(len(TXY))
    out=parse_to_simc_handler(TXY) #THEN SEND IT TO GET CLEANED UP AND TURNED INTO A SIMC SCRIPT
    T.delete(1.0,tk.END)
    for i in out:
        T.insert(tk.END, str(i)+str('\n'))

#
# OUTPUTTING STUFF INTO SIMC RAID_EVENTS:
#

#takes the data from TXY, then converts it into a usable format (via TXY_to_TM), then slaps the data into the simcraft format
def parse_to_simc_handler(TXY):
 #I FEEL LIKE THESE LISTS WOULD BE BETTER PLACED OUTSIDE THE FUNCTION, BUT IDK.
    FIGHTS_WITH_ADDS=[2418,2402,2406,2412,2417,2407]# list contains encounterIDs for: HUNTSMAN,INNERVA,SUN KING, COUNCIL, SLG, DENATHRIUS.
    FIGHTS_WITH_DMG_AMPS=[2399]#sludgefist
    FIGHTS_WITH_BOSS_IMMUNES=[2398,2412,2417,2407]#shriekwing, sunking,council,SLG, denathrius
    FIGHTS_WITH_EXTRA_PLAYER_MOVEMENT=[2383,2399] #hungering, sludgefist
    #get_start_end_EID(boss_selected.get())
    formated_events=[] 
    moves=movement_intervals(TXY_to_TM(TXY))
    for i in moves: formated_events.append(str("raid_events+=/movement,cooldown=9999,distance=")+str(i[3])+str(",duration=")+str(i[2])+str(",first=")+str(i[0])) #generate the normal movement script

 #check if other fight specific overrides are needed, and then call the functions to handle them:
    if V['EID'] in FIGHTS_WITH_ADDS:
        adds=ADDS()
        for i in adds:
            formated_events.append(str("raid_events+=/adds,count=1,first=")+str(i[0])+str(",duration=")+str(i[1])+str(",cooldown=9999"))

    if V['EID'] in FIGHTS_WITH_EXTRA_PLAYER_MOVEMENT:
        extra_moves=EXTRA_PLAYER_MOVENTS()
        for i in extra_moves: formated_events.append(str("raid_events+=/movement,cooldown=9999,first="+str(i[0])+str(",duration=")+str(i[1])+str(",direction=away")))

    if V['EID'] in FIGHTS_WITH_DMG_AMPS:
        dmg_amps=DMG_AMP()
        for i in dmg_amps: formated_events.append(str("raid_events+=/vulnerable,cooldown=9999,first=")+str(i[0])+str(",duration=")+str(i[1])+str(",multiplier=")+str(i[2]))
        
    if V['EID'] in FIGHTS_WITH_BOSS_IMMUNES:
        #print('wtf why am i here?',V['EID'] )
        immunes=IMMUNE_PHASES()
        for i in immunes: formated_events.append(str("raid_events+=/invulnerable,cooldown=9999,first=")+str(i[0])+str(",duration=")+str(i[1])+str(",retarget=")+str(i[2]))

    return formated_events

##########################################
##  ENCOUNTER SPECIFIC VARIANCES BELOW  ##
##########################################


def grab_events(EventType,spell_ID,sendDuration=1): # RESTRUCTURE SO THAT I DON'T HAVE TO PASTE THE SAME SHIT 82 TIMES
    V['spellID'] = spell_ID
    TYPE='' #used for selecting what the important lines are (cause every event has a line for when it started, and a line for when it ended)
    events=[]
    EventStarts=[]
    if EventType == 'buff':
        QUERY = Q.Buff_detector_query
        TYPE='applybuff' 
    elif EventType == 'cast':
        QUERY =Q.cast_detector_query
        TYPE='begincast' 
    elif EventType == 'debuff':
        QUERY =Q.debuff_detector_query
        TYPE='applydebuff'
    elif EventType == 'buff_END':
        QUERY = Q.Buff_detector_query
        TYPE='removebuff'
        
    response = requests.request("POST", url, json={"query": QUERY, "variables":V}, headers=token).json()

    for i in response['data']['reportData']['report']['events']['data']:
            if i['type'] == TYPE:
                EventStarts.append(round((i['timestamp']- V['start'])/1000,1))    
    if sendDuration==1: #if a duration calc is wanted (it usually is, and is default)
        k = response['data']['reportData']['report']['events']['data']
        duration  = round((k[1]['timestamp'] - k[0]['timestamp'])/1000,2) #ARBITRARILY PICKING THE FIRST EVENT TO BE WHAT DETERMINES THE DURATION.
        for i in EventStarts:
            events.append([i,duration])
        return events # format is [[timestamp,duration], [timestamp,duration].....]
    
    else: return EventStarts #otherwise just send all the starts



#TO DO: DETECT MULTIPLE ADDS SPAWNING AT ROUGHLY THE SAME TIME AND MERGE THEM INTO A SINGULAR ADDSPAWN EVENT (SO MULTIPLE RAIDEVENTS AREN'T NEEDED FOR EACH WAVE OF ADDS)
def ADDS():
    Adds=[]
    #print('called adds')
    response = requests.request("POST", url, json={"query": Q.add_detector_query, "variables":V}, headers=token).json()
    #generating raid_events at minimum requires knowing: 1) when the add spawned 2) how long the add was alive for
    for i in response['data']['reportData']['report']['table']['data']['entries']:
        print(i)
        if V['EID'] == 2418:
            if i['name'] != 'Huntsman Altimor':
                spawn=round(((i['timestamp'] - i['deathWindow']) - V['start'])/1000,2)#takes timestamp(the point of death) and deathwindow window(a duration) and finds the timestamp of when the add spawned
                duration=round( i['deathWindow']/1000,2) #also converting the UTC timestamps into time since start of encounter
                if duration > 1.0: #if the add is alive for longer than 1 seconds (done to prevent critter deaths from showing up and adding pointless raidevent lines)
                    Adds.append([spawn,duration])
            
        else:
            if i['type'] != 'Boss':
                spawn=round(((i['timestamp'] - i['deathWindow']) - V['start'])/1000,2)#takes timestamp(the point of death) and deathwindow window(a duration) and finds the timestamp of when the add spawned
                duration=round( i['deathWindow']/1000,2) #also converting the UTC timestamps into time since start of encounter
                if duration > 1.0: #if the add is alive for longer than 1 seconds (done to prevent critter deaths from showing up and adding pointless raidevent lines)
                    Adds.append([spawn,duration])
    return Adds


#when immune phases are detected, this function pulls that information from the report 
def IMMUNE_PHASES():
    if V['EID'] == 2398: #SHRIEKWING 
        immunes = grab_events('buff',328921)
        retarget=0
        
    for i in immunes:
        i.append(retarget)
    return immunes


#for hungering/sludgefist, all (or at least, all melee) players runs away from the boss while the boss remains stationary, so default method of tracking boss movement is not sufficient.
def EXTRA_PLAYER_MOVENTS():
    moves=[]
    if V['EID'] == 2399: #if it's sludgefist:
        moves = grab_events('cast',332318)  ##sludgefists stomp

    elif V['EID'] == 2383: #if it's hungering:
        consume_pt1=grab_events('cast',334522,sendDuration=0) #starts of consume casts
        consume_pt2=grab_events('buff_END',334522,sendDuration=0) #ends of consume channel, 
        for i in range (0,len(consume_pt1)):
            moves.append([consume_pt1[i],round(consume_pt2[i]-consume_pt1[i],1)])
            
    return moves 
 

#sludgefist takes increased damage every time he smashes a pillar. currently this is the only fight like this, but this should be future proofed for upcoming content
def DMG_AMP():
    if V['EID'] == 2399: #if it's sludgefist
        damage_amps = grab_events('buff',331314) #sludgefirst pillar smash buff
        DAMAGE_MULTIPLIER = 2 #boss takes 100% extra damage
        
    for i in damage_amps:
        i.append(DAMAGE_MULTIPLIER)
    return damage_amps



#this is a variance designed to handle creating overrides for encounters that give you special buffs
#e.g.: the haste buff granted by the dance phase on council
def CUSTOM_BUFFS():
    pass







#########################################################################################################################################################
#########################################################################################################################################################
#SPAWNING THE GUI, AND GETTING EVERYTHING INITIALIZED HAPPENS BELOW
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
    
OUTPUT_TEXT = ''
root = Tk()
root.geometry('650x600')


T = Text(root, height = 30, width = 80) 
T.pack()
T.place(x=2, y=100)
T.insert(tk.END, OUTPUT_TEXT)

entrylabel=tk.Label(root, text="WCL Log URL:")
entrylabel.pack()
entrylabel.place(x=0,y=0)
#the entry box
URL_entry = tk.Entry(root,width=50)
URL_entry.pack()
URL_entry.place(x=80,y=1)

bGRAB = Button(root, text="Grab Log", command=grab_report_code)
bGRAB.pack()
bGRAB.place(x=385)




mainloop()




#############################################################################################################


'''
THINKING OUT LOUD:

SLG:
    a seemingly straight forward way to simulate the bosses is to treat is as 1 boss with immune phases + an add that spawns for p3 that's treated as the 2nd boss.
    the  obvious problem with this is that it will not accurately simulate condemns >80% usability.
    it's possible to set particular unit's initial HP% (this is what raidbots does for execute patchwork sims)
        enemy="NAME"
        enemy_initial_health_percentage="20"
    it's not immediately clear how to use this in conjuction with creating the "boss" add for p3. but I see no obvious reasons why there wouldn't be a way to do it.
    assuming that works out, we then gotta deal with the fact that after each intermission, you get a new boss, and therefore it effectively "heals" back to full HP.
    There might be a way to implement a raid_event to heal the boss during the immunity phases, but I am currently unsure.

    
MERGING MULTIPLE ADD SPAWNS:
 right now every add spawn gets it's own raidEvent.
 this is fine for fights with a few adds (huntsman/innerva), but will make fights with lots of adds very messy (easy/obvious example is echos of sin on denathrius p1)
 the first potential solution to this that comes to mind is to collect all the add spawns as we currently do, but to compare the spawn times of the adds in the list, and then group all adds that spawn within a certain time window
 the obvious way of determining the duration of a group of adds is to calculate the average (mean or median) lifespan of the adds in that grouping. if we want to be fancy, simcraft has functionality for creating a distribution of durations given a mean and standard deviation
 One solvable complicating factor in doing this is when multiple adds spawn that have significantly different HPs, such that they die at very different times. the most obvious example of this is innerva, so some extra consideration should be made


SIMULATING "RANDOM RUN-OUT" MECHANICS:
any mechanic where you have to run away from the boss, that doesn't happen to everyone simultaneously. you know the type. run the debuff out, drop the puddle over here, bla bla bla.
YES WE COULD IMPLEMENT THE RANDOM RUN OUT MECHANICS AND STUFF. NO I DON'T WANT TO.
while that technically makes the simulation 'more accurate' doing so just adds more variance/randomness that conflicts with what the entire point of this project is meant to accomplish 
 that is:
   1)  trying to generate an accurate approximation of what your gear is capable of on a given fight. This is meant to be the upperbound, as it simulates perfect play. It makes no sense to me to inject variances that will make generating that upper bound less accurate
   2)  optimizing gear decisions on a per fight basis. my gut feeling is that random runout mechanics are extremly unlikely to have any meaningful impact on gearing decisions. 
that said, if we ever get bored enough to implement random run out mechanics, then I would expect there to be a toggle to turn them on and off.    



PIPE-DREAMING:
    1)MERGING OF LOGS/SCRIPTS
    TO GENERATE SIMPLE PRESETS @ VARIOUS KILL TIMES 
        once this tool is fully operational for individual logs, I'd be interested trying to generate presets for individual fights by sampling a large set of logs and "averaging" them together such that it
        reduces the 'noise' present in the data of individual logs. the primary benefit to this is that it would allow users to adjust the fight lengths while maintaining the accuracy of the simulation.
        That said, creating a system to do this seems like a monumental undertaking, and seems like it could potentially be beyond what my tiny brain is capable of. 


        
    2)CANVAS+TIMELINE --> SIMCRAFT TOOL
        a major limitation of the strength this project is that it requires you to have done the thing. That is, there must be logs of the strategy in action, and to get an accurate simulation it must have been a kill.
        Not all strategies are exact copies of what other guilds are doing, and if you can't find a log of someone using a sufficiently similar strategy, then you're not going to have an accurate simulation.
        more simply: The WCL->Simc project is able to optimize, but is incapable of producing innovations.
        

        My idea for overcomming this limitation would be creating an entirely different tool.
        the premise would be to create a canvas tool like raidplan.io, which is a tool that provides overhead images of boss rooms, and allows users to overlay images of the boss, of adds, and of player marker.
        raidplain.io is primarily used for creating visual aids that help brainstorm/explain boss strategies. This is especially valuable for guilds when they are progressing on a boss.

        This tool would have all of that functionality, but it would also have a timeline. This would allow users to set the boss position at certain times,
        so they can say at time t1 we move the boss from A to B. and then at time t2 we move the boss from B to C. at time t3 we get adds that spawn,etc.
        once this timeline has been created by the user, the tool would be able to generate the simcraft overrides to simulate that strategy in Simcraft.

        extrapolating from this initial functionality, there is much that could be done to maximize the benefit of the tool:

            you could allow for placing of movement CDs (windrush/roar  ) (something not currently available in raidplan.io)
            if melee/ranged don't just follow the boss movements you could force them to move in particular ways at particular times
            you could specify your composition, and simulate the raid using that composition via the simcraft preset gearsets.
                    doing this for multiple strategy options would enable you to pick the most optimal one for your raids DPS.
            It would give world-first guilds the ability to simulate their strategies for upcoming bosses.
            
        
        The biggest problem for me personally is that I have precisely zero experience making anything remotely like a cavnas tool, and I have no real sense of how/where to begin creating a tool like this. 

        


    
    

'''
