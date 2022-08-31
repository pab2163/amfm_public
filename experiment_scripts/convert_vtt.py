import pandas as pd
import sys
import re

'''
3 command line args:

1 - filepath to vtt file (raw from zoom)
2 - experimenter name (first name before spaces as it appears in zoom transcript)
3 - how many space-separated words are in the experimenter name (in the zoom transcript)
'''

file = sys.argv[1]
experimenter_name = sys.argv[2]
experimenter_length = int(sys.argv[3])

# put together subid / ses from filename
subid = file.split('_')[0]
ses = file.split('_')[1].replace('ses', '')


opened_file = open(file,encoding='utf8')
content = opened_file.read()
segments = content.split('\n\n') #SPLIT ON DOUBLE NEWLINE, IMPORTANT

#CLEAN SEGMENTS
m = re.compile(r"\<.*?\>")#Strips unwanted tags
o = re.compile(r"\.+\d+")#Strips miliseconds

def clean(content):    
	new_content = m.sub('',content)
	new_content = o.sub('',new_content)
	new_content = new_content.replace('align:start position:0%','')
	new_content = new_content.replace('-->','')
	return new_content

new_segments = [clean(s) for s in segments if len(s)!=0][2:]

#TRIM TIME CODES
def clean_time(time):
	time = time.split(':')
	if time[0]=='00':
		return time[1]+':'+time[2]
	if not time[0]=='00':
		return time[0]+':'+time[1]+':'+time[2]

trimmed_segments = []
data_list = []
for segment in new_segments:
	split_segment = segment.split()
	time_code = split_segment[0] 
	if split_segment[3] not in [experimenter_name, 'PARTICIPANT:']:
		split_segment.insert(3, 'UNKNOWN')

	if split_segment[3] == experimenter_name:
		# if experimenter zoom name has a space within it
		text_string = ' '.join(split_segment[3+experimenter_length:])

	else:
		text_string = ' '.join(split_segment[4:])

	text = ' '.join(segment.split()[2:])
	trimmed_segment = (time_code, text) 
	trimmed_segments.append(trimmed_segment)

	row = pd.DataFrame({'time_code': [split_segment[1]], 'speaker': [split_segment[3]], 'sentence': [text_string]})
	data_list.append(row)


out_data = pd.concat(data_list)
out_data['subid'] = subid
out_data['session'] = ses
out_data['experimenter'] = experimenter_name
out_data[['event', 'trial', 'exclude_trial', 
		  'exclusion_reason', 'transcriber', 'scorer',
		  'memory_duration', 'probe',
		  'eventDetIn',	'eventDetEx', 'placeDetIn', 'placeDetEx',
		  'timeDetIn',	'timeDetEx', 'percDetIn', 'percDetEx',
		  'emothDetIn' ,'emothDetEx', 'semDet', 'repDet', 
		  'othDet', 'notes_scoring', 'notes_transcribing']] = None

# reorder columns
out_data = out_data[['subid', 'session', 'event', 'trial', 'exclude_trial',
					 'exclusion_reason', 'transcriber', 'scorer', 'memory_duration',
					 'experimenter', 'time_code', 'speaker', 'sentence', 'probe',
					 'eventDetIn',	'eventDetEx', 'placeDetIn', 'placeDetEx',
					 'timeDetIn',	'timeDetEx', 'percDetIn', 'percDetEx',
					 'emothDetIn' ,'emothDetEx', 'semDet', 'repDet', 
					 'othDet', 'notes_scoring', 'notes_transcribing']]

# save out
out_data.to_csv(file.replace('.vtt', '.csv'), index = False)

