import sys
import pandas as pd 
import time

# get command line input of participant ID
subid = sys.argv[1]

# function to validate responses/prompt until we enter a valid response
def validate_response(question, possible_responses):
	while True:
		participant_response = input(question)
		# if valid response
		if participant_response in possible_responses:
			break
		else:
			print(f'Invalid response! Response should be in {possible_responses}')
	return(participant_response)


def memory():
	# Memory test, altogether two trials.
	input('--[MEMORY TEST - Read the following instructions to the participant.]\n')
	print('This part is a memory test. \n\
I am going to read you a list of words that you will need to remember now and later on.\n\
Please listen carefully. When I am through, tell me as many words as you can remember.\n\
It does not matter in what order you say them. \n')
	input('Are these instructions clear? Do you have any questions? \n')
	input("Okay, let's get started.\n")
	# First trial
	input('--[Read the following list of five words to the participant, ONE WORD PER SECOND. First trial.]\n')
	input('FACE  VELVET  CHURCH  DAISY  RED \n')
	input('Now can you repeat the words I just read to you back to me? \n')

	# Second trial
	input('--[Read the same list again, ONE WORD PER SECOND. Second trial.]\n')
	print('I am going to read the same list for a second time. \n\
Try to remember and tell me as many words as you can, including words you said the first time. \n\
Here we go.\n')
	input('FACE  VELVET  CHURCH  DAISY  RED\n')
	input('Now can you repeat the words I just read to you back to me?\n')
	# Memory scoring instructions
	input('--[NO points are given for the memory test.]\n')
	input('Great. Please try to remember these words as I will ask you to recall them again at the end of the call. \n')
	print('----[END OF MEMORY TEST]---- \n\n')



