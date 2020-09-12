# YACHT DICE (Original rule)

import os
import sys
import termios
from random import randrange
from time import sleep

CRED	= '\033[91m'
CGREEN	= '\033[92m'
CGRAY	= '\033[90m'
CEND	= '\033[0m'

dicenumbers = [_ for _ in range(6)]
dicenumbers[0] = "●"," "," "," "," "," "," "
dicenumbers[1] = " "," ","●"," "," ","●"," "
dicenumbers[2] = "●"," ","●"," "," ","●"," "
dicenumbers[3] = " ","●","●"," "," ","●","●"
dicenumbers[4] = "●","●","●"," "," ","●","●"
dicenumbers[5] = " ","●","●","●","●","●","●"

class Yacht:
	def __init__(self):
		self.Pane = "\n\
    ┌───────────────────────────────────────────────────────────────┐\n\
    │  🎲 Yacht-Dice!                                               │\n\
    │    ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐  │\n\
    │    │ {fmt_a1}   {fmt_a2} │   │ {fmt_b1}   {fmt_b2} │   │ {fmt_c1}   {fmt_c2} │   │ {fmt_d1}   {fmt_d2} │   │ {fmt_e1}   {fmt_e2} │  │\n\
    │    │ {fmt_a3} {fmt_a0} {fmt_a4} │   │ {fmt_b3} {fmt_b0} {fmt_b4} │   │ {fmt_c3} {fmt_c0} {fmt_c4} │   │ {fmt_d3} {fmt_d0} {fmt_d4} │   │ {fmt_e3} {fmt_e0} {fmt_e4} │  │\n\
    │    │ {fmt_a5}   {fmt_a6} │   │ {fmt_b5}   {fmt_b6} │   │ {fmt_c5}   {fmt_c6} │   │ {fmt_d5}   {fmt_d6} │   │ {fmt_e5}   {fmt_e6} │  │\n\
    │    └───────┘   └───────┘   └───────┘   └───────┘   └───────┘  │\n\
    │       [{fmt_dice0_lock}]         [{fmt_dice1_lock}]         [{fmt_dice2_lock}]         [{fmt_dice3_lock}]         [{fmt_dice4_lock}]     │\n\
    ├───────────────────────────────────────────────────────────────┤\n\
    │  🎲 Score Board                                               │\n\
    │                                                               │\n\
    │     {fmt_ptr0}  Ones     [{fmt_score0}]        │    {fmt_ptr6}  Choice            [{fmt_score6}]    │\n\
    │     {fmt_ptr1}  Twoes    [{fmt_score1}]        │    {fmt_ptr7}  Four of a Kind    [{fmt_score7}]    │\n\
    │     {fmt_ptr2}  Threes   [{fmt_score2}]        │    {fmt_ptr8}  Full House        [{fmt_score8}]    │\n\
    │     {fmt_ptr3}  Fourss   [{fmt_score3}]        │    {fmt_ptr9}  Little Straight   [{fmt_score9}]    │\n\
    │     {fmt_ptr4}  Fives    [{fmt_score4}]        │    {fmt_ptr10}  Big Straight      [{fmt_score10}]    │\n\
    │     {fmt_ptr5}  Sixes    [{fmt_score5}]        │    {fmt_ptr11}  Yacht             [{fmt_score11}]    │\n\
    ├───────────────────────────────────────────────────────────────┤\n\
    │        reroll chance : {fmt_chance}            Total : {fmt_total}               │\n\
    └───────────────────────────────────────────────────────────────┘\n\
	"
		# Dice
		self.dicelist = [0 for _ in range(5)]
		self.dicelist_lock = [False for _ in range(5)]

		# Score Board
		self.scorelist = [0 for _ in range(12)]
		self.scorelist_lock = [ False for _ in range(12)]
		self.scorelist_str = ["" for _ in range(12)]

		self.chance = 3
		self.ptr_value = 0

		# init
		self.reroll_motion()
		self.show_pane()


	def reroll_motion(self):
		for _ in range(10):
			self.show_pane(calc_score=False)
			sleep(0.05)
			for i in range(5):
				if not self.dicelist_lock[i]:
					self.dicelist[i] = randrange(1,7) 

	def reroll_dice(self):
		if self.chance < 1:
			return
		self.chance -= 1
		self.reroll_motion()

	def up_pointer(self):
		if (self.ptr_value > 0):
			self.ptr_value -= 1

	def down_pointer(self):
		if (self.ptr_value < 11):
			self.ptr_value += 1

	def dice_lock(self, n):
		self.dicelist_lock[n-1] = not self.dicelist_lock[n-1]

	def record_score(self):
		n = self.ptr_value
		if not self.scorelist_lock[n]:
			self.scorelist_lock[n] = True
			self.chance = 3
			for i in range(5):
				self.dicelist_lock[i] = False
			self.reroll_motion()

	def get_numbers(self, n):
		result = 0
		for dice in self.dicelist:
			if dice == n:
				result += n
		return result

	def get_choice(self):
		return sum(self.dicelist)

	def get_four_kind(self):
		for i in range(6):
			if self.dicelist.count(i+1) >= 4:
				return sum(self.dicelist)
		return 0

	def get_fullhouse(self):
		for i in range(1, 7):
		 	for j in range(1, 7):
		 		if (self.dicelist.count(i) == 3) and (self.dicelist.count(j)) == 2:
		 			return sum(self.dicelist)
		return 0

	def get_straight(self):
		nums = sorted(set(self.dicelist))
		gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
		edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
		return list(zip(edges, edges))

	def get_little_straight(self):
		if (1, 4) in self.get_straight()	\
		or (2, 5) in self.get_straight()	\
		or (3, 6) in self.get_straight():
			return 30
		return 0

	def get_big_straight(self):
		if (1, 5) in self.get_straight()	\
		or (2, 6) in self.get_straight():
			return 30
		return 0

	def get_yacht(self):
		for i in range(6):
			if (self.dicelist.count(i+1) == 5):
				return 50
		return 0

	def get_score(self, num, get_function):
		if not self.scorelist_lock[num]:
			self.scorelist[num] = get_function
		else:
			self.scorelist[num] = self.scorelist[num]
		
	def show_pane(self, calc_score=True):
		os.system("clear")
		self.dicelist_locks = [" " if not self.dicelist_lock[i] else (CRED+"X"+CEND) for i in range(5)]

		# Dice
		self.a0, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6 = dicenumbers[ self.dicelist[0] - 1 ]
		self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6 = dicenumbers[ self.dicelist[1] - 1 ]
		self.c0, self.c1, self.c2, self.c3, self.c4, self.c5, self.c6 = dicenumbers[ self.dicelist[2] - 1 ]
		self.d0, self.d1, self.d2, self.d3, self.d4, self.d5, self.d6 = dicenumbers[ self.dicelist[3] - 1 ]
		self.e0, self.e1, self.e2, self.e3, self.e4, self.e5, self.e6 = dicenumbers[ self.dicelist[4] - 1 ]

		# Pointer
		self.ptr = [" " for _ in range(14)]
		self.ptr[self.ptr_value] = CGREEN + "▶" + CEND

		# Get Scores
		if calc_score:
			for i in range(6):
				self.get_score(i, self.get_numbers(i+1))
			self.get_score(6, self.get_choice())
			self.get_score(7, self.get_four_kind())
			self.get_score(8, self.get_fullhouse())
			self.get_score(9, self.get_little_straight())
			self.get_score(10, self.get_big_straight())
			self.get_score(11, self.get_yacht())

		self.total = 0
		for i in range(12):
			self.scorelist_str[i] = "%2d" % self.scorelist[i]
			if self.scorelist_lock[i]:
				self.total += self.scorelist[i]
				self.scorelist_str[i] = CGREEN + ("%2d" % self.scorelist[i]) + CEND

		# Total
		total = "%3d" % self.total

		print(self.Pane.format(
			fmt_a0=self.a0, fmt_a1=self.a1, fmt_a2=self.a2, fmt_a3=self.a3, fmt_a4=self.a4, fmt_a5=self.a5, fmt_a6=self.a6,
			fmt_b0=self.b0, fmt_b1=self.b1, fmt_b2=self.b2, fmt_b3=self.b3, fmt_b4=self.b4, fmt_b5=self.b5, fmt_b6=self.b6,
			fmt_c0=self.c0, fmt_c1=self.c1, fmt_c2=self.c2, fmt_c3=self.c3, fmt_c4=self.c4, fmt_c5=self.c5, fmt_c6=self.c6,
			fmt_d0=self.d0, fmt_d1=self.d1, fmt_d2=self.d2, fmt_d3=self.d3, fmt_d4=self.d4, fmt_d5=self.d5, fmt_d6=self.d6,
			fmt_e0=self.e0, fmt_e1=self.e1, fmt_e2=self.e2, fmt_e3=self.e3, fmt_e4=self.e4, fmt_e5=self.e5, fmt_e6=self.e6,

			fmt_dice0_lock=self.dicelist_locks[0],
			fmt_dice1_lock=self.dicelist_locks[1],
			fmt_dice2_lock=self.dicelist_locks[2],
			fmt_dice3_lock=self.dicelist_locks[3],
			fmt_dice4_lock=self.dicelist_locks[4],

			fmt_score0=self.scorelist_str[0],
			fmt_score1=self.scorelist_str[1],
			fmt_score2=self.scorelist_str[2],
			fmt_score3=self.scorelist_str[3],
			fmt_score4=self.scorelist_str[4],
			fmt_score5=self.scorelist_str[5],
			fmt_score6=self.scorelist_str[6],
			fmt_score7=self.scorelist_str[7],
			fmt_score8=self.scorelist_str[8],
			fmt_score9=self.scorelist_str[9],
			fmt_score10=self.scorelist_str[10],
			fmt_score11=self.scorelist_str[11],
			
			fmt_ptr0=self.ptr[0],
			fmt_ptr1=self.ptr[1],
			fmt_ptr2=self.ptr[2],
			fmt_ptr3=self.ptr[3],
			fmt_ptr4=self.ptr[4],
			fmt_ptr5=self.ptr[5],
			fmt_ptr6=self.ptr[6],
			fmt_ptr7=self.ptr[7],
			fmt_ptr8=self.ptr[8],
			fmt_ptr9=self.ptr[9],
			fmt_ptr10=self.ptr[10],
			fmt_ptr11=self.ptr[11],

			fmt_total=total,
			fmt_chance=self.chance
		))


def get_keyboard_input():
	result = None
	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	
	try:
		result = sys.stdin.read(1)
	except IOError:
		pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

	return result


def get_user_control(yacht):
	Input = get_keyboard_input()

	if (Input in "12345"):
		yacht.dice_lock(int(Input))
	elif (Input in "AB"):
		if (Input == "A"):
			yacht.up_pointer()
		else:
			yacht.down_pointer()
	elif (Input == "r"):
		yacht.reroll_dice()
	elif (Input == " "):
		yacht.record_score()
	else:
		pass


def play_yacht():
	yacht = Yacht()
	while True:
		get_user_control(yacht)
		yacht.show_pane()


def main():
	play_yacht()


if __name__ == '__main__':
	main()


# EOF

