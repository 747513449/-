# coding=utf-8
import json
import time
import requests

#sit 域名
#url_head ='http://oss.oasit.com/'

#prd域名
url_head = 'http://oss-api.oa.com/'

def get_time_now():
    '''获取当前时间戳'''
    time_now = time.time()
    time_now = int(time_now)
    return  time_now

def get_companycode():
    ''' 获取机构code '''
    #sit 请求格式
    #url = url_head + 'config/get?key=yypt.base.company_list'

    #prd 请求格式
    url = url_head + 'config/get?key=sys.yypt.base.company_list'

    response = requests.get(url)
    js = response.json()
    company_length = len(js['companyList'])
    company_code_list=[]
    #print company_length
    #循环list，提取companycode
    for i in range(company_length):
        company_code_list.append(js['companyList'][i]['companyCode'])
        i=i+1
    return company_code_list
# get_companycode(companylist_url)


def check_company_code(companycode):
        result = '''<tr><td rowspan='4'>%s</td>''' %companycode
        return result

def get_company_gift(companycode, projecttype=1):
    ''' 获取机构礼品 ,车主服务A方案 '''
    gift_url = url_head + 'v1/offerService/GetGiftInfo'
    post_data={
    "body":{
        "companyCode":companycode,
        "productCode":"PC01",
        "giftType": 2,
        "projectType":projecttype
    },
    "head":{
        "randNum":"9527",
        "timestamp":"4654857500",
        "accessId":"carinsure-dataflow-customtagchecker",
        "clientCode":"123456",
        "requestId":"carinsure-dataflow-customtagchecker",
        "signature":"49ce6a257c0bc1c05292f5197542badd"
    }
}
    response = requests.post(gift_url,data=json.dumps(post_data))
    js = response.json()
    #print js["body"]['giftInfoList'][0]['useExplanation']
    return len(js['body']['giftInfoList'])
#get_company_gift('WBOS1440300')

def check_company_gift(companycode):
    '''检查车主服务A方案配置'''
    gift_lenth = get_company_gift(companycode)
    if gift_lenth > 0:
        result = '<td rowspan="4">√</td>'
        return result
    else:
        result = '<td rowspan="4" bgcolor="red">×</td>'
        return result

def get_company_ratio_new(time, companycode, businesstype=2):
    '''获取机构代理费率'''
    ratio_url = url_head + 'v1/rebateService/GetRebateRatioNew'
    post_data ={
    "head":{
        "accessId":"0db098384fa74cadb5e1acd521a3f1a3",
        "requestId":"e4d04028f29beaac",
        "clientCode":"data",
        "timestamp":time,
        "randNum":"5990482929064819019",
        "signature":"8d2e1e3c358d532bd77cb64a0c948dd085abe7ea"
    },
    "body":{
        "attributedCompanyCode":companycode,
        "credentialType":"01",
        "credentialNo":"testNo",
        "businessType":businesstype,
        "reckonedLossRatio":0.9,
        "riskList":[
            {
                "riskCode":"PCR01",
                "customTagCode":""
            },
            {
                "riskCode":"PCR02",
                "customTagCode":""
            }
        ]
    }
}
    response = requests.post(ratio_url,data=json.dumps(post_data))
    js = response.json()
    #商业险代理费率
    pcr01_ratio_new = js['body']['expenseList'][0]['expenseSettingKey']
    #交强险代理费率
    pcr02_ratio_new = js['body']['expenseList'][1]['expenseSettingKey']
    #返利分桶
    pcr01_ratio_old = js['body']['expenseList'][0]['partitionName']
    pcr02_ratio_old = js['body']['expenseList'][1]['partitionName']
    return pcr01_ratio_new, pcr02_ratio_new,pcr01_ratio_old,pcr02_ratio_old



def check_company_ratio_new(companycode,businesstype):
    '''检查代理费率配置'''
    time = str(get_time_now())
    result_ratio = get_company_ratio_new(time, companycode,businesstype)
    name = {1:'新保',2:'续保',3:'脱保',4:'转保'}
    result=[]
    #返回不同续保类型结果
    #商业险代理费率
    if result_ratio[0] !='':
        result.append('<td> %s :√</td>' %(name[businesstype]) )
    else:
        result.append('<td bgcolor="red"> %s:×</td>'  %(name[businesstype]))

    #交强险代理费率
    if result_ratio[1] !='':
        result.append('<td> %s:√</td>'  %(name[businesstype]))
    else:
        result.append('<td bgcolor="red"> %s:×</td>'  %(name[businesstype]))

    #交商同保返利分桶
    if result_ratio[2] !='' and result_ratio[3] !='':
        result.append('<td> %s:√</td>'  %(name[businesstype]))
    else:
        result.append('<td bgcolor="red"> %s:×</td>'  %(name[businesstype]))
    return  result



