# Gameplay defines
global TOTAL_POINTS_PER_GAME
global TOTAL_GOALS_PER_GAME
global TOTAL_GOALS_PER_GAME_ES
global TOTAL_GOALS_PER_GAME_PP
global TOTAL_GOALS_PER_GAME_PK
global SCF_SF_FACTOR
global PROBABILITY_FOR_OT
global CURRENT_TEAM
global OPPONENT_TEAM
global SIMULATION_LIGHT
global SIMULATION_EXT
global HT_ADVANTAGE
global AT_ADVANTAGE
global WS_DEF
global WS_CEN
global WS_WNG
global WS_FWD
TOTAL_POINTS_PER_GAME = 2.1066089693154995
TOTAL_GOALS_PER_GAME = 5.209284028324154
TOTAL_GOALS_PER_GAME_ES = 0
TOTAL_GOALS_PER_GAME_PP = 0
TOTAL_GOALS_PER_GAME_PK = 0
SCF_SF_FACTOR =  4.292072174177282
PROBABILITY_FOR_OT = 0.10660896931549961
CURRENT_TEAM = ['ht','at']
OPPONENT_TEAM = ['at','ht']
SIMULATION_LIGHT = 0
SIMULATION_EXT = 1
HT_ADVANTAGE = 1.1878
AT_ADVANTAGE = 1/HT_ADVANTAGE
WS_DEF = [1,0.75,0.15] # weighted scale suggestion for defenders
WS_CEN = [1,1,0.5] # weighted scale suggestion for centers
WS_WNG = [0.75,1,1] # weighted scale suggestion for wingers
WS_FWD = [1.25,1.25,0.5]

global STAT_ES
global STAT_PP
global STAT_PK
global STAT_INDEX
STAT_ES = 0
STAT_PP = 1
STAT_PK = 2
STAT_INDEX = [STAT_ES,STAT_PP,STAT_PK]


global SKATER_BIO_BIT
global SKATER_ES_BIT
global SKATER_PP_BIT
global SKATER_PK_BIT
global SKATER_ON_ICE_BIT
global SKATER_RELATIVE_BIT
global GOALIE_ES_BIT
global GOALIE_PP_BIT
global GOALIE_PK_BIT
global TEAM_ES_BIT
global TEAM_PP_BIT
global TEAM_PK_BIT
global TEAM_HOME_BIT
global TEAM_AWAY_BIT
global UNAVAILABLE_PLAYERS_BIT
global DATABASE_BIT_REGISTER
global CONNECTION_TIMEOUT

SKATER_BIO_BIT = 0
SKATER_ES_BIT = 1
SKATER_PP_BIT = 2
SKATER_PK_BIT = 3
SKATER_ON_ICE_BIT = 4
SKATER_RELATIVE_BIT = 5
GOALIE_ES_BIT = 6
GOALIE_PP_BIT = 7
GOALIE_PK_BIT = 8
TEAM_ES_BIT = 9
TEAM_PP_BIT = 10
TEAM_PK_BIT = 11
TEAM_HOME_BIT = 12
TEAM_AWAY_BIT = 13
UNAVAILABLE_PLAYERS_BIT = 14
DATABASE_BIT_REGISTER = 15*[True]
CONNECTION_TIMEOUT = 60						# Connection will timeout after 60 seconds

global GAMEPLAY_ES
global GAMEPLAY_PP_HT
global GAMEPLAY_PP_AT
global GAMEPLAY_PK_HT
global GAMEPLAY_PK_AT
global NO_GOALIE_HT
global NO_GOALIE_AT
GAMEPLAY_ES = 0
GAMEPLAY_PP_HT = 1
GAMEPLAY_PP_AT = 2
GAMEPLAY_PK_HT = 2
GAMEPLAY_PK_AT = 1
NO_GOALIE_HT = 3
NO_GOALIE_AT = 4

