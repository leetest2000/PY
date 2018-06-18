from jinja2 import Environment, FileSystemLoader

#This line uses the current directory called 'templates'
file_loader = FileSystemLoader('templates')

env = Environment(loader=file_loader)
#template file
template = env.get_template('template_conf.txt')
variable = 'VARIABLE!!'
#replace contents in template with {{}} variables 
output = template.render(local_asn = '22223', var = variable)

#Print the output
print(output)
