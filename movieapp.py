import requests

def get_jobs_table(html_text, table_id):
	"""Returns table (string) from html_text passed, where table id matches table_id"""
	try:
		#Find table id "job-opportunity"
		table_start = html_text.find('<table id="%s">' % (table_id))
		#Find end of table
		table_end =  html_text.find('</table', table_start)
		return html_text[table_start : table_end]
	except Exception, e:
		#print 'Exception in get_jobs_table:', e
		return

def get_jobs_table_rows(table_body):
	"""Returns rows (list) from table_body passed"""
	rows = []
	row_start = 0
	while row_start >= 0:
		row_start = table_body.find('<tr>', row_start)
		row_end = table_body.find('</tr>', row_start)
		rows.append(table_body[row_start : row_end])
		row_start = row_end
	return rows

def print_jobs(table_rows, base_url):
	"""Prints job title, url and location in JSON format from table_rows passed"""
	jobs = '{"jobs" : ['
	for row in table_rows:
		try:
			jobs += '\n\t{"title" : "%s", \n\t"url : "%s", \n\t"location" : "%s"}, ' %  (row.split('<td>')[1].split('</td>')[0].split('<a href="')[1].split('">')[1].split('</a>')[0],
													base_url + row.split('<td>')[1].split('</td>')[0].split('<a href="')[1].split('">')[0],
													row.split('<td>')[4].split('</td>')[0])
		except Exception, e:
			#print 'Exception in print_positions:', e
			continue
	print jobs[:-2] + ']}'

def main():
	"""Pretty-prints the titles, URLs, and locations of each job to standard output in JSON format
	from the second page of job listings on the site https://www.besmith.com/candidates/search"""
	base_url = 'https://www.besmith.com'
	search_url = 'https://www.besmith.com/candidates/search'
	search_page = {'page' : 1} 
	#Get second page of job listings of URL
	r = requests.get(search_url, params=search_page)
	#Get html text from response
	html_text = r.text
	#Get the jobs table from html text with specific id
	table_id = 'job-opportunity'
	table_body = get_jobs_table(html_text, table_id)
	#Get all the rows from the jobs table
	table_rows = get_jobs_table_rows(table_body)
	#Print job positions in JSON format to standard output
	print_jobs(table_rows, base_url)

if __name__ == '__main__':
	main()