global ACTIVE_SKATERS
global ACTIVE_GOALIES
global ACTIVE_PLAYERS
global ACTIVE_TEAMS
ACTIVE_SKATERS = set()
ACTIVE_GOALIES = set()
ACTIVE_PLAYERS = set()
ACTIVE_TEAMS = ['ANA','ARI','BOS','BUF','CAR','CBJ','CGY','CHI','COL','DAL','DET','EDM','FLA','LAK','MIN','MTL','NJD','NSH','NYI','NYR','OTT','PHI','PIT','SJS','STL','TBL','TOR','VAN','VGK','WPG','WSH']
'''
Skater Bio-DB from naturalstattrick.com
,"Player","Team","Position","Age","Date of Birth",
"Birth City","Birth State/Province","Birth Country",
"Nationality","Height (in)","Weight (lbs)","Draft Year",
"Draft Team","Draft Round","Round Pick","Overall Draft Position"
'''
global SKATER_DB_BIO_NAME
global SKATER_DB_BIO_TEAM_ID
global SKATER_DB_BIO_POSITION
global SKATER_DB_BIO_AGE
global SKATER_DB_BIO_DOB
global SKATER_DB_BIO_HEIGHT
global SKATER_DB_BIO_WEIGHT
global SKATER_DB_BIO_DRAFT_YEAR
global SKATER_DB_BIO_DRAFT_TEAM
global SKATER_DB_BIO_DRAFT_ROUND
global SKATER_DB_BIO_ROUND_PICK
global SKATER_DB_BIO_TOTAL_DRAFT_POS
SKATER_DB_BIO_NAME = 1
SKATER_DB_BIO_TEAM_ID = 2
SKATER_DB_BIO_POSITION = 3
SKATER_DB_BIO_AGE = 4
SKATER_DB_BIO_DOB = 5
SKATER_DB_BIO_HEIGHT = 10
SKATER_DB_BIO_WEIGHT = 11
SKATER_DB_BIO_DRAFT_YEAR = 12
SKATER_DB_BIO_DRAFT_TEAM = 13
SKATER_DB_BIO_DRAFT_ROUND = 14
SKATER_DB_BIO_ROUND_PICK = 15
SKATER_DB_BIO_TOTAL_DRAFT_POS = 16
SKATER_DB_BIO_LENGTH = 17

'''
Skater Individual-DB, ES, from naturalstattrick.com
'''
global SKATER_DB_IND_TEAM_ID
global SKATER_DB_IND_TOI
global SKATER_DB_IND_GOALS
global SKATER_DB_IND_ASSIST
global SKATER_DB_IND_FIRST_ASSIST
global SKATER_DB_IND_SECOND_ASSIST
global SKATER_DB_IND_SF
global SKATER_DB_IND_SH_PCG
global SKATER_DB_IND_IXG
global SKATER_DB_IND_ICF
global SKATER_DB_IND_IFF
global SKATER_DB_IND_ISCF
global SKATER_DB_IND_IHDCF
global SKATER_DB_IND_RUSH_ATTEMPTS
global SKATER_DB_IND_REBOUNDS_CREATED
global SKATER_DB_IND_TOTAL_PENALTIES
global SKATER_DB_IND_MINOR
global SKATER_DB_IND_MAJOR
global SKATER_DB_IND_MISCONDUCT
global SKATER_DB_IND_PENALTIES_DRAWN
global SKATER_DB_IND_GIVEAWAYS
global SKATER_DB_IND_TAKEAWAYS
global SKATER_DB_IND_HITS
global SKATER_DB_IND_HITS_TAKEN
global SKATER_DB_IND_SHOTS_BLOCKED
global SKATER_DB_IND_FACEOFFS_WON
global SKATER_DB_IND_FACEOFFS_LOST
global SKATER_DB_IND_FACEOFFS_WON_PCG
SKATER_DB_IND_TEAM_ID = 2
SKATER_DB_IND_TOI = 5
SKATER_DB_IND_GOALS = 6
SKATER_DB_IND_ASSIST = 7
SKATER_DB_IND_FIRST_ASSIST = 8
SKATER_DB_IND_SECOND_ASSIST = 9
SKATER_DB_IND_SF = 12
SKATER_DB_IND_SH_PCG = 13
SKATER_DB_IND_IXG = 14
SKATER_DB_IND_ICF = 15
SKATER_DB_IND_IFF = 16
SKATER_DB_IND_ISCF = 17
SKATER_DB_IND_IHDCF = 18
SKATER_DB_IND_RUSH_ATTEMPTS = 19
SKATER_DB_IND_REBOUNDS_CREATED = 20
SKATER_DB_IND_PIM = 21
SKATER_DB_IND_TOTAL_PENALTIES = 22
SKATER_DB_IND_MINOR = 23
SKATER_DB_IND_MAJOR = 24
SKATER_DB_IND_MISCONDUCT = 25
SKATER_DB_IND_PENALTIES_DRAWN = 26
SKATER_DB_IND_GIVEAWAYS = 27
SKATER_DB_IND_TAKEAWAYS = 28
SKATER_DB_IND_HITS = 29
SKATER_DB_IND_HITS_TAKEN = 30
SKATER_DB_IND_SHOTS_BLOCKED = 31
SKATER_DB_IND_FACEOFFS_WON = 32
SKATER_DB_IND_FACEOFFS_LOST = 33
SKATER_DB_IND_FACEOFFS_WON_PCG = 34
SKATER_DB_IND_LENGTH = 35

