import re
from translator.regex import *
from translator.translatorabstr import AbstractTranslator
import traceback

class IToYTranslator(AbstractTranslator):
    __qualname__ = 'IToYTranslator'

    def parse(self):
        tb = None
        try:
            logical_linenum = 0
            file_linenum = 0
            seen_all_players = False
            while(file_linenum < len(self.history)):
                line = self.history[file_linenum]
                self._get_step(line)
                if logical_linenum == 0: # Header
                    obj = self._lookup_line(RE_HAND_ID, line)
                    if obj:
                        self.hand_id = obj.group(1)
                        blinds = obj.group(2).strip().replace("(","$").replace("/","/$").replace(")","")
                        self.header_lines += ["GAME " + self.hand_id + ": Texas Hold'em  NL " + blinds]
                elif logical_linenum < 3:
                    self.header_lines += [line]
                    
                elif logical_linenum > 3 and not seen_all_players:
                    obj = self._lookup_line(RE_PLAYERS,line)
                    if obj:
                        self.num_actual_players += 1
                        seatnum = int(obj.group(2))
                        playername = self._process_user_name(obj.group(3))
                        balance = "("+self._process_value(obj.group(4)) + " in chips)"
                        self.players[playername] = (seatnum, balance)
                        self.sorted_players[seatnum] = (playername, balance)
                    else:
                        seen_all_players = True
                         
                elif logical_linenum == 3+self.num_actual_players:
                    obj = self._lookup_line(RE_DEALER, line)
                    if obj:
                        self.dealer = [name for name in self.players.keys() if self.players[name][0] == int(obj.group(1))][0]
                
                elif logical_linenum > 3 + self.num_actual_players and not self.step: 
                    if self._lookup_line(RE_SB, line) and not self.sb: #SB:
                        obj = self._lookup_line(RE_SB, line) #SB
                        self.sb = (self._process_user_name(obj.group(1)), self._process_blind(obj.group(2)), self._process_value(obj.group(3))) 
                    elif self._lookup_line(RE_BB, line): #SB
                        obj = self._lookup_line(RE_BB, line)
                        if obj:
                            self.bb = (self._process_user_name(obj.group(1)), self._process_blind(obj.group(2)), self._process_value(obj.group(3)))
                            
                    elif self._lookup_line(RE_ANTE, line): #SB
                        obj = self._lookup_line(RE_ANTE, line)
                        if obj:
                            self.antes.append((self._process_user_name(obj.group(1)), self._process_value(obj.group(2))))
                                     
                elif self.step == 1: # PREFLOP
                    if not self.hero:
                        obj = self._lookup_line(RE_HERO,line)
                        if obj:
                            self.hero = self._process_user_name(obj.group(1))
                            self.hero_cards = self._process_cards(obj.group(3))
                    else:
                        obj = self._lookup_line(RE_ACT, line)
                        if obj:
                            player = obj.group(1)
                            act = self._process_action(obj.group(2))
                            val,all_in = self._find_all_in(obj.group(3))
                            if act != None:
                                self.pf_actions.append({player : (act,all_in,self._process_value(val))})
                                                                
                    
                elif self.step == 2: # FLOP
                    obj = self._lookup_line(RE_FLOP_H, line)
                    if obj:
                        self.flop_cards = self._process_cards(obj.group(1))
                    else:
                        obj = self._lookup_line(RE_ACT, line)
                        if obj:
                            player = obj.group(1)
                            act = self._process_action(obj.group(2))
                            val,all_in = self._find_all_in(obj.group(3))
                            if act != None:
                                self.flop_actions.append({player : (act,all_in,self._process_value(val))})
                
                elif self.step == 3: # TURN
                    obj = self._lookup_line(RE_TURN_H, line)
                    if obj:
                        self.turn_cards = self._process_cards(obj.group(1))
                    else:
                        obj = self._lookup_line(RE_ACT, line)
                        if obj:
                            player = obj.group(1)
                            act = self._process_action(obj.group(2))
                            val,all_in = self._find_all_in(obj.group(3))
                            if act != None:
                                self.turn_actions.append({player : (act,all_in,self._process_value(val))})
                
                elif self.step == 4: # RIVER
                    obj = self._lookup_line(RE_RIVER_H, line)
                    if obj:
                        self.river_cards = self._process_cards(obj.group(1))
                    else:
                        obj = self._lookup_line(RE_ACT, line)
                        if obj:
                            player = obj.group(1)
                            act = self._process_action(obj.group(2))
                            val,all_in = self._find_all_in(obj.group(3))
                            if act != None:
                                self.river_actions.append({player : (act,all_in,self._process_value(val))})
                    
                elif self.step == 5: # SUMMARY
                    obj = self._lookup_line(RE_SUMM_RAKEPOT,line) # Pot line
                    if obj:
                        self.pot = self._process_value(obj.group(1))
                        self.rake = self._process_value(obj.group(2))
                    obj = self._lookup_line(RE_SUMM_BOARD,line) # Board cards
                    if obj:
                        self.board = self._process_cards(obj.group(1))
                    line = re.sub(r"\([+0-9]*\)", "", line)
                    obj = self._lookup_line(RE_SUMM_L,line)
                    if obj:
                        seatnum = int(obj.group(1))
                        player = self._process_user_name(obj.group(2))
                        is_winner = False
                        if obj.group(3).strip() == "won":
                            is_winner = True
                        #print("Player %s %s" % (player,is_winner))
                        val = self._process_value(obj.group(4))
                        cards_played = self._process_cards(obj.group(5))
                        cards_descr = obj.group(6)
                        self.summary_actions[seatnum] = (is_winner, val, str(cards_played),cards_descr)
                        #print("Seatnum %d belongs to %s, who %s %s, playing %s %s" % (seatnum, player, is_winner,val, str(cards_played), cards_descr))
                        
                if line == "":
                    #print("RESET at linenum %d"% file_linenum)
                    logical_linenum = 0
                    self._print_to_out()
                    self.clear()
                    seen_all_players = False
                
                else:
                    logical_linenum += 1
                file_linenum += 1 
            