def get_company_ratio_old(time, companycode,businesstype,riskcode ):
    '''获取机构返利分桶'''
    ratio_url = url_head + 'v1/rebateService/GetRebateRatioNew'
    post_data ={
    "head":{
        "accessId":"0db098384fa74cadb5e1acd521a3f1a3",
        "requestId":"e4d04028f29beaac",
        "clientCode":"data",
        "timestamp":time,
        "randNum":"5990482929064819019",
        "signature":"8d2e1e3c358d532bd77cb64a0c948dd085abe7ea"
    },
    "body":{
        "attributedCompanyCode":companycode,
        "credentialType":"01",
        "credentialNo":"testNo",
        "businessType":businesstype,
        "reckonedLossRatio":0.9,
        "riskList":[
            {
                "riskCode":riskcode,
                "customTagCode":""
            }
        ]
    }
}
    response = requests.post(ratio_url,data=json.dumps(post_data))
    js = response.json()
    #代理费率
    result = js['body']['expenseList'][0]['partitionName']
    return result


def check_company_ratio_old(companycode, businesstype, riskcode):
    '''检查代理费率配置'''
    time = str(get_time_now())
    result_ratio = get_company_ratio_old(time, companycode, businesstype, riskcode)
    name = {1:'新保',2:'续保',3:'脱保',4:'转保'}
    #单险返利分桶
    if result_ratio !='':
        result = ('<td> %s:√</td>' %(name[businesstype]))
    else:
        result = ('<td bgcolor="red"> %s:×</td>'  %((name[businesstype])))
    return result


def get_company_mch(companycode):
    '''获取机构商户号ID'''
    mch_url = url_head + 'config/get?key=sys.yypt.base.company_product_mch.PC01.1.2.'+companycode
    try:
        response = requests.get(mch_url)
        js =  response.json()
        mch = js['mchId']
        return  mch
    except Exception, e:
        print e


def pack_html(path):
    '''HTML组装'''
    html_start = '''<!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
    </head>
    <style>
    body {
        background-color: #ffffff;
        font-size: 14px;
        color: #000;
        font-weight: 500;
    }
    table {
      border-collapse: collapse;
      border-spacing: 0;
      margin-bottom: 20px;
      font-size:14px;
    }
    th{
        background-color: #CCCCCC;
        vertical-align: bottom;
        border-bottom: 2px solid #000;
    }
    th,td {
      border: 1px solid #000 !important;
      padding: 20px 50px 0 20px;
      border-top: 1px solid #000;
    }

    </style>
    <body>
    <div  style="position:relative">
        <div style="margin:20px 0 0 20px;">
            <p > Hi,All:</p>
            <p style="margin-left:30px;"> OSS-PRD 配置监控结果</p>
            <p style="margin-left:30px;"><span style='color:red'> 标红提示部分，请@产品同学检查配置</span></p>
            <table style="margin-left:30px;">
                <tr>
                    <th style="width:120px"; rowspan='2'>机构代码</th>
                    <th style="width:100px;" rowspan='2'>车主服务(A)</th>
                    <th style="width:160px;"; colspan="2">代理费率</th>
                    <th style="width:160px;"; colspan="3">返利分桶</th>
                </tr>
                <tr>                
                    <td>代理费率(商）</td>
                    <td>代理费率(交）</td>
                   	<td>交商同保     </td>
                   	<td>单保商业险   </td>
                   	<td>单保交强险   </td>
                </tr>'''
    html_end = '''</table>
        <p style="margin-left:30px;"> *注：判断逻辑如下</p>
        <p style="margin-left:30px;">   1.车主服务：返回礼品列表≥1  </p>
        <p style="margin-left:30px;">   2.代理费率：返回费用代码key值≠空  </p>
        <p style="margin-left:30px;">   3.返利分桶：返利ABC分桶≠空  </p>                
        </br>
        </br>
    </div>
</body>
</html>'''
	t_start = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
	print '---------------------------------------------start:%s' %t_start
    riskcode=['PCR01','PCR02']
    result = []
    result.append(html_start)
    company_list=get_companycode()
    # HTML 根据机构代码组装结果
    for i in range(len(company_list)):
        companycode = company_list[i]
        result_companycode = check_company_code(companycode)
        result_gift = check_company_gift(companycode)
        result_ratio_new = check_company_ratio_new(companycode,1)
        result_ratio_pcr01 = check_company_ratio_old(companycode, 1, riskcode[0])
        result_ratio_pcr02 = check_company_ratio_old(companycode, 1, riskcode[1])
        #数据第一行合并
        result.append(result_companycode)
        result.append(result_gift)
        result.append(result_ratio_new[0])
        result.append(result_ratio_new[1])
        result.append(result_ratio_new[2])
        result.append(result_ratio_pcr01)
        result.append(result_ratio_pcr02)
        result.append('</tr>')
        #返利配置合并
        for k in range(2,5):
            result_ratio_new = check_company_ratio_new(companycode,k)
            result.append('<tr>')
            result.append(result_ratio_new[0])
            result.append(result_ratio_new[1])
            result.append(result_ratio_new[2])
            # 返利分桶合并
            for i in riskcode:
                result_ratio_old = check_company_ratio_old(companycode,k,i)
                result.append(result_ratio_old)
            result.append('</tr>')
        print '%s is done' %companycode
	t_end = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    result.append(html_end)
    filename = path +'//'+ t_end + 'result.html'
    f = open(filename,'w')
    f.writelines(result)
	print '---------------------------------------------end:%s' %t_end	
    f.close()
    print 'Finish'