'''
Skater OnIce-DB from naturalstattrick.com
'''
global SKATER_DB_ON_ICE_TOI
global SKATER_DB_ON_ICE_GP
global SKATER_DB_ON_ICE_CF
global SKATER_DB_ON_ICE_CA
global SKATER_DB_ON_ICE_CF_PERCENT
global SKATER_DB_ON_ICE_FF
global SKATER_DB_ON_ICE_FA
global SKATER_DB_ON_ICE_FF_PERCENT
global SKATER_DB_ON_ICE_SF
global SKATER_DB_ON_ICE_SA
global SKATER_DB_ON_ICE_SF_PERCENT
global SKATER_DB_ON_ICE_GF
global SKATER_DB_ON_ICE_GA
global SKATER_DB_ON_ICE_GF_PERCENT
global SKATER_DB_ON_ICE_xGF
global SKATER_DB_ON_ICE_xGA
global SKATER_DB_ON_ICE_xGF_PERCENT
global SKATER_DB_ON_ICE_SCF
global SKATER_DB_ON_ICE_SCA
global SKATER_DB_ON_ICE_SCF_PERCENT
global SKATER_DB_ON_ICE_HDCF
global SKATER_DB_ON_ICE_HDCA
global SKATER_DB_ON_ICE_HDCF_PERCENT
global SKATER_DB_ON_ICE_OZS
global SKATER_DB_ON_ICE_NZS
global SKATER_DB_ON_ICE_DZS
global SKATER_DB_ON_ICE_OZS_PERCENT
global SKATER_DB_ON_ICE_OZFO
global SKATER_DB_ON_ICE_NZFO
global SKATER_DB_ON_ICE_DZFO
global SKATER_DB_ON_ICE_OZFO_PERCENT
SKATER_DB_ON_ICE_GP = 4
SKATER_DB_ON_ICE_TOI_UL = 5
SKATER_DB_ON_ICE_CF = 6
SKATER_DB_ON_ICE_CA = 7
SKATER_DB_ON_ICE_CF_PERCENT = 8
SKATER_DB_ON_ICE_FF = 9
SKATER_DB_ON_ICE_FA = 10
SKATER_DB_ON_ICE_FF_PERCENT = 11
SKATER_DB_ON_ICE_SF = 12
SKATER_DB_ON_ICE_SA = 13
SKATER_DB_ON_ICE_SF_PERCENT = 14
SKATER_DB_ON_ICE_GF = 15
SKATER_DB_ON_ICE_GA = 16
SKATER_DB_ON_ICE_GF_PERCENT = 17
SKATER_DB_ON_ICE_xGF = 18
SKATER_DB_ON_ICE_xGA = 19
SKATER_DB_ON_ICE_xGF_PERCENT = 20
SKATER_DB_ON_ICE_SCF = 21
SKATER_DB_ON_ICE_SCA = 22
SKATER_DB_ON_ICE_SCF_PERCENT = 23
SKATER_DB_ON_ICE_HDCF = 24
SKATER_DB_ON_ICE_HDCA = 25
SKATER_DB_ON_ICE_HDCF_PERCENT = 26
SKATER_DB_ON_ICE_OZS = 45
SKATER_DB_ON_ICE_NZS = 46
SKATER_DB_ON_ICE_DZS = 47
SKATER_DB_ON_ICE_OZS_PERCENT = 49
SKATER_DB_ON_ICE_OZFO = 50
SKATER_DB_ON_ICE_NZFO = 51
SKATER_DB_ON_ICE_DZFO = 52
SKATER_DB_ON_ICE_OZFO_PERCENT = 53
SKATER_DB_ON_ICE_LENGTH = 54