def attention():
	# Attention, digit session.
	input('--[ATTENTION TEST - FORWARD DIGIT SPAN]\n')
	print('--[Read the following instructions to the participant.]\n')
	print('Now I am going to say some numbers and when I am through, \n\
please repeat them to me *EXACTLY* as I said them. \n')
	input('Do you have any questions? -- Here we go.\n')
	# FORWARD DIGIT SPAN
	input('--[Read the following numbers to the participant at the rate of ONE DIGIT PER SECOND.]\n')
	input('2  1  8  5  4 \n')
	print('Can you repeat the numbers back to me? \n')
	# FORWARD DIGIT SPAN Scoring instructions
	print('--[Score 1 point if the participant repeated the numbers correctly.] \n')
	atten_digit_1 = validate_response(question = '[Input 1 for correct repetition, 0 for incorrect response:] \n',
		possible_responses = ['1', '0'])
	# BACKWARD DIGIT SPAN
	input('--[ATTENTION TEST - BACKWARD DIGIT SPAN] \n')
	print('Now I am going to say more numbers, but this time when I am through, \n\
please repeat them to me in the *BACKWARD* order. \n')
	input('Do you have any questions? -- Here we go. \n')
	print('--[Read the following list to the participant at the rate of ONE DIGIT PER SECOND.]\n')
	input('7  4  2 \n')
	print('Can you repeat the list back to me? \n')
	print('--[NOTE: if the participant repeated the sequence in the *FORWARD* order, \n\
*DO NOT* ask them to repeat the sequence in backward order at this point. \n')
	# BACKWARD DIGIT SPAN Scoring instructions
	print('--[Correct response: 2-4-7. Score 1 point if the participant repeated the list correctly.] \n')
	atten_digit_2 = validate_response(question = '[Input 1 for correct repetition (2-4-7); 0 for incorrect response:] \n',
		possible_responses = ['1', '0'])
	atten_digit = float(atten_digit_1) + float(atten_digit_2)
	
	

	# Attention, vigilance session.
	input('--[ATTENTION TEST - VIGILANCE] \n')
	print('--[Read the following instructions to the participant.] \n')
	input('Now I am going to read you a sequence of letters. \n\
Every time I say the letter *A*, please *TAP/CLAP* your hands once. \n\
If I say a different letter, DO NOT tap/clap your hands. \n\
Do you have any questions? \n')
	input('--[SUGGESTION: ask them to clap/tap hands and make sure you can hear the clap/see the gesture.] \n')
	input("Great, let's get started. \n")
	input('--[Read the following list to the participant. \n\
They must *CLAP* at each letter A. \n\
Pay attention to the NUMBER of errors they may make. \n\
(error: tap on a wrong letter OR failure to tap on letter A)] \n')
	input('F B A C M N A A J K L B A F A K D E A A A J A M O F A A B \n')
	# VIGILANCE Scoring instructions
	atten_vigilance = validate_response(question = '[Input 1 if error < 2; 0 if >= 2 errors:] \n',
		possible_responses = ['1', '0'])

	# Attention, 'serial 7s' subtraction session.
	input('--[ATTENTION TEST - SERIAL 7S SUBTRACTION] \n')
	print('--[Read the following instructions to the participant.] \n')
	input('Now, I will ask you to count by subtracting 7 from 100, and then, \n\
keep subtracting 7 from your answer until I tell you to stop. \n')
	input('Do you have any questions? -- Please go ahead. \n')
	print('--[NOTE: the participant MUST perform a MENTAL CALCULATION; \n\
they may not use fingers/pencil/paper to execute the task. \n\
*DO NOT* repeat their answers; if they ask what their last given number was \n\
or what number they must subtract from their answers, \n\
respond by repeating the instructions if not already done so.] \n')
	input("[Please type the participant's responses:] \n")
	# SUBTRACTION Scoring instructions
	print('--[Correct original response: 93 86 79 72 65. Ask them to stop after 5 subtractions.] \n')
	print('--[SCORING INSTRUCTIONS: \n\
4 or 5 correct subtractions -- 3 pts; \n\
2 or 3 correct subtractions -- 2 pts; \n\
1 correct subtraction -- 1 pt; \n\
0 correct subtraction -- 0 pt. \n\
* Each subtraction is evaluated *INDEPENDENTLY*: if the participant responds with an incorrect number but continues to correctly subtract 7 from it, \n\
each correct subtraction is counted.] \n')
	atten_subtract = validate_response(question = '[Input score obtained from correct subtractions:] \n',
		possible_responses = ['0', '1', '2', '3'])
	print('----[END OF ATTENTION TEST]---- \n\n')

	# Add up all scores obtained from the Attention test.
	atten_score = float(atten_digit) + float(atten_vigilance) + float(atten_subtract)
	return(atten_score)

def language():
	# Language, repetition session.
	input('--[LANGUAGE TEST - SENTENCE REPETITION] \n')
	print('--[Read the following instructions to the participant.] \n')
	input("Let's move on to the next part. \n\
I am going to read you a sentence, please repeat it after me, exactly as I say it [PAUSE]: \n\n\
I ONLY KNOW THAT JOHN IS THE ONE TO HELP TODAY. \n")
	print('--[SCORING INSTRUCTIONS: repetitions must be *EXACT*; \n\
pay attention to omissions, substitutions/additions, grammar errors/altering plurals, etc.] \n')
	lan_rep_1 = validate_response(question = '[Input 1 for correct repetition, 0 for incorrect response:] \n',
		possible_responses = ['0', '1'])
	input('Now I am going to read you another sentence. Repeat it after me, exactly as I say it [PAUSE]: \n\n\
THE CAT ALWAYS HID UNDER THE COUCH WHEN DOGS WERE IN THE ROOM. \n')
	print('--[SCORING INSTRUCTIONS: repetitions must be *EXACT*; \n\
pay attention to omissions, substitutions/additions, grammar errors/altering plurals, etc.] \n')
	lan_rep_2 = validate_response(question = '[Input 1 for correct repetition, 0 for incorrect response:] \n',
		possible_responses = ['0', '1'])
	lan_rep = float(lan_rep_1) + float(lan_rep_2)

	# Language, fluency session.
	input('--[LANGUAGE TEST - VERBAL FLUENCY] \n')
	print('--[Read the following instructions to the participant.] \n')
	input('Now I want you to tell me as many words as you can think of that begin with the letter F. \n\
I will tell you to stop after one minute. Proper nouns, numbers, and different forms of a verb are not permitted. \n\
Are you ready? -- Please go ahead. \n')
	print('--[Begin timing, after 60 seconds say Stop. Record all the words, make sure repeated words are not scored.] \n')
	print('--[NOTE: if the participant names *TWO CONSECUTIVE* words that begin with *ANOTHER* letter of the alphabet, \n\
*REPEAT* the target letter (F) if the instructions have not yet been repeated.] \n')
	print('Type in the words they named, separate with space: \n')
	time.sleep(60)
	lan_flu = validate_response(question = '[Input 1 for >= 11 words, 0 for otherwise:] \n',
		possible_responses = ['0', '1'])

	print('----[END OF LANGUAGE TEST]---- \n\n')

	# Add up scores obtained from the Language session.
	lan_score = float(lan_rep) + float(lan_flu)
	return(lan_score)


