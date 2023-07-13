import requests


def weather_message_36h():
    req = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-454EF92F-4FB5-443B-B662-9642724A2BDD&format=JSON&locationName=%E6%96%B0%E7%AB%B9%E7%B8%A3&elementName=',
            headers = {'accept': 'application/json'})
    weather_json = req.json()
    weather = weather_json['records']['location'][0]['weatherElement']
    weather_msg = ''
    for i in range(3):
        msg = td_or_tmr(weather_json, i)+day_or_night(weather_json, i)+'-天氣狀況:'+ weather[0]['time'][i]['parameter']['parameterName'] +'；'
        msg+='降雨機率:'+ weather[1]['time'][i]['parameter']['parameterName']+'%；'
        msg+='最低氣溫:'+weather[2]['time'][i]['parameter']['parameterName']+'攝氏度；最高氣溫:'+weather[4]['time'][i]['parameter']['parameterName']+'攝氏度；'
        msg+='體感舒適度:'+weather[3]['time'][i]['parameter']['parameterName']+'。'
        weather_msg+=msg
    return weather_msg


def day_or_night(json, index):
    if (str(json['records']['location'][0]['weatherElement'][4]['time'][index]['startTime'])[-8:]=='06:00:00'):
        return '白天'
    elif (str(json['records']['location'][0]['weatherElement'][4]['time'][index]['startTime'])[-8:]=='12:00:00'):
        return '下午'
    elif (str(json['records']['location'][0]['weatherElement'][4]['time'][index]['startTime'])[-8:]=='00:00:00'):
        return '凌晨'
    else:
        return '晚上'

def td_or_tmr(json, index):
    if index==0:
        return '今天'
    elif index==1 and day_or_night(json, index)!='白天':
        return '今天'
    else:
        return '明天'
    
def get_am_or_pm(hour):
    if hour <=3:
        return '凌晨'
    elif hour <12:
        return '上午'
    elif hour==12:
        return '中午'
    elif hour<18:
        return '下午'
    else:
        return '晚上'
    
def get_hour(hour):
    if hour <=12:
        return hour
    else:
        return hour-12
    
def get_date_time_message():
    get_time = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=Asia/Taipei')
    time = get_time.json()
    out = '今天是民國'+ str(time['year']-1911)+ '年'+ str(time['month'])+'月'+str(time['day'])+'日，'+time['dayOfWeek']+'。現在時間是'+ get_am_or_pm(time['hour'])+ str(get_hour(time['hour']))+'點'+ str(time['minute'])+'分'
    return out
