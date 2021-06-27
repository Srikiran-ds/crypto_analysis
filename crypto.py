#from collections import namedtuple
#import altair as alt
import math
import pandas as pd
import streamlit as st
import plotly
#from pycoingecko import CoinGeckoAPI
import datetime
import plotly.express as px
#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')

def aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    #customize gridOptions
    #gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

    #gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

    #gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
    #gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
    gb.configure_column("market_caps", type=[ "customCurrencyFormat"], custom_currency_symbol="$")

    #configures last row to use custom styles based on cell's value, injecting JsCode on components front end


    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    #Display the grid
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        #height=grid_height, 
        width='100%',
        #data_return_mode=return_mode_value, 
        #update_mode=update_mode_value,
        #fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        )

    df = grid_response['data']
    #selected = grid_response['selected_rows']
    #selected_df = pd.DataFrame(selected)

st.title("Crypto Analysis")
st.write('___')
st.write('')

'''
cg = CoinGeckoAPI()
#data=cg.get_coin_market_chart_range_by_id()
id_list=pd.DataFrame(cg.get_coins_list(include_platform=False))

#st.write(id_list)

#lst=['AvalancheAVAX',	'SafeMoonSAFEMOON',	'Huobi TokenHT',	'BitTorrentBTT',	'The GraphGRT',	'Hedera HashgraphHBAR',	'THORChainRUNE',	'DecredDCR',	'KusamaKSM',	'TrueUSDTUSD',	'WavesWAVES',	'Huobi BTCHBTC',	'SushiSUSHI',	'DashDASH',	'ChilizCHZ',	'CompoundCOMP',	'TelcoinTEL',	'ZcashZEC',	'ElrondEGLD',	'QuantQNT',	'yearn.financeYFI',	'HoloHOT',	'Lido Staked EtherSTETH',	'NEMXEM',	'HeliumHNT',	'Synthetix Network TokenSNX',	'Enjin CoinENJ',	'Paxos StandardPAX',	'ZilliqaZIL',	'MdexMDX',	'NearNEAR',	'Basic Attention TokenBAT',	'Liquity USDLUSD',	'XDC NetworkXDC',	'NEXONEXO',	'Bitcoin GoldBTG',	'StacksSTX',	'HorizenZEN',	'HUSDHUSD',	'Bancor Network TokenBNT',	'DecentralandMANA',	'QtumQTUM',	'HarmonyONE',	'NanoNANO',	'DigiByteDGB',	'cUSDTCUSDT',	'KuCoin TokenKCS',	'FantomFTM',	'OntologyONT',	'Pirate ChainARRR']
#lst=['AVAX',	'SAFEMOON',	'HT',	'BTT',	'HBAR',	'RUNE',	'GRT',	'DCR',	'KSM',	'TUSD',	'WAVES',	'HBTC',	'SUSHI',	'DASH',	'CHZ',	'COMP',	'TEL',	'ZEC',	'EGLD',	'QNT',	'YFI',	'HOT',	'STETH',	'XEM',	'HNT',	'SNX',	'ENJ',	'PAX',	'ZIL',	'MDX',	'NEAR',	'BAT',	'LUSD',	'XDC',	'NEXO',	'BTG',	'STX',	'ZEN',	'HUSD',	'BNT',	'MANA',	'QTUM',	'ONE',	'NANO',	'DGB',	'CUSDT',	'KCS',	'FTM',	'ONT',	'ARRR']

lst=['avalanche',	'safemoon',	'huobi token',	'bittorrent',	'hedera hashgraph',	'thorchain',	'the graph',	'decred',	'kusama',	'trueusd',	'waves',	'huobi btc',	'sushi',	'dash',	'chiliz',	'compound',	'telcoin',	'zcash',	'elrond',	'quant',	'yearn.finance',	'holo',	'lido staked ether',	'nem',	'helium',	'synthetix network token',	'enjin coin',	'paxos standard',	'zilliqa',	'mdex',	'near',	'basic attention token',	'liquity usd',	'xdc network',	'nexo',	'bitcoin gold',	'stacks',	'horizen',	'husd',	'bancor network token',	'decentraland',	'qtum',	'harmony',	'nano',	'digibyte',	'cusdt',	'kucoin token',	'fantom',	'ontology',	'pirate chain',	'ARRR']
id_list['name']=id_list['name'].str.lower()
id_list=id_list[id_list['name'].isin(lst)]
#st.write(id_list)
#id_list=id_list.head()

#dataset=pd.DataFrame(cg.get_coin_market_chart_range_by_id(id='decentraland',vs_currency='usd', from_timestamp='1616598000',to_timestamp='1624633200'))

#dataset=pd.DataFrame(cg.get_coin_market_chart_range_by_id(ids=list(id_list['id']),vs_currencies='usd',days=91))
#st.write(dataset)
dataset_main=pd.DataFrame()
dataset_main['id']=''
dataset_main['prices']=''
dataset_main['market_caps']=''
dataset_main['total_volumes']=''
#,'prices','market_caps','total_volumes']
for i in range(id_list.shape[0]):
    #st.write(list(id_list['id'])[i])
    try:
        dataset=pd.DataFrame(cg.get_coin_market_chart_range_by_id(id=list(id_list['id'])[i],vs_currency='usd', from_timestamp='1616598000',to_timestamp='1624633200'))
        dataset['id']=list(id_list['id'])[i]
        dataset=dataset[['id','prices','market_caps','total_volumes']]
#dataset=pd.DataFrame(cg.get_coin_market_chart_range_by_id(ids=list(id_list['id']),vs_currencies='usd',days=91))
        #st.write(dataset)
        dataset_main=dataset_main.append(dataset)

    except:
        pass

'''
dataset_main=pd.read_csv('dataset_main.csv',header=True)
dataset_main['date']=dataset_main['prices'].apply(lambda x: int(str(x[0])[:10]))

