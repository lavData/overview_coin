import datetime
import requests
import json
import pandas as pd
import plotly


class overview_coin:
    __API__URL__BASE = "https://api.coingecko.com/api/v3/"
    def __init__(self, api_base_url = __API__URL__BASE):
        self.api_base_utl = api_base_url
        self.timeout = 120
    def __request(self,url):
        respond = requests.get(url, timeout= self.timeout)
        content = json.loads(respond.content.decode('utf-8'))
        return content

    def request_bitcoin(self, id, vs_currency, days):
        api_url = f'{self.api_base_utl}coins/{id}/market_chart?' + \
            f'vs_currency={vs_currency}&days={days}'    
        coin_price = self.__request(api_url)['prices']
        candles = self.im_to_df(coin_price)
        self.draw_plot(candles)
    
    def im_to_df(self, coin_price):
        df = pd.DataFrame(coin_price, columns=["timestap", "price"])
        df['date'] = df['timestap'].apply(lambda d: datetime.date.fromtimestamp(d/1000))
        candles = df.groupby(df.date, as_index= False).agg({'price': ["min", "max", "first", "last"]})
        return candles

    def draw_plot(self, candles):
        fig = plotly.graph_objects.Figure(data=[plotly.graph_objects.Candlestick(x = candles['date'],
                open=candles['price']['first'], 
                high=candles['price']['max'],
                low=candles['price']['min'], 
                close=candles['price']['last'])
                ])

        fig.update_layout(xaxis_rangeslider_visible=False)

        fig.show()
over = overview_coin()
data = over.request_bitcoin('bitcoin','usd', 60)


