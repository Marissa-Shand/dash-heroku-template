import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

article1 = 'In ["The narrowing, but persistent, gender gap in pay"](https://www.pewresearch.org/fact-tank/2019/03/22/gender-pay-gap-facts/) article by Nikki Graf, Anna Brown and Eileen Patten, they claim that the gender wage gap has decreased about 50% since 1980. This is in large part because educational attainment made by women since 1980 has increased dramatically and they are breaking glass ceilings.'

article2 = 'In ["What is the generder pay gap and is it real?"](https://www.epi.org/publication/what-is-the-gender-pay-gap-and-is-it-real/#epi-toc-29) by Elise Gould, Jessica Schieder, and Kathleen Geier, they discuss different aspects of the gender wage gap including how education and occupational characteristics affect this gap. They found that at each level of educational attainment, women make less than men on average. Additionally, they found that there exists a gender wage gap within and between industries and occupations. This means that within the same industry, women make less than men on average, and across industries, female dominated fields pay less than male dominated fields. This may be because men are more likely to pursue careers in the STEM field which are often associated with higher salaries. However, they found that in industries where there are unions, there tends to be a smaller wage gap between men and women.'

## Create a table that has the mean values for men and women rounded to 2 decimal places
table_sex = gss_clean.groupby('sex')[['income', 'job_prestige', 'socioeconomic_index', 'education']].mean().round(2)

## Reset the index so we have sex as a column
table_sex = table_sex.reset_index()

## Use more presentable column names
table_sex.columns = ['Sex', 'Avg. Income', 'Avg. Occupational Prestige', 'Avg. Socioeconomic Status', 'Avg. Years of Education']

## Format the table in an interactive and web-enabled way
table_sex = ff.create_table(table_sex)

## Produce a crosstab between sex and male_breadwinner to show levels of agreement
gss_breadwinner = pd.crosstab(gss_clean.sex, gss_clean.male_breadwinner).reset_index()

## Melt the data frame to turn male_breadwinner into a column
gss_breadwinner = pd.melt(gss_breadwinner, id_vars = 'sex', value_vars = ['strongly agree', 'agree', 'disagree', 'strongly disagree'])

## Create an interactive barplot
fig_bar = px.bar(gss_breadwinner, x = 'male_breadwinner', y = 'value', color = 'sex',
            labels = {'male_breadwinner': 'Opinion on Male as the Breadwinner', 'value': 'Frequency of Responses'},
            barmode = 'group',
            color_discrete_map = {'male':'green', 'female':'mediumpurple'})
fig_bar.update_layout(showlegend = True)
fig_bar.update(layout = dict(title = dict(x = 0.5)))
fig_bar.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Create an interactive scatterplot
fig_scatter = px.scatter(gss_clean, x = 'job_prestige', y = 'income', color = 'sex',
                 trendline = 'ols',
                 labels = {'job_prestige': 'Occupational Prestige', 'income': 'Income', 'sex': 'Sex'},
                 hover_data = ['education', 'socioeconomic_index'],
                 color_discrete_map = {'male':'green', 'female':'mediumpurple'})
fig_scatter.update(layout = dict(title = dict(x = 0.5)))
fig_scatter.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Create an interactive box plot for income of men and women
fig_box_income = px.box(gss_clean, x = 'income', y = 'sex', color = 'sex',
             labels = {'income': 'Income', 'sex': ''},
             color_discrete_map = {'male':'green', 'female':'mediumpurple'},
                       height = 400)
fig_box_income.update_layout(showlegend = False)
fig_box_income.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Create an interactive box plot for education of men and women
fig_box_educ = px.box(gss_clean, x = 'education', y = 'sex', color = 'sex',
             labels = {'education': 'Years of Education', 'sex': ''},
             color_discrete_map = {'male':'green', 'female':'mediumpurple'},
                     height = 400)
fig_box_educ.update_layout(showlegend = False)
fig_box_educ.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Create an interactive box plot for job_prestige of men and women
fig_box_prestige = px.box(gss_clean, x = 'job_prestige', y = 'sex', color = 'sex',
             labels = {'job_prestige': 'Occupational Prestige', 'sex': ''},
             color_discrete_map = {'male':'green', 'female':'mediumpurple'},
                         height = 400)
fig_box_prestige.update_layout(showlegend = False)
fig_box_prestige.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Create a new dataframe that contains only income, sex, and job_prestige
gss_facet = gss_clean[['income', 'sex', 'job_prestige']]

## Create a new feature in this dataframe that breaks job_prestige into sex categories with equally sized ranges
gss_facet['prestige_bins'] = pd.cut(gss_facet['job_prestige'], bins = 6)

## Drop all rows with any missing values in this dataframe
gss_facet.dropna(inplace = True)

## Create a facet grid
fig_box_facet = px.box(gss_facet, x = 'income', y = 'sex', color = 'sex',
              facet_col = 'prestige_bins', facet_col_wrap = 2,
              color_discrete_map = {'male':'green', 'female':'mediumpurple'},
              labels = {'income': 'Income', 'sex': ''})
fig_box_facet.update_layout(showlegend = False)
fig_box_facet.for_each_annotation(lambda a: a.update(text = a.text.replace("prestige_bins=", "")))
fig_box_facet.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')

