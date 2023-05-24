beasely_patterns = [
    r"mali\w*\sbea\w*\b",
    r"(?<!malik\s)\bbeas(?:l|e)\w*\b",
    r"(?<!malik\s)bbeastl\w+\b"
    ]

beasely_patterns_trade = [
    r"\bmalik\b(?!\sbea\w*|\smon\w*\b)"
]

beasely_trade_date = '2023-02-09'

russ_patterns = [
    r"\b\w*russ\w*\s\w*broo\w*\b",
    r"\brus\w*\swes\w*\b",
    r"(?<!\bruss\s)(?<!\brussel\s)(?<!\brussell\s)\bwestb\w*\b",
    r"(?<!\bruss\s)(?<!\brussel\s)(?<!\brussell\s)\b\w*tbrook\b",
    r"\bbrodie\b",
    r"\bwb\b",
    r"\brw\b",
    r"\bruss\b", 
]

russ_trade_date = '2023-02-09'

dennis_patterns = [
    r"\bden\w*\ssch\w*\b",
    r"\bdennis\b(?!\ssch\w*\b)(?!\sshr\w*\b)(?!\sscr\w*\b)(?!\sthe\smen\w*\b)",
    r"\bden\w*\sshr\w*\b",
    r"\bden\w*\sscr\w*\b",
    r"\bdenis\b",
    r"\bdennis\s\the\smen\w*\b",
    r"\bds\b", 
    r"(?<!\bdennis\s)(?<!\bdenis\s)\bschro\w*\b",
    r"(?<!\bdennis\s)(?<!\bdenis\s)\bshro\w*\b",
    r"(?<!\bdennis\s)(?<!\bdenis\s)\bschrö\w*\b"
]

wenyen_patterns=[
    r"\bwen\w*\sgab\w*\b",
    r"\bweny\w*\b(?!\sgab\w*\b)",
    r"(?<!\bwenyen\s)(?<!\bwenyan\s)(?<!\bwenyon\s)\bgabriel\b",
    r"(?<!\bwenyen\s)(?<!\bwenyan\s)(?<!\bwenyon\s)\bgabriels\b",
    r"\bwg\b"
]

reaves_patterns=[
    r"\baust\w*\sre(?:e|a)\w*\b",
    r"\bausti\w*\b(?!\sre(?:e|a)\w*\b)",
    r"\bhillb\w*\s(?:k|m)\w*\b",
    r"\baust\s{0,1}him\b",
    r"\bar\s{0,1}\d+\b",
    r"\bar\b(?!\s{0,1}\d+\b)",
    r"(?<!\baustin\s)(?<!\baust\s)(?<!\baust\shim\s)(?<!\bausthim\s)\breav\w+\b",
    r"\bleaustin\b",
    

]

bron_patterns=[
    r"\bleb\w*\sjam\w*\b",
    r"\bleb\w*\b(?!\sjam\w*\b)",
    r"\blegm\w*\b",
    r"\blegoat\b",
    r"\blefuc\w*\b",
    r"\blerbon\w*\b",
    r"\bledad\b",
    r"\blecoa\w*\b",
    r"\bbron\b",
    r"\bking\sja\w*\b",
    r"👑",
    r"(?<!bronny\s)(?<!big\sgame\s)(?<!lebron\s)(?<!king\s)james\b(?!\sharden|\sdolan|\sennis|\swiseman|\sworthy)" ,
    r"\blbj\b",

]

ad_patterns = [
    r"\bant(?!o)\w*\sda\w*\b",
    r"\bad\b",
    r"(?<!carmelo\s)\banth\w*\b(?!\sedward|\stowns|\sdaniels|\sdavis|\sirwin|\sday|\sbennett|\shopkins|\sbrown)",
    r"(?<!the\s)\bbrow\b",
    r"\bthe\s{0,1}brow\b"
    r"day\s\w{1,3}\sdav\w*\b",
    r"(?<!anthony\s)(?<!day\sto\s)\bdavis\w*\b",
    r"〰️"
]


vando_patterns = [
    r"\bjar\w+\svand\w*\b",   
    r"(?<!jarred\s)(?<!jared\s)(?<!darth\s)\bvand\w*(?!r)\b(?!\sblue)",
    r"\bjarred\b(?!\svand\w*\b)",
    r"\bjared\b(?!\svand\w*\b)",
    r"\bjared\b(?!\svand\w*\b)(?!\sdudley\b)(?!\sbutler)"   
    r"\bdarth\svander\b"
]


