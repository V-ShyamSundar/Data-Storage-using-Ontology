from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

# Create an RDF graph
g = Graph()

# Define namespaces
college = Namespace("http://example.org/college/")
schema = Namespace("http://schema.org/")

# Define classes
g.add((college.Department, RDF.type, RDFS.Class))
g.add((college.Undergraduate, RDF.type, RDFS.Class))
g.add((college.Postgraduate, RDF.type, RDFS.Class))
g.add((college.BE, RDF.type, RDFS.Class))
g.add((college.BTech, RDF.type, RDFS.Class))
g.add((college.ME, RDF.type, RDFS.Class))

# Define subclasses
g.add((college.BE, RDFS.subClassOf, college.Undergraduate))
g.add((college.BTech, RDFS.subClassOf, college.Undergraduate))
g.add((college.ME, RDFS.subClassOf, college.Postgraduate))

# Add labels to classes
g.add((college.Department, RDFS.label, Literal("Department")))
g.add((college.Undergraduate, RDFS.label, Literal("Undergraduate")))
g.add((college.Postgraduate, RDFS.label, Literal("Postgraduate")))
g.add((college.BE, RDFS.label, Literal("Bachelor of Engineering (B.E.)")))
g.add((college.BTech, RDFS.label, Literal("Bachelor of Technology (B.Tech.)")))
g.add((college.ME, RDFS.label, Literal("Master of Engineering (M.E.)")))

# Add information about the college
college_uri = URIRef(college + "Vel_Tech_Multi_Tech")
g.add((college_uri, RDF.type, schema.College))
g.add((college_uri, schema.name, Literal("Vel Tech Multi Tech Dr. Rangarajan Dr. Sakunthala Engineering College")))
g.add((college_uri, schema.description, Literal(
    '''Vel Tech Multi Tech Dr. Rangarajan Dr. Sakunthala Engineering College, An Autonomous Institution, has been accredited by NAAC 
    in the year 2016 with ‘A’ Grade and with an impressive score of 3.49 / 4.0. The Institution stands among the top 200 Institutions 
    in NIRF India Ranking consecutively for three years in a row. Vel Tech Multi Tech is the first Self Financing Affiliated Institution 
    to bag Diamond rating in maximum categories in QS – IGAUGE Indian College and University Ranking. Our Institution excels as one of the 
    top premiere institutes in India owing to its State of the art Infrastructure, well equipped laboratories, and highly qualified 
    and experienced faculty members.'''
)))

# Define fee property
g.add((college.hasFee, RDF.type, RDF.Property))
g.add((college.hasFee, RDFS.label, Literal("has fee")))

# Add departments and courses
departments = [
    {"name": "B.E. Bio Medical Engineering", "short": "BME", "level": "BE", "fee": 75000},
    {"name": "B.E. Computer Science and Engineering", "short": "CSE", "level": "BE", "fee": 107000},
    {"name": "B.E. Computer Science and Engineering [Cyber Security]", "short": "CSE-Cyber", "level": "BE", "fee": 107000},
    {"name": "B.E. Electronics and Communication Engineering", "short": "ECE", "level": "BE", "fee": 107000},
    {"name": "B.E. Electrical and Electronics Engineering", "short": "EEE", "level": "BE", "fee": 75000},
    {"name": "B.E. Mechanical Engineering", "short": "MECH", "level": "BE", "fee": 107000},
    {"name": "B.Tech. Artificial Intelligence and Data Science", "short": "AIDS", "level": "BTech", "fee": 107000},
    {"name": "B.Tech. Computer Science and Business Systems", "short": "CSBS", "level": "BTech", "fee": 107000},
    {"name": "B.Tech. Information Technology", "short": "IT", "level": "BTech", "fee": 107000},
    {"name": "M.E. VLSI Design", "short": "VLSI", "level": "ME", "fee": None},
    {"name": "M.E. Embedded System Technologies", "short": "Embedded", "level": "ME", "fee": None}
]

for dept in departments:
    dept_uri = URIRef(college + dept["short"])
    g.add((dept_uri, RDF.type, college.Course))
    g.add((dept_uri, RDFS.label, Literal(dept["name"])))
    level_uri = URIRef(college + dept["level"])
    g.add((dept_uri, RDFS.subClassOf, level_uri))
    g.add((college_uri, college.hasDepartment, dept_uri))
    if dept["fee"]:
        g.add((dept_uri, college.hasFee, Literal(dept["fee"])))

# Add key personnel
personnel = [
    {"name": "DR. V. RAJAMANI", "role": "Principal"},
    {"name": "DR. A. KARTHIKEYAN", "role": "Vice Principal"},
    {"name": "DR. K A. HARISH", "role": "Planning Incharge"},
    {"name": "DR. G. SASI", "role": "HoD", "department": "BME"},
    {"name": "MR. M. SELVAM", "role": "HoD", "department": "MECH"},
    {"name": "MR. R. PRABU", "role": "HoD", "department": "IT"},
    {"name": "DR. V. PRABHU", "role": "HoD", "department": "ECE"},
    {"name": "DR. K. IMMANUVEL AROKIA JAMES", "role": "HoD", "department": "AIDS"},
    {"name": "DR. K. IMMANUVEL AROKIA JAMES", "role": "HoD", "department": "CSBS"}
]

for person in personnel:
    person_uri = URIRef(college + person["name"].replace(" ", "_").replace(".", ""))
    g.add((person_uri, RDF.type, college.Professor))
    g.add((person_uri, RDFS.label, Literal(person["name"])))
    if person["role"] == "Principal":
        g.add((person_uri, RDF.type, college.Principal))
        g.add((college_uri, schema.headOf, person_uri))
    elif person["role"] == "Vice Principal":
        g.add((person_uri, RDF.type, college.VicePrincipal))
        g.add((college_uri, schema.vice, person_uri))
    elif person["role"] == "Planning Incharge":
        g.add((person_uri, RDF.type, college.Planning))
        g.add((college_uri, schema.plan, person_uri))
    elif person["role"] == "HoD":
        dept_uri = URIRef(college + person["department"])
        g.add((person_uri, college.headOf, dept_uri))

# Serialize the RDF graph to a file
g.serialize(destination="vel_tech_onto.ttl", format="turtle")

print("Ontology generated successfully!")