## Options for interative bar plot
options1 = gss_clean[['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']]
options2 = gss_clean[['sex', 'region', 'education']]

## There are so many levels of education, let's limit this
options2.education = options2.education.astype('category')
options2 = options2.assign(education = pd.cut(gss_clean['education'],
                                                bins = [-0.1, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 100.0],
                                                labels = ('10 years or fewer', '11 years', '12 years', '13 years', '14 years', '15 years', '16 years', 'More than 16 years')))



app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        
        html.H2("Exploring the 2019 General Social Survey"),
        
        dcc.Markdown(children = article1),
        
        dcc.Markdown(children = article2),
        
        html.H3("Comparing Average Social Metric Scores Between Men and Women"),
        
        dcc.Graph(figure = table_sex),
        
        html.H3("Bar Graph of Different Social Metric Scores"),
        
        html.Div([
            
            html.H4("x-axis feature"),
            
            dcc.Dropdown(id='x-axis',
                         options=[{'label': i, 'value': i} for i in options1],
                         value='male_breadwinner'),
            
            html.H4("colors"),
            
            dcc.Dropdown(id='color',
                         options=[{'label': i, 'value': i} for i in options2],
                         value = 'sex')
        
        ], style={'height': 500, 'width': '25%', 'float': 'left'}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),
        
        html.H3("Income v. Occupational Prestige by Sex"),
        
        dcc.Graph(figure=fig_scatter),
        
        html.Div([
            
            html.H3("Distribution of Income by Sex"),
            
            dcc.Graph(figure=fig_box_income),
            
            dcc.Markdown(children = 'Looking at these graphs, we can see that men have higher salaries than women. We want to investigate whether this difference is due to the fact that men have jobs with higher occupational prestige than women or if they have a higher educational attaintment than women. Looking at the distribution of educational attainment by sex, we can see that the range of values is very similar for both men and women, but women have a higher median educational attainment than women. Looking at the distribution of occupational pretsige by sex we can see that the range of occupational prestige is about the same for both men and women, but the median occupational prestige is slightly higher for women than men. The 75th percentile is about the same for men and women, however, the 25th percentile is lower for women than men, this will lead to men and women having roughly the same average occupational prestige. These graphs shows that the difference in salaries for men and women is not due to the fact that men have jobs with higher occupational prestige than women or because men have more years of education, but something else.'),
            
        ], style = {'height': 1000, 'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H3("Distribution of Education by Sex"),
            
            dcc.Graph(figure=fig_box_educ),
            
            html.H3("Distribution of Job Prestige by Sex"),
            
            dcc.Graph(figure=fig_box_prestige),
            
        ], style = {'height': 1000, 'width':'48%', 'float':'right'}),
        
        html.H3("Distribution of Income for Different Levels of Job Prestige by Sex"),
        
        dcc.Graph(figure=fig_box_facet)
        
    ], style={'background-color':'rgb(173, 164, 195)'}
)

@app.callback(Output(component_id="graph",component_property="figure"),
             [Input(component_id='x-axis',component_property="value"),
              Input(component_id='color',component_property="value")])

def make_figure(x, color):
    ## There are different levels of x
    ## {'very dissatisfied', 'a little dissat', 'mod. satisfied', 'very satisfied'} = satjob
    if x in ['satjob']:
        bar = px.bar(
            pd.melt(pd.crosstab(options2[color], options1[x]).reset_index(), id_vars = color, value_vars = ['very dissatisfied', 'a little dissat', 'mod. satisfied', 'very satisfied']),
            x = x, y = 'value', color = color,
            labels = {x : x, 'value' : 'Frequency of Responses'},
            barmode = 'group')
    
    ## {'strongly disagree', 'disagree', 'agree', 'strongly agree'} = relationship, male_breadwinner, child_suffer
    elif x in ['relationship', 'male_breadwinner', 'child_suffer']:
        bar = px.bar(
            pd.melt(pd.crosstab(options2[color], options1[x]).reset_index(), id_vars = color, value_vars = ['strongly disagree', 'disagree', 'agree', 'strongly agree']),
            x = x, y = 'value', color = color,
            labels = {x : x, 'value' : 'Frequency of Responses'},
            barmode = 'group')    
    
    ## {'disagree', 'agree'} = men_bettersuited
    elif x in ['men_bettersuited']:
        bar = px.bar(
            pd.melt(pd.crosstab(options2[color], options1[x]).reset_index(), id_vars = color, value_vars = ['disagree', 'agree']),
            x = x, y = 'value', color = color,
            labels = {x : x, 'value' : 'Frequency of Responses'},
            barmode = 'group')
        
    ## {'strongly disagree', 'disagree', 'neither agree nor disagree', 'agree', 'strongly agree'} = men_overwork
    else:
        bar = px.bar(
            pd.melt(pd.crosstab(options2[color], options1[x]).reset_index(), id_vars = color, value_vars = ['strongly disagree', 'disagree', 'neither agree nor disagree', 'agree', 'strongly agree']),
            x = x, y = 'value', color = color,
            labels = {x : x, 'value' : 'Frequency of Responses'},
            barmode = 'group')    
    
    bar.update_layout(paper_bgcolor = 'rgb(173, 164, 195)')
    return bar

if __name__ == '__main__':
    app.run_server(debug=True, port=8046)