lonnie_patterns=[
    r"\blon\w*\swal\w*\siv\b",
    r"\blon\w*\swal\w*\b(?!iv\b)", 
    r"\blon(?:n|i)\w*\b(?!\swal\w*\b)(?!\ssky)",
    r"(?<!lonnie\s)\bwalk\w*\siv\b",
    r"(?<!lonnie\s)(?<!antoine\s)(?<!sky\s)\bwalker\b(?!\siv\b)(?!\skess\w*\b)",  
    r"sky\s{0,1}walker\w*\b",
    r"\blw\b"
]

nunn_patterns=[
    r"\bkend\w*\sn\w*\b",
    r"kendr\w*\b(?!\slamar|\sperkins|\snun\w*\b|\snone)",
    r"(?<!kendrick\s)\bnunn\b",
    r"(?<!kendrick\s)\bnun\b"
    r"kendr\w*\sb\w*\b",
    r"kenb\w*\b"
]

bev_patterns=[
    r"\bpat\w*\sbev\w*\b",
    r"(?<!st\s)patric\w*\b(?!\sbev\w*\b)(?!\swill\w*\b)(?!\sewing\b)(?!\smaho\w*\b)",
    r"(?<!\bpatrick\s)(?<!\bpat\s)\bbev\w*\b",
    r"\bpb\b"
]

tbj_patterns=[
    r"\btro\w*\sbr\w*\sj\w{0,1}\b",
    r"\btro\w*\sbrow\w*\b(?!\sj\w{0,1}\b)",
    r"(?<!troy\s)\bbrown\sjr\b",
    r"\btbrown\b",  
    r"\btroy\b(?!\sbrow\w*\b)",  
    r"\btbj\b",
    

]

rui_patterns=[
    r"\brui\sh(?:a|i)(?:c|m|b)\w*\b",
    r"(?<!rui\s)\bhach\w*\b",
    r"\brui\b(?!\sh(?:a|i)(?:c|m|b)\w*)",
    r"(?<!ck\s)\brh\b",
]

tb_patterns=[
    r"\bthom\w*\sbry\w*\b",
    r"\btom\w*\sbry\w*\b",
    r"(?<!isiah\s)(?<!isaiah\s)(?<!cam\s)(?<!tristan\s)\bthomas\w*\b(?!\sbry\w*\b)",
    r"\btb\b",
    r"(?<!\bkobe\s)(?<!\bbean\s)(?<!cking\s)(?<!\bgigi\s)(?<!\bkobeeee\s)(?<!\bvanessa\s)(?<!\bmrs\s)(?<!mas\s)\bbryant\b",
    r"\bt.{0,1}bryan\w*\b"
]

max_patterns=[
    r"\bmax\schr\w*\b",
    r"\bmax\scr\w*\b",
    r"(?<!max\s)\bchristie\b",
    
]

jta_patterns=[
    r"\bjta\b",
    r"\bj\w*\stos\w*\sand\w*\b",
    r"(?<!juan\s)(?<!j\s)tosc\w*\sande\w*\b"
    r"\bjuan\st(?:o|a|e|u)sc\w*\b(?!ande\w*)",
    r"(?<!juan\s)\bt(?:o|a|e|u)sc\w*\b(?!\sand\w*\b)",
    r"\bjuan\stos\w*\b(?!\sande\w*)"
    
]

mo_patterns=[
    r"\bmo\s\w*mba\w*\b",
    r"(?<!mo\s)b\w*mba\b",
    r"\bmo\b(?!\s\w*mba\w*)",
    r"(?<!no\s)\bmo\b(?!\s\w*mba\w*|\swag\w*|\shark\w*|\swill\w*)" 
    
]

dlo_patterns=[
    r"\bd\w{0,1}ang\w*\srus\w*\b",
    r"\bd\srus\w*\b",
    r"\bd\w{0,1}angelo\b(?!\sruss\w*\b)",
    r"\bdlo\b",
    r"\bdloading\b"
]

dlo_patterns_trade=[
    r"(?<!gelo\s)(?<!d\s)(?<!bill\s)\brussel\w{0,1}\b(?!\swest\w*|\swil\w*)"
]


dlo_trade_date = '2023-02-09'

jeanie_patterns=[
    r"\bjean(?:n|i)\w*\sbus\w*\b",
    r"\bjean(?:n|i)\w*\b(?!\sbus\w*)",
    r"(?<!jeannie\s)(?<!jeanie\s)(?<!dr\s)(?<!jerry\s)(?<!jim\s)(?<!jesse\s)(?<!joey\s)buss\b(?!\sfamily|\schild\w*|\sbo\w*|\sbro\w*|\skid\w*)",
    r"\bour\sowner\b",
]

