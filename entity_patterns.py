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