#st.write(dataset_main['date'])
#st.write(datetime.datetime.fromtimestamp(1616630400))1616630400
#dataset_main['new_date'] = pd.to_datetime(dataset_main['date'],unit='D',errors='coerce')
dataset_main['new_date']=dataset_main['date'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
#,format='%Y%m%d')
dataset_main['prices']=dataset_main['prices'].apply(lambda x: x[1])
dataset_main['market_caps']=dataset_main['market_caps'].apply(lambda x: x[1])
dataset_main['total_volumes']=dataset_main['total_volumes'].apply(lambda x: x[1])
#st.write(dataset_main['prices'].apply(lambda x: x[1]))
#st.write(dataset_main['date'].min(),dataset_main['date'].max())
#st.write('1616598000','1624633200')
#st.write(dataset_main)
#st.write(dataset_main.dtypes)

dataset_main['new_date']= pd.to_datetime(dataset_main['new_date'])
my_expander = st.beta_expander(label='Expand to view data')
with my_expander:

    #clicked = st.button('Click me!')
    #aggrid(dataset_main)
    st.write(dataset_main)

my_expander2 = st.beta_expander(label='Expand to Methodology')
with my_expander2:

    #clicked = st.button('Click me!')
    st.subheader('Methodology:')
    st.write('->Data was fetched from coingecko using API')
    st.write('->Cryptos with ranking between 51 and 100 on coingecko were filtered out for analysis')
    st.write('->Timeperiod of analysis is last 90 days')
    st.write('->A huge dip was seen on almost all of them on May 20,2021. So, analysis was done for phase1(until May 20), phase2(after May 20) and also across timeperiod')
    st.write('->Ranking was given based on the average day on day growth along with discounting out cryptos which had more day on day drops were more compared to rise')
    st.write('->And then cryptos with higher day on day peaks were given better rank')

df_lag=dataset_main[['new_date','id','market_caps']]
df_lag_org=df_lag
#st.write(df_lag)
df_lag = df_lag.set_index(["new_date", "id"]) # index
df_lag = df_lag.unstack().shift(1)          # pull out the groups, shift with lag step=1
df_lag= df_lag.stack(dropna=True)      # stack the groups back, keep the missing values
df_lag.reset_index().sort_values("id")
#st.write(df_lag)
df_lag=pd.merge(df_lag_org,df_lag,on=['new_date','id'],how='inner')
#st.write(df_lag)
df_lag['change']=((df_lag['market_caps_x']-df_lag['market_caps_y'])/df_lag['market_caps_y'])*100
#st.write(df_lag)
#df_lag['change']=df_lag['change'].apply(lambda x: min(max(x,-200),200))
df_lag['flag']=df_lag['change'].apply(lambda x: 1 if x>0 else -1)
#st.write(df_lag)  
df_lag_phase1=df_lag[df_lag['new_date']<='20210519']
df_lag_phase2=df_lag[df_lag['new_date']>='20210521']
#st.write(df_lag_phase1)
#st.write(df_lag_phase2)

df_lag_rank1=df_lag_phase1.groupby(['id'])['change','flag'].mean().sort_values(['change'],ascending=False)
#st.write(df_lag_rank)  
df_lag_rank1=df_lag_rank1.loc[df_lag_rank1['flag']>0,:].reset_index()
#st.write(df_lag_rank)


df_lag_rank2=df_lag_phase2.groupby(['id'])['change','flag'].mean().sort_values(['change'],ascending=False)
#st.write(df_lag_rank)  
df_lag_rank2=df_lag_rank2.loc[df_lag_rank2['flag']>0,:].reset_index()
#st.write(df_lag_rank)

df_lag_rank=df_lag.groupby(['id'])['change','flag'].mean().sort_values(['change'],ascending=False)
#st.write(df_lag_rank)  
df_lag_rank=df_lag_rank.loc[df_lag_rank['flag']>0,:].reset_index()
#st.write(df_lag_rank)



#st.write(dataset_main)

st.header('')
st.write('___')
max=st.number_input("Top :",3)


dataset_main1=dataset_main[dataset_main['new_date']<='20210519']
dataset_main2=dataset_main[dataset_main['new_date']>='20210521']
dataset_main_subset1=pd.merge(df_lag_rank1.loc[:max-1,'id'],dataset_main1,on=['id'],how='left')
dataset_main_subset2=pd.merge(df_lag_rank2.loc[:max-1,'id'],dataset_main2,on=['id'],how='left')
dataset_main_subset=pd.merge(df_lag_rank.loc[:max-1,'id'],dataset_main,on=['id'],how='left')



df_ts=dataset_main_subset1.pivot(index="new_date", columns="id", values="market_caps")

df = df_ts.reset_index()


#st.write(df)
col1, col2 = st.beta_columns(2)

fig1 = px.line(df, x="new_date", y=df.columns,
              hover_data={"new_date": "|%B %d, %Y"},
              title='Phase1 Market Cap(2021/03/25-2021/05/19)')
fig1.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
#fig.show()
fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(title_text='Market Cap($)')
col1.plotly_chart(fig1)
#st.write(df)




df_ts=dataset_main_subset2.pivot(index="new_date", columns="id", values="market_caps")

df = df_ts.reset_index()


#st.write(df)


fig2 = px.line(df, x="new_date", y=df.columns,
              hover_data={"new_date": "|%B %d, %Y"},
              title='Phase2 Market Cap(2021/05/20-2021/06/27)')
fig2.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
#fig.show()
fig2.update_xaxes(title_text='Date')
fig2.update_yaxes(title_text='Market Cap($)')
col2.plotly_chart(fig2)
#st.write(df)
col3, col4 = st.beta_columns(2)

df_lag_rank1=df_lag_rank1.loc[:max-1,['id','change']]
df_lag_rank1.columns=['Crypto ID', 'Avg daily change(%)']
df_lag_rank2=df_lag_rank2.loc[:max-1,['id','change']]
df_lag_rank2.columns=['Crypto ID', 'Avg daily change(%)']

col3.write(df_lag_rank1)
col4.write(df_lag_rank2)

st.header('')

df_ts=dataset_main_subset.pivot(index="new_date", columns="id", values="market_caps")

df = df_ts.reset_index()


#st.write(df)


fig = px.line(df, x="new_date", y=df.columns,
              hover_data={"new_date": "|%B %d, %Y"},
              title='Overall Market Cap(2021/03/25-2021/06/27)',height=500,width=1200)
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
#fig.show()
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Market Cap($)')
st.plotly_chart(fig)

df_lag_rank=df_lag_rank.loc[:max-1,['id','change']]
df_lag_rank.columns=['Crypto ID', 'Avg daily change(%)']

st.write(df_lag_rank)



    