rob_patterns=[
    r"\brob\w*\spel\w*\b",
    r"(?<!rob\s)\bpelin\w*\b",
    r"(?<!robert\s)\bpelink\w*\b",
    r"\brob\slowe\b",
    r"(?<!shot\s)\brob\b(?!\spelin\w*|\sparker)",
    r"\bour\sgm\b",
    
]

ham_patterns=[
    r"\bdarv\w*\sham\w*\b",
    r"\bdarw\w*\sham\w*\b",
    r"(?<!darvin\s)(?<!darwin\s)\bham\b",
    r"(?<!darvin\s)(?<!darwin\s)\bhamm\b",
    r"\bour\scoach\b(?!\sdarv\w*\b|\sham\b)",
    r"\brookie\scoach\b(?!\sdarv\w*\b|\sham\b)",
    r"\byear\scoach\b(?!\sdarv\w*\b|\sham\b)",  
    
]

lakers_patterns=[
    r"\bthis\steam\w{0,1}\b",
    r"\bour\steam\w{0,1}\b",
    r"\bthe\slakers\b",
    r"(?<!\bthe\s)(?<!\bdaily\s)(?<!\br\s)\blakers\b(?!\sreddit\b)(?!\sjersey)(?!\sfan\w*\b)"
    
]



## create dict w patterns ##
index = 0
entities = {}
for k, v in full_names.items():
    entities[k] = {}
    entities[k]['full_name'] = v
    entities[k]['patterns'] = patterns[index]
    entities[k]['trade_patterns'] = []
    entities[k]['trade_date'] = None
        
    index += 1
entities


new_words_emojis = {
    'face_with_tears_of_joy':1.0, 'rolling_on_the_floor_laughing': 1.0, 'fire_emj': 3.0, 'skull':-1.0,
    'hundred_points': 2.5, 'face_with_steam_from_nose': 3.0, 'eyes_watching':2.0, 'folded_hands':0.5,
    'folded_hands_medium_skin_tone':0.5, 'thinking_face':0.0, 'clown_face':-4.0, 'man_facepalming_yellow':-2.55,
    'goat':3.5, 'crown':3.0, 'man_shrugging':0.0, 'man_shrugging_medium_skin_tone':0.0,       
    'man_facepalming_medium_dark_skin_tone':-2.5, 'pensive_face':-3.0, 'face_with_rolling_eyes':-1.5, 'red_heart_one':3.85,
    'smirking_face':1.5, 'flexed_biceps':3.5, 'man_facepalming_medium_skin_tone':-2.5, 'skull_and_crossbones':-1.0,
    'man_shrugging_light_skin_tone':0.0, 'flushed_face':2.0, 'clapping_hands':1.0, 'exploding_head':2.0,
    'man_facepalming_light_skin_tone':-2.5, 'cold_face':1.5, 'handshake':0.0, 'winking_face':2.0, 'trophy':3.8,
    'man_shrugging_medium_dark_skin_tone':0.0, 'woman_shrugging_medium_dark_skin_tone':0.0, 'white_heavy_check_mark':2.2,
    'face_vomiting':-3.5, 'crossed_fingers_medium_skin_tone':0.5, 'crossed_fingers':0.5, 'pleading_face':1.0,
    'neutral_face':-2.0, 'billed_cap':-1.0, 'shushing_face':0.0, 'nerd_face':0.0, 'raising_hands':2.75, 'unamused_face':-3.3,
    'face_with_raised_eyebrow':0.7, 'pile_of_poo':-3.8, 'speaking_head':0.0, 'nauseated_face':-3.5, 'woozy_face':0.7,
    'person_shrugging':0.0, 'broken_heart':-2.8, 'person_facepalming':-2.5, 'folded_hands_medium_dark_skin_tone':0.5,
    'money_bag':2.5, 'hot_face':1.0, 'flexed_biceps_medium_dark_skin_tone':3.5, 'victory_hand':1.5, 
    'folded_hands_medium_light_skin_tone':0.5, 'waste_basket':-3.85, 'litter_in_bin_sign':-3.85, 'woman_shrugging':0.0,
    'face_screaming_in_fear':0.0, 'zany_face':0.4, 'pouting_face':-2.0, 'flexed_biceps_medium_skin_tone':3.5,
    'folded_hands_light_skin_tone':0.5, 'locked':0.0, 'relieved_face':2.8, 'expressionless_face':-1.5, 
    'thumbs_up_medium_light_skin_tone':2.5, 'sleepy_face':-1.8, 'squinting_face_with_tongue':1.9, 'oncoming_fist':2.8,
    'flexed_biceps_medium_light_skin_tone':3.5,
    'icey': 2.0, 'snowflake_biggest':2.0, 'direct_hit':2.0, 'face_with_symbols_on_mouth':-1.5, 'ring':1.5, 'sweat_droplets':2.5,
    'thumbs_up':2.5, 'thumbs_up_light_skin_tone':2.5, 'cross_mark':0.0, 'winking_face_with_tongue':2.0, 'drooling_face':2.8,
    'index_pointing_up':0.0, 'birthday_cake':0.5, 'man_facepalming_dark_skin_tone':-2.5, 'thumbs_up_medium_skin_tone':2.5,
    'crossed_fingers_light_skin_tone':0.5, 'bomb':-1.0, 'clapping_hands_medium_skin_tone':1.0, 'rocketship':3.5,
    'crossed_fingers_medium_dark_skin_tone':0.5, 'face_with_open_mouth':2.0, 'backhand_index_pointing_up':0.0,
    'man_shrugging_dark_skin_tone':0.0, 'sad_but_relieved_face':0.0, 'money_mouth_face':1.0, 'raising_hands_light_skin_tone':2.75,
    'man_facepalming_medium_ligh_skin_tone':-2.5, 'raising_hands_medium_light_skin_tone':2.75,
    'clapping_hands_medium_dark_skin_tone':1.0, 'flexed_biceps_light_skin_tone':3.5
}



