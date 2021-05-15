import json
import subprocess

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

############################################################
# Pages for each tab
############################################################

def get_selector(sel_name) : 
    # List of regex options in json format
    # Could this be written to at some point by users?
    rvals   = json.load(open("regex.json","r"))
    is_open = True if 'date' in sel_name.lower() else False
    return [
        html.Hr(),
        html.Div([
        html.H5(children=[sel_name]),
        html.Details([
        html.Summary('Click to expand/collapse'),
        dcc.Checklist(
            id='%s_checklist_vals'%(sel_name.lower()),
            options=rvals[sel_name]
        )],open=is_open),
        ])
    ]

def regex_selector_page() :
    selector_div = [
        html.H4(
            children=['Instructions'],
            style={
                'textAlign': 'left',
                'color': '#404140'
            }
        ),
        html.H6(
            children=['1. Select desired regexes from checklists below, 2. Copy contents of "Regex list" for later use'],
            style={
                'textAlign': 'left',
                'color': '#404140'
            }
        ),
        html.Hr(),

        html.H4(children=['Regex list']),

        html.Div([dcc.Textarea(id='live-update-text',style={
            'width' : '100%',
            'height': '300px',
            'padding': '12px 20px',
            'box-sizing': 'border-box',
            'border': '1px solid',
            'border-radius': '4px',
            'background-color': '#ffffff',
        })]),
    ]
    for pii_type in ['DATE','SUBJID','AGE'] : 
        selector_div.extend(get_selector(pii_type))
    return html.Div(selector_div, className="pretty_container")

def regex_tester_page() :
    return html.Div([
        html.Div([''],style={'padding': '12px 20px'}),
        html.Div([html.Button('Test regex', id='run-button', style = {'background-color':'#1674C8','color':'white','margin-left': '43%'})]),
        html.H5(children=['Test text']),
        html.Div([dcc.Textarea(id='test-text',value='Enter some text here...',style={
            'width' : '63%',
            'height': '300px',
            'padding': '12px 20px',
            'box-sizing': 'border-box',
            'border': '1px solid',
            'border-radius': '4px',
            'background-color': '#ffffff',
            'margin-right' : '22px'
        }),
        dcc.Textarea(id='result-text',style={
            'width' : '35%',
            'height': '300px',
            'padding': '12px 20px',
            'box-sizing': 'border-box',
            'border': '1px solid',
            'border-radius': '4px',
            'background-color': '#f8f8f8',
        })]),

        html.H5(children=['Regex list']),
        html.Div([dcc.Textarea(id='regex-text',style={
            'width' : '100%',
            'height': '300px',
            'padding': '12px 20px',
            'box-sizing': 'border-box',
            'border': '1px solid',
            'border-radius': '4px',
            'background-color': '#ffffff',
        })]),

    ],className="pretty_container")

############################################################
# Main function
############################################################

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.H2(children=['Regex tester'],style={'textAlign': 'center','color': '#404140'}),
        dcc.Tabs(id="tabs-example", parent_className='custom-tabs', className='custom-tabs-container',children=[
            dcc.Tab(label='Regex selector', children = [regex_selector_page()], className='custom-tab', selected_className='custom-tab--selected'), 
            dcc.Tab(label='Regex tester', children = [regex_tester_page()], className='custom-tab', selected_className='custom-tab--selected')
    #     ]),
        ]),
    html.Div(id='tabs-content-example', style = {'align-items': 'center', 'justify-content': 'center'})
    ])
])

# #############################################################
# # Callback for updating regex list dynamically
# #############################################################

@app.callback(Output('live-update-text', 'value'),
              [Input('%s_checklist_vals'%(pii_type), 'value') for pii_type in ['date','subjid','age']]
              )
def update_text(values_date,values_subjid,values_age) :
    sout = ''
    if values_date is not None and len(values_date)>0 : 
        sout += 'Type: DATE\n'
        sout += '\n'.join(values_date)
        sout += '\n'
    if values_subjid is not None and len(values_subjid)>0 :
        sout += 'Type: SUBJID\n'
        sout += '\n'.join(values_subjid)
        sout += '\n'
    if values_age is not None and len(values_age)>0 :
        sout += 'Type: AGE\n'
        sout += '\n'.join(values_age)
        sout += '\n'
    # Get rid of dangling newline
    if sout.endswith("\n") :
        sout = sout[0:-1]
    return sout

#############################################################
# Callback for running regex tester
#############################################################

@app.callback(Output('result-text', 'value'),
              [ Input('run-button', 'n_clicks') ],
              [ State('test-text', 'value'),State('regex-text','value') ])
def run_regex(n_clicks,test_text,regex_text) :

    if n_clicks is None or n_clicks==0 :
        return 'Results will appear here ...'

    sout = ''

    rsplit = []
    if regex_text is not None : 
        rsplit = regex_text.split("\n")

    if n_clicks is not None and n_clicks>0 :
        for ir in rsplit :
            if ir == '' :
                continue
            if ir.startswith("Type:") :
                sout += ir+"\n"
                continue
            results = subprocess.check_output(["./run_regex.sh",test_text,ir]).decode().split("\n")
            print(results)
            if len(results)>0 and results[0] != '' :
                for res in results :
                    sout += res.replace("[1] ","")+"\n"
            else :
                sout += "No matches found!\n"

    sout = sout.replace("\n\n","\n")
    return sout

#############################################################
# MAIN ROUTINE
#############################################################

if __name__ == '__main__':
    app.run_server(debug=True)
