import json
import subprocess

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# List of regex options in json format
# Is there a better, more dynamical way to load this?
rvals = json.load(open("regex.json","r"))

############################################################
# Pages for each tab
############################################################

def regex_selector_page() :
    return html.Div([
        html.H4(
            children=['Instructions'],
            style={
                'textAlign': 'left',
                'color': '#404140'
            }
        ),
        html.H6(
            children=['1. Select desired regexes from checklist, 2. Click "Generate regex", 3. Copy results into regex file'],
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
            'background-color': '#f8f8f8',
        })]),

        html.Hr(),

        html.H5(children=['DATE']),

        dcc.Checklist(
            id='date_checklist_vals',
            options=rvals['DATE']
        ),
        html.Hr(),

        html.H5(children=['SUBJID']),

        dcc.Checklist(
            id='subjid_checklist_vals',
            options=rvals['SUBJID']
        ),
        html.Hr()
    ])

def regex_tester_page() :
    return html.Div([
        html.Div([''],style={'padding': '12px 20px'}),
        html.Div([html.Button('Run tester', id='run-button',style = {'margin-left': '43%'})]),
        # html.Div([html.H5(children=['Testing text'])],className="two columns"),
        # html.Div([html.H5(children=['Results'])],className="two columns"),
        # html.Div([''],style={'padding': '12px 20px'}),
        html.H5(children=['Test text']),
        html.Div([dcc.Textarea(id='test-text',style={
            'width' : '50%',
            'height': '300px',
            'padding': '12px 20px',
            'box-sizing': 'border-box',
            'border': '1px solid',
            'border-radius': '4px',
            'background-color': '#f8f8f8',
        }),
        dcc.Textarea(id='result-text',style={
            'width' : '50%',
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
            'background-color': '#f8f8f8',
        })]),

    ])

############################################################
# Main function
############################################################

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
    html.Img(src=app.get_asset_url('IQVIA-Privacy-Analytics-Logo-rgb.png'),style={
        'maxWidth': '20%',
        'maxHeight': '20%',
        'marginLeft': 'auto',
        'marginRight': 'auto'})
    ],
    style = {'textAlign':'center'}
    ),
    html.H1(
        children=['CTT DOCS regex tools'],
        style={
            'textAlign': 'center',
            'color': '#404140'
        },
    ),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Regex selector', children = [regex_selector_page()]), # value='tab-1-example'),
        dcc.Tab(label='Regex tester', children = [regex_tester_page()]) # value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
],style = {'align-items': 'center', 'justify-content': 'center'})

#############################################################
# Callback for updating regex list dynamically
#############################################################

@app.callback(Output('live-update-text', 'value'),
              [Input('date_checklist_vals', 'value'),Input('subjid_checklist_vals', 'value')]
              )
def update_text(values_date,values_subjid) :
    sout = ''
    if values_date is not None and len(values_date)>0 : 
        sout += 'Type: DATE\n'
        sout += '\n'.join(values_date)
        sout += '\n'
    if values_subjid is not None and len(values_subjid)>0 :
        sout += 'Type: SUBJID\n'
        sout += '\n'.join(values_subjid)
        sout += '\n'
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

    return sout

#############################################################
# MAIN ROUTINE
#############################################################

if __name__ == '__main__':
    app.run_server(debug=True)