new_words = {
    "unemployed":-1.5, "turnover":-1.2 "turnovers":-1.5, "scorer":1.0, "scoring":0.5, "assist":0.5,
    "assists":0.5, "points":0.5, "pts":0.3, "rebound":0.5, "reb":0.3, "rebounds":0.5, "block":0.5, "blocks":0.5,
    "mvp":3.5, "dpoy":3.0, "technical":-2.5, "flagrant":-2.5, "foul":-1.5, "fouls":-1.5, "steals":1.0,
    "high":1.1, "defense": 0.5, "defensive":0.0, "offense":0.5, "offensive":0.0,"trash":-3.0, "garbage":-3.0, 
    "elite":3.5, "intensity":1.1, "lol":0.0, "meh":-0.5, "play":0.0, "plays":0.0, "playing":0.0, "played":0.0,
    "need":-0.5, "needs":-0.5, "lmao":0.0, "concerns":-0.8, "rob":0.0, "making":1.0, "made":0.8, "make":0.5,
    "shoot":0.0, "beaten":-0.5, "deep":0.5, "deeper":0.7, "deepest":1.0, "spam":0.0, "crazy":0.0,
    "fit":0.0, "decent":0.2, "star":1.5, "clearly":0.0, "god":0.0, "straight":0.0, "contender":0.5,
    "contenders":0.5, "ill":0.0, "mid":-1.0, "ring":0.0, "potential":0.5, "insane":0.3, "incredible":2.5,
    "tremendous":3.5, "impact":0.5, "hot":1.5, "fair":0.3, "effort":0.3, "leader":1.5, "leadership":1.5,
    "chemistry":0.4, "clear":0.0, "brick":-1.5, "haha":1.0, "hand":0.0, "blow":-1.5, "1":0.0, "superstar":2.5,
    "superstars":1.0, "offensively":0.0, "defensively":0.0, "washed":-2.5, "cheap":-0.5, "backup":-0.3, "starter":0.3,
    "delusional":-1.0, "joke":-1.5, "jokes":0.0, "compete":0.5, "playmaking":1.0, "lmfao":0.0, "correct":.7,
    "incorrect":-1.0, "bum":-2.5, "hard":0.0, "soft":-1.0, "softest":-1.5, "softer":-1.25, "athletic":1.0,
    "unprotected":0.0, "excuse":-0.3, "dominant":2.0, "dominated":1.5, "dominate":0.7, "dominates":0.5
    "consistent":0.5, "inconsistent":-1.5, "momentum":0.5, "athleticism":0.5, "lacking":-1.5, "lack":-2.5,
    "attack":0.0, "toxic":-2.0, "idiots":-2.0, "clown":-4.0, "beast":2.0, "beasts":2.0, "poorly":-2.0, "blew":-1.5,
    "blown":-1.5, "blowing": -1.5, "lead":0.5, "reliable":0.5, "mediocre":-0.8, "liability":-2.0, "relax":0.3,
    "glass":-0.5, "nuts":0.0, "contention":0.5, "contend":0.5, "know":1.0, "knows":1.0, "knowing":1.0, "knew":1.0}