'''
Relative stats from naturalstattrick.com
'''
global SKATER_DB_RELATIVE_NAME
global SKATER_DB_RELATIVE_CF_PER_60
global SKATER_DB_RELATIVE_CA_PER_60
global SKATER_DB_RELATIVE_CF_PCG
global SKATER_DB_RELATIVE_FF_PER_60
global SKATER_DB_RELATIVE_FA_PER_60
global SKATER_DB_RELATIVE_FF_PCG
global SKATER_DB_RELATIVE_SF_PER_60
global SKATER_DB_RELATIVE_SA_PER_60
global SKATER_DB_RELATIVE_SF_PCG
global SKATER_DB_RELATIVE_GF_PER_60
global SKATER_DB_RELATIVE_GA_PER_60
global SKATER_DB_RELATIVE_GF_PCG
global SKATER_DB_RELATIVE_xGF_PER_60
global SKATER_DB_RELATIVE_XGA_PER_60
global SKATER_DB_RELATIVE_xGF_PCG
global SKATER_DB_RELATIVE_SCF_PER_60
global SKATER_DB_RELATIVE_SCA_PER_60
global SKATER_DB_RELATIVE_SCF_PCG
SKATER_DB_RELATIVE_NAME = 1
SKATER_DB_RELATIVE_CF_PER_60 = 7
SKATER_DB_RELATIVE_CA_PER_60 = 8
SKATER_DB_RELATIVE_CF_PCG = 9
SKATER_DB_RELATIVE_FF_PER_60 = 10
SKATER_DB_RELATIVE_FA_PER_60 = 11
SKATER_DB_RELATIVE_FF_PCG = 12
SKATER_DB_RELATIVE_SF_PER_60 = 13
SKATER_DB_RELATIVE_SA_PER_60 = 14
SKATER_DB_RELATIVE_SF_PCG = 15
SKATER_DB_RELATIVE_GF_PER_60 = 16
SKATER_DB_RELATIVE_GA_PER_60 = 17
SKATER_DB_RELATIVE_GF_PCG = 18
SKATER_DB_RELATIVE_xGF_PER_60 = 19
SKATER_DB_RELATIVE_XGA_PER_60 = 20
SKATER_DB_RELATIVE_xGF_PCG = 21
SKATER_DB_RELATIVE_SCF_PER_60 = 22
SKATER_DB_RELATIVE_SCA_PER_60 = 23
SKATER_DB_RELATIVE_SCF_PCG = 24
'''
Goalie-DB from naturalstattrick.com
'''
global GOALIE_DB_NAME
global GOALIE_DB_TEAM_ID
global GOALIE_DB_GP
global GOALIE_DB_TOI
global GOALIE_DB_SA
global GOALIE_DB_SV
global GOALIE_DB_GA
global GOALIE_DB_SV_PCG
global GOALIE_DB_GAA
global GOALIE_DB_GSAA
global GOALIE_DB_XGA
global GOALIE_DB_AVG_SHOT_DIST
global GOALIE_DB_AVG_GOAL_DIST
GOALIE_DB_NAME = 1
GOALIE_DB_TEAM_ID = 2
GOALIE_DB_GP = 3
GOALIE_DB_TOI = 4
GOALIE_DB_SA = 5
GOALIE_DB_SV = 6
GOALIE_DB_GA = 7
GOALIE_DB_SV_PCG = 8
GOALIE_DB_GAA = 9
GOALIE_DB_GSAA = 10
GOALIE_DB_XGA = 11
GOALIE_DB_AVG_SHOT_DIST = 30
GOALIE_DB_AVG_GOAL_DIST = 31
GOALIE_DB_LENGTH = 32