#             print("PRINTING")
            self._print_to_out()       
            return True
        except:
            tb = traceback.print_exc()
        finally:
            if tb:
                print("Exception was raised : " + tb)
                return False
            else:
                return True
            
            
    def _process_cards(self, cards):
        if cards == None:
            return ""
        tmp =  [a[::-1].upper() for a in cards.replace("[","").replace("]","").replace("'","").split(" ")]
        return "["+ " ".join(tmp) + "]"
        
        

    def _print_to_out(self):
        if self.hand_id == None:
            return
        for line in self.header_lines:
            self._writeln( line)
        for seatnum in sorted(self.sorted_players.keys()):
            (player, balance) = self.sorted_players[seatnum]
            player_string = "Seat " + str(seatnum) +": " + player + " "+balance
            if self.dealer == player:
                player_string += " DEALER"
            self._writeln( player_string)
        for uname,val in self.antes:
            self._writeln(uname+": Ante "+ val)
        self._writeln( self.sb[0] + ": " + self.sb[1] + " "+ self.sb[2])
        self._writeln( self.bb[0] + ": " + self.bb[1] + " "+ self.bb[2])
        self._writeln( "*** HOLE CARDS ***")
        self._writeln( "Dealt to "+ self.hero + " " + self.hero_cards)
        for action in self.pf_actions:
            self._writeln(self._process_action_for_print(action))
        
        if len(self.flop_cards):
            self._writeln( "*** FLOP *** " + self.flop_cards)        
        if len(self.flop_actions):
            for action in self.flop_actions:
                self._writeln(self._process_action_for_print(action))
        if self.turn_card:
            self._writeln( "*** TURN *** " + self.flop_cards + " " + self.turn_cards)
        if len(self.turn_actions):
            for action in self.turn_actions:
                self._writeln(self._process_action_for_print(action))
        if self.river_card:
            self._writeln( "*** RIVER *** " + self.flop_cards + " " + self.turn_cards + " " + self.river_cards)
        if len(self.river_actions):
            for action in self.river_actions:
                self._writeln(self._process_action_for_print(action))
        
                    
        self._writeln( "*** SUMMARY ***")            
        self._writeln( "Total pot " + self.pot +" Rake " + self.rake)
        win_str = ""
        for seatnum in self.summary_actions:
            (has_won, val, cards, cards_descr) = self.summary_actions[seatnum]
            player = self.sorted_players[seatnum][0]
            #print("Seatnum %d belongs to %s, who %s %s, playing %s %s" % (seatnum, player, has_won,val, str(cards), cards_descr))
            if has_won:
                win_str = player + ": wins " + val
            if cards != "":
                self._writeln( player + ": Shows " + cards + " " + cards_descr)
        self._writeln(win_str)
        self._writeln("\n")
                
    def _process_action_for_print(self,action):
        for player in action.keys(): # should be a single entry
                (act,all_in,val) = action[player]
                act_string = player
                if all_in is not None and act == "Raise":
                    act_string += ": Allin"
                else:
                    act_string += ": " + act
                if val is not None:
                        act_string += " " + val
                return act_string   
    
    def _writeln(self, line):
        if self.out_file is not None:
            self.out_file.write(line + "\n")        
                        
    def _process_user_name(self,name):
        name = name.strip()
#         if not re.search(r".*[a-zA-Z]+.*",name) or " " in name: 
#             name= "\"" + name + "\""
        return name
                
            
    def _get_step(self,line):
        line = line.replace("*","").replace(" ","")
        if re.search(r"HOLECARDS",line):
            self.step = 1
        if re.search(r"FLOP",line):
            self.step = 2
        if re.search(r"TURN",line):
            self.step = 3
        if re.search(r"RIVER",line):
            self.step = 4
        if re.search(r"SUMMARY",line):
            self.step =5
            
    def _process_action(self,act):
        if act == "raises":
            return "Raise"
        if act == "checks":
            return "Check"
        if act == "folds":
            return "Fold"
        if act == "calls":
            return "Call"
        if act== "bets":
            return "Bet"
        return None

    def _find_all_in(self,string):
        obj = re.search(RE_ALL_IN, string.replace(" ",""))
        if obj:
            return obj.group(2), obj.group(1)
        else:
            return None
        
    def _lookup_line(self, regex, line):
        obj = re.search(regex, line)
        if obj:
            return obj
        else:
            #print("For line '%s', Regex pattern '%s' return None" % (line, regex))
            return None
        
    def _process_blind(self, string):
        if string == "raises all-in":
            return "Allin"
        elif string == "posts small blind":
            return "Post SB"
        else:
            return "Post BB"
    
    def _process_value(self, val):
        if val == None or val == "":
            return ""
        return "$"+val.replace(",","")