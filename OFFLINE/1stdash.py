from flask import Flask, render_template, url_for, request, redirect, flash
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)

server.secret_key = "1stDashAPP"


from sqlalchemy.orm import sessionmaker, relationship

# # this part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
meta = MetaData()
engine = create_engine("postgresql://postgres:161086@localhost/test-db-02", echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# database here
class FlightNum(Base):
	__tablename__ = 'flight_num'
	id = Column('id', Integer, primary_key=True)
	city = Column('city', String(20))
	amount = Column('amount', Integer)

	def __init__(self, city, amount):
		self.city = city
		self.amount = amount

Session = sessionmaker(bind=engine)
db_session = Session()

@server.route('/')
def index():
    return render_template("home.html")



@server.route('/cities', methods=['GET', 'POST'])
def cities():
	place = request.form.get("place")
	people = request.form.get("people")
	# '''
	# input data into database to load graph.  Flask jinja does NOT work
	# request.form.get("...") does not work.
	# You can only make single entries into database
	# '''
	if request.method == 'GET':	
		return render_template('cities.html')
	else:
		# Add entries into database. 
		db_data = FlightNum(place, people)
		db_session.add(db_data)
		db_session.commit()
		flash(f'your entry has been logged! CITY:{place} PEOPLE:{people}')
		return render_template('cities.html')

	


def sf_data():
	# get all the numbers from san fran
    city_data = db_session.query(FlightNum).filter(FlightNum.city=="sf").all()
    return [s.amount for s in city_data]


def mont_data():
	# get all numbers from montreal
	city_data = db_session.query(FlightNum).filter(FlightNum.city=="montreal").all()
	return ([s.amount for s in city_data])


def leng_sf():
	# list length of entries in sf
    city_data = db_session.query(FlightNum).filter(FlightNum.city=="sf").all()
    return list(range(len([s.amount for s in city_data])))

def leng_mont():
	# list length of entries in sf
    city_data = db_session.query(FlightNum).filter(FlightNum.city=="montreal").all()
    return list(range(len([s.amount for s in city_data])))



@server.route('/test_sf')
def test_sf():
	return f"{sf_data()}"

@server.route('/test_mont')
def test_mont():
	return f"{mont_data()}"	

@server.route('/len_sf')
def len_sf():
	return f"{leng_sf()}"

# dash graph
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': leng_sf(), 'y': sf_data(), 'type': 'bar', 'name': 'SF'},
                {'x': leng_mont(), 'y': mont_data(), 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)