boss_Damage_taken_query="""
query ($code: String! $start: Float $end: Float $EID: Int  $Local_npcID: Int ){
  reportData {
    report(code: $code){ 
     events(
      startTime: $start, 
      endTime: $end, 
      encounterID: $EID 
      dataType:  DamageTaken, 
      killType: Kills, 
      hostilityType: Enemies 
      sourceInstanceID: $Local_npcID 
      abilityID: 1,
      includeResources: true 
      limit: 10000
    ){data nextPageTimestamp}
    }}
}
"""

get_start_end_EID_query="""
query ($code: String!){
    reportData {
    report(code: $code)
      {fights( killType: Kills)
        {
          name 
          startTime 
          endTime 
          encounterID
        }
      }
    }
}
"""

get_boss_IDs_query="""
query($code: String!){
  reportData {
    report(code: $code) {
      masterData{
        actors{name id gameID subType}}
    }
  }
}
"""

add_detector_query="""
query ($code: String! $start: Float $end: Float ){
    reportData {
    report(code: $code){ 
     table( 
      startTime: $start,
      endTime: $end,
      hostilityType: Enemies
      dataType: Deaths
    )
    }}}


"""
Buff_detector_query="""
query ($code: String! $start: Float $end: Float $EID: Int $spellID: Float ){
    reportData {
    report(code: $code){ 
     events(
      startTime: $start, 
      endTime: $end, 
      encounterID: $EID 
      dataType:  Buffs 
      hostilityType: Enemies 
      abilityID:$spellID 
    ){data}
    }}}

"""
debuff_detector_query="""
query ($code: String! $start: Float $end: Float $EID: Int $spellID: Float ){
    reportData {
    report(code: $code){ 
     events(
      startTime: $start, 
      endTime: $end, 
      encounterID: $EID 
      dataType:  Debuff 
      hostilityType: Enemies 
      abilityID:$spellID 
    ){data}
    }}}
"""
cast_detector_query="""
query ($code: String! $start: Float $end: Float $EID: Int $spellID: Float ){
    reportData {
    report(code: $code){ 
     events(
      startTime: $start, 
      endTime: $end, 
      encounterID: $EID 
      dataType: Casts   
      hostilityType: Enemies 
      abilityID:$spellID 
    ){data}
    }}}
"""




