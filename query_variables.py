#hard coding in some ph variables so I can slap shit in there while building
HARD_CODED_REPORT_ID_PLZ_REMOVE="Nvh1C3qyb9wKA4GB"
start=5357463
end=5695227
EID=2406
Local_npcID=104
spellID=1
npcID=332318


#THIS CAN BE THE MASTER LIST OF ALL VARIABLES THAT GET USE
variables={ 
    "code": HARD_CODED_REPORT_ID_PLZ_REMOVE,
    "start":start,
    "end":end,
    "EID":EID,
    "npcID":npcID,
    "Local_npcID":Local_npcID,
    "spellID":spellID,
    }







'''
LOL SO THIS IS FUCKING USELESS AND SEEMS LIKE I WILL NEVER NEED IT BUT JUST IN CASE IM LEAVING IT HERE


BDTvars=[str(V['code']),V['start'],V['end'],V['npcID'],V['Local_npcID']] #BOSS DAMAGE TAKEN VARIABLES
CodeOnly = V['code']                                                #get_boss_IDs AND get_start_end_EID only need the report ID variable
CBDvars =[V['code'],V['start'],V['end'],V['spellID']]               #variables for cast/buff/debuff(CBD) detection
Addsvars =[V['code'],V['start'],V['end']]                           #variables for the adds detection query
'''
