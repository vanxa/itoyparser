import os
class AbstractTranslator:
    __qualname__ = 'AbstractTranslator'
    
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir

    def initialize(self, flname): # Reset the parser and set new file to process
        self.filename = flname
        self.out_file = open(os.path.join(self.outdir,self.filename+"_converted.txt"),"w")    
        self.history = open(os.path.join(self.indir,flname), "r").read().split('\n')
        self.clear()

    def clear(self):
        self.hand_id = None
        self.bb = None
        self.sb = None
        self.hero = None
        self.hero_cards = []
        self.flop_cards = []
        self.turn_card = None
        self.river_card = None
        self.pf_actions = []
        self.flop_actions = []
        self.turn_actions = []
        self.river_actions = []
        self.summary_actions = {}
        self.players = {}
        self.sorted_players = {}
        self.num_actual_players = 0
        self.header_lines = []
        self.dealer = []
        self.pot = None
        self.rake = None
        self.board = None
        self.num_players = 0
        self.step = 0 
        self.num_actual_players = 1
        self.antes = []
        
class TranslateException(Exception):
    __qualname__ = 'TranslateException'
    
    def __init__(self, msg, hand_id = ''):
        self.msg = msg
        self.hand_id = hand_id

    
    def __str__(self):
        if self.hand_id:
            return self.msg + ' -> hand_id: ' + self.hand_id
        return None.msg

    
    def __repr__(self):
        if self.hand_id:
            return self.msg + ' -> hand_id: ' + self.hand_id
        return None.msg