def abstraction():
	input('--[ABSTRACTION TEST] \n')
	print('--[Read the following instructions to the participant. This part asks the participant to explain what each pair of words has in common. \n\
(The following question is an example that will not be scored.)] \n')
	# practice trial for the participant
	input('Now I will give you two words and I would like you to tell me to what category they belong to: [PAUSE] \n\
AN ORANGE AND A BANANA \n')
	abs_example = validate_response(question = '[Was the response correct? (Y/N):] \n',
		possible_responses = ['Y','N'])
	if abs_example == 'N':
		print('[PROMPT:] Tell me another category to which these items belong to. \n')
		abs_example = validate_response(question = '[Was the response correct? (Y/N):] \n',
			possible_responses = ['Y','N'])
		if abs_example == 'N':
			print('Yes, and they also both belong to the category Fruits. \n\
[NO additional instructions or clarifications are given.] \n')
		else:
			print('Yes, both items are part of the category Fruits. \n')
	else: 
		print('Yes, both items are part of the category Fruits. \n')

	# First question in abstraction session.
	input('Now, A TRAIN AND A BICYCLE. What category do they belong to? \n')
	print('[ACCEPTABLE RESPONSES: means of transportation / means of travelling / you take trips in both \n\
UNACCEPTABLE RESPONSES: they have wheels] \n')
	abs_1_resp = validate_response(question = '[Was the response correct? (Y/N):] \n',
		possible_responses = ['Y','N'])
	if abs_1_resp == 'N':
		abs_prompt = validate_response(question = '[Was a prompt given in the example? (Y/N)] \n',
			possible_responses = ['Y','N'])
		if  abs_prompt == 'N':
			print('[PROMPT:] Tell me another category to which these items belong to. \n')
			abs_1_resp = validate_response(question = '[Was the response correct? (Y/N):] \n',
			possible_responses = ['Y','N'])
			if abs_1_resp == 'N':
				abs_1_score = validate_response(question = '[Input 0 for incorrect response; NO additional instructions or clarifications are given:] \n',
					possible_responses = ['0'])
			else:
				abs_1_score = validate_response(question = '[Input 1 for correct response:] \n',
					possible_responses = ['1'])
		else:
			abs_1_score = validate_response(question = '[Input 0 for incorrect response; NO additional instructions or clarifications are given:] \n',
					possible_responses = ['0'])
	else:
		abs_1_score = validate_response(question = '[Input 1 for correct response:] \n',
			possible_responses = ['1'])

	# Second question in abstraction session.
	input('Now, A RULER AND A WATCH. What category do they belong to? \n')
	print('[ACCEPTABLE RESPONSES: measuring instruments / used to measure \n\
UNACCEPTABLE RESPONSES: they have numbers] \n')
	abs_2_resp = validate_response(question = '[Was the response correct? (Y/N):] \n',
		possible_responses = ['Y','N'])
	if abs_2_resp == 'N':
		abs_prompt = validate_response(question = '[Was a prompt given before? (Y/N)] \n',
			possible_responses = ['Y','N'])
		if  abs_prompt == 'N':
			print('[PROMPT:] Tell me another category to which these items belong to. \n')
			abs_2_resp = validate_response(question = '[Was the response correct? (Y/N): \n]',
			possible_responses = ['Y','N'])
			if abs_2_resp == 'N':
				abs_2_score = validate_response(question = '[Input 0 for incorrect response; NO additional instructions or clarifications are given:] \n',
					possible_responses = ['0'])
			else:
				abs_2_score = validate_response(question = '[Input 1 for correct response:] \n',
					possible_responses = ['1'])
		else:
			abs_2_score = validate_response(question = '[Input 0 for incorrect response; NO additional instructions or clarifications are given:] \n',
					possible_responses = ['0'])
	else:
		abs_2_score = validate_response(question = '[Input 1 for correct response:] \n',
			possible_responses = ['1'])

	print('----[END OF ABSTRACTION TEST]---- \n\n')

	# Add up scores obtained from the Abstraction session.
	abs_score = float(abs_1_score) + float(abs_2_score)
	return(abs_score)

