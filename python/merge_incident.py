#!/usr/local/bin/python



if __name__ == '__main__':

	import sys

	# [ Sprout Unit ]
	# Primary key:	
	#   1. incident_id;
	# Attributes:	
	# - TAG 1: 
	#   2. cad_call_type, 3. call_type, 4. location, 5. avg_lat, 
	#   6. avg_long, 7. city, 8. command_area, 
	# - TAG 2:
	#   9. reporting_dst, 10. shift, 11. occur_date, 12. occur_time,
	#   13. how_committed
	# - TAG 3:
	#   14. remarks

	last_incident_id = '-1'
	last_tag         = '-1'

	for line in sys.stdin:
		data = line.strip().split('\t')
		if len(data) <= 2:
			print data
			continue
		incident_id = data[0]
		tag         = data[1]

		# Process data by incident id
		if incident_id != last_incident_id:
			print '\t'.join([
				incident_id, incident_date, cad_call_type, call_type, \
				location, avg_lat, avg_long, city, command_area, reporting_dst, \
				shift, occur_date, occur_time, how_committed, remarks \
			])
			remarks = ''

		# Process data by tag
		try:
			if tag == '1':
				incident_date = data[2]
				cad_call_type = data[3]
				call_type     = data[4]
				location      = data[5]
				avg_lat       = data[6]
				avg_long      = data[7]
				city          = data[8]
				command_area  = data[9]
				# shift         = data[10]
			elif tag == '2':
				# location      = data[2]
				# city          = data[3]
				reporting_dst = data[4]
				# command_area  = data[5]
				shift         = data[6]
				occur_date    = data[7]
				occur_time    = data[8]
				how_committed = data[9]
			elif tag == '3':
				if remarks != '':
					remarks += '\2'
				remarks += data[2]
		except:
			print >> sys.stderr, line

		last_incident_id = incident_id