'''
Team-DB from naturalstattrick.com
Columns:
0-10:  0,"Team","GP","TOI","W","L","OTL","ROW","Points","Point %","CF",
11-20: "CA","CF%","FF","FA","FF%","SF","SA","SF%","GF","GA",
21-30: "GF%","xGF","xGA","xGF%","SCF","SCA","SCF%","SCSF","SCSA","SCSF%",
31-40: "SCGF","SCGA","SCGF%","SCSH%","SCSV%","HDCF","HDCA","HDCF%","HDSF","HDSA",
41-50: "HDSF%","HDGF","HDGA","HDGF%","HDSH%","HDSV%","MDCF","MDCA","MDCF%","MDSF",
51-60: "MDSA","MDSF%","MDGF","MDGA","MDGF%","MDSH%","MDSV%","LDCF","LDCA","LDCF%",
61-70: "LDSF","LDSA","LDSF%","LDGF","LDGA","LDGF%","LDSH%","LDSV%","SH%","SV%",
71-80: "PDO"
'''
global TEAM_DB_NAME_COL
global TEAM_DB_GP_COL
global TEAM_DB_TOI_COL
global TEAM_DB_W_COL
global TEAM_DB_L_COL
global TEAM_DB_OTL_COL
global TEAM_DB_ROW_COL
global TEAM_DB_P_COL
global TEAM_DB_P_PCG_COL
global TEAM_DB_CF_COL
global TEAM_DB_CA_COL
global TEAM_DB_CF_PCG_COL
global TEAM_DB_SF_COL
global TEAM_DB_SA_COL
global TEAM_DB_SF_PCG_COL
global TEAM_DB_GF_COL
global TEAM_DB_GA_COL
global TEAM_DB_GF_PCG_COL
global TEAM_DB_FF_COL
global TEAM_DB_FA_COL
global TEAM_DB_FF_PCG_COL
global TEAM_DB_SCF_COL
global TEAM_DB_SCA_COL
global TEAM_DB_SCF_PCG_COL
global TEAM_DB_xGF_COL
global TEAM_DB_xGA_COL
global TEAM_DB_xGF_PCG_COL
global TEAM_DB_HDCF_COL
global TEAM_DB_HDCA_COL
global TEAM_DB_HDCF_PCG_COL
global TEAM_DB_SV_PCG_COL
global TEAM_DB_PDO_COL
global P_PCG_FACTOR
TEAM_DB_NAME_COL = 1
TEAM_DB_GP_COL = 2
TEAM_DB_TOI_COL = 3
TEAM_DB_W_COL = 4
TEAM_DB_L_COL = 5
TEAM_DB_OTL_COL = 6
TEAM_DB_ROW_COL = 7
TEAM_DB_P_COL = 8
TEAM_DB_P_PCG_COL = 9
TEAM_DB_CF_COL = 10
TEAM_DB_CA_COL = 11
TEAM_DB_CF_PCG_COL = 12
TEAM_DB_FF_COL = 13
TEAM_DB_FA_COL = 14
TEAM_DB_FF_PCG_COL = 15
TEAM_DB_SF_COL = 16
TEAM_DB_SA_COL = 17
TEAM_DB_SF_PCG_COL = 18
TEAM_DB_GF_COL = 19
TEAM_DB_GA_COL = 20
TEAM_DB_GF_PCG_COL = 21
TEAM_DB_xGF_COL = 22
TEAM_DB_xGA_COL = 23
TEAM_DB_xGF_PCG_COL = 24
TEAM_DB_SCF_COL = 25
TEAM_DB_SCA_COL = 26
TEAM_DB_SCF_PCG_COL = 27
TEAM_DB_HDCF_COL = 36
TEAM_DB_HDCA_COL = 37
TEAM_DB_HDCF_PCG_COL = 38
TEAM_DB_SV_PCG_COL = 70
TEAM_DB_PDO_COL = 71
TEAM_DB_LENGTH = 72
P_PCG_FACTOR = 0.25 		# This defines how much/little the point% of the season should be weighted in to the rating.