def delayed_recall():
	input('--[DELAYED RECALL TEST] \n')
	print('--[Read the following instructions to the participant.] \n')
	input('I read some words to you earlier, which I asked you to remember. \n\
Now please tell me as many of those words as you can remember. \n')
	input('--[MEMORY WORDS LIST: face velvet church daisy red] \n')
	delayed_recall_no_cue = validate_response(question = '[How many words did the participant successfully recall *WITHOUT ANY CUES*? \n\
Allocate 1 point for each word:] \n',
		possible_responses = ['0','1','2','3','4','5'])
	# if delayed_recall_no_cue != '5':
		# print('[Which word(s) was not recalled?')
		# Need to add the cues algorithms
	# else:
		# print('Perfect!')
		
	print('----[END OF DELAYED_RECALL TEST]---- \n\n')

	return(float(delayed_recall_no_cue))

	

def orientation():
	input('--[ORIENTATION TEST] \n')
	print('--[Read the following instructions to the participant.] \n')
	input("Now, close your eyes, and tell me *TODAY'S DATE*, *DAY OF THE WEEK*, *MONTH*, and *YEAR*. \n")
	ori_date = validate_response(question = '[Allocate 1 point for each item correctly answered:] \n',
		possible_responses = ['0','1','2','3','4'])
	input('From what institution am I calling you from? \n')
	ori_place = validate_response(question = '[Input 1 for correct response, 0 for incorrect response:] \n',
		possible_responses = ['0','1'])
	input('What is the city in which our institution is located? \n')
	ori_city = validate_response(question = '[Input 1 for correct response, 0 for incorrect response:] \n',
		possible_responses = ['0','1'])
	ori_score = float(ori_date) + float(ori_place) + float(ori_city)
	return(ori_score)

	print('----[END OF ABSTRACTION TEST]---- \n\n')



# output dictionary
output_scores = {}


# Run the moca and add scores to the dictionry
memory()
output_scores['attention'] = [attention()]
output_scores['language'] = [language()]
output_scores['abstraction'] = [abstraction()]
output_scores['delayed_recall'] = [delayed_recall()]
output_scores['orientation'] = [orientation()]


# convert dictionary to data frame
output_df = pd.DataFrame(output_scores)
output_df['total_score'] = output_df.attention + output_df.language + output_df.abstraction + output_df.delayed_recall + output_df.orientation

# Print scores
print(output_df)

# write participant T-MOCA scores to csv file in their folder
output_df.to_csv(f'../raw_data/{subid}/{subid}_tmoca.csv', index = False)

# Print decision
if output_df.total_score[0] >= 16:
	print('include participant')
else:
	print('Exclude participant')