sample_sentiments={
    2, 2, 0, 2, 0, 0, 1, 2, 0, 2, #10
    1, 0, 1, 0, 1, 1, 0, 2, 1, 2, #20
    0, 0, 1, 1, 0, 0, 0, 0, 1, 0, #30
    0, 0, 0, 2, 0, 2, 0, 1, 2, 1, #40
    1, 2, 1, 1, 2, 2, 0, 0, 1, 0, #50
    2, 1, 1, 2, 2, 0, 2, 0, 1, 2, #60
    0, 0, 0, 1, 0, 0, 0, 0, 0, 2, #70
    1, 2, 2, 0, 2, 0, 2, 0, 0, 1, #80
    0, 2, 0, 1, 1, 0, 1, 0, 1, 0, #90
    1, 0, 2, 2, 2, 1, 0, 1, 0, 2, #100
    0, 2, 0, 1, 0, 0, 0, 0, 0, 0, #110
    2, 2, 0, 1, 0, 1, 0, 2, 0, 0, #120
    1, 0, 1, 0, 1, 1, 2, 0, 1, 2, #130
    0, 0, 2, 1, 0, 1, 2, 2, 1, 0, #140
    1, 2, 2, 0, 0, 0, 1, 0, 1, 0, #150
    2, 2, 0, 2, 0, 0, 1, 0, 0, 1, #160
    2, 2, 0, 1, 2, 2, 2, 1, 0, 0, #170
    0, 2, 1, 2, 0, 1, 0, 1, 0, 2, #180
    2, 0, 1, 1, 0, 0, 0, 0, 0, 0, #190
    0, 1, 1, 0, 2, 2, 0, 0, 1, 1, #200
    0, 2, 0, 0, 0, 0, 1, 1, 0, 2, #210
    0, 0, 0, 0, 0, 0, 2, 0, 0, 1, #220
    2, 0, 2, 0, 1, 2, 2, 0, 0, 0, #230
    1, 2, 0, 0, 0, 2, 0, 2, 2, 2, #240
    2, 1, 0, 0, 2, 1, 2, 1, 1, 1, #250
    1, 2, 2, 0, 1, 0, 0, 1, 0, 1, #260
    0, 0, 2, 2, 0, 1, 0, 0, 2, 1, #270
    2, 1, 1, 2, 1, 2, 1, 2, 0, 0, #280
    0, 0, 1, 0, 1, 0, 0, 2, 2, 0, #290
    1, 0, 0, 2, 1, 2, 1, 1, 1, 0, #300
    2, 2, 0, 2, 2, 2, 0, 2, 2, 2, #310
    0, 0, 1, 1, 0, 0, 2, 1, 0, 2, #320
    0, 0, 2, 0, 1, 0, 0, 0, 1, 1, #330
    2, 2, 0, 0, 1, 1, 0, 1, 2, 0, #340
    0, 1, 0, 0, 1, 1, 2, 2, 2, 2, #350
    0, 1, 1, 0, 0, 0, 2, 1, 1, 2, #360
    0, 2, 2, 0, 1, 1, 0, 1, 1, 1, #370
    1, 0, 2, 1, 1, 1, 0, 0, 1, 2, #380
    2, 1, 0, 1, 1, 0, 0, 0, 2, 2, #390
    1, 1, 1, 2, 2, 1, 2, 2, 2, 2, #400
    2, 0, 2, 0, 2, 0, 2, 0, 1, 0, #410
    0, 0, 1, 2, 2, 0, 0, 1, 0, 1, #420
    2, 1, 1, 1, 2, 1, 0, 2, 1, 0, #430
    1, 2, 2, 2, 1, 1, 1, 0, 0, 2, #440
    0, 0, 0, 1, 1, 2, 2, 2, 0, 0, #450
    0, 0, 0, 2, 0, 2, 2, 0, 0, 0, #460
    2, 1, 1, 2, 1, 1, 2, 1, 0, 2, #470
    2, 2, 0, 2, 1, 0, 2, 1, 0, 2, #480
    0, 2, 2, 1, 2, 0, 0, 0, 2, 0, #490
    0, 0, 1, 1, 2, 1, 0, 1, 2, 2, #500
    
}


